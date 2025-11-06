cd ./umalauncher
python create_version.py
pyinstaller threader_global.spec || exit /b 1
cd ..