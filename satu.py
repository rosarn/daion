"""
============================================================================
SALES PERFORMANCE ANALYTICS DASHBOARD 
============================================================================

Author: Data Analyst Team
Version: 3.0 (Enhanced with Maps & Best Practices)
Business Context: Multi-area sales performance tracking and optimization
Technical Stack: Streamlit, Plotly, Pandas, Folium
"""

# ============================================================================
# IMPORT LIBRARIES AND DEPENDENCIES
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import warnings
import io
import openpyxl  
import re
import folium
from streamlit_folium import st_folium

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION AND SETUP
# ============================================================================

st.set_page_config(
    page_title="Sales Performance Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': None,
        'About': "Sales Performance Analytics Dashboard v3.0 - With Maps Visualization"
    }
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'periode_data' not in st.session_state:
    st.session_state.periode_data = "Juli - Agustus 2024"

if 'language' not in st.session_state:
    st.session_state.language = 'indonesia'

LANGUAGES = {
    'indonesia': {
        'dashboard_title': "Dashboard Analisis Kinerja Penjualan",
        'dashboard_controls': "Kontrol Dashboard",
        'upload_data': "Unggah Data",
        'upload_help': "Unggah file dengan kolom: Area, SubArea, Nama, Grade, Target, Sales",
        'file_loaded': "File berhasil diupload",
        'data_records': "Data",
        'period_detected': "Periode terdeteksi",
        'period_config': "Konfigurasi Periode Data",
        'month_start': "Bulan Mulai",
        'month_end': "Bulan Akhir",
        'year': "Tahun",
        'update_period': "Update Periode dari Pilihan",
        'period_updated': "Periode diupdate",
        'period_display': "Periode Data",
        'data_filters': "Filter Data",
        'select_area': "Pilih Area",
        'select_grade': "Pilih Grade",
        'performance_range': "Rentang Kinerja",
        'min_achievement': "Pencapaian Minimum (%)",
        'max_achievement': "Pencapaian Maksimum (%)",
        'performance_category': "Kategori Kinerja",
        'filter_summary': "Ringkasan Filter",
        'download_template': "Download Template",
        'download_help': "Download template untuk mengisi data sales",
        'period_label': "Period",
        'enhanced_dashboard': "Enhanced Analytics Dashboard",
        'kpis': "Indikator Kinerja Utama",
        'overall_achievement': "Pencapaian Keseluruhan",
        'average_performance': "Rata-rata Kinerja",
        'top_performer': "Top Performer",
        'team_size': "Ukuran Tim",
        'needs_attention': "Perlu Perhatian",
        'overview': "Overview",
        'performers': "Performers",
        'detailed_data': "Detailed Data",
        'recommendations': "Recommendations",
        'footer_text': "Dashboard updated automatically • Data period",
        'last_updated': "Last updated",
        'search_name': "Cari berdasarkan Nama",
        'sort_by': "Urutkan berdasarkan",
        'export_format': "Format Export",
        'records_shown': "Records Shown",
        'avg_achievement': "Avg Achievement",
        'total_gap': "Total Gap",
        'group_achievement': "Group Achievement",
        'excellent_performers': "Excellent Performers",
        'good_performers': "Good Performers",
        'average_performers': "Average Performers",
        'needs_improvement': "Needs Improvement",
        'top_performers': "Top 10 Performers",
        'bottom_performers': "Bottom 10 Performers",
        'executive_summary': "Executive Summary",
        'overall_status': "Overall Status",
        'risk_level': "Risk Level",
        'quick_wins': "Quick Wins",
        'benchmarks': "Benchmarks",
        'immediate_actions': "Immediate Priority Actions",
        'area_maps': "Peta Area",
        'geographic_distribution': "Distribusi Geografis",
        'map_type': "Pilih Jenis Peta",
        'interactive_map': "Peta Interaktif",
        'heatmap': "Heatmap",
        'bubble_map': "Bubble Map",
        'map_legend': "Legenda Peta",
        'performance_color': "Kode Warna Performa",
        'bubble_size': "Ukuran Bubble",
        'map_tips': "Tips Peta",
        'area_summary': "Ringkasan Area",
        'regional_analysis': "Analisis Regional",
        'top_performing_areas': "Area Berkinerja Terbaik",
        'areas_need_attention': "Area Perlu Perhatian"
    },
    'english': {
        'dashboard_title': "Sales Performance Analytics Dashboard",
        'dashboard_controls': "Dashboard Controls",
        'upload_data': "Upload Data File",
        'upload_help': "Upload file with columns: Area, SubArea, Nama, Grade, Target, Sales",
        'file_loaded': "File successfully uploaded",
        'data_records': "Data",
        'period_detected': "Period detected",
        'period_config': "Data Period Configuration",
        'month_start': "Start Month",
        'month_end': "End Month",
        'year': "Year",
        'update_period': "Update Period from Selection",
        'period_updated': "Period updated",
        'period_display': "Data Period",
        'data_filters': "Data Filters",
        'select_area': "Select Area",
        'select_grade': "Select Grade",
        'performance_range': "Performance Range",
        'min_achievement': "Minimum Achievement (%)",
        'max_achievement': "Maximum Achievement (%)",
        'performance_category': "Performance Category",
        'filter_summary': "Filter Summary",
        'download_template': "Download Template",
        'download_help': "Download template for sales data",
        'period_label': "Period",
        'enhanced_dashboard': "Enhanced Analytics Dashboard",
        'kpis': "Key Performance Indicators",
        'overall_achievement': "Overall Achievement",
        'average_performance': "Average Performance",
        'top_performer': "Top Performer",
        'team_size': "Team Size",
        'needs_attention': "Needs Attention",
        'overview': "Overview",
        'performers': "Performers",
        'detailed_data': "Detailed Data",
        'recommendations': "Recommendations",
        'footer_text': "Dashboard updated automatically • Data period",
        'last_updated': "Last updated",
        'search_name': "Search by Name",
        'sort_by': "Sort by",
        'export_format': "Export Format",
        'records_shown': "Records Shown",
        'avg_achievement': "Avg Achievement",
        'total_gap': "Total Gap",
        'group_achievement': "Group Achievement",
        'excellent_performers': "Excellent Performers",
        'good_performers': "Good Performers",
        'average_performers': "Average Performers",
        'needs_improvement': "Needs Improvement",
        'top_performers': "Top 10 Performers",
        'bottom_performers': "Bottom 10 Performers",
        'executive_summary': "Executive Summary",
        'overall_status': "Overall Status",
        'risk_level': "Risk Level",
        'quick_wins': "Quick Wins",
        'benchmarks': "Benchmarks",
        'immediate_actions': "Immediate Priority Actions",
        'area_maps': "Area Maps",
        'geographic_distribution': "Geographic Distribution",
        'map_type': "Select Map Type",
        'interactive_map': "Interactive Map",
        'heatmap': "Heatmap",
        'bubble_map': "Bubble Map",
        'map_legend': "Map Legend",
        'performance_color': "Performance Color Code",
        'bubble_size': "Bubble Size",
        'map_tips': "Map Tips",
        'area_summary': "Area Summary",
        'regional_analysis': "Regional Analysis",
        'top_performing_areas': "Top Performing Areas",
        'areas_need_attention': "Areas Need Attention"
    }
}

def get_text(key):
    return LANGUAGES[st.session_state.language][key]

# ============================================================================
# ENHANCED CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1f77b4;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .excellent { 
        color: #28a745; 
        font-weight: bold;
        background-color: rgba(40, 167, 69, 0.1);
        padding: 2px 8px;
        border-radius: 12px;
    }
    .good { 
        color: #17a2b8; 
        font-weight: bold;
        background-color: rgba(23, 162, 184, 0.1);
        padding: 2px 8px;
        border-radius: 12px;
    }
    .warning { 
        color: #ffc107; 
        font-weight: bold;
        background-color: rgba(255, 193, 7, 0.1);
        padding: 2px 8px;
        border-radius: 12px;
    }
    .danger { 
        color: #dc3545; 
        font-weight: bold;
        background-color: rgba(220, 53, 69, 0.1);
        padding: 2px 8px;
        border-radius: 12px;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .footer {
        text-align: center;
        color: #6c757d;
        font-style: italic;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #dee2e6;
    }
    
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    
    .map-container {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .metric-card {
            margin: 0.25rem;
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA LOADING AND PROCESSING FUNCTIONS
# ============================================================================

def process_uploaded_file(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(
                uploaded_file,
                delimiter=',',
                skipinitialspace=True,
                encoding='utf-8',
                on_bad_lines='skip'
            )
        else:
            df = pd.read_excel(uploaded_file, sheet_name=0, engine='openpyxl')
        
        df.columns = df.columns.str.strip()
        
        required_columns = ['Area', 'SubArea', 'Nama', 'Grade', 'Target', 'Sales']
        available_columns = [col.strip() for col in df.columns]
        missing_columns = []
        
        for req_col in required_columns:
            if req_col not in available_columns:
                found = False
                for avail_col in available_columns:
                    if req_col.lower() == avail_col.lower():
                        df = df.rename(columns={avail_col: req_col})
                        found = True
                        break
                if not found:
                    missing_columns.append(req_col)
        
        if missing_columns:
            st.error(f"❌ Missing columns: {missing_columns}")
            st.info(f"✅ Available columns: {list(df.columns)}")
            return None
        
        df = df.dropna(subset=required_columns)
        
        try:
            df['Target'] = pd.to_numeric(df['Target'], errors='coerce')
            df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
        except Exception as e:
            st.error(f"Error converting numeric columns: {e}")
            return None
        
        df = df.dropna(subset=['Target', 'Sales'])
        
        df['Minus/plus'] = df['Sales'] - df['Target']
        df['Percentage'] = (df['Sales'] / df['Target'] * 100).round(2)
        
        def categorize_performance(percentage):
            if percentage >= 120:
                return 'Excellent'
            elif percentage >= 100:
                return 'Good'
            elif percentage >= 80:
                return 'Average'
            elif percentage >= 60:
                return 'Below Average' 
            else:
                return 'Poor'
        
        df['Performance_Category'] = df['Percentage'].apply(categorize_performance)
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def load_sample_data():
    # Sample data with various Indonesian areas
    sample_areas = ['Jakarta', 'Bandung', 'Surabaya', 'Medan', 
                    'Semarang', 'Yogyakarta']
    
    sample_data = {
        'Area': np.random.choice(sample_areas, 100),
        'SubArea': ['SubArea ' + str(i) for i in range(1, 101)],
        'Nama': [f'Sales Person {i}' for i in range(1, 101)],
        'Grade': np.random.choice(['DS', 'S2', 'SPV'], 100),
        'Target': np.random.randint(20, 50, 100),
        'Sales': np.random.randint(15, 60, 100)
    }
    
    df = pd.DataFrame(sample_data)
    df['Minus/plus'] = df['Sales'] - df['Target']
    df['Percentage'] = (df['Sales'] / df['Target'] * 100).round(2)
    
    def categorize_performance(percentage):
        if percentage >= 120:
            return 'Excellent'
        elif percentage >= 100:
            return 'Good'
        elif percentage >= 80:
            return 'Average'
        elif percentage >= 60:
            return 'Below Average' 
        else:
            return 'Poor'
    
    df['Performance_Category'] = df['Percentage'].apply(categorize_performance)
    
    return df

def extract_period_from_filename(filename):
    bulan_map = {
        'jan': 'Januari', 'feb': 'Februari', 'mar': 'Maret', 'apr': 'April',
        'mei': 'Mei', 'jun': 'Juni', 'jul': 'Juli', 'agu': 'Agustus',
        'sep': 'September', 'okt': 'Oktober', 'nov': 'November', 'des': 'Desember',
        'januari': 'Januari', 'februari': 'Februari', 'maret': 'Maret',
        'april': 'April', 'juni': 'Juni', 'juli': 'Juli',
        'agustus': 'Agustus', 'september': 'September',
        'oktober': 'Oktober', 'november': 'November', 'desember': 'Desember'
    }
    
    filename_lower = filename.lower()
    found_months = []
    
    for key, bulan in bulan_map.items():
        if key in filename_lower:
            found_months.append(bulan)
    
    found_months = list(dict.fromkeys(found_months))
    
    tahun_match = re.search(r'(20\d{2})', filename)
    tahun = tahun_match.group(1) if tahun_match else "2024"
    
    if len(found_months) >= 2:
        return f"{found_months[0]} - {found_months[1]} {tahun}"
    elif len(found_months) == 1:
        semua_bulan = list(bulan_map.values())[:12]
        try:
            idx = semua_bulan.index(found_months[0])
            bulan_berikutnya = semua_bulan[(idx + 1) % 12]
            return f"{found_months[0]} - {bulan_berikutnya} {tahun}"
        except:
            return f"{found_months[0]} {tahun}"
    else:
        return st.session_state.periode_data

def calculate_team_metrics(df):
    metrics = {
        'total_team_size': len(df),
        'total_target': df['Target'].sum(),
        'total_sales': df['Sales'].sum(),
        'overall_achievement': (df['Sales'].sum() / df['Target'].sum() * 100).round(2) if df['Target'].sum() > 0 else 0,
        'avg_individual_performance': df['Percentage'].mean().round(2) if not df.empty else 0,
        'performance_std': df['Percentage'].std().round(2) if not df.empty else 0,
        'top_performer': df.loc[df['Percentage'].idxmax(), 'Nama'] if not df.empty else 'N/A',
        'top_performance': df['Percentage'].max() if not df.empty else 0,
        'bottom_performer': df.loc[df['Percentage'].idxmin(), 'Nama'] if not df.empty else 'N/A',
        'bottom_performance': df['Percentage'].min() if not df.empty else 0,
        'zero_sales_count': len(df[df['Sales'] == 0]),
        'excellent_performers': len(df[df['Performance_Category'] == 'Excellent']),
        'good_performers': len(df[df['Performance_Category'] == 'Good']),
        'needs_improvement': len(df[df['Performance_Category'].isin(['Below Average', 'Poor'])])
    }
    return metrics  

def get_area_performance(df):
    if df.empty:
        return pd.DataFrame()
    
    area_stats = df.groupby('Area').agg({
        'Target': 'sum',
        'Sales': 'sum',
        'Percentage': ['mean', 'std', 'count'],
        'Nama': 'count'
    }).round(2)
    
    area_stats.columns = ['Total_Target', 'Total_Sales', 'Avg_Performance', 'Performance_Std', 'Performance_Count', 'Team_Size']
    area_stats['Achievement_Rate'] = (area_stats['Total_Sales'] / area_stats['Total_Target'] * 100).round(2)
    area_stats = area_stats.sort_values('Achievement_Rate', ascending=False)
    
    return area_stats

def get_grade_analysis(df):
    if df.empty:
        return pd.DataFrame()
    
    grade_stats = df.groupby('Grade').agg({
        'Target': ['sum', 'mean'],
        'Sales': ['sum', 'mean'],
        'Percentage': ['mean', 'std'],
        'Nama': 'count'
    }).round(2)
    
    grade_stats.columns = ['Total_Target', 'Avg_Target', 'Total_Sales', 'Avg_Sales', 'Avg_Performance', 'Performance_Std', 'Count']
    grade_stats['Achievement_Rate'] = (grade_stats['Total_Sales'] / grade_stats['Total_Target'] * 100).round(2)
    
    return grade_stats

# ============================================================================
# MAP VISUALIZATION FUNCTIONS 
# ============================================================================

def get_indonesia_coordinates(area_name):
    """Get approximate coordinates for Indonesian areas - PULAU-BASED VERSION"""
    # Normalize area name
    area_lower = area_name.lower().strip()
    
    # Koordinat database DENGAN PULAU INFO
    coordinates_by_island = {
        'JAWA': {
            'Jakarta': {'lat': -6.2088, 'lon': 106.8456},
            'Jakarta Pusat': {'lat': -6.2088, 'lon': 106.8456},
            'Bandung': {'lat': -6.9175, 'lon': 107.6191},
            'Surabaya': {'lat': -7.2575, 'lon': 112.7521},
            'Semarang': {'lat': -6.9667, 'lon': 110.4167},
            'Yogyakarta': {'lat': -7.7956, 'lon': 110.3695},
            'Malang': {'lat': -7.9666, 'lon': 112.6326},
            'Bogor': {'lat': -6.5944, 'lon': 106.7892},
            'Bekasi': {'lat': -6.2349, 'lon': 106.9920},
            # ... (semua kota Jawa lainnya)
        },
        'SUMATERA': {
            'Medan': {'lat': 3.5952, 'lon': 98.6722},
            'Palembang': {'lat': -2.9761, 'lon': 104.7754},
            'Padang': {'lat': -0.9492, 'lon': 100.3543},
            # ... (semua kota Sumatera lainnya)
        },
        'KALIMANTAN': {
            'Banjarmasin': {'lat': -3.3186, 'lon': 114.5944},
            'Balikpapan': {'lat': -1.2680, 'lon': 116.8283},
            # ... (semua kota Kalimantan lainnya)
        },
        'SULAWESI': {
            'Makassar': {'lat': -5.1477, 'lon': 119.4327},
            'Manado': {'lat': 1.4748, 'lon': 124.8421},
            # ... (semua kota Sulawesi lainnya)
        },
        'BALI_NUSA_TENGGARA': {
            'Denpasar': {'lat': -8.6705, 'lon': 115.2126},
            'Bali': {'lat': -8.4095, 'lon': 115.1889},
            # ... (semua kota Bali/Nusa Tenggara)
        },
        'MALUKU_PAPUA': {
            'Ambon': {'lat': -3.6954, 'lon': 128.1814},
            'Jayapura': {'lat': -2.5333, 'lon': 140.7167},
            # ... (semua kota Maluku/Papua)
        }
    }
    
    # Abbreviation mapping DENGAN PULAU INFO
    abbrev_map = {
        'jkt': ('Jakarta', 'JAWA'),
        'bdg': ('Bandung', 'JAWA'),
        'sby': ('Surabaya', 'JAWA'),
        'smg': ('Semarang', 'JAWA'),
        'jogja': ('Yogyakarta', 'JAWA'),
        'mlg': ('Malang', 'JAWA'),
        'mdn': ('Medan', 'SUMATERA'),
        'bpn': ('Balikpapan', 'KALIMANTAN'),
        'mks': ('Makassar', 'SULAWESI'),
        'dps': ('Denpasar', 'BALI_NUSA_TENGGARA'),
        'bjm': ('Banjarmasin', 'KALIMANTAN'),
        'pku': ('Pekanbaru', 'SUMATERA'),
        'plg': ('Palembang', 'SUMATERA'),
    }
    
    # 1. Check abbreviations first
    for abbrev, (full_name, island) in abbrev_map.items():
        if abbrev in area_lower:
            return coordinates_by_island[island][full_name]
    
    # 2. Check exact match in each island
    for island, cities in coordinates_by_island.items():
        for city, coords in cities.items():
            if area_lower == city.lower():
                return coords
    
    # 3. Check partial match (contains)
    for island, cities in coordinates_by_island.items():
        for city, coords in cities.items():
            city_lower = city.lower()
            if city_lower in area_lower or area_lower in city_lower:
                return coords
    
    # 4. Determine island based on keywords
    island_keywords = {
        'JAWA': ['jawa', 'jabar', 'jateng', 'jatim', 'jawabarat', 'jatengah', 'jatimur'],
        'SUMATERA': ['sumatera', 'sumatra', 'aceh', 'medan', 'padang', 'palembang', 'lampung', 'riau'],
        'KALIMANTAN': ['kalimantan', 'borneo', 'banjarmasin', 'balikpapan', 'samarinda', 'pontianak'],
        'SULAWESI': ['sulawesi', 'makassar', 'manado', 'palu', 'kendari', 'gorontalo'],
        'BALI_NUSA_TENGGARA': ['bali', 'denpasar', 'lombok', 'ntb', 'ntt', 'kupang', 'mataram', 'flores'],
        'MALUKU_PAPUA': ['papua', 'jayapura', 'maluku', 'ambon', 'ternate', 'sorong', 'irian']
    }
    
    detected_island = None
    for island, keywords in island_keywords.items():
        for keyword in keywords:
            if keyword in area_lower:
                detected_island = island
                break
        if detected_island:
            break
    
    # 5. Return coordinates based on detected island
    if detected_island:
        # Return center of that island (TIDAK RANDOM!)
        island_centers = {
            'JAWA': {'lat': -7.5, 'lon': 110.0},
            'SUMATERA': {'lat': 0.0, 'lon': 101.0},
            'KALIMANTAN': {'lat': -2.0, 'lon': 114.0},
            'SULAWESI': {'lat': -2.5, 'lon': 121.0},
            'BALI_NUSA_TENGGARA': {'lat': -8.5, 'lon': 116.5},
            'MALUKU_PAPUA': {'lat': -4.0, 'lon': 138.0},
        }
        return island_centers[detected_island]
    
    # 6. Default to Java (most common) - TIDAK RANDOM!
    return {'lat': -7.5, 'lon': 110.0}

def create_performance_map(df):
    """Create Folium interactive map with performance markers"""
    if df.empty:
        return folium.Map(location=[-2.5489, 118.0149], zoom_start=4)
    
    # === TAMBAHKAN LOGGING ===
    st.info(f"📊 Processing map for {len(df)} records, {df['Area'].nunique()} unique areas")
    
    # Calculate average performance per area
    area_stats = df.groupby('Area').agg({
        'Percentage': 'mean',
        'Sales': 'sum',
        'Target': 'sum',
        'Nama': 'count'
    }).round(2)
    
    # === TAMBAHKAN LOGGING ===
    st.write(f"📍 Areas detected: {list(area_stats.index)}")
    
    # Create base map centered on Indonesia
    performance_map = folium.Map(
        location=[-2.5489, 118.0149],  # Center of Indonesia
        zoom_start=4,
        tiles='cartodbpositron'
    )
    
    # Add markers for each area
    for area in area_stats.index:
        avg_performance = area_stats.loc[area, 'Percentage']
        total_sales = area_stats.loc[area, 'Sales']
        team_size = area_stats.loc[area, 'Nama']
        
        # Get coordinates
        coords = get_indonesia_coordinates(area)
        
        # Determine marker color based on performance
        if avg_performance >= 120:
            color = 'green'
            icon_color = 'green'
        elif avg_performance >= 100:
            color = 'lightgreen'
            icon_color = 'lightgreen'
        elif avg_performance >= 80:
            color = 'orange'
            icon_color = 'orange'
        else:
            color = 'red'
            icon_color = 'red'
        
        # Determine icon
        if team_size >= 10:
            icon_type = 'star'
        elif team_size >= 5:
            icon_type = 'info-sign'
        else:
            icon_type = 'info-sign'
        
        # Create popup content
        popup_html = f"""
        <div style="width: 250px; padding: 10px;">
            <h4 style="color: {color}; margin-bottom: 5px;">{area}</h4>
            <hr style="margin: 5px 0;">
            <p><b>Average Performance:</b> <span style="color: {color}; font-weight: bold;">{avg_performance:.1f}%</span></p>
            <p><b>Total Sales:</b> Rp {total_sales:,.0f}</p>
            <p><b>Team Size:</b> {int(team_size)} people</p>
            <p><b>Performance Category:</b> 
                <span style="color: {color}; font-weight: bold;">
                    {'Excellent' if avg_performance >= 120 else 'Good' if avg_performance >= 100 else 'Average' if avg_performance >= 80 else 'Needs Attention'}
                </span>
            </p>
        </div>
        """
        
        # Add marker
        folium.Marker(
            location=[coords['lat'], coords['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{area}: {avg_performance:.1f}%",
            icon=folium.Icon(
                color=icon_color,
                icon=icon_type,
                prefix='fa' if icon_type == 'star' else 'glyphicon'
            )
        ).add_to(performance_map)
    
    # Add layer control
    folium.LayerControl().add_to(performance_map)
    
    return performance_map

def create_heatmap_data(df):
    """Prepare data for heatmap visualization - DYNAMIC VERSION"""
    if df.empty:
        return pd.DataFrame()
    
    area_stats = df.groupby('Area').agg({
        'Percentage': 'mean',
        'Sales': 'sum',
        'Nama': 'count'
    }).round(2)
    
    # Create DataFrame with coordinates - generate for ALL areas
    heatmap_data = []
    areas_processed = set()  # Track processed areas
    
    for area in area_stats.index:
        if area in areas_processed:
            continue
            
        coords = get_indonesia_coordinates(area)
        heatmap_data.append({
            'Area': area,
            'lat': coords['lat'],
            'lon': coords['lon'],
            'Percentage': area_stats.loc[area, 'Percentage'],
            'Sales': area_stats.loc[area, 'Sales'],
            'Nama': int(area_stats.loc[area, 'Nama'])
        })
        areas_processed.add(area)
    
    # Create DataFrame and remove duplicates
    result_df = pd.DataFrame(heatmap_data).drop_duplicates(subset=['Area'])
    
    # Log for debugging
    print(f"Generated coordinates for {len(result_df)} unique areas")
    print(f"Areas found: {list(result_df['Area'])}")
    
    return result_df

def create_bubble_map_figure(area_data):
    """Create bubble map using Plotly"""
    if area_data.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title="No data available for bubble map",
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        return fig
    
    # Create bubble map
    fig = px.scatter_mapbox(
        area_data,
        lat="lat",
        lon="lon",
        size="Nama",  # Bubble size based on team size
        color="Percentage",  # Color based on performance
        hover_name="Area",
        hover_data=["Sales", "Percentage", "Nama"],
        color_continuous_scale="RdYlGn",
        size_max=30,
        zoom=4,
        height=500,
        title="Bubble Map: Performance by Area (Size = Team Size)"
    )
    
    # Update layout
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(
            center=dict(lat=-2.5489, lon=118.0149),
            zoom=4
        ),
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title="Performance (%)",
            thickness=20,
            len=0.5
        )
    )
    
    return fig

# ============================================================================
# MAIN DASHBOARD EXECUTION
# ============================================================================

# SIDEBAR CONFIGURATION
st.sidebar.header(f"🎯 {get_text('dashboard_controls')}")
st.sidebar.markdown("---")

# FILE UPLOAD
st.sidebar.subheader(f"📁 {get_text('upload_data')}")
uploaded_file = st.sidebar.file_uploader(
    get_text('upload_help'),
    type=['xlsx', 'xls', 'csv'],
    help=get_text('upload_help')
)

if uploaded_file is not None:
    data = process_uploaded_file(uploaded_file)
    if data is not None:
        st.sidebar.success(f"✅ {get_text('file_loaded')}: {uploaded_file.name}")
        st.sidebar.info(f"📊 {get_text('data_records')}: {len(data)} records")
        auto_period = extract_period_from_filename(uploaded_file.name)
        st.session_state.periode_data = auto_period
        st.sidebar.info(f"📅 {get_text('period_detected')}: {auto_period}")
    else:
        st.sidebar.warning("⚠️ Using sample data")
        data = load_sample_data()
else:
    st.sidebar.info("📝 Please upload data file or use sample data")
    data = load_sample_data()

# PERIOD CONFIGURATION
st.sidebar.markdown("---")
st.sidebar.subheader(f"📅 {get_text('period_config')}")

bulan_list = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

col_per1, col_per2 = st.sidebar.columns(2)
with col_per1:
    bulan_mulai = st.sidebar.selectbox(
        f"📍 {get_text('month_start')}:",
        bulan_list,
        index=6
    )
with col_per2:
    bulan_akhir = st.sidebar.selectbox(
        f"📍 {get_text('month_end')}:",
        bulan_list,
        index=7
    )

tahun = st.sidebar.selectbox(
    f"📅 {get_text('year')}:",
    [2023, 2024, 2025],
    index=1
)

if st.sidebar.button(f"🔄 {get_text('update_period')}"):
    manual_period = f"{bulan_mulai} - {bulan_akhir} {tahun}"
    st.session_state.periode_data = manual_period
    st.sidebar.success(f"✅ {get_text('period_updated')}: {manual_period}")

st.sidebar.info(f"📊 {get_text('period_display')}: {st.session_state.periode_data}")

# DATA FILTERS
st.sidebar.markdown("---")
st.sidebar.subheader(f"📊 {get_text('data_filters')}")

areas = ['All'] + sorted(data['Area'].unique().tolist())
area_performance = get_area_performance(data)
area_options = []
for area in areas:
    if area == 'All':
        area_options.append(area)
    else:
        perf = area_performance.loc[area, 'Achievement_Rate'] if area in area_performance.index else 0
        area_options.append(f"{area} ({perf:.1f}%)")

selected_area_display = st.sidebar.selectbox(f"📍 {get_text('select_area')}:", area_options)
selected_area = selected_area_display.split(' (')[0] if '(' in selected_area_display else selected_area_display

grades = ['All'] + sorted(data['Grade'].unique().tolist())
grade_analysis = get_grade_analysis(data)
grade_options = []
for grade in grades:
    if grade == 'All':
        grade_options.append(grade)
    else:
        count = grade_analysis.loc[grade, 'Count'] if grade in grade_analysis.index else 0
        grade_options.append(f"{grade} ({int(count)} orang)")

selected_grade_display = st.sidebar.selectbox(f"👥 {get_text('select_grade')}:", grade_options)
selected_grade = selected_grade_display.split(' (')[0] if '(' in selected_grade_display else selected_grade_display

st.sidebar.subheader(f"🎯 {get_text('performance_range')}")
min_achievement = st.sidebar.slider(f"📉 {get_text('min_achievement')}:", 0, 200, 0)
max_achievement = st.sidebar.slider(f"📈 {get_text('max_achievement')}:", 0, 200, 200)

st.sidebar.subheader(f"📈 {get_text('performance_category')}")
categories = ['All'] + data['Performance_Category'].unique().tolist()
selected_category = st.sidebar.selectbox(f"📊 {get_text('performance_category')}:", categories)

# APPLY FILTERS
filtered_data = data.copy()
if selected_area != 'All':
    filtered_data = filtered_data[filtered_data['Area'] == selected_area]
if selected_grade != 'All':
    filtered_data = filtered_data[filtered_data['Grade'] == selected_grade]
if selected_category != 'All':
    filtered_data = filtered_data[filtered_data['Performance_Category'] == selected_category]

filtered_data = filtered_data[
    (filtered_data['Percentage'] >= min_achievement) & 
    (filtered_data['Percentage'] <= max_achievement)
]

# FILTER SUMMARY
st.sidebar.markdown("---")
st.sidebar.subheader(f"📋 {get_text('filter_summary')}")
st.sidebar.info(f"""
**Data yang ditampilkan:**
- Total Records: {len(filtered_data):,}
- Area: {selected_area}
- Grade: {selected_grade}
- Performance: {min_achievement}% - {max_achievement}%
- Category: {selected_category}
""")

# DOWNLOAD TEMPLATE
st.sidebar.markdown("---")
st.sidebar.subheader(f"📥 {get_text('download_template')}")

template_data = {
    'Area': ['Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Makassar'],
    'SubArea': ['Jakarta Pusat', 'Bandung Timur', 'Surabaya Barat', 'Medan Selatan', 'Makassar Utara'], 
    'Nama': ['Sales Person 1', 'Sales Person 2', 'Sales Person 3', 'Sales Person 4', 'Sales Person 5'],
    'Grade': ['DS', 'S2', 'SPV', 'DS', 'S2'],
    'Target': [25, 35, 35, 25, 35],
    'Sales': [20, 32, 30, 28, 40]
}
template_df = pd.DataFrame(template_data)

csv_template = template_df.to_csv(index=False)
st.sidebar.download_button(
    label=f"📋 {get_text('download_template')}",
    data=csv_template,
    file_name="sales_data_template.csv",
    mime="text/csv",
    help=f"📄 {get_text('download_help')}"
)

# MAIN DASHBOARD CONTENT
st.markdown(f'<div class="main-header">📊 {get_text("dashboard_title")}</div>', unsafe_allow_html=True)
st.markdown(f"**📅 {get_text('period_label')}: {st.session_state.periode_data} | 🎯 {get_text('enhanced_dashboard')}**")

team_metrics = calculate_team_metrics(filtered_data)

# KEY METRICS
st.subheader(f"🎯 {get_text('kpis')}")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_sales = team_metrics['total_sales']
    total_target = team_metrics['total_target']
    achievement = team_metrics['overall_achievement']
    delta_color = "normal" if achievement >= 100 else "inverse"
    st.metric(
        f"🎯 {get_text('overall_achievement')}",
        f"{achievement:.1f}%", 
        f"{total_sales:,}/{total_target:,}",
        delta_color=delta_color
    )

with col2:
    avg_performance = team_metrics['avg_individual_performance']
    performance_std = team_metrics['performance_std']
    st.metric(
        f"📊 {get_text('average_performance')}",
        f"{avg_performance:.1f}%",
        f"±{performance_std:.1f}% std"
    )

with col3:
    top_performance = team_metrics['top_performance']
    top_performer = team_metrics['top_performer']
    st.metric(
        f"🏆 {get_text('top_performer')}",
        f"{top_performance:.1f}%", 
        f"{top_performer[:15]}..." if len(top_performer) > 15 else top_performer
    )

with col4:
    team_size = team_metrics['total_team_size']
    excellent_count = team_metrics['excellent_performers']
    st.metric(
        f"👥 {get_text('team_size')}",
        f"{team_size} people",
        f"{excellent_count} excellent"
    )

with col5:
    zero_sales = team_metrics['zero_sales_count']
    needs_improvement = team_metrics['needs_improvement']
    st.metric(
        f"⚠️ {get_text('needs_attention')}",
        f"{needs_improvement} people",
        f"{zero_sales} zero sales",
        delta_color="inverse" if needs_improvement > 0 else "normal"
    )

st.markdown("---")

# TABS - WITH MAPS AS FIRST TAB
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    f"🗺️ {get_text('area_maps')}",
    f"📈 {get_text('overview')}",
    f"🏆 {get_text('performers')}", 
    f"📋 {get_text('detailed_data')}",
    f"🎯 {get_text('recommendations')}"
])

# TAB 1: MAPS VISUALIZATION
with tab1:
    st.subheader(f"🗺️ {get_text('geographic_distribution')}")
    
    # Map type selection
    map_type = st.radio(
        f"📍 {get_text('map_type')}:",
        [get_text('interactive_map'), get_text('heatmap'), get_text('bubble_map')],
        horizontal=True
    )
    
    col_map, col_legend = st.columns([3, 1])
    
    with col_map:
        if map_type == get_text('interactive_map'):
            # Display interactive map
            st.write(f"**📍 {get_text('interactive_map')}**")
            st.caption("Klik marker untuk detail performa setiap area")
            
            # Create and display map
            performance_map = create_performance_map(filtered_data)
            
            # Display the map
            map_data = st_folium(
                performance_map,
                width=800,
                height=600,
                returned_objects=[]
            )
            
            # Show area count
            unique_areas = filtered_data['Area'].nunique()
            st.info(f"📍 **{unique_areas} area unik** ditemukan dalam data")
            
        elif map_type == get_text('heatmap'):
            st.write(f"**🔥 {get_text('heatmap')}**")
            st.caption("Area dengan warna lebih merah membutuhkan perhatian khusus")
            
            # Create heatmap data
            area_data = create_heatmap_data(filtered_data)
            
            if not area_data.empty:
                # Create heatmap figure
                fig = px.density_mapbox(
                    area_data,
                    lat='lat',
                    lon='lon',
                    z='Percentage',
                    radius=30,
                    center=dict(lat=-2.5489, lon=118.0149),
                    zoom=4,
                    mapbox_style="carto-positron",
                    hover_data=['Area', 'Sales', 'Nama'],
                    title='Heatmap Performa Berdasarkan Area',
                    color_continuous_scale='RdYlGn_r',
                    range_color=[filtered_data['Percentage'].min(), filtered_data['Percentage'].max()],
                    labels={
                        'Percentage': 'Rata-rata Performa (%)',
                        'Sales': 'Total Penjualan',
                        'Nama': 'Jumlah Sales'
                    }
                )
                fig.update_layout(
                    margin=dict(l=0, r=0, t=40, b=0),
                    height=500,
                    coloraxis_colorbar=dict(
                        title="Performa (%)",
                        thickness=20
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Tidak cukup data untuk membuat heatmap")
                
        else:  # Bubble Map
            st.write(f"**🌀 {get_text('bubble_map')}**")
            st.caption("Ukuran bubble menunjukkan jumlah sales person di area tersebut")
            
            area_data = create_heatmap_data(filtered_data)
            
            if not area_data.empty:
                fig = create_bubble_map_figure(area_data)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Tidak cukup data untuk membuat bubble map")
    
    with col_legend:
        st.write(f"**📊 {get_text('map_legend')}**")
        
        # Performance color legend
        st.markdown(f"### 🎯 {get_text('performance_color')}:")
        st.markdown("""
        - 🟢 **Hijau**: ≥120% (Excellent)
        - 🟡 **Hijau Muda**: 100-119% (Good)
        - 🟠 **Oranye**: 80-99% (Average)
        - 🔴 **Merah**: <80% (Perlu Perhatian)
        
        ### 📈 {bubble_size}:
        - Ukuran menunjukkan jumlah sales person
        - Semakin besar = lebih banyak tim
        
        ### 💡 {map_tips}:
        1. Zoom in/out untuk detail
        2. Klik marker untuk informasi detail
        3. Filter data di sidebar untuk fokus area tertentu
        """.format(
            bubble_size=get_text('bubble_size'),
            map_tips=get_text('map_tips')
        ))
        
        # Quick area summary
        if not filtered_data.empty:
            st.write(f"**📋 {get_text('area_summary')}:**")
            
            # Calculate top areas
            area_stats = filtered_data.groupby('Area').agg({
                'Percentage': 'mean',
                'Sales': 'sum'
            }).round(1)
            
            # Show top 3 areas
            for area in area_stats.index[:3]:
                perf = area_stats.loc[area, 'Percentage']
                sales = area_stats.loc[area, 'Sales']
                st.metric(
                    label=area,
                    value=f"{perf:.1f}%",
                    delta=f"Rp {sales:,.0f}"
                )
    
    # Additional analysis below map
    st.markdown("---")
    
    col_top, col_bottom = st.columns(2)
    
    with col_top:
        # Top 5 performing areas
        if not filtered_data.empty:
            top_areas = filtered_data.groupby('Area')['Percentage'].mean().nlargest(5)
            st.write(f"**🏆 {get_text('top_performing_areas')}:**")
            for area, perf in top_areas.items():
                progress = min(perf / 150, 1.0)  # Normalize for progress bar
                st.progress(
                    float(progress),
                    text=f"{area}: {perf:.1f}%"
                )
    
    with col_bottom:
        # Bottom 5 performing areas
        if not filtered_data.empty:
            bottom_areas = filtered_data.groupby('Area')['Percentage'].mean().nsmallest(5)
            st.write(f"**⚠️ {get_text('areas_need_attention')}:**")
            for area, perf in bottom_areas.items():
                st.error(f"{area}: {perf:.1f}%")
                st.caption(f"Action: Review strategy for {area}")
    
    # Detailed area performance data table
    st.markdown("---")
    st.write(f"**📋 {get_text('regional_analysis')}:**")
    
    if not filtered_data.empty:
        area_detail = filtered_data.groupby('Area').agg({
            'Nama': 'count',
            'Target': 'sum',
            'Sales': 'sum',
            'Percentage': 'mean',
            'Minus/plus': 'sum'
        }).round(2)
        
        area_detail['Achievement'] = (area_detail['Sales'] / area_detail['Target'] * 100).round(1)
        area_detail = area_detail.sort_values('Achievement', ascending=False)
        
        # Style the dataframe
        def color_achievement(val):
            if val >= 120:
                color = '#28a745'
            elif val >= 100:
                color = '#17a2b8'
            elif val >= 80:
                color = '#ffc107'
            else:
                color = '#dc3545'
            return f'color: {color}; font-weight: bold'
        
        styled_area = area_detail.style.format({
            'Target': 'Rp {:,.0f}',
            'Sales': 'Rp {:,.0f}',
            'Percentage': '{:.1f}%',
            'Achievement': '{:.1f}%',
            'Minus/plus': 'Rp {:+,.0f}'
        }).applymap(color_achievement, subset=['Achievement'])
        
        st.dataframe(styled_area, use_container_width=True)
    else:
        st.info("📊 Tidak ada data untuk ditampilkan")

    # Validasi koordinat
    st.markdown("---")
    st.write("### 🗺️ Area Coordinate Validation")
    
    if not filtered_data.empty:
        unique_areas = filtered_data['Area'].unique()
        
        # Tampilkan mapping area -> koordinat
        for area in unique_areas[:10]:  # Batasi 10 area pertama
            coords = get_indonesia_coordinates(area)
            st.write(f"📍 **{area}**: lat={coords['lat']:.4f}, lon={coords['lon']:.4f}")
        
        if len(unique_areas) > 10:
            st.info(f"📋 ... dan {len(unique_areas) - 10} area lainnya")

# TAB 2: OVERVIEW
with tab2:
    st.subheader("📊 Performance Overview & Analytics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if not filtered_data.empty:
            area_stats = get_area_performance(filtered_data)
            if not area_stats.empty:
                area_stats_reset = area_stats.reset_index()
                
                fig = px.bar(
                    area_stats_reset, 
                    x='Area', 
                    y='Achievement_Rate', 
                    title='🏆 Achievement Rate by Area',
                    color='Achievement_Rate', 
                    color_continuous_scale='RdYlGn',
                    text='Achievement_Rate',
                    hover_data=['Team_Size', 'Total_Sales', 'Total_Target']
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(
                    xaxis_title="Area",
                    yaxis_title="Achievement Rate (%)",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not filtered_data.empty:
            performance_dist = filtered_data['Performance_Category'].value_counts()
            colors = ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545']
            
            fig_pie = px.pie(
                values=performance_dist.values, 
                names=performance_dist.index,
                title='📈 Performance Distribution',
                color_discrete_sequence=colors
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    if not filtered_data.empty:
        st.subheader("📊 Sales vs Target Analysis by Sub-Area")
        subarea_stats = filtered_data.groupby('SubArea').agg({
            'Sales': 'sum', 
            'Target': 'sum',
            'Nama': 'count'
        }).reset_index()
        subarea_stats['Achievement'] = (subarea_stats['Sales'] / subarea_stats['Target'] * 100).round(1)
        subarea_stats = subarea_stats.sort_values('Achievement', ascending=True)
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name='Target', 
            x=subarea_stats['SubArea'], 
            y=subarea_stats['Target'],
            marker_color='lightblue',
            text=subarea_stats['Target'],
            textposition='auto'
        ))
        fig_bar.add_trace(go.Bar(
            name='Sales', 
            x=subarea_stats['SubArea'], 
            y=subarea_stats['Sales'],
            marker_color='darkblue',
            text=subarea_stats['Sales'],
            textposition='auto'
        ))
        
        fig_bar.update_layout(
            title='Sales vs Target by Sub-Area (Sorted by Achievement)',
            barmode='group',
            xaxis_title="Sub-Area",
            yaxis_title="Amount",
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# TAB 3: PERFORMERS
with tab3:
    st.subheader("🏆 Top Performers Analysis & Insights")
    
    if not filtered_data.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            excellent_performers = len(filtered_data[filtered_data['Performance_Category'] == 'Excellent'])
            st.metric(get_text('excellent_performers'), excellent_performers, f"{excellent_performers/len(filtered_data)*100:.1f}%")
        
        with col2:
            good_performers = len(filtered_data[filtered_data['Performance_Category'] == 'Good'])
            st.metric(get_text('good_performers'), good_performers, f"{good_performers/len(filtered_data)*100:.1f}%")
        
        with col3:
            avg_performers = len(filtered_data[filtered_data['Performance_Category'] == 'Average'])
            st.metric(get_text('average_performers'), avg_performers, f"{avg_performers/len(filtered_data)*100:.1f}%")
        
        with col4:
            poor_performers = len(filtered_data[filtered_data['Performance_Category'].isin(['Below Average', 'Poor'])])
            st.metric(get_text('needs_improvement'), poor_performers, f"{poor_performers/len(filtered_data)*100:.1f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            top_10 = filtered_data.nlargest(10, 'Percentage')[['Nama', 'SubArea', 'Grade', 'Sales', 'Target', 'Percentage', 'Performance_Category']]
            st.write(f"**🏅 {get_text('top_performers')}:**")
            
            def highlight_performance(val):
                if val >= 120:
                    return 'background-color: #d4edda; color: #155724'
                elif val >= 100:
                    return 'background-color: #cce5ff; color: #004085'
                else:
                    return ''
            
            styled_top = top_10.style.format({
                'Sales': '{:.0f}',
                'Target': '{:.0f}', 
                'Percentage': '{:.1f}%'
            }).applymap(highlight_performance, subset=['Percentage'])
            
            st.dataframe(styled_top, use_container_width=True)
        
        with col2:
            bottom_10 = filtered_data.nsmallest(10, 'Percentage')[['Nama', 'SubArea', 'Grade', 'Sales', 'Target', 'Percentage', 'Performance_Category']]
            st.write(f"**⚠️ {get_text('bottom_performers')}:**")
            
            def highlight_poor_performance(val):
                if val < 60:
                    return 'background-color: #f8d7da; color: #721c24'
                elif val < 80:
                    return 'background-color: #fff3cd; color: #856404'
                else:
                    return ''
            
            styled_bottom = bottom_10.style.format({
                'Sales': '{:.0f}',
                'Target': '{:.0f}',
                'Percentage': '{:.1f}%'
            }).applymap(highlight_poor_performance, subset=['Percentage'])
            
            st.dataframe(styled_bottom, use_container_width=True)

# TAB 4: DETAILED DATA
with tab4:
    st.subheader("📋 Detailed Data View & Analysis")
    
    if not filtered_data.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input(f"🔍 {get_text('search_name')}:")
        with col2:
            sort_by = st.selectbox(f"📊 {get_text('sort_by')}:", [
                'Percentage DESC', 'Percentage ASC', 
                'Sales DESC', 'Sales ASC',
                'Target DESC', 'Target ASC',
                'Name A-Z', 'Name Z-A',
                'Area A-Z'
            ])
        with col3:
            export_format = st.selectbox(f"📤 {get_text('export_format')}:", ['View Only', 'CSV Download', 'Excel Download'])
        
        display_df = filtered_data.copy()
        if search_name:
            display_df = display_df[display_df['Nama'].str.contains(search_name, case=False, na=False)]
        
        sort_columns = {
            'Percentage DESC': ['Percentage', False],
            'Percentage ASC': ['Percentage', True],
            'Sales DESC': ['Sales', False],
            'Sales ASC': ['Sales', True],
            'Target DESC': ['Target', False],
            'Target ASC': ['Target', True],
            'Name A-Z': ['Nama', True],
            'Name Z-A': ['Nama', False],
            'Area A-Z': ['Area', True]
        }
        sort_col, ascending = sort_columns[sort_by]
        display_df = display_df.sort_values(sort_col, ascending=ascending)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('records_shown'), len(display_df))
        with col2:
            avg_achievement = display_df['Percentage'].mean()
            st.metric(get_text('avg_achievement'), f"{avg_achievement:.1f}%")
        with col3:
            total_gap = display_df['Minus/plus'].sum()
            st.metric(get_text('total_gap'), f"{total_gap:+.0f}")
        with col4:
            achievement_rate = (display_df['Sales'].sum() / display_df['Target'].sum() * 100) if display_df['Target'].sum() > 0 else 0
            st.metric(get_text('group_achievement'), f"{achievement_rate:.1f}%")
        
        st.write(f"**📊 Showing {len(display_df)} of {len(filtered_data)} records**")
        
        display_columns = ['Nama', 'Area', 'SubArea', 'Grade', 'Target', 'Sales', 'Minus/plus', 'Percentage', 'Performance_Category']
        
        def style_dataframe(df):
            def highlight_performance_row(row):
                if row['Percentage'] >= 120:
                    return ['background-color: #d4edda'] * len(row)
                elif row['Percentage'] >= 100:
                    return ['background-color: #cce5ff'] * len(row)
                elif row['Percentage'] >= 80:
                    return ['background-color: #fff3cd'] * len(row)
                elif row['Percentage'] >= 60:
                    return ['background-color: #ffeaa7'] * len(row)
                else:
                    return ['background-color: #f8d7da'] * len(row)
            
            return df.style.format({
                'Target': '{:.0f}', 
                'Sales': '{:.0f}', 
                'Minus/plus': '{:+.0f}',
                'Percentage': '{:.1f}%'
            }).apply(highlight_performance_row, axis=1)
        
        styled_df = style_dataframe(display_df[display_columns])
        st.dataframe(styled_df, use_container_width=True, height=500)
        
        if export_format == 'CSV Download':
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"sales_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("📊 Tidak ada data untuk ditampilkan")

# TAB 5: RECOMMENDATIONS
with tab5:
    st.subheader("🎯 Strategic Recommendations & Action Plans")
    
    if not filtered_data.empty:
        critical_areas = filtered_data.groupby('SubArea')['Percentage'].mean().nsmallest(3)
        zero_sales = filtered_data[filtered_data['Sales'] == 0]
        poor_performers = filtered_data[filtered_data['Performance_Category'].isin(['Below Average', 'Poor'])]
        excellent_performers = filtered_data[filtered_data['Performance_Category'] == 'Excellent']
        
        st.markdown(f"### 📋 {get_text('executive_summary')}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall_achievement = (filtered_data['Sales'].sum() / filtered_data['Target'].sum() * 100) if filtered_data['Target'].sum() > 0 else 0
            status = "🟢 Good" if overall_achievement >= 100 else "🟡 Needs Attention" if overall_achievement >= 80 else "🔴 Critical"
            st.metric(get_text('overall_status'), status, f"{overall_achievement:.1f}%")
        
        with col2:
            risk_level = len(poor_performers) / len(filtered_data) * 100 if len(filtered_data) > 0 else 0
            risk_status = "🔴 High" if risk_level > 30 else "🟡 Medium" if risk_level > 15 else "🟢 Low"
            st.metric(get_text('risk_level'), risk_status, f"{risk_level:.1f}%")
        
        with col3:
            improvement_potential = len(filtered_data[(filtered_data['Percentage'] >= 50) & (filtered_data['Percentage'] < 80)])
            st.metric(get_text('quick_wins'), f"{improvement_potential} people", "Medium performers")
        
        with col4:
            benchmark_performers = len(excellent_performers)
            st.metric(get_text('benchmarks'), f"{benchmark_performers} people", "Excellent performers")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"### 🔴 {get_text('immediate_actions')}")
            
            if len(critical_areas) > 0:
                st.markdown(f"""
                **1. 🚨 Critical Areas Intervention:**
                - **{critical_areas.index[0] if len(critical_areas) > 0 else 'N/A'}**: {(critical_areas.iloc[0] if len(critical_areas) > 0 else 0):.1f}% achievement
                - **{critical_areas.index[1] if len(critical_areas) > 1 else 'N/A'}**: {(critical_areas.iloc[1] if len(critical_areas) > 1 else 0):.1f}% achievement
                - **{critical_areas.index[2] if len(critical_areas) > 2 else 'N/A'}**: {(critical_areas.iloc[2] if len(critical_areas) > 2 else 0):.1f}% achievement

                **📋 Action Items:**
                - Immediate area manager meetings
                - Resource reallocation assessment
                - Market condition analysis
                """)
            
            if len(zero_sales) > 0:
                st.markdown(f"""
                **2. 🎯 Zero-Sales Intervention:**
                - **{len(zero_sales)} people** with zero sales
                - Immediate 1-on-1 coaching required
                - Performance improvement plans (PIP)
                
                **📋 Action Items:**
                - Daily check-ins for 2 weeks
                - Skills assessment and training
                - Mentorship pairing
                """)
    else:
        st.info("📊 Tidak ada data untuk rekomendasi")

# FOOTER
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: gray;'>
    <i>📊 {get_text('footer_text')}: {st.session_state.periode_data} • ⏰ {get_text('last_updated')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
</div>
""", unsafe_allow_html=True)