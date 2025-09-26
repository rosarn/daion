import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style seaborn
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# Data input untuk TASIKMALAYA
data = {
    'NO': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    'NAMA': [
        'BANGBANG HIMUN H, S.KOM', 'HENGKI PERMANA', 'AHMAD SYAHRIAR IRAWAN', 
        'FALHAN BASYA', 'HENDRA IRAWAN', 'DAYU GAPURA IRIANTO',
        'RAISA SITI AINIYAH', 'HENDAR SUHENDAR', 'DAVIN ALIM',
        'AGUNG DWI LAKSONO', 'ARI HIDAYAT', 'CUCU KOMARUDIN',
        'BERENT FARIZ', 'MUHAMMAD FAJAR SIDDIQ', 'ENTIS',
        'DADANG DIMYATI', 'DICKY FAUZI NURHIDAYAT', 'VERI SEPTIANA',
        'PIKI BADARUDIN', 'ACEP RIZAL'
    ],
    'ROLE': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'Grade': [35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 25],
    'Target': [35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 25],
    'Sales': [0, 61, 25, 6, 18, 3, 2, 28, 34, 31, 29, 21, 1, 25, 32, 32, 36, 25, 28, 34],
    'Minus/plus': [-35, 36, 0, -19, -7, -22, -33, 3, 9, 6, 4, -4, -34, 0, 7, 7, 11, 0, 3, 9],
    '%': [0, 244, 100, 24, 72, 12, 6, 112, 136, 124, 116, 84, 3, 100, 128, 128, 144, 100, 112, 136]
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
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
fig.suptitle('ANALISIS PENCAPAIAN SALES TEAM TASIKMALAYA\nPeriode: 21 Juli - 20 Agustus', 
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
performance_bins = [0, 50, 80, 100, 250]
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
    axes[1, 1].text(i - width/2, target + 10, f'{target}', ha='center', fontweight='bold')
    axes[1, 1].text(i + width/2, sales + 10, f'{sales}', ha='center', fontweight='bold')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# Print summary yang lebih jelas
print("=" * 80)
print("ANALISIS PENCAPAIAN SALES TEAM TASIKMALAYA")
print("Periode: 21 Juli - 20 Agustus")
print("=" * 80)

print(f"\n📊 SUMMARY KESELURUHAN:")
print(f"   Total Target: {total_target}")
print(f"   Total Sales: {total_sales}")
print(f"   Pencapaian Tim: {overall_percentage:.1f}%")
print(f"   Jumlah Personil: {len(df)} orang")
print(f"   Selisih: -{abs(df['Selisih'].sum())} (Hampir mencapai target)")

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

print(f"\n🏆 TOP 5 PERFORMERS:")
top_5 = df.nlargest(5, 'Pencapaian_%')[['NAMA', 'ROLE', 'Sales', 'Target', 'Pencapaian_%']]
for _, row in top_5.iterrows():
    print(f"   • {row['NAMA']} ({row['ROLE']}): {row['Pencapaian_%']:.0f}% ({row['Sales']}/{row['Target']})")

print(f"\n⚠️  BOTTOM 5 PERFORMERS:")
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
print(f"\n⭐ OUTSTANDING PERFORMERS (≥100%):")
excellent_performers = df[df['Pencapaian_%'] >= 100]
print(f"   {len(excellent_performers)} orang dengan pencapaian excellent:")
for _, row in excellent_performers.iterrows():
    print(f"     • {row['NAMA']}: {row['Pencapaian_%']:.0f}% ({row['Sales']}/25)")

print(f"\n🚨 MASALAH SERIUS:")
critical_performers = df[df['Sales'] <= 3]
print(f"   {len(critical_performers)} orang dengan ≤3 sales: {', '.join(critical_performers['NAMA'].tolist())}")

print(f"\n💡 REKOMENDASI UNTUK TASIKMALAYA:")
print("   1. 🎉 TIM EXCELLENT! 96% pencapaian - hampir perfect!")
print("   2. 🌟 HENGKI PERMANA: Legendary 244% (61/25) - exceptional performance!")
print("   3. ⭐ 12 EXCELLENT PERFORMERS: Tim memiliki banyak stars")
print("   4. ⚠️  EVALUASI SPV: Ketiga SPV underperform parah (0%, 6%, 3%)")
print("   5. 🔄 COACHING: Untuk 4 DS dengan performa <50%")
print("   6. 🤝 KNOWLEDGE SHARING: Hengki dan top performers jadi mentor")
print("   7. 🏆 REWARD SYSTEM: Berikan apresiasi khusus untuk top performers")
print("   8. 📊 FOKUS PADA LEADERSHIP: Ganti SPV yang underperform")

print("=" * 80)

# Analisis detail performa
print("\n" + "=" * 60)
print("ANALISIS DETAIL PERFORMA TASIKMALAYA")
print("=" * 60)

# Analisis polarisasi
high_performers = df[df['Pencapaian_%'] >= 100]
low_performers = df[df['Pencapaian_%'] < 50]

print(f"🔍 POLARISASI TIM:")
print(f"   • High Performers (≥100%): {len(high_performers)} orang")
print(f"   • Low Performers (<50%): {len(low_performers)} orang")
print(f"   • Gap terbesar: {df['Pencapaian_%'].max() - df['Pencapaian_%'].min():.0f}%")

print(f"\n🎯 PERFORMANCE BREAKTHROUGH:")
print(f"   • HENGKI PERMANA: 244% (61/25) - LEGENDARY!")
print(f"   • DICKY FAUZI NURHIDAYAT: 144% (36/25) - OUTSTANDING!")
print(f"   • DAVIN ALIM: 136% (34/25) - EXCELLENT!")
print(f"   • ACEP RIZAL: 136% (34/25) - EXCELLENT!")
print(f"   • AGUNG DWI LAKSONO: 124% (31/25) - EXCELLENT!")
print(f"   • ENTIS: 128% (32/25) - EXCELLENT!")
print(f"   • DADANG DIMYATI: 128% (32/25) - EXCELLENT!")
print(f"   • ARI HIDAYAT: 116% (29/25) - GREAT!")
print(f"   • HENDAR SUHENDAR: 112% (28/25) - GREAT!")
print(f"   • PIKI BADARUDIN: 112% (28/25) - GREAT!")
print(f"   • 4 orang dengan perfect 100%")

print(f"\n📊 POTENSI TIM TASIKMALAYA:")
print("   • Memiliki 12 excellent performers (60% dari tim)")
print("   • Hanya 4 anggota yang perlu improvement signifikan")
print("   • Masalah utama di level leadership (SPV)")
print("   • Dengan perbaikan SPV, tim bisa mencapai >100%")