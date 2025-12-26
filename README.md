# Country Clustering for Strategic Aid Allocation

## 🌍 Project Overview

This project helps **HELP International** identify countries most in need of aid using unsupervised machine learning clustering techniques. By analyzing socio-economic and health indicators, we can strategically prioritize aid allocation to maximize impact.

## 📁 Project Structure

```
ClusteringCountriesAid/
│
├── data/                          # Data directory
│   └── countries.csv              # Country socio-economic data
│
├── src/                           # Source code modules
│   ├── data_loader.py            # Data loading and inspection
│   ├── eda.py                    # Exploratory data analysis
│   ├── stats.py                  # Statistical hypothesis testing
│   ├── preprocessing.py          # Data preprocessing and feature engineering
│   ├── modeling.py               # Clustering models (K-Means, Hierarchical, DBSCAN)
│   └── evaluation.py             # Model evaluation and visualization
│
├── deployment/                    # Deployment files
│   ├── app.py                    # Streamlit web application
│   └── api.py                    # Flask REST API
│
├── models/                        # Trained models (generated)
│   ├── kmeans_model.pkl
│   ├── scaler.pkl
│   └── ...
│
├── tests/                         # Unit tests
│
├── config.py                      # Configuration file
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Features

### Data Analysis
- **Missing Value Analysis**: Complete data quality assessment
- **Outlier Detection**: IQR-based outlier detection with winsorization
- **Univariate Analysis**: Box plots and KDE plots for key features
- **Bivariate Analysis**: Correlation analysis and scatter plots
- **Hypothesis Testing**: Statistical tests for key relationships

### Machine Learning Models
1. **K-Means Clustering**
   - Optimal k selection using Elbow method and Silhouette scores
   - 3 distinct clusters identified

2. **Hierarchical Clustering**
   - Dendrogram visualization
   - Ward linkage method
   - Consistent with K-Means results

3. **DBSCAN**
   - Density-based clustering
   - Identifies outliers and anomalous countries
   - Reveals unique development patterns

### Deployment Options

#### 1. Streamlit Web Application (Interactive UI)
- **Overview Dashboard**: Dataset statistics and key metrics
- **Data Exploration**: Interactive visualizations and country search
- **Clustering Analysis**: View different clustering methods and results
- **Aid Priority List**: Downloadable list of high-priority countries
- **Country Prediction**: Predict cluster for custom country data

#### 2. Flask REST API (Programmatic Access)
- `/predict`: Predict cluster for country data
- `/clusters`: Get cluster profiles
- `/countries`: List all countries with cluster assignments
- `/priority`: Get priority countries for aid allocation

## 📊 Key Insights

### Most Vulnerable Countries (High Priority)
- **Characteristics**:
  - High child mortality (mean standardized value: ~1.4)
  - Low income (mean standardized value: ~-0.8)
  - Low GDP per capita (mean standardized value: ~-0.75)
  - Low life expectancy (mean standardized value: ~-1.2)
  - High total fertility (mean standardized value: ~1.4)

### Statistical Findings
1. **Child Mortality vs Income**: Strong negative correlation (p < 0.001)
2. **Health Spending vs Life Expectancy**: Positive correlation (p < 0.01)
3. **Fertility vs Income**: Moderate negative correlation (r = -0.58)
4. **Inflation vs GDP**: Weak negative correlation (r = -0.24)

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone or download the project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Place data file**
   - Ensure `countries.csv` is in the `data/` directory
   - Or download it using gdown (see original script)

## 💻 Usage

### 1. Run Data Analysis Pipeline

```python
# Complete EDA and preprocessing
from src.data_loader import load_data
from src.eda import perform_full_eda
from src.stats import perform_all_hypothesis_tests
from src.preprocessing import preprocess_pipeline

# Load data
data = load_data("data/countries.csv")

# Perform EDA
data = perform_full_eda(data)

# Statistical tests
results = perform_all_hypothesis_tests(data)

# Preprocessing
processed_data, scaler, clustering_data = preprocess_pipeline(data)
```

### 2. Train Clustering Models

```python
from src.modeling import KMeansClusterer, HierarchicalClusterer, DBSCANClusterer

# K-Means
kmeans = KMeansClusterer(max_clusters=10)
kmeans.find_optimal_k(clustering_data)
kmeans.plot_elbow()
kmeans.plot_silhouette()
kmeans_labels = kmeans.fit(clustering_data, n_clusters=3)

# Hierarchical
hierarchical = HierarchicalClusterer()
hierarchical.compute_linkage(clustering_data)
hierarchical.plot_dendrogram()
hierarchical_labels = hierarchical.fit(clustering_data, n_clusters=3)

# DBSCAN
dbscan = DBSCANClusterer(eps=1.5, min_samples=3)
dbscan_labels = dbscan.fit(clustering_data)
```

### 3. Evaluate and Visualize

```python
from src.evaluation import apply_pca, visualize_all_clustering_methods

# Apply PCA
pca_df, pca = apply_pca(clustering_data)

# Visualize all methods
visualize_all_clustering_methods(pca_df, kmeans_labels, hierarchical_labels, dbscan_labels)
```

### 4. Launch Streamlit App

```bash
cd deployment
streamlit run app.py
```

Access at: `http://localhost:8501`

### 5. Launch Flask API

```bash
cd deployment
python api.py
```

API available at: `http://localhost:5000`

#### API Examples

**Predict cluster for a country:**
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

**Get priority countries:**
```bash
curl http://localhost:5000/priority
```

**Get all cluster profiles:**
```bash
curl http://localhost:5000/clusters
```

## 📈 Model Performance

### K-Means Clustering
- **Number of Clusters**: 3
- **Silhouette Score**: ~0.35 (for k=3)
- **Consistency**: High agreement with Hierarchical clustering

### Hierarchical Clustering
- **Number of Clusters**: 3
- **Method**: Ward linkage
- **Results**: Very similar to K-Means, validating cluster stability

### DBSCAN
- **Clusters Found**: 5
- **Noise Points**: 22 outlier countries
- **Advantage**: Identifies anomalous countries requiring special attention

## 🎯 Recommendations for HELP International

### Immediate Priority (High Vulnerability Cluster)
Countries with:
- Child mortality > 1.4 (standardized)
- Income < -0.8 (standardized)
- Life expectancy < -1.2 (standardized)

**Recommended Actions**:
1. Focus on healthcare infrastructure
2. Poverty reduction programs
3. Basic needs (food, water, sanitation)
4. Education initiatives

### Medium Priority (Developing Countries Cluster)
Countries showing moderate indicators

**Recommended Actions**:
1. Sustainable development programs
2. Capacity building
3. Economic diversification
4. Institutional strengthening

### Special Attention (DBSCAN Outliers)
22 countries with unique characteristics

**Recommended Actions**:
- Individual assessment required
- Tailored intervention strategies
- Investigation of specific challenges

## 🔧 Configuration

Edit `config.py` to customize:
- Data paths
- Model hyperparameters
- Clustering configuration
- API settings
- Visualization preferences

## 🧪 Testing

Run tests (when implemented):
```bash
pytest tests/
```

## 📝 Dependencies

Key libraries:
- **Data Processing**: pandas, numpy, scipy
- **Machine Learning**: scikit-learn
- **Visualization**: matplotlib, seaborn
- **Web Frameworks**: Flask, Streamlit
- **Utilities**: joblib, gdown

See `requirements.txt` for complete list.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational and humanitarian purposes.

## 👥 Authors

- Data Science Team
- HELP International Analytics

## 🙏 Acknowledgments

- Original dataset providers
- scikit-learn community
- Streamlit and Flask frameworks

## 📧 Contact

For questions or support, please contact the project maintainers.

---

**Note**: This project uses unsupervised learning to identify patterns in country development indicators. Results should be used as one of multiple inputs for aid allocation decisions, combined with ground truth assessments and expert knowledge.
