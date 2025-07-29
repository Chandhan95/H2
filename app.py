from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Load the trained KNN model
model = joblib.load(os.path.join("model", "Heart-Prediction-KNN-Classifier.joblib"))

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "saichandhan95155@gmail.com"  # Your Gmail
SENDER_PASSWORD = "wypz umae nldv ryxp"  # App password

def send_email_to_user(prediction, user_email):
    if prediction == 1:
        result_text = "Based on the given data, our model predicted that the person may get heart disease."
    else:
        result_text = "Based on the given data, our model predicted that the person may not get heart disease."

    subject = "Heart Disease Prediction Result"
    body = f"{result_text}\n\nThank you for using our Heart Disease Prediction service."

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def home():
    return render_template('index.html', prediction_text='')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_features = [float(request.form[key]) for key in request.form if key != 'email']
        user_email = request.form.get('email')

        if len(input_features) != 13:
            return jsonify({'error': 'Please provide exactly 13 input features.'})

        columns = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
                   "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
        input_data = pd.DataFrame([input_features], columns=columns)
        prediction = model.predict(input_data)
        send_email_to_user(prediction[0], user_email)
        return render_template('index.html', prediction_text=f'Heart Prediction (0 = No Disease, 1 = Disease): {prediction[0]}')
    except Exception as e:
        return f"An error occurred:"
if __name__ == "__main__":
    app.run(debug=True)
