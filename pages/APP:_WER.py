
import streamlit as st
import speech_recognition as sr
from difflib import SequenceMatcher
import re

# Normalize text by converting to lowercase and removing non-alphanumeric characters
def normalize_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

# Function to recognize speech from an audio file
def recognize_audio(audio_file):
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

# Calculate the Word Error Rate (WER)
def calculate_wer(original, recognized):
    original = normalize_text(original)
    recognized = normalize_text(recognized)
    original_words = original.split()
    recognized_words = recognized.split()
    sm = SequenceMatcher(None, original_words, recognized_words)
    deletions, insertions, substitutions = 0, 0, 0
    for opcode, a0, a1, b0, b1 in sm.get_opcodes():
        if opcode == 'replace':
            substitutions += max(a1 - a0, b1 - b0)
        elif opcode == 'insert':
            insertions += (b1 - b0)
        elif opcode == 'delete':
            deletions += (a1 - a0)
    wer = (substitutions + deletions + insertions) / len(original_words) if original_words else 0
    return wer * 100  # percentage

def highlight_differences(original, recognized):
    original = normalize_text(original)
    recognized = normalize_text(recognized)
    original_words = original.split()
    recognized_words = recognized.split()
    sm = SequenceMatcher(None, original_words, recognized_words)
    result = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            result.append(' '.join(original_words[i1:i2]))  # Convert list of words to a single string
        elif tag == 'replace':
            original_segment = ' '.join(original_words[i1:i2])
            recognized_segment = ' '.join(recognized_words[j1:j2])
            result.append(f"<em>{original_segment}</em>")  # Italicize the original segment
            result.append(f"<em>{recognized_segment}</em>")  # Italicize the recognized segment
        elif tag == 'delete':
            result.append(f"<em>{' '.join(original_words[i1:i2])}</em>")  # Italicize the deleted segment
        elif tag == 'insert':
            result.append(f"<em>{' '.join(recognized_words[j1:j2])}</em>")  # Italicize the inserted segment
    return ' '.join(result)  # Ensure all elements are strings


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
        st.write("😊 Recognized Text:", st.session_state['recognized_text'])
        st.markdown(f"📕 Expected Text: {st.session_state['feedback']}", unsafe_allow_html=True)
        st.markdown("---")
        st.write("Word Error Rate (WER):", f"{st.session_state['wer']:.2f}%")

