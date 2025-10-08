"""
============================================================================
VISUALIZATION CHARTS MODULE
============================================================================

Author: Data Analyst Team
Version: 2.0 (Restructured)
Purpose: Handle all chart creation and visualization functions

This module contains:
- Performance visualization charts
- Area and grade analysis charts
- Scatter plots and distribution charts
- Improvement potential visualizations
- Interactive Plotly chart configurations
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Any
import streamlit as st


class ChartTheme:
    """Chart theme configuration and color palettes"""
    
    PERFORMANCE_COLORS = {
        'Excellent': '#28a745',
        'Good': '#17a2b8', 
        'Average': '#ffc107',
        'Below Average': '#fd7e14',
        'Poor': '#dc3545'
    }
    
    CHART_HEIGHT = 400
    LARGE_CHART_HEIGHT = 600
    
    @staticmethod
    def get_plotly_theme() -> Dict[str, Any]:
        """Get the standard theme configuration for Plotly charts"""
        return {
            'layout': {
                'font': {'family': 'Arial, sans-serif', 'size': 12},
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'colorway': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            }
        }


def create_area_achievement_chart(area_stats: pd.DataFrame) -> go.Figure:
    """
    Create achievement rate by area bar chart
    
    Args:
        area_stats (pd.DataFrame): Area performance statistics
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Color-coded achievement rates
        - Hover data with team size and sales info
        - Text labels on bars
        - Responsive design
    """
    
    if area_stats.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    area_stats_reset = area_stats.reset_index()
    
    fig = px.bar(
        area_stats_reset, 
        x='Area', 
        y='Achievement_Rate', 
        title='🏆 Achievement Rate by Area',
        color='Achievement_Rate', 
        color_continuous_scale='RdYlGn',
        text='Achievement_Rate',
        hover_data=['Team_Size', 'Total_Sales', 'Total_Target']
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        xaxis_title="Area",
        yaxis_title="Achievement Rate (%)",
        showlegend=False,
        height=ChartTheme.CHART_HEIGHT
    )
    
    return fig


def create_performance_distribution_pie(performance_dist: pd.Series) -> go.Figure:
    """
    Create performance distribution pie chart
    
    Args:
        performance_dist (pd.Series): Performance category distribution
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Color-coded performance categories
        - Percentage and label display
        - Interactive hover information
    """
    
    if performance_dist.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    colors = [ChartTheme.PERFORMANCE_COLORS.get(cat, '#gray') for cat in performance_dist.index]
    
    fig = px.pie(
        values=performance_dist.values, 
        names=performance_dist.index,
        title='📈 Performance Distribution',
        color_discrete_sequence=colors
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=ChartTheme.CHART_HEIGHT)
    
    return fig


def create_sales_vs_target_chart(subarea_stats: pd.DataFrame) -> go.Figure:
    """
    Create sales vs target comparison chart by sub-area
    
    Args:
        subarea_stats (pd.DataFrame): Sub-area statistics with sales and target data
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Grouped bar chart comparing sales vs target
        - Sorted by achievement rate
        - Text labels on bars
        - Responsive layout
    """
    
    if subarea_stats.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Target', 
        x=subarea_stats['SubArea'], 
        y=subarea_stats['Target'],
        marker_color='lightblue',
        text=subarea_stats['Target'],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Sales', 
        x=subarea_stats['SubArea'], 
        y=subarea_stats['Sales'],
        marker_color='darkblue',
        text=subarea_stats['Sales'],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Sales vs Target by Sub-Area (Sorted by Achievement)',
        barmode='group',
        xaxis_title="Sub-Area",
        yaxis_title="Amount",
        xaxis_tickangle=-45,
        height=500
    )
    
    return fig


def create_grade_achievement_chart(grade_stats: pd.DataFrame) -> go.Figure:
    """
    Create achievement rate by grade bar chart
    
    Args:
        grade_stats (pd.DataFrame): Grade performance statistics
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Color-coded by achievement rate
        - Text labels showing percentages
        - Viridis color scale
    """
    
    if grade_stats.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    grade_stats_reset = grade_stats.reset_index()
    
    fig = px.bar(
        grade_stats_reset,
        x='Grade',
        y='Achievement_Rate',
        title='Achievement Rate by Grade',
        color='Achievement_Rate',
        color_continuous_scale='Viridis',
        text='Achievement_Rate'
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=ChartTheme.CHART_HEIGHT)
    
    return fig


def create_grade_scatter_chart(grade_stats: pd.DataFrame) -> go.Figure:
    """
    Create scatter plot of average target vs sales by grade
    
    Args:
        grade_stats (pd.DataFrame): Grade performance statistics
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Bubble size based on team count
        - Color-coded by grade
        - 100% achievement reference line
        - Hover data with achievement rates
    """
    
    if grade_stats.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    grade_stats_reset = grade_stats.reset_index()
    
    fig = px.scatter(
        grade_stats_reset,
        x='Avg_Target',
        y='Avg_Sales',
        size='Count',
        color='Grade',
        title='Average Target vs Sales by Grade',
        hover_data=['Achievement_Rate']
    )
    
    # Add diagonal line for 100% achievement
    max_val = max(grade_stats_reset['Avg_Target'].max(), grade_stats_reset['Avg_Sales'].max())
    fig.add_trace(go.Scatter(
        x=[0, max_val], 
        y=[0, max_val],
        mode='lines', 
        name='100% Line',
        line=dict(dash='dash', color='red')
    ))
    
    fig.update_layout(height=ChartTheme.CHART_HEIGHT)
    
    return fig


def create_performance_scatter_plot(df: pd.DataFrame) -> go.Figure:
    """
    Create performance scatter plot: Target vs Sales
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Color-coded by performance category
        - Bubble size based on achievement percentage
        - 100% achievement reference line
        - Detailed hover information
    """
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    fig = px.scatter(
        df, 
        x='Target', 
        y='Sales', 
        color='Performance_Category', 
        size='Percentage',
        hover_data=['Nama', 'SubArea', 'Grade'],
        title='Performance Scatter Plot: Target vs Sales (Colored by Performance Category)',
        color_discrete_map=ChartTheme.PERFORMANCE_COLORS
    )
    
    # Add target achievement line
    max_target = df['Target'].max()
    fig.add_trace(go.Scatter(
        x=[0, max_target], 
        y=[0, max_target],
        mode='lines', 
        name='100% Achievement Line',
        line=dict(dash='dash', color='red', width=2)
    ))
    
    fig.update_layout(
        xaxis_title="Target",
        yaxis_title="Sales Achievement",
        height=ChartTheme.LARGE_CHART_HEIGHT
    )
    
    return fig


def create_stacked_performance_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create stacked bar chart of performance distribution by area
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Stacked bars showing performance categories
        - Color-coded performance levels
        - Area-wise breakdown
    """
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    area_performance_dist = df.groupby(['Area', 'Performance_Category']).size().unstack(fill_value=0)
    
    fig = px.bar(
        area_performance_dist.reset_index(),
        x='Area',
        y=['Excellent', 'Good', 'Average', 'Below Average', 'Poor'],
        title='Performance Category Distribution by Area',
        color_discrete_map=ChartTheme.PERFORMANCE_COLORS
    )
    
    fig.update_layout(
        barmode='stack',
        xaxis_title="Area",
        yaxis_title="Number of People",
        height=ChartTheme.CHART_HEIGHT
    )
    
    return fig


def create_improvement_priority_chart(improvement_df: pd.DataFrame, top_n: int = 8) -> go.Figure:
    """
    Create improvement priority bar chart
    
    Args:
        improvement_df (pd.DataFrame): Improvement potential data
        top_n (int): Number of top areas to display
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Priority score visualization
        - Color-coded by performance gap
        - Top N areas focus
        - Rotated x-axis labels
    """
    
    if improvement_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    top_areas = improvement_df.head(top_n)
    
    fig = px.bar(
        top_areas, 
        x='SubArea', 
        y='Priority_Score',
        color='Performance_Gap',
        title='🎯 Priority Areas for Improvement (Priority Score)',
        labels={'Priority_Score': 'Priority Score', 'Performance_Gap': 'Gap %'},
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=ChartTheme.CHART_HEIGHT
    )
    
    return fig


def create_revenue_potential_scatter(improvement_df: pd.DataFrame) -> go.Figure:
    """
    Create revenue potential scatter plot
    
    Args:
        improvement_df (pd.DataFrame): Improvement potential data
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Team size vs revenue potential
        - Bubble size based on priority score
        - Color-coded by current performance
        - Hover data with sub-area information
    """
    
    if improvement_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    fig = px.scatter(
        improvement_df,
        x='Team_Size',
        y='Revenue_Potential',
        size='Priority_Score',
        color='Current_Performance',
        hover_data=['SubArea'],
        title='💰 Revenue Recovery Potential',
        labels={'Revenue_Potential': 'Potential Revenue Recovery', 'Team_Size': 'Team Size'},
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(height=ChartTheme.CHART_HEIGHT)
    
    return fig


def create_performance_histogram(df: pd.DataFrame) -> go.Figure:
    """
    Create performance distribution histogram
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Achievement percentage distribution
        - Color-coded bins
        - Statistical insights
    """
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    fig = px.histogram(
        df,
        x='Percentage',
        nbins=20,
        title='Performance Distribution Histogram',
        labels={'Percentage': 'Achievement Percentage (%)', 'count': 'Number of People'},
        color_discrete_sequence=['#1f77b4']
    )
    
    fig.update_layout(
        xaxis_title="Achievement Percentage (%)",
        yaxis_title="Number of People",
        height=ChartTheme.CHART_HEIGHT
    )
    
    return fig


def create_trend_analysis_chart(df: pd.DataFrame, date_column: str = None) -> go.Figure:
    """
    Create trend analysis chart (if date data is available)
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        date_column (str): Date column name (optional)
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Time series analysis
        - Performance trends
        - Moving averages
    """
    
    if df.empty or date_column is None or date_column not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Trend analysis requires date data", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Group by date and calculate metrics
    daily_stats = df.groupby(date_column).agg({
        'Sales': 'sum',
        'Target': 'sum',
        'Percentage': 'mean'
    }).reset_index()
    
    daily_stats['Achievement_Rate'] = (daily_stats['Sales'] / daily_stats['Target'] * 100)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_stats[date_column],
        y=daily_stats['Achievement_Rate'],
        mode='lines+markers',
        name='Achievement Rate',
        line=dict(color='#1f77b4', width=2)
    ))
    
    fig.update_layout(
        title='Performance Trend Analysis',
        xaxis_title="Date",
        yaxis_title="Achievement Rate (%)",
        height=ChartTheme.CHART_HEIGHT
    )
    
    return fig


def create_comparison_chart(df1: pd.DataFrame, df2: pd.DataFrame, 
                          label1: str = "Period 1", label2: str = "Period 2") -> go.Figure:
    """
    Create comparison chart between two datasets
    
    Args:
        df1 (pd.DataFrame): First dataset
        df2 (pd.DataFrame): Second dataset
        label1 (str): Label for first dataset
        label2 (str): Label for second dataset
        
    Returns:
        go.Figure: Plotly figure object
        
    Features:
        - Side-by-side comparison
        - Performance metrics comparison
        - Visual difference highlighting
    """
    
    if df1.empty or df2.empty:
        fig = go.Figure()
        fig.add_annotation(text="Comparison requires two datasets", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Calculate metrics for both datasets
    metrics1 = {
        'Total Sales': df1['Sales'].sum(),
        'Total Target': df1['Target'].sum(),
        'Avg Performance': df1['Percentage'].mean(),
        'Team Size': len(df1)
    }
    
    metrics2 = {
        'Total Sales': df2['Sales'].sum(),
        'Total Target': df2['Target'].sum(),
        'Avg Performance': df2['Percentage'].mean(),
        'Team Size': len(df2)
    }
    
    categories = list(metrics1.keys())
    values1 = list(metrics1.values())
    values2 = list(metrics2.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name=label1,
        x=categories,
        y=values1,
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name=label2,
        x=categories,
        y=values2,
        marker_color='darkblue'
    ))
    
    fig.update_layout(
        title=f'Performance Comparison: {label1} vs {label2}',
        barmode='group',
        height=ChartTheme.CHART_HEIGHT
    )
    
    return fig


def display_chart(fig: go.Figure, use_container_width: bool = True) -> None:
    """
    Display a Plotly chart in Streamlit
    
    Args:
        fig (go.Figure): Plotly figure object
        use_container_width (bool): Whether to use container width
        
    Features:
        - Streamlit integration
        - Responsive display
        - Error handling
    """
    
    try:
        st.plotly_chart(fig, use_container_width=use_container_width)
    except Exception as e:
        st.error(f"Error displaying chart: {str(e)}")
        st.info("Please check your data and try again.")


def create_custom_chart(df: pd.DataFrame, chart_type: str, **kwargs) -> go.Figure:
    """
    Create custom chart based on type and parameters
    
    Args:
        df (pd.DataFrame): Data for the chart
        chart_type (str): Type of chart to create
        **kwargs: Additional chart parameters
        
    Returns:
        go.Figure: Plotly figure object
        
    Supported chart types:
        - 'bar', 'scatter', 'line', 'pie', 'histogram', 'box'
    """
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available for custom chart", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    try:
        if chart_type == 'bar':
            fig = px.bar(df, **kwargs)
        elif chart_type == 'scatter':
            fig = px.scatter(df, **kwargs)
        elif chart_type == 'line':
            fig = px.line(df, **kwargs)
        elif chart_type == 'pie':
            fig = px.pie(df, **kwargs)
        elif chart_type == 'histogram':
            fig = px.histogram(df, **kwargs)
        elif chart_type == 'box':
            fig = px.box(df, **kwargs)
        else:
            fig = go.Figure()
            fig.add_annotation(text=f"Unsupported chart type: {chart_type}", 
                              xref="paper", yref="paper",
                              x=0.5, y=0.5, showarrow=False)
        
        fig.update_layout(height=ChartTheme.CHART_HEIGHT)
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error creating chart: {str(e)}", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig