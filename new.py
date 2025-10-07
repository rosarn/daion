
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
            'Semarang', 'Semarang', 'Semarang', 'Semarang',
            # Kendal (13)
            'Kendal', 'Kendal', 'Kendal', 'Kendal', 'Kendal', 'Kendal', 'Kendal', 
            'Kendal', 'Kendal', 'Kendal', 'Kendal', 'Kendal', 'Kendal',
            # Demak (12)
            'Demak', 'Demak', 'Demak', 'Demak', 'Demak', 'Demak', 
            'Demak', 'Demak', 'Demak', 'Demak', 'Demak', 'Demak',
            # Kudus (4)
            'Kudus', 'Kudus', 'Kudus', 'Kudus'
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
            'Semarang', 'Semarang', 'Semarang', 'Semarang',
            # Kendal (13)
            'Kendal', 'Kendal', 'Kendal', 'Kendal', 'Kendal', 'Kendal', 'Kendal', 
            'Kendal', 'Kendal', 'Kendal', 'Kendal', 'Kendal', 'Kendal',
            # Demak (12)
            'Demak', 'Demak', 'Demak', 'Demak', 'Demak', 'Demak', 
            'Demak', 'Demak', 'Demak', 'Demak', 'Demak', 'Demak',
            # Kudus (4)
            'Kudus', 'Kudus', 'Kudus', 'Kudus'
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
            'Yosi Imelda', 'Lilik Setiawan',
            
            # Kendal Team (13 members)
            'MASHUDI', 'Hendrik Prasetyo', 'Rizky Akbarudin', 'Sigit Fendian Oktavianto',
            'Firdaus Koban', 'Fatahuya alim', 'Catur setyawati', 'Ainus safin',
            'ANUGRAH CAHYO WARDIYANTANTO', 'Mega Kristiawan', 'Ahmad Mustofa Habib',
            'Yonatan Nurwidiastoni', 'Diah perdana yulianingrum',
            
            # Demak Team (12 members)
            'AGUNG SUGIARTO', 'Dika Catur Susilo', 'Ahsanul Khuluk', 'Anita Noviani',
            'Muhammad Afifuddin', 'Septi prima Aretha', 'TRIAS PUSPITASARI', 'Hendra',
            'Angga Erwanto', 'Mohamad samsuri', 'Nur Fattah Robi Damara', 'Rio priambodo',
            
            # Kudus Team (4 members)
            'Achmad Sahlan Chafid', 'Syahrul Ramadhan', 'Rizky Rimayandi Oktiawan', 'Afifah Nilam Sari'
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
            'DS', 'DS', 'DS', 'DS',
            # Kendal (13) - 2 SPV + 11 DS
            'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS',
            # Demak (12) - 2 SPV + 10 DS
            'SPV', 'DS', 'DS', 'DS', 'DS', 'DS', 'SPV', 'DS', 'DS', 'DS', 'DS', 'DS',
            # Kudus (4) - 4 DS
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
            25,25,35,25,25,25,25,25,25,35,25,25,25,25,35,25,25,25,25,25,35,25,25,25,25,25,
            # Kendal (13)
            35,25,25,25,25,25,25,25,35,25,25,25,25,
            # Demak (12)
            35,25,25,25,25,25,35,25,25,25,25,25,
            # Kudus (4)
            25,25,25,25
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
            36,19,7,27,35,14,19,44,1,13,57,26,28,26,18,20,22,17,32,17,5,19,33,11,2,14,
            # Kendal (13)
            9,45,23,92,20,14,10,7,18,19,20,25,10,
            # Demak (12)
            29,30,17,12,18,10,16,11,15,14,1,1,
            # Kudus (4)
            16,17,16,1
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
        'top_performer': df.loc[df['Percentage'].idxmax(), 'Nama'] if df['Percentage'].max() > 0 else 'N/A',
        'top_performance': df['Percentage'].max().round(2),
        'bottom_performer': df.loc[df['Percentage'].idxmin(), 'Nama'] if len(df) > 0 else 'N/A',
        'bottom_performance': df['Percentage'].min().round(2),
        'zero_sales_count': (df['Sales'] == 0).sum(),
        'excellent_performers': (df['Percentage'] >= 120).sum(),
        'good_performers': ((df['Percentage'] >= 100) & (df['Percentage'] < 120)).sum(),
        'needs_improvement': (df['Percentage'] < 80).sum()
    }
    
    return metrics

def create_performance_chart(df):
    performance_counts = df['Performance_Category'].value_counts().reindex(
        ['Excellent', 'Good', 'Average', 'Below Average', 'Poor'], fill_value=0
    )
    
    fig = px.bar(
        x=performance_counts.index,
        y=performance_counts.values,
        title="Performance Distribution",
        labels={'x': 'Performance Category', 'y': 'Number of Team Members'},
        color=performance_counts.values,
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=400
    )
    
    return fig

def create_area_comparison_chart(df):
    area_performance = df.groupby('Area').agg({
        'Target': 'sum',
        'Sales': 'sum'
    }).reset_index()
    
    area_performance['Achievement_Rate'] = (area_performance['Sales'] / area_performance['Target'] * 100).round(2)
    
    fig = px.bar(
        area_performance,
        x='Area',
        y='Achievement_Rate',
        title="Area Performance Comparison",
        labels={'Achievement_Rate': 'Achievement Rate (%)'},
        color='Achievement_Rate',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400
    )
    
    return fig

# ============================================================================
# MAIN DASHBOARD LAYOUT
# ============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Sales Performance Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.markdown('<h2 class="sub-header">🔍 Filters</h2>', unsafe_allow_html=True)
    
    # Area filter
    areas = ['All'] + sorted(df['Area'].unique().tolist())
    selected_area = st.sidebar.selectbox('Select Area:', areas)
    
    # Grade filter
    grades = ['All'] + sorted(df['Grade'].unique().tolist())
    selected_grade = st.sidebar.selectbox('Select Grade:', grades)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_area != 'All':
        filtered_df = filtered_df[filtered_df['Area'] == selected_area]
    if selected_grade != 'All':
        filtered_df = filtered_df[filtered_df['Grade'] == selected_grade]
    
    # Calculate metrics
    metrics = calculate_team_metrics(filtered_df)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Team Size", metrics['total_team_size'])
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Sales", f"{metrics['total_sales']:,}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Achievement Rate", f"{metrics['overall_achievement']}%")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Performance", f"{metrics['avg_individual_performance']}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_performance = create_performance_chart(filtered_df)
        st.plotly_chart(fig_performance, use_container_width=True)
    
    with col2:
        if selected_area == 'All':
            fig_area = create_area_comparison_chart(filtered_df)
            st.plotly_chart(fig_area, use_container_width=True)
        else:
            fig_performance_dist = px.histogram(
                filtered_df, 
                x='Percentage', 
                title=f"Performance Distribution - {selected_area}",
                nbins=20
            )
            st.plotly_chart(fig_performance_dist, use_container_width=True)
    
    # Detailed data table
    st.markdown('<h2 class="sub-header">📋 Detailed Performance Data</h2>', unsafe_allow_html=True)
    
    display_df = filtered_df[['Area', 'SubArea', 'Nama', 'Grade', 'Target', 'Sales', 'Minus/plus', 'Percentage', 'Performance_Category']].copy()
    display_df.columns = ['Area', 'SubArea', 'Name', 'Grade', 'Target', 'Sales', 'Variance', 'Achievement %', 'Performance']
    
    st.dataframe(
        display_df.sort_values('Achievement %', ascending=False),
        use_container_width=True,
        height=400
    )
    
    # Performance insights
    st.markdown('<h2 class="sub-header">💡 Performance Insights</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top Performers:**")
        if metrics['top_performer'] != 'N/A':
            st.write(f"🏆 {metrics['top_performer']}: {metrics['top_performance']}%")
        
        st.markdown("**Team Composition:**")
        st.write(f"⭐ Excellent: {metrics['excellent_performers']}")
        st.write(f"✅ Good: {metrics['good_performers']}")
        st.write(f"📊 Average/Below: {len(filtered_df) - metrics['excellent_performers'] - metrics['good_performers']}")
    
    with col2:
        st.markdown("**Areas for Improvement:**")
        if metrics['bottom_performer'] != 'N/A' and metrics['bottom_performance'] < 80:
            st.write(f"🔴 {metrics['bottom_performer']}: {metrics['bottom_performance']}%")
        
        st.markdown("**Performance Statistics:**")
        st.write(f"📈 Standard Deviation: {metrics['performance_std']}%")
        st.write(f"❌ Zero Sales: {metrics['zero_sales_count']}")
        st.write(f"📉 Needs Improvement (<80%): {metrics['needs_improvement']}")

if __name__ == "__main__":
    main()