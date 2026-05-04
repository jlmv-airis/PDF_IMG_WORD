# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['desktop-app/AIRIS_Converter.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('desktop-app/worker.py', '.'),
        ('C:/Users/Jorge Meneses/AppData/Roaming/Python/Python314/site-packages/tkinterdnd2/tkdnd', 'tkinterdnd2/tkdnd'),
        ('C:/Users/Jorge Meneses/AppData/Roaming/Python/Python314/site-packages/customtkinter', 'customtkinter'),
    ],
    hiddenimports=[
        'fitz', 'PIL', 'PIL.Image', 'PIL.ImageOps', 'docx', 'docx.shared', 
        'docx.enum.text', 'docx.enum.section', 'customtkinter', 'tkinterdnd2',
        'concurrent.futures', 'multiprocessing'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'sqlalchemy', 'django', 'numpy', 'pandas', 'scipy', 'matplotlib',
        'flask', 'unittest'
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AIRIS_Converter',
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
    icon=None,
)
