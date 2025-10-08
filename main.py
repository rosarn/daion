"""
============================================================================
SALES PERFORMANCE ANALYTICS DASHBOARD - MAIN APPLICATION
============================================================================

Author: Data Analyst Team
Version: 2.0 (Restructured Monorepo)
Purpose: Main orchestration file for the Sales Performance Analytics Dashboard

This is the main entry point that coordinates all modules:
- Data loading and processing
- UI components and styling
- Analytics and metrics calculation
- Visualization and charts
- Business intelligence insights

Architecture:
- Modular design with clear separation of concerns
- Robust dependency management
- Comprehensive error handling
- Scalable and maintainable codebase
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from src.data.loader import load_sales_data
from src.data.models import validate_sales_data
from src.ui.styles import configure_page, apply_custom_css, display_header
from src.ui.components import (
    create_sidebar_filters, apply_filters, display_filter_summary,
    create_kpi_cards, display_performance_table, create_export_options
)
from src.analytics.metrics import (
    calculate_team_metrics, get_area_performance, get_grade_analysis,
    analyze_performance_segments, calculate_improvement_potential,
    generate_executive_insights, calculate_critical_areas, calculate_best_areas,
    calculate_roi_projections, generate_action_timeline
)
from src.visualizations.charts import (
    create_area_achievement_chart, create_performance_distribution_pie,
    create_sales_vs_target_chart, create_grade_achievement_chart,
    create_grade_scatter_chart, create_performance_scatter_plot,
    create_stacked_performance_chart, create_improvement_priority_chart,
    create_revenue_potential_scatter, display_chart
)


def initialize_app():
    """Initialize the Streamlit application with configuration and styling"""
    configure_page()
    apply_custom_css()


def load_and_validate_data():
    """Load and validate the sales data"""
    try:
        data = load_sales_data()
        if validate_sales_data(data):
            return data
        else:
            st.error("❌ Data validation failed. Please check your data source.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame()


def render_sidebar(data: pd.DataFrame):
    """Render the sidebar with filters and return filtered data"""
    if data.empty:
        st.sidebar.error("No data available for filtering")
        return data, {}
    
    # Create sidebar filters
    filter_values = create_sidebar_filters(data)
    
    # Apply filters to data
    filtered_data = apply_filters(data, filter_values)
    
    # Display filter summary
    display_filter_summary(filtered_data, filter_values)
    
    return filtered_data, filter_values


def render_kpi_section(filtered_data: pd.DataFrame):
    """Render the Key Performance Indicators section"""
    st.subheader("🎯 Key Performance Indicators")
    
    if filtered_data.empty:
        st.warning("No data available for KPI calculation")
        return
    
    # Calculate comprehensive metrics
    team_metrics = calculate_team_metrics(filtered_data)
    
    # Create and display KPI cards using the original data instead of team_metrics
    create_kpi_cards(filtered_data)


def render_overview_tab(filtered_data: pd.DataFrame):
    """Render the Overview tab with performance analytics"""
    st.subheader("📊 Performance Overview & Analytics")
    
    if filtered_data.empty:
        st.warning("No data available for overview")
        return
    
    # Enhanced area performance comparison
    col1, col2 = st.columns([2, 1])
    
    with col1:
        area_stats = get_area_performance(filtered_data)
        if not area_stats.empty:
            fig_area = create_area_achievement_chart(area_stats)
            display_chart(fig_area)
        else:
            st.info("No area performance data available")
    
    with col2:
        # Performance distribution pie chart
        performance_dist = filtered_data['Performance_Category'].value_counts()
        if not performance_dist.empty:
            fig_pie = create_performance_distribution_pie(performance_dist)
            display_chart(fig_pie)
        else:
            st.info("No performance distribution data available")
    
    # Sales vs Target analysis
    st.subheader("📊 Sales vs Target Analysis by Sub-Area")
    subarea_stats = filtered_data.groupby('SubArea').agg({
        'Sales': 'sum', 
        'Target': 'sum',
        'Nama': 'count'
    }).reset_index()
    
    if not subarea_stats.empty:
        subarea_stats['Achievement'] = (subarea_stats['Sales'] / subarea_stats['Target'] * 100).round(1)
        subarea_stats = subarea_stats.sort_values('Achievement', ascending=True)
        
        fig_bar = create_sales_vs_target_chart(subarea_stats)
        display_chart(fig_bar)
    else:
        st.info("No sub-area data available")
    
    # Grade performance analysis
    st.subheader("👥 Performance Analysis by Grade")
    grade_stats = get_grade_analysis(filtered_data)
    
    if not grade_stats.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_grade = create_grade_achievement_chart(grade_stats)
            display_chart(fig_grade)
        
        with col2:
            fig_scatter_grade = create_grade_scatter_chart(grade_stats)
            display_chart(fig_scatter_grade)
    else:
        st.info("No grade analysis data available")


def render_performers_tab(filtered_data: pd.DataFrame):
    """Render the Top Performers Analysis tab"""
    st.subheader("🏆 Top Performers Analysis & Insights")
    
    if filtered_data.empty:
        st.warning("No data available for performer analysis")
        return
    
    # Performance summary cards
    segments = analyze_performance_segments(filtered_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        excellent_count = len(segments['excellent_performers'])
        excellent_pct = excellent_count / len(filtered_data) * 100 if len(filtered_data) > 0 else 0
        st.metric("Excellent Performers", excellent_count, f"{excellent_pct:.1f}%")
    
    with col2:
        good_count = len(segments['good_performers'])
        good_pct = good_count / len(filtered_data) * 100 if len(filtered_data) > 0 else 0
        st.metric("Good Performers", good_count, f"{good_pct:.1f}%")
    
    with col3:
        avg_count = len(segments['average_performers'])
        avg_pct = avg_count / len(filtered_data) * 100 if len(filtered_data) > 0 else 0
        st.metric("Average Performers", avg_count, f"{avg_pct:.1f}%")
    
    with col4:
        poor_count = len(segments['below_average_performers']) + len(segments['poor_performers'])
        poor_pct = poor_count / len(filtered_data) * 100 if len(filtered_data) > 0 else 0
        st.metric("Needs Improvement", poor_count, f"{poor_pct:.1f}%")
    
    # Top and bottom performers tables
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌟 Top 10 Performers")
        top_10 = filtered_data.nlargest(10, 'Percentage')[['Nama', 'Area', 'SubArea', 'Grade', 'Sales', 'Target', 'Percentage']]
        if not top_10.empty:
            display_performance_table(top_10)
        else:
            st.info("No top performers data available")
    
    with col2:
        st.subheader("⚠️ Bottom 10 Performers")
        bottom_10 = filtered_data.nsmallest(10, 'Percentage')[['Nama', 'Area', 'SubArea', 'Grade', 'Sales', 'Target', 'Percentage']]
        if not bottom_10.empty:
            display_performance_table(bottom_10)
        else:
            st.info("No bottom performers data available")
    
    # Performance scatter plot
    st.subheader("📊 Performance Scatter Analysis")
    fig_scatter = create_performance_scatter_plot(filtered_data)
    display_chart(fig_scatter)
    
    # Performance distribution by area
    st.subheader("🌍 Performance Distribution by Area")
    fig_stacked = create_stacked_performance_chart(filtered_data)
    display_chart(fig_stacked)


def render_detailed_data_tab(filtered_data: pd.DataFrame):
    """Render the Detailed Data View tab"""
    st.subheader("📋 Detailed Data View & Analysis")
    
    if filtered_data.empty:
        st.warning("No data available for detailed view")
        return
    
    # Enhanced search and filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_name = st.text_input("🔍 Search by Name:")
    
    with col2:
        sort_options = [
            'Percentage DESC', 'Percentage ASC', 
            'Sales DESC', 'Sales ASC',
            'Target DESC', 'Target ASC',
            'Name A-Z', 'Name Z-A',
            'Area A-Z'
        ]
        sort_by = st.selectbox("📊 Sort by:", sort_options)
    
    with col3:
        export_format = st.selectbox("📤 Export Format:", ['View Only', 'CSV Download', 'Excel Download'])
    
    # Apply search filter
    display_df = filtered_data.copy()
    if search_name:
        display_df = display_df[display_df['Nama'].str.contains(search_name, case=False, na=False)]
    
    # Apply sorting
    sort_mapping = {
        'Percentage DESC': ('Percentage', False),
        'Percentage ASC': ('Percentage', True),
        'Sales DESC': ('Sales', False),
        'Sales ASC': ('Sales', True),
        'Target DESC': ('Target', False),
        'Target ASC': ('Target', True),
        'Name A-Z': ('Nama', True),
        'Name Z-A': ('Nama', False),
        'Area A-Z': ('Area', True)
    }
    
    if sort_by in sort_mapping:
        column, ascending = sort_mapping[sort_by]
        display_df = display_df.sort_values(column, ascending=ascending)
    
    # Display the data table
    st.subheader(f"📊 Data Table ({len(display_df)} records)")
    display_performance_table(display_df)
    
    # Export options
    if export_format != 'View Only':
        create_export_options(display_df, export_format)


def render_recommendations_tab(filtered_data: pd.DataFrame):
    """Render the Recommendations & Action Plan tab"""
    st.subheader("🎯 Performance Improvement Recommendations")
    
    if filtered_data.empty:
        st.warning("No data available for recommendations")
        return
    
    # Executive insights
    insights = generate_executive_insights(filtered_data)
    segments = analyze_performance_segments(filtered_data)
    
    # Executive summary
    st.subheader("📋 Executive Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        **Overall Status:** {insights['overall_status']}
        
        **Achievement Rate:** {insights['overall_achievement']:.1f}%
        """)
    
    with col2:
        st.markdown(f"""
        **Risk Level:** {insights['risk_status']}
        
        **Risk Percentage:** {insights['risk_level']:.1f}%
        """)
    
    with col3:
        st.markdown(f"""
        **Quick Wins:** {insights['quick_wins']} people
        
        **Benchmarks:** {insights['benchmarks']} people
        """)
    
    # Critical areas and recommendations
    st.subheader("🚨 Immediate Priority Actions")
    
    critical_areas = calculate_critical_areas(filtered_data)
    best_areas = calculate_best_areas(filtered_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚠️ Critical Areas")
        if not critical_areas.empty:
            for area, achievement in critical_areas.items():
                st.markdown(f"- **{area}**: {achievement:.1f}% achievement")
        else:
            st.info("No critical areas identified")
    
    with col2:
        st.markdown("### 🏆 Best Performing Areas")
        if not best_areas.empty:
            for area, achievement in best_areas.items():
                st.markdown(f"- **{area}**: {achievement:.1f}% achievement")
        else:
            st.info("No benchmark areas available")
    
    # Improvement potential analysis
    st.subheader("📈 Performance Improvement Potential")
    
    improvement_df = calculate_improvement_potential(filtered_data)
    
    if not improvement_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_improve = create_improvement_priority_chart(improvement_df)
            display_chart(fig_improve)
        
        with col2:
            fig_revenue = create_revenue_potential_scatter(improvement_df)
            display_chart(fig_revenue)
    else:
        st.info("No improvement potential data available")
    
    # Action plan timeline
    st.subheader("📅 Recommended Action Timeline")
    timeline_df = generate_action_timeline()
    st.dataframe(timeline_df, use_container_width=True)
    
    # ROI Projection
    st.subheader("💹 Projected ROI from Recommendations")
    roi_metrics = calculate_roi_projections(filtered_data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Potential Revenue Recovery", f"{roi_metrics['potential_recovery']:,.0f}", "From gap closure")
    
    with col2:
        st.metric("Quick Win Potential", f"{roi_metrics['quick_win_potential']:,.0f}", "From medium performers")
    
    with col3:
        st.metric("Total Improvement Potential", f"{roi_metrics['roi_percentage']:.1f}%", "Of current target")


def render_footer():
    """Render the application footer"""
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: gray;'>
        <i>Dashboard updated automatically • Data period: 21 Juli - 20 Agustus 2024 • Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application function"""
    # Initialize the application
    initialize_app()
    
    # Display header
    display_header()
    
    # Load and validate data
    data = load_and_validate_data()
    
    if data.empty:
        st.error("❌ Unable to load data. Please check your data source and try again.")
        return
    
    # Render sidebar and get filtered data
    filtered_data, filter_values = render_sidebar(data)
    
    # Render KPI section
    render_kpi_section(filtered_data)
    
    st.markdown("---")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🏆 Performers", "📋 Detailed Data", "🎯 Recommendations"])
    
    with tab1:
        render_overview_tab(filtered_data)
    
    with tab2:
        render_performers_tab(filtered_data)
    
    with tab3:
        render_detailed_data_tab(filtered_data)
    
    with tab4:
        render_recommendations_tab(filtered_data)
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
