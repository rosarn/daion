"""
============================================================================
DATA LOADER MODULE
============================================================================

Author: Data Analyst Team
Version: 2.0 (Restructured)
Purpose: Handle data loading, processing, and caching

This module contains:
- Data loading functions
- Data processing and transformation
- Caching mechanisms
- Raw data definitions
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from .models import validate_sales_data, categorize_performance


@st.cache_data(ttl=3600)  # Cache for 1 hour for better performance
def load_sales_data() -> pd.DataFrame:
    """
    Load and process sales performance data
    
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
    complete_data = _get_raw_data()
    
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
    df['Performance_Category'] = df['Percentage'].apply(categorize_performance)
    
    # DATA QUALITY VALIDATION:
    # =======================
    # Ensure data integrity and consistency
    validate_sales_data(df)
    
    return df


def _get_raw_data() -> Dict[str, List]:
    """
    Get raw sales data structure
    
    Returns:
        Dict[str, List]: Raw data dictionary with all sales information
    """
    return {
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
        'Nama': _get_team_members(),
        
        # ROLE CLASSIFICATION:
        # ===================
        # Hierarchical structure: SPV (Supervisor), S2 (Senior Sales), DS (Direct Sales)
        'Grade': _get_grades(),
        
        # TARGET ALLOCATION:
        # =================
        # Role-based target setting aligned with market potential and experience level
        'Target': _get_targets(),
        
        # ACTUAL SALES ACHIEVEMENT:
        # ========================
        # Performance data reflecting market conditions and individual capabilities
        'Sales': _get_sales_data()
    }


def _get_team_members() -> List[str]:
    """Get complete team member roster"""
    return [
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
    ]


def _get_grades() -> List[str]:
    """Get grade assignments for all team members"""
    return (['SPV'] + ['DS']*15 + ['SPV'] + ['DS']*8 + ['SPV'] + ['DS']*9 +
            ['SPV'] + ['S2']*25 + ['SPV'] + ['S2']*21 + ['S2']*1 +
            ['SPV'] + ['S2']*7 + ['SPV'] + ['S2']*5 + ['S2']*7 + ['SPV'] + ['S2']*7 + ['SPV'] + ['DS']*12 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 +
            ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*6 + ['SPV'] + ['DS']*4 + ['SPV'] + ['DS']*6 + ['SPV'] + ['DS']*4 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 + #semarang
            ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*4 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 + ['DS']*4  + #KendalDemakKudus
            #CilacapKebumenPurwokerto
            ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*7 + ['SPV']*2 + ['DS']*7 + ['SPV'] + ['DS']*4 +
            ['SPV'] + ['DS']*9 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*8 + ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*6 + ['SPV'] + ['DS']*7 + #TegalSoloKlatenJogja
            ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*5 + ['SPV'] + ['DS']*7 + ['SPV'] + ['DS']*5 #TasikmlayaKabTasik
            )


def _get_targets() -> List[int]:
    """Get target assignments for all team members"""
    return ([35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,25,
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
             )


def _get_sales_data() -> List[int]:
    """Get actual sales data for all team members"""
    return ([32,22,18,20,28,15,30,12,38,28,22,15,18,20,25,22,28,20,15,18,22,25,28,20,15,
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