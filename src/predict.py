
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image

PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_DIR / "models" / "fruit_freshness_model.keras"
LABELS_PATH = PROJECT_DIR / "models" / "class_names.json"

# Load the model and labels once when this module is imported.
model = tf.keras.models.load_model(MODEL_PATH)

with open(LABELS_PATH, "r", encoding="utf-8") as file:
    CLASS_NAMES = json.load(file)


def predict_fruit(image: Image.Image) -> dict:
    """Predict the fruit freshness class for a PIL image."""
    image = image.convert("RGB").resize((224, 224))

    image_array = np.asarray(image, dtype=np.float32)
    image_batch = np.expand_dims(image_array, axis=0)

    probabilities = model.predict(image_batch, verbose=0)[0]
    predicted_index = int(np.argmax(probabilities))

    return {
        "class_name": CLASS_NAMES[predicted_index],
        "confidence": float(probabilities[predicted_index]),
        "probabilities": {
            name: float(score)
            for name, score in zip(CLASS_NAMES, probabilities)
        },
    }
