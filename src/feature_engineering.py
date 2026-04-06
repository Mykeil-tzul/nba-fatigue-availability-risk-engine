"""
Feature engineering for NBA fatigue and workload metrics.
"""

import pandas as pd


def add_basic_fatigue_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add fatigue-related features using real NBA game log columns.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned NBA game log data.

    Returns
    -------
    pd.DataFrame
        Data with engineered features.
    """
    featured_df = df.copy()

    # Days of rest since previous game for each player
    featured_df["days_rest"] = (
        featured_df.groupby("player_name")["game_date"]
        .diff()
        .dt.days
    )

    # Fill first game missing rest value with 3
    featured_df["days_rest"] = featured_df["days_rest"].fillna(3)

    # Back-to-back flag: 1 if only 1 day between games
    featured_df["is_back_to_back"] = (featured_df["days_rest"] == 1).astype(int)

    # Rolling averages by player
    featured_df["rolling_min_3"] = (
        featured_df.groupby("player_name")["min"]
        .transform(lambda s: s.rolling(3, min_periods=1).mean())
    )

    featured_df["rolling_pts_3"] = (
        featured_df.groupby("player_name")["pts"]
        .transform(lambda s: s.rolling(3, min_periods=1).mean())
    )

    featured_df["rolling_ast_3"] = (
        featured_df.groupby("player_name")["ast"]
        .transform(lambda s: s.rolling(3, min_periods=1).mean())
    )

    featured_df["rolling_reb_3"] = (
        featured_df.groupby("player_name")["reb"]
        .transform(lambda s: s.rolling(3, min_periods=1).mean())
    )

    # Simple workload score
    featured_df["workload_score"] = (
        featured_df["min"] * 0.5
        + featured_df["pts"] * 0.2
        + featured_df["is_back_to_back"] * 8
        + (1 / (featured_df["days_rest"] + 1)) * 5
    )

    return featured_df