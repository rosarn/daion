import streamlit as st
from src.language.language_config import get_text
from src.data.data_processor import process_uploaded_file, load_sample_data, extract_period_from_filename
from src.analytics.metrics import get_area_performance, get_grade_analysis

def render_sidebar():
    st.sidebar.header(f"🎯 {get_text('dashboard_controls')}")
    st.sidebar.markdown("---")

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

    st.sidebar.markdown("---")
    st.sidebar.subheader(f"📅 {get_text('period_config')}")

    bulan_list = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]

    col_per1, col_per2 = st.sidebar.columns(2)
    with col_per1:
        bulan_mulai = st.sidebar.selectbox(f"📍 {get_text('month_start')}:",
                                           bulan_list, index=6)
    with col_per2:
        bulan_akhir = st.sidebar.selectbox(f"📍 {get_text('month_end')}:",
                                           bulan_list, index=7)

    tahun = st.sidebar.selectbox(f"📅 {get_text('year')}:",
                                 [2023, 2024, 2025], index=1)

    if st.sidebar.button(f"🔄 {get_text('update_period')}"):
        manual_period = f"{bulan_mulai} - {bulan_akhir} {tahun}"
        st.session_state.periode_data = manual_period
        st.sidebar.success(f"✅ {get_text('period_updated')}: {manual_period}")

    st.sidebar.info(f"📊 {get_text('period_display')}: {st.session_state.periode_data}")

    # Filters
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

    selected_area_display = st.sidebar.selectbox(f"📍 {get_text('select_area')}:",
                                                 area_options)
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

    selected_grade_display = st.sidebar.selectbox(f"👥 {get_text('select_grade')}:",
                                                  grade_options)
    selected_grade = selected_grade_display.split(' (')[0] if '(' in selected_grade_display else selected_grade_display

    st.sidebar.subheader(f"🎯 {get_text('performance_range')}")
    min_achievement = st.sidebar.slider(f"📉 {get_text('min_achievement')}:",
                                       0, 200, 0)
    max_achievement = st.sidebar.slider(f"📈 {get_text('max_achievement')}:",
                                       0, 200, 200)

    st.sidebar.subheader(f"📈 {get_text('performance_category')}")
    categories = ['All'] + data['Performance_Category'].unique().tolist()
    selected_category = st.sidebar.selectbox(f"📊 {get_text('performance_category')}:",
                                             categories)

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

    # Filter summary
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

    # Download template
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
    import pandas as pd
    template_df = pd.DataFrame(template_data)
    csv_template = template_df.to_csv(index=False)
    st.sidebar.download_button(
        label=f"📋 {get_text('download_template')}",
        data=csv_template,
        file_name="sales_data_template.csv",
        mime="text/csv",
        help=f"📄 {get_text('download_help')}"
    )

    return data, filtered_data
