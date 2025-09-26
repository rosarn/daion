import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style seaborn
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# Data input
data = {
    'NO': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
    'NAMA': [
        'Santoso Nainggolan', 'Daniel Parlindungan', 'Santo Yahya Purba', 
        'Ibbe Arfiah Ambarita', 'Ninton Silitonga', 'Irwan Panjaitan',
        'Ignatius Romy Setyawan', 'Rokhyati BT Wain', 'Hendrik Pandapotan',
        'Juwisri Mariati Simanjuntak', 'Lely Meyana', 'Daniel Toni Sagala',
        'Bastian Ronaldo Butar Butar', 'Maryanti Manalu', 'Fadli Syawalludin',
        'Dimposma Hutagalung', 'Leo Hermansyah', 'Alvin Jon Raya S',
        'Julietta Winar Pasha', 'Hinando Praya Saragih', 'Suriati T.Situmeang',
        'Rani Martina Samosir', 'Bruno Mario', 'Moh Marifan Delavena',
        'Indrah Septian', 'Irwanto'
    ],
    'ROLE': ['SPV', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'SPV', 'S2', 'S2', 'S2', 
             'S2', 'S2', 'S2', 'SPV', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'SPV', 'S2', 'S2', 'S2'],
    'Grade': [35, 25, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25],
    'Target': [35, 25, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25],
    'Sales': [7, 24, 24, 17, 7, 26, 18, 0, 14, 30, 25, 21, 17, 15, 10, 3, 17, 24, 13, 22, 16, 15, 1, 1, 1, 2],
    'Minus/plus': [-28, -1, -1, -8, -18, 1, -7, -25, -21, 5, 0, -4, -8, -10, -15, -32, -8, -1, -12, -3, -9, -10, -34, -24, -24, -23],
    '%': [20, 96, 96, 68, 28, 104, 72, 0, 40, 120, 100, 84, 68, 60, 40, 9, 68, 96, 52, 88, 64, 60, 3, 4, 4, 8]
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
fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('ANALISIS PENCAPAIAN SALES TEAM Periode: 21 Juli - 20 Agustus', 
             fontsize=12, fontweight='bold')

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
    axes[0, 1].text(i, v + 3, f'{v:.1f}%', ha='center', fontweight='bold')

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
    axes[1, 1].text(i - width/2, target + 5, f'{target}', ha='center', fontweight='bold')
    axes[1, 1].text(i + width/2, sales + 5, f'{sales}', ha='center', fontweight='bold')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# Print summary yang lebih jelas
print("=" * 70)
print("ANALISIS PENCAPAIAN SALES TEAM")
print("Periode: 21 Juli - 20 Agustus")
print("=" * 70)

print(f"\n📊 SUMMARY KESELURUHAN:")
print(f"   Total Target: {total_target}")
print(f"   Total Sales: {total_sales}")
print(f"   Pencapaian Tim: {overall_percentage:.1f}%")
print(f"   Jumlah Personil: {len(df)} orang")

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

print(f"\n💡 REKOMENDASI:")
print("   1. Evaluasi kinerja SPV yang sangat rendah (rata-rata 18%)")
print("   2. Coaching intensif untuk 10 sales dengan pencapaian <50%")
print("   3. Pelajari strategi dari top performers (Juwisri, Irwan, Lely) dengan pencapaian excellent")
print("   4. Implementasi mentoring program: top performers membantu lower performers")
print("   5. Review target untuk memastikan realistis dan achievable")
print("   6. Pertimbangkan reward system untuk top performers sebagai motivasi")
print("   7. Perhatian khusus untuk 4 sales dengan pencapaian <10%")

print("=" * 70)