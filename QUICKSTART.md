# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download Data File
```bash
python download_data.py
```
This will download the country data from Google Drive to `data/countries.csv`.

### Step 3: Choose Your Path

#### Option A: Run Complete Analysis (Recommended for First Time)
```bash
python run_analysis.py
```
This will:
- Load and analyze the data
- Train all clustering models
- Generate visualizations
- Save results

#### Option B: Launch Interactive Web App
```bash
cd deployment
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

#### Option C: Launch REST API
```bash
cd deployment
python api.py
```
API available at `http://localhost:5000`

## 📊 Using the Streamlit App

Once launched, you can:
1. **Overview** - View dataset statistics
2. **Data Exploration** - Explore features and correlations
3. **Clustering Analysis** - Compare different clustering methods
4. **Aid Priority List** - See which countries need urgent aid
5. **Country Prediction** - Predict cluster for custom data

## 🔌 Using the REST API

### Example: Predict Cluster
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "child_mort": 25.0,
    "exports": 28.5,
    "health": 5.2,
    "imports": 32.1,
    "income": 8500.0,
    "inflation": 6.3,
    "life_expec": 68.5,
    "total_fer": 3.1,
    "gdpp": 7200.0
  }'
```

### Example: Get Priority Countries
```bash
curl http://localhost:5000/priority
```

## 📝 Using Individual Modules

```python
# Load data
from src.data_loader import load_data
data = load_data("data/countries.csv")

# Run EDA
from src.eda import perform_full_eda
data = perform_full_eda(data)

# Preprocess
from src.preprocessing import preprocess_pipeline
processed_data, scaler, clustering_data = preprocess_pipeline(data)

# Train K-Means
from src.modeling import KMeansClusterer
kmeans = KMeansClusterer()
labels = kmeans.fit(clustering_data, n_clusters=3)

# Visualize with PCA
from src.evaluation import apply_pca, visualize_clusters
pca_df, pca = apply_pca(clustering_data)
visualize_clusters(pca_df, labels, 'K-Means Clusters')
```

## 🎯 Key Features to Try

1. **Compare Clustering Methods** - See how K-Means, Hierarchical, and DBSCAN differ
2. **Identify Outliers** - DBSCAN finds 22 anomalous countries
3. **Export Priority List** - Download CSV of countries needing urgent aid
4. **Interactive Predictions** - Input custom country data to see cluster assignment

## 🐛 Troubleshooting

**Issue**: Module not found
- **Solution**: Make sure you're running from the project root directory

**Issue**: Data file not found
- **Solution**: Check that `countries.csv` is in the `data/` directory

**Issue**: Port already in use
- **Solution**: Change port in `config.py` or kill the process using the port

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the code in the `src/` directory
- Customize clustering parameters in `config.py`
- Add your own analysis or visualizations

## 💡 Tips

- All models are cached in Streamlit for faster performance
- The Flask API automatically saves trained models to `models/`
- Results are saved to `data/clustering_results.csv` after running `run_analysis.py`
- Adjust clustering parameters in `config.py` for different results

## 🎓 Understanding the Results

### Priority Levels
- **HIGH**: Countries with child mortality > 0.5 (standardized) - Urgent aid needed
- **MEDIUM**: Countries with -0.5 < child mortality < 0.5 - Moderate aid needed
- **LOW**: Countries with child mortality < -0.5 - Minimal aid needed

### Cluster Interpretation
- **Cluster with highest child_mort** → Most vulnerable, prioritize for aid
- **Cluster with lowest income/gdpp** → Economic challenges, need development support
- **DBSCAN noise points (-1)** → Unique cases requiring individual assessment

Happy Analyzing! 🎉
