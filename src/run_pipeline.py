"""
End-to-end pipeline runner for the NBA Fatigue + Availability Risk Engine project.
"""

import pandas as pd

from src.preprocessing import preprocess_game_logs
from src.feature_engineering import add_basic_fatigue_features
from src.labeling import create_performance_dip_label
from src.train import train_model


def run_pipeline():
    """
    Run the full pipeline on real multi-player NBA data.
    """
    print("Step 1: Loading real multi-player data...")
    df = pd.read_csv("data/raw/multi_player_game_logs.csv")

    print("Step 2: Preprocessing game logs...")
    df = preprocess_game_logs(df)

    print("Step 3: Engineering fatigue features...")
    df = add_basic_fatigue_features(df)

    print("Step 4: Creating target labels...")
    df = create_performance_dip_label(df)

    print("Step 5: Training model...")
    model = train_model(df)

    print("Pipeline completed successfully.")
    return df, model


if __name__ == "__main__":
    run_pipeline()