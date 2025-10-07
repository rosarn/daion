import pandas as pd

# File Excel sumber
file_path = "REKAPAN PENCAPAIAN NASIONAL 21 JULI -20 AGUSTUS.xlsx"

# Baca semua sheet jadi dict
all_sheets = pd.read_excel(file_path, sheet_name=None)

# List buat simpan hasil
all_data = []

for sheet_name, df in all_sheets.items():
    df = df.copy()
    df["region"] = sheet_name  # Tambah kolom nama sheet

    # Normalisasi nama kolom (hapus spasi, uppercase)
    df.columns = df.columns.str.strip().str.upper()

    # Ubah kolom NAMA DS jadi sales_person
    if "NAMA DS" in df.columns:
        df.rename(columns={"NAMA DS": "sales_person"}, inplace=True)

    all_data.append(df)

# Gabung semua jadi satu DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Simpan ke CSV
final_df.to_csv("REKAPAN_PENCAPAIAN_ALL.csv", index=False, encoding="utf-8-sig")

print("✅ Berhasil! File REKAPAN_PENCAPAIAN_ALL.csv sudah dibuat.")
