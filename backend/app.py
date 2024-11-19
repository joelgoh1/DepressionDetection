import speech_recognition as sr
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import torchaudio
import torch
import numpy as np
from speechbrain.pretrained import EncoderClassifier
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables for models
wav2vec2_processor = None
wav2vec2_model = None
emotion_model = None

def initialize_models():
    """Initialize all models at startup"""
    global wav2vec2_processor, wav2vec2_model, emotion_model
    
    print("Loading models... This might take a few minutes...")
    
    try:
        # Load Wav2Vec2 models
        wav2vec2_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
        wav2vec2_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        
        # Load Emotion Recognition model
        emotion_model = EncoderClassifier.from_hparams(
            source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
            savedir="./pretrained_emotion"
        )
        
        print("All models loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return False

def audio_data_to_tensor(audio_data):
    """Convert AudioData to tensor format required by the model"""
    audio_np = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
    
    audio_float = audio_np.astype(np.float32) / 32768.0
    waveform = torch.FloatTensor(audio_float)
    
    if len(waveform.shape) == 1:
        waveform = waveform.unsqueeze(0)
    
    if audio_data.sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(
            orig_freq=audio_data.sample_rate,
            new_freq=16000
        )
        waveform = resampler(waveform)
    
    return waveform


def classify_emotion(audio_data):
    """Classify emotion from AudioData object"""
    global emotion_model
    
    try:
        # Convert AudioData to tensor
        waveform = audio_data_to_tensor(audio_data)
        
        # Sliding window parameters
        window_size = 2.0  # seconds (increased for better phrase detection)
        step_size = 1.0    # seconds
        sample_rate = 16000  # Hz
        emotion_results = []
        phrase_emotion_scores = []

        # Process each window
        for i in range(0, waveform.shape[-1], int(step_size * sample_rate)):
            # Get window for current segment
            window = waveform[:, i:i + int(window_size * sample_rate)]
            if window.shape[-1] < window_size * sample_rate:
                break

            # Get emotion scores for this window
            score = emotion_model.mods.output_mlp(emotion_model.mods.wav2vec2(window))
            
            # Convert window to AudioData for transcription
            window_np = window.numpy().flatten()
            window_bytes = (window_np * 32767).astype(np.int16).tobytes()
            window_audio = sr.AudioData(
                window_bytes,
                sample_rate=sample_rate,
                sample_width=2
            )
            
            try:
                # Try to get transcription for this window
                transcription = sr.Recognizer().recognize_google(window_audio)
                if transcription.strip():  
                    avg_emotion_score = score[0].mean(axis = 0).tolist()
                    
                    phrase_emotion_scores.append({
                        "phrase": transcription,
                        "emotion_score": avg_emotion_score,
                        "overall_emotion": ['neutral', 'happy', 'sad', 'angry'][avg_emotion_score.index(max(avg_emotion_score))]
                    })
                

            except sr.UnknownValueError:
                # No speech detected in this window
                continue
            except Exception as e:
                print(f"Error processing window: {str(e)}")
                continue
        overall = {'neutral':0, 'happy':0, 'sad': 0, 'angry':0}

        for i in phrase_emotion_scores:
            overall[i['overall_emotion']] += 1
        overarching_emotion = max(overall, key = overall.get)

        has_emotion_changes = False
        emotion_change_text = ""
        
        if len(phrase_emotion_scores) > 1:
            for i in range(1, len(phrase_emotion_scores)):
                prev_dominant_idx = np.argmax(np.abs(phrase_emotion_scores[i-1]['emotion_score']))
                curr_dominant_idx = np.argmax(np.abs(phrase_emotion_scores[i]['emotion_score']))
                
                prev_magnitude = abs(phrase_emotion_scores[i-1]['emotion_score'][prev_dominant_idx])
                curr_magnitude = abs(phrase_emotion_scores[i]['emotion_score'][curr_dominant_idx])
                
                magnitude_threshold = 5.0 
                
                if (prev_dominant_idx != curr_dominant_idx and 
                    prev_magnitude > magnitude_threshold and 
                    curr_magnitude > magnitude_threshold):
                    
                    has_emotion_changes = True
                    emotion_change_text += f"\nEmotion shift detected: {phrase_emotion_scores[i-1]['phrase']} ({phrase_emotion_scores[i-1]['overall_emotion']}) → {phrase_emotion_scores[i]['phrase']} ({phrase_emotion_scores[i]['overall_emotion']})"

        return overarching_emotion, has_emotion_changes, emotion_change_text
        
    except Exception as e:
        print(f"Error in emotion classification: {str(e)}")
        raise

def generate_response(text, overarching_emotion, has_emotion_changes, emotion_change_text):
    prompt = ""
    if has_emotion_changes:
        prompt = f"""
        You are a virtual therapist known for your empathy and understanding. A user has shared a message along with their overall emotional state and a specific portion of the text that reflects a change in emotions. This includes the text, the previous emotion, and the subsequent emotion.

        Your goal is to:
        1. Acknowledge the user's overarching emotion with sensitivity.
        2. Pay special attention to the transition described in the priority segment (`emotion_change_text`), acknowledging both the before and after emotional states and offering insights or support specific to this transition.
        3. Provide a succinct response that validates the user's feelings, offers understanding, and provides comforting or actionable input, focusing on the change in emotions.

        Message: "{text}"
        Overall Emotion: "{overarching_emotion}"
        Priority Segment (Emotion Transition): "{emotion_change_text}"

        Respond thoughtfully and empathetically, focusing on the emotional shift described in the priority segment while maintaining a supportive tone. Limit your response to 100 words.
        """
    else:
        prompt = f"""
        You are a virtual therapist known for your empathy and understanding. A user has shared a message along with their overall emotional state.

        Your goal is to:
        1. Acknowledge the user's overarching emotion with sensitivity.
        2. Respond to the entire message with thoughtful and empathetic input, considering the user's emotional context as a whole.
        3. Provide a succinct response that offers validation, understanding, and actionable or comforting input, tailored to the user's emotional context.

        Message: "{text}"
        Overall Emotion: "{overarching_emotion}"

        Respond thoughtfully and empathetically, addressing the user's message as a whole while maintaining a supportive tone. Limit your response to 100 words.
        """
    data = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "seed": 123}
    }
    response = requests.post('http://localhost:11434/api/generate', json=data)
    return response.json()['response']

@app.route('/listen', methods=['GET'])
def listen_and_respond():
    if not emotion_model:
        return jsonify({"error": "Models not initialized properly"}), 500
        
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise; please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=4)
            overarching_emotion, has_emotion_changes, emotion_change_text = classify_emotion(audio)
            speech_text = recognizer.recognize_google(audio)
            
            response = generate_response(speech_text, overarching_emotion, has_emotion_changes, emotion_change_text)
            
            return jsonify({
                "response": response
            })
            
        except sr.WaitTimeoutError:
            return jsonify({"error": "No speech detected within 4 seconds."}), 408
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand the audio."}), 400
        except sr.RequestError:
            return jsonify({"error": "Request error while recognizing the speech."}), 503
        except Exception as e:
            print(f"Error in listen_and_respond: {str(e)}")
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Initialize models before starting the server
    if initialize_models():
        app.run(debug=True, host='0.0.0.0', port=5001)
    else:
        print("Failed to initialize models. Exiting...")
        exit(1)