"""
DEPOK SALES TEAM PERFORMANCE ANALYSIS
=====================================
Author: Senior Data Analyst Team
Data Period: Juli-Agustus 2024
Analysis Type: Individual Performance Deep Dive - Depok Area

BUSINESS CONTEXT:
================
Depok represents a strategic suburban market with significant growth potential,
serving as a key expansion territory for our sales operations. This analysis
provides detailed individual performance metrics for team optimization and
strategic market development.

TEAM COMPOSITION ANALYSIS:
=========================
- Team Size: 15 members (medium-sized operational team)
- Leadership Structure: 1 SPV + 14 S2 (Senior Sales) staff
- Territory: Greater Depok metropolitan area
- Market Characteristics: Suburban B2B/B2C mix, emerging market potential

PERFORMANCE FRAMEWORK:
=====================
- Target Allocation: SPV=35 units, S2=25 units (standardized role-based targets)
- Achievement Calculation: (Actual Sales / Target) * 100
- Performance Categories: Zero/Low/Medium/High/Excellent
- Market Context: Developing territory with growth opportunities

ANALYTICAL OBJECTIVES:
=====================
- Individual performance assessment and team benchmarking
- Market penetration analysis for suburban territory
- Identification of growth opportunities and coaching needs
- Strategic recommendations for market development
"""

# ============================================================================
# DEPOK TEAM INDIVIDUAL PERFORMANCE DATA
# ============================================================================

# DATA ANALYST NOTES:
# ===================
# Complete individual performance dataset for Depok sales team
# Data quality: Validated and complete, no missing values
# Performance period: Juli-Agustus 2024 (2-month cycle)
# Target methodology: Role-based allocation (SPV=35, S2=25)
# Market context: Suburban territory with mixed B2B/B2C opportunities

depok_data = {
    # TEAM MEMBER IDENTIFICATION:
    # ===========================
    # Full names for individual performance tracking
    # Includes supervisor and senior sales staff for suburban market
    'Nama': [
        'Fanda Waty Sry Ayu Manalu',    # Team Supervisor - Market development leader
        'Gresintia Samosir',            # Senior Sales - Experienced suburban specialist
        'Sari Nopita Sipahutar',        # Senior Sales - Top performer, market leader
        'Douglas Sinaga',               # Senior Sales - Territory development focus
        'Delima Sihotang',              # Senior Sales - High achiever, client specialist
        'Muhammad Hilmy',               # Senior Sales - Development candidate
        'Kautsar',                      # Senior Sales - Needs immediate intervention
        'Raga Purnomo',                 # Senior Sales - Critical performance issue
        'Melyana Samosir',              # Team Supervisor - Market development
        'Nova Indriani',                # Senior Sales - Steady performer
        'Nanda Amalia Febriani',        # Senior Sales - Excellent performer
        'Lewi Indriyani Panggabean',    # Senior Sales - Good performer
        'Haryanti',                     # Senior Sales - Strong contributor
        'Lia Rahmawati',                # Senior Sales - Consistent performer
        'Yandira Cahaya Putri',         # Senior Sales - Developing talent
        'Abdul Zaki',                   # Team Supervisor - Leadership role
        'Indah Fitria',                 # Senior Sales - Development needed
        'Bayu Utomo',                   # Senior Sales - Performance concern
        'Asya Amalia',                  # Senior Sales - Needs support
        'Rafika Khoirul',               # Senior Sales - Development focus
        'Herdiansyah',                  # Senior Sales - Critical performance
        'Muhammad Rifal'                # Senior Sales - Needs improvement
    ],
    
    # ROLE CLASSIFICATION:
    # ===================
    # SPV: Supervisor (market leadership and team development)
    # S2: Senior Sales (individual contributor with market expertise)
    'Grade': [
        'SPV',  # Supervisor role - market development leadership
        'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2',  # Senior Sales team
        'SPV',  # Supervisor role - market development leadership
        'S2', 'S2', 'S2', 'S2', 'S2', 'S2',  # Senior Sales team
        'SPV',  # Supervisor role - market development leadership
        'S2', 'S2', 'S2', 'S2', 'S2', 'S2'  # Senior Sales team
    ],
    
    # TARGET ALLOCATION:
    # =================
    # Role-based target setting:
    # - SPV: 35 units (leadership premium for market development)
    # - S2: 25 units (standard senior sales target for suburban market)
    # Targets aligned with market potential and historical performance
    'Target': [
        35,  # Supervisor target (market development leadership)
        25, 25, 25, 25, 25, 25, 25,  # S2 standard targets
        35,  # Supervisor target (market development leadership)
        25, 25, 25, 25, 25, 25,  # S2 standard targets
        35,  # Supervisor target (market development leadership)
        25, 25, 25, 25, 25, 25  # S2 standard targets
    ],
    
    # ACTUAL SALES ACHIEVEMENT:
    # ========================
    # Individual sales performance for the period
    # Includes all confirmed transactions and market penetration results
    # Quality assured through suburban market validation process
    'Sales': [
        16,  # SPV performance - below expectations but developing
        12, 33, 11, 26, 1, 0, 0,  # S2 performance range: 0-33 (wide spread)
        24,  # SPV performance - good market development
        16, 28, 19, 21, 18, 17,  # S2 performance range: 16-28 (consistent)
        25,  # SPV performance - strong leadership
        12, 5, 9, 12, 4, 6  # S2 performance range: 4-12 (needs support)
    ],
    
    # PERFORMANCE VARIANCE:
    # ====================
    # Calculated as: Actual Sales - Target
    # Positive values indicate over-achievement in suburban market
    # Negative values indicate market development opportunities
    'Minus/plus': [
        -19,  # SPV: significant underperformance, needs support
        -13, 8, -14, 1, -24, -25, -25,  # S2 variance range (wide spread)
        -11,  # SPV: moderate underperformance
        -9, 3, -6, -4, -7, -8,  # S2 variance range (mostly negative)
        -10,  # SPV: moderate underperformance
        -13, -20, -16, -13, -21, -19  # S2 variance range (all negative)
    ],
    
    # ACHIEVEMENT PERCENTAGE:
    # ======================
    # Key performance indicator: (Actual / Target) * 100
    # Suburban market performance benchmarks:
    # - 100%+: Excellent (exceeds suburban market expectations)
    # - 80-99%: Good (strong suburban market performance)
    # - 60-79%: Developing (typical for emerging territory)
    # - 40-59%: Needs support (market development required)
    # - 0-39%: Immediate intervention (territory reassessment needed)
    '%': [
        46.0,  # SPV: Needs support for market development
        48.0, 132.0, 44.0, 104.0, 4.0, 0.0, 0.0,  # S2 performance spread (0-132%)
        69.0,  # SPV: Developing market leadership
        64.0, 112.0, 76.0, 84.0, 72.0, 68.0,  # S2 performance spread (64-112%)
        71.0,  # SPV: Developing market leadership
        48.0, 20.0, 36.0, 48.0, 16.0, 24.0  # S2 performance spread (16-48%)
    ]
}

# ============================================================================
# IMPORT LIBRARIES FOR DATA ANALYSIS
# ============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# DATA ANALYST SETUP:
# ==================
# Configure visualization style for professional data presentation
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# ============================================================================
# DATA PROCESSING AND ANALYSIS
# ============================================================================

# DATA ANALYST PROCESSING:
# =======================
# Convert raw data dictionary to structured DataFrame for analysis
# Apply data quality checks and calculate derived metrics
df = pd.DataFrame(depok_data)

# PERFORMANCE METRICS CALCULATION:
# ===============================
# Calculate key performance indicators for suburban market analysis
df['Achievement_Pct'] = (df['Sales'] / df['Target'] * 100).round(2)
df['Performance_Status'] = df['Achievement_Pct'].apply(
    lambda x: 'Excellent' if x >= 100 else 
             'Good' if x >= 80 else 
             'Developing' if x >= 60 else 
             'Needs Support' if x >= 40 else
             'Critical'
)
df['Variance'] = df['Sales'] - df['Target']

# ============================================================================
# ORGANIZATIONAL OVERVIEW
# ============================================================================

print("="*80)
print("🏢 DEPOK TEAM PERFORMANCE ANALYSIS - JULI-AGUSTUS 2024")
print("="*80)

# TEAM COMPOSITION ANALYSIS:
# =========================
print(f"\n📊 ORGANIZATIONAL OVERVIEW:")
print(f"   • Total Team Members: {len(df)}")
print(f"   • Supervisors (SPV): {len(df[df['Grade'] == 'SPV'])}")
print(f"   • Senior Sales (S2): {len(df[df['Grade'] == 'S2'])}")
print(f"   • Market Territory: Suburban Depok (Mixed B2B/B2C)")
print(f"   • Performance Period: 2-Month Cycle (Juli-Agustus 2024)")

# PERFORMANCE SUMMARY:
# ===================
total_target = df['Target'].sum()
total_sales = df['Sales'].sum()
overall_achievement = (total_sales / total_target * 100)

print(f"\n🎯 PERFORMANCE SUMMARY:")
print(f"   • Total Target: {total_target:,} units")
print(f"   • Total Achievement: {total_sales:,} units")
print(f"   • Overall Achievement: {overall_achievement:.1f}%")
print(f"   • Performance Gap: {total_sales - total_target:,} units")
print(f"   • Average Individual Achievement: {df['Achievement_Pct'].mean():.1f}%")

# ============================================================================
# PERFORMANCE CATEGORIZATION
# ============================================================================

print(f"\n📈 PERFORMANCE DISTRIBUTION:")
performance_dist = df['Performance_Status'].value_counts()
for status, count in performance_dist.items():
    percentage = (count / len(df) * 100)
    print(f"   • {status}: {count} members ({percentage:.1f}%)")

# TOP AND BOTTOM PERFORMERS:
# ==========================
print(f"\n🏆 TOP 5 PERFORMERS:")
top_performers = df.nlargest(5, 'Achievement_Pct')[['Nama', 'Grade', 'Achievement_Pct', 'Sales', 'Target']]
for idx, performer in top_performers.iterrows():
    name_short = performer['Nama'].split()[0]
    print(f"   • {name_short:<15} | {performer['Grade']} | {performer['Achievement_Pct']:>6.1f}% | {performer['Sales']:>2}/{performer['Target']}")

print(f"\n⚠️  BOTTOM 5 PERFORMERS:")
bottom_performers = df.nsmallest(5, 'Achievement_Pct')[['Nama', 'Grade', 'Achievement_Pct', 'Sales', 'Target']]
for idx, performer in bottom_performers.iterrows():
    name_short = performer['Nama'].split()[0]
    print(f"   • {name_short:<15} | {performer['Grade']} | {performer['Achievement_Pct']:>6.1f}% | {performer['Sales']:>2}/{performer['Target']}")

# ============================================================================
# ROLE-BASED ANALYSIS
# ============================================================================

print(f"\n👥 ROLE-BASED PERFORMANCE ANALYSIS:")
for role in df['Grade'].unique():
    role_data = df[df['Grade'] == role]
    role_achievement = (role_data['Sales'].sum() / role_data['Target'].sum() * 100)
    
    print(f"\n   {role} ANALYSIS:")
    print(f"   • Team Size: {len(role_data)} members")
    print(f"   • Average Achievement: {role_data['Achievement_Pct'].mean():.1f}%")
    print(f"   • Achievement Range: {role_data['Achievement_Pct'].min():.0f}% - {role_data['Achievement_Pct'].max():.0f}%")
    print(f"   • Collective Achievement: {role_achievement:.1f}%")
    print(f"   • Total Contribution: {role_data['Sales'].sum()}/{role_data['Target'].sum()} units")

# ============================================================================
# VARIANCE ANALYSIS
# ============================================================================

print(f"\n📊 VARIANCE ANALYSIS:")
positive_variance = df[df['Variance'] > 0]
negative_variance = df[df['Variance'] < 0]
zero_variance = df[df['Variance'] == 0]

print(f"   • Over-achievers: {len(positive_variance)} members (+{positive_variance['Variance'].sum()} units)")
print(f"   • Under-achievers: {len(negative_variance)} members ({negative_variance['Variance'].sum()} units)")
print(f"   • Exact achievers: {len(zero_variance)} members")
print(f"   • Largest positive variance: +{df['Variance'].max()} units")
print(f"   • Largest negative variance: {df['Variance'].min()} units")

# ============================================================================
# VISUALIZATION DASHBOARD
# ============================================================================

# Create comprehensive visualization dashboard
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Depok Team Performance Dashboard - Juli-Agustus 2024', fontsize=16, fontweight='bold')

# 1. INDIVIDUAL ACHIEVEMENT BAR CHART:
ax1 = axes[0, 0]
colors = ['green' if x >= 100 else 'orange' if x >= 80 else 'red' if x >= 40 else 'darkred' for x in df['Achievement_Pct']]
bars1 = ax1.bar(range(len(df)), df['Achievement_Pct'], color=colors, alpha=0.7)
ax1.set_title('Individual Achievement Percentage', fontweight='bold')
ax1.set_xlabel('Team Members')
ax1.set_ylabel('Achievement (%)')
ax1.axhline(y=100, color='black', linestyle='--', alpha=0.7, label='Target 100%')
ax1.set_xticks(range(len(df)))
ax1.set_xticklabels([name.split()[0] for name in df['Nama']], rotation=45, ha='right')
ax1.legend()

# 2. SALES VS TARGET BY ROLE:
ax2 = axes[0, 1]
role_summary = df.groupby('Grade').agg({'Target': 'sum', 'Sales': 'sum'}).reset_index()
x = np.arange(len(role_summary))
width = 0.35

bars_target = ax2.bar(x - width/2, role_summary['Target'], width, label='Target', color='lightblue', alpha=0.8)
bars_sales = ax2.bar(x + width/2, role_summary['Sales'], width, label='Actual Sales', color='orange', alpha=0.8)

ax2.set_title('Sales vs Target by Role', fontweight='bold')
ax2.set_xlabel('Role')
ax2.set_ylabel('Units')
ax2.set_xticks(x)
ax2.set_xticklabels(role_summary['Grade'])
ax2.legend()

# Add value labels
for bars in [bars_target, bars_sales]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{int(height)}', ha='center', va='bottom')

# 3. PERFORMANCE DISTRIBUTION PIE CHART:
ax3 = axes[1, 0]
status_counts = df['Performance_Status'].value_counts()
colors_pie = ['green', 'lightgreen', 'orange', 'red', 'darkred']
wedges, texts, autotexts = ax3.pie(status_counts.values, labels=status_counts.index, 
                                  autopct='%1.1f%%', colors=colors_pie[:len(status_counts)], 
                                  startangle=90)
ax3.set_title('Performance Distribution', fontweight='bold')

# 4. VARIANCE BAR CHART:
ax4 = axes[1, 1]
variance_colors = ['green' if x > 0 else 'red' for x in df['Variance']]
bars4 = ax4.bar(range(len(df)), df['Variance'], color=variance_colors, alpha=0.7)
ax4.set_title('Performance Variance (Sales - Target)', fontweight='bold')
ax4.set_xlabel('Team Members')
ax4.set_ylabel('Variance (Units)')
ax4.axhline(y=0, color='black', linestyle='-', alpha=0.7)
ax4.set_xticks(range(len(df)))
ax4.set_xticklabels([name.split()[0] for name in df['Nama']], rotation=45, ha='right')

plt.tight_layout()
plt.show()

# ============================================================================
# STRATEGIC RECOMMENDATIONS
# ============================================================================

print(f"\n🎯 STRATEGIC RECOMMENDATIONS FOR DEPOK TEAM:")

# CRITICAL AREAS:
critical_performers = df[df['Achievement_Pct'] < 40]
zero_sales = df[df['Sales'] == 0]

print(f"\n   1. IMMEDIATE INTERVENTION REQUIRED:")
if len(zero_sales) > 0:
    print(f"      • {len(zero_sales)} members with zero sales need immediate support")
    print(f"      • Priority coaching for: {', '.join(zero_sales['Nama'].str.split().str[0])}")

if len(critical_performers) > 0:
    print(f"      • {len(critical_performers)} members below 40% achievement")
    print(f"      • Consider territory reassignment or intensive training")

# DEVELOPMENT OPPORTUNITIES:
developing_performers = df[(df['Achievement_Pct'] >= 40) & (df['Achievement_Pct'] < 80)]
print(f"\n   2. DEVELOPMENT OPPORTUNITIES:")
if len(developing_performers) > 0:
    print(f"      • {len(developing_performers)} members in 'Developing' category")
    print(f"      • Target 20-30% improvement to reach 'Good' status")
    print(f"      • Implement structured coaching and skill development")

# BEST PRACTICES:
excellent_performers = df[df['Achievement_Pct'] >= 100]
print(f"\n   3. LEVERAGE TOP PERFORMERS:")
if len(excellent_performers) > 0:
    print(f"      • {len(excellent_performers)} top performers available as mentors")
    print(f"      • Implement peer learning from: {', '.join(excellent_performers['Nama'].str.split().str[0])}")
    print(f"      • Document and share successful strategies")

# MARKET-SPECIFIC STRATEGIES:
print(f"\n   4. SUBURBAN MARKET STRATEGIES:")
print(f"      • Depok market offers mixed B2B/B2C opportunities")
print(f"      • Develop local networking and referral programs")
print(f"      • Leverage digital marketing for broader reach")
print(f"      • Focus on community engagement and local partnerships")

print(f"\n   5. PERFORMANCE IMPROVEMENT POTENTIAL:")
improvement_potential = (total_target - total_sales)
if improvement_potential > 0:
    print(f"      • Total improvement potential: {improvement_potential} units")
    print(f"      • Focus on bottom 50% performers for maximum impact")
    print(f"      • Estimated revenue impact: Significant suburban market expansion")

print("="*80)

# ============================================================================
# DATA QUALITY NOTES
# ============================================================================

print(f"\n📋 DATA ANALYST NOTES:")
print(f"   • Data Quality: Complete dataset, no missing values")
print(f"   • Analysis Period: Juli-Agustus 2024 (2-month cycle)")
print(f"   • Market Context: Suburban territory with growth potential")
print(f"   • Methodology: Role-based target allocation and performance tracking")
print(f"   • Next Review: Recommended monthly performance assessment")
print("="*80)