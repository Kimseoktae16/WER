import streamlit as st

# URL you want to link to
url = 'https://mk-316-wer-recording.hf.space/'

# Create a button in Streamlit that links to the URL
st.markdown(f"<a href='{url}' target='_blank'><button style='color: black; background-color: #FF4B4B; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px;'>Go to WER Recording Space</button></a>", unsafe_allow_html=True)
