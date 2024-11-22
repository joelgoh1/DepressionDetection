Coding Overview
The project consists of three main components:

01: Praat Script for Prosodic Feature Extraction
This script works in conjunction with a WAV transcript file to extract phrase-level features, referred to as "segment sound." The extracted features include:

Pitch (F0)
Intensity (Energy)
Voice Quality Metrics (Jitter, Shimmer, HNR)
Duration

02: Jupyter Notebook for Emotion Score Extraction
This Python notebook is designed to extract emotion scores [Neutral, Happy, Sad, Angry] from WAV files using a pretrained SpeechBrain model. The extraction process relies on the time boundaries of voice transcriptions for each phrase. Phrases are analyzed at the phrase level, with emotion scores averaged for each chunk. This approach contrasts with the frame-level method, where raw scores are used directly without averaging.

03: Jupyter Notebook for Modeling and Evaluation
This notebook includes two key components:

Feature Engineering
Modeling and Evaluation
