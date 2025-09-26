import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Data Sales
# ==============================
data = {
    "NO": [1, 2, 3],
    "NAMA SALES": ["Sigit Fendian Oktavianto", "Widarwanto", "Ni Luh Putu Astiti Dewi"],
    "PENCAPAIAN": [92, 91, 84],
    "KOTA": ["Kendal", "Semarang", "Badung"]
}

df = pd.DataFrame(data)

# ==============================
# Urutkan berdasarkan pencapaian
# ==============================
df_sorted = df.sort_values(by="PENCAPAIAN", ascending=False).reset_index(drop=True)
df_sorted["JUARA"] = ["Juara 1", "Juara 2", "Juara 3"]

# ==============================
# Plot Grafik Batang
# ==============================
plt.figure(figsize=(8,5))
bars = plt.bar(df_sorted["JUARA"], df_sorted["PENCAPAIAN"], color=["red","blue","green"])

# Tambahkan nama sales, kota, dan nilai di atas batang
for bar, row in zip(bars, df_sorted.itertuples()):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{row._2} - {row.KOTA} ({row.PENCAPAIAN})",
             ha='center', fontsize=9)

# Judul dan label
plt.title("Best DS (Top 3 Sales)", fontsize=14)
plt.ylabel("Pencapaian")
plt.ylim(80, 100)
plt.grid(axis='y', linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
