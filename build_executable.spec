# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['web_interface.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'src.generators',
        'src.models',
        'src.utils',
        'src.exporter',
        'src.trend_generator',
        'src.crime_specific_generators',
        'src.ai_enhancer',
        'faker',
        'rich',
        'flask',
        'werkzeug',
        'werkzeug.formparser',
        'werkzeug.wrappers',
        'werkzeug.wrappers.request',
        'werkzeug.wrappers.response',
        'werkzeug.utils',
        'jinja2',
        'jinja2.ext',
        'click',
        'itsdangerous',
        'markupsafe',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CaseGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # UPX compression can cause zlib errors
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True to see errors and Flask output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)

