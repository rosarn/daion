import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set style untuk visualisasi
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Data preparation untuk Area Solo
data = {
    'Name': ['ANSI PUTRI LORENZA', 'RYAN PRAMASDA PUTRA', 'BUDI KRISTIAWAN', 'GUGUT JULI PRAYITNO', 'SISWANTI',
             'RAHMA PRASETYAWATI', 'MARIA AVIANTI', 'JOKO BINTORO', 'AWAN AFANOVA', 'ANTIK SULISTYOWATI',
             'SUGIYONO', 'TRI HARYANTO', 'SUSILO', 'IMAM MULADI', 'YULIANTO', 'MIFTA HASBI HARIRI',
             'HERPRATAMA INDRO SETYAJATI', 'M SULTAN FAHMI FIRMANSYAH', 'DANANG SETYAWAN', 'DENY AJI WIBOWO',
             'ARIF NUGROHO', 'MUHAMMAD DLUNUROEN', 'RIZKI BETA KURNIAWAN', 'EDWIN CHRISTIAN ISHUANTO',
             'SAPTOTO WAHYU NUGROHO', 'DODY WAHYU PRANOTO, SE'],
    'Grade': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS',
              'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'Target': [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25],
    'Sales': [0, 57, 10, 11, 12, 9, 0, 13, 19, 8, 31, 9, 0, 26, 21, 12, 2, 2, 0, 12, 1, 2, 20, 3, 0, 3],
    'Achievement_%': [0, 228, 40, 44, 48, 36, 0, 52, 76, 32, 124, 36, 0, 104, 84, 48, 8, 8, 0, 48, 4, 8, 80, 12, 0, 12]
}

df = pd.DataFrame(data)
df['Performance_Status'] = np.where(df['Achievement_%'] >= 100, 'Di Atas Target', 'Di Bawah Target')
df['Region'] = 'SOLO'  # Tambahkan kolom region

# Analisis berdasarkan Grade
grade_summary = df.groupby('Grade').agg(
    Total_Target=('Target', 'sum'),
    Total_Sales=('Sales', 'sum'),
    Avg_Achievement=('Achievement_%', 'mean'),
    Count=('Name', 'count')
).reset_index()
grade_summary['Achievement_%'] = (grade_summary['Total_Sales'] / grade_summary['Total_Target']) * 100

# Performance distribution
performance_dist = df['Performance_Status'].value_counts()

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('ANALISIS KINERJA AREA SOLO (21 Jul - 20 Agu)', fontsize=16, fontweight='bold')

# Warna untuk chart
warna_diatas = '#4ECDC4'  # Hijau
warna_dibawah = '#FF6B6B'  # Merah

# 1. Performansi berdasarkan Grade
grade_colors = [warna_dibawah if x < 100 else warna_diatas for x in grade_summary['Achievement_%']]
bars1 = axes[0,0].bar(grade_summary['Grade'], grade_summary['Achievement_%'], color=grade_colors)
axes[0,0].set_title('PERFORMANSI BERDASARKAN GRADE', fontweight='bold')
axes[0,0].set_ylabel('Pencapaian (%)')
axes[0,0].axhline(y=100, color='red', linestyle='--', alpha=0.7)
for bar, value, count in zip(bars1, grade_summary['Achievement_%'], grade_summary['Count']):
    axes[0,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                  f'{value:.0f}%\n(n={count})', ha='center', va='bottom', fontsize=10)

# 2. Distribusi Performansi
performance_colors = [warna_dibawah, warna_diatas]
wedges, texts, autotexts = axes[0,1].pie(performance_dist.values, labels=performance_dist.index, 
                                        autopct='%1.1f%%', colors=performance_colors, startangle=90)
axes[0,1].set_title('DISTRIBUSI PERFORMANSI TIM', fontweight='bold')

# 3. Top 10 Performers
top_10 = df.nlargest(10, 'Achievement_%')
top_colors = [warna_diatas if x >= 100 else warna_dibawah for x in top_10['Achievement_%']]
bars3 = axes[1,0].barh(top_10['Name'], top_10['Achievement_%'], color=top_colors)
axes[1,0].set_title('TOP 10 PERFORMER', fontweight='bold')
axes[1,0].set_xlabel('Pencapaian (%)')
axes[1,0].axvline(x=100, color='red', linestyle='--', alpha=0.7)
for bar, value in zip(bars3, top_10['Achievement_%']):
    axes[1,0].text(value + 5, bar.get_y() + bar.get_height()/2, f'{value}%', va='center')

# 4. Bottom 10 Performers
bottom_10 = df.nsmallest(10, 'Achievement_%')
bottom_colors = [warna_dibawah] * len(bottom_10)
bars4 = axes[1,1].barh(bottom_10['Name'], bottom_10['Achievement_%'], color=bottom_colors)
axes[1,1].set_title('BOTTOM 10 PERFORMER', fontweight='bold')
axes[1,1].set_xlabel('Pencapaian (%)')
axes[1,1].axvline(x=100, color='red', linestyle='--', alpha=0.7)
for bar, value in zip(bars4, bottom_10['Achievement_%']):
    axes[1,1].text(value + 5, bar.get_y() + bar.get_height()/2, f'{value}%', va='center')

plt.tight_layout()
plt.show()

# Analisis Mendalam
print("=" * 60)
print("📊 LAPORAN ANALISIS KINERJA AREA SOLO")
print("=" * 60)

print(f"\n🎯 RINGKASAN KINERJA:")
print("-" * 40)
print(f"Total Target: {df['Target'].sum():,} unit")
print(f"Total Penjualan: {df['Sales'].sum():,} unit")
print(f"Pencapaian Keseluruhan: {(df['Sales'].sum()/df['Target'].sum())*100:.1f}%")
print(f"Kekurangan: {df['Target'].sum() - df['Sales'].sum():,} unit")

print(f"\n⭐ PERFORMER TERBAIK:")
print("-" * 40)
top_3 = df.nlargest(3, 'Achievement_%')
for _, row in top_3.iterrows():
    print(f"🏆 {row['Name']}: {row['Achievement_%']}% ({row['Sales']} unit)")

print(f"\n⚠️  PERFORMER DENGAN ISSUE:")
print("-" * 40)
zero_sales = df[df['Sales'] == 0]
low_performers = df[df['Achievement_%'] < 20]
print(f"Penjualan 0 unit: {len(zero_sales)} orang")
print(f"Dibawah 20%: {len(low_performers)} orang")

if len(zero_sales) > 0:
    print("\n🔍 Detail Sales 0 unit:")
    for _, row in zero_sales.iterrows():
        print(f"   ❌ {row['Name']} ({row['Grade']})")

print(f"\n👥 ANALISIS BERDASARKAN GRADE:")
print("-" * 40)
for _, row in grade_summary.iterrows():
    status = "✅ DI ATAS TARGET" if row['Achievement_%'] >= 100 else "❌ DI BAWAH TARGET"
    print(f"{row['Grade']}: {row['Achievement_%']:.1f}% ({row['Count']} orang) - {status}")

print(f"\n📈 DISTRIBUSI PERFORMANSI:")
print("-" * 40)
above_target = len(df[df['Achievement_%'] >= 100])
below_target = len(df[df['Achievement_%'] < 100])
total_salespeople = len(df)
print(f"Di Atas Target: {above_target} orang ({above_target/total_salespeople*100:.1f}%)")
print(f"Di Bawah Target: {below_target} orang ({below_target/total_salespeople*100:.1f}%)")

print(f"\n💡 REKOMENDASI STRATEGIS:")
print("-" * 40)
print("1. 🎯 FOKUS pada 4 SPV yang penjualannya 0 unit")
print("2. ⭐ MANFAATKAN top performers (Ryan, Sugiyono, Imam) sebagai mentor")
print("3. 🔄 COACHING intensif untuk 10 performer terbawah")
print("4. 📊 REVIEW target untuk SPV yang konsisten underperform")
print("5. 🎪 BUAT kompetisi internal berdasarkan grade")
print("6. 🔍 INVESTIGASI akar masalah di performer dengan achievement < 20%")
print("7. 📈 OPTIMALKAN strategi dari performer di atas 100%")

print(f"\n🔢 STATISTIK DETAIL:")
print("-" * 40)
print(f"Rata-rata Pencapaian: {df['Achievement_%'].mean():.1f}%")
print(f"Pencapaian Tertinggi: {df['Achievement_%'].max():.0f}%")
print(f"Pencapaian Terendah: {df['Achievement_%'].min():.0f}%")
print(f"Median Pencapaian: {df['Achievement_%'].median():.1f}%")

# Analisis SPV khusus
print(f"\n👨‍💼 ANALISIS KHUSUS SPV:")
print("-" * 40)
spv_data = df[df['Grade'] == 'SPV']
if len(spv_data) > 0:
    for _, row in spv_data.iterrows():
        status = "✅ BAIK" if row['Achievement_%'] >= 100 else "❌ PERLU PERHATIAN"
        print(f"{row['Name']}: {row['Achievement_%']}% - {status}")
else:
    print("Tidak ada data SPV")

print(f"\n📋 LIST SEMUA SALESPERSON DENGAN ACHIEVEMENT < 50%:")
print("-" * 50)
low_achievers = df[df['Achievement_%'] < 50]
if len(low_achievers) > 0:
    for _, row in low_achievers.iterrows():
        print(f"{row['Name']}: {row['Achievement_%']}% ({row['Sales']} unit)")
else:
    print("Tidak ada salesperson dengan achievement di bawah 50%")