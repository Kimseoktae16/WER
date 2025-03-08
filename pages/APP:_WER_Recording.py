import streamlit as st
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models.widgets import Button

# Create a simple button
button = Button(label="Click me")

# Event handling using streamlit_bokeh_events
result = streamlit_bokeh_events(
    bokeh_objects=[button],
    events="button_click",
    key="any_key",
    refresh_on_update=True,
    override_height=75,
    debounce_time=500
)

if result:
    st.write("Button clicked")
