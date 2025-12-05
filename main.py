# main.py
import streamlit as st

# Language system
from src.language.language_config import init_language, get_text

# UI & styles
from src.ui.styles import inject_styles
from src.ui.header import render_header
from src.ui.sidebar import render_sidebar

# Analytics
from src.analytics.metrics import calculate_team_metrics

# Tabs (UI screens)
from src.ui.tabs import render_tabs

# NEW (for choropleth integration)
# If you already created these files, good — this import will work
# If not, I will generate the file maps/choro.py for you later
try:
    from src.maps.choropleth import create_province_choropleth
except Exception:
    create_province_choropleth = None


def main():
    # -------------------------
    # 🌐 Global page settings
    # -------------------------
    st.set_page_config(
        page_title="Sales Performance Analytics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # -------------------------
    # 🌐 Initialize language
    # -------------------------
    init_language()  # <--- IMPORTANT (keeps selected language across pages)

    # -------------------------
    # 🎨 Inject global CSS
    # -------------------------
    inject_styles()

    # -------------------------
    # 🏷️ Render Header
    # -------------------------
    render_header()

    # -------------------------
    # 🧭 Sidebar: file upload, filters, language switcher
    # returns: (data, filtered_data)
    # -------------------------
    data, filtered_data = render_sidebar()

    # -------------------------
    # 📊 Calculate KPIs
    # -------------------------
    team_metrics = calculate_team_metrics(filtered_data)

    # -------------------------
    # 🗂️ Render TABS (Maps, Overview, Performers, Detailed, Recommendations)
    # -------------------------
    render_tabs(filtered_data, team_metrics)

    # -------------------------
    # 📌 OPTIONAL: Show footer text (multilanguage)
    # -------------------------
    st.markdown(
        f"""
        <div style='text-align:center; margin-top: 30px; color: gray; font-size: 13px;'>
            <i>{get_text('footer_text')}</i>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
