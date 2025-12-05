import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ============================================================
#   MASTER KOORDINAT KOTA INDONESIA — LENGKAP & AKURAT
# ============================================================

def get_indonesia_coordinates(area_name):
    area_lower = area_name.lower().strip()

    # ============================
    #  PETA PROVINSI / PULAU
    # ============================
    coordinates_by_island = {

        # =======================
        #        JAWA
        # =======================
        'JAWA': {
            # DKI Jakarta
            'Jakarta': {'lat': -6.2088, 'lon': 106.8456},
            'Jakarta Pusat': {'lat': -6.1821, 'lon': 106.8415},
            'Jakarta Utara': {'lat': -6.1380, 'lon': 106.8823},
            'Jakarta Barat': {'lat': -6.1767, 'lon': 106.7559},
            'Jakarta Selatan': {'lat': -6.2660, 'lon': 106.8133},
            'Jakarta Timur': {'lat': -6.2250, 'lon': 106.9000},

            # Jawa Barat
            'Bandung': {'lat': -6.9175, 'lon': 107.6191},
            'Bekasi': {'lat': -6.2349, 'lon': 106.9920},
            'Depok': {'lat': -6.4025, 'lon': 106.7942},
            'Bogor': {'lat': -6.5944, 'lon': 106.7892},
            'Cirebon': {'lat': -6.7320, 'lon': 108.5523},
            'Sukabumi': {'lat': -6.9270, 'lon': 106.9310},
            'Tasikmalaya': {'lat': -7.3274, 'lon': 108.2207},
            'Banjar': {'lat': -7.1955, 'lon': 108.5346},
            'Garut': {'lat': -7.2279, 'lon': 107.9087},
            'Subang': {'lat': -6.5750, 'lon': 107.7576},
            'Karawang': {'lat': -6.3050, 'lon': 107.3050},
            'Cimahi': {'lat': -6.8722, 'lon': 107.5422},
            'Purwakarta': {'lat': -6.5569, 'lon': 107.4434},
            'Indramayu': {'lat': -6.3364, 'lon': 108.3250},

            # Jawa Tengah
            'Semarang': {'lat': -6.9667, 'lon': 110.4167},
            'Solo': {'lat': -7.5666, 'lon': 110.8167},
            'Surakarta': {'lat': -7.5666, 'lon': 110.8167},
            'Tegal': {'lat': -6.8698, 'lon': 109.1256},
            'Brebes': {'lat': -6.8783, 'lon': 109.0484},
            'Cilacap': {'lat': -7.7325, 'lon': 109.0139},
            'Magelang': {'lat': -7.4705, 'lon': 110.2170},
            'Kudus': {'lat': -6.8041, 'lon': 110.8405},
            'Pekalongan': {'lat': -6.8898, 'lon': 109.6753},

            # Jawa Timur
            'Surabaya': {'lat': -7.2575, 'lon': 112.7521},
            'Malang': {'lat': -7.9666, 'lon': 112.6326},
            'Sidoarjo': {'lat': -7.4469, 'lon': 112.7183},
            'Gresik': {'lat': -7.1630, 'lon': 112.6550},
            'Madiun': {'lat': -7.6297, 'lon': 111.5130},
            'Kediri': {'lat': -7.8480, 'lon': 112.0178},
            'Jember': {'lat': -8.1724, 'lon': 113.7000},
            'Banyuwangi': {'lat': -8.2196, 'lon': 114.3695},

            # DIY
            'Yogyakarta': {'lat': -7.7956, 'lon': 110.3695},

            # Banten
            'Tangerang': {'lat': -6.1783, 'lon': 106.6319},
            'Tangerang Selatan': {'lat': -6.2886, 'lon': 106.7176},
            'Serang': {'lat': -6.1120, 'lon': 106.1503},
            'Cilegon': {'lat': -6.0023, 'lon': 106.0113},
        },

        # =======================
        #      SUMATERA
        # =======================
        'SUMATERA': {
            'Medan': {'lat': 3.5952, 'lon': 98.6722},
            'Pekanbaru': {'lat': 0.5071, 'lon': 101.4478},
            'Padang': {'lat': -0.9492, 'lon': 100.3543},
            'Palembang': {'lat': -2.9761, 'lon': 104.7754},
            'Jambi': {'lat': -1.6101, 'lon': 103.6131},
            'Banda Aceh': {'lat': 5.5483, 'lon': 95.3238},
            'Batam': {'lat': 1.0456, 'lon': 104.0305},
            'Tanjungpinang': {'lat': 0.9181, 'lon': 104.4586},
            'Lampung': {'lat': -5.4500, 'lon': 105.2667},
            'Bandar Lampung': {'lat': -5.4500, 'lon': 105.2667}
        },

        # =======================
        #   KALIMANTAN
        # =======================
        'KALIMANTAN': {
            'Balikpapan': {'lat': -1.2680, 'lon': 116.8283},
            'Banjarmasin': {'lat': -3.3186, 'lon': 114.5944},
            'Pontianak': {'lat': -0.0374, 'lon': 109.3441},
            'Samarinda': {'lat': -0.5022, 'lon': 117.1536},
            'Tarakan': {'lat': 3.3270, 'lon': 117.5785},
        },

        # =======================
        #    SULAWESI
        # =======================
        'SULAWESI': {
            'Makassar': {'lat': -5.1477, 'lon': 119.4327},
            'Manado': {'lat': 1.4748, 'lon': 124.8421},
            'Palu': {'lat': -0.9000, 'lon': 119.8700},
            'Kendari': {'lat': -3.9670, 'lon': 122.5947},
            'Gorontalo': {'lat': 0.5400, 'lon': 123.0600},
        },

        # =======================
        #   BALI – NUSA TENGGARA
        # =======================
        'BALI_NUSA_TENGGARA': {
            'Denpasar': {'lat': -8.6705, 'lon': 115.2126},
            'Bali': {'lat': -8.4095, 'lon': 115.1889},
            'Mataram': {'lat': -8.5833, 'lon': 116.1167},
            'Kupang': {'lat': -10.1772, 'lon': 123.6070},
            'Lombok': {'lat': -8.6500, 'lon': 116.3249},
        },

        # =======================
        #     MALUKU – PAPUA
        # =======================
        'MALUKU_PAPUA': {
            'Ambon': {'lat': -3.6954, 'lon': 128.1814},
            'Jayapura': {'lat': -2.5333, 'lon': 140.7167},
            'Sorong': {'lat': -0.8762, 'lon': 131.2558},
            'Manokwari': {'lat': -0.8615, 'lon': 134.0620},
            'Ternate': {'lat': 0.7900, 'lon': 127.3800},
        }
    }

    # =====================================================
    #  ABBREVIATION MAP (biar "tng" → Tangerang)
    # =====================================================
    abbrev_map = {
        # Jawa Barat / Banten
        'tgr': ('Tangerang', 'JAWA'),
        'tng': ('Tangerang', 'JAWA'),
        'tngsel': ('Tangerang Selatan', 'JAWA'),
        'bdg': ('Bandung', 'JAWA'),
        'bgr': ('Bogor', 'JAWA'),
        'dpk': ('Depok', 'JAWA'),
        'tsm': ('Tasikmalaya', 'JAWA'),
        'cmi': ('Cimahi', 'JAWA'),
        'cjr': ('Cirebon', 'JAWA'),

        # Jawa Tengah
        'slo': ('Solo', 'JAWA'),
        'skt': ('Surakarta', 'JAWA'),

        # Jawa Timur
        'sby': ('Surabaya', 'JAWA'),
        'mlg': ('Malang', 'JAWA'),

        # Sumatera
        'mdn': ('Medan', 'SUMATERA'),
        'pku': ('Pekanbaru', 'SUMATERA'),
        'plg': ('Palembang', 'SUMATERA'),

        # Kalimantan
        'bjm': ('Banjarmasin', 'KALIMANTAN'),
        'bpn': ('Balikpapan', 'KALIMANTAN'),
        'smr': ('Samarinda', 'KALIMANTAN'),

        # Sulawesi
        'mks': ('Makassar', 'SULAWESI'),
        'mnd': ('Manado', 'SULAWESI'),

        # Bali
        'dps': ('Denpasar', 'BALI_NUSA_TENGGARA'),
    }

    # =====================================
    #   PENCARIAN 1 — Abbreviation
    # =====================================
    for abbr, (full_name, island) in abbrev_map.items():
        if abbr in area_lower:
            return coordinates_by_island[island][full_name]

    # =====================================
    #   PENCARIAN 2 — Exact Match
    # =====================================
    for island, cities in coordinates_by_island.items():
        for city, coords in cities.items():
            if area_lower == city.lower():
                return coords

    # =====================================
    #   PENCARIAN 3 — Partial Match
    # =====================================
    for island, cities in coordinates_by_island.items():
        for city, coords in cities.items():
            if city.lower() in area_lower:
                return coords

    # =====================================
    #   PENCARIAN 4 — Pulau (Fallback)
    # =====================================
    island_keywords = {
        'JAWA': ['jawa', 'jabar', 'jateng', 'jatim', 'bandung', 'jakarta'],
        'SUMATERA': ['sumatera', 'aceh', 'padang', 'palembang'],
        'KALIMANTAN': ['kalimantan', 'banjar', 'balikpapan'],
        'SULAWESI': ['sulawesi'],
        'BALI_NUSA_TENGGARA': ['bali', 'lombok', 'kupang', 'ntb', 'ntt'],
        'MALUKU_PAPUA': ['papua', 'maluku', 'ambon']
    }

    for island, keywords in island_keywords.items():
        if any(keyword in area_lower for keyword in keywords):
            island_centers = {
                'JAWA': {'lat': -7.5, 'lon': 110.0},
                'SUMATERA': {'lat': 0.0, 'lon': 101.0},
                'KALIMANTAN': {'lat': -2.0, 'lon': 114.0},
                'SULAWESI': {'lat': -2.5, 'lon': 121.0},
                'BALI_NUSA_TENGGARA': {'lat': -8.5, 'lon': 116.5},
                'MALUKU_PAPUA': {'lat': -4.0, 'lon': 138.0},
            }
            return island_centers[island]

    # FINAL fallback — Indonesia Center
    return {'lat': -2.5489, 'lon': 118.0149}



# ============================================================
#  GENERATE FOLIUM MAP
# ============================================================
def create_performance_map(df):
    if df.empty:
        return folium.Map(location=[-2.5489, 118.0149], zoom_start=4)

    area_stats = df.groupby('Area').agg({
        'Percentage': 'mean',
        'Sales': 'sum',
        'Target': 'sum',
        'Nama': 'count'
    }).round(2)

    performance_map = folium.Map(
        location=[-2.5489, 118.0149],
        zoom_start=5,
        tiles='cartodbpositron'
    )

    for area in area_stats.index:
        avg_performance = area_stats.loc[area, 'Percentage']
        total_sales = area_stats.loc[area, 'Sales']
        team_size = area_stats.loc[area, 'Nama']

        coords = get_indonesia_coordinates(area)

        # Color
        if avg_performance >= 120:
            color = 'green'
        elif avg_performance >= 100:
            color = 'lightgreen'
        elif avg_performance >= 80:
            color = 'orange'
        else:
            color = 'red'

        folium.CircleMarker(
            radius=10,
            location=[coords['lat'], coords['lon']],
            color=color,
            fill=True,
            fill_color=color,
            popup=f"{area} — {avg_performance:.1f}%"
        ).add_to(performance_map)

    folium.LayerControl().add_to(performance_map)
    return performance_map


# ============================================================
#  HEATMAP DATA
# ============================================================
def create_heatmap_data(df):
    if df.empty:
        return pd.DataFrame()

    area_stats = df.groupby('Area').agg({
        'Percentage': 'mean',
        'Sales': 'sum',
        'Nama': 'count'
    }).round(2)

    records = []
    for area in area_stats.index:
        coords = get_indonesia_coordinates(area)
        records.append({
            'Area': area,
            'lat': coords['lat'],
            'lon': coords['lon'],
            'Percentage': area_stats.loc[area, 'Percentage'],
            'Sales': area_stats.loc[area, 'Sales'],
            'Nama': int(area_stats.loc[area, 'Nama'])
        })

    return pd.DataFrame(records)


# ============================================================
#  BUBBLE MAP
# ============================================================
def create_bubble_map_figure(area_data):
    if area_data.empty:
        fig = go.Figure()
        fig.update_layout(title="No data available")
        return fig

    fig = px.scatter_mapbox(
        area_data,
        lat="lat",
        lon="lon",
        size="Nama",
        color="Percentage",
        hover_name="Area",
        zoom=4,
        size_max=30,
        color_continuous_scale="RdYlGn"
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={'l': 0, 'r': 0, 't': 30, 'b': 0}
    )

    return fig
