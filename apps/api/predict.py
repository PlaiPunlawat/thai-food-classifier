import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "packages" / "shared"))

import numpy as np
from keras_preprocessing.image import load_img
from keras_preprocessing.image import img_to_array
from keras.models import load_model
from keras.applications.xception import preprocess_input
from food_labels import FOOD_LABELS

MODEL_MOBILENET = load_model("./models/MobileNet.h5")
MODEL_XCEPTION = load_model("./models/Xception.h5")


def predict_image(filepath, model="xception"):

    if model != "xception" and model != "mobilenet":
        model = "mobilenet"

    selected_model = MODEL_MOBILENET if model == "mobilenet" else MODEL_XCEPTION

    img = load_img(filepath, target_size=(128, 128))
    img = img_to_array(img)
    img = preprocess_input(img)
    img /= 255
    img = np.expand_dims(img, axis=0)

    y_pred_prob = selected_model.predict(img, workers=8).flatten()

    top_indices = np.argsort(y_pred_prob)[::-1][:5]

    results = []
    for idx in top_indices:
        confidence = float(y_pred_prob[idx]) * 100
        results.append({
            "name_en": FOOD_LABELS[idx]["name_en"],
            "name_th": FOOD_LABELS[idx]["name_th"],
            "percent": f"{confidence:.2f}"
        })

    return results
