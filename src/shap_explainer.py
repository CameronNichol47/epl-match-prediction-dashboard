from pathlib import Path
import shap
import joblib

PROJECT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_DIR / "models" / "xgboost_model.pkl"


def load_model():
    model = joblib.load(MODEL_PATH)
    return model

def create_explainer():
    model = load_model()
    explainer = shap.TreeExplainer(model)

    return explainer

def explain(X_match, prediction):
    ex = create_explainer()
    shap_values = ex(X_match)
    print(shap.__version__)
    class_shap = shap_values[:, :, prediction]
    shap.plots.waterfall(class_shap[0])

