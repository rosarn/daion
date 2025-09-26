import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data untuk Tegal
data_tegal = {
    'No': range(1, 11),
    'Nama DS': [
        'PRASTIKA WIGATINING PANGESTUTI', 'HAMZAH FAHMI', 'LATHIF MUTTAQIN', 
        'HIJRAH SABILA', 'KHADZIQUL HUMAM MUNFI', 'FAUZAN MAULANA ADI', 
        'MITA LESTARI', 'Eko Krismanto', 'MOHAMAD IMRON, AMDS', 'MOHAMMAD KAMAL BUSTAMI'
    ],
    'Grade': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'Target': [35, 25, 25, 25, 25, 25, 25, 25, 25, 25],
    'Sales': [0, 36, 41, 35, 21, 31, 14, 22, 3, 3],
    '%': [0, 144, 164, 140, 84, 124, 56, 88, 12, 12]
}

# Membuat DataFrame
df = pd.DataFrame(data_tegal)

# Menambahkan kolom performa
df['Status'] = df['%'].apply(lambda x: 'Above Target' if x >= 100 else 'Below Target')

# 1. Ringkasan Kinerja Keseluruhan
total_target = df['Target'].sum()
total_sales = df['Sales'].sum()
percentage_achieved = (total_sales / total_target) * 100

print("=== RINGKASAN KINERJA TEGAL ===")
print(f"Regional Head: Susanto")
print(f"Sales Manager: Dede Regdimas Pangemanan")
print(f"Periode: 21 Juli - 20 Agustus")
print(f"Total Target: {total_target}")
print(f"Total Sales: {total_sales}")
print(f"Pencapaian: {percentage_achieved:.1f}%")
print(f"Selisih: {total_sales - total_target}")

# 2. Visualisasi Data yang Jelas
plt.style.use('default')
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Analisis Kinerja Sales Tegal (21 Juli - 20 Agustus)', fontsize=16, fontweight='bold')

# Warna untuk visualisasi
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# GRAFIK 1: Pencapaian per Salesperson dengan Nama Jelas
bars = axes[0, 0].bar(range(len(df)), df['%'], 
                     color=np.where(df['%'] >= 100, 'green', 
                                  np.where(df['%'] == 0, 'red', '#1f77b4')), 
                     alpha=0.7)
axes[0, 0].axhline(y=100, color='red', linestyle='--', alpha=0.7, linewidth=2)
axes[0, 0].set_title('PENCAPAIAN PER SALESPERSON', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Salesperson', fontsize=12)
axes[0, 0].set_ylabel('Pencapaian (%)', fontsize=12)
axes[0, 0].set_xticks(range(len(df)))
axes[0, 0].set_xticklabels([name.split()[0] for name in df['Nama DS']], rotation=45, ha='right')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Menambahkan nilai pada setiap bar
for i, (bar, percentage, sales, target) in enumerate(zip(bars, df['%'], df['Sales'], df['Target'])):
    height = bar.get_height()
    axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 2,
                   f'{percentage}%\n({sales}/{target})', 
                   ha='center', va='bottom', fontsize=9, fontweight='bold')

# GRAFIK 2: Status Pencapaian Target
status_counts = df['Status'].value_counts()
wedges, texts, autotexts = axes[0, 1].pie(status_counts.values, labels=status_counts.index, 
                                         autopct='%1.1f%%', colors=['red', 'green'], 
                                         startangle=90, textprops={'fontsize': 12})
axes[0, 1].set_title('STATUS PENCAPAIAN TARGET', fontsize=14, fontweight='bold')

# Membuat autotext lebih bold
for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

# GRAFIK 3: Perbandingan Grade
grade_performance = df.groupby('Grade')['%'].mean()
bars_grade = axes[1, 0].bar(grade_performance.index, grade_performance.values, 
                           color=['orange', 'blue'], alpha=0.7)
axes[1, 0].set_title('RATA-RATA PENCAPAIAN BERDASARKAN GRADE', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('Rata-rata Pencapaian (%)', fontsize=12)
axes[1, 0].set_xlabel('Grade', fontsize=12)
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Menambahkan nilai pada setiap batang grade
for i, (bar, value) in enumerate(zip(bars_grade, grade_performance.values)):
    axes[1, 0].text(bar.get_x() + bar.get_width()/2, value + 2, f'{value:.1f}%', 
                   ha='center', va='bottom', fontsize=11, fontweight='bold')

# GRAFIK 4: Top dan Bottom Performers
performance_data = [
    df.nlargest(3, '%')['%'].mean(),  # Rata-rata top 3
    df.nsmallest(3, '%')['%'].mean()   # Rata-rata bottom 3
]
labels = ['Top 3 Performers', 'Bottom 3 Performers']
colors_perf = ['green', 'red']

bars_perf = axes[1, 1].bar(labels, performance_data, color=colors_perf, alpha=0.7)
axes[1, 1].set_title('PERBANDINGAN TOP vs BOTTOM PERFORMERS', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('Rata-rata Pencapaian (%)', fontsize=12)
axes[1, 1].grid(True, alpha=0.3, axis='y')

# Menambahkan nilai pada setiap batang
for i, (bar, value) in enumerate(zip(bars_perf, performance_data)):
    axes[1, 1].text(bar.get_x() + bar.get_width()/2, value + 2, f'{value:.1f}%', 
                   ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()

# 3. Analisis Statistik Detail
print("\n=== ANALISIS STATISTIK ===")
print(f"Rata-rata pencapaian: {df['%'].mean():.1f}%")
print(f"Median pencapaian: {df['%'].median():.1f}%")
print(f"Standar deviasi: {df['%'].std():.1f}%")
print(f"Jumlah yang mencapai target: {len(df[df['%'] >= 100])} dari {len(df)} salesperson")

# 4. Kategori Performa
def categorize_performance(pct):
    if pct >= 150:
        return "Excellent (≥150%)"
    elif pct >= 100:
        return "Good (100-149%)"
    elif pct >= 80:
        return "Fair (80-99%)"
    elif pct >= 50:
        return "Poor (50-79%)"
    else:
        return "Very Poor (<50%)"

df['Kategori'] = df['%'].apply(categorize_performance)
category_counts = df['Kategori'].value_counts()

print("\n=== KATEGORI PERFORMANCE ===")
for category, count in category_counts.items():
    percentage = (count / len(df)) * 100
    print(f"{category}: {count} salesperson ({percentage:.1f}%)")

# 5. Detail Performa per Salesperson
print("\n" + "="*60)
print("DETAIL PERFORMANCE PER SALESPERSON")
print("="*60)

print(f"\n{'No':<3} {'Nama Salesperson':<30} {'Grade':<5} {'Target':<6} {'Sales':<5} {'Pencapaian':<8} {'Status'}")
print("-" * 70)
for _, row in df.iterrows():
    status = "✓" if row['%'] >= 100 else "✗"
    print(f"{row['No']:<3} {row['Nama DS']:<30} {row['Grade']:<5} {row['Target']:<6} {row['Sales']:<5} {row['%']:<8}% {status}")

# 6. Analisis Extreme Performers
print("\n" + "="*60)
print("ANALISIS EXTREME PERFORMERS")
print("="*60)

print("\nTOP PERFORMERS:")
top_3 = df.nlargest(3, '%')
for _, row in top_3.iterrows():
    print(f"  {row['Nama DS']}: {row['%']}% (Sales: {row['Sales']}/{row['Target']})")

print("\nBOTTOM PERFORMERS:")
bottom_3 = df.nsmallest(3, '%')
for _, row in bottom_3.iterrows():
    print(f"  {row['Nama DS']}: {row['%']}% (Sales: {row['Sales']}/{row['Target']})")

# 7. Rekomendasi Strategis
print("\n" + "="*60)
print("REKOMENDASI STRATEGIS UNTUK TEGAL")
print("="*60)

print(f"\n1. OVERVIEW KINERJA:")
print(f"   - Pencapaian keseluruhan: {percentage_achieved:.1f}%")
print(f"   - {len(df[df['%'] >= 100])} dari {len(df)} salesperson mencapai target")
print(f"   - 3 salesperson membutuhkan perhatian khusus (<50%)")

print(f"\n2. UNTUK TOP PERFORMERS:")
for _, row in top_3.iterrows():
    print(f"   - {row['Nama DS']}: Berikan apresiasi dan jadikan mentor")

print(f"\n3. UNTUK BOTTOM PERFORMERS:")
for _, row in bottom_3.iterrows():
    print(f"   - {row['Nama DS']}: Coaching intensif dan evaluasi penyebab")

print(f"\n4. UNTUK SPV:")
spv_perf = df[df['Grade'] == 'SPV']
if len(spv_perf) > 0:
    for _, row in spv_perf.iterrows():
        print(f"   - {row['Nama DS']}: Perlu evaluasi kinerja sebagai supervisor")

print(f"\n5. STRATEGI UMUM:")
print(f"   - Program knowledge sharing dari top performers")
print(f"   - Weekly performance review")
print(f"   - Target adjustment berdasarkan capability individual")