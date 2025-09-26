import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# Set style
plt.style.use('default')
sns.set_palette("Set2")

# Data sales team Purwakarta
sales_data = {
    'NAMA_DS': ['GANI MAULANA', 'RONI CAHYANI', 'FERDINAND EKO DEWA', 
                'AGUNG SURYANINGRAT', 'JONATHAN RIRIHENA', 'HERDIANSYAH FAUZAN'],
    'GRADE': ['DS', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'TARGET': [25, 25, 25, 25, 25, 25],
    'SALES': [2, 8, 4, 5, 2, 5],
    'MINUS_PLUS': [-23, -17, -21, -20, -23, -20],
    'PERSENTASE': [8, 32, 16, 20, 8, 20]
}

df = pd.DataFrame(sales_data)

# Calculate additional metrics
df['ACHIEVEMENT_RATE'] = (df['SALES'] / df['TARGET']) * 100
df['SHORTFALL'] = df['TARGET'] - df['SALES']

# Sort by achievement rate (lowest to highest)
df = df.sort_values('ACHIEVEMENT_RATE', ascending=True)

# Calculate average achievement by role
role_avg = df.groupby('GRADE')['ACHIEVEMENT_RATE'].mean().reset_index()
role_avg.columns = ['GRADE', 'AVG_ACHIEVEMENT']

# Display the dataframe
print("SALES PERFORMANCE DATA - PURWAKARTA AREA")
print("21 Juli - 20 Agustus")
print("="*65)
print(df[['NAMA_DS', 'GRADE', 'TARGET', 'SALES', 'ACHIEVEMENT_RATE']].to_string(index=False))
print("="*65)
print(f"TOTAL TARGET: {df['TARGET'].sum()}")
print(f"TOTAL SALES: {df['SALES'].sum()}")
print(f"TOTAL SHORTFALL: {df['SHORTFALL'].sum()}")
print(f"OVERALL ACHIEVEMENT RATE: {(df['SALES'].sum()/df['TARGET'].sum())*100:.1f}%")

# Create visualizations
fig = plt.figure(figsize=(20, 16))
fig.suptitle('ANALISIS KINERJA SALES - AREA PURWAKARTA\n21 Juli - 20 Agustus', 
             fontsize=18, fontweight='bold', y=0.98)

# 1. Pencapaian per Individu (Horizontal Bar Chart)
ax1 = plt.subplot(2, 2, 1)
colors = ['#2EC4B6' for _ in df['GRADE']]  # All DS

# Create horizontal bars
bars = ax1.barh(df['NAMA_DS'], df['ACHIEVEMENT_RATE'], color=colors, alpha=0.8)
ax1.set_title('Pencapaian per Individu', fontsize=14)
ax1.set_xlabel('Tingkat Pencapaian (%)', fontsize=12)
ax1.set_ylabel('Nama Sales', fontsize=12)
ax1.axvline(x=100, color='red', linestyle='--', alpha=0.7, label='Target 100%')
ax1.axvline(x=80, color='orange', linestyle='--', alpha=0.5, label='Minimum 80%')
ax1.axvline(x=50, color='yellow', linestyle='--', alpha=0.3, label='Warning 50%')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='x')
ax1.set_xlim(0, 100)

# Add value labels on bars
for bar in bars:
    width = bar.get_width()
    ax1.text(width + 2, bar.get_y() + bar.get_height()/2,
             f'{width:.0f}%', ha='left', va='center', fontsize=10)

# 2. Rata-rata Pencapaian berdasarkan Role (Grouped Bar Chart)
ax2 = plt.subplot(2, 2, 2)
roles = role_avg['GRADE']
avg_values = role_avg['AVG_ACHIEVEMENT']

colors_role = ['#2EC4B6' for _ in roles]  # All DS
bars2 = ax2.bar(roles, avg_values, color=colors_role, alpha=0.8)
ax2.set_title('Rata-rata Pencapaian berdasarkan Role', fontsize=14)
ax2.set_ylabel('Rata-rata Pencapaian (%)', fontsize=12)
ax2.set_xlabel('Role', fontsize=12)
ax2.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='Target 100%')
ax2.axhline(y=50, color='orange', linestyle='--', alpha=0.5, label='Warning 50%')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Add value labels on bars
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
             f'{height:.1f}%', ha='center', va='bottom')

# 3. Distribusi Kinerja Tim
ax3 = plt.subplot(2, 2, 3)

# Create performance categories
bins = [0, 10, 20, 30, 40, 50, 100]
labels = ['0-10%', '11-20%', '21-30%', '31-40%', '41-50%', '>50%']
df['PERFORMANCE_CAT'] = pd.cut(df['ACHIEVEMENT_RATE'], bins=bins, labels=labels, right=False)

# Count number of people in each category
performance_dist = df['PERFORMANCE_CAT'].value_counts().sort_index()

# Create bar chart for performance distribution
bars3 = ax3.bar(performance_dist.index, performance_dist.values, 
                color=['#FF6B6B', '#FF9F1C', '#F9DC5C', '#A8D5BA', '#4ECDC4', '#2EC4B6'], 
                alpha=0.8)

ax3.set_title('Distribusi Kinerja Tim', fontsize=14)
ax3.set_xlabel('Kategori Pencapaian', fontsize=12)
ax3.set_ylabel('Jumlah Sales', fontsize=12)
ax3.grid(True, alpha=0.3)

# Add value labels on bars
for bar in bars3:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.05,
             f'{int(height)}', ha='center', va='bottom')

# Add individual names to the chart
y_offset = 0.1
for i, row in df.iterrows():
    cat_index = list(performance_dist.index).index(str(row['PERFORMANCE_CAT']))
    name_parts = row['NAMA_DS'].split()
    short_name = name_parts[0] if len(name_parts) > 0 else row['NAMA_DS']
    ax3.text(cat_index, performance_dist.values[cat_index] + y_offset, 
             short_name, 
             ha='center', va='bottom', fontsize=9)
    y_offset += 0.1

# 4. Perbandingan Target vs Actual Sales per Role (Grouped Bar Chart)
ax4 = plt.subplot(2, 2, 4)

# Prepare data for grouped bar chart
role_data = df.groupby('GRADE').agg({'TARGET': 'sum', 'SALES': 'sum'}).reset_index()

x = np.arange(len(role_data['GRADE']))
width = 0.35

bars4a = ax4.bar(x - width/2, role_data['TARGET'], width, 
                label='Target', alpha=0.7, color='#FF6B6B')
bars4b = ax4.bar(x + width/2, role_data['SALES'], width, 
                label='Actual Sales', alpha=0.7, color='#4ECDC4')

ax4.set_title('Perbandingan Target vs Actual Sales per Role', fontsize=14)
ax4.set_ylabel('Jumlah Sales', fontsize=12)
ax4.set_xlabel('Role', fontsize=12)
ax4.set_xticks(x)
ax4.set_xticklabels(role_data['GRADE'])
ax4.legend()
ax4.grid(True, alpha=0.3)

# Add value labels on bars
for bars in [bars4a, bars4b]:
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom')

plt.tight_layout()
plt.subplots_adjust(top=0.93)
plt.show()

# Detailed Performance Analysis
print("\n" + "="*65)
print("ANALISIS DETAIL KINERJA")
print("="*65)

# Individual performance analysis
print("\n1. ANALISIS PER INDIVIDU:")
print("-" * 45)
for index, row in df.iterrows():
    if row['ACHIEVEMENT_RATE'] < 10:
        status = "SANGAT KRITIS"
    elif row['ACHIEVEMENT_RATE'] < 20:
        status = "KRITIS"
    elif row['ACHIEVEMENT_RATE'] < 50:
        status = "SANGAT BURUK"
    else:
        status = "BURUK"
    
    name_parts = row['NAMA_DS'].split()
    short_name = name_parts[0] + " " + (name_parts[1][0] + "." if len(name_parts) > 1 else "")
    
    print(f"{short_name.ljust(18)} ({row['GRADE']}): {row['ACHIEVEMENT_RATE']:6.1f}% - {status}")

# Performance distribution analysis
print("\n2. DISTRIBUSI KINERJA TIM:")
print("-" * 45)
for cat in labels:
    count = performance_dist.get(cat, 0)
    print(f"{cat}: {count} orang")

# Role-based analysis
print("\n3. ANALISIS BERDASARKAN ROLE:")
print("-" * 45)
for index, row in role_avg.iterrows():
    print(f"{row['GRADE']}: Rata-rata pencapaian {row['AVG_ACHIEVEMENT']:.1f}%")

# Overall analysis
print("\n4. ANALISIS KESELURUHAN:")
print("-" * 45)
print(f"Total Pencapaian: {df['SALES'].sum()}/{df['TARGET'].sum()} ({df['SALES'].sum()/df['TARGET'].sum()*100:.1f}%)")
print(f"Total Shortfall: {df['SHORTFALL'].sum()} unit")
print("Status: SANGAT KRITIS - Perlu intervensi segera!")

print("\n5. REKOMENDASI:")
print("-" * 45)
print("• INTERVENSI DARURAT untuk seluruh tim")
print("• Coaching intensif harian untuk semua DS")
print("• Evaluasi ulang strategi penjualan area Purwakarta")
print("• Review target yang mungkin tidak realistis")
print("• Monitoring ketat progress harian")
print("• Pertimbangan restrukturisasi tim")
print("• Pelatihan ulang teknik selling dasar")