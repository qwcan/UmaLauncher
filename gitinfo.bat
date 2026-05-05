cd umalauncher/_assets
git symbolic-ref -q HEAD >nul 2>&1
if %errorlevel% neq 0 (
    echo Detached HEAD > branch.txt
) else (
    git branch --show-current > branch.txt
)
git rev-parse --short HEAD > commit_hash.txt
powershell -Command "Get-Date -Format 'yyyy-MM-dd HH:mm:ss K'" > build_date.txt
git remote get-url origin > remote_url.txt
cd ../..