import streamlit as st
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models.widgets import Button
from bokeh.models import CustomJS

# Create the record button
record_button = Button(label="Record", button_type="success")

# JavaScript to handle the recording
record_button.js_on_event("button_click", CustomJS(code="""
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        
        const audioChunks = [];
        mediaRecorder.addEventListener("dataavailable", event => {
          audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
          const audioBlob = new Blob(audioChunks);
          const audioUrl = URL.createObjectURL(audioBlob);
          const audio = new Audio(audioUrl);
          const downloadLink = document.createElement('a');
          downloadLink.href = audioUrl;
          downloadLink.download = 'recording.wav';
          downloadLink.click();
        });

        setTimeout(() => {
          mediaRecorder.stop();
        }, 5000);  // Stop recording after 5 seconds
    });
"""))

# Streamlit interface
st.markdown('### 🍃 WER Speech Feedback (Direct Recording)')
st.caption("[25.03.08] Word Error Rate calculation: The lower the WER, the better your performance. 0% means no error :-)")

# Deploy the record button and handle the event
result = streamlit_bokeh_events(
    bokeh_objects=[record_button],
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

# Assuming the recorded audio is handled
# You would need additional backend logic to save and process the audio data from the recording

if "GET_TEXT" in result:
    audio_data = result.get("GET_TEXT")
    # Process the audio data here

# Additional Streamlit components can be added below
