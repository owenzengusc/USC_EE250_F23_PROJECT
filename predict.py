import tensorflow as tf
import librosa
import numpy as np

def load_and_prepare_audio(file_path, maxlen=200):
    wf, sr = librosa.load(file_path)
    mfcc_wf = librosa.feature.mfcc(y=wf, sr=sr)
    padded_mfcc = tf.keras.utils.pad_sequences(mfcc_wf, padding='post', maxlen=maxlen)
    return np.array([padded_mfcc])

def predict_gender(model, file_path):
    data = load_and_prepare_audio(file_path)
    prediction = model.predict(data)
    return 'male' if prediction[0][0] > 0.5 else 'female'

# Load the model
model = tf.keras.models.load_model("voice_gender_classifier_model")

# File paths
files_to_predict = ['recording.mp3', 'female.mp3']

# Predict and print results
for file in files_to_predict:
    gender = predict_gender(model, file)
    print(f"The voice in '{file}' is predicted to be: {gender}")
