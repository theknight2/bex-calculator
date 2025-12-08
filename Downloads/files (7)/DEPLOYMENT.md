# BEX Calculator - Deployment Guide

## Files Structure

```
├── app.py                    # Main Streamlit app (deployment entry point)
├── bex_calculator_streamlit.py  # Original development file
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── DEPLOYMENT.md            # This file
```

## Streamlit Cloud Deployment

### Step 1: Connect Repository

1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Click "New app"
3. Connect your GitHub repository: `theknight2/bex-calculator`
4. Select branch: `main`
5. Main file path: `app.py`

### Step 2: Deploy

- Streamlit Cloud will automatically detect `requirements.txt`
- The app will deploy using `app.py` as the entry point
- Configuration from `.streamlit/config.toml` will be applied

### Step 3: Access

- Your app will be available at: `https://your-app-name.streamlit.app`
- Share the URL with users

## Local Development

### Run Locally

```bash
streamlit run app.py
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## File Differences

- **`app.py`**: Clean deployment version, identical functionality
- **`bex_calculator_streamlit.py`**: Development version (same code)

## Configuration

The `.streamlit/config.toml` sets:
- Monochrome theme (black/white)
- Server settings
- Browser stats disabled

## Verification

After deployment, verify:
- ✅ Strategy selection works
- ✅ Calculations are correct
- ✅ Output displays properly
- ✅ Typography renders correctly

## Updates

To update the app:
1. Push changes to `main` branch
2. Streamlit Cloud auto-deploys
3. Changes go live in ~30 seconds

