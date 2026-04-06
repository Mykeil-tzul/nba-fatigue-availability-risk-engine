"""
Preprocessing logic for real NBA player game log data.
"""

import pandas as pd


def preprocess_game_logs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize NBA game log data for modeling.

    Parameters
    ----------
    df : pd.DataFrame
        Raw NBA game log data.

    Returns
    -------
    pd.DataFrame
        Cleaned and standardized game log data.
    """
    cleaned_df = df.copy()

    # Standardize column names
    cleaned_df.columns = [col.lower() for col in cleaned_df.columns]

    # Convert game date to datetime
    cleaned_df["game_date"] = pd.to_datetime(cleaned_df["game_date"])

    # Create simple home/away indicator from matchup text
    # Example:
    # "DAL vs. SAC" -> home game
    # "DAL @ LAL"   -> away game
    cleaned_df["home_game"] = cleaned_df["matchup"].str.contains("vs.").astype(int)

    # Convert win/loss to binary
    cleaned_df["win"] = (cleaned_df["wl"] == "W").astype(int)

    # Sort by player and date
    cleaned_df = cleaned_df.sort_values(["player_name", "game_date"]).reset_index(drop=True)

    return cleaned_df