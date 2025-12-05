# src/ui/tabs.py
import streamlit as st
from src.language.language_config import get_text
from src.analytics.metrics import get_area_performance
from src.maps.maps import create_performance_map, create_heatmap_data, create_bubble_map_figure
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def render_kpis_card_block(team_metrics):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        total_sales = team_metrics['total_sales']
        total_target = team_metrics['total_target']
        achievement = team_metrics['overall_achievement']
        delta_color = "normal" if achievement >= 100 else "inverse"
        st.metric(f"🎯 {get_text('overall_achievement')}", f"{achievement:.1f}%", f"{total_sales:,}/{total_target:,}", delta_color=delta_color)
    with col2:
        avg_performance = team_metrics['avg_individual_performance']
        performance_std = team_metrics['performance_std']
        st.metric(f"📊 {get_text('average_performance')}", f"{avg_performance:.1f}%", f"±{performance_std:.1f}% std")
    with col3:
        top_performance = team_metrics['top_performance']
        top_performer = team_metrics['top_performer']
        st.metric(f"🏆 {get_text('top_performer')}", f"{top_performance:.1f}%", f"{top_performer[:15]}..." if len(top_performer) > 15 else top_performer)
    with col4:
        team_size = team_metrics['total_team_size']
        excellent_count = team_metrics['excellent_performers']
        st.metric(f"👥 {get_text('team_size')}", f"{team_size} people", f"{excellent_count} excellent")
    with col5:
        zero_sales = team_metrics['zero_sales_count']
        needs_improvement = team_metrics['needs_improvement']
        st.metric(f"⚠️ {get_text('needs_attention')}", f"{needs_improvement} people", f"{zero_sales} zero sales", delta_color="inverse" if needs_improvement > 0 else "normal")

def render_tabs(filtered_data, team_metrics):
    render_kpis_card_block(team_metrics)
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        f"🗺️ {get_text('area_maps')}",
        f"📈 {get_text('overview')}",
        f"🏆 {get_text('performers')}",
        f"📋 {get_text('detailed_data')}",
        f"🎯 {get_text('recommendations')}"
    ])

    # TAB 1: MAPS
    with tab1:
        st.subheader(f"🗺️ {get_text('geographic_distribution')}")
        map_type = st.radio(
            f"📍 {get_text('map_type')}:",
            [get_text('interactive_map'), get_text('heatmap'), get_text('bubble_map')],
            horizontal=True
        )

        col_map, col_legend = st.columns([3, 1])

        with col_map:
            if map_type == get_text('interactive_map'):
                st.write(f"**📍 {get_text('interactive_map')}**")
                st.caption("Klik marker untuk detail performa setiap area")
                performance_map = create_performance_map(filtered_data)

                st_folium = None
                try:
                    from streamlit_folium import st_folium as _stf
                    st_folium = _stf
                except Exception:
                    st.write("streamlit_folium not installed - cannot render interactive folium map")

                if st_folium:
                    st_folium(performance_map, width=800, height=600, returned_objects=[])

                unique_areas = filtered_data['Area'].nunique()
                st.info(f"📍 **{unique_areas} area unik** ditemukan dalam data")

            elif map_type == get_text('heatmap'):
                st.write(f"**🔥 {get_text('heatmap')}**")
                st.caption("Area dengan warna lebih merah membutuhkan perhatian khusus")

                area_data = create_heatmap_data(filtered_data)

                if not area_data.empty:
                    fig = px.density_mapbox(
                        area_data,
                        lat='lat', lon='lon', z='Percentage',
                        radius=30, center=dict(lat=-2.5489, lon=118.0149),
                        zoom=4, mapbox_style="carto-positron",
                        hover_data=['Area', 'Sales', 'Nama'],
                        title='Heatmap Performa Berdasarkan Area',
                        color_continuous_scale='RdYlGn_r',
                        range_color=[filtered_data['Percentage'].min(), filtered_data['Percentage'].max()],
                        labels={'Percentage': 'Rata-rata Performa (%)', 'Sales': 'Total Penjualan', 'Nama': 'Jumlah Sales'}
                    )
                    fig.update_layout(
                        margin=dict(l=0, r=0, t=40, b=0),
                        height=500,
                        coloraxis_colorbar=dict(title="Performa (%)", thickness=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ Tidak cukup data untuk membuat heatmap")

            else:
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
            st.markdown("### 🎯 Performance Color Legend:")
            st.markdown("""
            - 🟢 **Hijau**: ≥120% (Excellent)
            - 🟡 **Hijau Muda**: 100-119% (Good)
            - 🟠 **Oranye**: 80-99% (Average)
            - 🔴 **Merah**: <80% (Perlu Perhatian)
            """)

            if not filtered_data.empty:
                st.write(f"**📋 {get_text('area_summary')}:**")
                area_stats = filtered_data.groupby('Area').agg({'Percentage': 'mean', 'Sales': 'sum'}).round(1)

                for area in area_stats.index[:3]:
                    perf = area_stats.loc[area, 'Percentage']
                    sales = area_stats.loc[area, 'Sales']
                    st.metric(label=area, value=f"{perf:.1f}%", delta=f"Rp {sales:,.0f}")

    # TAB 2: OVERVIEW
    with tab2:
        st.subheader("📊 Performance Overview & Analytics")

        if not filtered_data.empty:
            area_stats = get_area_performance(filtered_data)

            if not area_stats.empty:
                area_stats_reset = area_stats.reset_index()

                fig = px.bar(
                    area_stats_reset,
                    x='Area', y='Achievement_Rate',
                    title='🏆 Achievement Rate by Area',
                    color='Achievement_Rate',
                    color_continuous_scale='RdYlGn',
                    text='Achievement_Rate',
                    hover_data=['Team_Size', 'Total_Sales', 'Total_Target']
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(
                    xaxis_title="Area", yaxis_title="Achievement Rate (%)",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

        if not filtered_data.empty:
            subarea_stats = (
                filtered_data.groupby('SubArea')
                .agg({'Sales': 'sum', 'Target': 'sum', 'Nama': 'count'})
                .reset_index()
            )

            subarea_stats['Achievement'] = (
                subarea_stats['Sales'] / subarea_stats['Target'] * 100
            ).round(1)

            subarea_stats = subarea_stats.sort_values('Achievement', ascending=True)

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                name='Target',
                x=subarea_stats['SubArea'],
                y=subarea_stats['Target'],
                text=subarea_stats['Target'],
                textposition='auto'
            ))
            fig_bar.add_trace(go.Bar(
                name='Sales',
                x=subarea_stats['SubArea'],
                y=subarea_stats['Sales'],
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
                st.metric(get_text('excellent_performers'), excellent_performers, f"{excellent_performers / len(filtered_data) * 100:.1f}%")

            with col2:
                good_performers = len(filtered_data[filtered_data['Performance_Category'] == 'Good'])
                st.metric(get_text('good_performers'), good_performers, f"{good_performers / len(filtered_data) * 100:.1f}%")

            with col3:
                avg_performers = len(filtered_data[filtered_data['Performance_Category'] == 'Average'])
                st.metric(get_text('average_performers'), avg_performers, f"{avg_performers / len(filtered_data) * 100:.1f}%")

            with col4:
                poor_performers = len(filtered_data[filtered_data['Performance_Category'].isin(['Below Average', 'Poor'])])
                st.metric(get_text('needs_improvement'), poor_performers, f"{poor_performers / len(filtered_data) * 100:.1f}%")

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                top_10 = filtered_data.nlargest(10, 'Percentage')[[
                    'Nama', 'SubArea', 'Grade', 'Sales', 'Target', 'Percentage', 'Performance_Category'
                ]]
                st.write(f"**🏅 {get_text('top_performers')}:**")
                st.dataframe(
                    top_10.style.format({
                        'Sales': '{:.0f}', 'Target': '{:.0f}', 'Percentage': '{:.1f}%'
                    }),
                    use_container_width=True
                )

            with col2:
                bottom_10 = filtered_data.nsmallest(10, 'Percentage')[[
                    'Nama', 'SubArea', 'Grade', 'Sales', 'Target', 'Percentage', 'Performance_Category'
                ]]
                st.write(f"**⚠️ {get_text('bottom_performers')}:**")
                st.dataframe(
                    bottom_10.style.format({
                        'Sales': '{:.0f}', 'Target': '{:.0f}', 'Percentage': '{:.1f}%'
                    }),
                    use_container_width=True
                )

    # TAB 4: DETAILED DATA
    with tab4:
        st.subheader("📋 Detailed Data View & Analysis")

        if not filtered_data.empty:
            col1, col2, col3 = st.columns(3)

            with col1:
                search_name = st.text_input(f"🔍 {get_text('search_name')}:")

            with col2:
                sort_by = st.selectbox(
                    f"📊 {get_text('sort_by')}:",
                    [
                        'Percentage DESC', 'Percentage ASC',
                        'Sales DESC', 'Sales ASC',
                        'Target DESC', 'Target ASC',
                        'Name A-Z', 'Name Z-A',
                        'Area A-Z'
                    ]
                )

            with col3:
                export_format = st.selectbox(
                    f"📤 {get_text('export_format')}:",
                    ['View Only', 'CSV Download', 'Excel Download']
                )

            display_df = filtered_data.copy()

            if search_name:
                display_df = display_df[
                    display_df['Nama'].str.contains(search_name, case=False, na=False)
                ]

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
                achievement_rate = (
                    display_df['Sales'].sum() / display_df['Target'].sum() * 100
                    if display_df['Target'].sum() > 0
                    else 0
                )
                st.metric(get_text('group_achievement'), f"{achievement_rate:.1f}%")

            st.write(f"**📊 Showing {len(display_df)} of {len(filtered_data)} records**")

            display_columns = [
                'Nama', 'Area', 'SubArea', 'Grade', 'Target',
                'Sales', 'Minus/plus', 'Percentage', 'Performance_Category'
            ]

            styled_df = display_df[display_columns].style.format({
                'Target': '{:.0f}', 'Sales': '{:.0f}',
                'Minus/plus': '{:+.0f}', 'Percentage': '{:.1f}%'
            })

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
            poor_performers = filtered_data[
                filtered_data['Performance_Category'].isin(['Below Average', 'Poor'])
            ]
            excellent_performers = filtered_data[
                filtered_data['Performance_Category'] == 'Excellent'
            ]

            st.markdown(f"### 📋 {get_text('executive_summary')}")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                overall_achievement = (
                    filtered_data['Sales'].sum()
                    / filtered_data['Target'].sum() * 100
                    if filtered_data['Target'].sum() > 0
                    else 0
                )
                status = (
                    "🟢 Good" if overall_achievement >= 100
                    else "🟡 Needs Attention" if overall_achievement >= 80
                    else "🔴 Critical"
                )
                st.metric(get_text('overall_status'), status, f"{overall_achievement:.1f}%")

            with col2:
                risk_level = len(poor_performers) / len(filtered_data) * 100
                risk_status = (
                    "🔴 High" if risk_level > 30
                    else "🟡 Medium" if risk_level > 15
                    else "🟢 Low"
                )
                st.metric(get_text('risk_level'), risk_status, f"{risk_level:.1f}%")

            with col3:
                improvement_potential = len(
                    filtered_data[
                        (filtered_data['Percentage'] >= 50)
                        & (filtered_data['Percentage'] < 80)
                    ]
                )
                st.metric(
                    get_text('quick_wins'),
                    f"{improvement_potential} people",
                    "Medium performers"
                )

            with col4:
                benchmark_performers = len(excellent_performers)
                st.metric(
                    get_text('benchmarks'),
                    f"{benchmark_performers} people",
                    "Excellent performers"
                )

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

    st.markdown("---")

    st.markdown(
        f"""
        <div style='text-align: center; color: gray;'>
            <i>📊 {get_text('footer_text')}: {st.session_state.periode_data}
            • ⏰ {get_text('last_updated')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
        </div>
        """,
        unsafe_allow_html=True
    )
