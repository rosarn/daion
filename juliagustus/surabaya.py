import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style seaborn
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# Data input untuk SURABAYA
data = {
    'NO': [1, 2, 3, 4, 5, 6, 7],
    'NAMA': [
        'VINCENTIUS FAJAR PRISTIYOWANTO', 'AYOK SETIYAWAN', 'ACHMAD BAHAK UDIN', 
        'MOH DENDRON SEKUNDRATMO', 'NOVAN INDARTO', 'IMANDA HARYO KUSUMO',
        'GATOT TRI WIDODO'
    ],
    'ROLE': ['SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS'],
    'Grade': [35, 25, 25, 25, 25, 25, 25],
    'Target': [35, 25, 25, 25, 25, 25, 25],
    'Sales': [1, 4, 3, 4, 1, 1, 6],
    'Minus/plus': [-34, -21, -22, -21, -24, -24, -19],
    '%': [3, 16, 12, 16, 4, 4, 24]
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

# Create visualizations dengan penyesuaian untuk tim kecil
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('ANALISIS PENCAPAIAN SALES TEAM SURABAYA\nPeriode: 21 Juli - 20 Agustus', 
             fontsize=16, fontweight='bold')

# Plot 1: Performance per Individu
colors = ['orange' if role == 'SPV' else 'red' for role in df['ROLE']]  # Semua merah karena semua di bawah 50%
bars = axes[0, 0].barh(df['NAMA'], df['Pencapaian_%'], color=colors)
axes[0, 0].axvline(x=100, color='blue', linestyle='--', alpha=0.7, label='Target 100%')
axes[0, 0].axvline(x=50, color='orange', linestyle='--', alpha=0.7, label='Benchmark 50%')
axes[0, 0].set_xlabel('Pencapaian (%)')
axes[0, 0].set_title('Pencapaian per Individu\n(Orange: SPV, Red: Semua di bawah target)')
axes[0, 0].legend()

# Plot 2: Rata-rata Pencapaian per Role
role_avg = df.groupby('ROLE')['Pencapaian_%'].mean().reset_index()
colors_role = ['orange', 'red']
bars = axes[0, 1].bar(role_avg['ROLE'], role_avg['Pencapaian_%'], color=colors_role)
axes[0, 1].set_title('Rata-rata Pencapaian Berdasarkan Role')
axes[0, 1].set_ylabel('Pencapaian (%)')
axes[0, 1].set_xlabel('Role')
for i, v in enumerate(role_avg['Pencapaian_%']):
    axes[0, 1].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')

# Plot 3: Distribusi Pencapaian
performance_bins = [0, 10, 20, 30, 100]
performance_labels = ['Sangat Rendah (<10%)', 'Rendah (10-19%)', 'Sedang (20-29%)', 'Target (≥30%)']
df['Kategori'] = pd.cut(df['Pencapaian_%'], bins=performance_bins, labels=performance_labels)

# Hitung jumlah per kategori
kategori_count = df['Kategori'].value_counts().reindex(performance_labels)

colors_kategori = ['darkred', 'red', 'orange', 'green']
bars = axes[1, 0].bar(kategori_count.index, kategori_count.values, color=colors_kategori)
axes[1, 0].set_title('Distribusi Kinerja Tim')
axes[1, 0].set_ylabel('Jumlah Sales')
axes[1, 0].tick_params(axis='x', rotation=45)
for i, v in enumerate(kategori_count.values):
    axes[1, 0].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

# Plot 4: Perbandingan Target vs Actual per Individu
x = np.arange(len(df))
width = 0.35

bars1 = axes[1, 1].bar(x - width/2, df['Target'], width, 
                      label='Target', color='lightblue', alpha=0.7)
bars2 = axes[1, 1].bar(x + width/2, df['Sales'], width, 
                      label='Actual Sales', color=colors, alpha=0.7)

axes[1, 1].set_title('Perbandingan Target vs Actual Sales per Individu')
axes[1, 1].set_ylabel('Nilai')
axes[1, 1].set_xlabel('Salesperson')
axes[1, 1].set_xticks(x)
axes[1, 1].set_xticklabels(df['NAMA'], rotation=45, ha='right')
axes[1, 1].legend()

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# Print summary yang lebih jelas
print("=" * 80)
print("ANALISIS PENCAPAIAN SALES TEAM SURABAYA")
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
print(f"   Tidak ada yang mencapai bahkan 30% dari target! ❌")

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

print(f"\n📈 DISTRIBUSI KINERJA:")
for kategori in performance_labels:
    count = len(df[df['Kategori'] == kategori])
    print(f"   • {kategori}: {count} orang")

# Analisis masalah serius
critical_performers = df[df['Sales'] <= 1]
low_performers = df[df['Sales'] <= 4]
print(f"\n🚨 MASALAH SANGAT KRITIS:")
print(f"   • {len(critical_performers)} orang dengan ≤1 sales: {', '.join(critical_performers['NAMA'].tolist())}")
print(f"   • {len(low_performers)} orang dengan ≤4 sales: {len(low_performers)} dari {len(df)} anggota")

print(f"\n💡 REKOMENDASI DARURAT UNTUK SURABAYA:")
print("   1. 🚨 EMERGENCY INTERVENTION: Tim dalam kondisi sangat kritis (11% pencapaian)")
print("   2. ⚠️  EVALUASI SPV: Vincentius dengan 3% - gagal total sebagai leader")
print("   3. 🆘 CRITICAL CASES: 3 orang dengan hanya 1 sales (Novan, Imanda, Vincentius)")
print("   4. 🔄 BASIC TRAINING ULANG: Sales fundamental training untuk seluruh tim")
print("   5. 📊 RESET TARGET TOTAL: Target 25 tidak realistic, mulai dari dasar")
print("   6. 🤝 MENTORING EXTENSIF: Butuh bantuan dari tim successful terdekat")
print("   7. 👥 RESTRUKTURISASI MENYELURUH: Pertimbangkan rebuild tim dari nol")
print("   8. 📈 DAILY SUPERVISION INTENSIF: Monitoring ketat setiap hari")

print("=" * 80)

# Analisis detail performa
print("\n" + "=" * 60)
print("ANALISIS DETAIL PERFORMA SURABAYA")
print("=" * 60)

print(f"🔍 DETAIL KRITIS:")
print(f"   • Rata-rata sales per orang: {total_sales/len(df):.1f}")
print(f"   • Sales tertinggi: {df['Sales'].max()} (Gatot Tri Widodo)")
print(f"   • Sales terendah: {df['Sales'].min()} (3 orang dengan 1 sales)")
print(f"   • Gap performa: {df['Pencapaian_%'].max() - df['Pencapaian_%'].min():.0f}%")

print(f"\n🎯 PERFORMANCE BREAKDOWN:")
print(f"   • GATOT TRI WIDODO: 24% (6/25) - 'Terbaik' secara relatif")
print(f"   • AYOK SETIYAWAN: 16% (4/25)")
print(f"   • MOH DENDRON SEKUNDRATMO: 16% (4/25)")
print(f"   • ACHMAD BAHAK UDIN: 12% (3/25)")
print(f"   • NOVAN INDARTO: 4% (1/25) - Emergency")
print(f"   • IMANDA HARYO KUSUMO: 4% (1/25) - Emergency")
print(f"   • VINCENTIUS (SPV): 3% (1/35) - Gagal total sebagai leader")

print(f"\n📊 STATUS TIM SURABAYA:")
print("   • TIM DENGAN PERFORMANCE TERBURUK secara absolut")
print("   • Semua anggota di bawah 25% pencapaian")
print("   • 3 anggota dengan hanya 1 sales")
print("   • SPV menunjukkan leadership yang sangat buruk")
print("   • Membutuhkan intervensi darurat dan restrukturisasi total")