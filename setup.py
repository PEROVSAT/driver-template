#!/usr/bin/env python3
"""Bootstrap a PerovSat Zephyr driver repository from this template.

Usage:
  python3 setup.py
"""

from __future__ import annotations

import os
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

USE_COLOR = not os.environ.get("NO_COLOR") and sys.stdout.isatty()

# ANSI styles (disabled when USE_COLOR is false).
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RED = "\033[31m"


def style(text: str, *codes: str) -> str:
    if not USE_COLOR:
        return text
    return "".join(codes) + text + RESET


def step(message: str) -> None:
    print(f"\n{style('==>', BOLD, GREEN)} {style(message, BOLD)}")


def note(message: str) -> None:
    for line in message.splitlines():
        print(f"  {style(line, DIM, BLUE)}")


def info(message: str) -> None:
    print(f"  {style(message, DIM)}")


def success(message: str) -> None:
    print(f"  {style(message, GREEN)}")


def warn(message: str) -> None:
    print(f"  {style(message, RED)}")


def show_prompt_help(name: str, description: str | None = None,
                     examples: str | None = None) -> None:
    print(f"  {style(name, BOLD, CYAN)}")
    if description:
        print(f"  {style(description, DIM)}")
    if examples:
        print(f"  {style(f'e.g. {examples}', YELLOW)}")


def prompt(name: str, default: str | None = None, description: str | None = None,
           examples: str | None = None, validator=None) -> str:
    show_prompt_help(name, description, examples)
    while True:
        suffix = style(f" [{default}]", DIM) if default else ""
        answer = input(f"  {style(name, BOLD, CYAN)}{suffix}: ").strip()
        value = answer or default
        if value is None:
            warn("Value is required.")
            continue
        if validator and not validator(value):
            warn("Invalid value, try again.")
            continue
        print()
        return value


def normalize_compat_part(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "_", value)


def module_name(chip: str, mode: str) -> str:
    return f"{chip}-mock-driver" if mode == "mock" else f"{chip}-driver"


def gather() -> tuple[str, str, str, str]:
    note(
        "Name the repository after the physical device, not a logical role like IMU.\n"
        "Map logical roles in perovsat-app."
    )
    print()

    chip = prompt(
        "device-model",
        description="Lowercase slug used in filenames, C symbols, and devicetree compatible",
        examples="mpu6050",
        validator=lambda v: bool(SLUG_RE.match(v)),
    ).lower()
    vendor = prompt(
        "devicetree-vendor",
        description="Vendor prefix in compatible strings (not zephyr)",
        examples="invensense",
        validator=lambda v: bool(VENDOR_RE.match(v)),
    )
    mode = prompt(
        "driver-variant",
        default="hardware",
        description="Real device driver or static test-data mock",
        examples="hardware, mock",
        validator=lambda v: v in VALID_MODES,
    )
    subsys = prompt(
        "zephyr-subsystem",
        default="sensor",
        description="Driver subdirectory under drivers/",
        examples="sensor, gpio",
        validator=lambda v: bool(SLUG_RE.match(v)),
    )

    return mode, vendor, chip, subsys


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
            print(f"  {style(str(dest.relative_to(ROOT)), DIM)}")

    success(f"Rendered {file_count} files from template/{mode}/ and template/common/")


def finalize_readme() -> None:
    driver_readme = ROOT / "README.driver.md"
    if driver_readme.exists():
        driver_readme.replace(ROOT / "README.md")
        success("Promoted README.driver.md to README.md")


def cleanup_template() -> None:
    shutil.rmtree(TEMPLATE)
    Path(__file__).unlink(missing_ok=True)
    info("Removed template/ and setup.py")


def get_git_remotes() -> dict[str, str]:
    git_dir = ROOT / ".git"
    if not git_dir.exists():
        return {}

    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return {}

    remotes: dict[str, str] = {}
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[2] == "(fetch)":
            remotes[parts[0]] = parts[1]
    return remotes


def restore_git_remotes(remotes: dict[str, str]) -> None:
    for name, url in remotes.items():
        subprocess.run(["git", "remote", "add", name, url], cwd=ROOT, check=True)
        print(f"  {style('Restored remote', DIM)} {style(name, CYAN)}: {style(url, DIM)}")


def remove_git_metadata() -> None:
    git_dir = ROOT / ".git"
    if not git_dir.exists():
        return

    info("Removing existing .git metadata")
    if git_dir.is_file():
        git_dir.unlink()
    else:
        shutil.rmtree(git_dir)


def init_fresh_git() -> None:
    git_dir = ROOT / ".git"
    if find_workspace_root() is not None and git_dir.exists():
        success("Preserving existing git repository (west workspace)")
        return

    remotes = get_git_remotes()
    remove_git_metadata()

    subprocess.run(["git", "init"], cwd=ROOT, check=True)
    success("Initialized fresh git repository")

    if remotes:
        info("Restoring git remotes")
        restore_git_remotes(remotes)


def ensure_python_packages(packages: tuple[str, ...] = REQUIRED_PYTHON_PACKAGES) -> None:
    if not packages:
        return

    info(f"Installing: {', '.join(packages)}")
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
        info(f"Skipping {repo} (not a git repository)")
        return
    if not (repo / ".pre-commit-config.yaml").is_file():
        return

    info(f"Installing pre-commit hooks in {repo}")
    subprocess.run(["pre-commit", "install"], cwd=repo, check=True)


def install_perovsat_pre_commit_hooks() -> None:
    workspace = find_workspace_root()
    if workspace is None:
        install_pre_commit_in_repo(ROOT)
        return

    info(f"Found west workspace at {workspace}")
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

    print(style("PerovSat driver template setup", BOLD))
    info(f"Working directory: {ROOT}")

    step("Collecting driver configuration")
    mode, vendor, chip, subsys = gather()
    module = module_name(chip, mode)
    print()
    info(f"device-model={style(chip, CYAN)}, vendor={style(vendor, CYAN)}, "
         f"variant={style(mode, YELLOW)}")
    info(f"subsys={style(subsys, CYAN)}, module={style(module, CYAN)}")
    tokens = build_tokens(mode, vendor, chip, subsys, module)

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
    print(f"  {style('Module:', BOLD)} {style(tokens['__MODULE_NAME__'], CYAN)}")
    print(f"  {style('Mode:', BOLD)}   {style(tokens['__MODE__'], YELLOW)}")
    note("Next: wire the new driver into perovsat-app (see README.md)")


if __name__ == "__main__":
    main()
