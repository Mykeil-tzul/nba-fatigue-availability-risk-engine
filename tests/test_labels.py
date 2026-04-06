import pandas as pd
from src.labeling import create_performance_dip_label


def test_create_performance_dip_label():
    df = pd.DataFrame(
        {
            "points": [20, 10],
            "rolling_points_2": [18, 15],
        }
    )

    result = create_performance_dip_label(df)

    assert "performance_dip" in result.columns
    assert result["performance_dip"].tolist() == [0, 1]