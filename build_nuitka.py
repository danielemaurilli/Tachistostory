#!/usr/bin/env python3
"""
Tachistostory – Nuitka Build Script
====================================
Cross-platform build helper that wraps ``python -m nuitka`` with the correct
flags for macOS (.app bundle + DMG), Windows (.exe + ZIP) and Linux (tarball).

Usage examples
--------------
    python build_nuitka.py                 # build for current platform
    python build_nuitka.py --clean         # remove previous build artefacts first
    python build_nuitka.py --help          # show this help

Environment variables
---------------------
    APP_VERSION     Override the version string (default: read from settings.py)
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# ──────────────────────────  project constants  ──────────────────────────── #

ROOT_DIR = Path(__file__).resolve().parent
ENTRY_POINT = ROOT_DIR / "main.py"
ASSETS_DIR = ROOT_DIR / "assets"
DIST_DIR = ROOT_DIR / "dist"

APP_NAME = "Tachistostory"
BUNDLE_ID = "com.danielemaurilli.tachistostory"

# Read version from settings.py or environment
def _get_version() -> str:
    env_ver = os.environ.get("APP_VERSION")
    if env_ver:
        return env_ver
    try:
        settings_path = ROOT_DIR / "settings.py"
        ns: dict = {}
        exec(settings_path.read_text(encoding="utf-8"), ns)  # noqa: S102
        return str(ns.get("APP_VERSION", "0.0.0"))
    except Exception:
        return "0.0.0"

VERSION = _get_version()

# ── platform detection ────────────────────────────────────────────────────── #

IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"
IS_LINUX = sys.platform.startswith("linux")

MACOS_ICON = ASSETS_DIR / "tachistostory_icon.icns"
WINDOWS_ICON = ASSETS_DIR / "tachistostory_icon.ico"

# ── modules configuration ────────────────────────────────────────────────── #

# Packages to include explicitly (Nuitka may miss some dynamic imports)
INCLUDE_PACKAGES = [
    "pygame",
    "docx2txt",
    "src",
    "src.core",
    "src.loaders",
    "src.logging",
    "src.states",
    "src.ui",
    "src.utils",
]

# Modules / packages to exclude (shrink final binary)
NOFOLLOW_MODULES = [
    "pygame.tests",
    "pygame.examples",
    "tkinter",
    "unittest",
    "pydoc",
    "doctest",
    "difflib",
    "numpy",
    "scipy",
    "matplotlib",
    "PIL",
    "pytest",
    "setuptools",
    "pip",
    "pyinstaller",
    "PyInstaller",
]


# ──────────────────────────  build helpers  ──────────────────────────────── #


def _clean(verbose: bool = True) -> None:
    """Remove previous build artefacts."""
    dirs_to_remove = [
        DIST_DIR,
        ROOT_DIR / "main.build",
        ROOT_DIR / "main.dist",
        ROOT_DIR / "main.onefile-build",
    ]
    for d in dirs_to_remove:
        if d.exists():
            if verbose:
                print(f"  🗑  Removing {d}")
            shutil.rmtree(d)


def _build_nuitka_command() -> list[str]:
    """Assemble the ``python -m nuitka`` command line."""

    cmd: list[str] = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--assume-yes-for-downloading-dependency-walker-cache",
        f"--output-dir={DIST_DIR}",
        f"--output-filename={APP_NAME}",
    ]

    # ── include data files (assets/) ──────────────────────────────────── #
    cmd.append(f"--include-data-dir={ASSETS_DIR}=assets")

    # ── include settings.py and game.py alongside main ────────────────── #
    for extra in ("settings.py", "game.py"):
        p = ROOT_DIR / extra
        if p.exists():
            cmd.append(f"--include-data-files={p}={extra}")

    # ── package includes ──────────────────────────────────────────────── #
    for pkg in INCLUDE_PACKAGES:
        cmd.append(f"--include-package={pkg}")

    # ── nofollow (exclude) ────────────────────────────────────────────── #
    for mod in NOFOLLOW_MODULES:
        cmd.append(f"--nofollow-import-to={mod}")

    # ── disable console window on GUI platforms ──────────────────────── #
    if IS_MACOS or IS_WINDOWS:
        cmd.append("--disable-console")

    # ── platform-specific flags ──────────────────────────────────────── #
    if IS_MACOS:
        cmd.append("--macos-create-app-bundle")
        cmd.append(f"--macos-app-name={APP_NAME}")
        cmd.append(f"--macos-app-version={VERSION}")
        if MACOS_ICON.exists():
            cmd.append(f"--macos-app-icon={MACOS_ICON}")
    elif IS_WINDOWS:
        if WINDOWS_ICON.exists():
            cmd.append(f"--windows-icon-from-ico={WINDOWS_ICON}")
        cmd.append(f"--windows-file-description={APP_NAME}")
        cmd.append(f"--windows-product-name={APP_NAME}")
        cmd.append(f"--windows-file-version={VERSION}")
        cmd.append(f"--windows-product-version={VERSION}")
        cmd.append(f"--windows-company-name=Daniele Maurilli")
    elif IS_LINUX:
        if (ASSETS_DIR / "tachistostory_icon.png").exists():
            cmd.append(f"--linux-icon={ASSETS_DIR / 'tachistostory_icon.png'}")

    # ── optimisation ──────────────────────────────────────────────────── #
    cmd.append("--lto=yes")
    cmd.append("--remove-output")

    # ── entry point (must be last) ────────────────────────────────────── #
    cmd.append(str(ENTRY_POINT))

    return cmd


def _run_build(dry_run: bool = False) -> int:
    """Execute the Nuitka build."""
    cmd = _build_nuitka_command()

    print(f"\n{'=' * 60}")
    print(f"  Building {APP_NAME} v{VERSION}")
    print(f"  Platform: {platform.system()} {platform.machine()}")
    print(f"  Python:   {sys.version.split()[0]}")
    print(f"{'=' * 60}\n")

    if dry_run:
        print("Dry-run — command that would be executed:\n")
        print("  " + " \\\n    ".join(cmd))
        return 0

    print("Running Nuitka …\n")
    result = subprocess.run(cmd)
    return result.returncode


# ──────────────────────────  CLI  ────────────────────────────────────────── #


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="build_nuitka.py",
        description=f"Build {APP_NAME} with Nuitka (standalone binary).",
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Remove previous build artefacts before building.",
    )
    parser.add_argument(
        "--clean-only", action="store_true",
        help="Only clean, don't build.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the Nuitka command without executing it.",
    )
    parser.add_argument(
        "--version", action="version",
        version=f"{APP_NAME} build script — app version {VERSION}",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if args.clean or args.clean_only:
        _clean()
        if args.clean_only:
            print("  ✓ Clean complete.")
            return 0

    rc = _run_build(dry_run=args.dry_run)

    if rc == 0:
        print(f"\n  ✓ Build finished.  Output in: {DIST_DIR}\n")
    else:
        print(f"\n  ✗ Build failed (exit code {rc}).\n", file=sys.stderr)

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
