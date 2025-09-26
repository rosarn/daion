import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data untuk Semarang
data_semarang = {
    'No': range(1, 53),
    'Nama DS': [
        'INDRA SETIAWAN', 'Daima', 'Arief prabowo', 'Anisa salsa nabila meita',
        'Anityo kukuh wirastantyo', 'Moch syafrany', 'Sudibyo pujo wiyono',
        'Dedimy dwi saputra', 'RUDI KUNCORO', 'Achmad hasan arfie',
        'Aditia rahman', 'Lina indriyani', 'Rima kuti', 'Teguh subekti',
        'Michael kevin agusta putra', 'Andri afrizal', 'AKHMAD HARUN',
        'Eri setiawan', 'Dodo kristono', 'Avian wijayanto', 'Widarwanto',
        'Nur kholidin', 'Wiwin Apit Yulianto', 'NUR SALIM', 'Ahmad Syaikhu',
        'Taufik Jorgi Kurniawan', 'Pramunita Kristianti', 'Rindi Adi Pratama',
        'HELMY AS\'ARY', 'Aries sulistiyanto', 'Habib Akbar', 'Rezki Irwandy',
        'Bayu Satria Putra', 'Rifqi Mubarak', 'Abdurrahman', 'IDA BAGUS KAMAJAYA',
        'Aris Supriyadi', 'M Abidin ardiyanto', 'Putri puspitasari',
        'Nendra dewa kurniawan', 'PRANA BRAHMANTYA', 'Frengky Gilang Adi Pradana',
        'Antonia Widya', 'Khofsah Noor', 'Francois Febriyanto', 'Ardianto Arif Pramono',
        'NUR HADI', 'Yusuf Rani', 'Siti Nurjanah', 'Fitria Jayanti Mahmud',
        'Yosi Imelda', 'Lilik Setiawan'
    ],
    'Grade': [
        'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS',
        'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS',
        'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS',
        'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS',
        'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS',
        'DS', 'DS'
    ],
    'Target': [35, 25, 25, 25, 25, 25, 25, 25, 35, 25,
               25, 25, 25, 25, 25, 25, 35, 25, 25, 25,
               25, 25, 25, 35, 25, 25, 25, 25, 35, 25,
               25, 25, 25, 25, 25, 35, 25, 25, 25, 25,
               35, 25, 25, 25, 25, 25, 35, 25, 25, 25,
               25, 25],
    'Sales': [0, 73, 19, 46, 28, 43, 25, 28, 0, 41,
              60, 43, 22, 25, 14, 18, 0, 24, 22, 22,
              91, 18, 19, 29, 37, 37, 36, 19, 7, 27,
              35, 14, 19, 44, 1, 13, 57, 26, 28, 26,
              18, 20, 22, 17, 32, 17, 5, 19, 33, 11,
              2, 14],
    '%': [0, 292, 76, 184, 112, 172, 100, 112, 0, 164,
          240, 172, 88, 100, 56, 72, 0, 96, 88, 88,
          364, 72, 76, 83, 148, 148, 144, 76, 20, 108,
          140, 56, 76, 176, 4, 37, 228, 104, 112, 104,
          51, 80, 88, 68, 128, 68, 14, 76, 132, 44,
          8, 56]
}

# Membuat DataFrame
df = pd.DataFrame(data_semarang)

# Menambahkan kolom performa
df['Status'] = df['%'].apply(lambda x: 'Above Target' if x >= 100 else 'Below Target')

# 1. Ringkasan Kinerja Keseluruhan
total_target = df['Target'].sum()
total_sales = df['Sales'].sum()
percentage_achieved = (total_sales / total_target) * 100

print("=== RINGKASAN KINERJA SEMARANG ===")
print(f"Regional Head: Susanto")
print(f"Sub Regional Head: Arya Adithya Kurnia")
print(f"Sales Manager: Ilham Tejo Wahono")
print(f"Periode: 21 Juli - 20 Agustus")
print(f"Total Target: {total_target}")
print(f"Total Sales: {total_sales}")
print(f"Pencapaian: {percentage_achieved:.1f}%")
print(f"Selisih: {total_sales - total_target}")

# 2. Visualisasi Data
plt.style.use('default')
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Analisis Kinerja Sales Semarang (21 Juli - 20 Agustus)', fontsize=16, fontweight='bold')

# Warna untuk visualisasi
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Grafik 1: Distribusi Pencapaian per Salesperson
bars = axes[0, 0].bar(df['No'], df['%'], color=np.where(df['%'] >= 100, 'green', '#1f77b4'), alpha=0.7)
axes[0, 0].axhline(y=100, color='red', linestyle='--', alpha=0.7, linewidth=2)
axes[0, 0].set_title('Pencapaian per Salesperson', fontsize=14)
axes[0, 0].set_xlabel('Salesperson', fontsize=12)
axes[0, 0].set_ylabel('Pencapaian (%)', fontsize=12)
axes[0, 0].tick_params(axis='x', rotation=90)
axes[0, 0].grid(True, alpha=0.3)

# Menambahkan nama pada setiap bar (hanya untuk yang outstanding)
for i, bar in enumerate(bars):
    if df['%'][i] >= 150 or df['%'][i] == 0:  # Hanya label yang sangat tinggi atau 0%
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 5,
                       f'{df["Nama DS"][i].split()[0]}',
                       ha='center', va='bottom', fontsize=7, rotation=90)

# Grafik 2: Perbandingan Grade
grade_performance = df.groupby('Grade')['%'].mean()
bars_grade = axes[0, 1].bar(grade_performance.index, grade_performance.values, color=['orange', 'blue'])
axes[0, 1].set_title('Rata-rata Pencapaian berdasarkan Grade', fontsize=14)
axes[0, 1].set_ylabel('Rata-rata Pencapaian (%)', fontsize=12)
axes[0, 1].grid(True, alpha=0.3)

# Menambahkan nilai pada setiap batang grade
for i, (bar, value) in enumerate(zip(bars_grade, grade_performance.values)):
    axes[0, 1].text(bar.get_x() + bar.get_width()/2, value + 5, f'{value:.1f}%', 
                   ha='center', va='bottom', fontsize=10)

# Grafik 3: Top 10 Performers
top10 = df.nlargest(10, '%')
bars_top = axes[0, 2].barh(top10['Nama DS'], top10['%'], color='green', alpha=0.7)
axes[0, 2].set_title('Top 10 Performers', fontsize=14)
axes[0, 2].set_xlabel('Pencapaian (%)', fontsize=12)
axes[0, 2].grid(True, alpha=0.3)

# Menambahkan nilai pada setiap batang top performers
for i, (bar, value) in enumerate(zip(bars_top, top10['%'])):
    width = bar.get_width()
    axes[0, 2].text(width + 5, bar.get_y() + bar.get_height()/2, f'{value}%', 
                   ha='left', va='center', fontsize=9)

# Grafik 4: Bottom 10 Performers
bottom10 = df.nsmallest(10, '%')
bars_bottom = axes[1, 0].barh(bottom10['Nama DS'], bottom10['%'], color='red', alpha=0.7)
axes[1, 0].set_title('Bottom 10 Performers', fontsize=14)
axes[1, 0].set_xlabel('Pencapaian (%)', fontsize=12)
axes[1, 0].grid(True, alpha=0.3)

# Menambahkan nilai pada setiap batang bottom performers
for i, (bar, value) in enumerate(zip(bars_bottom, bottom10['%'])):
    width = bar.get_width()
    axes[1, 0].text(width + 1, bar.get_y() + bar.get_height()/2, f'{value}%', 
                   ha='left', va='center', fontsize=9)

# Grafik 5: Histogram Distribusi Frekuensi Pencapaian
counts, bins, patches = axes[1, 1].hist(df['%'], bins=12, alpha=0.7, color=colors[0], 
                                       edgecolor='black', rwidth=0.8)
axes[1, 1].set_title('Distribusi Frekuensi Pencapaian', fontsize=14)
axes[1, 1].set_xlabel('Persentase Pencapaian (%)', fontsize=12)
axes[1, 1].set_ylabel('Jumlah Salesperson', fontsize=12)
axes[1, 1].grid(True, alpha=0.3)

# Menambahkan nilai frekuensi di atas setiap batang histogram
for i, (count, bin_edge) in enumerate(zip(counts, bins)):
    if i < len(counts) and count > 0:
        axes[1, 1].text(bin_edge + (bins[1]-bins[0])/2, count + 0.1, 
                       f'{int(count)}', ha='center', va='bottom')

# Garis mean dan median
mean_percentage = df['%'].mean()
median_percentage = df['%'].median()
axes[1, 1].axvline(mean_percentage, color='green', linestyle='--', label=f'Mean: {mean_percentage:.1f}%')
axes[1, 1].axvline(median_percentage, color='blue', linestyle='--', label=f'Median: {median_percentage:.1f}%')
axes[1, 1].axvline(100, color='red', linestyle='-', alpha=0.7, label='Target (100%)')
axes[1, 1].legend()

# Grafik 6: Pie chart status pencapaian
status_counts = df['Status'].value_counts()
axes[1, 2].pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
               colors=['red', 'green'], startangle=90)
axes[1, 2].set_title('Proporsi Pencapaian Target', fontsize=14)

plt.tight_layout()
plt.show()

# 3. Analisis Statistik
print("\n=== ANALISIS STATISTIK ===")
print(f"Rata-rata pencapaian: {df['%'].mean():.1f}%")
print(f"Median pencapaian: {df['%'].median():.1f}%")
print(f"Standar deviasi: {df['%'].std():.1f}%")
print(f"Jumlah yang mencapai target: {len(df[df['%'] >= 100])} dari {len(df)} salesperson")

# 4. Analisis berdasarkan Grade
grade_analysis = df.groupby('Grade').agg({
    'Target': 'sum',
    'Sales': 'sum',
    '%': 'mean',
    'No': 'count'
}).rename(columns={'No': 'Jumlah Salesperson'})

grade_analysis['Pencapaian'] = (grade_analysis['Sales'] / grade_analysis['Target'] * 100).round(1)
print("\n=== ANALISIS BERDASARKAN GRADE ===")
print(grade_analysis)

# 5. Kategori Performa
def categorize_performance(pct):
    if pct >= 200:
        return "Outstanding (≥200%)"
    elif pct >= 150:
        return "Excellent (150-199%)"
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

# 6. Tabel Top dan Bottom Performers
print("\n=== TOP 10 PERFORMERS ===")
top_10 = df.nlargest(10, '%')[['Nama DS', 'Grade', '%', 'Sales', 'Target']]
print(top_10.to_string(index=False))

print("\n=== BOTTOM 10 PERFORMERS ===")
bottom_10 = df.nsmallest(10, '%')[['Nama DS', 'Grade', '%', 'Sales', 'Target']]
print(bottom_10.to_string(index=False))

# 7. Analisis SPV vs DS
print("\n=== PERFORMANCE SPV vs DS ===")
spv_count = len(df[df['Grade'] == 'SPV'])
spv_above_target = len(df[(df['Grade'] == 'SPV') & (df['%'] >= 100)])
ds_count = len(df[df['Grade'] == 'DS'])
ds_above_target = len(df[(df['Grade'] == 'DS') & (df['%'] >= 100)])

print(f"SPV: {spv_above_target}/{spv_count} mencapai target ({spv_above_target/spv_count*100:.1f}%)")
print(f"DS: {ds_above_target}/{ds_count} mencapai target ({ds_above_target/ds_count*100:.1f}%)")

# 8. Rekomendasi Strategis
print("\n" + "="*60)
print("REKOMENDASI STRATEGIS UNTUK SEMARANG")
print("="*60)
print("1. PERFORMANCE OVERVIEW:")
print(f"   - Pencapaian keseluruhan: 99% (hampir mencapai target)")
print(f"   - {len(df[df['%'] >= 100])} dari {len(df)} salesperson mencapai target")
print(f"   - 6 salesperson dengan pencapaian 0% perlu perhatian khusus")

print("\n2. TOP PERFORMERS (≥200%):")
print("   - Widarwanto (364%): Sales tertinggi (91 dari 25)")
print("   - Daima (292%): Performance outstanding")
print("   - Aditia rahman (240%): Kontribusi signifikan")
print("   - Aris Supriyadi (228%): Performance excellent")

print("\n3. AREA PERBAIKAN:")
print("   - 6 salesperson dengan 0% pencapaian (semua SPV kecuali 1)")
print("   - 5 salesperson dengan pencapaian <20%")
print("   - Performance SPV perlu ditingkatkan secara signifikan")

print("\n4. STRATEGI:")
print("   - Program mentoring: Top performers bantu underperformers")
print("   - Fokus pada improvement SPV yang underperform")
print("   - Pertahankan momentum top performers")
print("   - Review target allocation untuk optimalisasi")

print("\n5. TARGET PRIORITAS:")
print("   - Tingkatkan performa 11 salesperson dengan Very Poor (<50%)")
print("   - Bantu 6 salesperson dengan 0% pencapaian")
print("   - Pertahankan 22 salesperson yang sudah mencapai target")