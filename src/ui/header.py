# src/ui/header.py
import streamlit as st
from src.language.language_config import get_text

def render_header():
    st.markdown(f'<div class="main-header">📊 {get_text("dashboard_title")}</div>', unsafe_allow_html=True)
    st.markdown(f"**📅 {get_text('period_label')}: {st.session_state.get('periode_data','-')} | 🎯 {get_text('enhanced_dashboard')}**")
