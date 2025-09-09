block_cipher = None

a = Analysis(
    ['app/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('models/age_deploy.prototxt', 'models'),
        ('models/age_net.caffemodel', 'models'),
        ('models/emotion_model.hdf5', 'models'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[]
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='face_age_emotion_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # voorkomt CI issues
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='face_age_emotion_app'
)