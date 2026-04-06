"""
Model training script for the NBA fatigue project.
"""

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from src.config import MODELS_DIR, RANDOM_STATE, TEST_SIZE
from src.utils import ensure_directory


FEATURE_COLUMNS = [
    "min",
    "pts",
    "ast",
    "reb",
    "home_game",
    "win",
    "days_rest",
    "is_back_to_back",
    "rolling_min_3",
    "rolling_pts_3",
    "rolling_ast_3",
    "rolling_reb_3",
    "workload_score",
]


def plot_feature_importance(model, feature_names):
    """
    Plot feature importance from trained model.
    """
    importances = model.feature_importances_

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    }).sort_values(by="importance", ascending=False)

    print("\nTop Features Driving Fatigue Predictions:")
    print(importance_df)

    plt.figure()
    plt.barh(importance_df["feature"], importance_df["importance"])
    plt.gca().invert_yaxis()
    plt.title("Feature Importance - Fatigue Model")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig("reports/feature_importance.png")
    plt.close()


def train_model(df: pd.DataFrame) -> RandomForestClassifier:
    """
    Train a classification model to predict performance dips.
    """
    modeling_df = df.dropna(subset=FEATURE_COLUMNS + ["performance_dip"]).copy()

    X = modeling_df[FEATURE_COLUMNS]
    y = modeling_df["performance_dip"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    model = RandomForestClassifier(random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions, zero_division=0))

    ensure_directory(MODELS_DIR)
    model_path = MODELS_DIR / "fatigue_model.pkl"
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")

    # 👇 THIS IS NEW (feature importance)
    plot_feature_importance(model, FEATURE_COLUMNS)

    return model