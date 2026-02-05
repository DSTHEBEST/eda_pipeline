import numpy as np

def classify_columns(df):
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    return num_cols, cat_cols

import numpy as np

def cohens_d(group1, group2):

    mean1 = np.mean(group1)
    mean2 = np.mean(group2)

    std1 = np.std(group1, ddof=1)
    std2 = np.std(group2, ddof=1)

    n1 = len(group1)
    n2 = len(group2)

    pooled_std = np.sqrt(
        ((n1 - 1)*std1**2 + (n2 - 1)*std2**2) / (n1 + n2 - 2)
    )

    return (mean1 - mean2) / pooled_std



def detect_outliers(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return ((series < lower) | (series > upper)).sum()
