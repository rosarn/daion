import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data untuk Cengkareng
data_cengkareng = {
    'No': [1],
    'Nama DS': ['Muhammad Nur Zaman Akbar'],
    'Grade': ['S2'],
    'Target': [25],
    'Sales': [0],
    '%': [0]
}

# Membuat DataFrame
df = pd.DataFrame(data_cengkareng)

# Menambahkan kolom performa
df['Status'] = df['%'].apply(lambda x: 'Above Target' if x >= 100 else 'Below Target')

# 1. Ringkasan Kinerja Keseluruhan
total_target = df['Target'].sum()
total_sales = df['Sales'].sum()
percentage_achieved = (total_sales / total_target) * 100

print("=== RINGKASAN KINERJA CENGKARENG ===")
print(f"Regional Head: Benni Novensus")
print(f"Sub Regional: Barlian Purba")
print(f"Sales Manager: Asri Lusiana Sagala")
print(f"Periode: 21 Juli - 20 Agustus")
print(f"Total Target: {total_target}")
print(f"Total Sales: {total_sales}")
print(f"Pencapaian: {percentage_achieved:.1f}%")
print(f"Selisih: {total_sales - total_target}")

# 2. Visualisasi Data yang disesuaikan untuk data tunggal
plt.style.use('default')
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('Analisis Kinerja Sales Cengkareng (21 Juli - 20 Agustus)', fontsize=16, fontweight='bold')

# Warna untuk visualisasi
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Grafik 1: Pencapaian Salesperson
bars = axes[0].bar(df['No'], df['%'], color=colors[0], alpha=0.7, width=0.6)
axes[0].axhline(y=100, color='red', linestyle='--', alpha=0.7, linewidth=2)
axes[0].set_title('Pencapaian Salesperson', fontsize=14)
axes[0].set_xlabel('Salesperson', fontsize=12)
axes[0].set_ylabel('Pencapaian (%)', fontsize=12)
axes[0].set_xticks(df['No'])
axes[0].set_xticklabels([df['Nama DS'][0].split()[0]], rotation=45)
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim(0, 120)

# Menambahkan nilai pada bar
for bar, percentage in zip(bars, df['%']):
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{percentage}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

# Grafik 2: Pie chart status pencapaian
status_counts = df['Status'].value_counts()
axes[1].pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
           colors=[colors[4], colors[3]], startangle=90)
axes[1].set_title('Status Pencapaian Target', fontsize=14)

plt.tight_layout()
plt.show()

# 3. Analisis Statistik
print("\n=== ANALISIS STATISTIK ===")
print(f"Rata-rata pencapaian: {df['%'].mean():.1f}%")
print(f"Jumlah yang mencapai target: {len(df[df['%'] >= 100])} dari {len(df)} salesperson")

# 4. Analisis berdasarkan Grade
grade_analysis = df.groupby('Grade').agg({
    'Target': 'sum',
    'Sales': 'sum',
    '%': 'mean',
    'No': 'count'
}).rename(columns={'No': 'Jumlah Salesperson'})

print("\n=== ANALISIS BERDASARKAN GRADE ===")
print(grade_analysis)

# 5. Kategori Performa
def categorize_performance(pct):
    if pct >= 100:
        return "Excellent (≥100%)"
    elif pct >= 80:
        return "Good (80-99%)"
    elif pct >= 60:
        return "Fair (60-79%)"
    elif pct >= 40:
        return "Poor (40-59%)"
    else:
        return "Very Poor (<40%)"

df['Kategori'] = df['%'].apply(categorize_performance)
category_counts = df['Kategori'].value_counts()

print("\n=== KATEGORI PERFORMANCE ===")
for category, count in category_counts.items():
    percentage = (count / len(df)) * 100
    print(f"{category}: {count} salesperson ({percentage:.1f}%)")

# 6. Tabel Detail Performa
print("\n=== DETAIL PERFORMANCE ===")
print("No. | Nama Salesperson | Target | Sales | Pencapaian | Status")
print("-" * 65)
for _, row in df.iterrows():
    status = "✓" if row['%'] >= 100 else "✗"
    print(f"{row['No']:2} | {row['Nama DS'][:20]:20} | {row['Target']:6} | {row['Sales']:5} | {row['%']:9}% | {status}")

# 7. Rekomendasi Strategis
print("\n" + "="*60)
print("REKOMENDASI STRATEGIS UNTUK CENGKARENG")
print("="*60)
print("1. ANALISIS SITUASI:")
print("   - Hanya ada 1 salesperson di daerah Cengkareng")
print("   - Pencapaian: 0% (Tidak ada sales sama sekali)")
print("   - Ini menunjukkan masalah serius yang perlu segera ditangani")

print("\n2. PENYELIDIKAN YANG DIPERLUKAN:")
print("   - Apakah salesperson masih aktif bekerja?")
print("   - Apakah ada kendala teknis atau administrasi?")
print("   - Apakah daerah Cengkareng masih menjadi area coverage?")
print("   - Apakah salesperson mendapatkan training yang cukup?")

print("\n3. TINDAKAN SEGERA:")
print("   - Hubungi salesperson untuk memahami situasi")
print("   - Review assignment dan territory coverage")
print("   - Berikan coaching dan support intensif")
print("   - Pertimbangkan penambahan salesperson di area tersebut")

print("\n4. STRATEGI JANGKA PANJANG:")
print("   - Evaluasi potensi pasar di daerah Cengkareng")
print("   - Pertimbangkan realokasi resources jika diperlukan")
print("   - Develop strategy untuk market development")
print("   - Setup performance monitoring yang lebih ketat")

print("\n5. TARGET PEMULIHAN:")
print("   - Immediate: Identifikasi dan selesaikan masalah dasar")
print("   - Short-term: Capai minimal 40% target dalam bulan berikutnya")
print("   - Medium-term: Capai 80%+ target dalam 3 bulan")