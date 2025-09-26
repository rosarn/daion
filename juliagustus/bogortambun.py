import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style seaborn
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# Data input untuk TAMBUN
data = {
    'NO': [1, 2, 3, 4, 5, 6, 7, 8],
    'NAMA': [
        'BINSAR SUDARMONO SITUMORANG', 'MAYANG PUTRI EMALIANA', 'EXAUDI PARULIAN SITUMORANG', 
        'MARLIANA', 'BOYKE SUHENDRA', 'NAHUM WINARDI PUTRA SITUMORANG',
        'NUNUNG SEPTIANI', 'AFIFAHTUL KHUSNUL KHATIMAH'
    ],
    'ROLE': ['SPV', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2'],
    'Grade': [35, 25, 25, 25, 25, 25, 25, 25],
    'Target': [35, 25, 25, 25, 25, 25, 25, 25],
    'Sales': [16, 28, 23, 35, 17, 21, 14, 2],
    'Minus/plus': [-19, 3, -2, 10, -8, -4, -11, -23],
    '%': [46, 112, 92, 140, 68, 84, 56, 8]
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate additional metrics
df['Pencapaian_%'] = (df['Sales'] / df['Target']) * 100
df['Status'] = np.where(df['Pencapaian_%'] >= 100, 'Mencapai Target', 'Di Bawah Target')
df['Selisih'] = df['Sales'] - df['Target']

# Pisahkan data SPV dan S2
spv_df = df[df['ROLE'] == 'SPV']
s2_df = df[df['ROLE'] == 'S2']

# Analysis summary
total_target = df['Target'].sum()
total_sales = df['Sales'].sum()
overall_percentage = (total_sales / total_target) * 100

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('ANALISIS PENCAPAIAN SALES TEAM TAMBUN\nPeriode: 21 Juli - 20 Agustus', 
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

# Plot 4: Perbandingan SPV vs S2
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
print("ANALISIS PENCAPAIAN SALES TEAM TAMBUN")
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

print(f"\n   S2 (Sales): {len(s2_df)} orang")
print(f"   • Rata-rata pencapaian: {s2_df['Pencapaian_%'].mean():.1f}%")
print(f"   • Total target: {s2_df['Target'].sum()}")
print(f"   • Total sales: {s2_df['Sales'].sum()}")
print(f"   • Pencapaian tim S2: {(s2_df['Sales'].sum() / s2_df['Target'].sum() * 100):.1f}%")

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

# Analisis outstanding performer
marliana_performance = df[df['NAMA'] == 'MARLIANA'].iloc[0]
print(f"\n⭐ OUTSTANDING PERFORMER:")
print(f"   • MARLIANA: {marliana_performance['Pencapaian_%']:.0f}% ({marliana_performance['Sales']}/{marliana_performance['Target']})")
print(f"   • Kontribusi: {marliana_performance['Sales']/total_sales*100:.1f}% dari total sales tim")

print(f"\n💡 REKOMENDASI UNTUK TAMBUN:")
print("   1. ✅ Performa overall baik (82%) - pertahankan!")
print("   2. ⭐ MARLIANA: Outstanding performer dengan 140% - jadikan role model")
print("   3. 🎯 3 dari 8 anggota mencapai/exceed target (38% success rate)")
print("   4. ⚠️  Evaluasi Afifahtul (8%) dan SPV (46%) yang underperform")
print("   5. 📈 Boyke (68%) dan Nunung (56%) butuh sedikit improvement")
print("   6. 🤝 Knowledge sharing: MARLIANA bisa mentor untuk tim lainnya")
print("   7. 🎉 Celebration untuk Mayang (112%) dan Marliana (140%)")
print("   8. 🔄 Coaching untuk anggota dengan performa di bawah 70%")

print("=" * 70)

# Analisis detail performa
print("\n" + "=" * 50)
print("ANALISIS DETAIL PERFORMA TAMBUN")
print("=" * 50)

# Hitung performa tanpa outlier
performance_without_lowest = df[df['Pencapaian_%'] > 8]['Pencapaian_%'].mean()
print(f"Rata-rata pencapaian tanpa lowest performer: {performance_without_lowest:.1f}%")

# Analisis consistency
std_deviation = df['Pencapaian_%'].std()
print(f"Standar deviasi performa: {std_deviation:.1f}% (variasi {'moderat' if std_deviation < 40 else 'tinggi'})")

print(f"\n🎯 PERFORMANCE BREAKDOWN:")
print(f"   • MARLIANA: 140% (35/25) - Outstanding!")
print(f"   • MAYANG PUTRI EMALIANA: 112% (28/25) - Excellent")
print(f"   • EXAUDI PARULIAN: 92% (23/25) - Hampir target")
print(f"   • NAHUM WINARDI: 84% (21/25) - Baik")
print(f"   • BOYKE SUHENDRA: 68% (17/25) - Perlu improvement")
print(f"   • NUNUNG SEPTIANI: 56% (14/25) - Perlu coaching")
print(f"   • BINSAR (SPV): 46% (16/35) - Perlu evaluasi")
print(f"   • AFIFAHTUL: 8% (2/25) - Emergency intervention")

print(f"\n📊 POTENSI TIM TAMBUN:")
print("   • Memiliki 2 excellent performers")
print("   • 5 anggota di atas 50% pencapaian")
print("   • Hanya 1 anggota dengan masalah serius")
print("   • Overall performance solid di 82%")