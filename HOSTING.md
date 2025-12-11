# How to Host Your Flask App from GitHub

## Option 1: Render (Recommended - Free & Easy) ⭐

### Steps:

1. **Go to [render.com](https://render.com)** and sign up (free account)

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub account** and select your repository:
   - Repository: `Poooooooooooooh/test`
   - Branch: `master`

4. **Configure the service:**
   - **Name**: `piggy-expense-tracker` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or paid for better performance)

5. **Add Environment Variables:**
   - Go to "Environment" tab
   - Add: `GOOGLE_APPLICATION_CREDENTIALS` = `serviceAccountKey.json`
   - (Make sure `serviceAccountKey.json` is in your repository)

6. **Deploy:**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Your app will be live at: `https://your-app-name.onrender.com`

### Important Notes:
- ✅ Free tier available (apps may sleep after inactivity)
- ✅ Automatic deployments on git push
- ✅ HTTPS included
- ⚠️ Free tier has slower cold starts

---

## Option 2: Railway (Also Free)

### Steps:

1. **Go to [railway.app](https://railway.app)** and sign up with GitHub

2. **Click "New Project" → "Deploy from GitHub repo"**

3. **Select your repository**: `Poooooooooooooh/test`

4. **Railway will auto-detect Python** and use your `requirements.txt`

5. **Add Environment Variable:**
   - Go to "Variables" tab
   - Add: `GOOGLE_APPLICATION_CREDENTIALS` = `serviceAccountKey.json`

6. **Deploy automatically!**
   - Railway will deploy automatically
   - Get your URL from the project dashboard

---

## Option 3: PythonAnywhere (Simple for Beginners)

### Steps:

1. **Go to [pythonanywhere.com](https://www.pythonanywhere.com)** and sign up (free)

2. **Open Bash Console**

3. **Clone your repository:**
   ```bash
   git clone https://github.com/Poooooooooooooh/test.git
   cd test
   ```

4. **Install dependencies:**
   ```bash
   pip3.10 install --user -r requirements.txt
   pip3.10 install --user gunicorn
   ```

5. **Create Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Flask and Python 3.10
   - Set source code directory to `/home/yourusername/test`

6. **Configure WSGI file:**
   - Edit the WSGI file to point to your app:
   ```python
   import sys
   path = '/home/yourusername/test'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

7. **Set Environment Variables:**
   - In Web tab → "Environment variables"
   - Add: `GOOGLE_APPLICATION_CREDENTIALS` = `/home/yourusername/test/serviceAccountKey.json`

8. **Reload Web App**

---

## Option 4: Google Cloud Run (Best for Firebase Projects)

### Steps:

1. **Install Google Cloud SDK** from [cloud.google.com/sdk](https://cloud.google.com/sdk)

2. **Create a Dockerfile** (already created for you)

3. **Deploy:**
   ```bash
   # Set your project
   gcloud config set project YOUR_PROJECT_ID
   
   # Build and deploy
   gcloud run deploy piggy-expense-tracker \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

---

## Important: Firebase Credentials

⚠️ **Security Note**: Your `serviceAccountKey.json` file contains sensitive credentials.

**Option A: Commit to Private Repo** (Easiest)
- Make sure your GitHub repo is **private**
- Commit `serviceAccountKey.json` to the repo
- Hosting platforms can access it

**Option B: Use Environment Variables** (More Secure)
- Don't commit `serviceAccountKey.json`
- Copy the JSON content
- Paste it as an environment variable on your hosting platform
- Modify `firebase_config.py` to read from environment variable

---

## Quick Start: Render (5 minutes)

1. **Push your code to GitHub** (already done ✅)

2. **Go to render.com** → New Web Service

3. **Connect GitHub** → Select `Poooooooooooooh/test`

4. **Settings:**
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`

5. **Add environment variable:**
   - `GOOGLE_APPLICATION_CREDENTIALS` = `serviceAccountKey.json`

6. **Deploy!** 🚀

Your app will be live in ~5 minutes!

---

## Troubleshooting

### App won't start
- Check logs in your hosting platform
- Ensure `gunicorn` is in `requirements.txt` ✅
- Verify `serviceAccountKey.json` path is correct

### Firebase connection errors
- Verify `serviceAccountKey.json` is uploaded/accessible
- Check environment variable `GOOGLE_APPLICATION_CREDENTIALS`
- Ensure Firestore API is enabled in Firebase Console

### 500 errors
- Check application logs
- Verify all dependencies are in `requirements.txt`
- Ensure Python version matches (3.8+)

---

## Need Help?

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- PythonAnywhere: https://help.pythonanywhere.com
- Google Cloud Run: https://cloud.google.com/run/docs

