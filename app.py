from flask import Flask, request, jsonify
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, db
from flask_cors import CORS
import traceback
import os
import json

app = Flask(__name__)
CORS(app)

# Load API Key from environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY environment variable")

genai.configure(api_key=GOOGLE_API_KEY)

# Firebase Initialization (if required)
FIREBASE_CREDENTIALS = os.environ.get("FIREBASE_CREDENTIALS")

if FIREBASE_CREDENTIALS:
    try:
        cred_dict = json.loads(FIREBASE_CREDENTIALS)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://your-database.firebaseio.com/"
        })
        print("Firebase Initialized")
    except Exception as e:
        print("Error initializing Firebase:", str(e))

@app.route("/chat-asd", methods=["POST"])
def chat_asd():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Prompt for AI Model
        prompt = (
            f"You are a chatbot that helps individuals with autism spectrum disorder (ASD). "
            f"Provide detailed and supportive advice for the following question: {user_message} "
            f"Your response should include helpful suggestions on activities, routines, or exercises for individuals with ASD."
        )

        # Call Google Generative AI
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if response and response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify(
                {"response": "I'm sorry, I couldn't find the information you need."}
            )

    except Exception as e:
        print("Error occurred:", e)
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render default port is 10000
    app.run(host="0.0.0.0", port=port, debug=True)
