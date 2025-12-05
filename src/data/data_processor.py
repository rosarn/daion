# src/data/data_processor.py
import streamlit as st
import pandas as pd
import numpy as np
import re
import openpyxl

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
    sample_areas = ['Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Semarang', 'Yogyakarta']
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
