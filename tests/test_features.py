import pandas as pd
from src.feature_engineering import add_basic_fatigue_features


def test_add_basic_fatigue_features():
    df = pd.DataFrame(
        {
            "player_name": ["Player A", "Player A"],
            "game_date": ["2025-01-01", "2025-01-02"],
            "minutes": [30, 35],
            "points": [20, 25],
            "assists": [5, 6],
            "rebounds": [4, 5],
            "is_back_to_back": [0, 1],
            "days_rest": [2, 0],
            "home_game": [1, 0],
        }
    )

    result = add_basic_fatigue_features(df)

    assert "rolling_minutes_2" in result.columns
    assert "rolling_points_2" in result.columns
    assert "workload_score" in result.columns