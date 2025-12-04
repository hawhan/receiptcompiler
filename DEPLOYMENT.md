# Deploying to Streamlit Community Cloud

This guide walks you through deploying the Receipts Compiler PWA to Streamlit Community Cloud (free tier).

## Prerequisites

- GitHub account
- Streamlit Community Cloud account (free - sign up at [share.streamlit.io](https://share.streamlit.io))
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Step 1: Create GitHub Repository

### Option A: Using GitHub Desktop or Git CLI

1. **Initialize Git repository** (if not already done):
   ```bash
   cd "H:/My Drive/--- Antigravity/Receipts Compiler"
   git init
   ```

2. **Add all files**:
   ```bash
   git add .
   ```

3. **Commit**:
   ```bash
   git commit -m "Initial commit - Receipts Compiler PWA"
   ```

4. **Create repository on GitHub**:
   - Go to [github.com/new](https://github.com/new)
   - Name it `receipts-compiler` (or your preferred name)
   - **DO NOT** initialize with README (you already have one)
   - Click "Create repository"

5. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/receipts-compiler.git
   git branch -M main
   git push -u origin main
   ```

### Option B: Using GitHub Web Interface

1. Go to [github.com/new](https://github.com/new)
2. Create a new repository named `receipts-compiler`
3. Upload all files from your project folder (except `.env` file!)

## Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**:
   - Click "New app" button
   - Select your repository: `YOUR_USERNAME/receipts-compiler`
   - Set main file path: `app.py`
   - Click "Advanced settings"

3. **Configure Secrets**:
   In the "Secrets" section, add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
   
   > [!IMPORTANT]
   > Replace `your_actual_api_key_here` with your actual Google Gemini API key

4. **Deploy**:
   - Click "Deploy!"
   - Wait for deployment to complete (usually 2-3 minutes)

## Step 3: Access Your App

Once deployed, you'll get a URL like:
```
https://YOUR_USERNAME-receipts-compiler-app-RANDOM.streamlit.app
```

This URL is:
- ✅ Publicly accessible
- ✅ HTTPS enabled (required for PWA)
- ✅ Always available (as long as Streamlit Cloud is running)

## Step 4: Install PWA on Mobile

### Android

1. **Open the app URL** in Chrome on your Android phone
2. **Tap the menu** (⋮) in the top-right
3. **Select "Add to Home screen"** or "Install app"
4. **Confirm** the installation
5. **Find the icon** on your home screen

### iOS

1. **Open the app URL** in Safari on your iPhone
2. **Tap the Share button** (square with arrow)
3. **Scroll down** and tap "Add to Home Screen"
4. **Customize the name** if desired
5. **Tap "Add"**
6. **Find the icon** on your home screen

## Step 5: Verify PWA Features

1. **Open DevTools** (F12) on desktop browser
2. **Go to Application tab**
3. **Check Manifest**: Should show "Receipts Compiler & Organizer"
4. **Check Service Worker**: Should be "activated and running"
5. **Test offline**: Enable offline mode, refresh - UI should still load

## Updating Your App

When you make changes to your code:

1. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```

2. **Streamlit Cloud auto-deploys**: Your app will automatically redeploy within a few minutes

## Troubleshooting

### App Won't Deploy

- **Check logs** in Streamlit Cloud dashboard
- **Verify requirements.txt** has all dependencies
- **Check Python version** compatibility

### API Key Not Working

- **Verify secrets** are configured correctly in Streamlit Cloud
- **Check format**: Should be `GEMINI_API_KEY = "your_key"`
- **No quotes** around the key in secrets

### PWA Not Installing

- **Must use HTTPS**: Streamlit Cloud provides this automatically
- **Check manifest**: Open DevTools → Application → Manifest
- **Clear cache**: Try in incognito/private mode first

### Service Worker Not Registering

- **Check browser console** for errors
- **Verify static files** are being served
- **Try hard refresh**: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

## Resource Limits (Free Tier)

Streamlit Community Cloud free tier includes:

- ✅ 1 GB RAM
- ✅ 1 CPU core
- ✅ Unlimited public apps
- ⚠️ Apps sleep after inactivity (wake up when accessed)
- ⚠️ Limited to 1 concurrent user for free tier

For heavy usage, consider upgrading to a paid plan.

## Security Best Practices

1. **Never commit** `.env` files or API keys to GitHub
2. **Use Streamlit Secrets** for all sensitive configuration
3. **Review `.gitignore`** before pushing to ensure no secrets are included
4. **Rotate API keys** periodically
5. **Monitor usage** of your Gemini API key

## Custom Domain (Optional)

To use a custom domain:

1. Upgrade to Streamlit Cloud paid plan
2. Follow [Streamlit's custom domain guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/custom-domains)

## Support

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: Report bugs in your repository

---

## Quick Reference

### Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `.env` file NOT in repository
- [ ] Secrets configured in Streamlit Cloud
- [ ] App deployed successfully
- [ ] PWA installable on mobile
- [ ] Service worker registered
- [ ] API key working correctly

### Useful Commands

```bash
# Check git status
git status

# View deployment logs
# (In Streamlit Cloud dashboard → Manage app → Logs)

# Test locally before deploying
streamlit run app.py

# Force refresh in browser
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)
```

Enjoy your deployed PWA! 🎉
