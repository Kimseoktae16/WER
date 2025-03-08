import streamlit as st
import speech_recognition as sr
from difflib import SequenceMatcher
import re
from pydub import AudioSegment  # Importing the library for audio conversion
import io

def normalize_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def convert_audio_to_wav(audio_file):
    # Convert the Streamlit UploadedFile to a byte stream
    file_format = audio_file.name.split('.')[-1]
    audio = AudioSegment.from_file_using_temporary_files(audio_file, format=file_format)
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    return buffer

def recognize_audio(audio_file):
    # Convert audio to WAV format if it's not a WAV file
    if audio_file.type != "audio/wav":
        audio_file = convert_audio_to_wav(audio_file)

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

# Streamlit interface and rest of the code
st.title('Speech Recognition Feedback Tool')
with st.form("record_audio"):
    audio_file = st.file_uploader("Upload your audio file here:", type=['wav', 'mp3'])
    expected_text = st.text_area("Paste the expected text here:")
    submit_button = st.form_submit_button("Analyze Recording")

if submit_button and audio_file and expected_text:
    recognized_text = recognize_audio(audio_file)
    wer = calculate_wer(expected_text, recognized_text)
    feedback = highlight_differences(expected_text, recognized_text)
    st.session_state['feedback'] = feedback
    st.session_state['recognized_text'] = recognized_text
    st.session_state['wer'] = wer

if st.button("Display Feedback"):
    if 'feedback' in st.session_state and 'recognized_text' in st.session_state and 'wer' in st.session_state:
        st.write("Recognized Text:", st.session_state['recognized_text'])
        st.write("Word Error Rate (WER):", f"{st.session_state['wer']:.2f}%")
        st.markdown(f"Comparison: {st.session_state['feedback']}", unsafe_allow_html=True)
