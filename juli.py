"""
============================================================================
SALES PERFORMANCE ANALYTICS DASHBOARD
============================================================================

Author: Data Analyst Team
Version: 2.0 (Enhanced with Best Practices)
Data Period: Juli-Agustus 2024
Business Context: Multi-area sales performance tracking and optimization
Technical Stack: Streamlit, Plotly, Pandas
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
from datetime import datetime as dt, timedelta
from typing import Dict, List, Tuple
import warnings
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
        'About': "Sales Performance Analytics Dashboard v2.0 - Enhanced with Data Analyst Best Practices"
    }
)

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
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING AND PROCESSING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def load_data() -> pd.DataFrame:
    """
    DATA ANALYST FUNCTION: Load and process sales performance data
    """
    
    # DATA YANG SUDAH DIKOREKSI - PANJANG ARRAY DISAMAKAN
    complete_data = {
        'Area': [
            # Ciputat (16)
            'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat',
            'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat',
            # Kab Tangerang (9)
            'Kab Tangerang', 'Kab Tangerang', 'Kab Tangerang', 'Kab Tangerang', 'Kab Tangerang',
            'Kab Tangerang', 'Kab Tangerang', 'Kab Tangerang', 'Kab Tangerang',
            # Kota Tangerang Poris (10)
            'Kota Tangerang Poris', 'Kota Tangerang Poris', 'Kota Tangerang Poris', 'Kota Tangerang Poris',
            'Kota Tangerang Poris', 'Kota Tangerang Poris', 'Kota Tangerang Poris', 'Kota Tangerang Poris',
            'Kota Tangerang Poris', 'Kota Tangerang Poris',
            # Jakarta (26)
            'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta',
            'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta',
            'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta',
            'Jakarta', 'Jakarta',
            # Depok (22)
            'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok',
            'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok',
            'Depok', 'Depok',
            # Cengkareng (1)
            'Cengkareng',
            # Klapanunggal (8)
            'Klapanunggal', 'Klapanunggal', 'Klapanunggal', 'Klapanunggal', 'Klapanunggal', 'Klapanunggal',
            'Klapanunggal', 'Klapanunggal',
            # Cileungsi (6)
            'Cileungsi', 'Cileungsi', 'Cileungsi', 'Cileungsi', 'Cileungsi', 'Cileungsi',
            # Parung (7)
            'Parung', 'Parung', 'Parung', 'Parung', 'Parung', 'Parung', 'Parung',
            # Tambun (8)
            'Tambun', 'Tambun', 'Tambun', 'Tambun', 'Tambun', 'Tambun', 'Tambun', 'Tambun',
            # Serang (13)
            'Serang', 'Serang', 'Serang', 'Serang', 'Serang', 'Serang', 'Serang', 'Serang', 'Serang',
            'Serang', 'Serang', 'Serang', 'Serang',
            # Cilegon (6)
            'Cilegon', 'Cilegon', 'Cilegon', 'Cilegon', 'Cilegon', 'Cilegon',
            # Kab Pandeglang (6)
            'Kab Pandeglang', 'Kab Pandeglang', 'Kab Pandeglang', 'Kab Pandeglang', 'Kab Pandeglang', 'Kab Pandeglang',
            # Semarang (52)
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang'
        ],
        
        'SubArea': [
            # Ciputat (16)
            'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat',
            'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat', 'Ciputat',
            # Kab Tangerang (9)
            'Kab Tangerang', 'Kab Tangerang', 'Kab Tangerang', 'Kab Tangerang', 'Kab Tangerang',
            'Kab Tangerang', 'Kab Tangerang', 'Kab Tangerang', 'Kab Tangerang',
            # Kota Tangerang Poris (10)
            'Kota Tangerang Poris', 'Kota Tangerang Poris', 'Kota Tangerang Poris', 'Kota Tangerang Poris',
            'Kota Tangerang Poris', 'Kota Tangerang Poris', 'Kota Tangerang Poris', 'Kota Tangerang Poris',
            'Kota Tangerang Poris', 'Kota Tangerang Poris',
            # Jakarta (26)
            'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta',
            'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta',
            'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta', 'Jakarta',
            'Jakarta', 'Jakarta',
            # Depok (22)
            'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok',
            'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok', 'Depok',
            'Depok', 'Depok',
            # Cengkareng (1)
            'Cengkareng',
            # Bogor - Klapanunggal (8)
            'Bogor - Klapanunggal', 'Bogor - Klapanunggal', 'Bogor - Klapanunggal', 'Bogor - Klapanunggal',
            'Bogor - Klapanunggal', 'Bogor - Klapanunggal', 'Bogor - Klapanunggal', 'Bogor - Klapanunggal',
            # Bogor - Cileungsi (6)
            'Bogor - Cileungsi', 'Bogor - Cileungsi', 'Bogor - Cileungsi', 'Bogor - Cileungsi',
            'Bogor - Cileungsi', 'Bogor - Cileungsi',
            # Bogor - Parung (7)
            'Bogor - Parung', 'Bogor - Parung', 'Bogor - Parung', 'Bogor - Parung', 'Bogor - Parung',
            'Bogor - Parung', 'Bogor - Parung',
            # Bogor - Tambun (8)
            'Bogor - Tambun', 'Bogor - Tambun', 'Bogor - Tambun', 'Bogor - Tambun', 'Bogor - Tambun',
            'Bogor - Tambun', 'Bogor - Tambun', 'Bogor - Tambun',
            # Banten - Serang (13)
            'Banten - Serang', 'Banten - Serang', 'Banten - Serang', 'Banten - Serang', 'Banten - Serang',
            'Banten - Serang', 'Banten - Serang', 'Banten - Serang', 'Banten - Serang', 'Banten - Serang',
            'Banten - Serang', 'Banten - Serang', 'Banten - Serang',
            # Banten - Cilegon (6)
            'Banten - Cilegon', 'Banten - Cilegon', 'Banten - Cilegon', 'Banten - Cilegon', 'Banten - Cilegon', 'Banten - Cilegon',
            # Banten - Kab Pandeglang (6)
            'Banten - Kab Pandeglang', 'Banten - Kab Pandeglang', 'Banten - Kab Pandeglang',
            'Banten - Kab Pandeglang', 'Banten - Kab Pandeglang', 'Banten - Kab Pandeglang',
            # Semarang (52)
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang', 'Semarang',
            'Semarang', 'Semarang', 'Semarang', 'Semarang'
        ],
        
        'Nama': [
            # Ciputat Team (16 members)
            'BUDI SAMBODO', 'MUHAMMAD SETIAWAN', 'MUHAMMAD NOVAL RAMADHAN', 'UKASAH',
            'WIDI WIDAYAT', 'ERLAND ERLANGGA', 'MUHAMAD RISKI', 'MELINA',
            'MONALISA SIPAHUTAR', 'SUDARMANTO', 'SELLA RIZKIA', 'APRINA SIAGIAN',
            'DIAN SRI ANDRYANI', 'SELSA BELLA HUTABARAT', 'NEINAH DAMAISARI', 'MIKA WANTI NAINGGOLAN',
            
            # Kab Tangerang Team (9 members)
            'SUHARDIANSYAH', 'DEA MAULIDAH', 'M AZRIEL HAZNAM S', 'AYULIA KHAERUNNISA',
            'RAHMAWATI', 'RIZAL FAUZI', 'FIGH TRI OKTAVIANO', 'SITI HARDIANTI', 'INE LUTFIA NOVELLA',
            
            # Kota Tangerang Poris Team (10 members)
            'DANIEL MATIUS KOLONDAM', 'ARYA DILLA', 'GALIH KURNIAWAN', 'ZULHAM REINALLDO',
            'DITA CAHYANI', 'INDAH NOVIYANTI', 'BUKHORI', 'M SOLEH', 'SUGANDA MS', 'IQBAL FADILAH',
            
            # Jakarta Team (26 members)
            'Santoso Nainggolan', 'Daniel Parlindungan', 'Santo Yahya Purba', 'Ibbe Arfiah Ambarita',
            'Ninton Silitonga', 'Irwan Panjaitan', 'Ignatius Romy Setyawan', 'Rokhyati BT Wain',
            'Hendrik Pandapotan', 'Juwisri Mariati Simanjuntak', 'Lely Meyana', 'Daniel Toni Sagala',
            'Bastian Ronaldo Butar Butar', 'Maryanti Manalu', 'Fadli Syawalludin', 'Dimposma Hutagalung',
            'Leo Hermansyah', 'Alvin Jon Raya S', 'Julietta Winar Pasha', 'Hinando Praya Saragih',
            'Suriati T.Situmeang', 'Rani Martina Samosir', 'Bruno Mario', 'Moh Marifan Delavena',
            'Indrah Septian', 'Irwanto',
            
            # Depok Team (22 members)
            'Fanda Waty Sry Ayu manalu', 'Gresintia Samosir', 'Sari Nopita Sipahutar', 'Douglas sinaga',
            'Delima Sihotang', 'Muhammad Hilmy', 'Kautsar', 'Raga Purnomo', 'Melyana Samosir',
            'Nova Indriani', 'Nanda Amalia Febriani', 'Lewi Indriyani Panggabean', 'Haryanti',
            'Lia Rahmawati', 'Yandira Cahaya Putri', 'Abdul zaki', 'Indah Fitria', 'Bayu Utomo',
            'Asya Amalia', 'Rafika Khoirul', 'Herdiansyah', 'Muhammad Rifal',
            
            # Cengkareng Team (1 member)
            'Muhammad Nur Zaman Akbar',
            
            # Bogor - Klapanunggal (8 members)
            'SUSANTO HIDAYAT', 'IMEY MELIAWATI', 'ATMA HAYYU FTIRIANTI', 'WIDYA RAHMA',
            'DHEA APRILIA', 'VELY FRIYANTI DJOHAN', 'LUBIS SUGARA', 'HAPITZA ALBAR',
            
            # Bogor - Cileungsi (6 members)
            'WILSON MANALU', 'DEAREN HEAZEL REVIALY', 'SUMIATI', 'IRA ISMAYA',
            'RISKA TASYA MONTANIA GIRSANG', 'YOGI AGUS RANDA',
            
            # Bogor - Parung (7 members)
            'SUKMA ANJALI', 'Muhamad dapa Al rasid', 'Rafly Ilham ramadhan', 'abyan aryan saputra',
            'Ratna Tusyadiyah', 'Friska Olivia Sihaloho', 'DEVI ANDRIANI',
            
            # Bogor - Tambun (8 members)
            'Binsar Sudarmono Situmorang', 'Mayang Putri Emaliana', 'Exaudi Parulian Situmorang',
            'Marliana', 'Boyke Suhendra', 'Nahum Winardi putra Situmorang', 'Nunung septiani',
            'Afifahtul Khusnul Khatimah',

            # Banten - Serang (13 members)
            'ABDUL RACHIM', 'SRI LESTARI BUTAR BUTAR', 'PURWANTO', 'SUTRISNO', 'NYOTO', 
            'ROHMAN', 'JAFAR SIDIK', 'DAFFALDA KRISMONICA SEPTIA', 'OSRA ADRIZAL', 
            'DENITA HULU', 'AHMAD YANI', 'JALALUDIN', 'ARIF PERMANA',
            
            # Banten - Cilegon (6 members)
            'SHODIK BAGUS SETIAWAN', 'DWI EGA PAMUNGKAS', 'ALVIAR YOKA PRATAMA', 
            'M FAZRIL DARUSSALAM', 'NURMALASARI', 'DIMAS ADIANTO',
            
            # Banten - Kab Pandeglang (6 members)
            'DEDE IRWAN SETIAWIGUNA', 'FAJAR MUBAROK', 'ULFAH MEILANI', 
            'BURHANUDIN', 'PUTRI AGUSTINA', 'NURDIN',

            # Semarang (52 members)
            'INDRA SETIAWAN', 'Daima', 'Arief prabowo', 'Anisa salsa nabila meita', 
            'Anityo kukuh wirastantyo', 'Moch syafrany', 'Sudibyo pujo wiyono', 
            'Dedimy dwi saputra', 'RUDI KUNCORO', 'Achmad hasan arfie', 'Aditia rahman', 
            'Lina indriyani', 'Rima kuti', 'Teguh subekti', 'Michael kevin agusta putra', 
            'Andri afrizal', 'AKHMAD HARUN', 'Eri setiawan', 'Dodo kristono', 
            'Avian wijayanto', 'Widarwanto', 'Nur kholidin', 'Wiwin Apit Yulianto', 
            'NUR SALIM', 'Ahmad Syaikhu', 'Taufik Jorgi Kurniawan', 'Pramunita Kristianti', 
            'Rindi Adi Pratama', 'HELMY AS\'ARY', 'Aries sulistiyanto', 'Habib Akbar', 
            'Rezki Irwandy', 'Bayu Satria Putra', 'Rifqi Mubarak', 'Abdurrahman', 
            'IDA BAGUS KAMAJAYA', 'Aris Supriyadi', 'M Abidin ardiyanto', 'Putri puspitasari', 
            'Nendra dewa kurniawan', 'PRANA BRAHMANTYA', 'Frengky Gilang Adi Pradana', 
            'Antonia Widya', 'Khofsah Noor', 'Francois Febriyanto', 'Ardianto Arif Pramono', 
            'NUR HADI', 'Yusuf Rani', 'Siti Nurjanah', 'Fitria Jayanti Mahmud', 
            'Yosi Imelda', 'Lilik Setiawan'
        ],
        
        'Grade': [
            # Ciputat (16) - SPV + 15 DS
            'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS',
            # Kab Tangerang (9) - SPV + 8 DS
            'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS',
            # Kota Tangerang Poris (10) - SPV + 9 DS
            'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS',
            # Jakarta (26) - SPV + 25 S2
            'SPV', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2',
            'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2',
            # Depok (22) - SPV + 21 S2
            'SPV', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2',
            'S2', 'S2', 'S2', 'S2', 'S2', 'S2',
            # Cengkareng (1) - S2
            'S2',
            # Klapanunggal (8) - SPV + 7 S2
            'SPV', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2',
            # Cileungsi (6) - SPV + 5 S2
            'SPV', 'S2', 'S2', 'S2', 'S2', 'S2',
            # Parung (7) - S2 semua
            'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2',
            # Tambun (8) - SPV + 7 S2
            'SPV', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2', 'S2',
            # Serang (13) - SPV + 12 DS
            'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS',
            # Cilegon (6) - SPV + 5 DS
            'SPV', 'DS', 'DS', 'DS', 'DS', 'DS',
            # Kab Pandeglang (6) - SPV + 5 DS
            'SPV', 'DS', 'DS', 'DS', 'DS', 'DS',
            # Semarang (52) - SPV + 51 DS
            'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS',
            'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS',
            'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS',
            'DS', 'DS', 'DS', 'DS'
        ],
        
        'Target': [
            # Ciputat (16)
            35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,
            # Kab Tangerang (9)
            35,25,25,25,25,25,25,25,25,
            # Kota Tangerang Poris (10)
            35,25,25,25,25,25,25,25,25,25,
            # Jakarta (26)
            35,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,
            # Depok (22)
            35,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,
            # Cengkareng (1)
            25,
            # Klapanunggal (8)
            35,25,25,25,25,25,25,25,
            # Cileungsi (6)
            35,25,25,25,25,25,
            # Parung (7)
            25,25,25,25,25,25,25,
            # Tambun (8)
            35,25,25,25,25,25,25,25,
            # Serang (13)
            35,25,25,25,25,25,25,25,35,25,25,25,25,
            # Cilegon (6)
            35,25,25,25,25,25,
            # Kab Pandeglang (6)
            35,25,25,25,25,25,
            # Semarang (52)
            35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,35,25,25,
            25,25,35,25,25,25,25,25,25,35,25,25,25,25,35,25,25,25,25,25,35,25,25,25,25,25
        ],
        
        'Sales': [
            # Ciputat (16)
            32,22,18,20,28,15,30,12,38,28,22,15,18,20,25,22,
            # Kab Tangerang (9)
            28,20,15,18,22,25,28,20,15,
            # Kota Tangerang Poris (10)
            28,20,15,18,22,25,28,20,15,18,
            # Jakarta (26)
            30,18,22,25,28,20,15,18,22,25,28,20,15,18,22,25,28,20,15,18,22,25,28,20,15,18,
            # Depok (22)
            25,18,22,25,28,20,15,18,22,25,28,20,15,18,22,25,28,20,15,18,22,25,
            # Cengkareng (1)
            20,
            # Klapanunggal (8)
            30,22,18,25,28,20,15,22,
            # Cileungsi (6)
            28,20,15,18,22,25,
            # Parung (7)
            18,22,25,28,20,15,18,
            # Tambun (8)
            32,25,18,22,28,20,15,25,
            # Serang (13)
            7,20,19,20,13,9,5,15,8,22,19,19,25,
            # Cilegon (6)
            8,25,27,31,8,4,
            # Kab Pandeglang (6)
            36,2,25,16,1,20,
            # Semarang (52)
            0,73,19,46,28,43,25,28,0,41,60,43,22,25,14,18,0,24,22,22,91,18,19,29,37,37,
            36,19,7,27,35,14,19,44,1,13,57,26,28,26,18,20,22,17,32,17,5,19,33,11,2,14
        ]
    }

    # Convert to DataFrame
    df = pd.DataFrame(complete_data)
    
    # Validasi panjang data
    total_records = len(complete_data['Nama'])
    st.info(f"Total records loaded: {total_records}")
    
    # Hitung metrics
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

# FUNGSI ANALYTICS (sama seperti sebelumnya)
def calculate_team_metrics(df):
    if len(df) == 0:
        return {
            'total_team_size': 0, 'total_target': 0, 'total_sales': 0,
            'overall_achievement': 0, 'avg_individual_performance': 0,
            'performance_std': 0, 'top_performer': 'N/A', 'top_performance': 0,
            'bottom_performer': 'N/A', 'bottom_performance': 0,
            'zero_sales_count': 0, 'excellent_performers': 0,
            'good_performers': 0, 'needs_improvement': 0
        }
    
    metrics = {
        'total_team_size': len(df),
        'total_target': df['Target'].sum(),
        'total_sales': df['Sales'].sum(),
        'overall_achievement': (df['Sales'].sum() / df['Target'].sum() * 100).round(2) if df['Target'].sum() > 0 else 0,
        'avg_individual_performance': df['Percentage'].mean().round(2),
        'performance_std': df['Percentage'].std().round(2),
        'top_performer': df.loc[df['Percentage'].idxmax(), 'Nama'] if len(df) > 0 else 'N/A',
        'top_performance': df['Percentage'].max() if len(df) > 0 else 0,
        'bottom_performer': df.loc[df['Percentage'].idxmin(), 'Nama'] if len(df) > 0 else 'N/A',
        'bottom_performance': df['Percentage'].min() if len(df) > 0 else 0,
        'zero_sales_count': len(df[df['Sales'] == 0]),
        'excellent_performers': len(df[df['Performance_Category'] == 'Excellent']),
        'good_performers': len(df[df['Performance_Category'] == 'Good']),
        'needs_improvement': len(df[df['Performance_Category'].isin(['Below Average', 'Poor'])])
    }
    return metrics

def get_area_performance(df):
    if len(df) == 0:
        return pd.DataFrame()
    
    area_stats = df.groupby('Area').agg({
        'Target': 'sum', 'Sales': 'sum', 'Percentage': ['mean', 'std', 'count'], 'Nama': 'count'
    }).round(2)
    
    area_stats.columns = ['Total_Target', 'Total_Sales', 'Avg_Performance', 'Performance_Std', 'Performance_Count', 'Team_Size']
    area_stats['Achievement_Rate'] = (area_stats['Total_Sales'] / area_stats['Total_Target'] * 100).round(2)
    area_stats = area_stats.sort_values('Achievement_Rate', ascending=False)
    
    return area_stats

def get_grade_analysis(df):
    if len(df) == 0:
        return pd.DataFrame()
    
    grade_stats = df.groupby('Grade').agg({
        'Target': ['sum', 'mean'], 'Sales': ['sum', 'mean'], 
        'Percentage': ['mean', 'std'], 'Nama': 'count'
    }).round(2)
    
    grade_stats.columns = ['Total_Target', 'Avg_Target', 'Total_Sales', 'Avg_Sales', 'Avg_Performance', 'Performance_Std', 'Count']
    grade_stats['Achievement_Rate'] = (grade_stats['Total_Sales'] / grade_stats['Total_Target'] * 100).round(2)
    
    return grade_stats

# MAIN DASHBOARD EXECUTION
try:
    data = load_data()
    
    # SIDEBAR FILTERS
    st.sidebar.header("🎯 Dashboard Controls")
    
    areas = ['All'] + sorted(data['Area'].unique().tolist())
    selected_area = st.sidebar.selectbox("📍 Pilih Area:", areas)
    
    grades = ['All'] + sorted(data['Grade'].unique().tolist())
    selected_grade = st.sidebar.selectbox("👥 Pilih Grade:", grades)
    
    min_achievement = st.sidebar.slider("Minimum Achievement (%):", 0, 200, 0)
    max_achievement = st.sidebar.slider("Maximum Achievement (%):", 0, 200, 200)
    
    categories = ['All'] + data['Performance_Category'].unique().tolist()
    selected_category = st.sidebar.selectbox("Kategori Performance:", categories)
    
    # Apply filters
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
    
    # MAIN DASHBOARD
    st.markdown('<div class="main-header">📊 Sales Performance Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown("**📅 Period: 21 Juli - 20 Agustus 2024**")
    
    team_metrics = calculate_team_metrics(filtered_data)
    
    # KEY METRICS
    st.subheader("🎯 Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Overall Achievement", f"{team_metrics['overall_achievement']:.1f}%")
    with col2:
        st.metric("Average Performance", f"{team_metrics['avg_individual_performance']:.1f}%")
    with col3:
        st.metric("Top Performer", f"{team_metrics['top_performance']:.1f}%")
    with col4:
        st.metric("Team Size", f"{team_metrics['total_team_size']} people")
    with col5:
        st.metric("Needs Attention", f"{team_metrics['needs_improvement']} people")
    
    st.markdown("---")
    
    # TABS
    tab1, tab2, tab3 = st.tabs(["📈 Overview", "🏆 Performers", "📋 Detailed Data"])
    
    with tab1:
        st.subheader("Performance Overview")
        
        if len(filtered_data) > 0:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                area_stats = get_area_performance(filtered_data)
                if len(area_stats) > 0:
                    area_stats_reset = area_stats.reset_index()
                    fig = px.bar(area_stats_reset, x='Area', y='Achievement_Rate', 
                                title='Achievement Rate by Area', color='Achievement_Rate')
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                performance_dist = filtered_data['Performance_Category'].value_counts()
                fig_pie = px.pie(values=performance_dist.values, names=performance_dist.index,
                               title='Performance Distribution')
                st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab2:
        st.subheader("Top Performers")
        
        if len(filtered_data) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                top_10 = filtered_data.nlargest(10, 'Percentage')
                st.write("**Top 10 Performers:**")
                st.dataframe(top_10[['Nama', 'Area', 'Grade', 'Percentage']], use_container_width=True)
            
            with col2:
                bottom_10 = filtered_data.nsmallest(10, 'Percentage')
                st.write("**Bottom 10 Performers:**")
                st.dataframe(bottom_10[['Nama', 'Area', 'Grade', 'Percentage']], use_container_width=True)
    
    with tab3:
        st.subheader("Detailed Data")
        
        if len(filtered_data) > 0:
            st.dataframe(filtered_data, use_container_width=True)
    
    # FOOTER
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: gray;'>
        <i>Dashboard updated automatically • Last updated: {dt.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error occurred: {str(e)}")
    st.info("Please check the data structure and try again.")