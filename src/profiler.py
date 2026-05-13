from typing import Dict, Any, List
import numpy as np
import pandas as pd

def get_column_groups(df: pd.DataFrame) -> Dict[str, List[str]]:
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    datetime_columns = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()
    categorical_columns = [
        col for col in df.columns
        if col not in numeric_columns and col not in datetime_columns
    ]
    return {
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "datetime_columns": datetime_columns,
    }

def detect_possible_outliers(df: pd.DataFrame, numeric_columns: List[str]) -> pd.DataFrame:
    rows = []
    for col in numeric_columns:
        series = df[col].dropna()
        if series.empty:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        count = int(((series < lower) | (series > upper)).sum())
        rows.append({
            "column": col,
            "lower_bound": round(float(lower), 4),
            "upper_bound": round(float(upper), 4),
            "possible_outlier_count": count,
            "possible_outlier_rate": round(count / len(series), 4),
        })
    return pd.DataFrame(rows)

def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    groups = get_column_groups(df)
    numeric_columns = groups["numeric_columns"]
    categorical_columns = groups["categorical_columns"]

    column_types = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(dtype) for dtype in df.dtypes],
        "non_null_count": [int(df[col].notna().sum()) for col in df.columns],
        "unique_count": [int(df[col].nunique(dropna=True)) for col in df.columns],
    })

    missing_values = pd.DataFrame({
        "column": df.columns,
        "missing_count": [int(df[col].isna().sum()) for col in df.columns],
        "missing_rate": [round(float(df[col].isna().mean()), 4) for col in df.columns],
    }).sort_values("missing_rate", ascending=False)

    descriptive_statistics = (
        df[numeric_columns].describe().transpose().round(4)
        if numeric_columns
        else pd.DataFrame()
    )

    possible_outliers = detect_possible_outliers(df, numeric_columns)

    if len(numeric_columns) >= 2:
        correlation_matrix = df[numeric_columns].corr(numeric_only=True).round(4)
    else:
        correlation_matrix = pd.DataFrame()

    top_categories = {}
    for col in categorical_columns[:10]:
        top_categories[col] = (
            df[col].astype(str).value_counts(dropna=False).head(10).to_dict()
        )

    return {
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "column_types": column_types,
        "missing_values": missing_values,
        "descriptive_statistics": descriptive_statistics,
        "possible_outliers": possible_outliers,
        "correlation_matrix": correlation_matrix,
        "top_categories": top_categories,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "datetime_columns": groups["datetime_columns"],
    }

def _df_to_records(df: pd.DataFrame, max_rows: int = 20):
    if df is None or df.empty:
        return []
    return df.head(max_rows).replace({np.nan: None}).to_dict(orient="records")

def build_llm_profile_summary(profile: Dict[str, Any]) -> Dict[str, Any]:
    correlation_matrix = profile["correlation_matrix"]
    strongest_correlations = []

    if not correlation_matrix.empty:
        cols = correlation_matrix.columns
        for i, col1 in enumerate(cols):
            for col2 in cols[i + 1:]:
                corr = correlation_matrix.loc[col1, col2]
                if pd.notna(corr):
                    strongest_correlations.append({
                        "column_1": col1,
                        "column_2": col2,
                        "correlation": round(float(corr), 4),
                    })

        strongest_correlations = sorted(
            strongest_correlations,
            key=lambda x: abs(x["correlation"]),
            reverse=True,
        )[:10]

    descriptive_stats = []
    if not profile["descriptive_statistics"].empty:
        descriptive_stats = _df_to_records(
            profile["descriptive_statistics"].reset_index(names="column"),
            50,
        )

    return {
        "row_count": profile["row_count"],
        "column_count": profile["column_count"],
        "numeric_columns": profile["numeric_columns"],
        "categorical_columns": profile["categorical_columns"],
        "datetime_columns": profile["datetime_columns"],
        "column_types": _df_to_records(profile["column_types"], 50),
        "missing_values": _df_to_records(profile["missing_values"], 50),
        "descriptive_statistics": descriptive_stats,
        "possible_outliers": _df_to_records(profile["possible_outliers"], 50),
        "strongest_correlations": strongest_correlations,
        "top_categories": profile["top_categories"],
    }
