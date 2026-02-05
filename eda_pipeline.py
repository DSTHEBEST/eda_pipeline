import os
import yaml
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sweetviz as sv
from utils import classify_columns, detect_outliers, cohens_d


from scipy.stats import ttest_ind, f_oneway, chi2_contingency

from logger import get_logger
from utils import classify_columns, detect_outliers

logger = get_logger()


# ------------------------------
# Custom Technical Palette
# ------------------------------
CUSTOM_PALETTE = [
    "#003f5c",
    "#58508d",
    "#bc5090",
    "#ff6361",
    "#ffa600"
]

sns.set_theme(style="whitegrid")
sns.set_palette(CUSTOM_PALETTE)

plt.rcParams["figure.figsize"] = (10, 6)


class EDAPipeline:

    def __init__(self, config_path):

        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

        self.df = None
        self.report_path = self.config["report_path"]

        os.makedirs(self.report_path, exist_ok=True)

    # ----------------------------------
    def load_data(self):

        logger.info("Loading dataset")
        self.df = pd.read_csv(self.config["data_path"])
        logger.info(f"Dataset shape: {self.df.shape}")

    # ----------------------------------
    def drop_id_columns(self):

        ids = self.config.get("id_columns", [])
        self.df.drop(columns=ids, inplace=True, errors="ignore")
        logger.info("ID columns removed")

    # ----------------------------------
    def missing_value_analysis(self):

        missing = self.df.isnull().mean()
        missing = missing[missing > 0]
        missing.to_csv(self.report_path + "missing_values.csv")

    # ----------------------------------
    def duplicate_analysis(self):

        duplicates = self.df.duplicated().sum()
        logger.info(f"Duplicate rows: {duplicates}")

    # ----------------------------------
    def classify_columns(self):

        self.num_cols, self.cat_cols = classify_columns(self.df)

    # ----------------------------------
    # Distribution Plot
    # ----------------------------------
    def distribution_plots(self):

        if not self.config["plots"]["distribution"]:
            return

        for col in self.num_cols:

            plt.figure()

            sns.histplot(
                self.df[col],
                kde=True,
                bins=40,
                color=CUSTOM_PALETTE[0]
            )

            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")

            plt.tight_layout()
            plt.savefig(self.report_path + f"{col}_distribution.png")
            plt.close()

    # ----------------------------------
    # Target Analysis + T Test
    # ----------------------------------
    def target_analysis(self):

        if not self.config["plots"]["target_analysis"]:
            return

        target = self.config["target_column"]

        stats_results = []

        unique_groups = self.df[target].unique()

        # Works only for binary target
        if len(unique_groups) != 2:
            logger.warning("Cohen's D requires binary target.")
            return

        g1, g2 = unique_groups

        for col in self.num_cols:

            if col == target:
                continue

            group1 = self.df[self.df[target] == g1][col].dropna()
            group2 = self.df[self.df[target] == g2][col].dropna()

            # T-test
            _, p_value = ttest_ind(group1, group2)

            # Cohen's D
            effect_size = cohens_d(group1, group2)

            stats_results.append([col, p_value, effect_size])

            # Plot
            plt.figure()

            sns.boxplot(
                x=self.df[target],
                y=self.df[col],
                palette=[CUSTOM_PALETTE[1], CUSTOM_PALETTE[3]]
            )

            means = self.df.groupby(target)[col].mean()

            for i, mean in enumerate(means):
                plt.scatter(i, mean, color=CUSTOM_PALETTE[4], s=120)

            title = (
                f"{col} vs {target}\n"
                f"p = {p_value:.4e} | Cohen's D = {effect_size:.2f}"
            )

            plt.title(title)

            plt.tight_layout()
            plt.savefig(self.report_path + f"{col}_vs_target.png")
            plt.close()

        pd.DataFrame(
            stats_results,
            columns=["Feature", "p_value", "Cohens_d"]
        ).to_csv(self.report_path + "ttest_effectsize_results.csv", index=False)

    # ----------------------------------
    # Correlation Heatmap
    # ----------------------------------
    def correlation_analysis(self):

        if not self.config["plots"]["correlation"]:
            return

        corr = self.df[self.num_cols].corr()

        plt.figure(figsize=(10, 8))

        sns.heatmap(
            corr,
            annot=True,
            cmap=sns.color_palette(CUSTOM_PALETTE, as_cmap=True),
            fmt=".2f"
        )

        plt.title("Feature Correlation Matrix")
        plt.tight_layout()

        plt.savefig(self.report_path + "correlation.png")
        plt.close()

    # ----------------------------------
    # Feature vs Target Correlation
    # ----------------------------------
    def feature_target_correlation(self):

        target = self.config["target_column"]

        corr = self.df.corr(numeric_only=True)[target].drop(target)

        plt.figure()

        sns.barplot(
            x=corr.values,
            y=corr.index,
            color=CUSTOM_PALETTE[2]
        )

        plt.title(f"Correlation with {target}")
        plt.tight_layout()

        plt.savefig(self.report_path + "target_correlation.png")
        plt.close()

    # ----------------------------------
    # Categorical vs Target Chi-Square
    # ----------------------------------
    def categorical_statistical_tests(self):

        target = self.config["target_column"]
        results = []

        for col in self.cat_cols:

            contingency = pd.crosstab(self.df[col], self.df[target])

            chi2, p, _, _ = chi2_contingency(contingency)

            results.append([col, p])

            plt.figure()

            sns.countplot(
                x=self.df[col],
                hue=self.df[target],
                palette=CUSTOM_PALETTE
            )

            plt.title(f"{col} vs {target} (p={p:.4f})")
            plt.xticks(rotation=30)

            plt.tight_layout()
            plt.savefig(self.report_path + f"{col}_categorical.png")
            plt.close()

        pd.DataFrame(results, columns=["Feature", "Chi2_p_value"])\
            .to_csv(self.report_path + "chi2_results.csv", index=False)

    # ----------------------------------
    def outlier_analysis(self):

        if not self.config["outlier_detection"]:
            return

        results = {}

        for col in self.num_cols:
            results[col] = detect_outliers(self.df[col])

        pd.Series(results).to_csv(self.report_path + "outlier_counts.csv")

    # ----------------------------------
    def generate_sweetviz(self):

        try:
            report = sv.analyze(self.df)
            report.show_html(self.report_path + "sweetviz_report.html")

        except Exception as e:
            logger.error(f"Sweetviz failed: {e}")

    # ----------------------------------
    def run(self):

        self.load_data()
        self.drop_id_columns()
        self.missing_value_analysis()
        self.duplicate_analysis()
        self.classify_columns()
        self.distribution_plots()
        self.target_analysis()
        self.correlation_analysis()
        self.feature_target_correlation()
        self.categorical_statistical_tests()
        self.outlier_analysis()
        self.generate_sweetviz()

        logger.info("EDA Pipeline Completed")
