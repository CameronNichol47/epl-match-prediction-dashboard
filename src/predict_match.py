from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "logistic_regression.pkl"

model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
feature_names = model_data["feature_names"]
class_labels = model_data["class_labels"]

print(model)
print(feature_names)
print(class_labels)