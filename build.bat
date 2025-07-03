cd ./umalauncher
python create_version.py
pyinstaller threader.spec
pyinstaller threader_global.spec
cd ..