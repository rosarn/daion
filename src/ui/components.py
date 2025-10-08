"""
============================================================================
UI COMPONENTS MODULE
============================================================================

Author: Data Analyst Team
Version: 2.0 (Restructured)
Purpose: Handle UI components, filters, and interactive elements

This module contains:
- Sidebar filter components
- Interactive widgets
- Data display components
- User interface elements
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple, Any
from ..data.models import PerformanceCategory, Grade


def create_sidebar_filters(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create sidebar filters for data filtering
    
    Args:
        df (pd.DataFrame): The sales data DataFrame
        
    Returns:
        Dict[str, Any]: Dictionary containing all filter values
    """
    
    st.sidebar.markdown("## 🎛️ DATA FILTERS")
    st.sidebar.markdown("---")
    
    # Area Filter
    st.sidebar.markdown("### 📍 Geographic Filter")
    areas = ['All Areas'] + sorted(df['Area'].unique().tolist())
    selected_area = st.sidebar.selectbox(
        "Select Area:",
        areas,
        help="Filter data by geographic area"
    )
    
    # Grade Filter
    st.sidebar.markdown("### 👥 Role Filter")
    grades = ['All Grades'] + sorted(df['Grade'].unique().tolist())
    selected_grade = st.sidebar.selectbox(
        "Select Grade/Role:",
        grades,
        help="Filter by employee grade/role (SPV=Supervisor, S2=Senior Sales, DS=Direct Sales)"
    )
    
    # Performance Range Filter
    st.sidebar.markdown("### 📊 Performance Range")
    min_perf, max_perf = st.sidebar.slider(
        "Achievement Percentage Range:",
        min_value=0,
        max_value=int(df['Percentage'].max()) + 10,
        value=(0, int(df['Percentage'].max()) + 10),
        step=5,
        help="Filter by performance achievement percentage"
    )
    
    # Performance Category Filter
    st.sidebar.markdown("### 🎯 Performance Category")
    categories = ['All Categories'] + [cat.value for cat in PerformanceCategory]
    selected_category = st.sidebar.selectbox(
        "Select Performance Category:",
        categories,
        help="Filter by performance classification"
    )
    
    # Additional Filters
    st.sidebar.markdown("### 🔍 Advanced Filters")
    
    # Zero Sales Filter
    show_zero_sales = st.sidebar.checkbox(
        "Include Zero Sales",
        value=True,
        help="Include/exclude team members with zero sales"
    )
    
    # Target Achievement Filter
    target_achieved_only = st.sidebar.checkbox(
        "Target Achieved Only",
        value=False,
        help="Show only team members who achieved their targets"
    )
    
    return {
        'area': selected_area,
        'grade': selected_grade,
        'min_achievement': min_perf,
        'max_achievement': max_perf,
        'category': selected_category,
        'show_zero_sales': show_zero_sales,
        'target_achieved_only': target_achieved_only
    }


def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply selected filters to the DataFrame
    
    Args:
        df (pd.DataFrame): Original DataFrame
        filters (Dict[str, Any]): Filter values from sidebar
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    
    filtered_df = df.copy()
    
    # Apply area filter
    if filters['area'] != 'All Areas':
        filtered_df = filtered_df[filtered_df['Area'] == filters['area']]
    
    # Apply grade filter
    if filters['grade'] != 'All Grades':
        filtered_df = filtered_df[filtered_df['Grade'] == filters['grade']]
    
    # Apply performance range filter
    filtered_df = filtered_df[
        (filtered_df['Percentage'] >= filters['min_achievement']) &
        (filtered_df['Percentage'] <= filters['max_achievement'])
    ]
    
    # Apply category filter
    if filters['category'] != 'All Categories':
        filtered_df = filtered_df[filtered_df['Performance_Category'] == filters['category']]
    
    # Apply zero sales filter
    if not filters['show_zero_sales']:
        filtered_df = filtered_df[filtered_df['Sales'] > 0]
    
    # Apply target achievement filter
    if filters['target_achieved_only']:
        filtered_df = filtered_df[filtered_df['Percentage'] >= 100]
    
    return filtered_df


def display_filter_summary(filtered_data: pd.DataFrame, filters: Dict[str, Any]) -> None:
    """
    Display a summary of applied filters
    
    Args:
        filtered_data (pd.DataFrame): Filtered data
        filters (Dict[str, Any]): Applied filters
    """
    
    st.markdown("### 📋 Filter Summary")
    
    summary_text = f"""
    **Data yang ditampilkan:**
    - Total Records: {len(filtered_data):,}
    - Area: {filters['area']}
    - Grade: {filters['grade']}
    - Performance: {filters['min_achievement']}% - {filters['max_achievement']}%
    - Category: {filters['category']}
    """
    
    if not filters['show_zero_sales']:
        summary_text += "\n    - Excluding zero sales"
    
    if filters['target_achieved_only']:
        summary_text += "\n    - Target achieved only"
    
    st.markdown(summary_text)


def create_kpi_cards(df: pd.DataFrame) -> None:
    """
    Create and display KPI metric cards
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
    """
    
    # Calculate KPIs
    total_sales = df['Sales'].sum()
    total_target = df['Target'].sum()
    overall_achievement = (total_sales / total_target * 100) if total_target > 0 else 0
    total_people = len(df)
    avg_achievement = df['Percentage'].mean()
    
    # Performance distribution
    excellent_count = len(df[df['Performance_Category'] == 'Excellent'])
    good_count = len(df[df['Performance_Category'] == 'Good'])
    poor_count = len(df[df['Performance_Category'] == 'Poor'])
    
    # Display KPI cards in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Sales",
            value=f"{total_sales:,}",
            delta=f"Target: {total_target:,}"
        )
    
    with col2:
        st.metric(
            label="🎯 Overall Achievement",
            value=f"{overall_achievement:.1f}%",
            delta=f"Avg: {avg_achievement:.1f}%"
        )
    
    with col3:
        st.metric(
            label="👥 Total People",
            value=f"{total_people:,}",
            delta=f"Excellent: {excellent_count}"
        )
    
    with col4:
        achievement_color = "normal"
        if overall_achievement >= 100:
            achievement_color = "normal"
        elif overall_achievement >= 80:
            achievement_color = "normal"
        else:
            achievement_color = "inverse"
            
        st.metric(
            label="📈 Performance Status",
            value="On Track" if overall_achievement >= 80 else "Needs Attention",
            delta=f"Good: {good_count}, Poor: {poor_count}"
        )


def display_performance_table(df: pd.DataFrame, max_rows: int = 20) -> None:
    """
    Display a formatted performance table
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        max_rows (int): Maximum number of rows to display
    """
    
    st.markdown("### 📊 Detailed Performance Data")
    
    # Prepare display DataFrame
    display_df = df.copy()
    
    # Format columns for better display
    display_df['Sales'] = display_df['Sales'].apply(lambda x: f"{x:,}")
    display_df['Target'] = display_df['Target'].apply(lambda x: f"{x:,}")
    
    # Check if Minus/plus column exists before formatting
    if 'Minus/plus' in display_df.columns:
        display_df['Minus/plus'] = display_df['Minus/plus'].apply(lambda x: f"{x:+,}")
        columns_to_show = ['Nama', 'Area', 'SubArea', 'Grade', 'Target', 'Sales', 'Minus/plus', 'Percentage', 'Performance_Category']
        column_names = ['Name', 'Area', 'Sub Area', 'Grade', 'Target', 'Sales', 'Variance', 'Achievement %', 'Category']
    else:
        columns_to_show = ['Nama', 'Area', 'SubArea', 'Grade', 'Target', 'Sales', 'Percentage']
        column_names = ['Name', 'Area', 'Sub Area', 'Grade', 'Target', 'Sales', 'Achievement %']
    
    display_df['Percentage'] = display_df['Percentage'].apply(lambda x: f"{x:.1f}%")
    
    # Select columns to display (only those that exist)
    available_columns = [col for col in columns_to_show if col in display_df.columns]
    display_df = display_df[available_columns]
    
    # Rename columns for better readability
    display_df.columns = column_names[:len(available_columns)]
    
    # Display with pagination
    if len(display_df) > max_rows:
        st.info(f"Showing top {max_rows} records out of {len(display_df)} total records")
        display_df = display_df.head(max_rows)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


def create_export_options(df: pd.DataFrame) -> None:
    """
    Create export options for the filtered data
    
    Args:
        df (pd.DataFrame): Data to export
    """
    
    st.markdown("### 📥 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV Export
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📄 Download as CSV",
            data=csv_data,
            file_name=f"sales_performance_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download filtered data as CSV file"
        )
    
    with col2:
        # Summary Export
        summary_data = create_summary_report(df)
        st.download_button(
            label="📊 Download Summary Report",
            data=summary_data,
            file_name=f"sales_summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            help="Download summary analysis as text file"
        )


def create_summary_report(df: pd.DataFrame) -> str:
    """
    Create a text summary report of the data
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        str: Formatted summary report
    """
    
    total_sales = df['Sales'].sum()
    total_target = df['Target'].sum()
    overall_achievement = (total_sales / total_target * 100) if total_target > 0 else 0
    
    # Performance distribution
    performance_dist = df['Performance_Category'].value_counts()
    
    # Area performance
    area_performance = df.groupby('Area').agg({
        'Sales': 'sum',
        'Target': 'sum'
    })
    area_performance['Achievement'] = (area_performance['Sales'] / area_performance['Target'] * 100).round(1)
    
    report = f"""
SALES PERFORMANCE SUMMARY REPORT
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
=====================================

OVERALL METRICS:
- Total Sales: {total_sales:,}
- Total Target: {total_target:,}
- Overall Achievement: {overall_achievement:.1f}%
- Total Team Members: {len(df):,}

PERFORMANCE DISTRIBUTION:
"""
    
    for category, count in performance_dist.items():
        percentage = (count / len(df) * 100)
        report += f"- {category}: {count} people ({percentage:.1f}%)\n"
    
    report += f"""

TOP PERFORMING AREAS:
"""
    
    top_areas = area_performance.sort_values('Achievement', ascending=False).head(5)
    for area, row in top_areas.iterrows():
        report += f"- {area}: {row['Achievement']:.1f}% ({row['Sales']:,}/{row['Target']:,})\n"
    
    return report