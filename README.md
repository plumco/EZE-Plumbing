# Eze Plumbing BOQ — Streamlit App

Interactive Bill of Quantities tool for Huliot plumbing systems.  
Covers **HT Pro** and **Ultra Silent** series — April 2025 Price List.

---

## Features

- **Dashboard** — DN tile-based pipe selector + fitting category tiles; click to expand items
- **Search** — full-text search across 250+ products
- **BOQ** — editable quantity sheet with discount, GST, live totals
- **Excel Export** — downloads a formatted `.xlsx` with BOQ + Summary sheets
- **Excel Import** — re-loads a previously exported BOQ
- **Project Info** — site name, contractor, date stored per session

---

## Project Structure

```
eze_plumbing_app/
├── app.py                  ← Main Streamlit application
├── requirements.txt        ← Python dependencies
├── .streamlit/
│   └── config.toml         ← Theme + server settings
└── README.md               ← This file
```

---

## Local Development

### Prerequisites
- Python 3.9 or higher
- pip

### Steps

```bash
# 1. Clone or download the project folder
cd eze_plumbing_app

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## Deploy on Streamlit Community Cloud (Free)

Streamlit Community Cloud is the easiest free hosting option.

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit — Eze Plumbing BOQ"
   git remote add origin https://github.com/YOUR_USERNAME/eze-plumbing-boq.git
   git push -u origin main
   ```

2. **Go to** [share.streamlit.io](https://share.streamlit.io)

3. **Sign in** with your GitHub account

4. Click **"New app"** → select your repository and branch

5. Set **Main file path** to `app.py`

6. Click **"Deploy!"**

Your app will be live at:  
`https://YOUR_USERNAME-eze-plumbing-boq-app-XXXX.streamlit.app`

---

## Deploy on Railway (Free tier available)

Railway auto-detects Python apps.

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Add a `Procfile` for Railway:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

---

## Deploy on Render (Free tier)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect GitHub repo
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Deploy

---

## Deploy on Heroku

Create a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

```bash
heroku create eze-plumbing-boq
git push heroku main
heroku open
```

---

## Deploy with Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

```bash
docker build -t eze-plumbing-boq .
docker run -p 8501:8501 eze-plumbing-boq
```

---

## Dependencies

| Package    | Version  | Purpose                        |
|------------|----------|--------------------------------|
| streamlit  | ≥1.35.0  | Web UI framework               |
| pandas     | ≥2.0.0   | Data handling + Excel read     |
| openpyxl   | ≥3.1.0   | Excel write (.xlsx export)     |
| xlrd       | ≥2.0.1   | Excel read (older .xls import) |

---

## Usage Guide

### Adding Items to BOQ
1. **Dashboard tab** → Click a **DN tile** (e.g., "DN 110") to expand pipe lengths for that size
2. Click **+ Add** next to any item
3. Or click a **fitting category tile** (e.g., "BENDS") to expand those items

### Search
- Switch to **Search tab** → type description, code, or DN size

### Adjusting Quantities
- Go to **BOQ tab** → use the number inputs to set exact quantities
- Or click **✕** to remove an item

### Discount & GST
- Set in **sidebar** → applies live to totals

### Export
- Click **📥 Export Excel BOQ** (sidebar or BOQ tab)
- Downloads formatted Excel with BOQ lines + Summary sheet

### Import
- Click **📤 Import Excel BOQ** in sidebar
- Upload a previously exported `.xlsx` — items are matched by Item Code

---

## Price List Notes

- All prices are **List Prices (W.E.F April 2025)**, ex-factory/depot
- Actual selling price depends on applicable trade discount
- GST is extra unless explicitly included via the GST toggle

---

## Support

For product queries, contact Huliot Pipes and Fittings Pvt. Ltd.
