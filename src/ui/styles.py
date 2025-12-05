# src/ui/styles.py
import streamlit as st

def inject_styles():
    st.markdown("""
    <style>
        .main-header { font-size: 2.8rem; color: #1f77b4; text-align: center; margin-bottom: 2rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
        .sub-header { font-size: 1.5rem; color: #2c3e50; margin-bottom: 1rem; font-weight: 600; }
        .metric-card { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 1.5rem; border-radius: 15px; margin: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 4px solid #1f77b4; transition: transform 0.2s ease; }
        .metric-card:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
        .excellent { color: #28a745; font-weight: bold; background-color: rgba(40, 167, 69, 0.1); padding: 2px 8px; border-radius: 12px; }
        .good { color: #17a2b8; font-weight: bold; background-color: rgba(23, 162, 184, 0.1); padding: 2px 8px; border-radius: 12px; }
        .warning { color: #ffc107; font-weight: bold; background-color: rgba(255, 193, 7, 0.1); padding: 2px 8px; border-radius: 12px; }
        .danger { color: #dc3545; font-weight: bold; background-color: rgba(220, 53, 69, 0.1); padding: 2px 8px; border-radius: 12px; }
        .sidebar .sidebar-content { background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%); }
        .dataframe { border-radius: 10px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .footer { text-align: center; color: #6c757d; font-style: italic; margin-top: 2rem; padding: 1rem; border-top: 1px solid #dee2e6; }
    </style>
    """, unsafe_allow_html=True)
