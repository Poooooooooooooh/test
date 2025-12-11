# Render Deployment Setup Guide

## Fixing the serviceAccountKey.json Error

The error `FileNotFoundError: [Errno 2] No such file or directory: '/opt/render/project/src/serviceAccountKey.json'` occurs because the credentials file is not in your repository (which is correct for security).

## Solution: Use Environment Variables

### Option 1: Use FIREBASE_CREDENTIALS_JSON (Recommended)

1. **Get your serviceAccountKey.json content:**
   - Open your local `serviceAccountKey.json` file
   - Copy the entire JSON content

2. **In Render Dashboard:**
   - Go to your service → Environment
   - Click "Add Environment Variable"
   - **Key**: `FIREBASE_CREDENTIALS_JSON`
   - **Value**: Paste the entire JSON content (all in one line, or with proper escaping)
   - Click "Save Changes"

3. **Redeploy:**
   - Render will automatically redeploy
   - The app will now use the credentials from the environment variable

### Option 2: Upload the File via Render Shell

1. **Open Render Shell:**
   - Go to your service → Shell
   - Click "Open Shell"

2. **Create the file:**
   ```bash
   cd /opt/render/project/src
   nano serviceAccountKey.json
   ```
   - Paste your JSON content
   - Save (Ctrl+X, then Y, then Enter)

3. **Set environment variable:**
   - Go to Environment tab
   - Add: `GOOGLE_APPLICATION_CREDENTIALS=/opt/render/project/src/serviceAccountKey.json`

4. **Redeploy**

### Option 3: Add to Repository (NOT Recommended for Public Repos)

⚠️ **Only do this if your repository is private!**

1. **Temporarily remove from .gitignore:**
   ```bash
   # Edit .gitignore and comment out:
   # serviceAccountKey.json
   ```

2. **Add and commit:**
   ```bash
   git add serviceAccountKey.json
   git commit -m "Add serviceAccountKey.json"
   git push
   ```

3. **Redeploy on Render**

---

## Recommended: Option 1 (Environment Variable)

This is the most secure method. Your credentials stay in Render's secure environment variables and are never committed to git.

### Steps:

1. **Copy your serviceAccountKey.json content:**
   ```json
   {
     "type": "service_account",
     "project_id": "...",
     "private_key_id": "...",
     "private_key": "...",
     ...
   }
   ```

2. **In Render:**
   - Environment → Add Variable
   - Key: `FIREBASE_CREDENTIALS_JSON`
   - Value: Paste the entire JSON (you can format it or keep it as one line)

3. **Save and redeploy**

The updated `firebase_config.py` will automatically detect and use this environment variable!

---

## Verify It Works

After redeploying, check the logs:
- Go to Render → Your Service → Logs
- You should see: "Using Firebase credentials from FIREBASE_CREDENTIALS_JSON environment variable"
- No more FileNotFoundError!

---

## Security Notes

✅ **DO:**
- Use environment variables (FIREBASE_CREDENTIALS_JSON)
- Keep your repository private if you must commit the file
- Use Render's secure environment variables

❌ **DON'T:**
- Commit serviceAccountKey.json to public repositories
- Share your credentials
- Use the same credentials for multiple projects

---

## Troubleshooting

**Still getting errors?**
1. Check Render logs for the exact error message
2. Verify the JSON is valid (use a JSON validator)
3. Make sure there are no extra spaces or line breaks in the environment variable
4. Try escaping quotes if needed: `\"` instead of `"`

**Need help?**
- Render Docs: https://render.com/docs
- Firebase Docs: https://firebase.google.com/docs/admin/setup

