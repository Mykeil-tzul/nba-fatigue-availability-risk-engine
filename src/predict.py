"""
Prediction helpers for scoring NBA fatigue risk.
"""

import joblib
import pandas as pd

from src.train import FEATURE_COLUMNS


def load_model(model_path: str):
    """
    Load a saved model from disk.
    """
    return joblib.load(model_path)


def generate_predictions(df: pd.DataFrame, model) -> pd.DataFrame:
    """
    Generate fatigue predictions and probabilities.
    """
    scored_df = df.copy()

    scored_df["predicted_performance_dip"] = model.predict(scored_df[FEATURE_COLUMNS])
    scored_df["dip_probability"] = model.predict_proba(scored_df[FEATURE_COLUMNS])[:, 1]
    scored_df["fatigue_risk_score"] = (scored_df["dip_probability"] * 100).round(1)

    return scored_df


def format_prediction_output(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep the most useful columns for reporting and dashboards.
    """
    columns_to_keep = [
        "player_name",
        "game_date",
        "min",
        "pts",
        "ast",
        "reb",
        "days_rest",
        "is_back_to_back",
        "workload_score",
        "predicted_performance_dip",
        "dip_probability",
        "fatigue_risk_score",
    ]

    available_columns = [col for col in columns_to_keep if col in df.columns]
    return df[available_columns].sort_values(
        by=["fatigue_risk_score", "player_name", "game_date"],
        ascending=[False, True, True]
    ).reset_index(drop=True)