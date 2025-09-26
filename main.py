"""
SALES PERFORMANCE ANALYTICS DASHBOARD
=====================================
Author: Data Analyst Team
Purpose: Comprehensive sales performance monitoring and analysis system
Data Period: Juli - Agustus 2024

BUSINESS CONTEXT:
- Multi-area sales team performance tracking
- Individual and team-level KPI monitoring  
- Real-time dashboard for management decision making
- Performance categorization and improvement recommendations

TECHNICAL STACK:
- Streamlit: Interactive web dashboard framework
- Pandas: Data manipulation and analysis
- Plotly: Interactive visualizations
- Seaborn/Matplotlib: Statistical plotting
"""

import streamlit as st
import sys
import os

# Add project modules to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """
    Main application entry point
    
    DATA ANALYST NOTES:
    - This is a basic entry point that should redirect to the main dashboard
    - Consider implementing proper routing for multiple dashboard views
    - Add authentication layer for production deployment
    """
    
    st.set_page_config(
        page_title="Sales Analytics Hub",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🏢 Sales Performance Analytics Hub")
    st.markdown("---")
    
    # Navigation options
    st.markdown("""
    ### Available Dashboards:
    
    1. **📈 Comprehensive Sales Dashboard** - Main performance analytics
    2. **🔍 Individual Area Analysis** - Detailed area-specific insights
    3. **📊 Historical Trends** - Time-series performance analysis
    
    **Recommendation:** Use `satu.py` for the main comprehensive dashboard.
    """)
    
    # Quick stats preview
    st.info("💡 **Data Analyst Insight**: This hub serves as the central entry point for all sales analytics. For detailed analysis, navigate to the comprehensive dashboard.")

if __name__ == "__main__":
    main()
