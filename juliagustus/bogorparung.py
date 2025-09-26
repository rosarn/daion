import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style seaborn
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (14, 8)

# Data input untuk PARUNG
data = {
    'NO': [1, 2, 3, 4, 5, 6, 7],
    'NAMA': [
        'SUKMA ANJALI', 'MUHAMAD DAPA AL RASID', 'RAFLY ILHAM RAMADHAN', 
        'ABYAN ARYAN SAPUTRA', 'RATNA TUSYADIYAH', 'FRISKA OLIVIA SIHALOHO',
        'DEVI ANDRIANI'
    ],
    'ROLE': ['S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2'],
    'Grade': [25, 25, 25, 25, 25, 25, 25],
    'Target': [25, 25, 25, 25, 25, 25, 25],
    'Sales': [6, 5, 2, 1, 0, 1, 6],
    'Minus/plus': [-19, -20, -23, -24, -25, -24, -19],
    '%': [24, 20, 8, 4, 0, 4, 24]
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

# Create visualizations dengan format yang sama seperti sebelumnya
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('ANALISIS PENCAPAIAN SALES TEAM PARUNG\nPeriode: 21 Juli - 20 Agustus', 
             fontsize=16, fontweight='bold')

# Plot 1: Performance per Individu (format sama seperti tim lain)
colors = ['red' for _ in range(len(df))]  # Semua merah karena semua di bawah target
bars = axes[0, 0].barh(df['NAMA'], df['Pencapaian_%'], color=colors)
axes[0, 0].axvline(x=100, color='blue', linestyle='--', alpha=0.7, label='Target 100%')
axes[0, 0].set_xlabel('Pencapaian (%)')
axes[0, 0].set_title('Pencapaian per Individu\n(Semua anggota di bawah target)')
axes[0, 0].legend()

# Plot 2: Rata-rata Pencapaian per Role (karena hanya S2, kita buat khusus)
role_avg = df.groupby('ROLE')['Pencapaian_%'].mean().reset_index()
colors_role = ['lightblue']
bars = axes[0, 1].bar(role_avg['ROLE'], role_avg['Pencapaian_%'], color=colors_role)
axes[0, 1].set_title('Rata-rata Pencapaian Berdasarkan Role')
axes[0, 1].set_ylabel('Pencapaian (%)')
axes[0, 1].set_xlabel('Role')
for i, v in enumerate(role_avg['Pencapaian_%']):
    axes[0, 1].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')

# Plot 3: Distribusi Pencapaian (format sama)
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

# Plot 4: Perbandingan Target vs Actual (karena hanya S2, kita bandingkan dengan target ideal)
x = np.arange(1)
width = 0.35

bars1 = axes[1, 1].bar(x - width/2, total_target, width, label='Total Target', color='lightblue', alpha=0.7)
bars2 = axes[1, 1].bar(x + width/2, total_sales, width, label='Total Actual Sales', color='red', alpha=0.7)

axes[1, 1].set_title('Perbandingan Total Target vs Actual Sales')
axes[1, 1].set_ylabel('Nilai')
axes[1, 1].set_xlabel('Tim Parung')
axes[1, 1].set_xticks(x)
axes[1, 1].set_xticklabels(['PARUNG'])
axes[1, 1].legend()

# Tambahkan nilai di atas bars
axes[1, 1].text(x - width/2, total_target + 5, f'{total_target}', ha='center', fontweight='bold')
axes[1, 1].text(x + width/2, total_sales + 5, f'{total_sales}', ha='center', fontweight='bold')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# Print summary dengan format yang sama seperti tim lain
print("=" * 70)
print("ANALISIS PENCAPAIAN SALES TEAM PARUNG")
print("Periode: 21 Juli - 20 Agustus")
print("=" * 70)

print(f"\n📊 SUMMARY KESELURUHAN:")
print(f"   Total Target: {total_target}")
print(f"   Total Sales: {total_sales}")
print(f"   Pencapaian Tim: {overall_percentage:.1f}%")
print(f"   Jumlah Personil: {len(df)} orang")
print(f"   Selisih: -{abs(df['Selisih'].sum())} (Jauh di bawah target) ❌")

print(f"\n🎯 TARGET vs PENCAPAIAN:")
print(f"   Sales yang mencapai target: {len(df[df['Pencapaian_%'] >= 100])} orang")
print(f"   Sales di bawah target: {len(df[df['Pencapaian_%'] < 100])} orang")

print(f"\n👥 ANALISIS BERDASARKAN ROLE:")
print(f"\n   S2 (Sales): {len(df)} orang")
print(f"   • Rata-rata pencapaian: {df['Pencapaian_%'].mean():.1f}%")
print(f"   • Total target: {total_target}")
print(f"   • Total sales: {total_sales}")
print(f"   • Pencapaian tim: {overall_percentage:.1f}%")

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
top_performers = df.nlargest(2, 'Sales')[['NAMA', 'Sales', 'Pencapaian_%']]
total_top_sales = top_performers['Sales'].sum()
print(f"   Top 2 performers berkontribusi {total_top_sales} dari {total_sales} sales ({total_top_sales/total_sales*100:.1f}%)")

# Analisis masalah serius
zero_performers = df[df['Sales'] == 0]
print(f"\n🚨 MASALAH SERIUS:")
print(f"   {len(zero_performers)} orang dengan 0 sales: {', '.join(zero_performers['NAMA'].tolist())}")

print(f"\n💡 REKOMENDASI UNTUK PARUNG:")
print("   1. 🚨 EVALUASI MENYELURUH: Tim dalam kondisi kritis (11% pencapaian)")
print("   2. 🔄 BASIC TRAINING: Sales fundamental training untuk seluruh tim")
print("   3. 🎯 RESET TARGET: Target mungkin tidak realistic, mulai dengan target lebih rendah")
print("   4. 👥 MENTORING: Pair dengan tim successful untuk learning")
print("   5. 📊 FOKUS PADA SUKMA & DEVI: Dua orang dengan performa relatif terbaik")
print("   6. ❌ EVALUASI KINERJA: Untuk anggota dengan ≤2 sales")
print("   7. 🔍 ROOT CAUSE ANALYSIS: Cari tahu mengapa performa sangat rendah")
print("   8. 📈 DAILY MONITORING: Supervisi ketat setiap hari")

print("=" * 70)

# Analisis komparatif
print("\n" + "=" * 50)
print("ANALISIS KOMPARATIF DENGAN TIM LAIN")
print("=" * 50)

print(f"📉 PARUNG vs RATA-RATA TIM:")
print(f"   • Parung: 11% vs Rata-rata tim: ~60%")
print(f"   • Gap: ~49 percentage points")
print(f"   • Parung butuh improvement 5x lipat")

print(f"\n📊 RATA-RATA SALES PER ORANG:")
print(f"   • Parung: {total_sales/len(df):.1f} sales/orang")
print(f"   • Tim Terbaik: ~30 sales/orang")
print(f"   • Perbedaan: ~27 sales/orang")

print(f"\n🎯 REKOMENDASI PRIORITAS:")
print("   1. Set realistic target (mungkin 10-15 untuk mulai)")
print("   2. Pair dengan successful team untuk learning")
print("   3. Daily monitoring dan coaching")
print("   4. Motivational program")
print("   5. Pertimbangkan restructuring jika tidak ada improvement")