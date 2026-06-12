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
PEROVSAT_GITHUB_ORG = "github.com/PEROVSAT"
SKIP_PRE_COMMIT_PROJECTS = frozenset({"imu-driver", "imu-mock-driver"})
REQUIRED_PYTHON_PACKAGES = ("pre-commit",)
INITIAL_COMMIT_MESSAGE = "Template Clone"


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


def ensure_python_packages(packages: tuple[str, ...] = REQUIRED_PYTHON_PACKAGES) -> None:
    if not packages:
        return

    subprocess.run(
        [sys.executable, "-m", "pip", "install", *packages],
        check=True,
    )


def find_workspace_root() -> Path | None:
    for parent in ROOT.parents:
        if (parent / ".west").is_dir():
            return parent
    return None


def is_perovsat_west_project(name: str, url: str) -> bool:
    if name in SKIP_PRE_COMMIT_PROJECTS:
        return False
    return name == "manifest" or PEROVSAT_GITHUB_ORG in url


def install_pre_commit_in_repo(repo: Path) -> None:
    if not (repo / ".git").is_dir():
        print(f"Skipping {repo} (not a git repository)")
        return
    if not (repo / ".pre-commit-config.yaml").is_file():
        return

    print(f"Installing pre-commit hooks in {repo}")
    subprocess.run(["pre-commit", "install"], cwd=repo, check=True)


def install_perovsat_pre_commit_hooks() -> None:
    workspace = find_workspace_root()
    if workspace is None:
        install_pre_commit_in_repo(ROOT)
        return

    result = subprocess.run(
        ["west", "list", "-f", "{name} {path} {url}"],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=True,
    )

    for line in result.stdout.splitlines():
        if not line.strip():
            continue

        name, rel_path, url = line.split(maxsplit=2)
        if not is_perovsat_west_project(name, url):
            continue

        install_pre_commit_in_repo(workspace / rel_path)

    # The repo we just created may not be listed in west.yml yet.
    install_pre_commit_in_repo(ROOT)


def format_repository() -> None:
    if not (ROOT / ".pre-commit-config.yaml").is_file():
        return

    print("Applying code style checks...")
    subprocess.run(["pre-commit", "run", "--all-files"], cwd=ROOT, check=True)


def create_initial_commit() -> None:
    if not (ROOT / ".git").is_dir():
        return

    format_repository()

    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)

    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=ROOT,
    )
    if staged.returncode == 0:
        print("Nothing to commit.")
        return

    print(f"Creating initial commit ({INITIAL_COMMIT_MESSAGE!r})...")
    result = subprocess.run(
        ["git", "commit", "-m", INITIAL_COMMIT_MESSAGE],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return

    if "Please tell me who you are" in (result.stdout + result.stderr):
        print("Initial commit skipped: git user.name and user.email are not configured.")
        print("Files are formatted and staged. After configuring git, run:")
        print(f'  git commit -m "{INITIAL_COMMIT_MESSAGE}"')
        return

    print(result.stdout, file=sys.stderr)
    print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=VALID_MODES)
    parser.add_argument("--device", help="Logical device name, e.g. IMU")
    parser.add_argument("--vendor", help="Devicetree vendor prefix, e.g. invensense")
    parser.add_argument("--driver", help="Driver slug, e.g. mpu6050")
    parser.add_argument("--subsys", help="Zephyr driver subsystem, default sensor")
    parser.add_argument("--module", help="West module / repository name")
    parser.add_argument("--no-fresh-git", action="store_true",
                        help="Keep existing .git history and skip the initial commit")
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
    ensure_python_packages()
    install_perovsat_pre_commit_hooks()
    if not args.no_fresh_git:
        create_initial_commit()
    print(f"Rendered {tokens['__MODULE_NAME__']} ({tokens['__MODE__']})")


if __name__ == "__main__":
    main()
