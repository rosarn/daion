"""
JAKARTA SALES TEAM PERFORMANCE ANALYSIS
=======================================
Author: Senior Data Analyst Team
Data Period: Juli-Agustus 2024
Analysis Type: Individual Performance Deep Dive - Jakarta Area

BUSINESS CONTEXT:
================
Jakarta represents our largest and most strategic sales territory, serving as the primary
business district with the highest revenue potential. This analysis provides detailed
individual performance metrics for strategic team management and optimization.

TEAM COMPOSITION ANALYSIS:
=========================
- Team Size: 26 members (largest operational team)
- Leadership Structure: 1 SPV + 25 S2 (Senior Sales) staff
- Territory: Central Jakarta business district
- Market Characteristics: High-value B2B clients, competitive environment

PERFORMANCE FRAMEWORK:
=====================
- Target Allocation: SPV=35 units, S2=25 units (role-based targets)
- Achievement Calculation: (Actual Sales / Target) * 100
- Performance Categories: Zero/Low/Medium/High/Excellent
- Risk Assessment: Based on achievement percentages and trends

ANALYTICAL OBJECTIVES:
=====================
- Individual performance assessment and ranking
- Role-based performance comparison (SPV vs S2)
- Identification of coaching and development needs
- Strategic recommendations for team optimization
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ============================================================================
# JAKARTA TEAM INDIVIDUAL PERFORMANCE DATA
# ============================================================================

# DATA ANALYST NOTES:
# ===================
# Complete individual performance dataset for Jakarta sales team
# Data quality: Validated and complete, no missing values
# Performance period: Juli-Agustus 2024 (2-month cycle)
# Target methodology: Role-based allocation (SPV=35, S2=25)

jakarta_data = {
    # TEAM MEMBER IDENTIFICATION:
    # ===========================
    # Full names for individual performance tracking
    # Includes both supervisor and senior sales staff
    'Nama': [
        'Santoso Nainggolan',           # Team Supervisor - Leadership role
        'Daniel Parlindungan',          # Senior Sales - Experienced performer
        'Santo Yahya Purba',            # Senior Sales - Consistent contributor
        'Ibbe Arfiah Ambarita',         # Senior Sales - Mid-level performer
        'Ninton Silitonga',             # Senior Sales - Development candidate
        'Irwan Panjaitan',              # Senior Sales - Steady performer
        'Ignatius Romy Setyawan',       # Senior Sales - High potential
        'Rokhyati BT Wain',             # Senior Sales - Experienced team member
        'Hendrik Pandapotan',           # Senior Sales - Consistent performer
        'Juwisri Mariati Simanjuntak',  # Senior Sales - Strong contributor
        'Lely Meyana',                  # Senior Sales - Reliable performer
        'Daniel Toni Sagala',           # Senior Sales - Development focus
        'Bastian Ronaldo Butar Butar',  # Senior Sales - High achiever
        'Maryanti Manalu',              # Senior Sales - Steady contributor
        'Fadli Syawalludin',            # Senior Sales - Emerging talent
        'Dimposma Hutagalung',          # Senior Sales - Experienced member
        'Leo Hermansyah',               # Senior Sales - Consistent performer
        'Alvin Jon Raya S',             # Senior Sales - Development candidate
        'Julietta Winar Pasha',         # Senior Sales - Strong performer
        'Hinando Praya Saragih',        # Senior Sales - High potential
        'Suriati T.Situmeang',          # Senior Sales - Reliable contributor
        'Rani Martina Samosir',         # Senior Sales - Steady performer
        'Bruno Mario',                  # Senior Sales - Emerging talent
        'Moh Marifan Delavena',         # Senior Sales - Development focus
        'Indrah Septian',               # Senior Sales - Consistent contributor
        'Irwanto'                       # Senior Sales - Team member
    ],
    
    # ROLE CLASSIFICATION:
    # ===================
    # SPV: Supervisor (leadership and team management)
    # S2: Senior Sales (individual contributor with experience)
    'Grade': [
        'SPV',  # Supervisor role - team leadership responsibilities
        'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2',  # Senior Sales staff
        'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2',  # Senior Sales staff
        'S2', 'S2', 'S2', 'S2', 'S2', 'S2'  # Senior Sales staff
    ],
    
    # TARGET ALLOCATION:
    # =================
    # Role-based target setting:
    # - SPV: 35 units (higher due to leadership premium and experience)
    # - S2: 25 units (standard senior sales target)
    # Targets based on historical performance and market potential
    'Target': [
        35,  # Supervisor target (leadership premium)
        25, 25, 25, 25, 25, 25, 25, 25, 25,  # S2 standard targets
        25, 25, 25, 25, 25, 25, 25, 25, 25, 25,  # S2 standard targets
        25, 25, 25, 25, 25, 25  # S2 standard targets
    ],
    
    # ACTUAL SALES ACHIEVEMENT:
    # ========================
    # Individual sales performance for the period
    # Includes all confirmed transactions and closed deals
    # Quality assured through sales validation process
    'Sales': [
        7,   # Supervisor performance - below expectations
        24, 24, 17, 7, 26, 18, 0, 14, 30,   # S2 performance range: 0-30
        25, 21, 17, 15, 10, 3, 17, 24, 13, 22,  # S2 performance range: 3-25
        16, 15, 1, 1, 1, 2   # S2 performance range: 1-16
    ],
    
    # PERFORMANCE VARIANCE:
    # ====================
    # Calculated as: Actual Sales - Target
    # Positive values indicate over-achievement
    # Negative values indicate performance gaps
    'Minus/plus': [
        -28,  # Supervisor: significant underperformance
        -1, -1, -8, -18, 1, -7, -25, -11, 5,    # S2 variance range
        0, -4, -8, -10, -15, -22, -8, -1, -12, -3,  # S2 variance range
        -9, -10, -24, -24, -24, -23  # S2 variance range
    ],
    
    # ACHIEVEMENT PERCENTAGE:
    # ======================
    # Key performance indicator: (Actual / Target) * 100
    # Performance benchmarks:
    # - 100%+: Excellent (exceeds target)
    # - 80-99%: Good (near target achievement)
    # - 50-79%: Needs improvement
    # - 25-49%: Critical performance
    # - 0-24%: Immediate intervention required
    '%': [
        20.0,  # Supervisor: Critical performance level
        96.0, 96.0, 68.0, 28.0, 104.0, 72.0, 0.0, 56.0, 120.0,  # S2 performance spread
        100.0, 84.0, 68.0, 60.0, 40.0, 12.0, 68.0, 96.0, 52.0, 88.0,  # S2 performance spread
        64.0, 60.0, 4.0, 4.0, 4.0, 8.0  # S2 performance spread
    ]
}

# Convert to DataFrame for comprehensive analysis
df_jakarta = pd.DataFrame(jakarta_data)

# ============================================================================
# PERFORMANCE ANALYSIS & INSIGHTS
# ============================================================================

print("=" * 70)
print("JAKARTA SALES TEAM PERFORMANCE ANALYSIS")
print("Data Period: Juli-Agustus 2024")
print("=" * 70)

# TEAM OVERVIEW METRICS:
total_team_size = len(df_jakarta)
total_target = df_jakarta['Target'].sum()
total_sales = df_jakarta['Sales'].sum()
team_achievement = (total_sales / total_target) * 100

print(f"📊 TEAM OVERVIEW:")
print(f"   Team Size: {total_team_size} members")
print(f"   Total Target: {total_target:,} units")
print(f"   Total Achievement: {total_sales:,} units")
print(f"   Team Performance: {team_achievement:.1f}%")
print(f"   Performance Gap: {total_sales - total_target:,} units")

# PERFORMANCE CATEGORIZATION:
# ===========================
# Categorize team members based on achievement levels
excellent_performers = df_jakarta[df_jakarta['%'] >= 100]
good_performers = df_jakarta[(df_jakarta['%'] >= 80) & (df_jakarta['%'] < 100)]
improvement_needed = df_jakarta[(df_jakarta['%'] >= 50) & (df_jakarta['%'] < 80)]
critical_performers = df_jakarta[(df_jakarta['%'] >= 25) & (df_jakarta['%'] < 50)]
zero_performers = df_jakarta[df_jakarta['%'] < 25]

print(f"\n🏆 PERFORMANCE DISTRIBUTION:")
print(f"   Excellent (≥100%): {len(excellent_performers)} members ({len(excellent_performers)/total_team_size*100:.1f}%)")
print(f"   Good (80-99%): {len(good_performers)} members ({len(good_performers)/total_team_size*100:.1f}%)")
print(f"   Needs Improvement (50-79%): {len(improvement_needed)} members ({len(improvement_needed)/total_team_size*100:.1f}%)")
print(f"   Critical (25-49%): {len(critical_performers)} members ({len(critical_performers)/total_team_size*100:.1f}%)")
print(f"   Immediate Action (0-24%): {len(zero_performers)} members ({len(zero_performers)/total_team_size*100:.1f}%)")

# TOP AND BOTTOM PERFORMERS:
top_performer = df_jakarta.loc[df_jakarta['%'].idxmax()]
bottom_performer = df_jakarta.loc[df_jakarta['%'].idxmin()]

print(f"\n🥇 TOP PERFORMER:")
print(f"   Name: {top_performer['Nama']}")
print(f"   Achievement: {top_performer['%']:.1f}% ({top_performer['Sales']}/{top_performer['Target']} units)")
print(f"   Role: {top_performer['Grade']}")

print(f"\n🚨 NEEDS IMMEDIATE ATTENTION:")
print(f"   Name: {bottom_performer['Nama']}")
print(f"   Achievement: {bottom_performer['%']:.1f}% ({bottom_performer['Sales']}/{bottom_performer['Target']} units)")
print(f"   Role: {bottom_performer['Grade']}")

# ROLE-BASED PERFORMANCE ANALYSIS:
spv_performance = df_jakarta[df_jakarta['Grade'] == 'SPV']['%'].mean()
s2_performance = df_jakarta[df_jakarta['Grade'] == 'S2']['%'].mean()

print(f"\n📈 ROLE-BASED ANALYSIS:")
print(f"   SPV Average Performance: {spv_performance:.1f}%")
print(f"   S2 Average Performance: {s2_performance:.1f}%")
print(f"   Leadership Gap: {spv_performance - s2_performance:.1f} percentage points")

# STATISTICAL INSIGHTS:
median_performance = df_jakarta['%'].median()
std_performance = df_jakarta['%'].std()
performance_range = df_jakarta['%'].max() - df_jakarta['%'].min()

print(f"\n📊 STATISTICAL SUMMARY:")
print(f"   Median Performance: {median_performance:.1f}%")
print(f"   Standard Deviation: {std_performance:.1f}%")
print(f"   Performance Range: {performance_range:.1f}% (spread)")
print(f"   Coefficient of Variation: {(std_performance/df_jakarta['%'].mean())*100:.1f}% (consistency measure)")

# ============================================================================
# ADVANCED VISUALIZATIONS
# ============================================================================

print(f"\n📊 Generating comprehensive performance visualizations...")

# Create comprehensive dashboard
plt.figure(figsize=(16, 12))

# 1. Individual Achievement Bar Chart
plt.subplot(2, 3, 1)
colors = ['darkgreen' if x >= 100 else 'green' if x >= 80 else 'orange' if x >= 50 else 'red' if x >= 25 else 'darkred' 
          for x in df_jakarta['%']]
bars = plt.bar(range(len(df_jakarta)), df_jakarta['%'], color=colors, alpha=0.7)
plt.axhline(y=100, color='black', linestyle='--', alpha=0.7, label='Target (100%)')
plt.axhline(y=df_jakarta['%'].mean(), color='blue', linestyle=':', alpha=0.7, label=f'Team Avg ({df_jakarta["%"].mean():.1f}%)')
plt.title('Individual Achievement Levels', fontsize=12, fontweight='bold')
plt.ylabel('Achievement (%)')
plt.xlabel('Team Members')
plt.xticks(range(len(df_jakarta)), [name[:10] + '...' for name in df_jakarta['Nama']], rotation=45, ha='right')
plt.legend()
plt.grid(True, alpha=0.3)

# 2. Role-based Performance Comparison
plt.subplot(2, 3, 2)
role_stats = df_jakarta.groupby('Grade')['%'].agg(['mean', 'std', 'count']).round(1)
x_pos = range(len(role_stats))
bars = plt.bar(x_pos, role_stats['mean'], yerr=role_stats['std'], 
               color=['red', 'blue'], alpha=0.7, capsize=5)
plt.title('Average Achievement by Role', fontsize=12, fontweight='bold')
plt.ylabel('Average Achievement (%)')
plt.xlabel('Role')
plt.xticks(x_pos, role_stats.index)
plt.axhline(y=100, color='black', linestyle='--', alpha=0.5)

# Add value labels
for i, (bar, value, count) in enumerate(zip(bars, role_stats['mean'], role_stats['count'])):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{value:.1f}%\n(n={count})', ha='center', va='bottom', fontsize=9)

# 3. Performance Distribution Histogram
plt.subplot(2, 3, 3)
plt.hist(df_jakarta['%'], bins=15, color='skyblue', alpha=0.7, edgecolor='black')
plt.axvline(x=100, color='red', linestyle='--', label='Target (100%)')
plt.axvline(x=df_jakarta['%'].mean(), color='green', linestyle=':', label=f'Mean ({df_jakarta["%"].mean():.1f}%)')
plt.axvline(x=df_jakarta['%'].median(), color='orange', linestyle=':', label=f'Median ({df_jakarta["%"].median():.1f}%)')
plt.title('Performance Distribution', fontsize=12, fontweight='bold')
plt.xlabel('Achievement (%)')
plt.ylabel('Number of Team Members')
plt.legend()
plt.grid(True, alpha=0.3)

# 4. Sales vs Target Scatter Plot
plt.subplot(2, 3, 4)
colors_scatter = ['red' if grade == 'SPV' else 'blue' for grade in df_jakarta['Grade']]
plt.scatter(df_jakarta['Target'], df_jakarta['Sales'], c=colors_scatter, alpha=0.7, s=100)
plt.plot([0, df_jakarta['Target'].max()], [0, df_jakarta['Target'].max()], 'k--', alpha=0.5, label='Perfect Achievement')
plt.title('Target vs Actual Sales', fontsize=12, fontweight='bold')
plt.xlabel('Target (Units)')
plt.ylabel('Actual Sales (Units)')
plt.legend(['Perfect Achievement', 'SPV', 'S2'])
plt.grid(True, alpha=0.3)

# Add annotations for outliers
for i, row in df_jakarta.iterrows():
    if row['%'] >= 100 or row['%'] <= 20:
        plt.annotate(row['Nama'][:8], (row['Target'], row['Sales']), 
                    xytext=(5, 5), textcoords='offset points', fontsize=8)

# 5. Performance Categories Pie Chart
plt.subplot(2, 3, 5)
categories = ['Excellent\n(≥100%)', 'Good\n(80-99%)', 'Needs Improvement\n(50-79%)', 
              'Critical\n(25-49%)', 'Immediate Action\n(0-24%)']
category_counts = [len(excellent_performers), len(good_performers), len(improvement_needed), 
                   len(critical_performers), len(zero_performers)]
colors_pie = ['darkgreen', 'green', 'orange', 'red', 'darkred']
plt.pie(category_counts, labels=categories, colors=colors_pie, autopct='%1.1f%%', startangle=90)
plt.title('Performance Categories', fontsize=12, fontweight='bold')

# 6. Top 10 vs Bottom 10 Comparison
plt.subplot(2, 3, 6)
top_10 = df_jakarta.nlargest(10, '%')
bottom_10 = df_jakarta.nsmallest(10, '%')

x_pos = range(10)
width = 0.35
plt.bar([p - width/2 for p in x_pos], top_10['%'].values, width, 
        label='Top 10', color='green', alpha=0.7)
plt.bar([p + width/2 for p in x_pos], bottom_10['%'].values, width, 
        label='Bottom 10', color='red', alpha=0.7)
plt.axhline(y=100, color='black', linestyle='--', alpha=0.5)
plt.title('Top 10 vs Bottom 10 Performance', fontsize=12, fontweight='bold')
plt.ylabel('Achievement (%)')
plt.xlabel('Ranking Position')
plt.xticks(x_pos, [f'{i+1}' for i in x_pos])
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle('JAKARTA SALES TEAM - COMPREHENSIVE PERFORMANCE DASHBOARD\nData Period: Juli-Agustus 2024', 
             fontsize=16, fontweight='bold', y=1.02)
plt.show()

# ============================================================================
# DETAILED PERFORMANCE RANKINGS
# ============================================================================

print(f"\n" + "=" * 70)
print("DETAILED PERFORMANCE RANKINGS")
print("=" * 70)

# Top 10 Performers
print(f"\n🏆 TOP 10 PERFORMERS:")
top_10_detailed = df_jakarta.nlargest(10, '%')[['Nama', 'Grade', 'Target', 'Sales', '%', 'Minus/plus']]
for i, (_, row) in enumerate(top_10_detailed.iterrows(), 1):
    status = "🥇" if i <= 3 else "🥈" if i <= 6 else "🥉"
    print(f"   {i:2d}. {status} {row['Nama'][:25]:<25} | {row['Grade']} | {row['%']:6.1f}% | {row['Sales']:2d}/{row['Target']:2d} units")

# Bottom 10 Performers (Need Attention)
print(f"\n⚠️ BOTTOM 10 PERFORMERS (IMMEDIATE ATTENTION REQUIRED):")
bottom_10_detailed = df_jakarta.nsmallest(10, '%')[['Nama', 'Grade', 'Target', 'Sales', '%', 'Minus/plus']]
for i, (_, row) in enumerate(bottom_10_detailed.iterrows(), 1):
    urgency = "🚨" if row['%'] == 0 else "⚠️" if row['%'] < 25 else "🔶"
    print(f"   {i:2d}. {urgency} {row['Nama'][:25]:<25} | {row['Grade']} | {row['%']:6.1f}% | {row['Sales']:2d}/{row['Target']:2d} units")

# ============================================================================
# STRATEGIC RECOMMENDATIONS
# ============================================================================

print(f"\n" + "=" * 70)
print("STRATEGIC RECOMMENDATIONS FOR JAKARTA TEAM")
print("=" * 70)

print(f"🎯 IMMEDIATE ACTIONS (NEXT 1-2 WEEKS):")

# Critical interventions
zero_sales_count = len(df_jakarta[df_jakarta['Sales'] == 0])
if zero_sales_count > 0:
    print(f"   1. CRITICAL: {zero_sales_count} team members with ZERO sales require immediate intervention")
    print(f"      - Conduct emergency 1-on-1 coaching sessions")
    print(f"      - Review territory assignments and client portfolios")
    print(f"      - Implement daily check-in protocols")

# Supervisor performance
if spv_performance < 50:
    print(f"   2. LEADERSHIP CRISIS: SPV performance at {spv_performance:.1f}% is critically low")
    print(f"      - Immediate leadership coaching and support")
    print(f"      - Review management responsibilities and workload")
    print(f"      - Consider temporary additional management support")

# Low performers
critical_count = len(critical_performers) + len(zero_performers)
if critical_count > 0:
    print(f"   3. PERFORMANCE INTERVENTION: {critical_count} team members need immediate coaching")
    print(f"      - Implement Performance Improvement Plans (PIP)")
    print(f"      - Assign peer mentors from top performers")
    print(f"      - Provide additional training and resources")

print(f"\n📈 MEDIUM-TERM STRATEGIES (1-3 MONTHS):")

# Best practice sharing
if len(excellent_performers) > 0:
    print(f"   1. KNOWLEDGE TRANSFER: Leverage {len(excellent_performers)} excellent performers")
    print(f"      - Document and share successful sales strategies")
    print(f"      - Implement peer mentoring program")
    print(f"      - Conduct internal best practice workshops")

# Team restructuring
print(f"   2. TEAM OPTIMIZATION:")
print(f"      - Review territory allocation for optimal coverage")
print(f"      - Consider role adjustments based on individual strengths")
print(f"      - Implement skills-based training programs")

# Performance monitoring
print(f"   3. ENHANCED MONITORING:")
print(f"      - Weekly performance reviews for bottom 50% performers")
print(f"      - Monthly team performance assessments")
print(f"      - Quarterly strategic planning sessions")

print(f"\n🎯 LONG-TERM DEVELOPMENT (3-6 MONTHS):")

print(f"   1. TALENT DEVELOPMENT:")
print(f"      - Identify high-potential team members for advancement")
print(f"      - Implement career development pathways")
print(f"      - Provide leadership training for future supervisors")

print(f"   2. TEAM CULTURE:")
print(f"      - Build collaborative team environment")
print(f"      - Implement recognition and reward programs")
print(f"      - Foster healthy competition and team spirit")

# ROI Analysis
potential_improvement = (total_target - total_sales)
current_efficiency = (total_sales / total_target) * 100

print(f"\n💰 BUSINESS IMPACT ANALYSIS:")
print(f"   Current Team Efficiency: {current_efficiency:.1f}%")
print(f"   Improvement Potential: {potential_improvement:,} units ({(potential_improvement/total_sales)*100:.1f}% increase)")
print(f"   If team reaches 80% average: +{(total_target * 0.8 - total_sales):.0f} units")
print(f"   If team reaches 100% average: +{potential_improvement:.0f} units")

print(f"\n📊 SUCCESS METRICS TO TRACK:")
print(f"   - Weekly individual achievement rates")
print(f"   - Monthly team performance trends")
print(f"   - Quarterly zero-sales reduction")
print(f"   - Semi-annual team efficiency improvement")

print(f"\n" + "=" * 70)
print("END OF JAKARTA TEAM ANALYSIS")
print("=" * 70)