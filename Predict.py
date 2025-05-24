import streamlit
import requests
from PIL import Image 
import io

def run(): 
    streamlit.title("Plant Disease Detector")
    streamlit.write("Upload a leaf image!")

    uploaded_file = streamlit.file_uploader("Choose an image", type=["jpg", "png"])

    @streamlit.cache_data(show_spinner=False)
    def load_image(file):
        return file.read()

    if uploaded_file is not None:
        uploaded_file.seek(0)
        image_bytes = load_image(uploaded_file)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((128, 128))
        streamlit.image(image, caption="Uploaded Image", use_column_width=True)

        if streamlit.button("Predict"):
            with streamlit.spinner("Thinking..."):
                try:
                    # Move file read here (Streamlit reuses `uploaded_file` object and closes it after read)
                    files = {"file": (uploaded_file.name, image_bytes, uploaded_file.type)}

                    response = requests.post("http://127.0.0.1:8000/predict/", files=files)
                    
                    if response.status_code == 200:
                        response_json = response.json()
                        if "prediction" in response_json and "confidence" in response_json:
                            prediction = response_json["prediction"]
                            confidence = response_json["confidence"]
                            streamlit.success(f"Prediction: **{prediction}**\n")
                            streamlit.success(f"Confidence: **{confidence}**")
                            print("Prediction displayed successfully")
                            print("🔎 Raw response from server:", response.text)
                        else:
                            streamlit.error(f"Server responded with: {response_json.get('error', 'Unknown error')}")
                    else:
                        streamlit.error("Prediction failed, please try again.")
                except requests.exceptions.Timeout:
                    streamlit.error("Request timed out. Try again!")
                except requests.exceptions.RequestException as e:
                    streamlit.error(f"Connection error: {e}")
