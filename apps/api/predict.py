import os
from pathlib import Path

import numpy as np
from huggingface_hub import hf_hub_download
from keras.models import load_model
from keras.preprocessing import image as keras_image
from food_labels import FOOD_LABELS

HF_REPO_ID = os.getenv("HF_MODEL_REPO", "PlaiPunlawat/thai-food-classifier")
MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", "./models")

_models = {}


def get_model_path(model_name: str) -> str:
    filename = {"xception": "Xception.h5", "mobilenet": "MobileNet.h5"}[model_name]
    return hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=filename,
        cache_dir=MODEL_CACHE_DIR,
    )


def _get_model(model_name: str):
    if model_name not in _models:
        model_path = get_model_path(model_name)
        _models[model_name] = load_model(model_path)
    return _models[model_name]


def predict_image(filepath, model="xception"):
    if model not in ("xception", "mobilenet"):
        model = "mobilenet"

    selected_model = _get_model(model)

    img = keras_image.load_img(filepath, target_size=(128, 128))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    predictions = selected_model.predict(img_array, verbose=0)
    top_indices = np.argsort(predictions[0])[::-1][:5]

    results = []
    for idx in top_indices:
        confidence = float(predictions[0][idx]) * 100
        results.append({
            "name_en": FOOD_LABELS[idx]["name_en"],
            "name_th": FOOD_LABELS[idx]["name_th"],
            "percent": f"{confidence:.2f}"
        })

    return results
