import numpy as np
from keras_preprocessing.image import load_img
from keras_preprocessing.image import img_to_array
from keras.models import load_model
from keras.applications.xception import preprocess_input
from foodnames import FOOD_NAME

MODEL_MOBILENET = load_model("./models/MobileNet.h5")
MODEL_XCEPTION = load_model("./models/Xception.h5")


def predict_image(filepath, model="xception"):

    if model != "xception" and model != "mobilenet":
        model = "mobilenet"

    print(model)

    selected_model = MODEL_MOBILENET if model == "mobilenet" else MODEL_XCEPTION if model == "xception" else None

    # Preprocess
    img = load_img(filepath, target_size=(128, 128))
    img = img_to_array(img)
    img = preprocess_input(img)
    img /= 255
    img = np.expand_dims(img, axis=0)

    # Predict result
    y_pred_prob = selected_model.predict(img, workers=8).flatten()

    ind_class = np.argpartition(y_pred_prob, -5)[-5:]
    top5_prob = y_pred_prob[ind_class] * 100

    top5_result = zip(FOOD_NAME[ind_class], top5_prob)
    sorted_top5 = [{"name": i[0].split(", ")[1], "name_th": i[0].split(", ")[0], "confident": float(i[1])} for i in sorted(
        top5_result, key=lambda item: item[1], reverse=True)]
    return sorted_top5
