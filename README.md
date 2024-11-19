# CS5647 Term Project Final Report: Depression Detection in Voice Clips based on Prosodic and Emotion Features

## Abstract
This study aims to enhance depression detection by integrating prosody-aware features with zero-shot emotion detection from pretrained transformer models. The proposed framework leverages SpeechBrain for automatic speech recognition (ASR) and emotion detection, utilizing a model trained on diverse, emotion-rich datasets to ensure robust performance. Key prosodic features are extracted using Praat software and fused with emotion scores from SpeechBrain to create a multimodal input for depression classification.

Two approaches were explored for the classification task: a tree-based model and an LSTM with attention mechanism. The tree-based model achieved Regression of PHQ scores in terms of RMSE at 0.0197, while the LSTM+Attention model achieved an RMSE of 0.XXX, indicating improved prediction accuracy with the latter. 

A mock-up depression detection demo is also presented to highlight the potential of combining linguistic, emotional, and prosodic cues in developing emotion-aware mental health tools, which is the core interest of our project team.

## Instructions to run

### Model visualisation


### App demonstration
Note: Testing for this project was only conducted on macOS. Compatibility with other operating systems has not been verified. App currently only supports ios.
#### Frontend
**Pre-run requirements:**
1. Ensure npm is installed on your system. You can verify this by running `npm -v` in your terminal.
2. Install Expo CLI globally if you haven't already by running:
  ```
  npm install -g expo-cli
  ```
3. If running on macOS, ensure Xcode is set up for ios development by doing the following:
    1. Download Xcode from the Mac App Store
    2. Open a terminal and run the following command
       ```
       xcode-select --install
       ```
    3. Accept the license agreement by running:
       ```
       sudo xcodebuild -license
       ```
**Running Steps:**
1. Navigate to the frontend directory by running: `cd aitherapist`
2. Start the expo server by running: `npx expo start`
3. To boot up the IOS server, press i
4. The home screen should appear

#### Backend
Open a separate terminal
**Pre-run requirements:**
1. Ensure you have Python installed (specifically we used Python 3.9 for this project, other variants of Python were not tested)
2. Navigate to the backend directory by running: `cd backend` 
3. Create and activate a virtual environment by running the following command in your terminal:
   ```
   python3 -m venv myenv
   source myenv/bin/activate
   ```
4. Install all required libraries by running
   ```
   pip install -r 'requirements.txt'
   ```
**Running steps:**
1. Start the server by running `gunicorn -w 1 -b 0.0.0.0:5001 app:app`
2. Wait for at least 2 minutes for the model to load

After activating both backend and frontend servers, you can click on the `Call now` button to initiate a virtual call.


