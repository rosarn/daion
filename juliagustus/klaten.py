import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set style untuk visualisasi
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Data preparation untuk Area Klaten
data = {
    'Name': ['MUAMMAL IQBAL', 'IMAM BAGUS FAISAL', 'FENDI YULIYANTO', 'HARIYANTO', 
             'ARCELA', 'ADITYA DANAR SAPUTRA', 'SALSA NUR FITRIA', 
             'BEASTRICE ARUM SEKARWANGI', 'TOTOK YUNUS WEDIYANTO'],
    'Grade': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'Target': [25, 25, 25, 25, 25, 25, 25, 25, 25],
    'Sales': [10, 10, 17, 13, 17, 3, 4, 5, 1],
    'Achievement_%': [40, 40, 68, 52, 68, 12, 16, 20, 4]
}

df = pd.DataFrame(data)
df['Performance_Status'] = np.where(df['Achievement_%'] >= 100, 'Di Atas Target', 'Di Bawah Target')
df['Region'] = 'KLATEN'  # Tambahkan kolom region

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
fig.suptitle('ANALISIS KINERJA AREA KLATEN (21 Jul - 20 Agu)', fontsize=16, fontweight='bold')

# Warna untuk chart
warna_diatas = '#4ECDC4'  # Hijau
warna_dibawah = '#FF6B6B'  # Merah

# 1. Performansi Tim Klaten
achievement_values = df['Achievement_%']
names = df['Name']
colors = [warna_dibawah] * len(df)  # Semua merah karena semua di bawah target

bars1 = axes[0,0].barh(names, achievement_values, color=colors)
axes[0,0].set_title('PERFORMANSI INDIVIDUAL TIM KLATEN', fontweight='bold')
axes[0,0].set_xlabel('Pencapaian (%)')
axes[0,0].axvline(x=100, color='green', linestyle='--', alpha=0.7, label='Target 100%')
axes[0,0].axvline(x=50, color='orange', linestyle='--', alpha=0.7, label='Batas 50%')
for bar, value in zip(bars1, achievement_values):
    axes[0,0].text(value + 2, bar.get_y() + bar.get_height()/2, f'{value}%', va='center', fontsize=9)

# 2. Sales vs Target Comparison
x_pos = np.arange(len(df))
width = 0.35
axes[0,1].bar(x_pos - width/2, df['Target'], width, label='Target', alpha=0.8, color='#FF9F45')
axes[0,1].bar(x_pos + width/2, df['Sales'], width, label='Penjualan Aktual', alpha=0.8, color='#36AE7C')
axes[0,1].set_title('TARGET vs PENJUALAN AKTUAL', fontweight='bold')
axes[0,1].set_ylabel('Jumlah Unit')
axes[0,1].set_xticks(x_pos)
axes[0,1].set_xticklabels([name.split()[0] for name in df['Name']], rotation=45)
axes[0,1].legend()

# 3. Ranking Performansi
sorted_df = df.sort_values('Achievement_%', ascending=True)
bars3 = axes[1,0].barh(sorted_df['Name'], sorted_df['Achievement_%'], color=warna_dibawah)
axes[1,0].set_title('RANKING PERFORMANSI (Terendah ke Tertinggi)', fontweight='bold')
axes[1,0].set_xlabel('Pencapaian (%)')
axes[1,0].axvline(x=50, color='orange', linestyle='--', alpha=0.7, label='Batas 50%')
for bar, value in zip(bars3, sorted_df['Achievement_%']):
    axes[1,0].text(value + 2, bar.get_y() + bar.get_height()/2, f'{value}%', va='center', fontsize=9)

# 4. Analysis by Achievement Range
bins = [0, 20, 50, 100, 200]
labels = ['Sangat Rendah (<20%)', 'Rendah (20-50%)', 'Sedang (50-100%)', 'Tinggi (>100%)']
df['Achievement_Category'] = pd.cut(df['Achievement_%'], bins=bins, labels=labels, right=False)
category_counts = df['Achievement_Category'].value_counts()

category_colors = ['#FF4757', '#FF6B6B', '#FF9F45', '#4ECDC4']
wedges, texts, autotexts = axes[1,1].pie(category_counts.values, labels=category_counts.index, 
                                        autopct='%1.1f%%', colors=category_colors, startangle=90)
axes[1,1].set_title('DISTRIBUSI BERDASARKAN KATEGORI PENCAPAIAN', fontweight='bold')

plt.tight_layout()
plt.show()

# Analisis Mendalam
print("=" * 60)
print("📊 LAPORAN ANALISIS KINERJA AREA KLATEN")
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

print(f"\n⚠️  PERFORMER DENGAN ISSUE KRITIS:")
print("-" * 40)
very_low = df[df['Achievement_%'] < 20]
extremely_low = df[df['Achievement_%'] < 10]
print(f"Dibawah 20%: {len(very_low)} orang")
print(f"Dibawah 10%: {len(extremely_low)} orang")

if len(very_low) > 0:
    print("\n🔍 Detail Performa Sangat Rendah (<20%):")
    for _, row in very_low.iterrows():
        print(f"   ❌ {row['Name']}: {row['Achievement_%']}% ({row['Sales']} unit)")

print(f"\n👥 ANALISIS BERDASARKAN GRADE:")
print("-" * 40)
for _, row in grade_summary.iterrows():
    status = "✅ DI ATAS TARGET" if row['Achievement_%'] >= 100 else "❌ DI BAWAH TARGET"
    print(f"{row['Grade']}: {row['Achievement_%']:.1f}% ({row['Count']} orang) - {status}")

print(f"\n📊 DISTRIBUSI PERFORMANSI:")
print("-" * 40)
for category in labels:
    count = len(df[df['Achievement_Category'] == category])
    percentage = (count / len(df)) * 100
    print(f"{category}: {count} orang ({percentage:.1f}%)")

print(f"\n🔢 STATISTIK DETAIL:")
print("-" * 40)
print(f"Rata-rata Pencapaian: {df['Achievement_%'].mean():.1f}%")
print(f"Pencapaian Tertinggi: {df['Achievement_%'].max():.0f}%")
print(f"Pencapaian Terendah: {df['Achievement_%'].min():.0f}%")
print(f"Median Pencapaian: {df['Achievement_%'].median():.1f}%")

print(f"\n💡 REKOMENDASI STRATEGIS UNTUK KLATEN:")
print("-" * 50)
print("1. 🚨 STATUS DARURAT: Tim Klaten dalam kondisi KRITIS (35%)")
print("2. 🎯 FOKUS segera pada 4 salesperson dengan achievement < 20%")
print("3. 👥 KELOMPOKKAN tim menjadi:")
print("   - GROUP A (40-68%): FENDI, ARCELA, HARIYANTO, MUAMMAL, IMAM")
print("   - GROUP B (<20%): ADITYA, SALSA, BEASTRICE, TOTOK")
print("4. 📊 BUAT program coaching khusus untuk GROUP B")
print("5. 🔄 PAIRING: Totok (4%) dengan Fendi (68%) untuk mentoring")
print("6. 🎪 BUAT kompetisi antara GROUP A dan GROUP B")
print("7. 📈 SET target incremental: Group A target 75%, Group B target 30%")
print("8. 🔍 INVESTIGASI akar masalah: apakah masalah training, motivasi, atau external factor")
print("9. 🏆 BERI reward untuk yang mencapai improvement terbesar")
print("10. 📅 LAKUKAN daily monitoring untuk Group B")

print(f"\n📋 ACTION PLAN IMMEDIATE:")
print("-" * 40)
print("MINGGU 1:")
print("- One-on-one coaching untuk 4 lowest performers")
print("- Set weekly target yang realistic")
print("- Daily progress check")

print("\nMINGGU 2:")
print("- Group training untuk sales techniques")
print("- Role playing session")
print("- Review hasil weekly target")

print(f"\n🎯 TARGET PEMULIHAN:")
print("-" * 40)
print("Bulan 1: Mencapai 50% overall achievement")
print("Bulan 2: Mencapai 65% overall achievement") 
print("Bulan 3: Mencapai 80% overall achievement")

# Analisis detail per salesperson
print(f"\n🔍 ANALYSIS PER SALESPERSON:")
print("-" * 40)
for _, row in df.iterrows():
    status = "🟢 BAIK" if row['Achievement_%'] >= 50 else "🟡 PERLU PERBAIKAN" if row['Achievement_%'] >= 20 else "🔴 KRITIS"
    gap = row['Target'] - row['Sales']
    print(f"{row['Name']}: {row['Achievement_%']}% | {status} | Gap: {gap} unit")