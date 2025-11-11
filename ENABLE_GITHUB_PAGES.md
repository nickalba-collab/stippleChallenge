# Enable GitHub Pages - Step by Step

## Quick Steps

1. **Go to your repository on GitHub:**
   ```
   https://github.com/nickalba-collab/stippleChallenge
   ```

2. **Click on "Settings"** (top right of the repository page, next to "Code")

3. **Click on "Pages"** (left sidebar, under "Code and automation")

4. **Under "Source":**
   - Select: **"Deploy from a branch"**
   - Branch: Select **"main"**
   - Folder: Select **"/docs"**
   - Click **"Save"**

5. **Wait 1-2 minutes** for GitHub to build your site

6. **Your site will be live at:**
   ```
   https://nickalba-collab.github.io/stippleChallenge
   ```

## Visual Guide

```
GitHub Repository Page
├── Top Bar
│   ├── Code
│   ├── Issues
│   ├── Pull requests
│   └── Settings ← CLICK HERE
│
Settings Page (Left Sidebar)
├── General
├── Access
├── Secrets and variables
├── Actions
├── Pages ← CLICK HERE
│
Pages Settings
├── Source: Deploy from a branch
├── Branch: main
├── Folder: /docs
└── Save button ← CLICK HERE
```

## After Enabling

- ✅ Your clean website will show only images and text
- ✅ No code files visible on the website
- ✅ Professional presentation for your professor
- ✅ Repository still has all code (for grading)

## Verify It's Working

After enabling, you'll see:
- A message: "Your site is live at https://nickalba-collab.github.io/stippleChallenge"
- The site will show your stippled images
- It may take 1-2 minutes to build initially

## Troubleshooting

**If you don't see "Pages" in Settings:**
- Make sure you're the repository owner or have admin access
- The repository must be public (or you have GitHub Pro)

**If the site doesn't load:**
- Wait a few minutes (GitHub needs to build it)
- Check that `docs/index.md` exists (it does!)
- Check that `docs/outputs/` folder has images (it does!)

**If images don't show:**
- Make sure `docs/outputs/stipple.png` and `docs/outputs/progressive.gif` exist
- They should be there already!

## What Your Professor Will See

**On the GitHub Pages site:**
- Clean webpage with your stippled image
- Progressive GIF animation
- Description of blue-noise stippling
- No code files visible

**On the repository (if they check):**
- All your code files
- README.md
- Everything for grading

