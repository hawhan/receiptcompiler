# PWA Installation & Testing Guide

## 🚀 Running the App

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. The app will open in your default browser (usually at `http://localhost:8501`)

## 📱 Installing as PWA

### On Desktop (Chrome/Edge)

1. **Look for the install icon** in the address bar (right side):
   - Chrome: Shows a ⊕ or install icon
   - Edge: Shows a + icon with "App available"

2. **Click the install icon** or:
   - Chrome: Click the three dots menu → "Install Receipts Compiler..."
   - Edge: Click the three dots menu → "Apps" → "Install this site as an app"

3. **Confirm installation** in the popup dialog

4. The app will open in its own window without browser UI

### On Mobile (Android)

1. Open the app in Chrome browser
2. Tap the three dots menu (⋮)
3. Select "Add to Home screen" or "Install app"
4. Confirm and the app icon will appear on your home screen

### On Mobile (iOS)

1. Open the app in Safari
2. Tap the Share button (square with arrow)
3. Scroll down and tap "Add to Home Screen"
4. Customize the name if desired and tap "Add"

## ✅ Verifying PWA Installation

### Check Service Worker Registration

1. Open browser DevTools (F12)
2. Go to **Application** tab (Chrome) or **Debugger** → **Service Workers** (Firefox)
3. Under "Service Workers", you should see:
   - Status: "activated and is running"
   - Source: `/static/service-worker.js`

### Check Manifest

1. In DevTools → **Application** tab
2. Click **Manifest** in the left sidebar
3. Verify:
   - Name: "Receipts Compiler & Organizer"
   - Icons: 192x192 and 512x512 icons should be visible
   - Theme color: #ff4b4b (red)

### Check Cache Storage

1. In DevTools → **Application** tab
2. Click **Cache Storage** in the left sidebar
3. You should see cache named `receipts-compiler-v1`
4. Expand it to see cached files

## 🧪 Testing Offline Functionality

1. **Install the app** first (see above)
2. **Open the installed app** (not the browser version)
3. In DevTools, go to **Network** tab
4. Check the **Offline** checkbox (or set throttling to "Offline")
5. **Refresh the page** - the UI should still load (from cache)
6. Note: Processing receipts requires internet connection (server-side processing)

## 🎨 PWA Features

✅ **What Works:**
- Install on desktop and mobile
- App icon on home screen/desktop
- Standalone window (no browser UI)
- Offline UI viewing (cached interface)
- Custom theme color
- Splash screen on mobile

⚠️ **Limitations:**
- Receipt processing requires internet connection
- Streamlit server must be running
- File uploads need active connection
- Full offline processing not supported (server-side AI)

## 🔧 Troubleshooting

### Install prompt doesn't appear
- Make sure you're using HTTPS or localhost
- Clear browser cache and reload
- Check DevTools console for errors

### Service Worker not registering
- Check browser console for errors
- Verify `/static/service-worker.js` is accessible
- Make sure `.streamlit/config.toml` has `enableStaticServing = true`

### Icons not showing
- Verify icon files exist in `/static/icons/`
- Check manifest.json paths are correct
- Clear cache and reload

## 📂 PWA File Structure

```
Receipts Compiler/
├── static/
│   ├── manifest.json          # PWA manifest
│   ├── service-worker.js      # Service worker for caching
│   ├── favicon.ico            # Browser favicon
│   └── icons/
│       ├── icon-192.png       # 192x192 app icon
│       └── icon-512.png       # 512x512 app icon
├── .streamlit/
│   └── config.toml            # Streamlit config for static serving
└── app.py                     # Main app with PWA integration
```
