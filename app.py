
import streamlit as st
import numpy as np
import librosa
from sklearn.neighbors import KNeighborsClassifier
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Smart Pet Translator 🐾", page_icon="🐶", layout='centered')

st.markdown("<center><h1 style='color:#ff6b6b'>🐾 Smart Pet Translator</h1></center>", unsafe_allow_html=True)
st.write("Upload a pet sound (WAV or MP3) and discover what your pet might be saying!")

def make_demo_tone(freq, duration=1.0, sr=22050, noise=0.01):
    t = np.linspace(0, duration, int(sr*duration), False)
    tone = 0.12 * np.sin(2*np.pi*freq*t)
    tone += noise * np.random.randn(len(t))
    return tone

sr = 22050
training_sounds = {
    'dog_happy': make_demo_tone(600, sr=sr, noise=0.02),
    'dog_angry': make_demo_tone(900, sr=sr, noise=0.04),
    'cat_neutral': make_demo_tone(350, sr=sr, noise=0.015),
    'cat_content': make_demo_tone(420, sr=sr, noise=0.01)
}

X, y = [], []
for label, data in training_sounds.items():
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13).T, axis=0)
    X.append(mfcc)
    y.append(label)

model = KNeighborsClassifier(n_neighbors=1)
model.fit(X, y)

messages = {
    'dog_happy': 'Your dog sounds happy!',
    'dog_angry': 'Your dog might be angry!',
    'cat_neutral': 'Your cat sounds normal.',
    'cat_content': 'Your cat is feeling relaxed.'
}

st.markdown(
    "<div style='background:#fff7f2;border-radius:12px;padding:18px'>"
    "<h3 style='color:#ff6b6b'>Cute mode: playful colors and pet emojis</h3>"
    "<p>Tip: For a real translator, upload multiple labeled training samples.</p>"
    "</div>", unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload a pet sound (wav/mp3)", type=["wav","mp3"], accept_multiple_files=False)

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1])
    tfile.write(uploaded_file.getbuffer())
    tfile.flush()
    tfile.close()

    try:
        data_test, sr_test = librosa.load(tfile.name, sr=None)
        mfcc_test = np.mean(librosa.feature.mfcc(y=data_test, sr=sr_test, n_mfcc=13).T, axis=0)
        predicted = model.predict([mfcc_test])[0]
        message = messages.get(predicted, f"Detected: {predicted}")
        st.success(f"🔊 Translation: {message}")

        tts = gTTS(message)
        tts_path = os.path.join(tempfile.gettempdir(), 'smart_pet_message.mp3')
        tts.save(tts_path)
        st.audio(tts_path)

        st.audio(tfile.name)
    except Exception as e:
        st.error(f"Failed to process audio: {e}")

st.markdown("<hr><small>Made with ❤️ — replace demo sounds with real labeled pet recordings for best results.</small>", unsafe_allow_html=True)
