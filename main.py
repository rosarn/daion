# main.py
import streamlit as st

# init language/session if needed
from src.language.language_config import init_language, get_text
from src.ui.styles import inject_styles
from src.ui.header import render_header
from src.ui.sidebar import render_sidebar
from src.analytics.metrics import calculate_team_metrics
from src.ui.tabs import render_tabs

def main():
    st.set_page_config(
        page_title="Sales Performance Analytics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_language()
    inject_styles()
    render_header()

    # Sidebar returns (data, filtered_data)
    data, filtered_data = render_sidebar()

    # KPIs
    team_metrics = calculate_team_metrics(filtered_data)

    # Tabs (maps, overview, performers, detailed, recommendations)
    render_tabs(filtered_data, team_metrics)

if __name__ == "__main__":
    main()
