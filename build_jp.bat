cd ./umalauncher
python create_version.py
pyinstaller threader.spec || exit /b 1
cd ..