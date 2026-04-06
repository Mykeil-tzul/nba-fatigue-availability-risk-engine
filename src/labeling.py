"""
Label creation for performance dip modeling.
"""

import pandas as pd


def create_performance_dip_label(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a binary target for whether a player's points
    fall below their recent rolling average.

    Parameters
    ----------
    df : pd.DataFrame
        Feature-engineered NBA game log data.

    Returns
    -------
    pd.DataFrame
        Data with performance dip label.
    """
    labeled_df = df.copy()

    labeled_df["performance_dip"] = (
        labeled_df["pts"] < labeled_df["rolling_pts_3"]
    ).astype(int)

    return labeled_df