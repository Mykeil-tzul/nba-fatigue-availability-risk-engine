from src.data_collection import create_sample_game_log
from src.preprocessing import preprocess_game_logs
from src.feature_engineering import add_basic_fatigue_features
from src.labeling import create_performance_dip_label


def test_pipeline_runs_end_to_end():
    df = create_sample_game_log()
    df = preprocess_game_logs(df)
    df = add_basic_fatigue_features(df)
    df = create_performance_dip_label(df)

    assert not df.empty
    assert "performance_dip" in df.columns