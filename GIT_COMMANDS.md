# Git Commands for Pushing to GitHub

## Step 1: Verify Files are Ignored

First, make sure your credentials won't be committed:

```bash
# Check what will be committed
git status
```

**You should NOT see:**
- `storage-*.json` files
- `credentials.json`
- `google_drive_file_id.txt`

If you see these files, **STOP** and check your `.gitignore`.

## Step 2: Initialize Git Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Check what's staged
git status
```

## Step 3: Create First Commit

```bash
git commit -m "Initial commit: Chat Storage API

- FastAPI backend for Custom GPT chat logging
- Google Drive/Docs integration
- Service Account authentication
- Supports both Google Docs and plain text files"
```

## Step 4: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `chat-storage-api` (or your choice)
3. Description: "FastAPI backend to store Custom GPT chats in Google Drive"
4. **Private** repository (recommended for internal projects)
5. **Do NOT** initialize with README (we already have one)
6. Click **Create repository**

## Step 5: Connect to GitHub

GitHub will show you commands. Use these:

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/chat-storage-api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 6: Verify on GitHub

1. Go to your repository on GitHub
2. **Double-check** that `storage-*.json` files are NOT visible
3. Verify `credentials.template.json` IS there
4. Check that `README.md` displays correctly

## Important: Before Pushing

**✅ Checklist:**
- [ ] `.gitignore` file exists
- [ ] Actual credentials file is backed up locally (`.backup` extension)
- [ ] `google_storage.py` has placeholder values (no real folder IDs)
- [ ] `storage-*.json` is listed in `.gitignore`
- [ ] Ran `git status` and confirmed no sensitive files

**❌ Never commit:**
- Service account JSON files
- Real folder IDs
- API keys or tokens
- Any file with real credentials

## Sharing Credentials with Team

**Option 1: Secure Storage**
- Use 1Password, LastPass, or similar
- Share credentials vault with team

**Option 2: Direct Share** (less secure)
- Send via encrypted email
- Or use your company's secure file sharing

**Option 3: Environment Variables** (production)
- Store in deployment platform (Render, Heroku, etc.)
- Never commit `.env` files

## Updating Code Later

When you make changes:

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push
```

## If You Accidentally Committed Credentials

**IMMEDIATELY:**

```bash
# Remove from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch storage-*.json" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
```

Then:
1. **Revoke** the compromised Service Account
2. Create a new one
3. Update the backup file
4. Inform your team lead

---

**Ready to push?** Follow the steps above and you'll be all set! 🚀
