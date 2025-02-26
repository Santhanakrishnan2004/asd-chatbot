import os
import flask
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
CORS(app)

# Load API Key from Environment Variable
API_KEY = os.environ.get("API_KEY")

# Configure Google Gemini API
genai.configure(api_key=API_KEY)

# Load Firebase credentials from environment variable (stored as JSON string)
# FIREBASE_CREDENTIALS = os.environ.get("FIREBASE_CREDENTIALS")
# if FIREBASE_CREDENTIALS:
#     cred = credentials.Certificate(eval(FIREBASE_CREDENTIALS))
#     firebase_admin.initialize_app(cred, {'databaseURL': os.environ.get("DATABASE_URL")})

@app.route('/chat-asd', methods=['POST'])
def chat_asd():
    data = request.get_json()
    input_text = data.get("input", "")

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input_text)

    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True)
