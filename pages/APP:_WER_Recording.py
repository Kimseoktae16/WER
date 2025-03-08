import streamlit as st

st.markdown("### 🍃 WER Speech Feedback: Direct Microphone Recording")

# URL you want to link to
url = 'https://mk-316-wer-recording.hf.space/'

# App Description
description = """
🔮 This application allows you to record your speaking directly through the web interface 
and immediately receive feedback on your pronunciation and speech clarity. 

Click the button below 
to access the app and start recording your speech to analyze the Word Error Rate (WER) and get detailed feedback.
"""

# Display the description
st.markdown(description, unsafe_allow_html=True)

# Create a button in Streamlit that links to the URL
st.markdown(f"<a href='{url}' target='_blank'><button style='color: black; background-color: #99CCFF; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px;'>Go to WER Recording Space</button></a>", unsafe_allow_html=True)
