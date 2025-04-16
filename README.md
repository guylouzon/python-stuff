# 🐍 Python Data Science Tools
> A collection of specialized Python tools for data analysis and machine learning

## 📊 Pluster: Clustering Analysis Tool
A Python class designed to simplify and enhance clustering analysis workflows.

### Features
#### 🎯 Feature Importance Analysis
```python
def get_cluster_importance(dataframe, cluster_column):
    """
    Analyzes feature importance for clustering results.
    
    Args:
        dataframe: pandas DataFrame containing the data
        cluster_column: name of the column containing cluster assignments
    
    Returns:
        DataFrame with feature importance scores
    """
```

#### 📈 Elbow Analysis
```python
def get_elbow_analysis(dataframe, max_clusters=10, **kmeans_params):
    """
    Performs elbow analysis and silhouette scoring.
    
    Args:
        dataframe: input DataFrame
        max_clusters: maximum number of clusters to test
        **kmeans_params: additional KMeans parameters
    
    Returns:
        DataFrame with elbow curve metrics and silhouette scores
    """
```

### Usage Example
```python
from pluster import ClusterAnalyzer

# Initialize analyzer
analyzer = ClusterAnalyzer()

# Analyze feature importance
importance_df = analyzer.get_cluster_importance(df, 'cluster_labels')

# Perform elbow analysis
elbow_results = analyzer.get_elbow_analysis(df, max_clusters=15)
```

## 📈 LTV Revenue Projection Model
A sophisticated model for calculating Expected Lifetime Value (LTV) and marketing ROI.

### Overview
Based on Eric Benjamin Seufert's methodology from "Building a marketing P&L using LTV and ROAS", this tool provides:
- Revenue projections
- Spend analysis
- Profit calculations
- User growth visualization

### Key Features
- 📊 Data manipulation with Pandas
- 📉 Visualization using Matplotlib
- 💹 LTV calculations
- 📈 Growth projections

![LTV Analysis Graphs](pygraph.png)

### Documentation
For detailed implementation and usage instructions, see the [full documentation](LTV_README.md).

## 🛠️ Installation
```bash
git clone https://github.com/YourUsername/python-stuff.git
cd python-stuff
pip install -r requirements.txt
```

## 📝 License
MIT License - feel free to use and modify for your own projects!

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
