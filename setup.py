#!/usr/bin/env python3
"""Bootstrap a PerovSat Zephyr driver repository from this template.

Usage:
  python3 setup.py
  python3 setup.py --mode mock --device IMU --vendor invensense --driver mpu6050
  python3 setup.py --mode hardware --device IMU --vendor invensense --driver mpu6050 --no-fresh-git
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "template"

VALID_MODES = ("hardware", "mock")
SLUG_RE = re.compile(r"^[a-z][a-z0-9_-]*$")
VENDOR_RE = re.compile(r"^[a-z][a-z0-9_-]*$")
DEVICE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def normalize_compat_part(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "_", value)


def prompt(name: str, default: str | None = None, validator=None) -> str:
    while True:
        suffix = f" [{default}]" if default else ""
        answer = input(f"{name}{suffix}: ").strip()
        value = answer or default
        if value is None:
            print("  Value is required.")
            continue
        if validator and not validator(value):
            print("  Invalid value, try again.")
            continue
        return value


def gather(args: argparse.Namespace) -> tuple[str, str, str, str, str, str]:
    non_interactive = all([args.mode, args.device, args.vendor, args.driver])

    def value(name: str, cli_value: str | None, default: str | None = None,
              validator=None) -> str:
        if cli_value:
            if validator and not validator(cli_value):
                sys.exit(f"Invalid --{name}: {cli_value}")
            return cli_value
        if non_interactive and default is not None:
            return default
        return prompt(name, default, validator)

    mode = value("mode", args.mode, "hardware", lambda v: v in VALID_MODES)
    device = value("device", args.device, validator=lambda v: bool(DEVICE_RE.match(v)))
    vendor = value("vendor", args.vendor, validator=lambda v: bool(VENDOR_RE.match(v)))
    driver = value("driver", args.driver, validator=lambda v: bool(SLUG_RE.match(v))).lower()
    subsys = value("subsys", args.subsys, "sensor", lambda v: bool(SLUG_RE.match(v)))

    default_module = f"{driver}-mock-driver" if mode == "mock" else f"{driver}-driver"
    module = value("module", args.module, default_module)

    return mode, device, vendor, driver, subsys, module


def build_tokens(mode: str, device: str, vendor: str, driver: str, subsys: str,
                 module: str) -> dict[str, str]:
    compat = f"{vendor},{driver}" + ("-mock" if mode == "mock" else "")
    driver_upper = normalize_compat_part(driver).upper()
    dt_compat = normalize_compat_part(compat).lower()
    dt_has = f"DT_HAS_{normalize_compat_part(compat).upper()}_ENABLED"
    kconfig_sym = f"PEROVSAT_{device}" + ("_MOCK" if mode == "mock" else "")

    return {
        "__MODULE_NAME__": module,
        "__DEVICE__": device,
        "__MODE__": mode,
        "__SUBSYS__": subsys,
        "__VENDOR__": vendor,
        "__DRIVER_SLUG__": driver,
        "__DRIVER_UPPER__": driver_upper,
        "__COMPAT__": compat,
        "__DT_COMPAT__": dt_compat,
        "__DT_HAS_ENABLED__": dt_has,
        "__KCONFIG_SYM__": kconfig_sym,
    }


def substitute(text: str, tokens: dict[str, str]) -> str:
    """Replace tokens longest-key-first to avoid partial substitutions."""
    for key in sorted(tokens, key=len, reverse=True):
        text = text.replace(key, tokens[key])
    return text


def render_variant(mode: str, tokens: dict[str, str]) -> None:
    sources = [TEMPLATE / "common", TEMPLATE / mode]
    for src in sources:
        if not src.is_dir():
            sys.exit(f"Missing template directory: {src}")

        for path in sorted(src.rglob("*")):
            if path.is_dir():
                continue

            rel = path.relative_to(src)
            dest = ROOT / substitute(str(rel), tokens)
            dest.parent.mkdir(parents=True, exist_ok=True)

            try:
                dest.write_text(substitute(path.read_text(encoding="utf-8"), tokens),
                                encoding="utf-8")
            except UnicodeDecodeError:
                shutil.copy2(path, dest)


def finalize_readme() -> None:
    driver_readme = ROOT / "README.driver.md"
    if driver_readme.exists():
        driver_readme.replace(ROOT / "README.md")


def cleanup_template() -> None:
    shutil.rmtree(TEMPLATE)
    Path(__file__).unlink(missing_ok=True)


def init_fresh_git(no_fresh_git: bool) -> None:
    if no_fresh_git:
        return

    git_dir = ROOT / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)

    subprocess.run(["git", "init"], cwd=ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=VALID_MODES)
    parser.add_argument("--device", help="Logical device name, e.g. IMU")
    parser.add_argument("--vendor", help="Devicetree vendor prefix, e.g. invensense")
    parser.add_argument("--driver", help="Driver slug, e.g. mpu6050")
    parser.add_argument("--subsys", help="Zephyr driver subsystem, default sensor")
    parser.add_argument("--module", help="West module / repository name")
    parser.add_argument("--no-fresh-git", action="store_true",
                        help="Keep existing .git history instead of re-initializing")
    return parser.parse_args()


def main() -> None:
    if not TEMPLATE.is_dir():
        sys.exit("template/ not found. Has this repo already been bootstrapped?")

    args = parse_args()
    mode, device, vendor, driver, subsys, module = gather(args)
    tokens = build_tokens(mode, device, vendor, driver, subsys, module)

    render_variant(mode, tokens)
    finalize_readme()
    cleanup_template()
    init_fresh_git(args.no_fresh_git)
    print(f"Rendered {tokens['__MODULE_NAME__']} ({tokens['__MODE__']})")


if __name__ == "__main__":
    main()
