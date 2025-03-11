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

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    input_data = preprocess_image(image)
    prediction = model.predict(input_data)
    
    # Convertir la prédiction en valeur flottante pour la sérialisation JSON
    prediction_value = float(prediction[0][0]) if prediction.ndim > 1 else float(prediction[0])
    
    predict_animal='inconnu'
    if prediction_value > 0.5:
        predict_animal='Chien'
    else:
        predict_animal='Chat'
    
    return {
        "class_name": predict_animal,
        "confidence": prediction_value
    }
