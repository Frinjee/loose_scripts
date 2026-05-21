@echo off
setlocal

set /p REPO=Enter repo (owner/repo): 

if "%REPO%"=="" (
  echo Repo not provided. Exiting.
  exit /b 1
)

echo.
echo Repo: %REPO%
echo This will:
echo   - Keep the MOST RECENT deployment
echo   - Mark ALL older deployments as INACTIVE
echo   - DELETE all older deployments
echo.

set /p CONFIRM=Type YES to continue: 

if /i not "%CONFIRM%"=="YES" (
  echo Aborted.
  exit /b 0
)

echo.
echo Fetching deployments...

gh api "repos/%REPO%/deployments?per_page=100" | jq -r ".[].id" > deployment_ids.txt

if not exist deployment_ids.txt (
  echo Failed to retrieve deployments.
  exit /b 1
)

more +1 deployment_ids.txt > deployment_ids_old.txt

for %%A in (deployment_ids_old.txt) do (
  if not "%%~zA"=="0" goto has_old
)

echo No old deployments found.
exit /b 0

:has_old
echo Marking old deployments inactive...
for /f %%i in (deployment_ids_old.txt) do (
  gh api --method POST ^
    -H "Accept: application/vnd.github+json" ^
    -H "X-GitHub-Api-Version: 2022-11-28" ^
    "repos/%REPO%/deployments/%%i/statuses" ^
    -f state=inactive
)

echo Deleting old deployments...
for /f %%i in (deployment_ids_old.txt) do (
  gh api --method DELETE ^
    -H "Accept: application/vnd.github+json" ^
    -H "X-GitHub-Api-Version: 2022-11-28" ^
    "repos/%REPO%/deployments/%%i"
)

echo.
echo Cleanup complete.
endlocal
