import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set style untuk visualisasi
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Data preparation untuk Area Jogja
data = {
    'Name': ['THERESIA OKTAVIA', 'SAFII', 'MUHAMAD IKSAN', 'DINA LISTIANA', 'ANDEG LALA',
             'MIRA SUKMA DEWI ISKANDAR PUTRI', 'MUHAMMAD RIZKY EKA PUTRA', 'RIMA TRILIA FIKA SARI',
             'DEMISA ZAI', 'NUR HIDAYAT SULISTYA', 'CHARISMA PRIYA PURNOMO', 'ESTHI NUGROHO DEWI',
             'MARYADI', 'DANIEL TUMANAN', 'RIO MARTIN RUDIANTO', 'SUMARYADI', 'AHLISH HIDAYATULLOH',
             'YOGI PUTRO WASKITO', 'ARIS KURNIANTORO', 'RORI PUJI ASTUTI', 'NOVI EFENDI',
             'MATIAS NOPRYANTO RAUNGKU', 'R. SUHARJONO'],
    'Grade': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS',
              'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'Target': [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25],
    'Sales': [0, 18, 12, 11, 15, 12, 7, 5, 0, 13, 26, 10, 3, 1, 9, 0, 49, 13, 14, 12, 18, 11, 10],
    'Achievement_%': [0, 72, 48, 44, 60, 48, 28, 20, 0, 52, 104, 40, 12, 4, 36, 0, 196, 52, 56, 48, 72, 44, 40]
}

df = pd.DataFrame(data)
df['Performance_Status'] = np.where(df['Achievement_%'] >= 100, 'Di Atas Target', 'Di Bawah Target')
df['Region'] = 'JOGJA'

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
fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('ANALISIS KINERJA AREA JOGJA (21 Jul - 20 Agu)', fontsize=16, fontweight='bold')

# Warna untuk chart
warna_diatas = '#4ECDC4'  # Hijau
warna_dibawah = '#FF6B6B'  # Merah

# 1. Performansi Individual
achievement_values = df['Achievement_%']
names = df['Name']
colors = [warna_diatas if x >= 100 else warna_dibawah for x in achievement_values]

bars1 = axes[0,0].barh(names, achievement_values, color=colors)
axes[0,0].set_title('PERFORMANSI INDIVIDUAL TIM JOGJA', fontweight='bold')
axes[0,0].set_xlabel('Pencapaian (%)')
axes[0,0].axvline(x=100, color='green', linestyle='--', alpha=0.7, label='Target 100%')
axes[0,0].axvline(x=50, color='orange', linestyle='--', alpha=0.7, label='Batas 50%')
for bar, value in zip(bars1, achievement_values):
    axes[0,0].text(value + 5, bar.get_y() + bar.get_height()/2, f'{value}%', va='center', fontsize=8)

# 2. Analysis by Achievement Range
bins = [0, 20, 50, 100, 250]
labels = ['Sangat Rendah (<20%)', 'Rendah (20-50%)', 'Sedang (50-100%)', 'Tinggi (>100%)']
df['Achievement_Category'] = pd.cut(df['Achievement_%'], bins=bins, labels=labels, right=False)
category_counts = df['Achievement_Category'].value_counts()

category_colors = ['#FF4757', '#FF6B6B', '#FF9F45', '#4ECDC4']
wedges, texts, autotexts = axes[0,1].pie(category_counts.values, labels=category_counts.index, 
                                        autopct='%1.1f%%', colors=category_colors, startangle=90)
axes[0,1].set_title('DISTRIBUSI BERDASARKAN KATEGORI PENCAPAIAN', fontweight='bold')

# 3. Top 10 vs Bottom 10 Performers
top_10 = df.nlargest(10, 'Achievement_%')
bottom_10 = df.nsmallest(10, 'Achievement_%')

# Top 10
bars3 = axes[1,0].barh(top_10['Name'], top_10['Achievement_%'], color=warna_diatas)
axes[1,0].set_title('TOP 10 PERFORMER JOGJA', fontweight='bold')
axes[1,0].set_xlabel('Pencapaian (%)')
axes[1,0].axvline(x=100, color='green', linestyle='--', alpha=0.7)
for bar, value in zip(bars3, top_10['Achievement_%']):
    axes[1,0].text(value + 5, bar.get_y() + bar.get_height()/2, f'{value}%', va='center', fontsize=8)

# Bottom 10
bars4 = axes[1,1].barh(bottom_10['Name'], bottom_10['Achievement_%'], color=warna_dibawah)
axes[1,1].set_title('BOTTOM 10 PERFORMER JOGJA', fontweight='bold')
axes[1,1].set_xlabel('Pencapaian (%)')
axes[1,1].axvline(x=50, color='orange', linestyle='--', alpha=0.7)
for bar, value in zip(bars4, bottom_10['Achievement_%']):
    axes[1,1].text(value + 5, bar.get_y() + bar.get_height()/2, f'{value}%', va='center', fontsize=8)

plt.tight_layout()
plt.show()

# Analisis Mendalam
print("=" * 60)
print("📊 LAPORAN ANALISIS KINERJA AREA JOGJA")
print("=" * 60)

print(f"\n🎯 RINGKASAN KINERJA:")
print("-" * 40)
print(f"Total Target: {df['Target'].sum():,} unit")
print(f"Total Penjualan: {df['Sales'].sum():,} unit")
print(f"Pencapaian Keseluruhan: {(df['Sales'].sum()/df['Target'].sum())*100:.1f}%")
print(f"Kekurangan: {df['Target'].sum() - df['Sales'].sum():,} unit")

print(f"\n⭐ TOP 3 PERFORMER:")
print("-" * 40)
top_3 = df.nlargest(3, 'Achievement_%')
for _, row in top_3.iterrows():
    print(f"🏆 {row['Name']}: {row['Achievement_%']}% ({row['Sales']} unit)")

print(f"\n⚠️  PERFORMER DENGAN ISSUE KRITIS:")
print("-" * 40)
zero_sales = df[df['Sales'] == 0]
very_low = df[df['Achievement_%'] < 20]
print(f"Penjualan 0 unit: {len(zero_sales)} orang")
print(f"Dibawah 20%: {len(very_low)} orang")

if len(zero_sales) > 0:
    print("\n🔍 SPV dengan Penjualan 0:")
    for _, row in zero_sales.iterrows():
        print(f"   ❌ {row['Name']} ({row['Grade']})")

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

print(f"\n💡 REKOMENDASI STRATEGIS UNTUK JOGJA:")
print("-" * 50)
print("1. ⚠️  AREA TANPA SALES MANAGER: Butuh penanganan khusus!")
print("2. 🎯 FOKUS pada 3 SPV dengan penjualan 0 unit")
print("3. ⭐ MANFAATKAN AHLISH (196%) sebagai role model dan mentor")
print("4. 🔄 PAIRING SYSTEM:")
print("   - Daniel (4%) pairing dengan AHLISH (196%)")
print("   - Maryadi (12%) pairing dengan CHARISMA (104%)")
print("   - Rima (20%) pairing dengan NOVI (72%)")
print("5. 📊 KELOMPOKKAN tim menjadi:")
print("   - GROUP STAR: AHLISH, CHARISMA (above 100%)")
print("   - GROUP SOLID: SAFII, ANDEG, NOVI, YOGI, ARIS (50-72%)")
print("   - GROUP NEED HELP: lainnya (<50%)")
print("6. 🎪 BUAT kompetisi antar group dengan reward system")
print("7. 📈 SET target bertahap untuk improvement")

print(f"\n🎯 TARGET PEMULIHAN:")
print("-" * 40)
print("Minggu 1: Focus pada 3 SPV zero sales dan 5 lowest performers")
print("Bulan 1: Mencapai 60% overall achievement")
print("Bulan 2: Mencapai 75% overall achievement")
print("Bulan 3: Mencapai 85% overall achievement")

print(f"\n🚨 PRIORITAS SEGERA:")
print("-" * 40)
print("1. Angkat Sales Manager untuk Jogja")
print("2. Coaching intensif untuk 3 SPV")
print("3. Mentoring untuk 5 lowest performers")
print("4. Optimalkan top performers sebagai coach")

# Analisis SPV khusus
print(f"\n👨‍💼 ANALISIS KHUSUS SPV:")
print("-" * 40)
spv_data = df[df['Grade'] == 'SPV']
if len(spv_data) > 0:
    total_spv_sales = spv_data['Sales'].sum()
    total_spv_target = spv_data['Target'].sum()
    spv_achievement = (total_spv_sales / total_spv_target) * 100 if total_spv_target > 0 else 0
    
    print(f"Jumlah SPV: {len(spv_data)} orang")
    print(f"Total Penjualan SPV: {total_spv_sales} unit")
    print(f"Pencapaian SPV: {spv_achievement:.1f}%")
    print("\nDetail SPV:")
    for _, row in spv_data.iterrows():
        status = "✅ BAIK" if row['Achievement_%'] >= 100 else "❌ PERLU PERHATIAN"
        print(f"  {row['Name']}: {row['Achievement_%']}% - {status}")
else:
    print("Tidak ada data SPV")

print(f"\n📋 LIST KRITIS (Achievement < 30%):")
print("-" * 50)
critical_list = df[df['Achievement_%'] < 30]
if len(critical_list) > 0:
    for _, row in critical_list.iterrows():
        print(f"{row['Name']}: {row['Achievement_%']}% ({row['Sales']} unit)")
else:
    print("Tidak ada salesperson dengan achievement di bawah 30%")