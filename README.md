# 🌿 PlantPedia

**PlantPedia** is a web-based plant identification system that uses a Convolutional Neural Network (CNN) to recognize plant species from uploaded images. The system is designed to provide fast, accurate predictions, along with educational insights on identified plants.

---

## 📁 Project Structure

```
PlantPedia/
├── website/                    # Flask app package
│   ├── app.py                  # Main Flask application
│   └── templates/              # HTML templates
│       ├── index.html          # Homepage with upload form
│       ├── result.html         # Displays prediction + info
│       └── about.html          # About the project
│
├── data/
│   └── database.csv            # Plant info referenced in results
│
├── models/
│   └── E35_D5_LeakyRelu_0.0005_A94.h5  # Trained CNN model (rename for clarity)
│
├── training/
│   └── leakyRelu_3dense_70_15_10.ipynb       # Jupyter notebook for training
│
├── .gitignore
├── requirements.txt
├── Procfile
└── README.md

```

---

## 🚀 How to Run Locally

### 1. 📦 Install Dependencies

Make sure Python is installed. Then install Flask and other required packages:

```bash
pip install -r requirements.txt
```

### 2. ▶️ Start the Flask Server

```bash
cd website
python app.py
```

### 3. 🌐 Open in Browser

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🌱 Features

- 🌿 **Upload Image**: Identify a plant by uploading its image.
- 📊 **Prediction Results**: Displays plant species and related data in table format.
- 🧠 **CNN-Based Model**: Uses a trained `.h5` deep learning model for classification.
- 📖 **About Page**: Highlights the features and benefits of PlantPedia.
- 🎨 **Modern UI**: Responsive, accessible, and clean front-end built with HTML/CSS.

---

## 🔒 Deployment

- This app is intended for **local use** or deployment on **oracleVM**.
- also configured for Heroku or public cloud,.

---

## 👨‍💻 Contributors

- Mani Jain (221648)  
- Mansi Jain (2216049)  
- Shruti Agarwal (2216077)

---

## 📄 License

*This project does not use any license.*

---

## 📸 Sample Use

1. Open the home page (`index.html`)
2. Upload a JPG/PNG image of a plant
3. Get predictions + plant details in `result.html`

---

## 🙌 Acknowledgements

- Dataset preprocessing and training done prior to deployment


> _"Empowering people to identify, learn, and explore the green world around them."_