import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
    .positive { color: #00cc96; }
    .negative { color: #ef553b; }
    .warning { color: #ffa15a; }
</style>
""", unsafe_allow_html=True)

# Data Preparation Function
@st.cache_data
def load_data():
    complete_data = {
        'Area': (['Ciputat']*16 + ['Kab Tangerang']*9 + ['Kota Tangerang Poris']*10 + 
                 ['Jakarta']*26 + ['Depok']*22 + ['Cengkareng']*1 + 
                 ['Klapanunggal']*8 + ['Cileungsi']*6 + ['Parung']*7 + ['Tambun']*8),
        'SubArea': (['Ciputat']*16 + ['Kab Tangerang']*9 + ['Kota Tangerang Poris']*10 + 
                    ['Jakarta']*26 + ['Depok']*22 + ['Cengkareng']*1 + 
                    ['Bogor - Klapanunggal']*8 + ['Bogor - Cileungsi']*6 + 
                    ['Bogor - Parung']*7 + ['Bogor - Tambun']*8),
        'Nama': [
            # Ciputat
            'BUDI SAMBODO', 'MUHAMMAD SETIAWAN', 'MUHAMMAD NOVAL RAMADHAN', 'UKASAH',
            'WIDI WIDAYAT', 'ERLAND ERLANGGA', 'MUHAMAD RISKI', 'MELINA',
            'MONALISA SIPAHUTAR', 'SUDARMANTO', 'SELLA RIZKIA', 'APRINA SIAGIAN',
            'DIAN SRI ANDRYANI', 'SELSA BELLA HUTABARAT', 'NEINAH DAMAISARI', 'MIKA WANTI NAINGGOLAN',
            # Kab Tangerang
            'SUHARDIANSYAH', 'DEA MAULIDAH', 'M AZRIEL HAZNAM S', 'AYULIA KHAERUNNISA',
            'RAHMAWATI', 'RIZAL FAUZI', 'FIGH TRI OKTAVIANO', 'SITI HARDIANTI', 'INE LUTFIA NOVELLA',
            # Kota Tangerang Poris
            'DANIEL MATIUS KOLONDAM', 'ARYA DILLA', 'GALIH KURNIAWAN', 'ZULHAM REINALLDO',
            'DITA CAHYANI', 'INDAH NOVIYANTI', 'BUKHORI', 'M SOLEH', 'SUGANDA MS', 'IQBAL FADILAH',
            # Jakarta
            'Santoso Nainggolan', 'Daniel Parlindungan', 'Santo Yahya Purba', 'Ibbe Arfiah Ambarita',
            'Ninton Silitonga', 'Irwan Panjaitan', 'Ignatius Romy Setyawan', 'Rokhyati BT Wain',
            'Hendrik Pandapotan', 'Juwisri Mariati Simanjuntak', 'Lely Meyana', 'Daniel Toni Sagala',
            'Bastian Ronaldo Butar Butar', 'Maryanti Manalu', 'Fadli Syawalludin', 'Dimposma Hutagalung',
            'Leo Hermansyah', 'Alvin Jon Raya S', 'Julietta Winar Pasha', 'Hinando Praya Saragih',
            'Suriati T.Situmeang', 'Rani Martina Samosir', 'Bruno Mario', 'Moh Marifan Delavena',
            'Indrah Septian', 'Irwanto',
            # Depok
            'Fanda Waty Sry Ayu manalu', 'Gresintia Samosir', 'Sari Nopita Sipahutar', 'Douglas sinaga',
            'Delima Sihotang', 'Muhammad Hilmy', 'Kautsar', 'Raga Purnomo', 'Melyana Samosir',
            'Nova Indriani', 'Nanda Amalia Febriani', 'Lewi Indriyani Panggabean', 'Haryanti',
            'Lia Rahmawati', 'Yandira Cahaya Putri', 'Abdul zaki', 'Indah Fitria', 'Bayu Utomo',
            'Asya Amalia', 'Rafika Khoirul', 'Herdiansyah', 'Muhammad Rifal',
            # Cengkareng
            'Muhammad Nur Zaman Akbar',
            # Bogor - Klapanunggal
            'SUSANTO HIDAYAT', 'IMEY MELIAWATI', 'ATMA HAYYU FTIRIANTI', 'WIDYA RAHMA',
            'DHEA APRILIA', 'VELY FRIYANTI DJOHAN', 'LUBIS SUGARA', 'HAPITZA ALBAR',
            # Bogor - Cileungsi
            'WILSON MANALU', 'DEAREN HEAZEL REVIALY', 'SUMIATI', 'IRA ISMAYA',
            'RISKA TASYA MONTANIA GIRSANG', 'YOGI AGUS RANDA',
            # Bogor - Parung
            'SUKMA ANJALI', 'Muhamad dapa Al rasid', 'Rafly Ilham ramadhan', 'abyan aryan saputra',
            'Ratna Tusyadiyah', 'Friska Olivia Sihaloho', 'DEVI ANDRIANI',
            # Bogor - Tambun
            'Binsar Sudarmono Situmorang', 'Mayang Putri Emaliana', 'Exaudi Parulian Situmorang',
            'Marliana', 'Boyke Suhendra', 'Nahum Winardi putra Situmorang', 'Nunung septiani',
            'Afifahtul Khusnul Khatimah'
        ],
        'Grade': (['SPV'] + ['DS']*15 + ['SPV'] + ['DS']*8 + ['SPV'] + ['DS']*9 +
                  ['SPV'] + ['S2']*25 + ['SPV'] + ['S2']*21 + ['S2']*1 +
                  ['SPV'] + ['S2']*7 + ['SPV'] + ['S2']*5 + ['S2']*7 + ['SPV'] + ['S2']*7),
        'Target': ([35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,25,
                    35,25,25,25,25,25,25,25,25,25] +
                   [35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,25,25] +
                   [35,25,25,25,25,25,25,25,35,25,25,25,25,25,25,25,35,25,25,25,25,25] +
                   [25] +
                   [35,25,25,25,25,25,25,25] +
                   [35,25,25,25,25,25] +
                   [25,25,25,25,25,25,25] +
                   [35,25,25,25,25,25,25,25]),
        'Sales': ([10,20,21,14,23,10,12,3,2,23,22,20,32,24,6,5,0,26,32,28,5,2,0,5,2,
                   0,50,19,7,2,2,2,17,2,1] +
                  [7,24,24,17,7,26,18,0,14,30,25,21,17,15,10,3,17,24,13,22,16,15,1,1,1,2] +
                  [16,12,33,11,26,1,0,0,24,16,28,19,21,18,17,25,12,5,9,12,4,6] +
                  [0] +
                  [0,32,28,36,19,15,5,8] +
                  [0,28,27,45,23,29] +
                  [6,5,2,1,0,1,6] +
                  [16,28,23,35,17,21,14,2])
    }
    
    df = pd.DataFrame(complete_data)
    df['Minus/plus'] = df['Sales'] - df['Target']
    df['Percentage'] = (df['Sales'] / df['Target'] * 100).round(1)
    df['Performance_Category'] = pd.cut(df['Percentage'], 
                                      bins=[-1, 0, 50, 80, 100, 200],
                                      labels=['Zero', 'Low (<50%)', 'Medium (50-80%)', 'High (80-100%)', 'Excellent (>100%)'])
    
    return df

# Load data
df = load_data()

# Sidebar
st.sidebar.title("🔧 Filter Dashboard")
st.sidebar.markdown("---")

# Area filter
all_areas = ['All'] + sorted(df['Area'].unique())
selected_area = st.sidebar.selectbox("Select Area:", all_areas)

# Grade filter
all_grades = ['All'] + sorted(df['Grade'].unique())
selected_grade = st.sidebar.selectbox("Select Grade:", all_grades)

# Performance threshold
min_percentage = st.sidebar.slider("Minimum Achievement (%):", 0, 200, 0)

# Apply filters
filtered_df = df.copy()
if selected_area != 'All':
    filtered_df = filtered_df[filtered_df['Area'] == selected_area]
if selected_grade != 'All':
    filtered_df = filtered_df[filtered_df['Grade'] == selected_grade]
filtered_df = filtered_df[filtered_df['Percentage'] >= min_percentage]

# Main content
st.markdown('<div class="main-header">📊 Sales Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown("**Period: 21 Juli - 20 Agustus**")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df['Sales'].sum()
    total_target = filtered_df['Target'].sum()
    achievement = (total_sales / total_target * 100) if total_target > 0 else 0
    st.metric("Overall Achievement", f"{achievement:.1f}%", 
              f"{total_sales:,}/{total_target:,}")

with col2:
    avg_performance = filtered_df['Percentage'].mean()
    st.metric("Average Performance", f"{avg_performance:.1f}%")

with col3:
    top_performer = filtered_df.loc[filtered_df['Percentage'].idxmax()]
    st.metric("Top Performer", f"{top_performer['Percentage']:.1f}%", 
              f"{top_performer['Nama']}")

with col4:
    team_size = len(filtered_df)
    st.metric("Team Size", f"{team_size} people")

st.markdown("---")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🏆 Performers", "📋 Detailed Data", "🎯 Recommendations"])

with tab1:
    st.subheader("Performance Overview")
    
    # Area performance comparison
    col1, col2 = st.columns([2, 1])
    
    with col1:
        area_stats = filtered_df.groupby('Area').agg({
            'Sales': 'sum', 
            'Target': 'sum',
            'Percentage': 'mean'
        }).reset_index()
        area_stats['Achievement'] = (area_stats['Sales'] / area_stats['Target'] * 100).round(1)
        
        fig = px.bar(area_stats, x='Area', y='Achievement', 
                    title='Achievement by Area',
                    color='Achievement', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Performance distribution
        performance_dist = filtered_df['Performance_Category'].value_counts()
        fig_pie = px.pie(values=performance_dist.values, 
                        names=performance_dist.index,
                        title='Performance Distribution')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Sales vs Target by SubArea
    subarea_stats = filtered_df.groupby('SubArea').agg({'Sales': 'sum', 'Target': 'sum'}).reset_index()
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(name='Target', x=subarea_stats['SubArea'], y=subarea_stats['Target']))
    fig_bar.add_trace(go.Bar(name='Sales', x=subarea_stats['SubArea'], y=subarea_stats['Sales']))
    fig_bar.update_layout(title='Sales vs Target by Sub-Area', barmode='group')
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("Top Performers Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 performers
        top_10 = filtered_df.nlargest(10, 'Percentage')[['Nama', 'SubArea', 'Sales', 'Target', 'Percentage']]
        st.write("**🏅 Top 10 Performers:**")
        st.dataframe(top_10.style.format({
            'Sales': '{:.0f}',
            'Target': '{:.0f}', 
            'Percentage': '{:.1f}%'
        }), use_container_width=True)
    
    with col2:
        # Bottom 10 performers
        bottom_10 = filtered_df.nsmallest(10, 'Percentage')[['Nama', 'SubArea', 'Sales', 'Target', 'Percentage']]
        st.write("**⚠️ Bottom 10 Performers:**")
        st.dataframe(bottom_10.style.format({
            'Sales': '{:.0f}',
            'Target': '{:.0f}',
            'Percentage': '{:.1f}%'
        }), use_container_width=True)
    
    # Performance scatter plot
    fig_scatter = px.scatter(filtered_df, x='Target', y='Sales', 
                            color='Percentage', size='Sales',
                            hover_data=['Nama', 'SubArea'],
                            title='Performance Scatter Plot (Target vs Sales)',
                            color_continuous_scale='RdYlGn')
    fig_scatter.add_trace(go.Scatter(x=[0, filtered_df['Target'].max()], 
                                   y=[0, filtered_df['Target'].max()],
                                   mode='lines', name='Target Line',
                                   line=dict(dash='dash', color='red')))
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.subheader("Detailed Data View")
    
    # Search and filter options
    col1, col2 = st.columns(2)
    with col1:
        search_name = st.text_input("🔍 Search by Name:")
    with col2:
        sort_by = st.selectbox("Sort by:", ['Percentage DESC', 'Percentage ASC', 'Sales DESC', 'Name A-Z'])
    
    # Apply search filter
    display_df = filtered_df.copy()
    if search_name:
        display_df = display_df[display_df['Nama'].str.contains(search_name, case=False, na=False)]
    
    # Apply sorting
    sort_columns = {
        'Percentage DESC': ['Percentage', False],
        'Percentage ASC': ['Percentage', True],
        'Sales DESC': ['Sales', False],
        'Name A-Z': ['Nama', True]
    }
    sort_col, ascending = sort_columns[sort_by]
    display_df = display_df.sort_values(sort_col, ascending=ascending)
    
    # Display data
    st.write(f"**Showing {len(display_df)} records**")
    st.dataframe(display_df[['Nama', 'Area', 'SubArea', 'Grade', 'Target', 'Sales', 'Percentage']]
                .style.format({'Target': '{:.0f}', 'Sales': '{:.0f}', 'Percentage': '{:.1f}%'})
                .applymap(lambda x: 'color: green' if isinstance(x, (int, float)) and x > 100 else 
                         'color: red' if isinstance(x, (int, float)) and x < 50 else 
                         'color: orange', subset=['Percentage']),
                use_container_width=True, height=400)

with tab4:
    st.subheader("Strategic Recommendations")
    
    # Generate recommendations based on data
    critical_areas = df.groupby('SubArea')['Percentage'].mean().nsmallest(3)
    best_areas = df.groupby('SubArea')['Percentage'].mean().nlargest(3)
    zero_sales = df[df['Sales'] == 0]
    medium_performers = df[(df['Percentage'] >= 50) & (df['Percentage'] < 80)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🔴 Priority Actions")
        st.markdown("""
        **1. Critical Areas Intervention:**
        - {}: {:.1f}% achievement
        - {}: {:.1f}% achievement  
        - {}: {:.1f}% achievement
        
        **2. Zero-Sales Performers:**
        - {} people need immediate coaching
        - Individual performance reviews required
        
        **3. Supervisor Performance:**
        - Review SPV leadership effectiveness
        - Implement supervisor training
        """.format(
            critical_areas.index[0], critical_areas.iloc[0],
            critical_areas.index[1], critical_areas.iloc[1],
            critical_areas.index[2], critical_areas.iloc[2],
            len(zero_sales)
        ))
    
    with col2:
        st.write("### 🟢 Best Practices & Opportunities")
        st.markdown("""
        **1. Best Performing Areas:**
        - {}: {:.1f}% achievement
        - {}: {:.1f}% achievement
        - {}: {:.1f}% achievement
        
        **2. Quick Win Opportunities:**
        - {} medium performers (50-80%)
        - Targeted coaching can yield immediate results
        
        **3. Knowledge Sharing:**
        - Document success factors from top areas
        - Cross-area mentoring program
        """.format(
            best_areas.index[0], best_areas.iloc[0],
            best_areas.index[1], best_areas.iloc[1],
            best_areas.index[2], best_areas.iloc[2],
            len(medium_performers)
        ))
    
    # Performance improvement chart
    st.write("### 📊 Performance Improvement Potential")
    
    improvement_data = []
    for area in df['SubArea'].unique():
        area_data = df[df['SubArea'] == area]
        current_perf = area_data['Percentage'].mean()
        potential_gain = 100 - current_perf if current_perf < 100 else 0
        improvement_data.append({
            'SubArea': area,
            'Current': current_perf,
            'Potential': potential_gain
        })
    
    improvement_df = pd.DataFrame(improvement_data)
    fig_improve = px.bar(improvement_df.nlargest(10, 'Potential'), 
                        x='SubArea', y=['Current', 'Potential'],
                        title='Top 10 Areas with Improvement Potential',
                        labels={'value': 'Achievement %', 'variable': 'Metric'},
                        barmode='stack')
    st.plotly_chart(fig_improve, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <i>Dashboard updated automatically • Data period: 21 Juli - 20 Agustus</i>
</div>
""", unsafe_allow_html=True)