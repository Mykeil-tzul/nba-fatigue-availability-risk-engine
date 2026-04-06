"""
Evaluation helpers for trained models.
"""

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def evaluate_classification_model(y_true, y_pred) -> dict:
    """
    Return standard classification metrics.
    """
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }