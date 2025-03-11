# Cat vs Dog Classifier

Je fais ce projet dans le cadre de mon auto-formation. Après avoir suivi une série de vidéo de MachineLearnia qui explique certains principes fondamentaux du machine et deep learning.

## 1. Classification Chat vs Chien - Approche native

Dans cette première partie du projet, j'ai exploré les concepts mathématiques fondamentaux de la classification d'images sans utiliser de frameworks avancés.

### Méthodologie
- Implémentation d'un réseau de neurones simple (perceptron multicouche)
- Extraction manuelle des caractéristiques des images (histogrammes de couleurs, détection de contours)
- Utilisation d'algorithmes classiques comme la descente de gradient
- Normalisation des données et techniques de prétraitement basiques

### Résultats
J'ai obtenu des résultats encourageants avec cette approche, atteignant une précision d'environ 70% sur mon jeu de test. Cette expérience m'a permis de comprendre les fondements mathématiques qui sous-tendent les réseaux de neurones avant de passer à des outils plus sophistiqués.

## 2. Classification avec TensorFlow

Après avoir eu de bons scores sur le petit réseau de perceptron, je suis passé sur TensorFlow pour améliorer les performances.

### Découverte des CNN
J'ai commencé par explorer les réseaux de neurones convolutifs (CNN), qui sont particulièrement adaptés aux tâches de vision par ordinateur. J'ai pu voir que les réseaux convolutifs offrent de superbes résultats sur des problématiques de classification d'images.

### Préparation des données
- Adaptation du jeu de données pour TensorFlow (redimensionnement, normalisation)
- Augmentation des données pour améliorer la généralisation (rotations, zoom, flips)
- Division en ensembles d'entraînement, de validation et de test

### Expérimentation
J'ai expérimenté avec différentes architectures et hyperparamètres :
- Variation du nombre de couches convolutives
- Ajustement des tailles de filtres
- Test de différentes fonctions d'activation
- Optimisation des taux d'apprentissage
- Implémentation de techniques de régularisation (dropout, batch normalization)

### Transfer Learning
Face aux limitations en termes de données et de puissance de calcul, j'ai opté pour le transfert d'apprentissage :
- Utilisation d'un modèle pré-entraîné (MobileNet/VGG/ResNet)
- Fine-tuning des dernières couches pour adapter le modèle à ma classification binaire
- Amélioration significative des performances (précision >95%)
- Réduction considérable du temps d'entraînement
- Optimisation de la taille du modèle final pour le déploiement

## 3. Déploiement avec FastAPI

Pour rendre mon modèle accessible et utilisable, j'ai développé une API simple avec FastAPI.

### Fonctionnalités
- Endpoint pour télécharger une image et obtenir une prédiction
- Prétraitement automatique des images soumises
- Réponse JSON avec la classe prédite et le niveau de confiance

### Implémentation
```python
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    input_data = preprocess_image(image)
    prediction = model.predict(input_data)
    
    prediction_value = float(prediction[0][0]) if prediction.ndim > 1 else float(prediction[0])
    
    predict_animal = 'Chat' if prediction_value <= 0.5 else 'Chien'
    
    return {
        "classe": predict_animal,
        "confiance": prediction_value
    }
```

### Déploiement
- Installation simple avec pip
- Documentation automatique via Swagger UI
- Possibilité de déployer sur différentes plateformes (Heroku, AWS, etc.)

## Conclusion

Ce projet m'a permis d'explorer le cycle complet du développement d'un modèle de deep learning, de la compréhension des concepts fondamentaux jusqu'au déploiement d'une solution fonctionnelle. J'ai pu constater l'efficacité des réseaux convolutifs et du transfer learning pour la classification d'images, ainsi que la facilité de mise en production avec des outils modernes comme FastAPI.

## Prochaines étapes
- Amélioration de l'interface utilisateur
- Extension à d'autres classes d'animaux
- Optimisation des performances de l'API
- Déploiement sur une plateforme cloud

