import streamlit as st
from modules.caption_scraper import run_caption_scraper
from modules.image_spoofer import run_image_spoofer

st.set_page_config(page_title="BlessingTools", layout="wide")

st.markdown("""
<h1 style='text-align:center; color:#D4AF37;'>BlessingTools</h1>
<p style='text-align:center; color:white;'>Elegant Dark Suite</p>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 Caption Scraper", "🖼️ Image Spoofer"])

with tab1:
    run_caption_scraper()

with tab2:
    run_image_spoofer()
