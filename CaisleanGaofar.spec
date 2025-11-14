# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Caislean Gaofar
Optimized to reduce Windows Defender false positives
"""

block_cipher = None

# Analysis: Scan the main script and dependencies
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include map data files
        ('data/maps', 'data/maps'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ: Python archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE: Executable configuration
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CaisleanGaofar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Explicitly disable UPX compression (reduces AV false positives)
    console=False,  # Windowed mode (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows version information (helps legitimize the executable)
    version='version_info.txt',
    icon=None,  # TODO: Add icon file to further legitimize
)
