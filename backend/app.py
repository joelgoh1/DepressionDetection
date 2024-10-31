import speech_recognition as sr
import pyttsx3
import re
import string
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to normalize text input
def normalize_answer(s):
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text, flags=re.UNICODE)
    def white_space_fix(text):
        return ' '.join(text.split())
    def remove_punc(text):
        return ''.join(ch for ch in text if ch not in set(string.punctuation))
    def lower(text):
        return text.lower()
    return white_space_fix(remove_articles(remove_punc(lower(s))))

# Function to convert text to speech
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# API call to the local machine learning model server
def generate_response(text, emotion, priority):
    prompt = f"""
    You are an empathetic and understanding assistant. The user provides a message, and you respond considering the emotion and priority they indicate.

    Message: "{text}"
    Emotion: "{emotion}"
    Priority: "{priority}"

    Respond to the message in a way that acknowledges the emotion and focuses on the priority segment provided.
    """
    data = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "seed": 123}
    }
    response = requests.post('http://localhost:11434/api/generate', json=data)
    return response.json()['response']

@app.route('/listen', methods=['GET'])
def listen_and_respond():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise; please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=2)
            speech_text = recognizer.recognize_google(audio)
            normalized_text = normalize_answer(speech_text)
            # Example static call for emotion and priority
            response = generate_response(normalized_text, "calm", "high")
            return jsonify({"speech_text": speech_text, "normalized_text": normalized_text, "response": response})
        except sr.WaitTimeoutError:
            return jsonify({"error": "No speech detected within 10 seconds."}), 408
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand the audio."}), 400
        except sr.RequestError:
            return jsonify({"error": "Request error while recognizing the speech."}), 503
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

