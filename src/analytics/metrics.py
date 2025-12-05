# src/analytics/metrics.py
import pandas as pd

def calculate_team_metrics(df):
    metrics = {
        'total_team_size': len(df),
        'total_target': df['Target'].sum(),
        'total_sales': df['Sales'].sum(),
        'overall_achievement': (df['Sales'].sum() / df['Target'].sum() * 100).round(2) if df['Target'].sum() > 0 else 0,
        'avg_individual_performance': df['Percentage'].mean().round(2) if not df.empty else 0,
        'performance_std': df['Percentage'].std().round(2) if not df.empty else 0,
        'top_performer': df.loc[df['Percentage'].idxmax(), 'Nama'] if not df.empty else 'N/A',
        'top_performance': df['Percentage'].max() if not df.empty else 0,
        'bottom_performer': df.loc[df['Percentage'].idxmin(), 'Nama'] if not df.empty else 'N/A',
        'bottom_performance': df['Percentage'].min() if not df.empty else 0,
        'zero_sales_count': len(df[df['Sales'] == 0]),
        'excellent_performers': len(df[df['Performance_Category'] == 'Excellent']),
        'good_performers': len(df[df['Performance_Category'] == 'Good']),
        'needs_improvement': len(df[df['Performance_Category'].isin(['Below Average', 'Poor'])])
    }
    return metrics

def get_area_performance(df):
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

def get_grade_analysis(df):
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
