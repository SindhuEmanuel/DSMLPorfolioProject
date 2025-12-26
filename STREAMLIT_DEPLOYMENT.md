# 🚀 Streamlit Cloud Deployment Guide

## Quick Deployment to Streamlit Cloud (FREE)

### Prerequisites
- GitHub account
- Project pushed to GitHub repository

### Step-by-Step Deployment

#### 1. Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Streamlit Cloud deployment"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git push -u origin main
```

#### 2. Deploy on Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with GitHub

3. **Click** "New app"

4. **Configure**:
   - **Repository**: Select your repository
   - **Branch**: `main`
   - **Main file path**: `deployment/app.py`
   - **App URL** (optional): Choose a custom URL

5. **Advanced settings** (click "Advanced settings"):
   - **Python version**: 3.11 or 3.12
   - **Requirements file**: Leave as `streamlit_requirements.txt` (will auto-detect)

6. **Click** "Deploy!"

#### 3. Wait for Deployment

The app will:
- Install dependencies from `streamlit_requirements.txt`
- Download data automatically on first run
- Train models (cached after first run)
- Be live in 2-5 minutes!

### 📁 Required Files (Already Created!)

✅ **`.streamlit/config.toml`** - Streamlit configuration
✅ **`streamlit_requirements.txt`** - Python dependencies for deployment
✅ **`packages.txt`** - System dependencies
✅ **`deployment/app.py`** - Updated with auto-download capability

### 🔧 Important Notes

1. **Data File**: The app will automatically download `countries.csv` from Google Drive on first deployment

2. **Model Training**: Models are trained on startup and cached using `@st.cache_resource`

3. **Free Tier Limits**:
   - 1 GB RAM
   - 1 CPU core
   - App sleeps after 7 days of inactivity
   - Unlimited public apps

4. **Performance**: First load takes ~30 seconds to train models. Subsequent loads are instant (cached).

### 📊 What Gets Deployed

Your Streamlit app includes:
- ✅ 5 interactive pages
- ✅ Data exploration tools
- ✅ 3 clustering algorithms
- ✅ Priority country lists
- ✅ Country prediction tool
- ✅ Downloadable results

### 🎨 Customization

#### Update App Title/Icon
Edit `deployment/app.py`:
```python
st.set_page_config(
    page_title="Your Title Here",
    page_icon="🌍",
    layout="wide"
)
```

#### Update Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"  # Change colors here
```

### 🐛 Troubleshooting

**Issue**: "Module not found" error
- **Solution**: Check `streamlit_requirements.txt` includes all packages

**Issue**: App is slow
- **Solution**: Models are trained on first load. Use `@st.cache_resource` for caching

**Issue**: Data file not found
- **Solution**: App auto-downloads from Google Drive. Check internet connection.

**Issue**: Out of memory
- **Solution**: Streamlit free tier has 1GB RAM. Optimize data loading or upgrade.

### 📱 Share Your App

Once deployed, share the URL:
```
https://YOUR_APP_NAME.streamlit.app
```

### 🔄 Updates

To update your deployed app:
```bash
# Make changes locally
git add .
git commit -m "Update description"
git push

# Streamlit Cloud auto-deploys on push!
```

### 🎉 Example Deployment URL

After deployment, your app will be accessible at:
```
https://country-aid-clustering-YOUR_USERNAME.streamlit.app
```

### 📚 Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Deployment Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Community Forum**: https://discuss.streamlit.io

---

## Alternative: Docker Deployment

If you prefer Docker:

### Dockerfile

Already included in deployment guide! See `DEPLOYMENT_GUIDE.md` for Docker instructions.

### Docker Compose

Also available in `DEPLOYMENT_GUIDE.md` for running both Streamlit and Flask.

---

## 🎯 Next Steps

1. ✅ Push to GitHub
2. ✅ Deploy on Streamlit Cloud
3. ✅ Share your app URL
4. ✅ Monitor usage in Streamlit Cloud dashboard

**Your app is ready for deployment!** 🚀

---

*Last Updated: Project restructuring complete*
*Deployment: Streamlit Cloud ready*
