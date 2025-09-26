import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style seaborn
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# Data input untuk CILACAP
data = {
    'NO': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    'NAMA': [
        'AGUS WIDODO CILACAP', 'ANGGIA IKMA DEWI', 'HENDRI LISTIONO', 
        'SARWOTO', 'SHERENITA TRIAS YULIANA', 'DWI JAYANTI LESTARI',
        'BAYU PAMBUDI CILACAP', 'LINDA PANGESTIKA', 'AJI PRAYOGA',
        'RIZKI WINDU SANCOYO', 'LUKIS RUCIRA ARUNDATI', 'PUPUT FARIDA',
        'AWALIAH ZULFA TURROHMAH', 'DWIKI DARMAYUDA'
    ],
    'ROLE': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'Grade': [35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 25],
    'Target': [35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 25],
    'Sales': [0, 37, 14, 36, 28, 4, 4, 40, 25, 12, 20, 6, 6, 9],
    'Minus/plus': [-35, 12, -11, 11, 3, -21, -31, 15, 0, -13, -5, -19, -19, -16],
    '%': [0, 148, 56, 144, 112, 16, 11, 160, 100, 48, 80, 24, 24, 36]
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate additional metrics
df['Pencapaian_%'] = (df['Sales'] / df['Target']) * 100
df['Status'] = np.where(df['Pencapaian_%'] >= 100, 'Mencapai Target', 'Di Bawah Target')
df['Selisih'] = df['Sales'] - df['Target']

# Pisahkan data SPV dan DS
spv_df = df[df['ROLE'] == 'SPV']
ds_df = df[df['ROLE'] == 'DS']

# Analysis summary
total_target = df['Target'].sum()
total_sales = df['Sales'].sum()
overall_percentage = (total_sales / total_target) * 100

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('ANALISIS PENCAPAIAN SALES TEAM CILACAP\nPeriode: 21 Juli - 20 Agustus', 
             fontsize=16, fontweight='bold')

# Plot 1: Performance per Individu
colors = ['orange' if role == 'SPV' else ('green' if perc >= 100 else 'red') 
          for role, perc in zip(df['ROLE'], df['Pencapaian_%'])]
bars = axes[0, 0].barh(df['NAMA'], df['Pencapaian_%'], color=colors)
axes[0, 0].axvline(x=100, color='blue', linestyle='--', alpha=0.7, label='Target 100%')
axes[0, 0].set_xlabel('Pencapaian (%)')
axes[0, 0].set_title('Pencapaian per Individu\n(Orange: SPV, Green: ≥Target, Red: <Target)')
axes[0, 0].legend()

# Plot 2: Rata-rata Pencapaian per Role
role_avg = df.groupby('ROLE')['Pencapaian_%'].mean().reset_index()
colors_role = ['orange', 'lightblue']
bars = axes[0, 1].bar(role_avg['ROLE'], role_avg['Pencapaian_%'], color=colors_role)
axes[0, 1].set_title('Rata-rata Pencapaian Berdasarkan Role')
axes[0, 1].set_ylabel('Pencapaian (%)')
axes[0, 1].set_xlabel('Role')
for i, v in enumerate(role_avg['Pencapaian_%']):
    axes[0, 1].text(i, v + 10, f'{v:.1f}%', ha='center', fontweight='bold')

# Plot 3: Distribusi Pencapaian
performance_bins = [0, 50, 80, 100, 200]
performance_labels = ['Sangat Rendah (<50%)', 'Rendah (50-79%)', 'Baik (80-99%)', 'Excellent (≥100%)']
df['Kategori'] = pd.cut(df['Pencapaian_%'], bins=performance_bins, labels=performance_labels)

# Hitung jumlah per kategori
kategori_count = df['Kategori'].value_counts().reindex(performance_labels)

colors_kategori = ['red', 'orange', 'yellow', 'green']
bars = axes[1, 0].bar(kategori_count.index, kategori_count.values, color=colors_kategori)
axes[1, 0].set_title('Distribusi Kinerja Tim')
axes[1, 0].set_ylabel('Jumlah Sales')
axes[1, 0].tick_params(axis='x', rotation=45)
for i, v in enumerate(kategori_count.values):
    axes[1, 0].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

# Plot 4: Perbandingan SPV vs DS
role_comparison = df.groupby('ROLE').agg({
    'Target': 'sum',
    'Sales': 'sum'
}).reset_index()

x = np.arange(len(role_comparison))
width = 0.35

bars1 = axes[1, 1].bar(x - width/2, role_comparison['Target'], width, 
                      label='Target', color=['darkorange', 'lightblue'], alpha=0.7)
bars2 = axes[1, 1].bar(x + width/2, role_comparison['Sales'], width, 
                      label='Actual Sales', color=['orange', 'blue'], alpha=0.7)

axes[1, 1].set_title('Perbandingan Target vs Actual Sales per Role')
axes[1, 1].set_ylabel('Nilai')
axes[1, 1].set_xlabel('Role')
axes[1, 1].set_xticks(x)
axes[1, 1].set_xticklabels(role_comparison['ROLE'])
axes[1, 1].legend()

# Tambahkan nilai di atas bars
for i, (target, sales) in enumerate(zip(role_comparison['Target'], role_comparison['Sales'])):
    axes[1, 1].text(i - width/2, target + 5, f'{target}', ha='center', fontweight='bold')
    axes[1, 1].text(i + width/2, sales + 5, f'{sales}', ha='center', fontweight='bold')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# Print summary yang lebih jelas
print("=" * 70)
print("ANALISIS PENCAPAIAN SALES TEAM CILACAP")
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

print(f"\n👥 ANALISIS BERDASARKAN ROLE:")
print(f"\n   SPV (Supervisor): {len(spv_df)} orang")
print(f"   • Rata-rata pencapaian: {spv_df['Pencapaian_%'].mean():.1f}%")
print(f"   • Total target: {spv_df['Target'].sum()}")
print(f"   • Total sales: {spv_df['Sales'].sum()}")
print(f"   • Pencapaian tim SPV: {(spv_df['Sales'].sum() / spv_df['Target'].sum() * 100):.1f}%")

print(f"\n   DS (Sales): {len(ds_df)} orang")
print(f"   • Rata-rata pencapaian: {ds_df['Pencapaian_%'].mean():.1f}%")
print(f"   • Total target: {ds_df['Target'].sum()}")
print(f"   • Total sales: {ds_df['Sales'].sum()}")
print(f"   • Pencapaian tim DS: {(ds_df['Sales'].sum() / ds_df['Target'].sum() * 100):.1f}%")

print(f"\n🏆 TOP PERFORMERS:")
top_5 = df.nlargest(5, 'Pencapaian_%')[['NAMA', 'ROLE', 'Sales', 'Target', 'Pencapaian_%']]
for _, row in top_5.iterrows():
    print(f"   • {row['NAMA']} ({row['ROLE']}): {row['Pencapaian_%']:.0f}% ({row['Sales']}/{row['Target']})")

print(f"\n⚠️  BOTTOM PERFORMERS:")
bottom_5 = df.nsmallest(5, 'Pencapaian_%')[['NAMA', 'ROLE', 'Sales', 'Target', 'Pencapaian_%']]
for _, row in bottom_5.iterrows():
    print(f"   • {row['NAMA']} ({row['ROLE']}): {row['Pencapaian_%']:.0f}% ({row['Sales']}/{row['Target']})")

print(f"\n📈 DISTRIBUSI KINERJA:")
for kategori in performance_labels:
    count = len(df[df['Kategori'] == kategori])
    print(f"   • {kategori}: {count} orang")

# Analisis kontribusi sales
print(f"\n💰 KONTRIBUSI SALES:")
top_performers = df.nlargest(5, 'Sales')[['NAMA', 'Sales', 'Pencapaian_%']]
total_top_sales = top_performers['Sales'].sum()
print(f"   Top 5 performers berkontribusi {total_top_sales} dari {total_sales} sales ({total_top_sales/total_sales*100:.1f}%)")

# Analisis outstanding performers
print(f"\n⭐ OUTSTANDING PERFORMERS:")
excellent_performers = df[df['Pencapaian_%'] >= 100][['NAMA', 'Sales', 'Pencapaian_%']]
for _, row in excellent_performers.iterrows():
    print(f"   • {row['NAMA']}: {row['Pencapaian_%']:.0f}% ({row['Sales']}/25)")

print(f"\n🚨 MASALAH KRITIS:")
critical_performers = df[df['Sales'] <= 4]
print(f"   {len(critical_performers)} orang dengan ≤4 sales: {', '.join(critical_performers['NAMA'].tolist())}")

print(f"\n💡 REKOMENDASI UNTUK CILACAP:")
print("   1. 🌟 EXCELLENT PERFORMERS: Linda (160%), Anggia (148%), Sarwoto (144%) - luar biasa!")
print("   2. ✅ SOLID PERFORMERS: Sherenita (112%), Aji (100%) - excellent!")
print("   3. 🚨 EMERGENCY SPV: Kedua SPV underperform (Agus 0%, Bayu 11%) - evaluasi mendalam")
print("   4. 🔄 COACHING INTENSIF: Untuk 6 DS dengan performa <50%")
print("   5. 🤝 KNOWLEDGE SHARING: Linda, Anggia, Sarwoto bisa jadi mentor untuk tim")
print("   6. 🎯 FOKUS IMPROVEMENT: Pada mid performers (56-80%) yang hampir target")
print("   7. 📊 TIM BERPOLARISASI: 5 excellent vs 9 underperform - butuh balance strategy")
print("   8. 🏆 REWARD SYSTEM: Berikan apresiasi khusus untuk top performers")

print("=" * 70)

# Analisis detail performa
print("\n" + "=" * 50)
print("ANALISIS DETAIL PERFORMA CILACAP")
print("=" * 50)

# Analisis polarisasi
high_performers = df[df['Pencapaian_%'] >= 100]
low_performers = df[df['Pencapaian_%'] < 50]

print(f"🔍 POLARISASI TIM:")
print(f"   • High Performers (≥100%): {len(high_performers)} orang")
print(f"   • Low Performers (<50%): {len(low_performers)} orang")
print(f"   • Gap terbesar: {df['Pencapaian_%'].max() - df['Pencapaian_%'].min():.0f}%")

print(f"\n🎯 PERFORMANCE BREAKTHROUGH:")
print(f"   • LINDA PANGESTIKA: 160% (40/25) - LEGENDARY!")
print(f"   • ANGGIA IKMA DEWI: 148% (37/25) - OUTSTANDING!")
print(f"   • SARWOTO: 144% (36/25) - EXCELLENT!")
print(f"   • SHERENITA TRIAS YULIANA: 112% (28/25) - GREAT!")
print(f"   • AJI PRAYOGA: 100% (25/25) - PERFECT!")
print(f"   • LUKIS RUCIRA ARUNDATI: 80% (20/25) - BAIK")
print(f"   • HENDRI LISTIONO: 56% (14/25) - PERLU IMPROVEMENT")
print(f"   • DWIKI DARMAYUDA: 36% (9/25) - PERLU COACHING")
print(f"   • RIZKI WINDU SANCOYO: 48% (12/25) - PERLU COACHING")
print(f"   • PUPUT FARIDA: 24% (6/25) - PERLU INTERVENSI")
print(f"   • AWALIAH ZULFA TURROHMAH: 24% (6/25) - PERLU INTERVENSI")
print(f"   • DWI JAYANTI LESTARI: 16% (4/25) - EMERGENCY")
print(f"   • AGUS WIDODO (SPV): 0% (0/35) - EVALUASI MENDALAM")
print(f"   • BAYU PAMBUDI (SPV): 11% (4/35) - EVALUASI MENDALAM")

print(f"\n📊 POTENSI TIM CILACAP:")
print("   • Memiliki 5 superstar performers")
print("   • 2 anggota menunjukkan performa baik")
print("   • 7 anggota membutuhkan perhatian khusus")
print("   • Dengan perbaikan SPV dan coaching, tim bisa >80%")