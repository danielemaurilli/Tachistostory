#!/usr/bin/env python3
"""
Tachistostory - Nuitka Build Script
Cross-platform build script for Windows and macOS
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Build configuration
APP_NAME = "Tachistostory"
MAIN_SCRIPT = "main.py"
VERSION = "0.2.5"
AUTHOR = "Daniele Maurilli"
DESCRIPTION = "A tachistoscopy application to improve reading"

# Paths
ROOT_DIR = Path(__file__).parent.absolute()
ASSETS_DIR = ROOT_DIR / "assets"
BUILD_DIR = ROOT_DIR / "build_nuitka"
DIST_DIR = ROOT_DIR / "dist_nuitka"

# Icons
WINDOWS_ICON = ASSETS_DIR / "tachistostory.ico"
MACOS_ICON = ASSETS_DIR / "tachistostory.icns"


def get_platform() -> str:
    """Get current platform."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")


def check_nuitka_installed() -> bool:
    """Check if Nuitka is installed."""
    try:
        subprocess.run(
            [sys.executable, "-m", "nuitka", "--version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_nuitka():
    """Install Nuitka and dependencies."""
    print("[*] Installing Nuitka and dependencies...")
    
    packages = [
        "nuitka",
        "ordered-set",  # Performance optimization
        "zstandard",    # Compression support
    ]
    
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade"] + packages,
        check=True
    )
    print("[OK] Nuitka installed successfully!")


def clean_build_dirs():
    """Clean previous build directories."""
    print("[*] Cleaning previous builds...")
    
    for dir_path in [BUILD_DIR, DIST_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
    
    # Clean Nuitka cache
    nuitka_cache = ROOT_DIR / "main.build"
    if nuitka_cache.exists():
        shutil.rmtree(nuitka_cache)
    
    nuitka_dist = ROOT_DIR / "main.dist"
    if nuitka_dist.exists():
        shutil.rmtree(nuitka_dist)
    
    nuitka_onefile = ROOT_DIR / "main.onefile-build"
    if nuitka_onefile.exists():
        shutil.rmtree(nuitka_onefile)
    
    print("[OK] Clean complete!")


def get_base_nuitka_args() -> list:
    """Get base Nuitka arguments common to all platforms."""
    return [
        sys.executable, "-m", "nuitka",
        
        # Compilation mode
        "--standalone",                    # Create standalone distribution
        
        # Output
        f"--output-dir={BUILD_DIR}",
        
        # Include packages (pygame doesn't have a dedicated plugin)
        "--include-package=pygame",
        "--include-package=docx2txt",
        
        # Include pygame data files (fonts, icons, etc.)
        "--include-package-data=pygame",
        
        # Include data files
        f"--include-data-dir={ASSETS_DIR}=assets",
        
        # Optimization
        "--assume-yes-for-downloads",      # Auto-download dependencies
        "--remove-output",                 # Remove previous output
        
        # Show progress
        "--show-progress",
        "--show-memory",
        
        # Main script
        str(ROOT_DIR / MAIN_SCRIPT),
    ]


def get_windows_args() -> list:
    """Get Windows-specific Nuitka arguments."""
    args = [
        # Windows executable settings
        "--windows-console-mode=disable",  # No console window (GUI app)
        f"--windows-icon-from-ico={WINDOWS_ICON}",
        
        # Company/Product info
        f"--windows-company-name={AUTHOR}",
        f"--windows-product-name={APP_NAME}",
        f"--windows-file-version={VERSION}",
        f"--windows-product-version={VERSION}",
        f"--windows-file-description={DESCRIPTION}",
        
        # Output name
        f"--output-filename={APP_NAME}.exe",
    ]
    return args


def get_macos_args() -> list:
    """Get macOS-specific Nuitka arguments."""
    args = [
        # macOS app bundle settings
        "--macos-create-app-bundle",
        f"--macos-app-icon={MACOS_ICON}",
        f"--macos-app-name={APP_NAME}",
        f"--macos-app-version={VERSION}",
        
        # Signing (ad-hoc for local testing)
        "--macos-sign-identity=ad-hoc",
        
        # Output name
        f"--output-filename={APP_NAME}",
    ]
    return args


def get_onefile_args() -> list:
    """Get arguments for creating a single executable file."""
    return [
        "--onefile",                       # Single executable
        "--onefile-tempdir-spec=%TEMP%/tachistostory" if get_platform() == "windows" 
            else "--onefile-tempdir-spec=/tmp/tachistostory",
    ]


def build(onefile: bool = False, clean: bool = True):
    """Run the Nuitka build process."""
    current_platform = get_platform()
    print(f"[*] Building {APP_NAME} for {current_platform}...")
    print(f"    Version: {VERSION}")
    print(f"    Mode: {'Onefile' if onefile else 'Standalone'}")
    
    # Check/install Nuitka
    if not check_nuitka_installed():
        install_nuitka()
    
    # Clean if requested
    if clean:
        clean_build_dirs()
    
    # Build arguments
    args = get_base_nuitka_args()
    
    # Add platform-specific arguments
    if current_platform == "windows":
        args.extend(get_windows_args())
    elif current_platform == "macos":
        args.extend(get_macos_args())
    
    # Add onefile if requested
    if onefile:
        args.extend(get_onefile_args())
    
    # Run build
    print("\n[*] Starting Nuitka compilation...")
    print(f"    Command: {' '.join(args)}\n")
    
    try:
        subprocess.run(args, check=True, cwd=ROOT_DIR)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed with error code {e.returncode}")
        sys.exit(1)
    
    # Move output to dist directory
    organize_output(current_platform, onefile)
    
    print(f"\n[OK] Build completed successfully!")
    print(f"     Output: {DIST_DIR}")


def organize_output(platform_name: str, onefile: bool):
    """Organize build output into dist directory."""
    print("\n[*] Organizing output files...")
    
    DIST_DIR.mkdir(exist_ok=True)
    
    if platform_name == "macos":
        # macOS creates an .app bundle
        app_bundle = BUILD_DIR / f"{APP_NAME}.app"
        if app_bundle.exists():
            dest = DIST_DIR / f"{APP_NAME}.app"
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(app_bundle, dest)
            print(f"    [OK] {APP_NAME}.app")
    else:
        # Windows/Linux
        if onefile:
            exe_name = f"{APP_NAME}.exe" if platform_name == "windows" else APP_NAME
            exe_file = BUILD_DIR / exe_name
            if exe_file.exists():
                shutil.copy2(exe_file, DIST_DIR / exe_name)
                print(f"    [OK] {exe_name}")
        else:
            dist_folder = BUILD_DIR / "main.dist"
            if dist_folder.exists():
                dest = DIST_DIR / APP_NAME
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(dist_folder, dest)
                print(f"    [OK] {APP_NAME}/")


def print_usage():
    """Print usage information."""
    print("""
============================================================
             Tachistostory - Nuitka Build Script            
============================================================

Usage: python build_nuitka.py [OPTIONS]

Options:
    --standalone    Build standalone distribution (default)
    --onefile       Build single executable file
    --no-clean      Don't clean previous builds
    --help          Show this help message

Examples:
    python build_nuitka.py                    # Standalone build
    python build_nuitka.py --onefile          # Single file build
    python build_nuitka.py --onefile --no-clean

Platform detected: """ + get_platform() + """
""")


def main():
    """Main entry point."""
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        print_usage()
        sys.exit(0)
    
    onefile = "--onefile" in args
    clean = "--no-clean" not in args
    
    build(onefile=onefile, clean=clean)


if __name__ == "__main__":
    main()
