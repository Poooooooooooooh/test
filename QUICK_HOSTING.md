# Quick Hosting Guide 🚀

## Fastest Way: Render (5 minutes)

### Step 1: Push to GitHub
Your code is already on GitHub at: `https://github.com/Poooooooooooooh/test.git`

### Step 2: Deploy on Render

1. **Go to [render.com](https://render.com)** and sign up (free)

2. **Click "New +" → "Web Service"**

3. **Connect GitHub repository:**
   - Click "Connect GitHub"
   - Authorize Render
   - Select repository: `test`

4. **Configure Settings:**
   - **Name**: `piggy-expense-tracker` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. **Add Environment Variable:**
   - Go to "Environment" tab
   - Click "Add Environment Variable"
   - Key: `GOOGLE_APPLICATION_CREDENTIALS`
   - Value: `serviceAccountKey.json`

6. **Click "Create Web Service"**

7. **Wait 3-5 minutes** for deployment

8. **Your app is live!** 🎉
   - URL: `https://piggy-expense-tracker.onrender.com` (or your custom name)

---

## Alternative: Google Cloud Run (Firebase Ecosystem)

### Prerequisites:
- Google Cloud account (same as Firebase)
- Google Cloud SDK installed

### Quick Deploy:

1. **Install Google Cloud SDK:**
   - Download: https://cloud.google.com/sdk/docs/install

2. **Login and set project:**
   ```bash
   gcloud init
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Deploy:**
   ```bash
   # Build
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/piggy-expense-tracker
   
   # Deploy
   gcloud run deploy piggy-expense-tracker \
     --image gcr.io/YOUR_PROJECT_ID/piggy-expense-tracker \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. **Set environment variable in Cloud Run console:**
   - Go to Cloud Run → Your service → Edit
   - Add: `GOOGLE_APPLICATION_CREDENTIALS=/app/serviceAccountKey.json`

---

## Files Ready:
✅ `Dockerfile` - For containerized deployment  
✅ `requirements.txt` - Includes gunicorn  
✅ `.dockerignore` - Excludes unnecessary files  
✅ `app.yaml` - For App Engine (alternative)

---

## After Deployment:

1. **Test your app:**
   - Visit your URL
   - Try: `/test` endpoint
   - Try: `/login` page

2. **Update your app:**
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```
   Render will auto-redeploy!

---

## Troubleshooting:

**App won't start?**
- Check logs in Render/Cloud Run dashboard
- Ensure `gunicorn` is in requirements.txt ✅ (already added)

**Firebase errors?**
- Verify `serviceAccountKey.json` is in your repo
- Check environment variable is set correctly

**Need help?**
- Render: https://render.com/docs
- Cloud Run: https://cloud.google.com/run/docs

---

**That's it! Your Flask app will be live! 🎉**

