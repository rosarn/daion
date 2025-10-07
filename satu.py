"""
============================================================================
SALES PERFORMANCE ANALYTICS DASHBOARD
============================================================================

Author: Data Analyst Team
Version: 2.0 (Enhanced with Best Practices)
Data Period: Juli-Agustus 2024
Business Context: Multi-area sales performance tracking and optimization
Technical Stack: Streamlit, Plotly, Pandas

DATA ANALYST NOTES:
==================
- Enhanced dashboard with improved performance and user experience
- Implements Streamlit best practices for production deployment
- Optimized data processing with efficient caching strategies
- Professional UI/UX design with responsive layout
- Advanced analytics with predictive insights
- Real-time filtering and interactive visualizations
- Export capabilities for further analysis
- Mobile-responsive design for field access
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
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION AND SETUP
# ============================================================================

# DATA ANALYST SETUP:
# ==================
# Configure Streamlit page with professional settings for business dashboard
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

# DATA ANALYST UI/UX:
# ==================
# Professional styling for business dashboard with improved readability
st.markdown("""
<style>
    /* Main Dashboard Styling */
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
    
    /* Enhanced Metric Cards */
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
    
    /* Performance Status Colors */
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
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Data Table Styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Alert Boxes */
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
    
    /* Footer Styling */
    .footer {
        text-align: center;
        color: #6c757d;
        font-style: italic;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #dee2e6;
    }
    
    /* Loading Animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    
    /* Responsive Design */
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

@st.cache_data(ttl=3600)  # Cache for 1 hour for better performance
def load_data() -> pd.DataFrame:
    """
    DATA ANALYST FUNCTION: Load and process sales performance data
    
    Returns:
        pd.DataFrame: Processed sales data with calculated metrics
        
    Features:
        - Efficient data loading with caching
        - Comprehensive data validation
        - Advanced metric calculations
        - Performance categorization
        - Data quality checks
    """
    
    # RAW DATA STRUCTURE:
    # ==================
    # Multi-area sales team data with hierarchical organization
    complete_data = {
        # AREA CLASSIFICATION:
        # ===================
        # Primary market territories for strategic analysis
        'Area': (['Ciputat']*16 + ['Kab Tangerang']*9 + ['Kota Tangerang Poris']*10 + 
                 ['Jakarta']*26 + ['Depok']*22 + ['Cengkareng']*1 + ['Klapanunggal']*8 + ['Cileungsi']*6 + ['Parung']*7 + ['Tambun']*8 +
                 ['Serang']*13 + ['Cilegon']*6 + ['Kab Pandeglang']*6 +
                 ['Semarang']*52 + ['Kendal']*13 + ['Demak']*12 + ['Kudus']*4 + ['Cilacap']*14 + ['Kebumen']*9 + ['Purwokerto']*5 +
                 ['Tegal']*10 + ['Solo']*26 + ['Klaten']*9 + ['Jogja']*23 + ['Tasikmalaya']*20 + ['Kab Tasik']*6),
        
        # SUB-AREA CLASSIFICATION:
        # =======================
        # Detailed territory mapping for granular analysis
        'SubArea': (['Ciputat']*16 + ['Kab Tangerang']*9 + ['Kota Tangerang Poris']*10 + 
                    ['Jakarta']*26 + ['Depok']*22 + ['Cengkareng']*1 + 
                    ['Bogor - Klapanunggal']*8 + ['Bogor - Cileungsi']*6 + ['Bogor - Parung']*7 + ['Bogor - Tambun']*8 + 
                    ['Banten - Serang']*13 + ['Banten - Cilegon']*6 + ['Banten - Kab Pandeglang']*6 + 
                    ['Semarang']*52 + ['Kendal']*13 + ['Demak']*12 + ['Kudus']*4 + ['Cilacap']*14 + ['Kebumen']*9 + ['Purwokerto']*5 +
                    ['Tegal']*10 + ['Solo']*26 + ['Klaten']*9 + ['Jogja']*23 + ['Tasikmalaya']*20 + ['Kab Tasik']*6),
        
        # TEAM MEMBER IDENTIFICATION:
        # ===========================
        # Complete roster with individual performance tracking
        'Nama': [
            # Ciputat Team (16 members) - Urban market specialists
            'BUDI SAMBODO', 'MUHAMMAD SETIAWAN', 'MUHAMMAD NOVAL RAMADHAN', 'UKASAH',
            'WIDI WIDAYAT', 'ERLAND ERLANGGA', 'MUHAMAD RISKI', 'MELINA',
            'MONALISA SIPAHUTAR', 'SUDARMANTO', 'SELLA RIZKIA', 'APRINA SIAGIAN',
            'DIAN SRI ANDRYANI', 'SELSA BELLA HUTABARAT', 'NEINAH DAMAISARI', 'MIKA WANTI NAINGGOLAN',
            # Kab Tangerang Team (9 members) - Suburban territory
            'SUHARDIANSYAH', 'DEA MAULIDAH', 'M AZRIEL HAZNAM S', 'AYULIA KHAERUNNISA',
            'RAHMAWATI', 'RIZAL FAUZI', 'FIGH TRI OKTAVIANO', 'SITI HARDIANTI', 'INE LUTFIA NOVELLA', 
            # Kota Tangerang Poris Team (10 members) - Commercial district
            'DANIEL MATIUS KOLONDAM', 'ARYA DILLA', 'GALIH KURNIAWAN', 'ZULHAM REINALLDO',
            'DITA CAHYANI', 'INDAH NOVIYANTI', 'BUKHORI', 'M SOLEH', 'SUGANDA MS', 'IQBAL FADILAH',
            
            # Jakarta Team (26 members) - Premium market segment
            'Santoso Nainggolan', 'Daniel Parlindungan', 'Santo Yahya Purba', 'Ibbe Arfiah Ambarita',
            'Ninton Silitonga', 'Irwan Panjaitan', 'Ignatius Romy Setyawan', 'Rokhyati BT Wain',
            'Hendrik Pandapotan', 'Juwisri Mariati Simanjuntak', 'Lely Meyana', 'Daniel Toni Sagala',
            'Bastian Ronaldo Butar Butar', 'Maryanti Manalu', 'Fadli Syawalludin', 'Dimposma Hutagalung',
            'Leo Hermansyah', 'Alvin Jon Raya S', 'Julietta Winar Pasha', 'Hinando Praya Saragih',
            'Suriati T.Situmeang', 'Rani Martina Samosir', 'Bruno Mario', 'Moh Marifan Delavena',
            'Indrah Septian', 'Irwanto',
            
            # Depok Team (22 members) - Suburban mixed market
            'Fanda Waty Sry Ayu manalu', 'Gresintia Samosir', 'Sari Nopita Sipahutar', 'Douglas sinaga',
            'Delima Sihotang', 'Muhammad Hilmy', 'Kautsar', 'Raga Purnomo', 'Melyana Samosir',
            'Nova Indriani', 'Nanda Amalia Febriani', 'Lewi Indriyani Panggabean', 'Haryanti',
            'Lia Rahmawati', 'Yandira Cahaya Putri', 'Abdul zaki', 'Indah Fitria', 'Bayu Utomo',
            'Asya Amalia', 'Rafika Khoirul', 'Herdiansyah', 'Muhammad Rifal',
            
            # Cengkareng Team (1 member) - Strategic outpost
            'Muhammad Nur Zaman Akbar',
            
            # Bogor Regional Teams - Emerging markets
            # Klapanunggal (8 members) - Growth territory
            'SUSANTO HIDAYAT', 'IMEY MELIAWATI', 'ATMA HAYYU FTIRIANTI', 'WIDYA RAHMA',
            'DHEA APRILIA', 'VELY FRIYANTI DJOHAN', 'LUBIS SUGARA', 'HAPITZA ALBAR',
            # Cileungsi (6 members) - Development zone
            'WILSON MANALU', 'DEAREN HEAZEL REVIALY', 'SUMIATI', 'IRA ISMAYA',
            'RISKA TASYA MONTANIA GIRSANG', 'YOGI AGUS RANDA',
            # Parung (7 members) - Expansion area
            'SUKMA ANJALI', 'Muhamad dapa Al rasid', 'Rafly Ilham ramadhan', 'abyan aryan saputra',
            'Ratna Tusyadiyah', 'Friska Olivia Sihaloho', 'DEVI ANDRIANI',
            # Tambun (8 members) - New market penetration
            'Binsar Sudarmono Situmorang', 'Mayang Putri Emaliana', 'Exaudi Parulian Situmorang',
            'Marliana', 'Boyke Suhendra', 'Nahum Winardi putra Situmorang', 'Nunung septiani',
            'Afifahtul Khusnul Khatimah',

             # BANTEN - SERANG (13 members)
            'ABDUL RACHIM', 'SRI LESTARI BUTAR BUTAR', 'PURWANTO', 'SUTRISNO', 'NYOTO', 
            'ROHMAN', 'JAFAR SIDIK', 'DAFFALDA KRISMONICA SEPTIA', 'OSRA ADRIZAL', 
            'DENITA HULU', 'AHMAD YANI', 'JALALUDIN', 'ARIF PERMANA',
            # BANTEN - CILEGON (6 members)
            'SHODIK BAGUS SETIAWAN', 'DWI EGA PAMUNGKAS', 'ALVIAR YOKA PRATAMA', 
            'M FAZRIL DARUSSALAM', 'NURMALASARI', 'DIMAS ADIANTO',
            # BANTEN - KAB PANDEGLANG (6 members)
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

            #Kendal 13 members
            'MASHUDI', 'Hendrik Prasetyo', 'Rizky Akbarudin', 'Sigit Fendian Oktavianto', 
            'Firdaus Koban', 'Fatahuya alim', 'Catur setyawati', 'Ainus safin', 
            'ANUGRAH CAHYO WARDIYANTANTO', 'Mega Kristiawan', 'Ahmad Mustofa Habib', 
            'Yonatan Nurwidiastoni', 'Diah perdana yulianingrum',
            #Demak 12 members
            'AGUNG SUGIARTO', 'Dika Catur Susilo', 'Ahsanul Khuluk', 'Anita Noviani', 
            'Muhammad Afifuddin', 'Septi prima Aretha', 'TRIAS PUSPITASARI', 'Hendra', 
            'Angga Erwanto', 'Mohamad samsuri', 'Nur Fattah Robi Damara', 'Rio priambodo',
            #Kudus 4 members
            'Achmad Sahlan Chafid', 'Syahrul Ramadhan', 'Rizky Rimayandi Oktiawan', 'Afifah Nilam Sari',

            #Cilacap 14 members
            'AGUS WIDODO CILACAP', 'ANGGIA IKMA DEWI', 'HENDRI LISTIONO', 'SARWOTO',
            'SHERENITA TRIAS YULIANA', 'DWI JAYANTI LESTARI', 'BAYU PAMBUDI CILACAP',
            'LINDA PANGESTIKA', 'AJI PRAYOGA', 'RIZKI WINDU SANCOYO', 'LUKIS RUCIRA ARUNDATI',
            'PUPUT FARIDA', 'AWALIAH ZULFA TURROHMAH', 'DWIKI DARMAYUDA',
            #Kebumen 9 members
            'DONNY DHARMAWAN', 'ARIF PRIYANTORO KEBUMEN', 'SLAMET ARIFIN', 'TEGUH PRIHANTO',
            'SAEFUL AZIZ', 'SOLIHAT SOBARI', 'AMAD SAEFUDIN', 'ACHMAD BUDIMAN', 'AHMAD RUBIANTO',
            #Purwokerto 5 members
            'PANDU DWI KUSUMA PURWOKERTO', 'SIGIT PUJI ASTUTI', 'ASNI ALIFATUN NIDA',
            'DIKA RIZKI ABADI', 'EGA HUTARA PUTRA',

            #Tegal 10 members
            'PRASTIKA WIGATINING PANGESTUTI', 'HAMZAH FAHMI', 'LATHIF MUTTAQIN', 'HIJRAH SABILA',
            'KHADZIQUL HUMAM MUNFI', 'FAUZAN MAULANA ADI', 'MITA LESTARI', 'Eko Krismanto',
            'MOHAMAD IMRON, AMDS', 'MOHAMMAD KAMAL BUSTAMI',

            #Solo 26 members 
            'ANSI PUTRI LORENZA', 'RYAN PRAMASDA PUTRA', 'BUDI KRISTIAWAN', 'GUGUT JULI PRAYITNO',
            'SISWANTI', 'RAHMA PRASETYAWATI', 'MARIA AVIANTI', 'JOKO BINTORO', 'AWAN AFANOVA',
            'ANTIK SULISTYOWATI', 'SUGIYONO', 'TRI HARYANTO', 'SUSILO', 'IMAM MULADI', 'YULIANTO',
            'MIFTA HASBI HARIRI', 'HERPRATAMA INDRO SETYAJATI', 'M SULTAN FAHMI FIRMANSYAH',
            'DANANG SETYAWAN', 'DENY AJI WIBOWO', 'ARIF NUGROHO', 'MUHAMMAD DLUNUROEN',
            'RIZKI BETA KURNIAWAN', 'EDWIN CHRISTIAN ISHUANTO', 'SAPTOTO WAHYU NUGROHO',
            'DODY WAHYU PRANOTO, SE',

            #Klaten  9 members
            'MUAMMAL IQBAL', 'IMAM BAGUS FAISAL', 'FENDI YULIYANTO', 'HARIYANTO',
            'ARCELA', 'ADITYA DANAR SAPUTRA', 'SALSA NUR FITRIA', 'BEASTRICE ARUM SEKARWANGI',
            'TOTOK YUNUS WEDIYANTO',

            #Jogja 23 members
            'THERESIA OKTAVIA', 'SAFII', 'MUHAMAD IKSAN', 'DINA LISTIANA', 'ANDEG LALA',
            'MIRA SUKMA DEWI ISKANDAR PUTRI', 'MUHAMMAD RIZKY EKA PUTRA', 'RIMA TRILIA FIKA SARI',
            'DEMISA ZAI', 'NUR HIDAYAT SULISTYA', 'CHARISMA PRIYA PURNOMO', 'ESTHI NUGROHO DEWI',
            'MARYADI', 'DANIEL TUMANAN', 'RIO MARTIN RUDIANTO', 'SUMARYADI', 'AHLISH HIDAYATULLOH',
            'YOGI PUTRO WASKITO', 'ARIS KURNIANTORO', 'RORI PUJI ASTUTI', 'NOVI EFENDI',
            'MATIAS NOPRYANTO RAUNGKU', 'R. SUHARJONO',

            #Tasikmalaya 20 members
            'Bangbang Himun H, S.Kom', 'Hengki Permana', 'Ahmad Syahriar Irawan', 'Falhan Basya',
            'Hendra Irawan', 'Dayu Gapura Irianto', 'Raisa Siti Ainiyah', 'Hendar Suhendar',
            'Davin Alim', 'Agung Dwi Laksono', 'Ari Hidayat', 'Cucu Komarudin', 'Berent Fariz',
            'Muhammad Fajar Siddiq', 'Entis', 'Dadang Dimyati', 'Dicky Fauzi Nurhidayat',
            'Veri Septiana', 'Piki Badarudin', 'Acep Rizal',
            #Kab Tasik 6 members
            'Iman Firman', 'Dian Hernanda', 'Trisna Juliansyah', 'Abdul Koharudin',
            'Dasep Abdul Gopur', 'Rudiansyah Moch Azhar'
        ],
        
        # ROLE CLASSIFICATION:
        # ===================
        # Hierarchical structure: SPV (Supervisor), S2 (Senior Sales), DS (Direct Sales)
        'Grade': (['SPV'] + ['DS']*15 + ['SPV'] + ['DS']*8 + ['SPV'] + ['DS']*9 +
                  ['SPV'] + ['S2']*25 + ['SPV'] + ['S2']*21 + ['S2']*1 +
                  ['SPV'] + ['S2']*7 + ['SPV'] + ['S2']*5 + ['S2']*7 + ['SPV'] + ['S2']*7 + ['SPV'] + ['DS']*12 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 +
                  ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*6 + ['SPV'] + ['DS']*4 + ['SPV'] + ['DS']*6 + ['SPV'] + ['DS']*4 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 + #semarang
                  ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*4 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 + ['DS']*4  + #KendalDemakKudus
                  #CilacapKebumenPurwokerto
                  ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*7 + ['SPV']*2 + ['DS']*7 + ['SPV'] + ['DS']*4 +
                  ['SPV'] + ['DS']*9 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*8 + ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*6 + ['SPV'] + ['DS']*7 + #TegalSoloKlatenJogja
                  ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*5 #TasikmlayaKabTasik
                  ),
        
        # TARGET ALLOCATION:
        # =================
        # Role-based target setting aligned with market potential and experience level
        'Target': ([35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,25,
                    35,25,25,25,25,25,25,25,25,25] +
                   [35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,25,25] +
                   [35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,35,25,25,25,25,25] +
                   [25] +
                   [35,25,25,25,25,25,25,25] +
                   [35,25,25,25,25,25] +
                   [25,25,25,25,25,25,25] +
                   [35,25,25,25,25,25,25,25] +
                     # BANTEN AREA
                    [35,25,25,25,25,25,25,25,35,25,25,25,25] +
                    [35,25,25,25,25,25] +
                    [35,25,25,25,25,25] +
                    # Seamarang
                    [35, 25, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 
                    25, 25, 25, 35, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 
                    35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25] +
                    #KendalDemakKudus
                    [35, 25, 25, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25] + [35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25] + [25, 25, 25, 25] +
                    #CilacapKebumenPurwokerto
                    [35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 25] + [35, 25, 25, 25, 25, 25, 25, 25, 25] + [35, 25, 25, 25, 25] +
                    #TegalSoloKlatenJogja
                    [35, 25, 25, 25, 25, 25, 25, 25, 25, 25] + 
                    [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25] +
                    [25, 25, 25, 25, 25, 25, 25, 25, 25] +
                    [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25] +
                    #TasikmalayaKabTasik
                    [35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 35, 25, 25, 25, 25, 25, 25, 25] + [35, 25, 25, 25, 25, 25] 
                    ),
    
        # ACTUAL SALES ACHIEVEMENT:
        # ========================
        # Performance data reflecting market conditions and individual capabilities
        'Sales': ([32,22,18,20,28,15,30,12,38,28,22,15,18,20,25,22,28,20,15,18,22,25,28,20,15,
                   30,18,22,25,28,20,15,18,22,25] +
                    [28,20,15,18,22,25,28,20,15,18,22,25,28,20,15,18,22,25,28,20,15,18,22,25,28,20] +
                    [25,18,22,25,28,20,15,18,22,25,28,20,15,18,22,25,28,20,15,18,22,25] + [20] +
                    [30,22,18,25,28,20,15,22] + [28,20,15,18,22,25] + [18,22,25,28,20,15,18] + [32,25,18,22,28,20,15,25] +  # BANTEN AREA
                    [7,20,19,20,13,9,5,15,8,22,19,19,25] +  # Serang
                    [8,25,27,31,8,4] +  # Cilegon
                    [36,2,25,16,1,20] +  # Kab Pandeglang
                    [0, 73, 19, 46, 28, 43, 25, 28, 0, 41, 60, 43, 22, 25, 14, 18, 0, 24, 22, 22, 
                    91, 18, 19, 29, 37, 37, 36, 19, 7, 27, 35, 14, 19, 44, 1, 13, 57, 26, 28, 26, 
                    18, 20, 22, 17, 32, 17, 5, 19, 33, 11, 2, 14] +  #Semarang
                    [9, 45, 23, 92, 20, 14, 10, 7, 18, 19, 20, 25, 10] + [29, 30, 17, 12, 18, 10, 16, 11, 15, 14, 1, 1] + [16, 17, 16, 1] + #KendalDemakKudus
                    [0, 37, 14, 36, 28, 4, 4, 40, 25, 12, 20, 6, 6, 9] + [2, 6, 27, 25, 16, 11, 0, 0, 0] + [0, 36, 14, 7, 1] + #CilacapKebumenPPurwokerto
                    [0, 36, 41, 35, 21, 31, 14, 22, 3, 3] + [0, 57, 10, 11, 12, 9, 0, 13, 19, 8, 31, 9, 0, 26, 21, 12, 2, 2, 0, 12, 1, 2, 20, 3, 0, 3] +
                    [10, 10, 17, 13, 17, 3, 4, 5, 1] + [0, 18, 12, 11, 15, 12, 7, 5, 0, 13, 26, 10, 3, 1, 9, 0, 49, 13, 14, 12, 18, 11, 10] + #TegalSoloKlatenJogja
                    [0, 61, 25, 6, 18, 3, 2, 28, 34, 31, 29, 21, 1, 25, 32, 32, 36, 25, 28, 34] + [0, 38, 15, 36, 22, 15] #TasikmalayaKabTasik
                )
    }

    # DATA PROCESSING & ANALYTICS:
    # ============================
    # Convert to DataFrame for advanced analytics
    df = pd.DataFrame(complete_data)
    
    # PERFORMANCE VARIANCE CALCULATION:
    # ================================
    # Calculate gap between target and actual performance
    df['Minus/plus'] = df['Sales'] - df['Target']
    
    # ACHIEVEMENT PERCENTAGE:
    # ======================
    # Performance ratio as percentage for standardized comparison
    df['Percentage'] = (df['Sales'] / df['Target'] * 100).round(2)
    
    # PERFORMANCE CATEGORIZATION:
    # ==========================
    # Strategic classification for management insights
    def categorize_performance(percentage):
        """
        Categorize performance based on achievement percentage
        - Excellent: ≥120% (Exceeds expectations significantly)
        - Good: 100-119% (Meets/exceeds target)
        - Average: 80-99% (Close to target)
        - Below Average: 60-79% (Needs improvement)
        - Poor: <60% (Requires immediate attention)
        """
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
    
    # DATA QUALITY VALIDATION:
    # =======================
    # Ensure data integrity and consistency
    expected_count = len(complete_data['Nama'])
    assert len(df) == expected_count, f"Expected {expected_count} records, got {len(df)}"
    assert df['Target'].min() > 0, "All targets must be positive"
    assert df['Sales'].min() >= 0, "Sales cannot be negative"
    
    return df

# ADVANCED ANALYTICS FUNCTIONS:
# =============================

def calculate_team_metrics(df):

    """
    Calculate comprehensive team performance metrics
    Returns: Dictionary with key performance indicators
    """
    metrics = {
        'total_team_size': len(df),
        'total_target': df['Target'].sum(),
        'total_sales': df['Sales'].sum(),
        'overall_achievement': (df['Sales'].sum() / df['Target'].sum() * 100).round(2),
        'avg_individual_performance': df['Percentage'].mean().round(2),
        'performance_std': df['Percentage'].std().round(2),
        'top_performer': df.loc[df['Percentage'].idxmax(), 'Nama'],
        'top_performance': df['Percentage'].max(),
        'bottom_performer': df.loc[df['Percentage'].idxmin(), 'Nama'],
        'bottom_performance': df['Percentage'].min(),
        'zero_sales_count': len(df[df['Sales'] == 0]),
        'excellent_performers': len(df[df['Performance_Category'] == 'Excellent']),
        'good_performers': len(df[df['Performance_Category'] == 'Good']),
        'needs_improvement': len(df[df['Performance_Category'].isin(['Below Average', 'Poor'])])
    }
    return metrics

def get_area_performance(df):
    """
    Analyze performance by geographical area
    Returns: DataFrame with area-level metrics
    """
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
    """
    Analyze performance by role/grade
    Returns: DataFrame with role-level insights
    """
    grade_stats = df.groupby('Grade').agg({
        'Target': ['sum', 'mean'],
        'Sales': ['sum', 'mean'],
        'Percentage': ['mean', 'std'],
        'Nama': 'count'
    }).round(2)
    
    grade_stats.columns = ['Total_Target', 'Avg_Target', 'Total_Sales', 'Avg_Sales', 'Avg_Performance', 'Performance_Std', 'Count']
    grade_stats['Achievement_Rate'] = (grade_stats['Total_Sales'] / grade_stats['Total_Target'] * 100).round(2)
    
    return grade_stats

# MAIN DASHBOARD EXECUTION:
# ========================

# Load and process data
data = load_data()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

# SIDEBAR CONFIGURATION:
# =====================
st.sidebar.header("🎯 Dashboard Controls")
st.sidebar.markdown("---")

# Advanced filtering options
st.sidebar.subheader("📊 Data Filters")

# Area filter with performance indicators
areas = ['All'] + sorted(data['Area'].unique().tolist())
area_performance = get_area_performance(data)
area_options = []
for area in areas:
    if area == 'All':
        area_options.append(area)
    else:
        perf = area_performance.loc[area, 'Achievement_Rate'] if area in area_performance.index else 0
        area_options.append(f"{area} ({perf:.1f}%)")

selected_area_display = st.sidebar.selectbox("📍 Pilih Area:", area_options)
selected_area = selected_area_display.split(' (')[0] if '(' in selected_area_display else selected_area_display

# Grade filter with team size info
grades = ['All'] + sorted(data['Grade'].unique().tolist())
grade_analysis = get_grade_analysis(data)
grade_options = []
for grade in grades:
    if grade == 'All':
        grade_options.append(grade)
    else:
        count = grade_analysis.loc[grade, 'Count'] if grade in grade_analysis.index else 0
        grade_options.append(f"{grade} ({int(count)} orang)")

selected_grade_display = st.sidebar.selectbox("👥 Pilih Grade:", grade_options)
selected_grade = selected_grade_display.split(' (')[0] if '(' in selected_grade_display else selected_grade_display

# Performance range filter
st.sidebar.subheader("🎯 Performance Range")
min_achievement = st.sidebar.slider("Minimum Achievement (%):", 0, 200, 0)
max_achievement = st.sidebar.slider("Maximum Achievement (%):", 0, 200, 200)

# Performance category filter
st.sidebar.subheader("📈 Performance Category")
categories = ['All'] + data['Performance_Category'].unique().tolist()
selected_category = st.sidebar.selectbox("Kategori Performance:", categories)

# Apply comprehensive filters
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

# Display filter summary
st.sidebar.markdown("---")
st.sidebar.subheader("📋 Filter Summary")
st.sidebar.info(f"""
**Data yang ditampilkan:**
- Total Records: {len(filtered_data):,}
- Area: {selected_area}
- Grade: {selected_grade}
- Performance: {min_achievement}% - {max_achievement}%
- Category: {selected_category}
""")

# MAIN DASHBOARD CONTENT:
# ======================
st.markdown('<div class="main-header">📊 Sales Performance Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown("**📅 Period: 21 Juli - 20 Agustus 2024 | 🎯 Enhanced Analytics Dashboard**")

# Calculate comprehensive metrics
team_metrics = calculate_team_metrics(filtered_data)

# ENHANCED KEY METRICS SECTION:
# ============================
st.subheader("🎯 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_sales = team_metrics['total_sales']
    total_target = team_metrics['total_target']
    achievement = team_metrics['overall_achievement']
    delta_color = "normal" if achievement >= 100 else "inverse"
    st.metric(
        "Overall Achievement", 
        f"{achievement:.1f}%", 
        f"{total_sales:,}/{total_target:,}",
        delta_color=delta_color
    )

with col2:
    avg_performance = team_metrics['avg_individual_performance']
    performance_std = team_metrics['performance_std']
    st.metric(
        "Average Performance", 
        f"{avg_performance:.1f}%",
        f"±{performance_std:.1f}% std"
    )

with col3:
    top_performance = team_metrics['top_performance']
    top_performer = team_metrics['top_performer']
    st.metric(
        "Top Performer", 
        f"{top_performance:.1f}%", 
        f"{top_performer[:15]}..."
    )

with col4:
    team_size = team_metrics['total_team_size']
    excellent_count = team_metrics['excellent_performers']
    st.metric(
        "Team Size", 
        f"{team_size} people",
        f"{excellent_count} excellent"
    )

with col5:
    zero_sales = team_metrics['zero_sales_count']
    needs_improvement = team_metrics['needs_improvement']
    st.metric(
        "Needs Attention", 
        f"{needs_improvement} people",
        f"{zero_sales} zero sales",
        delta_color="inverse" if needs_improvement > 0 else "normal"
    )

st.markdown("---")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🏆 Performers", "📋 Detailed Data", "🎯 Recommendations"])

with tab1:
    st.subheader("📊 Performance Overview & Analytics")
    
    # Enhanced area performance comparison
    col1, col2 = st.columns([2, 1])
    
    with col1:
        area_stats = get_area_performance(filtered_data)
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
        # Enhanced performance distribution
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
    
    # Enhanced Sales vs Target visualization
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
    
    # Grade performance analysis
    st.subheader("👥 Performance Analysis by Grade")
    grade_stats = get_grade_analysis(filtered_data)
    grade_stats_reset = grade_stats.reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_grade = px.bar(
            grade_stats_reset,
            x='Grade',
            y='Achievement_Rate',
            title='Achievement Rate by Grade',
            color='Achievement_Rate',
            color_continuous_scale='Viridis',
            text='Achievement_Rate'
        )
        fig_grade.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_grade, use_container_width=True)
    
    with col2:
        fig_scatter_grade = px.scatter(
            grade_stats_reset,
            x='Avg_Target',
            y='Avg_Sales',
            size='Count',
            color='Grade',
            title='Average Target vs Sales by Grade',
            hover_data=['Achievement_Rate']
        )
        # Add diagonal line for 100% achievement
        max_val = max(grade_stats_reset['Avg_Target'].max(), grade_stats_reset['Avg_Sales'].max())
        fig_scatter_grade.add_trace(go.Scatter(
            x=[0, max_val], 
            y=[0, max_val],
            mode='lines', 
            name='100% Line',
            line=dict(dash='dash', color='red')
        ))
        st.plotly_chart(fig_scatter_grade, use_container_width=True)

with tab2:
    st.subheader("🏆 Top Performers Analysis & Insights")
    
    # Performance summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        excellent_performers = len(filtered_data[filtered_data['Performance_Category'] == 'Excellent'])
        st.metric("Excellent Performers", excellent_performers, f"{excellent_performers/len(filtered_data)*100:.1f}%")
    
    with col2:
        good_performers = len(filtered_data[filtered_data['Performance_Category'] == 'Good'])
        st.metric("Good Performers", good_performers, f"{good_performers/len(filtered_data)*100:.1f}%")
    
    with col3:
        avg_performers = len(filtered_data[filtered_data['Performance_Category'] == 'Average'])
        st.metric("Average Performers", avg_performers, f"{avg_performers/len(filtered_data)*100:.1f}%")
    
    with col4:
        poor_performers = len(filtered_data[filtered_data['Performance_Category'].isin(['Below Average', 'Poor'])])
        st.metric("Needs Improvement", poor_performers, f"{poor_performers/len(filtered_data)*100:.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Top 10 performers
        top_10 = filtered_data.nlargest(10, 'Percentage')[['Nama', 'SubArea', 'Grade', 'Sales', 'Target', 'Percentage', 'Performance_Category']]
        st.write("**🏅 Top 10 Performers:**")
        
        # Style the dataframe with colors
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
        # Enhanced Bottom 10 performers
        bottom_10 = filtered_data.nsmallest(10, 'Percentage')[['Nama', 'SubArea', 'Grade', 'Sales', 'Target', 'Percentage', 'Performance_Category']]
        st.write("**⚠️ Bottom 10 Performers:**")
        
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
    
    # Enhanced Performance scatter plot
    st.subheader("📊 Performance Scatter Analysis")
    
    fig_scatter = px.scatter(
        filtered_data, 
        x='Target', 
        y='Sales', 
        color='Performance_Category', 
        size='Percentage',
        hover_data=['Nama', 'SubArea', 'Grade'],
        title='Performance Scatter Plot: Target vs Sales (Colored by Performance Category)',
        color_discrete_map={
            'Excellent': '#28a745',
            'Good': '#17a2b8', 
            'Average': '#ffc107',
            'Below Average': '#fd7e14',
            'Poor': '#dc3545'
        }
    )
    
    # Add target achievement line
    max_target = filtered_data['Target'].max()
    fig_scatter.add_trace(go.Scatter(
        x=[0, max_target], 
        y=[0, max_target],
        mode='lines', 
        name='100% Achievement Line',
        line=dict(dash='dash', color='red', width=2)
    ))
    
    fig_scatter.update_layout(
        xaxis_title="Target",
        yaxis_title="Sales Achievement",
        height=600
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Performance distribution by area
    st.subheader("🌍 Performance Distribution by Area")
    
    area_performance_dist = filtered_data.groupby(['Area', 'Performance_Category']).size().unstack(fill_value=0)
    
    fig_stacked = px.bar(
        area_performance_dist.reset_index(),
        x='Area',
        y=['Excellent', 'Good', 'Average', 'Below Average', 'Poor'],
        title='Performance Category Distribution by Area',
        color_discrete_map={
            'Excellent': '#28a745',
            'Good': '#17a2b8', 
            'Average': '#ffc107',
            'Below Average': '#fd7e14',
            'Poor': '#dc3545'
        }
    )
    
    fig_stacked.update_layout(
        barmode='stack',
        xaxis_title="Area",
        yaxis_title="Number of People",
        height=400
    )
    
    st.plotly_chart(fig_stacked, use_container_width=True)

with tab3:
    st.subheader("📋 Detailed Data View & Analysis")
    
    # Enhanced search and filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        search_name = st.text_input("🔍 Search by Name:")
    with col2:
        sort_by = st.selectbox("📊 Sort by:", [
            'Percentage DESC', 'Percentage ASC', 
            'Sales DESC', 'Sales ASC',
            'Target DESC', 'Target ASC',
            'Name A-Z', 'Name Z-A',
            'Area A-Z'
        ])
    with col3:
        export_format = st.selectbox("📤 Export Format:", ['View Only', 'CSV Download', 'Excel Download'])
    
    # Apply search filter
    display_df = filtered_data.copy()
    if search_name:
        display_df = display_df[display_df['Nama'].str.contains(search_name, case=False, na=False)]
    
    # Apply sorting
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
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Records Shown", len(display_df))
    with col2:
        avg_achievement = display_df['Percentage'].mean()
        st.metric("Avg Achievement", f"{avg_achievement:.1f}%")
    with col3:
        total_gap = display_df['Minus/plus'].sum()
        st.metric("Total Gap", f"{total_gap:+.0f}")
    with col4:
        achievement_rate = (display_df['Sales'].sum() / display_df['Target'].sum() * 100) if display_df['Target'].sum() > 0 else 0
        st.metric("Group Achievement", f"{achievement_rate:.1f}%")
    
    # Enhanced data display
    st.write(f"**📊 Showing {len(display_df)} of {len(filtered_data)} records**")
    
    # Create enhanced display columns
    display_columns = ['Nama', 'Area', 'SubArea', 'Grade', 'Target', 'Sales', 'Minus/plus', 'Percentage', 'Performance_Category']
    
    # Enhanced styling function
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
    
    # Export functionality
    if export_format == 'CSV Download':
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"sales_performance_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    elif export_format == 'Excel Download':
        # Note: This would require openpyxl or xlsxwriter
        st.info("📝 Excel export functionality requires additional libraries (openpyxl)")
    
    # Detailed statistics table
    st.subheader("📈 Statistical Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Performance Statistics:**")
        stats_df = pd.DataFrame({
            'Metric': ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max'],
            'Achievement %': [
                len(display_df),
                display_df['Percentage'].mean(),
                display_df['Percentage'].std(),
                display_df['Percentage'].min(),
                display_df['Percentage'].quantile(0.25),
                display_df['Percentage'].median(),
                display_df['Percentage'].quantile(0.75),
                display_df['Percentage'].max()
            ]
        })
        stats_df['Achievement %'] = stats_df['Achievement %'].round(2)
        st.dataframe(stats_df, use_container_width=True)
    
    with col2:
        st.write("**Performance Category Breakdown:**")
        category_counts = display_df['Performance_Category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        category_counts['Percentage'] = (category_counts['Count'] / len(display_df) * 100).round(1)
        st.dataframe(category_counts, use_container_width=True)

with tab4:
    st.subheader("🎯 Strategic Recommendations & Action Plans")
    
    # Generate comprehensive recommendations based on filtered data
    critical_areas = filtered_data.groupby('SubArea')['Percentage'].mean().nsmallest(3)
    best_areas = filtered_data.groupby('SubArea')['Percentage'].mean().nlargest(3)
    zero_sales = filtered_data[filtered_data['Sales'] == 0]
    medium_performers = filtered_data[(filtered_data['Percentage'] >= 50) & (filtered_data['Percentage'] < 80)]
    poor_performers = filtered_data[filtered_data['Performance_Category'].isin(['Below Average', 'Poor'])]
    excellent_performers = filtered_data[filtered_data['Performance_Category'] == 'Excellent']
    
    # Executive Summary
    st.markdown("### 📋 Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        overall_achievement = (filtered_data['Sales'].sum() / filtered_data['Target'].sum() * 100) if filtered_data['Target'].sum() > 0 else 0
        status = "🟢 Good" if overall_achievement >= 100 else "🟡 Needs Attention" if overall_achievement >= 80 else "🔴 Critical"
        st.metric("Overall Status", status, f"{overall_achievement:.1f}%")
    
    with col2:
        risk_level = len(poor_performers) / len(filtered_data) * 100 if len(filtered_data) > 0 else 0
        risk_status = "🔴 High" if risk_level > 30 else "🟡 Medium" if risk_level > 15 else "🟢 Low"
        st.metric("Risk Level", risk_status, f"{risk_level:.1f}%")
    
    with col3:
        improvement_potential = len(medium_performers)
        st.metric("Quick Wins", f"{improvement_potential} people", "Medium performers")
    
    with col4:
        benchmark_performers = len(excellent_performers)
        st.metric("Benchmarks", f"{benchmark_performers} people", "Excellent performers")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🔴 Immediate Priority Actions")
        
        if len(critical_areas) > 0:
            st.markdown(f"""
            **1. 🚨 Critical Areas Intervention:**
            - **{critical_areas.index[0]}**: {critical_areas.iloc[0]:.1f}% achievement
            - **{critical_areas.index[1] if len(critical_areas) > 1 else 'N/A'}**: {critical_areas.iloc[1]:.1f}% achievement
            - **{critical_areas.index[2] if len(critical_areas) > 2 else 'N/A'}**: {critical_areas.iloc[2]:.1f}% achievement
            
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
        
        if len(poor_performers) > 0:
            st.markdown(f"""
            **3. 📈 Performance Recovery Program:**
            - **{len(poor_performers)} people** need intensive support
            - Below 80% achievement threshold
            
            **📋 Action Items:**
            - Root cause analysis
            - Customized training programs
            - Weekly progress reviews
            """)
    
    with col2:
        st.write("### 🟢 Growth Opportunities & Best Practices")
        
        if len(best_areas) > 0:
            st.markdown(f"""
            **1. 🏆 Best Performing Areas (Benchmarks):**
            - **{best_areas.index[0]}**: {best_areas.iloc[0]:.1f}% achievement
            - **{best_areas.index[1] if len(best_areas) > 1 else 'N/A'}**: {best_areas.iloc[1]:.1f}% achievement
            - **{best_areas.index[2] if len(best_areas) > 2 else 'N/A'}**: {best_areas.iloc[2]:.1f}% achievement
            
            **📋 Action Items:**
            - Document success factors
            - Best practice sharing sessions
            - Cross-area mentoring program
            """)
        
        if len(medium_performers) > 0:
            st.markdown(f"""
            **2. 🎯 Quick Win Opportunities:**
            - **{len(medium_performers)} people** in 50-80% range
            - High potential for immediate improvement
            
            **📋 Action Items:**
            - Targeted skill development
            - Goal-setting workshops
            - Incentive program design
            """)
        
        if len(excellent_performers) > 0:
            st.markdown(f"""
            **3. 🌟 Excellence Amplification:**
            - **{len(excellent_performers)} people** exceeding targets
            - Potential team leaders and mentors
            
            **📋 Action Items:**
            - Recognition and rewards
            - Leadership development
            - Success story documentation
            """)
    
    # Enhanced Performance improvement analysis
    st.markdown("---")
    st.write("### 📊 Performance Improvement Potential Analysis")
    
    # Calculate improvement potential by area
    improvement_data = []
    for area in filtered_data['SubArea'].unique():
        area_data = filtered_data[filtered_data['SubArea'] == area]
        current_perf = area_data['Percentage'].mean()
        team_size = len(area_data)
        total_gap = area_data['Minus/plus'].sum()
        potential_revenue = abs(total_gap) if total_gap < 0 else 0
        
        improvement_data.append({
            'SubArea': area,
            'Current_Performance': current_perf,
            'Team_Size': team_size,
            'Performance_Gap': 100 - current_perf if current_perf < 100 else 0,
            'Revenue_Potential': potential_revenue,
            'Priority_Score': (100 - current_perf) * team_size if current_perf < 100 else 0
        })
    
    improvement_df = pd.DataFrame(improvement_data)
    improvement_df = improvement_df.sort_values('Priority_Score', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top improvement potential areas
        fig_improve = px.bar(
            improvement_df.head(8), 
            x='SubArea', 
            y='Priority_Score',
            color='Performance_Gap',
            title='🎯 Priority Areas for Improvement (Priority Score)',
            labels={'Priority_Score': 'Priority Score', 'Performance_Gap': 'Gap %'},
            color_continuous_scale='Reds'
        )
        fig_improve.update_layout(
            xaxis_tickangle=-45,
            height=400
        )
        st.plotly_chart(fig_improve, use_container_width=True)
    
    with col2:
        # Revenue potential analysis
        fig_revenue = px.scatter(
            improvement_df,
            x='Team_Size',
            y='Revenue_Potential',
            size='Priority_Score',
            color='Current_Performance',
            hover_data=['SubArea'],
            title='💰 Revenue Recovery Potential',
            labels={'Revenue_Potential': 'Potential Revenue Recovery', 'Team_Size': 'Team Size'},
            color_continuous_scale='RdYlGn'
        )
        fig_revenue.update_layout(height=400)
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Action plan timeline
    st.write("### 📅 Recommended Action Timeline")
    
    timeline_data = {
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Month 2', 'Month 3'],
        'Priority Actions': [
            '🚨 Address zero-sales performers',
            '📊 Implement daily tracking for critical areas', 
            '🎯 Launch quick-win coaching programs',
            '📈 Begin performance recovery programs',
            '🏆 Establish mentoring partnerships',
            '📋 Review and optimize based on results'
        ],
        'Expected Impact': ['Immediate', 'Short-term', 'Short-term', 'Medium-term', 'Long-term', 'Sustained']
    }
    
    timeline_df = pd.DataFrame(timeline_data)
    st.dataframe(timeline_df, use_container_width=True)
    
    # ROI Projection
    st.write("### 💹 Projected ROI from Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        potential_recovery = improvement_df['Revenue_Potential'].sum()
        st.metric("Potential Revenue Recovery", f"{potential_recovery:,.0f}", "From gap closure")
    
    with col2:
        quick_win_potential = len(medium_performers) * 5  # Assume 5 unit improvement per person
        st.metric("Quick Win Potential", f"{quick_win_potential:,.0f}", "From medium performers")
    
    with col3:
        total_potential = potential_recovery + quick_win_potential
        roi_percentage = (total_potential / filtered_data['Target'].sum() * 100) if filtered_data['Target'].sum() > 0 else 0
        st.metric("Total Improvement Potential", f"{roi_percentage:.1f}%", "Of current target")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <i>Dashboard updated automatically • Data period: 21 Juli - 20 Agustus 2024 • Last updated: {}</i>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)