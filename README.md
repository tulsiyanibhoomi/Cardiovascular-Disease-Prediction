# 🫀 Cardiovascular Disease Risk Prediction System

A Machine Learning–based web application that predicts the **risk of cardiovascular disease** based on patient health parameters.  
The project uses a **Flask backend** for model inference and a **Streamlit-based UI** for an interactive and user-friendly experience.

---

### 🌐 Live Demo
🔗 [https://cardiovascular-disease-prediction-haql279rlazydhwkyfrdj4.streamlit.app/](https://cardiovascular-disease-prediction-haql279rlazydhwkyfrdj4.streamlit.app/)

---

## 🚀 Project Overview

Cardiovascular diseases (CVDs) are among the leading causes of death worldwide. Early detection can significantly improve patient outcomes.  
This project aims to assist in **early risk assessment** by leveraging machine learning techniques on medical data.

The system allows users to input health metrics such as age, cholesterol level, blood pressure, and lifestyle factors, and then predicts whether the individual is at **risk of cardiovascular disease**.

---

## 🧠 Machine Learning Model

- **Type:** Supervised Machine Learning (Classification)
- **Algorithm:** Gradient Boosting
- **Input:** Patient medical and lifestyle attributes
- **Output:** Risk prediction (At Risk / Not At Risk)
- **Model Training:** Performed using historical cardiovascular disease datasets
- **Preprocessing:**  
  - Handling missing values  
  - Feature scaling  
  - Encoding categorical variables  

---

## 🖥️ Tech Stack

### Frontend (UI)
- **Streamlit** – Interactive web interface

### Backend
- **Flask** – REST API for model prediction
- **Python**

### Machine Learning
- **Scikit-learn**
- **Pandas**
- **NumPy**

---

## 📊 Features

- User-friendly web interface
- Real-time cardiovascular disease risk prediction
- Machine learning–powered decision making
- Clean separation of frontend and backend
- Scalable and modular architecture

---

## 🗂️ Project Structure

- app.py # Flask backend API
- streamlit_app.py # Streamlit UI application
- model.pkl # Trained ML model
- requirements.txt # Project dependencies
- data/ # Dataset 
- notebooks/ # Jupyter notebooks for EDA & training
- README.md # Project documentation

---

## ⚙️ Installation & Setup

### Clone the Repository
```bash
git clone https://github.com/tulsiyanibhoomi/Cardiovascular-Disease-Prediction.git
cd Cardiovascular-Disease-Prediction
```
### Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Start Flask backend
```bash
python app.py
```
### Start streamlit frontend
```bash
Start Streamlit Frontend
```

---

### 🧪 Sample Input Parameters
- Age  
- Gender
- Height
- Weight
- Resting Blood Pressure (Systolic and Diastolic)
- Cholesterol Level  
- Fasting Blood Sugar  
- Smoking Status
- Alcohol intake status
- Physical Activity Level  

---

### 📈 Output
- **Prediction Result**
  - At Risk of Cardiovascular Disease  
  - Not At Risk of Cardiovascular Disease  

---

### 🔮 Future Enhancements
- Improve accuracy with advanced ML models
- Add authentication and authorization
- Store prediction history in a database
- Download full report

---

### ⚠️ Disclaimer
This application is intended **for educational and research purposes only**.  
It should **not be used as a substitute for professional medical advice**.

---

### 👩‍💻 Author
**Bhoomi Tulsiyani**  
GitHub: https://github.com/tulsiyanibhoomi  

---

⭐ If you find this project useful, please give it a star!


