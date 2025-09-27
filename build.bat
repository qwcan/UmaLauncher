call build_global.bat
if errorlevel 1 goto ERROR
call build_jp.bat
if errorlevel 1 goto ERROR
call build_jp_steam.bat
if errorlevel 1 goto ERROR
echo Success
goto EOF

:ERROR
echo Failed
exit /b 1

:EOF