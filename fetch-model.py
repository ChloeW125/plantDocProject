from fastapi import FastAPI, File, UploadFile
from tensorflow.keras.models import load_model
from PIL import Image, UnidentifiedImageError
import numpy
import uvicorn 

model = load_model("plant_disease_model.keras")
# model = 
app = FastAPI()

class_names = [    
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___healthy',
    'Potato___Late_blight',
    'Tomato___Target_Spot',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___healthy',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites_Two-spotted_spider_mite',
    ]
# class_names = [
#     "Apple___Apple_scab",
#     "Apple___Black_rot",
#     "Apple___Cedar_apple_rust",
#     "Apple___healthy",
#     "Blueberry___healthy",
#     "Cherry_(including_sour)___Powdery_mildew",
#     "Cherry_(including_sour)___healthy",
#     "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
#     "Corn_(maize)___Common_rust_",
#     "Corn_(maize)___Northern_Leaf_Blight",
#     "Corn_(maize)___healthy",
#     "Grape___Black_rot",
#     "Grape___Esca_(Black_Measles)",
#     "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
#     "Grape___healthy",
#     "Orange___Haunglongbing_(Citrus_greening)",
#     "Peach___Bacterial_spot",
#     "Peach___healthy",
#     "Pepper,_bell___Bacterial_spot",
#     "Pepper,_bell___healthy",
#     "Potato___Early_blight",
#     "Potato___Late_blight",
#     "Potato___healthy",
#     "Raspberry___healthy",
#     "Soybean___healthy",
#     "Squash___Powdery_mildew",
#     "Strawberry___Leaf_scorch",
#     "Strawberry___healthy",
#     "Tomato___Bacterial_spot",
#     "Tomato___Early_blight",
#     "Tomato___healthy",
#     "Tomato___Late_blight",
#     "Tomato___Leaf_Mold",
#     "Tomato___Septoria_leaf_spot",
#     "Tomato___Spider_mites Two-spotted_spider_mite",
#     "Tomato___Target_Spot",
#     "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
#     "Tomato___Tomato_mosaic_virus"
# ]

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        file.file.seek(0)
        image = Image.open(file.file).convert("RGB").resize((128, 128))
        img_array = numpy.expand_dims(numpy.array(image) / 255.0, axis = 0)
        probabilities = model.predict(img_array)[0]
        prediction_index = numpy.argmax(probabilities)
        prediction_confidence = float(probabilities[prediction_index])*100
        return {
            "prediction": class_names[prediction_index],
            "confidence": round(prediction_confidence, 2)
            }
    except UnidentifiedImageError:
        return {"error": "Cannot process image. Please double-check and upload a valid image file."}
    except Exception as e:
        return {"error": f"Unexpected server error: {str(e)}"}
