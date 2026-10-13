
import json
from pathlib import Path

import numpy as np
import tensorflow as tf

PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_DIR / "models" / "fruit_freshness_model.keras"
LABELS_PATH = PROJECT_DIR / "models" / "class_names.json"

print("TensorFlow version:", tf.__version__)

# Check that both files exist
assert MODEL_PATH.exists(), f"Model not found: {MODEL_PATH}"
assert LABELS_PATH.exists(), f"Class labels not found: {LABELS_PATH}"

# Load the saved model and class labels
model = tf.keras.models.load_model(MODEL_PATH)

with open(LABELS_PATH, "r", encoding="utf-8") as file:
    class_names = json.load(file)

print("Model loaded successfully.")
print("Input shape:", model.input_shape)
print("Output shape:", model.output_shape)
print("Classes:", class_names)

# Smoke test: verify that the model accepts an image-shaped tensor
height, width = model.input_shape[1:3]
dummy_image = np.zeros((1, height, width, 3), dtype=np.float32)

predictions = model.predict(dummy_image, verbose=0)
assert predictions.shape == (1, len(class_names)), (
    f"Unexpected prediction shape: {predictions.shape}"
)
assert np.isfinite(predictions).all(), "Predictions contain invalid values."

print("Inference smoke test passed.")
print("Output values:", predictions[0])
