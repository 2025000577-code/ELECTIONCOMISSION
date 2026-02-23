@echo off
echo ========================================
echo Git Setup for Online Voting System
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo After installation, restart this script.
    pause
    exit /b 1
)

echo Git is installed!
echo.

REM Check if already initialized
if exist .git (
    echo Git repository already initialized.
    echo.
) else (
    echo Initializing Git repository...
    git init
    echo.
)

REM Configure git (if not configured)
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo Git user not configured. Please enter your details:
    set /p GIT_NAME="Your Name: "
    set /p GIT_EMAIL="Your Email: "
    git config --global user.name "%GIT_NAME%"
    git config --global user.email "%GIT_EMAIL%"
    echo Configuration saved!
    echo.
)

REM Add files
echo Adding files to Git...
git add .
echo.

REM Create commit
echo Creating initial commit...
git commit -m "Initial commit: Online Voting System with Identity Verification"
echo.

REM Check if remote exists
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo Please enter your GitHub repository URL:
    echo Example: https://github.com/yourusername/online-voting-system.git
    set /p REPO_URL="Repository URL: "
    git remote add origin %REPO_URL%
    echo Remote added!
    echo.
)

REM Set main branch
echo Setting main branch...
git branch -M main
echo.

REM Push to GitHub
echo Pushing to GitHub...
echo You may be prompted for GitHub credentials.
echo Use your GitHub username and Personal Access Token (not password).
echo.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Project pushed to GitHub!
    echo ========================================
    echo.
    echo Your project is now on GitHub!
    echo You can view it at your repository URL.
) else (
    echo.
    echo ========================================
    echo Push failed. Common solutions:
    echo ========================================
    echo 1. Make sure you created the repository on GitHub
    echo 2. Use Personal Access Token instead of password
    echo 3. Check your internet connection
    echo 4. Verify the repository URL is correct
    echo.
    echo To get a Personal Access Token:
    echo 1. Go to GitHub Settings
    echo 2. Developer settings
    echo 3. Personal access tokens
    echo 4. Generate new token
    echo 5. Select 'repo' scope
    echo.
)

pause
