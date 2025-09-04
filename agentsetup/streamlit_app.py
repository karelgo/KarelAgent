import streamlit as st
import requests

st.set_page_config(page_title="KarelAgent Data & Analytics Platform", page_icon="🤖", layout="centered")

st.title("KarelAgent Data & Analytics Platform")

endpoints = [
    {"name": "Ingest", "path": "/ingest"},
    {"name": "Clean", "path": "/clean"},
    {"name": "Analyze", "path": "/analyze"},
    {"name": "Visualize", "path": "/visualize"},
    {"name": "Report", "path": "/report"},
]

selected = st.selectbox("Select Agent", endpoints, format_func=lambda x: x["name"])
data_input = st.text_input("Input Data", "")

if st.button("Send"):
    if not data_input:
        st.warning("Please enter some data.")
    else:
        with st.spinner("Processing..."):
            try:
                url = f"http://localhost:8000{selected['path']}"
                response = requests.post(url, json={"data": data_input})
                response.raise_for_status()
                result = response.json().get("result", "No result returned.")
                st.success(result)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("<hr />", unsafe_allow_html=True)
st.caption("© 2025 KarelAgent Platform")
