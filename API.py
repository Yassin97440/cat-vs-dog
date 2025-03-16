from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
from PIL import Image
import numpy as np
import io

app = FastAPI()

# Charger le modèle entraîné
try:
    model = tf.keras.models.load_model("cat_vs_dog_model.h5", compile=False)
except Exception as e:
    print(f"Erreur lors du chargement du modèle: {e}")
    # Solution alternative si le premier chargement échoue
    model = tf.keras.models.load_model("cat_vs_dog_model.h5", 
                                      custom_objects=None, 
                                      compile=False)

# Fonction de prétraitement
def preprocess_image(image: Image.Image):
    # Vérifier si l'image est en RGB, sinon la convertir
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize((128, 128))  # Adapter à la taille du modèle
    image = np.array(image) / 255.0   # Normalisation
    image = np.expand_dims(image, axis=0)  # Ajouter la dimension batch
    return image

def normalize_and_prepare_prediction(prediction_value):
    # Normalisation des probabilités pour avoir une somme de 100%
    prob_chien = prediction_value
    prob_chat = 1 - prediction_value
    
    predict_animal='inconnu'
    if prediction_value > 0.5:
        predict_animal='Chien'
        confidence = prob_chien

    else:
        predict_animal='Chat'
        confidence = prob_chat
    print("pred name :", predict_animal)
    # Conversion en pourcentage
    prediction_value = round(confidence * 100, 3)
    print("proba : ", prediction_value)
    return  predict_animal, prediction_value
    

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    input_data = preprocess_image(image)
    prediction = model.predict(input_data)
    
    # Convertir la prédiction en valeur flottante pour la sérialisation JSON
    prediction_value = float(prediction[0][0]) if prediction.ndim > 1 else float(prediction[0])
    
    predict_animal, prediction_value = normalize_and_prepare_prediction(prediction_value)
    
    print("name : ",predict_animal,"proba", prediction_value)
    return {
        "className": predict_animal,
        "confidence": prediction_value
    }
