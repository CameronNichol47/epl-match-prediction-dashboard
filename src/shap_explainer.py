from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import shap


PROJECT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_DIR / "models" / "xgboost_model.pkl"


def load_model_data():
    saved_data = joblib.load(MODEL_PATH)

    if isinstance(saved_data, dict):
        model = saved_data["model"]
        feature_names = saved_data["feature_names"]
        class_labels = saved_data["class_labels"]
    else:
        model = saved_data
        feature_names = model.get_booster().feature_names
        class_labels = model.classes_.tolist()

    return model, feature_names, class_labels


def create_explainer():
    model, _, _ = load_model_data()
    return shap.TreeExplainer(model)


def explain(X_match, prediction):
    _, _, class_labels = load_model_data()

    explainer = create_explainer()
    shap_values = explainer(X_match)

    predicted_label = int(prediction)
    class_index = class_labels.index(predicted_label)

    class_shap = shap_values[:, :, class_index]

    plt.figure()

    shap.plots.waterfall(
        class_shap[0],
        max_display=10,
        show=False,
    )

    return plt.gcf()