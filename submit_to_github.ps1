# PowerShell script to submit to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Submitting to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Adding all files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "Step 2: Committing changes..." -ForegroundColor Yellow
git commit -m "Add blue-noise stippling implementation with outputs and GitHub Pages"

Write-Host ""
Write-Host "Step 3: Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Done!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your code is now on GitHub!" -ForegroundColor Green
Write-Host "Repository: https://github.com/nickalba-collab/stippleChallenge" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to your repository on GitHub"
Write-Host "2. Settings > Pages > Source: main branch, /docs folder"
Write-Host "3. Save to enable GitHub Pages"
Write-Host ""

