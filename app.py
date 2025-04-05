from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Load the trained KNN model
model = joblib.load(r"C:\Users\saich\OneDrive\Desktop\HeartPredictionApp\Heart-Prediction-KNN-Classifier.joblib")

# Email Configuration (Modify with your email details)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "saichandhan_ganji@srmap.edu.in"  # Your Gmail address
SENDER_PASSWORD = "xtrt hvuv pahj xkwa"  # Use the app password here
def send_email_to_user(prediction, user_email):
    # Determine prediction message
    if prediction == 1:
        result_text = "Based on the given data,Our model predicted that the person may get heart disease."
    else:
        result_text = "Based on the given data,Our model predicted that the person may not get heart disease."

    # Prepare the email content
    subject = "Heart Disease Prediction Result"
    body = f"{result_text}\n\nThank you for using our Heart Disease Prediction service."


    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = user_email  # Send to user's email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try: 
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, user_email, text)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from the form
    input_features = [float(x) for x in request.form.values() if x != request.form.get('email')]
    user_email = request.form.get('email')

    if len(input_features) != 13:
        return jsonify({'error': 'Please provide exactly 13 input features.'})
    
    # Define the column names (Adjust these to match the model's training data)
    columns = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", 
               "exang", "oldpeak", "slope", "ca", "thal"]

    # Convert input features to pandas DataFrame to match the model's training format
    input_data = pd.DataFrame([input_features], columns=columns)
    
    # Predict using the model
    prediction = model.predict(input_data)

    # Send email with the prediction result to the user
    send_email_to_user(prediction[0], user_email)

    # Return the prediction result to the user on the webpage
    return render_template('index.html', prediction_text=f'Heart Prediction (0 or 1): {prediction[0]}')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
