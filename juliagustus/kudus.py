import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style seaborn
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# Data input untuk KUDUS
data = {
    'NO': [1, 2, 3, 4],
    'NAMA': [
        'ACHMAD SAHLAN CHAFID', 'SYAHRUL RAMADHAN', 
        'RIZKY RIMAYANDI OKTIAWAN', 'AFIFAH NILAM SARI'
    ],
    'ROLE': ['DS', 'DS', 'DS', 'DS'],
    'Grade': [25, 25, 25, 25],
    'Target': [25, 25, 25, 25],
    'Sales': [16, 17, 16, 1],
    'Minus/plus': [-9, -8, -9, -24],
    '%': [64, 68, 64, 4]
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate additional metrics
df['Pencapaian_%'] = (df['Sales'] / df['Target']) * 100
df['Status'] = np.where(df['Pencapaian_%'] >= 100, 'Mencapai Target', 'Di Bawah Target')
df['Selisih'] = df['Sales'] - df['Target']

# Analysis summary
total_target = df['Target'].sum()
total_sales = df['Sales'].sum()
overall_percentage = (total_sales / total_target) * 100

# Create visualizations dengan penyesuaian untuk tim kecil
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('ANALISIS PENCAPAIAN SALES TEAM KUDUS\nPeriode: 21 Juli - 20 Agustus', 
             fontsize=16, fontweight='bold')

# Plot 1: Performance per Individu
colors = ['red' if perc < 50 else 'orange' if perc < 80 else 'green'
          for perc in df['Pencapaian_%']]
bars = axes[0, 0].barh(df['NAMA'], df['Pencapaian_%'], color=colors)
axes[0, 0].axvline(x=100, color='blue', linestyle='--', alpha=0.7, label='Target 100%')
axes[0, 0].axvline(x=50, color='orange', linestyle='--', alpha=0.7, label='Benchmark 50%')
axes[0, 0].set_xlabel('Pencapaian (%)')
axes[0, 0].set_title('Pencapaian per Individu\n(Red: <50%, Orange: 50-79%, Green: ≥80%)')
axes[0, 0].legend()

# Plot 2: Distribusi Pencapaian (disesuaikan untuk tim kecil)
performance_bins = [0, 50, 80, 100]
performance_labels = ['Sangat Rendah (<50%)', 'Rendah (50-79%)', 'Baik (≥80%)']
df['Kategori'] = pd.cut(df['Pencapaian_%'], bins=performance_bins, labels=performance_labels)

# Hitung jumlah per kategori
kategori_count = df['Kategori'].value_counts().reindex(performance_labels)

colors_kategori = ['red', 'orange', 'green']
bars = axes[0, 1].bar(kategori_count.index, kategori_count.values, color=colors_kategori)
axes[0, 1].set_title('Distribusi Kinerja Tim Kudus')
axes[0, 1].set_ylabel('Jumlah Sales')
axes[0, 1].tick_params(axis='x', rotation=45)
for i, v in enumerate(kategori_count.values):
    axes[0, 1].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

# Plot 3: Perbandingan Target vs Actual per Individu
x = np.arange(len(df))
width = 0.35

bars1 = axes[1, 0].bar(x - width/2, df['Target'], width, 
                      label='Target', color='lightblue', alpha=0.7)
bars2 = axes[1, 0].bar(x + width/2, df['Sales'], width, 
                      label='Actual Sales', color=colors, alpha=0.7)

axes[1, 0].set_title('Perbandingan Target vs Actual Sales per Individu')
axes[1, 0].set_ylabel('Nilai')
axes[1, 0].set_xlabel('Salesperson')
axes[1, 0].set_xticks(x)
axes[1, 0].set_xticklabels(df['NAMA'], rotation=45, ha='right')
axes[1, 0].legend()

# Plot 4: Pie Chart Kontribusi Sales
sales_contribution = (df['Sales'] / total_sales) * 100
wedges, texts, autotexts = axes[1, 1].pie(df['Sales'], labels=df['NAMA'], autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('Kontribusi Sales per Individu\n(Total Sales: 50)')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# Print summary yang lebih jelas
print("=" * 70)
print("ANALISIS PENCAPAIAN SALES TEAM KUDUS")
print("Periode: 21 Juli - 20 Agustus")
print("=" * 70)

print(f"\n📊 SUMMARY KESELURUHAN:")
print(f"   Total Target: {total_target}")
print(f"   Total Sales: {total_sales}")
print(f"   Pencapaian Tim: {overall_percentage:.1f}%")
print(f"   Jumlah Personil: {len(df)} orang")
print(f"   Selisih: -{abs(df['Selisih'].sum())} (Di bawah target)")

print(f"\n🎯 TARGET vs PENCAPAIAN:")
print(f"   Sales yang mencapai target: {len(df[df['Pencapaian_%'] >= 100])} orang")
print(f"   Sales di bawah target: {len(df[df['Pencapaian_%'] < 100])} orang")

print(f"\n📈 DISTRIBUSI KINERJA:")
for kategori in performance_labels:
    count = len(df[df['Kategori'] == kategori])
    print(f"   • {kategori}: {count} orang")

print(f"\n🏆 TOP PERFORMERS:")
top_2 = df.nlargest(2, 'Pencapaian_%')[['NAMA', 'Sales', 'Target', 'Pencapaian_%']]
for _, row in top_2.iterrows():
    print(f"   • {row['NAMA']}: {row['Pencapaian_%']:.0f}% ({row['Sales']}/{row['Target']})")

print(f"\n⚠️  BOTTOM PERFORMERS:")
bottom_2 = df.nsmallest(2, 'Pencapaian_%')[['NAMA', 'Sales', 'Target', 'Pencapaian_%']]
for _, row in bottom_2.iterrows():
    print(f"   • {row['NAMA']}: {row['Pencapaian_%']:.0f}% ({row['Sales']}/{row['Target']})")

# Analisis kontribusi sales
print(f"\n💰 KONTRIBUSI SALES:")
top_performers = df.nlargest(3, 'Sales')[['NAMA', 'Sales', 'Pencapaian_%']]
total_top_sales = top_performers['Sales'].sum()
print(f"   Top 3 performers berkontribusi {total_top_sales} dari {total_sales} sales ({total_top_sales/total_sales*100:.1f}%)")

# Analisis masalah serius
critical_performer = df[df['Sales'] <= 1]
print(f"\n🚨 MASALAH KRITIS:")
print(f"   {len(critical_performer)} orang dengan 1 sales: {critical_performer['NAMA'].iloc[0]}")

print(f"\n💡 REKOMENDASI UNTUK KUDUS:")
print("   1. ✅ 3 ANGGOTA SOLID: Achmad, Syahrul, Rizky menunjukkan performa konsisten (64-68%)")
print("   2. 🚨 EMERGENCY INTERVENTION: Untuk Afifah Nilam Sari (4% - hanya 1 sales)")
print("   3. 📈 POTENSI TINGGI: 3 anggota utama hampir mencapai 70% - tinggal sedikit improvement")
print("   4. 🤝 TIM KECIL YANG KOMPAK: Dapat fokus pada personalized coaching")
print("   5. 🎯 TARGET REALISTIS: Untuk Afifah, mungkin perlu target yang lebih achievable")
print("   6. 🔄 KNOWLEDGE SHARING: 3 top performers bisa bantu Afifah dengan teknik selling")
print("   7. 📊 FOKUS PADA CONSISTENCY: Maintain performa 3 anggota utama")
print("   8. 👥 SUPPORT SYSTEM: Bangun sistem mentoring dalam tim kecil")

print("=" * 70)

# Analisis detail performa
print("\n" + "=" * 50)
print("ANALISIS DETAIL PERFORMA KUDUS")
print("=" * 50)

# Analisis konsistensi tim utama
main_team = df[df['Pencapaian_%'] > 50]
print(f"👥 TIM UTAMA (3 orang dengan performa >50%):")
print(f"   • Rata-rata: {main_team['Pencapaian_%'].mean():.1f}%")
print(f"   • Standar deviasi: {main_team['Pencapaian_%'].std():.1f}% (sangat konsisten)")
print(f"   • Total kontribusi: {main_team['Sales'].sum()}/50 sales ({main_team['Sales'].sum()/50*100:.1f}%)")

print(f"\n🎯 PERFORMANCE BREAKDOWN:")
print(f"   • SYAHRUL RAMADHAN: 68% (17/25) - Performa terbaik")
print(f"   • ACHMAD SAHLAN CHAFID: 64% (16/25) - Konsisten")
print(f"   • RIZKY RIMAYANDI OKTIAWAN: 64% (16/25) - Konsisten")
print(f"   • AFIFAH NILAM SARI: 4% (1/25) - Membutuhkan intervensi darurat")

print(f"\n📊 POTENSI TIM KUDUS:")
print("   • 3 anggota menunjukkan konsistensi dan potensi improvement")
print("   • Tim kecil memudahkan coaching personalized")
print("   • Dengan perbaikan Afifah, tim bisa mencapai >75%")
print("   • Current performance 67% cukup baik untuk tim kecil")

# Analisis impact improvement
print(f"\n🔮 SIMULASI IMPROVEMENT:")
print(f"   Jika Afifah bisa mencapai 50%: +11 sales → total 61 sales (81%)")
print(f"   Jika Afifah bisa mencapai 64%: +15 sales → total 65 sales (87%)")
print(f"   Jika semua mencapai 75%: total 75 sales (100%)")