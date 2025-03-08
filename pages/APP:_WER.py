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

# Categorize differences and format output
def categorize_differences(original, recognized):
    original = normalize_text(original)
    recognized = normalize_text(recognized)
    original_words = original.split()
    recognized_words = recognized.split()
    sm = SequenceMatcher(None, original_words, recognized_words)
    insertions, deletions, substitutions = [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'insert':
            insertions.append(' '.join(recognized_words[j1:j2]))
        elif tag == 'delete':
            deletions.append(' '.join(original_words[i1:i2]))
        elif tag == 'replace':
            # Adjusted format for substitutions
            original_segment = ' '.join(original_words[i1:i2])
            recognized_segment = ' '.join(recognized_words[j1:j2])
            substitutions.append(f"'{original_segment}' ---> '{recognized_segment}'")
    return insertions, deletions, substitutions

st.title('Speech Recognition Feedback Tool')

with st.form("record_audio"):
    audio_file = st.file_uploader("Upload your audio file here:", type=['wav', 'mp3'])
    expected_text = st.text_area("Paste the expected text here:")
    submit_button = st.form_submit_button("Step 1. Analyze Recording")

if submit_button and audio_file and expected_text:
    recognized_text = recognize_audio(audio_file)
    wer = calculate_wer(expected_text, recognized_text)
    insertions, deletions, substitutions = categorize_differences(expected_text, recognized_text)
    st.session_state['recognized_text'] = recognized_text
    st.session_state['wer'] = wer
    st.session_state['insertions'] = insertions
    st.session_state['deletions'] = deletions
    st.session_state['substitutions'] = substitutions

if st.button("Step 2. Display Feedback"):
    st.write("⭕ Your speech recognized as:", st.session_state['recognized_text'])
    st.markdown("---")
    if st.session_state['insertions']:
        st.write("⚪ Insertion Errors:", ', '.join(st.session_state['insertions']))
    else:
        st.write("⚪ Insertion Errors: (None)")

    if st.session_state['deletions']:
        st.write("⚪ Deletion Errors:", ', '.join(st.session_state['deletions']))
    else:
        st.write("⚪ Deletion Errors: (None)")

    if st.session_state['substitutions']:
        st.write("⚪ Substitution Errors:", ', '.join(st.session_state['substitutions']))
    else:
        st.write("⚪ Substitution Errors: (None)")
    st.markdown("---")
    st.write("⭕ Word Error Rate (WER):", f"{st.session_state['wer']:.1f}%")
    st.markdown("---")


        
    interpretation_text = """
    #### 🔑 Interpreting WER Results
    
    - **0% WER**: Indicates perfect accuracy, with the recognized text exactly matching the reference.
    - **Low WER (5% to 20%)**: High accuracy, with few errors relative to the number of words. The transcription is generally reliable.
    - **Moderate WER (20% to 50%)**: Moderate accuracy, noticeable errors that may affect understanding of certain parts of the text.
    - **High WER (over 50%)**: Poor accuracy, significant errors likely make the transcription unreliable without extensive corrections.
    
    ❗_Note:_The lower the WER, the better the performance of the speech recognition system. A high WER may suggest issues with audio quality, speaker's pronunciation, or the complexity of the language used.
    """
    
    st.info(interpretation_text)

