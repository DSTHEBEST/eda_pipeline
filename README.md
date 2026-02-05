# Industry-Grade Automated EDA Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

A fully modular, reusable, and statistically enriched **Exploratory Data Analysis (EDA)** pipeline built using Python. This pipeline automates visualization, statistical testing, and feature importance analysis for structured datasets.

---

## 📖 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Statistical Methodology](#-statistical-methodology)
- [Installation & Setup](#-installation--setup)
- [Usage](#️-usage)
- [Output Generated](#-output-generated)
- [Example Insights](#-example-insights)
- [Tech Stack](#-tech-stack)
- [Configuration](#-configuration)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 📖 Project Overview

This project provides an **industry-style automated EDA framework** designed to bridge the gap between **raw data exploration** and **machine learning readiness**.

### Core Capabilities

- **Automated data profiling** - Comprehensive dataset analysis with minimal manual effort
- **Advanced visualization** - Distribution, Correlation, and Categorical analysis
- **Statistical hypothesis testing** - T-Test and Chi-Square validation
- **Effect size analysis** - Cohen's D for practical significance
- **Feature importance evaluation** - Identify key predictors
- **Automatic report generation & logging** - Complete audit trail

---

## ✨ Key Features

### 📊 Visualization

The pipeline prioritizes technical clarity and minimal visual clutter using a research-grade design philosophy.

- **Distribution Plots** - Analyze numerical feature spreads with histograms and KDE
- **Target Comparison** - Visual separation of classes for supervised learning
- **Correlation Heatmaps** - Identify multicollinearity and feature relationships
- **Categorical Analysis** - Frequency distributions and cross-tabulations
- **Feature Importance** - Ranked charts for model interpretability

### 🧮 Statistical Analysis

Moves beyond visual inspection to statistical validation:

- **T-Test** - Evaluates mean differences for numerical features vs. binary targets
- **Chi-Square Test** - Tests independence between categorical variables
- **Cohen's D** - Quantifies the *practical* magnitude of differences

### ⚙️ Automation

- **Config-Driven** - Control all pipeline parameters via `config.yaml`
- **Logging** - Integrated `loguru`-based logging for debugging and monitoring
- **Modular Architecture** - Reusable components in `utils.py` and `eda_pipeline.py`

---

## 📂 Project Structure

```bash
eda_pipeline/
│
├── config.yaml          # Configuration settings for the pipeline
├── eda_pipeline.py      # Main pipeline logic
├── utils.py             # Helper functions for stats and plotting
├── logger.py            # Custom logging setup
├── run_pipeline.py      # Entry point script
├── reports/             # Generated outputs (Created automatically)
│   ├── plots/           # Visualization outputs
│   ├── statistics/      # Statistical test results
│   └── dashboard.html   # Interactive Sweetviz report
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

---

## 📉 Statistical Methodology

The pipeline employs rigorous statistical tests to validate insights:

### 1. T-Test

Evaluates whether the means of numerical features differ significantly across target classes.

- **Null Hypothesis (H₀):** No difference in means between groups
- **Alternative Hypothesis (H₁):** Significant difference exists
- **Significance Level:** α = 0.05 (default, configurable)

### 2. Chi-Square Test

Measures the association between categorical variables and the target variable.

- **Null Hypothesis (H₀):** Variables are independent
- **Alternative Hypothesis (H₁):** Variables are associated
- **Significance Level:** α = 0.05 (default, configurable)

### 3. Cohen's D Effect Size

Quantifies the practical importance of feature differences, separating statistical significance from real-world impact.

| Effect Size | Interpretation |
|-------------|----------------|
| 0.2         | Small          |
| 0.5         | Medium         |
| 0.8+        | Large          |

---

## 🚀 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone <your_repo_link>
cd eda_pipeline
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / Mac:**
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Basic Execution

To execute the full analysis pipeline, simply run the entry script:

```bash
python run_pipeline.py
```

### Custom Configuration

Modify `config.yaml` to customize pipeline behavior:

```yaml
# Example config.yaml
data:
  file_path: "data/your_dataset.csv"
  target_column: "target"

analysis:
  statistical_tests: true
  feature_importance: true
  generate_sweetviz: true

visualization:
  style: "seaborn-v0_8-darkgrid"
  save_format: "png"
  dpi: 300
```

### Programmatic Usage

```python
from eda_pipeline import EDAPipeline

# Initialize pipeline
pipeline = EDAPipeline(config_path="config.yaml")

# Run analysis
pipeline.run()

# Access results
results = pipeline.get_results()
```

---

## 📊 Output Generated

The pipeline automatically generates a `reports/` directory containing:

### Visualizations (`reports/plots/`)
- Distribution & density plots for all numerical features
- Target comparison plots (stratified by class)
- Correlation heatmap with hierarchical clustering
- Categorical frequency charts

### Statistical Analysis (`reports/statistics/`)
- T-test results (CSV format)
- Chi-square test results (CSV format)
- Effect size analysis tables
- Summary statistics report (TXT/CSV)

### Interactive Dashboard
- **Sweetviz HTML dashboard** - Comprehensive interactive data profiling

---

## 🧪 Example Insights

Based on sample execution with a mental health dataset:

✅ **Key Findings:**
- Lifestyle factors significantly correlate with depression indicators
- Stress level and academic performance show the strongest practical effects (Large Cohen's D > 0.8)
- Demographic features showed weaker associations despite statistical significance
- Sleep duration and exercise frequency are top predictors

📌 **Statistical Validation:**
- 12 out of 15 numerical features showed significant mean differences (p < 0.05)
- 8 categorical variables demonstrated strong associations with target
- Effect sizes ranged from 0.15 (negligible) to 1.2 (very large)

---

## 🔬 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Core** | Python 3.8+ |
| **Data Manipulation** | Pandas, NumPy |
| **Visualization** | Seaborn, Matplotlib, Sweetviz |
| **Statistics** | SciPy |
| **Logging** | Loguru |
| **Configuration** | PyYAML |

---

## 🛠 Configuration

### Available Configuration Options

```yaml
# Data Settings
data:
  file_path: "path/to/data.csv"
  target_column: "target"
  drop_columns: []  # Columns to exclude from analysis

# Analysis Options
analysis:
  statistical_tests: true
  feature_importance: true
  correlation_analysis: true
  generate_sweetviz: true
  
# Visualization Settings
visualization:
  style: "seaborn-v0_8-darkgrid"
  color_palette: "viridis"
  figure_size: [10, 6]
  save_format: "png"
  dpi: 300

# Statistical Thresholds
thresholds:
  significance_level: 0.05
  correlation_threshold: 0.7
  min_effect_size: 0.2

# Output Settings
output:
  reports_dir: "reports"
  save_intermediate: false
  verbose_logging: true
```

---

## 🎯 Future Improvements

- [ ] **SHAP Integration** - Model-agnostic explainability for feature contributions
- [ ] **Data Drift Monitoring** - Track statistical changes over time
- [ ] **Automated Feature Selection** - Remove low-importance features automatically
- [ ] **Interactive Dashboards** - Streamlit or Plotly Dash integration
- [ ] **ML Pipeline Integration** - Direct hook into scikit-learn workflows
- [ ] **Multi-target Support** - Handle regression and multi-class problems
- [ ] **Time Series Analysis** - Temporal pattern detection
- [ ] **Automated Outlier Detection** - Robust anomaly identification

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation accordingly

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Devansh Sharma**

- GitHub: [@devanshsharma](https://github.com/devanshsharma)
- LinkedIn: [Connect with me](https://linkedin.com/in/devanshsharma)

---

## 🙏 Acknowledgments

- Thanks to the open-source community for excellent data science libraries
- Inspired by industry best practices in automated ML pipelines
- Built with ❤️ for data scientists and ML engineers

---

## 📧 Contact & Support

For questions, suggestions, or issues:

- **Open an issue** on GitHub
- **Email:** your.email@example.com
- **Documentation:** [Wiki](https://github.com/yourrepo/wiki)

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with 🐍 and ☕

</div>