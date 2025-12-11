# Deploying to Render - Step by Step Guide

## Prerequisites
1. Your code is pushed to GitHub (✅ Already done!)
2. A Render account (free tier available)
3. Your Firebase `serviceAccountKey.json` file

## Step 1: Prepare Your Code

All necessary files are already created:
- ✅ `Procfile` - Tells Render how to run your app
- ✅ `requirements.txt` - Includes gunicorn
- ✅ Your Flask app is ready

## Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account (recommended for easy deployment)

## Step 3: Create New Web Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub account if not already connected
3. Select your repository: `Poooooooooooooh/test`
4. Select the branch: `master`

## Step 4: Configure Settings

Fill in the following settings:

### Basic Settings:
- **Name**: `piggy-expense-tracker` (or any name you like)
- **Environment**: `Python 3`
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `master`

### Build & Deploy:
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn app:app
  ```

### Plan:
- **Free** (or upgrade to Starter for better performance)

## Step 5: Upload Firebase Credentials (REQUIRED)

**Important:** `serviceAccountKey.json` is in `.gitignore` for security, so you need to add it as an environment variable.

### Steps:

1. **Open your local `serviceAccountKey.json` file**
2. **Copy the ENTIRE contents** (all the JSON, including `{` and `}`)
3. **In Render dashboard**, go to your service → **"Environment"** tab
4. **Click "Add Environment Variable"**
5. **Add the variable:**
   - **Key**: `FIREBASE_CREDENTIALS`
   - **Value**: Paste the entire JSON content from `serviceAccountKey.json`
   - **Example value format:**
     ```json
     {
       "type": "service_account",
       "project_id": "your-project-id",
       "private_key_id": "...",
       "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
       ...
     }
     ```
6. **Click "Save Changes"**

**Note:** The code now automatically reads from `FIREBASE_CREDENTIALS` environment variable if available, or falls back to the file for local development.

## Step 7: Deploy!

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies
   - Build your app
   - Deploy it
3. Wait 3-5 minutes for deployment to complete

## Step 8: Access Your App

Once deployed, your app will be available at:
```
https://piggy-expense-tracker.onrender.com
```
(Replace `piggy-expense-tracker` with your service name)

## Important Notes

### Free Tier Limitations:
- ⚠️ Apps may **sleep after 15 minutes of inactivity**
- ⚠️ First request after sleep takes ~30-50 seconds (cold start)
- ⚠️ Limited to 750 hours/month (enough for most use cases)

### Firebase Setup:
- Make sure your Firebase project has **Firestore API enabled**
- Ensure your `serviceAccountKey.json` has proper permissions
- Check Firebase Console → Project Settings → Service Accounts

### Troubleshooting:

**App won't start:**
- Check logs in Render dashboard
- Verify `gunicorn` is in `requirements.txt`
- Check that `serviceAccountKey.json` path is correct

**Firebase connection errors:**
- Verify `serviceAccountKey.json` is uploaded
- Check environment variable `GOOGLE_APPLICATION_CREDENTIALS`
- Ensure Firestore API is enabled in Firebase Console

**500 errors:**
- Check application logs in Render
- Verify all dependencies are in `requirements.txt`
- Ensure Python version matches (3.8+)

## Updating Your App

After making changes:
1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```
2. Render will automatically detect changes and redeploy
3. Or manually trigger redeploy from Render dashboard

## Need Help?

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Check Render dashboard logs for detailed error messages

---

**That's it! Your app should be live in ~5 minutes! 🚀**

