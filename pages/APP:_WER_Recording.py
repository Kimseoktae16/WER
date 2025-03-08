import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

button = Button(label="Click me!", width=300)
button.js_on_event("button_click", CustomJS(code="""
    console.log('button clicked');
    """))

# Ensure the event argument is correct as per the latest library version
result = streamlit_bokeh_events(
    bokeh_model=button,  # This might be 'bokeh_objects' or another parameter based on version
    events="button_click",
    key="click",
    refresh_on_update=True,
    debounce_time=500
)

if result:
    if "button_click" in result:
        st.write("Button was clicked")
