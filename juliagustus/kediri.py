import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style seaborn
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# Data input untuk KEDIRI
data = {
    'NO': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
    'NAMA': [
        'TEGUH JUNNARTO', 'NUR BUDI FEBRIANTO', 'DEWI YUNANIK', 
        'IMA PUSPITASARI', 'DIMAS RAMADHANA', 'LUSI PURWANTI',
        'KHOIRUL SULTONI', 'VIRDIAS FATKA PRATAMA', 'DWI OKTAVIANUS LANGGENG SAPUTRO',
        'ARIEF SETYAJI', 'IVON DENSI YOUS MARLINA', 'RAMADHAN VICKO RAFSANJANI',
        'IMAM FATONI', 'LUTFI HIDAYAT', 'TRI LESTARI', 'CAHYO WICAKSONO', 'DAFIT PRASETIO'
    ],
    'ROLE': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'Grade': [35, 25, 25, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 25],
    'Target': [35, 25, 25, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 25],
    'Sales': [2, 17, 16, 14, 17, 1, 5, 1, 0, 1, 17, 6, 9, 7, 7, 10, 17],
    'Minus/plus': [-33, -8, -9, -11, -8, -24, -20, -24, -25, -34, -8, -19, -16, -18, -18, -15, -8],
    '%': [6, 68, 64, 56, 68, 4, 20, 4, 0, 3, 68, 24, 36, 28, 28, 40, 68]
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
fig.suptitle('ANALISIS PENCAPAIAN SALES TEAM KEDIRI\nPeriode: 21 Juli - 20 Agustus', 
             fontsize=16, fontweight='bold')

# Plot 1: Performance per Individu
colors = ['orange' if role == 'SPV' else ('red' if perc < 50 else 'orange' if perc < 80 else 'green')
          for role, perc in zip(df['ROLE'], df['Pencapaian_%'])]
bars = axes[0, 0].barh(df['NAMA'], df['Pencapaian_%'], color=colors)
axes[0, 0].axvline(x=100, color='blue', linestyle='--', alpha=0.7, label='Target 100%')
axes[0, 0].axvline(x=50, color='orange', linestyle='--', alpha=0.7, label='Benchmark 50%')
axes[0, 0].set_xlabel('Pencapaian (%)')
axes[0, 0].set_title('Pencapaian per Individu\n(Orange: SPV, Red: <50%, Orange: 50-79%, Green: ≥80%)')
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
performance_bins = [0, 50, 80, 100]
performance_labels = ['Sangat Rendah (<50%)', 'Rendah (50-79%)', 'Baik (≥80%)']
df['Kategori'] = pd.cut(df['Pencapaian_%'], bins=performance_bins, labels=performance_labels)

# Hitung jumlah per kategori
kategori_count = df['Kategori'].value_counts().reindex(performance_labels)

colors_kategori = ['red', 'orange', 'green']
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
print("=" * 80)
print("ANALISIS PENCAPAIAN SALES TEAM KEDIRI")
print("Periode: 21 Juli - 20 Agustus")
print("=" * 80)

print(f"\n📊 SUMMARY KESELURUHAN:")
print(f"   Total Target: {total_target}")
print(f"   Total Sales: {total_sales}")
print(f"   Pencapaian Tim: {overall_percentage:.1f}%")
print(f"   Jumlah Personil: {len(df)} orang")
print(f"   Selisih: -{abs(df['Selisih'].sum())} (Sangat jauh di bawah target) ❌")

print(f"\n🎯 TARGET vs PENCAPAIAN:")
print(f"   Sales yang mencapai target: {len(df[df['Pencapaian_%'] >= 100])} orang")
print(f"   Sales di bawah target: {len(df[df['Pencapaian_%'] < 100])} orang")
print(f"   Tidak ada yang mencapai target! ❌")

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

print(f"\n🏆 RELATIVE TOP PERFORMERS:")
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

# Analisis masalah serius
critical_performers = df[df['Sales'] <= 1]
zero_performers = df[df['Sales'] == 0]
print(f"\n🚨 MASALAH KRITIS:")
print(f"   • {len(critical_performers)} orang dengan ≤1 sales")
print(f"   • {len(zero_performers)} orang dengan 0 sales: {', '.join(zero_performers['NAMA'].tolist())}")

print(f"\n💡 REKOMENDASI DARURAT UNTUK KEDIRI:")
print("   1. 🚨 EMERGENCY INTERVENTION: Tim dalam kondisi sangat kritis (35% pencapaian)")
print("   2. ⚠️  EVALUASI SPV: Kedua SPV underperform parah (Teguh 6%, Arief 3%)")
print("   3. 🆘 CRITICAL CASES: 5 orang dengan ≤1 sales membutuhkan intervensi darurat")
print("   4. 🔄 BASIC TRAINING: Sales fundamental training untuk seluruh tim")
print("   5. 📊 RESET TARGET: Target mungkin tidak realistic untuk kondisi tim")
print("   6. 🤝 MENTORING: Fokus pada 5 relative top performers sebagai foundation")
print("   7. 👥 RESTRUKTURISASI: Pertimbangkan reorganisasi tim menyeluruh")
print("   8. 📈 DAILY MONITORING: Supervisi ketat setiap hari")

print("=" * 80)

# Analisis detail performa
print("\n" + "=" * 60)
print("ANALISIS DETAIL PERFORMA KEDIRI")
print("=" * 60)

# Analisis kelompok performa
high_performers = df[df['Pencapaian_%'] >= 60]
mid_performers = df[(df['Pencapaian_%'] >= 30) & (df['Pencapaian_%'] < 60)]
low_performers = df[df['Pencapaian_%'] < 30]

print(f"🔍 KELOMPOK PERFORMA:")
print(f"   • Performa Tinggi (≥60%): {len(high_performers)} orang")
print(f"   • Performa Menengah (30-59%): {len(mid_performers)} orang")
print(f"   • Performa Rendah (<30%): {len(low_performers)} orang")

print(f"\n🎯 PERFORMANCE BREAKDOWN:")
print(f"   • Relative Best: Nur Budi, Dimas, Ivon, Dafit (masing-masing 68%)")
print(f"   • Masalah Sedang: Imam (36%), Cahyo (40%), Lutfi (28%), Tri (28%)")
print(f"   • Masalah Serius: Lusi (4%), Virdias (4%), Ramadhan (24%), Khoirul (20%)")
print(f"   • Emergency: Dwi Oktavianus (0%)")
print(f"   • SPV Gagal: Teguh (6%), Arief (3%)")

print(f"\n📊 POTENSI TIM KEDIRI:")
print("   • 5 anggota menunjukkan performa relatif baik (56-68%)")
print("   • 12 anggota membutuhkan intervensi darurat")
print("   • Leadership completely failed")
print("   • Membutuhkan turnaround strategy yang komprehensif")