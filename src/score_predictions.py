"""
Score NBA fatigue predictions using the trained model.
"""

from pathlib import Path
import pandas as pd

from src.config import MODELS_DIR, PREDICTIONS_DIR
from src.utils import ensure_directory
from src.preprocessing import preprocess_game_logs
from src.feature_engineering import add_basic_fatigue_features
from src.labeling import create_performance_dip_label
from src.predict import load_model, generate_predictions, format_prediction_output


def score_predictions() -> pd.DataFrame:
    """
    Load real NBA data, generate fatigue predictions, and save them.
    """
    print("Loading multi-player NBA data...")
    df = pd.read_csv("data/raw/multi_player_game_logs.csv")

    print("Preprocessing data...")
    df = preprocess_game_logs(df)

    print("Engineering features...")
    df = add_basic_fatigue_features(df)

    print("Creating labels...")
    df = create_performance_dip_label(df)

    print("Loading trained model...")
    model_path = MODELS_DIR / "fatigue_model.pkl"
    model = load_model(str(model_path))

    print("Generating predictions...")
    scored_df = generate_predictions(df, model)

    print("Formatting prediction output...")
    output_df = format_prediction_output(scored_df)

    ensure_directory(PREDICTIONS_DIR)
    output_path = PREDICTIONS_DIR / "fatigue_predictions.csv"
    output_df.to_csv(output_path, index=False)

    print(f"Predictions saved to: {output_path}")
    return output_df


if __name__ == "__main__":
    score_predictions()