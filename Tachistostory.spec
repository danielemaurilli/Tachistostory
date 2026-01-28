# -*- mode: python ; coding: utf-8 -*-
"""
Tachistostory - PyInstaller Spec File
Optimized configuration for macOS and Windows builds
"""

import sys
from pathlib import Path

# Paths
ROOT_DIR = Path(SPECPATH)
ASSETS_DIR = ROOT_DIR / 'assets'

# App info
APP_NAME = 'Tachistostory'
VERSION = '0.2.8'
BUNDLE_ID = 'com.danielemaurilli.tachistostory'

# Icons
MACOS_ICON = str(ASSETS_DIR / 'tachistostory.icns')
WINDOWS_ICON = str(ASSETS_DIR / 'tachistostory.ico')

# Determine icon based on platform
if sys.platform == 'darwin':
    ICON = MACOS_ICON
elif sys.platform == 'win32':
    ICON = WINDOWS_ICON
else:
    ICON = None

# Hidden imports (modules not detected automatically)
hiddenimports = [
    'pygame',
    'pygame.base',
    'pygame.constants',
    'pygame.rect',
    'pygame.surface',
    'pygame.display',
    'pygame.event',
    'pygame.locals',
    'pygame.color',
    'pygame.draw',
    'pygame.font',
    'pygame.image',
    'pygame.key',
    'pygame.mixer',
    'pygame.mouse',
    'pygame.time',
    'pygame.transform',
    'pygame.sprite',
    'pygame.cursors',
    'pygame.mixer_music',
    'docx2txt',
]

# Modules to exclude (reduce size)
excludes = [
    'pygame.tests',
    'pygame.examples',
    'tkinter',
    'unittest',
    'pydoc',
    'doctest',
    'difflib',
    'numpy',
    'scipy',
    'matplotlib',
    'PIL',
]

a = Analysis(
    ['main.py'],
    pathex=[str(ROOT_DIR)],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=2,
)

# Remove pygame test data
a.datas = [d for d in a.datas if not d[0].startswith('pygame/tests')]
a.datas = [d for d in a.datas if not d[0].startswith('pygame/examples')]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)

# macOS App Bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name=f'{APP_NAME}.app',
        icon=MACOS_ICON,
        bundle_identifier=BUNDLE_ID,
        info_plist={
            'CFBundleName': APP_NAME,
            'CFBundleDisplayName': APP_NAME,
            'CFBundleVersion': VERSION,
            'CFBundleShortVersionString': VERSION,
            'CFBundleIdentifier': BUNDLE_ID,
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',
            'NSRequiresAquaSystemAppearance': False,
        },
    )

