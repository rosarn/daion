import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# Set style
plt.style.use('default')
sns.set_palette("Set2")

# Data sales team Badung
sales_data = {
    'NAMA_DS': ['GEDE OKA CAHYADI PRATAMA', 'NI LUH PUTU ADINDA SUCI LESTARI', 'NI LUH PUTU ASTITI DEWI',
                'MALIANA', 'I MADE CANDRA PRANATA', 'I KADEK ALDI ARTANA', 
                'I GUSTI NGURAH AGUNG MARTA WEDANA PUTRA', 'IRVAN RYNALDI', 'YUDA PRATAMA',
                'AGUS JUNIANTO', 'MUHAMMAD CAHYO SAPUTRO', 'PUTU AGUS DARMAWAN',
                'AHMAD REHAN DIKI PRAYOGA', 'SAFRIZAL HUTAGALUNG', 'EBEN HAZAER ZAI',
                'CERELINA TIO FANI', 'BAYU FERNANDO', 'JORDI UMBU LELE',
                'PANGGAH LESTYO ARDIAN', 'M.DWIKI DHARMAWAN', 'HIKMA HAQIQI',
                'BINTANG SURIADI SIBARANI'],
    'GRADE': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS',
              'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS'],
    'TARGET': [35, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 25, 25],
    'SALES': [0, 31, 84, 19, 9, 2, 2, 0, 64, 25, 18, 21, 2, 0, 28, 51, 7, 29, 7, 6, 20, 1],
    'MINUS_PLUS': [-35, 6, 59, -6, -16, -23, -23, -25, 39, 0, -7, -4, -23, -35, 3, 26, -18, 4, -18, -19, -5, -24],
    'PERSENTASE': [0, 124, 336, 76, 36, 8, 8, 0, 256, 100, 72, 84, 8, 0, 112, 204, 28, 116, 28, 24, 80, 4]
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
print("SALES PERFORMANCE DATA - BADUNG AREA")
print("21 Juli - 20 Agustus")
print("="*80)
print(df[['NAMA_DS', 'GRADE', 'TARGET', 'SALES', 'ACHIEVEMENT_RATE']].to_string(index=False))
print("="*80)
print(f"TOTAL TARGET: {df['TARGET'].sum()}")
print(f"TOTAL SALES: {df['SALES'].sum()}")
print(f"TOTAL SHORTFALL: {df['SHORTFALL'].sum()}")
print(f"OVERALL ACHIEVEMENT RATE: {(df['SALES'].sum()/df['TARGET'].sum())*100:.1f}%")

# Create visualizations
fig = plt.figure(figsize=(20, 16))
fig.suptitle('ANALISIS KINERJA SALES - AREA BADUNG\n21 Juli - 20 Agustus', 
             fontsize=18, fontweight='bold', y=0.98)

# 1. Pencapaian per Individu (Horizontal Bar Chart)
ax1 = plt.subplot(2, 2, 1)
colors = ['#FF9F1C' if grade == 'SPV' else '#2EC4B6' for grade in df['GRADE']]

# Create horizontal bars
bars = ax1.barh(df['NAMA_DS'], df['ACHIEVEMENT_RATE'], color=colors, alpha=0.8)
ax1.set_title('Pencapaian per Individu', fontsize=14)
ax1.set_xlabel('Tingkat Pencapaian (%)', fontsize=12)
ax1.set_ylabel('Nama Sales', fontsize=12)
ax1.axvline(x=100, color='red', linestyle='--', alpha=0.7, label='Target 100%')
ax1.axvline(x=80, color='orange', linestyle='--', alpha=0.5, label='Minimum 80%')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='x')

# Add value labels on bars
for bar in bars:
    width = bar.get_width()
    ax1.text(width + 10, bar.get_y() + bar.get_height()/2,
             f'{width:.0f}%', ha='left', va='center', fontsize=7)

# 2. Rata-rata Pencapaian berdasarkan Role (Grouped Bar Chart)
ax2 = plt.subplot(2, 2, 2)
roles = role_avg['GRADE']
avg_values = role_avg['AVG_ACHIEVEMENT']

colors_role = ['#FF9F1C' if role == 'SPV' else '#2EC4B6' for role in roles]
bars2 = ax2.bar(roles, avg_values, color=colors_role, alpha=0.8)
ax2.set_title('Rata-rata Pencapaian berdasarkan Role', fontsize=14)
ax2.set_ylabel('Rata-rata Pencapaian (%)', fontsize=12)
ax2.set_xlabel('Role', fontsize=12)
ax2.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='Target 100%')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Add value labels on bars
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'{height:.1f}%', ha='center', va='bottom')

# 3. Distribusi Kinerja Tim
ax3 = plt.subplot(2, 2, 3)

# Create performance categories
bins = [0, 20, 50, 80, 100, 200, 400]
labels = ['0-20%', '21-50%', '51-80%', '81-100%', '101-200%', '>200%']
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
             ha='center', va='bottom', fontsize=6)
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
        ax4.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{int(height)}', ha='center', va='bottom')

plt.tight_layout()
plt.subplots_adjust(top=0.93)
plt.show()

# Detailed Performance Analysis
print("\n" + "="*80)
print("ANALISIS DETAIL KINERJA")
print("="*80)

# Individual performance analysis
print("\n1. ANALISIS PER INDIVIDU:")
print("-" * 60)
for index, row in df.iterrows():
    if row['ACHIEVEMENT_RATE'] == 0:
        status = "KRITIS (0%)"
    elif row['ACHIEVEMENT_RATE'] < 20:
        status = "SANGAT BURUK"
    elif row['ACHIEVEMENT_RATE'] < 50:
        status = "BURUK"
    elif row['ACHIEVEMENT_RATE'] < 80:
        status = "PERLU PERBAIKAN"
    elif row['ACHIEVEMENT_RATE'] < 100:
        status = "BAIK"
    elif row['ACHIEVEMENT_RATE'] < 200:
        status = "EXCELLENT"
    else:
        status = "OUTSTANDING"
    
    name_parts = row['NAMA_DS'].split()
    short_name = name_parts[0] + " " + (name_parts[1][0] + "." if len(name_parts) > 1 else "")
    
    print(f"{short_name.ljust(15)} ({row['GRADE']}): {row['ACHIEVEMENT_RATE']:6.1f}% - {status}")

# Performance distribution analysis
print("\n2. DISTRIBUSI KINERJA TIM:")
print("-" * 60)
for cat in labels:
    count = performance_dist.get(cat, 0)
    print(f"{cat}: {count} orang")

# Role-based analysis
print("\n3. ANALISIS BERDASARKAN ROLE:")
print("-" * 60)
for index, row in role_avg.iterrows():
    print(f"{row['GRADE']}: Rata-rata pencapaian {row['AVG_ACHIEVEMENT']:.1f}%")

# Overall analysis
print("\n4. ANALISIS KESELURUHAN:")
print("-" * 60)
print(f"Total Pencapaian: {df['SALES'].sum()}/{df['TARGET'].sum()} ({df['SALES'].sum()/df['TARGET'].sum()*100:.1f}%)")
print(f"Total Shortfall: {df['SHORTFALL'].sum()} unit")
print("Status: BAIK - Beberapa outstanding performers, tapi ada underperformer ekstrem")

print("\n5. REKOMENDASI:")
print("-" * 60)
print("• Fokus pada 3 SPV dan 5 DS dengan pencapaian di bawah 30%")
print("• Coaching intensif untuk 7 DS dengan pencapaian rendah (4-36%)")
print("• Replikasi best practices dari outstanding performers (NI LUH ASTITI 336%, YUDA 256%)")
print("• Evaluasi target untuk SPV yang mungkin tidak realistis")
print("• Program mentoring dari top performers ke underperformers")
print("• Reward untuk 6 DS dengan pencapaian excellent dan outstanding")