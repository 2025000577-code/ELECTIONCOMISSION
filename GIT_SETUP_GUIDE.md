# 📦 Git Setup and Push Guide

## Step 1: Install Git

### Download Git for Windows
1. Go to: https://git-scm.com/download/win
2. Download the installer
3. Run the installer with default settings
4. Restart your terminal/VS Code after installation

### Verify Installation
```bash
git --version
```

---

## Step 2: Configure Git (First Time Only)

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

---

## Step 3: Initialize Git Repository

```bash
# Navigate to your project folder
cd "C:\Users\ratim\OneDrive\Desktop\Rati Proj"

# Initialize git repository
git init

# Check status
git status
```

---

## Step 4: Create GitHub Repository

### Option A: Using GitHub Website
1. Go to https://github.com
2. Click "+" icon → "New repository"
3. Repository name: `online-voting-system`
4. Description: `Secure online voting system with identity verification`
5. Choose: Public or Private
6. **DO NOT** initialize with README (we already have one)
7. Click "Create repository"

### Option B: Using GitHub CLI (if installed)
```bash
gh repo create online-voting-system --public --source=. --remote=origin
```

---

## Step 5: Add Files to Git

```bash
# Add all files (respects .gitignore)
git add .

# Check what will be committed
git status

# Commit with message
git commit -m "Initial commit: Online Voting System with Identity Verification"
```

---

## Step 6: Connect to GitHub and Push

### Get your GitHub repository URL
After creating the repository on GitHub, you'll see a URL like:
- HTTPS: `https://github.com/yourusername/online-voting-system.git`
- SSH: `git@github.com:yourusername/online-voting-system.git`

### Push to GitHub
```bash
# Add remote repository (replace with your URL)
git remote add origin https://github.com/yourusername/online-voting-system.git

# Verify remote
git remote -v

# Push to GitHub (first time)
git branch -M main
git push -u origin main
```

---

## Step 7: Authenticate with GitHub

### Option A: Personal Access Token (Recommended)
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Voting System"
4. Select scopes: `repo` (full control)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)
7. When pushing, use token as password:
   - Username: your GitHub username
   - Password: paste the token

### Option B: GitHub CLI
```bash
# Install GitHub CLI from: https://cli.github.com/
gh auth login
```

---

## Quick Commands Reference

### Daily Git Workflow
```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

### Useful Commands
```bash
# View commit history
git log --oneline

# View remote repositories
git remote -v

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# View differences
git diff
```

---

## Step 8: Update README for GitHub

Your README.md is already created, but you might want to add:
- GitHub badges
- Live demo link (if deployed)
- Screenshots
- Contribution guidelines

---

## Common Issues & Solutions

### Issue 1: "fatal: not a git repository"
```bash
# Solution: Initialize git
git init
```

### Issue 2: "failed to push some refs"
```bash
# Solution: Pull first, then push
git pull origin main --rebase
git push origin main
```

### Issue 3: "Authentication failed"
```bash
# Solution: Use Personal Access Token instead of password
# Or use GitHub CLI: gh auth login
```

### Issue 4: "Large files detected"
```bash
# Solution: Remove large files or use Git LFS
git rm --cached large-file.ext
echo "large-file.ext" >> .gitignore
git commit -m "Remove large file"
```

---

## Files That Will Be Pushed

### ✅ Included (Safe to push)
- Source code (`.py`, `.html`, `.css`, `.js`)
- Configuration templates (`.env.example`)
- Documentation (`.md` files)
- Requirements (`requirements.txt`)
- Static files
- Templates

### ❌ Excluded (Protected by .gitignore)
- `.env` (contains secrets)
- `db.sqlite3` (database file)
- `__pycache__/` (Python cache)
- `venv/` (virtual environment)
- `media/` (user uploads)
- `logs/` (log files)
- `.vscode/` (editor settings)

---

## Project Structure on GitHub

```
online-voting-system/
├── .gitignore                    # Git ignore rules
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
├── manage.py                     # Django management
├── .env.example                  # Environment template
├── voting_system/                # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── voting/                       # Main app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── migrations/
├── templates/                    # HTML templates
├── static/                       # CSS, JS, images
└── docs/                         # Documentation
```

---

## Complete Setup Script

Save this as `git_setup.bat` and run it:

```batch
@echo off
echo ========================================
echo Git Setup for Online Voting System
echo ========================================

echo.
echo Step 1: Initializing Git repository...
git init

echo.
echo Step 2: Adding files...
git add .

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit: Online Voting System with Identity Verification"

echo.
echo Step 4: Setting up remote repository...
echo Please enter your GitHub repository URL:
set /p REPO_URL="Repository URL: "

git remote add origin %REPO_URL%
git branch -M main

echo.
echo Step 5: Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo Setup complete!
echo ========================================
pause
```

---

## Alternative: Using VS Code

### VS Code Git Integration
1. Open VS Code
2. Click Source Control icon (left sidebar)
3. Click "Initialize Repository"
4. Stage all changes (click + icon)
5. Enter commit message
6. Click ✓ to commit
7. Click "..." → "Remote" → "Add Remote"
8. Enter GitHub URL
9. Click "..." → "Push"

---

## Security Checklist Before Pushing

- [ ] `.env` file is in `.gitignore`
- [ ] No passwords in code
- [ ] No API keys in code
- [ ] Database file excluded
- [ ] Virtual environment excluded
- [ ] User uploads excluded
- [ ] Log files excluded

---

## After Pushing to GitHub

### Add Repository Description
1. Go to your repository on GitHub
2. Click "About" (gear icon)
3. Add description: "Secure online voting system with identity verification"
4. Add topics: `django`, `voting-system`, `python`, `web-application`
5. Add website URL (if deployed)

### Enable GitHub Pages (Optional)
1. Go to Settings → Pages
2. Select branch: `main`
3. Select folder: `/docs` or `root`
4. Save

### Add Collaborators
1. Go to Settings → Collaborators
2. Click "Add people"
3. Enter GitHub username or email

---

## Continuous Updates

### When you make changes:
```bash
# 1. Check what changed
git status

# 2. Add changes
git add .

# 3. Commit with descriptive message
git commit -m "Add: Identity verification system"

# 4. Push to GitHub
git push
```

### Commit Message Best Practices:
- `Add: New feature description`
- `Fix: Bug fix description`
- `Update: Changes to existing feature`
- `Remove: Removed feature/file`
- `Docs: Documentation updates`

---

## Need Help?

### Git Documentation
- Official Git Docs: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com/

### Common Git Commands
- Cheat Sheet: https://education.github.com/git-cheat-sheet-education.pdf

### GitHub Support
- GitHub Help: https://docs.github.com/

---

**Ready to Push!** 🚀

Follow the steps above to push your Online Voting System to GitHub.
