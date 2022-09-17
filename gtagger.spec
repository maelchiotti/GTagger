# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ["gtagger.py"],
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
        "sharp/settings-sharp.svg",
        "src/assets/img/icons/sharp/settings-sharp.svg",
        "DATA",
    ),
    (
        "outline/information-circle-outline.svg",
        "src/assets/img/icons/outline/information-circle-outline.svg",
        "DATA",
    ),
    (
        "sharp/information-circle-sharp.svg",
        "src/assets/img/icons/sharp/information-circle-sharp.svg",
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
    (
        "sharp/pricetag-sharp.svg",
        "src/assets/img/icons/sharp/pricetag-sharp.svg",
        "DATA",
    ),
    (
        "outline/help-circle-outline.svg",
        "src/assets/img/icons/outline/help-circle-outline.svg",
        "DATA",
    ),
    (
        "sharp/help-circle-sharp.svg",
        "src/assets/img/icons/sharp/help-circle-sharp.svg",
        "DATA",
    ),
    (
        "outline/text-outline.svg",
        "src/assets/img/icons/outline/text-outline.svg",
        "DATA",
    ),
    (
        "outline/close-outline.svg",
        "src/assets/img/icons/outline/close-outline.svg",
        "DATA",
    ),
    (
        "outline/contract-outline.svg",
        "src/assets/img/icons/outline/contract-outline.svg",
        "DATA",
    ),
    (
        "outline/expand-outline.svg",
        "src/assets/img/icons/outline/expand-outline.svg",
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
