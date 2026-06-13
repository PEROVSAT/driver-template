#!/usr/bin/env python3
"""Bootstrap a PerovSat Zephyr driver repository from this template.

Usage:
  python3 setup.py
"""

from __future__ import annotations

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
PEROVSAT_GITHUB_ORG = "github.com/PEROVSAT"
SKIP_PRE_COMMIT_PROJECTS = frozenset({"imu-driver", "imu-mock-driver"})
REQUIRED_PYTHON_PACKAGES = ("pre-commit",)


def step(message: str) -> None:
    print(f"\n==> {message}")


def normalize_compat_part(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "_", value)


def prompt(label: str, default: str | None = None, hint: str | None = None,
           validator=None) -> str:
    if hint:
        print(f"  {hint}")
    while True:
        suffix = f" [{default}]" if default else ""
        answer = input(f"{label}{suffix}: ").strip()
        value = answer or default
        if value is None:
            print("  Value is required.")
            continue
        if validator and not validator(value):
            print("  Invalid value, try again.")
            continue
        return value


def gather() -> tuple[str, str, str, str, str]:
    print("  Name the repository after the physical device (e.g. mpu6050), not a")
    print("  logical role like IMU. Map logical roles in perovsat-app.")

    chip = prompt(
        "Chip identifier",
        hint="Lowercase slug used in filenames, C symbols, and devicetree compatible",
        validator=lambda v: bool(SLUG_RE.match(v)),
    ).lower()
    vendor = prompt(
        "Devicetree vendor prefix",
        hint="Vendor in compatible strings, e.g. invensense (not zephyr)",
        validator=lambda v: bool(VENDOR_RE.match(v)),
    )
    mode = prompt(
        "Driver variant",
        "hardware",
        hint="hardware = real device driver, mock = static test data driver",
        validator=lambda v: v in VALID_MODES,
    )
    subsys = prompt(
        "Zephyr subsystem",
        "sensor",
        hint="Driver subdirectory under drivers/, e.g. sensor or gpio",
        validator=lambda v: bool(SLUG_RE.match(v)),
    )

    default_module = f"{chip}-mock-driver" if mode == "mock" else f"{chip}-driver"
    module = prompt(
        "West module name",
        default_module,
        hint="Repository and west project name",
    )

    return mode, vendor, chip, subsys, module


def build_tokens(mode: str, vendor: str, chip: str, subsys: str,
                 module: str) -> dict[str, str]:
    compat = f"{vendor},{chip}" + ("-mock" if mode == "mock" else "")
    driver_upper = normalize_compat_part(chip).upper()
    dt_compat = normalize_compat_part(compat).lower()
    dt_has = f"DT_HAS_{normalize_compat_part(compat).upper()}_ENABLED"
    kconfig_sym = f"PEROVSAT_{driver_upper}" + ("_MOCK" if mode == "mock" else "")
    driver_base = chip + ("_mock" if mode == "mock" else "")

    return {
        "__MODULE_NAME__": module,
        "__MODE__": mode,
        "__SUBSYS__": subsys,
        "__VENDOR__": vendor,
        "__DRIVER_SLUG__": chip,
        "__DRIVER_BASE__": driver_base,
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
    file_count = 0

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

            file_count += 1
            print(f"  {dest.relative_to(ROOT)}")

    print(f"  Rendered {file_count} files from template/{mode}/ and template/common/")


def finalize_readme() -> None:
    driver_readme = ROOT / "README.driver.md"
    if driver_readme.exists():
        driver_readme.replace(ROOT / "README.md")
        print("  Promoted README.driver.md to README.md")


def cleanup_template() -> None:
    shutil.rmtree(TEMPLATE)
    Path(__file__).unlink(missing_ok=True)
    print("  Removed template/ and setup.py")


def init_fresh_git() -> None:
    git_dir = ROOT / ".git"
    if git_dir.exists():
        print("  Removing existing .git directory")
        shutil.rmtree(git_dir)

    subprocess.run(["git", "init"], cwd=ROOT, check=True)
    print("  Initialized fresh git repository")


def ensure_python_packages(packages: tuple[str, ...] = REQUIRED_PYTHON_PACKAGES) -> None:
    if not packages:
        return

    print(f"  Installing: {', '.join(packages)}")
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
        print(f"  Skipping {repo} (not a git repository)")
        return
    if not (repo / ".pre-commit-config.yaml").is_file():
        return

    print(f"  Installing pre-commit hooks in {repo}")
    subprocess.run(["pre-commit", "install"], cwd=repo, check=True)


def install_perovsat_pre_commit_hooks() -> None:
    workspace = find_workspace_root()
    if workspace is None:
        install_pre_commit_in_repo(ROOT)
        return

    print(f"  Found west workspace at {workspace}")
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


def main() -> None:
    if not TEMPLATE.is_dir():
        sys.exit("template/ not found. Has this repo already been bootstrapped?")

    print("PerovSat driver template setup")
    print(f"Working directory: {ROOT}")

    step("Collecting driver configuration")
    mode, vendor, chip, subsys, module = gather()
    tokens = build_tokens(mode, vendor, chip, subsys, module)
    print(f"  chip={chip}, vendor={vendor}, variant={mode}")
    print(f"  subsys={subsys}, module={module}")

    step("Rendering template files")
    render_variant(mode, tokens)

    step("Finalizing README")
    finalize_readme()

    step("Cleaning up template files")
    cleanup_template()

    step("Initializing fresh git repository")
    init_fresh_git()

    step("Installing Python dependencies")
    ensure_python_packages()

    step("Installing pre-commit hooks")
    install_perovsat_pre_commit_hooks()

    step("Setup complete")
    print(f"  Module: {tokens['__MODULE_NAME__']}")
    print(f"  Mode:   {tokens['__MODE__']}")
    print("  Next: wire the new driver into perovsat-app (see README.md)")


if __name__ == "__main__":
    main()
