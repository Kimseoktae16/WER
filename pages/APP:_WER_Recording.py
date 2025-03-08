import streamlit as st
import sounddevice as sd
import wavio

def record(duration=5, fs=44100, save_path='output.wav'):
    """Record audio for a given duration and sampling rate."""
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    wavio.write(save_path, recording, fs, sampwidth=2)
    return save_path

st.markdown("## Audio Recorder")
record_button = st.button("Record Audio")

if record_button:
    # Assuming 5 seconds of recording
    path = record(duration=5)
    st.audio(path)
