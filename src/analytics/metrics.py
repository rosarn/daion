"""
============================================================================
ANALYTICS METRICS MODULE
============================================================================

Author: Data Analyst Team
Version: 2.0 (Restructured)
Purpose: Handle performance calculations, metrics, and business intelligence

This module contains:
- Team performance metrics calculation
- Area and grade analysis functions
- Performance improvement analysis
- Business intelligence insights
- ROI and potential calculations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from ..data.models import TeamMetrics, AreaStats, GradeStats


def calculate_team_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate comprehensive team performance metrics
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        Dict[str, Any]: Dictionary with key performance indicators
        
    Features:
        - Overall team performance statistics
        - Individual performance insights
        - Performance distribution analysis
        - Top and bottom performer identification
    """
    
    if df.empty:
        return {
            'total_team_size': 0,
            'total_target': 0,
            'total_sales': 0,
            'overall_achievement': 0,
            'avg_individual_performance': 0,
            'performance_std': 0,
            'top_performer': 'N/A',
            'top_performance': 0,
            'bottom_performer': 'N/A',
            'bottom_performance': 0,
            'zero_sales_count': 0,
            'excellent_performers': 0,
            'good_performers': 0,
            'needs_improvement': 0
        }
    
    metrics = {
        'total_team_size': len(df),
        'total_target': df['Target'].sum(),
        'total_sales': df['Sales'].sum(),
        'overall_achievement': (df['Sales'].sum() / df['Target'].sum() * 100).round(2) if df['Target'].sum() > 0 else 0,
        'avg_individual_performance': df['Percentage'].mean().round(2),
        'performance_std': df['Percentage'].std().round(2),
        'top_performer': df.loc[df['Percentage'].idxmax(), 'Nama'] if not df.empty else 'N/A',
        'top_performance': df['Percentage'].max(),
        'bottom_performer': df.loc[df['Percentage'].idxmin(), 'Nama'] if not df.empty else 'N/A',
        'bottom_performance': df['Percentage'].min(),
        'zero_sales_count': len(df[df['Sales'] == 0]),
        'excellent_performers': len(df[df['Performance_Category'] == 'Excellent']),
        'good_performers': len(df[df['Performance_Category'] == 'Good']),
        'needs_improvement': len(df[df['Performance_Category'].isin(['Below Average', 'Poor'])])
    }
    
    return metrics


def get_area_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze performance by geographical area
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with area-level metrics
        
    Features:
        - Area-wise performance aggregation
        - Achievement rate calculation
        - Team size and performance statistics
        - Sorted by achievement rate
    """
    
    if df.empty:
        return pd.DataFrame()
    
    area_stats = df.groupby('Area').agg({
        'Target': 'sum',
        'Sales': 'sum',
        'Percentage': ['mean', 'std', 'count'],
        'Nama': 'count'
    }).round(2)
    
    area_stats.columns = ['Total_Target', 'Total_Sales', 'Avg_Performance', 'Performance_Std', 'Performance_Count', 'Team_Size']
    area_stats['Achievement_Rate'] = (area_stats['Total_Sales'] / area_stats['Total_Target'] * 100).round(2)
    area_stats = area_stats.sort_values('Achievement_Rate', ascending=False)
    
    return area_stats


def get_grade_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze performance by role/grade
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with role-level insights
        
    Features:
        - Role-based performance analysis
        - Target and sales aggregation by grade
        - Performance statistics by role
        - Achievement rate calculation
    """
    
    if df.empty:
        return pd.DataFrame()
    
    grade_stats = df.groupby('Grade').agg({
        'Target': ['sum', 'mean'],
        'Sales': ['sum', 'mean'],
        'Percentage': ['mean', 'std'],
        'Nama': 'count'
    }).round(2)
    
    grade_stats.columns = ['Total_Target', 'Avg_Target', 'Total_Sales', 'Avg_Sales', 'Avg_Performance', 'Performance_Std', 'Count']
    grade_stats['Achievement_Rate'] = (grade_stats['Total_Sales'] / grade_stats['Total_Target'] * 100).round(2)
    
    return grade_stats


def analyze_performance_segments(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Segment performers into different categories for targeted analysis
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        Dict[str, pd.DataFrame]: Dictionary containing different performance segments
    """
    
    segments = {
        'excellent_performers': df[df['Performance_Category'] == 'Excellent'],
        'good_performers': df[df['Performance_Category'] == 'Good'],
        'average_performers': df[df['Performance_Category'] == 'Average'],
        'below_average_performers': df[df['Performance_Category'] == 'Below Average'],
        'poor_performers': df[df['Performance_Category'] == 'Poor'],
        'zero_sales': df[df['Sales'] == 0],
        'medium_performers': df[df['Percentage'].between(50, 80)],
        'high_potential': df[(df['Percentage'] >= 80) & (df['Percentage'] < 100)]
    }
    
    return segments


def calculate_improvement_potential(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate improvement potential by sub-area
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with improvement potential analysis
        
    Features:
        - Performance gap analysis
        - Revenue recovery potential
        - Priority scoring for intervention
        - Team size consideration
    """
    
    if df.empty:
        return pd.DataFrame()
    
    improvement_data = []
    
    for area in df['SubArea'].unique():
        area_data = df[df['SubArea'] == area]
        current_perf = area_data['Percentage'].mean()
        team_size = len(area_data)
        total_gap = area_data['Minus/plus'].sum()
        potential_revenue = abs(total_gap) if total_gap < 0 else 0
        
        improvement_data.append({
            'SubArea': area,
            'Current_Performance': current_perf,
            'Team_Size': team_size,
            'Performance_Gap': 100 - current_perf if current_perf < 100 else 0,
            'Revenue_Potential': potential_revenue,
            'Priority_Score': (100 - current_perf) * team_size if current_perf < 100 else 0
        })
    
    improvement_df = pd.DataFrame(improvement_data)
    improvement_df = improvement_df.sort_values('Priority_Score', ascending=False)
    
    return improvement_df


def generate_executive_insights(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate executive-level insights and recommendations
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        Dict[str, Any]: Executive insights and metrics
        
    Features:
        - Overall status assessment
        - Risk level calculation
        - Quick win identification
        - Benchmark performer analysis
    """
    
    if df.empty:
        return {
            'overall_status': 'No Data',
            'overall_achievement': 0,
            'risk_level': 0,
            'risk_status': 'No Data',
            'quick_wins': 0,
            'benchmarks': 0
        }
    
    # Performance segments
    segments = analyze_performance_segments(df)
    
    # Overall achievement
    overall_achievement = (df['Sales'].sum() / df['Target'].sum() * 100) if df['Target'].sum() > 0 else 0
    
    # Status determination
    if overall_achievement >= 100:
        status = "🟢 Excellent"
    elif overall_achievement >= 80:
        status = "🟡 Good"
    else:
        status = "🔴 Needs Attention"
    
    # Risk level calculation
    poor_performers = segments['poor_performers']
    risk_level = len(poor_performers) / len(df) * 100 if len(df) > 0 else 0
    
    if risk_level > 30:
        risk_status = "🔴 High Risk"
    elif risk_level > 15:
        risk_status = "🟡 Medium Risk"
    else:
        risk_status = "🟢 Low Risk"
    
    return {
        'overall_status': status,
        'overall_achievement': overall_achievement,
        'risk_level': risk_level,
        'risk_status': risk_status,
        'quick_wins': len(segments['medium_performers']),
        'benchmarks': len(segments['excellent_performers'])
    }


def calculate_critical_areas(df: pd.DataFrame, top_n: int = 3) -> pd.Series:
    """
    Identify critical areas that need immediate attention
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        top_n (int): Number of top critical areas to return
        
    Returns:
        pd.Series: Critical areas with their achievement rates
    """
    
    if df.empty:
        return pd.Series()
    
    area_performance = get_area_performance(df)
    
    if area_performance.empty:
        return pd.Series()
    
    # Filter areas with below 80% achievement
    critical_areas = area_performance[area_performance['Achievement_Rate'] < 80]
    critical_areas = critical_areas.sort_values('Achievement_Rate')
    
    return critical_areas['Achievement_Rate'].head(top_n)


def calculate_best_areas(df: pd.DataFrame, top_n: int = 3) -> pd.Series:
    """
    Identify best performing areas for benchmarking
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        top_n (int): Number of top areas to return
        
    Returns:
        pd.Series: Best performing areas with their achievement rates
    """
    
    if df.empty:
        return pd.Series()
    
    area_performance = get_area_performance(df)
    
    if area_performance.empty:
        return pd.Series()
    
    # Get top performing areas
    best_areas = area_performance.sort_values('Achievement_Rate', ascending=False)
    
    return best_areas['Achievement_Rate'].head(top_n)


def calculate_roi_projections(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate ROI projections from improvement recommendations
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        Dict[str, float]: ROI projection metrics
        
    Features:
        - Potential revenue recovery calculation
        - Quick win potential assessment
        - Total improvement potential
        - ROI percentage calculation
    """
    
    if df.empty:
        return {
            'potential_recovery': 0,
            'quick_win_potential': 0,
            'total_potential': 0,
            'roi_percentage': 0
        }
    
    # Calculate improvement potential
    improvement_df = calculate_improvement_potential(df)
    potential_recovery = improvement_df['Revenue_Potential'].sum() if not improvement_df.empty else 0
    
    # Quick win potential (assume 5 unit improvement per medium performer)
    segments = analyze_performance_segments(df)
    quick_win_potential = len(segments['medium_performers']) * 5
    
    # Total potential
    total_potential = potential_recovery + quick_win_potential
    
    # ROI percentage
    total_target = df['Target'].sum()
    roi_percentage = (total_potential / total_target * 100) if total_target > 0 else 0
    
    return {
        'potential_recovery': potential_recovery,
        'quick_win_potential': quick_win_potential,
        'total_potential': total_potential,
        'roi_percentage': roi_percentage
    }


def generate_action_timeline() -> pd.DataFrame:
    """
    Generate recommended action timeline for performance improvement
    
    Returns:
        pd.DataFrame: Action timeline with priorities and expected impact
    """
    
    timeline_data = {
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Month 2', 'Month 3'],
        'Priority Actions': [
            '🚨 Address zero-sales performers',
            '📊 Implement daily tracking for critical areas', 
            '🎯 Launch quick-win coaching programs',
            '📈 Begin performance recovery programs',
            '🏆 Establish mentoring partnerships',
            '📋 Review and optimize based on results'
        ],
        'Expected Impact': ['Immediate', 'Short-term', 'Short-term', 'Medium-term', 'Long-term', 'Sustained']
    }
    
    return pd.DataFrame(timeline_data)


def calculate_performance_distribution(df: pd.DataFrame) -> Dict[str, int]:
    """
    Calculate performance distribution across categories
    
    Args:
        df (pd.DataFrame): Sales data DataFrame
        
    Returns:
        Dict[str, int]: Performance distribution counts
    """
    
    if df.empty:
        return {category: 0 for category in ['Excellent', 'Good', 'Average', 'Below Average', 'Poor']}
    
    distribution = df['Performance_Category'].value_counts().to_dict()
    
    # Ensure all categories are present
    categories = ['Excellent', 'Good', 'Average', 'Below Average', 'Poor']
    for category in categories:
        if category not in distribution:
            distribution[category] = 0
    
    return distribution