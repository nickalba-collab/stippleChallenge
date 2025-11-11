@echo off
echo ========================================
echo Submitting to GitHub
echo ========================================
echo.

echo Step 1: Adding all files...
git add .

echo.
echo Step 2: Committing changes...
git commit -m "Add blue-noise stippling implementation with outputs and GitHub Pages"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo Done!
echo ========================================
echo.
echo Your code is now on GitHub!
echo Repository: https://github.com/nickalba-collab/stippleChallenge
echo.
echo Next steps:
echo 1. Go to your repository on GitHub
echo 2. Settings ^> Pages ^> Source: main branch, /docs folder
echo 3. Save to enable GitHub Pages
echo.
pause

