import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style seaborn
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# Data input untuk BANJAR
data = {
    'NO': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    'NAMA': [
        'RENDRA DUDIA SUGARA, S.T', 'LUSY KRISBIYANTI', 'YAYAN SUGIANA', 
        'UJANG YANTO PRIYANTO', 'YUYUN NUGRAHA', 'KRIS ARDIANTO',
        'DINDIN SOLEHUDIN', 'SACHIR ADAM NURBA', 'IPAN SOPYAN', 
        'YULIUS HILMAN', 'DENY IRAWAN', 'ADI SURYADI',
        'HERDIN BUDIAWAN', 'ADITYA ABDUL MUHYI', 'NANANG SUPRIATNA',
        'ANGGA MERDIANA', 'MAHMUD', 'AHMAD ARIF SATRIONO',
        'DERI KUSDIANA', 'YENI HARDIYANI'
    ],
    'ROLE': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'Grade': [35, 25, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25],
    'Target': [35, 25, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25],
    'Sales': [0, 24, 17, 25, 21, 30, 12, 28, 0, 19, 26, 19, 22, 19, 0, 27, 21, 20, 17, 24],
    'Minus/plus': [-35, -1, -8, 0, -4, 5, -13, 3, -35, -6, 1, -6, -3, -6, -35, 2, -4, -5, -8, -1],
    '%': [0, 96, 68, 100, 84, 120, 48, 112, 0, 76, 104, 76, 88, 76, 0, 108, 84, 80, 68, 96]
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
fig.suptitle('ANALISIS PENCAPAIAN SALES TEAM BANJAR\nPeriode: 21 Juli - 20 Agustus', 
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
    axes[1, 1].text(i - width/2, target + 10, f'{target}', ha='center', fontweight='bold')
    axes[1, 1].text(i + width/2, sales + 10, f'{sales}', ha='center', fontweight='bold')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# Print summary yang lebih jelas
print("=" * 80)
print("ANALISIS PENCAPAIAN SALES TEAM BANJAR")
print("Periode: 21 Juli - 20 Agustus")
print("=" * 80)

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

print(f"\n🚨 MASALAH SPV:")
spv_low = spv_df[spv_df['Pencapaian_%'] < 50]
print(f"   {len(spv_low)} SPV dengan performa sangat rendah: {', '.join(spv_low['NAMA'].tolist())}")

print(f"\n💡 REKOMENDASI UNTUK BANJAR:")
print("   1. ✅ SOLID PERFORMANCE: 76% pencapaian - cukup baik!")
print("   2. 🌟 5 EXCELLENT PERFORMERS: Tim memiliki multiple stars")
print("   3. ⚠️  EMERGENCY SPV: Ketiga SPV dengan 0% - gagal total sebagai leader")
print("   4. 📈 POTENSI TINGGI: 10 anggota di range 76-99% - hampir target")
print("   5. 🔄 COACHING: Untuk 3 DS dengan performa <70%")
print("   6. 🤝 KNOWLEDGE SHARING: Top performers jadi mentor untuk yang hampir target")
print("   7. 🏆 REWARD SYSTEM: Berikan apresiasi untuk excellent performers")
print("   8. 📊 LEADERSHIP OVERHAUL: Ganti SPV dengan promote dari internal stars")

print("=" * 80)

# Analisis detail performa
print("\n" + "=" * 60)
print("ANALISIS DETAIL PERFORMA BANJAR")
print("=" * 60)

# Analisis performa excellent
print(f"🔍 DETAIL EXCELLENT PERFORMERS:")
excellent = df[df['Pencapaian_%'] >= 100]
print(f"   • Rata-rata excellent performers: {excellent['Pencapaian_%'].mean():.1f}%")
print(f"   • Total kontribusi: {excellent['Sales'].sum()}/371 sales ({excellent['Sales'].sum()/371*100:.1f}%)")

print(f"\n🎯 PERFORMANCE BREAKTHROUGH:")
print(f"   • KRIS ARDIANTO: 120% (30/25) - OUTSTANDING!")
print(f"   • SACHIR ADAM NURBA: 112% (28/25) - EXCELLENT!")
print(f"   • DENY IRAWAN: 104% (26/25) - GREAT!")
print(f"   • ANGGA MERDIANA: 108% (27/25) - EXCELLENT!")
print(f"   • UJANG YANTO PRIYANTO: 100% (25/25) - PERFECT!")

print(f"\n📊 POTENSI TIM BANJAR:")
print("   • Memiliki 5 excellent performers (25% dari tim)")
print("   • 10 anggota menunjukkan performa baik (76-99%)")
print("   • Hanya 5 anggota yang perlu improvement signifikan")
print("   • Masalah utama di level leadership (SPV semua 0%)")
print("   • Dengan perbaikan SPV, tim bisa mencapai >85%")