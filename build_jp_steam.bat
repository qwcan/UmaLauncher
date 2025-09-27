cd ./umalauncher
python create_version.py
pyinstaller threader_jp_steam.spec || exit /b 1
cd ..