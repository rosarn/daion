import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style seaborn
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# Data input untuk KAB PANDEGLANG
data = {
    'NO': [1, 2, 3, 4, 5, 6],
    'NAMA': [
        'DEDE IRWAN SETIAWIGUNA', 'FAJAR MUBAROK', 'ULFAH MEILANI', 
        'BURHANUDIN', 'PUTRI AGUSTINA', 'NURDIN'
    ],
    'ROLE': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'Grade': [35, 25, 25, 25, 25, 25],
    'Target': [35, 25, 25, 25, 25, 25],
    'Sales': [36, 2, 25, 16, 1, 20],
    'Minus/plus': [1, -23, 0, -9, -24, -5],
    '%': [103, 8, 100, 64, 4, 80]
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
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('ANALISIS PENCAPAIAN SALES TEAM KAB PANDEGLANG\nPeriode: 21 Juli - 20 Agustus', 
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
    axes[0, 1].text(i, v + 5, f'{v:.1f}%', ha='center', fontweight='bold')

# Plot 3: Distribusi Pencapaian
performance_bins = [0, 50, 80, 100, 150]
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
    axes[1, 1].text(i - width/2, target + 2, f'{target}', ha='center', fontweight='bold')
    axes[1, 1].text(i + width/2, sales + 2, f'{sales}', ha='center', fontweight='bold')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# Print summary yang lebih jelas
print("=" * 70)
print("ANALISIS PENCAPAIAN SALES TEAM KAB PANDEGLANG")
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
top_3 = df.nlargest(3, 'Pencapaian_%')[['NAMA', 'ROLE', 'Sales', 'Target', 'Pencapaian_%']]
for _, row in top_3.iterrows():
    print(f"   • {row['NAMA']} ({row['ROLE']}): {row['Pencapaian_%']:.0f}% ({row['Sales']}/{row['Target']})")

print(f"\n⚠️  BOTTOM PERFORMERS:")
bottom_3 = df.nsmallest(3, 'Pencapaian_%')[['NAMA', 'ROLE', 'Sales', 'Target', 'Pencapaian_%']]
for _, row in bottom_3.iterrows():
    print(f"   • {row['NAMA']} ({row['ROLE']}): {row['Pencapaian_%']:.0f}% ({row['Sales']}/{row['Target']})")

print(f"\n📈 DISTRIBUSI KINERJA:")
for kategori in performance_labels:
    count = len(df[df['Kategori'] == kategori])
    print(f"   • {kategori}: {count} orang")

# Analisis kontribusi sales
print(f"\n💰 KONTRIBUSI SALES:")
top_performers = df.nlargest(3, 'Sales')[['NAMA', 'Sales', 'Pencapaian_%']]
total_top_sales = top_performers['Sales'].sum()
print(f"   Top 3 performers berkontribusi {total_top_sales} dari {total_sales} sales ({total_top_sales/total_sales*100:.1f}%)")

# Analisis masalah serius
low_performers = df[df['Sales'] <= 2]
print(f"\n🚨 MASALAH SERIUS:")
print(f"   {len(low_performers)} orang dengan ≤2 sales: {', '.join(low_performers['NAMA'].tolist())}")

print(f"\n💡 REKOMENDASI UNTUK KAB PANDEGLANG:")
print("   1. ✅ EXCELLENT SPV: Dede Irwan excellent (103%) - pertahankan!")
print("   2. ⭐ ULFAH MEILANI: Perfect 100% - berikan reward")
print("   3. 🚨 EMERGENCY COACHING: Untuk Fajar (8%) dan Putri (4%)")
print("   4. 📈 BURHANUDIN (64%) dan NURDIN (80%): Hampir target - berikan support")
print("   5. 🤝 KNOWLEDGE SHARING: Dede dan Ulfah bisa mentor untuk yang underperform")
print("   6. 🎯 FOKUS IMPROVEMENT: Pada 2 low performers yang sangat underperform")
print("   7. 📊 TIM KECIL DENGAN POTENSI: Dengan perbaikan, bisa mencapai >80%")
print("   8. 🔄 TARGET REVIEW: Untuk Fajar dan Putri, mungkin perlu target lebih realistis")

print("=" * 70)

# Analisis detail performa
print("\n" + "=" * 50)
print("ANALISIS DETAIL PERFORMA KAB PANDEGLANG")
print("=" * 50)

# Hitung performa tanpa 2 lowest performers
performance_without_lowest = df[df['Sales'] > 2]['Pencapaian_%'].mean()
print(f"Rata-rata pencapaian tanpa 2 lowest performers: {performance_without_lowest:.1f}% ✅")

# Analisis variasi performa
std_deviation = df['Pencapaian_%'].std()
print(f"Standar deviasi performa: {std_deviation:.1f}% (variasi sangat tinggi)")

print(f"\n🎯 PERFORMANCE BREAKDOWN:")
print(f"   • DEDE IRWAN (SPV): 103% (36/35) - Excellent leader")
print(f"   • ULFAH MEILANI: 100% (25/25) - Perfect achievement")
print(f"   • NURDIN: 80% (20/25) - Hampir target")
print(f"   • BURHANUDIN: 64% (16/25) - Perlu sedikit improvement")
print(f"   • FAJAR MUBAROK: 8% (2/25) - Emergency intervention needed")
print(f"   • PUTRI AGUSTINA: 4% (1/25) - Emergency intervention needed")

print(f"\n📊 POTENSI TIM KAB PANDEGLANG:")
print("   • SPV excellent sebagai panutan")
print("   • 4 dari 6 anggota menunjukkan performa baik")
print("   • Hanya 2 anggota dengan masalah serius")
print("   • Dengan perbaikan targeted, tim bisa sangat kuat")