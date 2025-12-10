from flask import Flask, render_template, request, send_from_directory
import os
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from PIL import Image, UnidentifiedImageError
import gdown

# --------------------------
# Google Drive model download
# --------------------------
def download_model_from_gdrive():
    # Go up one level to create/use 'models' folder outside 'website'
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(model_dir, exist_ok=True)

    model_filename = "E35_D5_LeakyRelu_0.0005_A94.h5"
    destination = os.path.join(model_dir, model_filename)

    if os.path.exists(destination):
        print("✅ Model file already exists.")
        return destination

    print("⬇️  Downloading model weights from Google Drive using gdown...")
    url = f"https://drive.google.com/uc?id=1AYaUN4QAskXZaN8kjv7Y92WjSgrUsCNC"
    gdown.download(url, destination, quiet=False)
    print("✅ Download complete.")
    return destination
    

def get_model():
    global model
    if 'model' not in globals():
        print("🔄 Loading model into memory...")
        model_path = download_model_from_gdrive()
        model = load_model(model_path)
        print("✅ Model loaded.")
    return model

# --------------------------
# Flask App
# --------------------------
app = Flask(__name__)

# Ensure the "uploads" directory exists
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Define class names (modify as per your dataset)
Class_names = [
    'Aloevera', 'Amar poi', 'Amla', 'Amruta_Balli', 'Arali', 'Ashoka', 
    'Ashwagandha', 'Astma_weed', 'Avacado', 'Badipala', 'Balloon_Vine', 
    'Bamboo', 'Basale', 'Beans', 'Betel', 'Betel_Nut', 'Bhrami', 
    'Bringaraja', 'Caricature', 'Castor', 'Catharanthus', 'Chakte', 
    'Chilly', 'Citron lime (herelikai)', 'Coffee', 'Common rue', 
    'Coriender', 'Curry_Leaf', 'Doddapatre', 'Drumstick', 'Ekka', 
    'Eucalyptus', 'Ganike', 'Gasagase', 'Geranium', 'Ginger', 
    'Globe Amarnath', 'Guava', 'Henna', 'Hibiscus', 'Honge', 'Insulin', 
    'Jackfruit', 'Jasmine', 'Kasambruga', 'Kohlrabi', 'Lantana', 'Lemon', 
    'Lemon_grass', 'Malabar_Nut', 'Mango', 'Marigold', 'Mint', 'Nagadali', 
    'Neem', 'Nelavembu', 'Nerale', 'Nooni', 'Onion', 'Padri', 
    'Palak(Spinach)', 'Papaya', 'Parijatha', 'Pea', 'Pepper', 'Pomegranate', 
    'Pumpkin', 'Raddish', 'Raktachandini', 'Rose', 'Sampige', 'Sapota', 
    'Seethaashoka', 'Seethapala', 'Tamarind', 'Taro', 'Tecoma', 'Thumbe', 
    'Tomato', 'Tulsi', 'Turmeric', 'Wood_sorel', 'camphor', 'kamakasturi', 
    'kepala'
]

# --------------------------
# Image Preprocessing
# --------------------------
def preprocess_image(image_path):
    try:
        # Try to open safely
        img = Image.open(image_path).convert("RGB")
    except UnidentifiedImageError:
        raise ValueError("❌ Unsupported image format. Please upload a JPG or PNG.")

    # Resize to match model input
    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# --------------------------
# Routes
# --------------------------
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def fetch_data_from_csv(class_name):
    # Update with the correct CSV file path
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "database.csv"))

    # Ensure column names match exactly
    if "Common Name" not in df.columns:
        print("Error: 'Common Name' column not found in CSV")
        return None

    # Filter rows where "Common Name" matches
    class_data = df[df["Common Name"] == class_name]

    return class_data.to_dict(orient='records') if not class_data.empty else None


@app.route("/", methods=["GET", "POST"])
def upload_and_predict():
    if request.method == "POST":
        file = request.files["image"]
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            try:
                preprocessed_image = preprocess_image(file_path)
                model = get_model()
                predictions = model.predict(preprocessed_image)
                predicted_class_ind = np.argmax(predictions, axis=-1)[0]
                pred_class_name = Class_names[predicted_class_ind]

                data = fetch_data_from_csv(pred_class_name)

                return render_template(
                    "result.html",
                    class_name=pred_class_name,
                    data=data if data else None,
                    input_image_path=f"/uploads/{filename}"
                )

            except ValueError as e:
                # Show error if bad/unsupported image
                return render_template("index.html", error_message=str(e))

    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
