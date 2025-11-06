# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ['threader.py'],
    pathex=['venv\\Lib\\site-packages'],
    binaries=[],
    datas=[('./_assets/icon/global/default.ico', '.'), ('./_assets/icon/global/connecting.ico', '.'), ('./_assets/icon/global/connected.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['global_runtime_hook.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
a.datas += Tree('./_assets', prefix='_assets')
a.datas += Tree('./external', prefix='external')
a.datas += Tree('./ff_profile', prefix='ff_profile')

a.datas += Tree('../venv/Lib/site-packages/google', prefix='external/google')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='UmaLauncher-Global',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    uac_admin=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['./_assets/icon/global/default.ico'],
    version='version_global.rc'
)
