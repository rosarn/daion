# 📊 Sales Performance Analytics Dashboard (Modular Monorepo)

Dashboard analisis performa sales berbasis **Streamlit**, hasil refactor dari file monolitik `satu.py` menjadi arsitektur modular yang rapi dan scalable.  
⚠️ **Tidak ada logic yang diubah** — hanya dipindah ke file terstruktur.

---

## 🚀 Features
- Upload & auto-clean data
- Auto detect periode dari nama file
- KPI Dashboard (Achievement, Avg Perf, Risk, Zero Sales)
- Top & Bottom Performer
- Heatmap, Bubble Map, Folium Map
- Multi-language (Indonesia & English)
- Executive Recommendations
- Data viewer + sort + filter + export
- Sangat modular (UI/Data/Analytics/Maps/Language)

---

## 📁 Project Structure

```
analyst/
├── main.py
└── src/
    ├── ui/
    │   ├── styles.py
    │   ├── header.py
    │   ├── sidebar.py
    │   └── tabs.py
    ├── data/
    │   └── data_processor.py
    ├── analytics/
    │   └── metrics.py
    ├── maps/
    │   └── maps.py
    ├── language/
    │   └── language_config.py
    └── utils/
        └── utils.py
├── backend
├── .venv
├── __pycache__
├── excel
├── csv
├── satu.py
├── style_dataframe.py
├── test.py
├── uv.lock
├── requirements.txt
└── README.md
```

---

## ▶️ Cara Menjalankan

### Install dependensi
```
pip install -r requirements.txt
```

### Run aplikasi
```
streamlit run main.py
```

Dashboard akan otomatis terbuka di browser dan **hasilnya 100% sama dengan `satu.py`**.

---

## 🔧 Modules Description

### `src/ui/`
- **styles.py** → CSS injection (copas dari satu.py)
- **header.py** → Judul & layout header
- **sidebar.py** → Upload, filter, periode
- **tabs.py** → Semua tab: Overview, Map, Table, Performers, Recommendation

### `src/data/`
- **data_processor.py** → process file upload, load sample, extract periode

### `src/analytics/`
- **metrics.py** → KPI, area stats, grade stats

### `src/maps/`
- **maps.py** → Folium map, heatmap, bubble map

### `src/language/`
- **language_config.py** → dictionary bahasa + get_text()

### `src/utils/`
- **utils.py** → helper functions

---

## ✔️ Goals Refactor
- Membuat project tetap **identik dengan `satu.py`**
- Memudahkan maintenance
- Memudahkan scaling
- Mengurangi 1 file besar menjadi struktur modular

---

## 📄 License
Private internal use only.
