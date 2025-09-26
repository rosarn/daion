import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
     
# Data
data_text = """No	Area Sales	Status 	TARGET	CA	MINUS/PLUS	%
1	JAKARTA	Active	640	370	-270	58%
2	DEPOK 	Active	570	315	-255	55%
3	CENGKARENG	Active	25	0	-25	0%
4	TANGGERANG SELATAN(CIPUTAT)	Active	380	247	-133	65%
5	KOTA TANGGERANG (PORIS)	Active	230	102	-128	44%
6	KAB TANGGERANG(LEGOK CIKASUNGKA)	Active	230	100	-130	43%
7	KLAPANUNGGAL	Active	190	143	-47	75%
8	CILEUNGSI	Active	150	152	2	101%
9	CIANJUR	Active	150	78	-72	52%
10	PARUNG BOGOR	Active	190	21	-169	11%
11	TAMBUN 	Active	190	156	-34	82%
12	SERANG	Active	340	201	-139	59%
13	KAB PANDEGLANG	Active	150	100	-50	67%
14	CILEGON	Active	150	103	-47	69%
15	CIREBON	Active	530	454	-76	86%
16	SUBANG	Active	380	231	-149	61%
17	KARAWANG	Active	150	82	-68	55%
18	PURWAKARTA	Active	150	26	-124	17%
19	CISOLOK	Active	150	56	-94	37%
20	TASIKMALAYA	Active	490	471	-19	96%
21	KAB. TASIK	Active	150	126	-24	84%
22	CIAMIS	Active	300	250	-50	83%
23	CIAWI	Active	190	160	-30	84%
24	BANDUNG	Active	190	237	47	125%
25	GARUT	Active	490	434	-56	89%
26	BANJAR	Active	490	371	-119	76%
27	SEMARANG	Active	1360	1346	-14	99%
28	KUDUS	Active	100	50	-50	50%
29	KENDAL	Active	340	312	-28	92%
30	DEMAK	Active	300	175	-125	58%
31	SOLO	Active	640	283	-357	44%
32	PURWOKERTO	Active	150	58	-92	39%
33	JOGJA	Active	570	269	-301	47%
34	KLATEN	Active	230	80	-150	35%
35	KEBUMEN	Active	225	87	-138	39%
36	CILACAP	Active	340	241	-99	71%
37	TEGAL	Active	240	206	-34	86%
38	KEDIRI	Active	420	147	-273	35%
39	MALANG	Active	150	16	-134	11%
40	PONOROGO	Active	150	16	-134	11%
41	BADUNG	Active	640	426	-214	67%
42	TABANAN	Active	150	42	-108	28%
43	DENPASAR	Active	530	230	-300	43%
44	NEGARA	Active	300	157	-143	52%
45	BANGKA BELITUNG	Active	450	218	-232	48%
46	MEDAN	Active	300	282	-18	94%
47	SURABAYA	Active	190	20	-170	11%
TOTAL		15020	9647	-5373	64%"""

# Membaca data dari string
df = pd.read_csv(io.StringIO(data_text), sep='\t')

# Membersihkan data
df = df[:-1]  # Remove total row untuk analisis
df['%'] = df['%'].str.replace('%', '').astype(float)
df['TARGET'] = df['TARGET'].astype(int)
df['CA'] = df['CA'].astype(int)
df['MINUS/PLUS'] = df['MINUS/PLUS'].astype(int)

# Streamlit App
st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")
st.title("📊 DASHBOARD PERFORMANCE SALES AREA")

# Sidebar
st.sidebar.header("🔍 FILTER DATA")
selected_areas = st.sidebar.multiselect(
    "Pilih Area Sales:",
    options=df['Area Sales'].unique(),
    default=df['Area Sales'].unique()
)

# Filter data
filtered_df = df[df['Area Sales'].isin(selected_areas)]

# METRICS HEADER
st.subheader("📈 PERFORMANCE OVERVIEW")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_target = filtered_df['TARGET'].sum()
    st.metric("TOTAL TARGET", f"{total_target:,}")

with col2:
    total_ca = filtered_df['CA'].sum()
    st.metric("TOTAL REALISASI (CA)", f"{total_ca:,}")

with col3:
    achievement = (total_ca / total_target * 100) if total_target > 0 else 0
    st.metric("ACHIEVEMENT RATE", f"{achievement:.1f}%")

with col4:
    gap = total_ca - total_target
    st.metric("TOTAL GAP", f"{gap:,}", delta=f"{gap:,}")

# MAIN CONTENT - TABS
tab1, tab2, tab3, tab4 = st.tabs(["📋 DATA TABLE", "📊 PERFORMANCE CHART", "🏆 TOP/BOTTOM PERFORMERS", "🔍 ANALYSIS"])

with tab1:
    st.subheader("📋 DATA PERFORMANCE DETAI                                          L")
    
    # Tampilkan data dalam format tabel yang rapi
    display_df = filtered_df.copy()
    display_df['%'] = display_df['%'].astype(str) + '%'
    
    # Style the dataframe
    styled_df = display_df.style.format({
        'TARGET': '{:,}',
        'CA': '{:,}',
        'MINUS/PLUS': '{:,}'
    }).background_gradient(subset=['%'], cmap='RdYlGn')
    
    st.dataframe(styled_df, use_container_width=True, height=400)

with tab2:
    st.subheader("📊 PERFORMANCE VISUALIZATION")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart Target vs CA
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(name='TARGET', x=filtered_df['Area Sales'], y=filtered_df['TARGET'], marker_color='blue'))
        fig1.add_trace(go.Bar(name='CA', x=filtered_df['Area Sales'], y=filtered_df['CA'], marker_color='green'))
        fig1.update_layout(title='TARGET vs REALISASI (CA) per Area', barmode='group', height=500)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Achievement Rate
        fig2 = px.bar(filtered_df, x='Area Sales', y='%', 
                     title='ACHIEVEMENT RATE (%) per Area',
                     color='%', color_continuous_scale='RdYlGn')
        fig2.update_layout(height=500)
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("🏆 TOP & BOTTOM PERFORMERS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 🥇 TOP 10 PERFORMERS")
        top_10 = filtered_df.nlargest(10, '%')
        
        fig_top = px.bar(top_10, x='Area Sales', y='%', 
                        color='%', color_continuous_scale='Greens',
                        title='Top 10 Achievement Rate')
        st.plotly_chart(fig_top, use_container_width=True)
        
        # Tabel top performers
        st.write("**Detail Top Performers:**")
        top_display = top_10[['No', 'Area Sales', 'TARGET', 'CA', '%']].copy()
        top_display['%'] = top_display['%'].astype(str) + '%'
        st.dataframe(top_display.style.format({'TARGET': '{:,}', 'CA': '{:,}'}), use_container_width=True)
    
    with col2:
        st.write("### 🔻 BOTTOM 10 PERFORMERS")
        bottom_10 = filtered_df.nsmallest(10, '%')
        
        fig_bottom = px.bar(bottom_10, x='Area Sales', y='%',
                           color='%', color_continuous_scale='Reds',
                           title='Bottom 10 Achievement Rate')
        st.plotly_chart(fig_bottom, use_container_width=True)
        
        # Tabel bottom performers
        st.write("**Detail Bottom Performers:**")
        bottom_display = bottom_10[['No', 'Area Sales', 'TARGET', 'CA', '%']].copy()
        bottom_display['%'] = bottom_display['%'].astype(str) + '%'
        st.dataframe(bottom_display.style.format({'TARGET': '{:,}', 'CA': '{:,}'}), use_container_width=True)

with tab4:
    st.subheader("🔍 DETAILED ANALYSIS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 📊 PERFORMANCE SUMMARY")
        
        # Metrics analysis
        above_target = len(filtered_df[filtered_df['MINUS/PLUS'] >= 0])
        below_target = len(filtered_df[filtered_df['MINUS/PLUS'] < 0])
        excellent_perf = len(filtered_df[filtered_df['%'] >= 100])
        good_perf = len(filtered_df[(filtered_df['%'] >= 80) & (filtered_df['%'] < 100)])
        poor_perf = len(filtered_df[filtered_df['%'] < 60])
        
        st.metric("Area Above Target", above_target)
        st.metric("Area Below Target", below_target)
        st.metric("Excellent Performance (≥100%)", excellent_perf)
        st.metric("Good Performance (80-99%)", good_perf)
        st.metric("Poor Performance (<60%)", poor_perf)
    
    with col2:
        st.write("### 🎯 KEY INSIGHTS")
        
        # Best performer
        best = filtered_df.loc[filtered_df['%'].idxmax()]
        st.success(f"**BEST PERFORMER**: {best['Area Sales']} - {best['%']}%")
        
        # Worst performer
        worst = filtered_df.loc[filtered_df['%'].idxmin()]
        st.error(f"**NEEDS ATTENTION**: {worst['Area Sales']} - {worst['%']}%")
        
        # Biggest gap
        biggest_gap = filtered_df.loc[filtered_df['MINUS/PLUS'].idxmin()]
        st.warning(f"**BIGGEST GAP**: {biggest_gap['Area Sales']} - Gap: {biggest_gap['MINUS/PLUS']:,}")
        
        # Highest achievement above 100%
        above_100 = filtered_df[filtered_df['%'] > 100]
        if not above_100.empty:
            highest_above = above_100.loc[above_100['%'].idxmax()]
            st.info(f"**HIGHEST ABOVE TARGET**: {highest_above['Area Sales']} - {highest_above['%']}%")

# FOOTER
st.markdown("---")
st.markdown("**Dashboard Created with Streamlit** | Data Update: Latest")

# Download option
st.sidebar.markdown("---")
st.sidebar.header("💾 EXPORT DATA")
if st.sidebar.button("Download Data as CSV"):
    csv = filtered_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="sales_performance.csv",
        mime="text/csv"
    )