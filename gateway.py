import streamlit as st
from main import app

streamlit_app = st.App("frontend.py")

# Initialize Streamlit's lifecycle with FastAPI
app.router.lifespan_context = streamlit_app.lifespan()

# Mount the frontend
app.mount("/", streamlit_app)