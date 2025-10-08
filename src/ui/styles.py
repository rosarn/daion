"""
============================================================================
UI STYLES MODULE
============================================================================

Author: Data Analyst Team
Version: 2.0 (Restructured)
Purpose: Handle all UI styling, CSS, and visual components

This module contains:
- Custom CSS styling
- UI component configurations
- Theme management
- Responsive design elements
"""

import streamlit as st
from typing import Dict, Any


def apply_custom_css() -> None:
    """
    Apply custom CSS styling to the Streamlit application
    
    Features:
        - Professional business dashboard styling
        - Responsive design for mobile and desktop
        - Enhanced metric cards with hover effects
        - Performance status color coding
        - Modern gradient backgrounds
        - Improved readability and accessibility
    """
    
    st.markdown("""
    <style>
        /* Main Dashboard Styling */
        .main-header {
            font-size: 2.8rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .sub-header {
            font-size: 1.5rem;
            color: #2c3e50;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        /* Enhanced Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #1f77b4;
            transition: transform 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Performance Status Colors */
        .excellent { 
            color: #28a745; 
            font-weight: bold;
            background-color: rgba(40, 167, 69, 0.1);
            padding: 2px 8px;
            border-radius: 12px;
        }
        .good { 
            color: #17a2b8; 
            font-weight: bold;
            background-color: rgba(23, 162, 184, 0.1);
            padding: 2px 8px;
            border-radius: 12px;
        }
        .warning { 
            color: #ffc107; 
            font-weight: bold;
            background-color: rgba(255, 193, 7, 0.1);
            padding: 2px 8px;
            border-radius: 12px;
        }
        .danger { 
            color: #dc3545; 
            font-weight: bold;
            background-color: rgba(220, 53, 69, 0.1);
            padding: 2px 8px;
            border-radius: 12px;
        }
        
        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* Data Table Styling */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Alert Boxes */
        .alert-success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 12px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .alert-warning {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 12px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .alert-danger {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 12px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        /* Footer Styling */
        .footer {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            margin-top: 2rem;
            padding: 1rem;
            border-top: 1px solid #dee2e6;
        }
        
        /* Loading Animation */
        .loading {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
            }
            .metric-card {
                margin: 0.25rem;
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)


def configure_page() -> None:
    """
    Configure Streamlit page settings for the dashboard
    
    Features:
        - Professional page configuration
        - Wide layout for better data visualization
        - Custom page icon and title
        - Enhanced menu options
    """
    
    st.set_page_config(
        page_title="Sales Performance Analytics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://docs.streamlit.io/',
            'Report a bug': None,
            'About': "Sales Performance Analytics Dashboard v2.0 - Enhanced with Data Analyst Best Practices"
        }
    )


def display_header() -> None:
    """
    Display the main dashboard header with professional styling
    """
    
    st.markdown("""
    <div class="main-header">
        📊 SALES PERFORMANCE ANALYTICS DASHBOARD
    </div>
    """, unsafe_allow_html=True)


def display_subheader(text: str) -> None:
    """
    Display a styled subheader
    
    Args:
        text (str): The subheader text to display
    """
    
    st.markdown(f"""
    <div class="sub-header">
        {text}
    </div>
    """, unsafe_allow_html=True)


def format_performance_status(percentage: float) -> str:
    """
    Format performance status with appropriate CSS class
    
    Args:
        percentage (float): Performance percentage
        
    Returns:
        str: HTML formatted performance status
    """
    
    if percentage >= 100:
        css_class = "excellent"
        status = "Excellent"
    elif percentage >= 80:
        css_class = "good"
        status = "Good"
    elif percentage >= 60:
        css_class = "warning"
        status = "Average"
    else:
        css_class = "danger"
        status = "Below Average" if percentage >= 40 else "Poor"
    
    return f'<span class="{css_class}">{status} ({percentage:.1f}%)</span>'


def create_metric_card(title: str, value: str, delta: str = None) -> str:
    """
    Create a styled metric card HTML
    
    Args:
        title (str): Card title
        value (str): Main value to display
        delta (str, optional): Delta value for comparison
        
    Returns:
        str: HTML formatted metric card
    """
    
    delta_html = f"<div style='color: #6c757d; font-size: 0.9rem;'>{delta}</div>" if delta else ""
    
    return f"""
    <div class="metric-card">
        <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.5rem;">{title}</div>
        <div style="font-size: 2rem; font-weight: bold; color: #2c3e50;">{value}</div>
        {delta_html}
    </div>
    """


def display_alert(message: str, alert_type: str = "info") -> None:
    """
    Display a styled alert message
    
    Args:
        message (str): Alert message
        alert_type (str): Type of alert (success, warning, danger, info)
    """
    
    css_class = f"alert-{alert_type}" if alert_type in ["success", "warning", "danger"] else "alert-info"
    
    st.markdown(f"""
    <div class="{css_class}">
        {message}
    </div>
    """, unsafe_allow_html=True)


def display_footer() -> None:
    """
    Display the dashboard footer with timestamp
    """
    
    from datetime import datetime
    
    st.markdown(f"""
    <div class="footer">
        <div style='text-align: center; color: gray;'>
            <i>Dashboard updated automatically • Data period: 21 Juli - 20 Agustus 2024 • Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
        </div>
    </div>
    """, unsafe_allow_html=True)


def get_color_palette() -> Dict[str, str]:
    """
    Get the standard color palette for charts and visualizations
    
    Returns:
        Dict[str, str]: Color palette mapping
    """
    
    return {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40',
        'excellent': '#28a745',
        'good': '#17a2b8',
        'average': '#ffc107',
        'poor': '#dc3545'
    }


def get_chart_theme() -> Dict[str, Any]:
    """
    Get the standard theme configuration for Plotly charts
    
    Returns:
        Dict[str, Any]: Chart theme configuration
    """
    
    return {
        'layout': {
            'font': {'family': 'Arial, sans-serif', 'size': 12},
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'colorway': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        }
    }