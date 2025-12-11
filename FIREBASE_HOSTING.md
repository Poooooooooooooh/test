# Hosting Your Flask App with Google Cloud (Firebase Ecosystem)

Since your app is a **Flask application** (Python backend), Firebase Hosting alone won't work. Firebase Hosting is for static websites only. However, you can use **Google Cloud Run** which is part of the Google Cloud/Firebase ecosystem.

## Option 1: Google Cloud Run (Recommended - Same Ecosystem as Firebase)

Google Cloud Run is perfect for Flask apps and works seamlessly with Firebase services.

### Prerequisites:
1. Google Cloud account (same as Firebase)
2. Google Cloud SDK installed
3. Docker installed (optional, but recommended)

### Steps:

#### 1. Install Google Cloud SDK
Download from: https://cloud.google.com/sdk/docs/install

#### 2. Initialize and Login
```bash
gcloud init
gcloud auth login
```

#### 3. Set Your Project
```bash
gcloud config set project YOUR_PROJECT_ID
```

#### 4. Create Dockerfile
Already created! The `Dockerfile` in your project is ready.

#### 5. Build and Deploy
```bash
# Build the container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/piggy-expense-tracker

# Deploy to Cloud Run
gcloud run deploy piggy-expense-tracker \
  --image gcr.io/YOUR_PROJECT_ID/piggy-expense-tracker \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=/app/serviceAccountKey.json
```

#### 6. Set Environment Variables
In Cloud Run console:
- Go to your service → Edit & Deploy New Revision
- Add environment variables:
  - `GOOGLE_APPLICATION_CREDENTIALS=/app/serviceAccountKey.json`

#### 7. Upload serviceAccountKey.json
Make sure `serviceAccountKey.json` is in your project directory (it should be).

**Note:** For production, consider using Secret Manager instead of committing the key file.

---

## Option 2: Render (Easier Alternative)

If you want something simpler, Render is a great option:

### Steps:

1. **Go to [render.com](https://render.com)** and sign up

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure:**
   - **Name**: `piggy-expense-tracker`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or paid)

4. **Add Environment Variable:**
   - `GOOGLE_APPLICATION_CREDENTIALS=serviceAccountKey.json`

5. **Deploy!**

Your app will be live at: `https://piggy-expense-tracker.onrender.com`

---

## Option 3: Railway (Also Easy)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. New Project → Deploy from GitHub
4. Select your repository
5. Add environment variable: `GOOGLE_APPLICATION_CREDENTIALS=serviceAccountKey.json`
6. Deploy automatically!

---

## Option 4: Firebase Hosting + Cloud Functions (Advanced)

If you really want to use Firebase Hosting, you'd need to:
1. Convert your Flask app to Cloud Functions
2. Serve static files with Firebase Hosting
3. Route API calls to Cloud Functions

This is more complex and requires restructuring your app.

---

## Quick Start: Render (Recommended for Beginners)

Since you already have your code on GitHub:

1. **Add gunicorn to requirements.txt** (if not already there):
   ```bash
   echo "gunicorn" >> requirements.txt
   ```

2. **Commit and push:**
   ```bash
   git add requirements.txt
   git commit -m "Add gunicorn for production"
   git push
   ```

3. **Deploy on Render:**
   - Go to render.com
   - New Web Service
   - Connect GitHub → Select your repo
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Add env var: `GOOGLE_APPLICATION_CREDENTIALS=serviceAccountKey.json`
   - Deploy!

**Done!** Your app will be live in ~5 minutes.

---

## Important Notes:

### Security:
- **Don't commit `serviceAccountKey.json` to public repos!**
- Use environment variables or Secret Manager for production
- Consider using Firebase Admin SDK with environment variables instead

### Production Checklist:
- [ ] Use `gunicorn` instead of Flask's development server
- [ ] Set `debug=False` in production
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS (automatic on Cloud Run/Render/Railway)
- [ ] Set up proper CORS if needed
- [ ] Configure proper error handling

### Updating Your App:
After making changes:
```bash
git add .
git commit -m "Your changes"
git push
```

Render/Railway will automatically redeploy. For Cloud Run, you'll need to rebuild and redeploy.

---

## Troubleshooting:

### App won't start:
- Check logs in your hosting platform
- Ensure `gunicorn` is in requirements.txt
- Verify `serviceAccountKey.json` path is correct

### Firebase connection errors:
- Verify `serviceAccountKey.json` is uploaded
- Check environment variable `GOOGLE_APPLICATION_CREDENTIALS`
- Ensure Firestore API is enabled in Firebase Console

### 500 errors:
- Check application logs
- Verify all dependencies are in requirements.txt
- Ensure Python version matches (3.8+)

---

## Need Help?

- Google Cloud Run: https://cloud.google.com/run/docs
- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Firebase: https://firebase.google.com/docs

