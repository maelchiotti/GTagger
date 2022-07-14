# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[],
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

a.datas += [
    (
        "outline/documents-outline.svg",
        "src/assets/img/icons/outline/documents-outline.svg",
        "DATA",
    ),
    (
        "outline/folder-open-outline.svg",
        "src/assets/img/icons/outline/folder-open-outline.svg",
        "DATA",
    ),
    (
        "outline/search-outline.svg",
        "src/assets/img/icons/outline/search-outline.svg",
        "DATA",
    ),
    (
        "outline/save-outline.svg",
        "src/assets/img/icons/outline/save-outline.svg",
        "DATA",
    ),
    (
        "outline/arrow-undo-outline.svg",
        "src/assets/img/icons/outline/arrow-undo-outline.svg",
        "DATA",
    ),
    (
        "outline/remove-circle-outline.svg",
        "src/assets/img/icons/outline/remove-circle-outline.svg",
        "DATA",
    ),
    (
        "outline/settings-outline.svg",
        "src/assets/img/icons/outline/settings-outline.svg",
        "DATA",
    ),
    (
        "outline/open-outline.svg",
        "src/assets/img/icons/outline/open-outline.svg",
        "DATA",
    ),
    (
        "outline/sunny-outline.svg",
        "src/assets/img/icons/outline/sunny-outline.svg",
        "DATA",
    ),
    (
        "outline/moon-outline.svg",
        "src/assets/img/icons/outline/moon-outline.svg",
        "DATA",
    ),
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="GTagger",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
