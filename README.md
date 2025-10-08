# 📊 Sales Performance Analytics Dashboard

**Comprehensive Sales Performance Monitoring & Analytics Platform**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)

## 🎯 Overview

**DAION** (Data Analytics & Intelligence Operations Network) adalah platform dashboard analytics yang dirancang khusus untuk monitoring dan analisis performa sales tim. Dashboard ini menyediakan insights mendalam tentang pencapaian target, distribusi performa, dan rekomendasi strategis untuk optimasi hasil penjualan.

### ✨ Key Features

- **📈 Real-time Performance Monitoring** - Tracking pencapaian sales vs target secara real-time
- **🎯 Advanced Analytics** - Analisis mendalam dengan berbagai metrik performa
- **🌍 Multi-Area Coverage** - Monitoring performa across multiple geographical areas
- **👥 Role-based Analysis** - Analisis berdasarkan grade/role (SPV, S2, DS)
- **📊 Interactive Visualizations** - Charts dan graphs yang interaktif menggunakan Plotly
- **🔍 Smart Filtering** - Filter canggih berdasarkan area, grade, dan performance range
- **💡 Strategic Recommendations** - AI-powered recommendations untuk improvement
- **📋 Detailed Reporting** - Export data dalam format CSV/Excel
- **🎨 Modern UI/UX** - Interface yang clean dan responsive

## 🏗️ Project Structure (Restructured Monorepo)

```
daion/
├── 📄 main.py                 # 🚀 Main application entry point
├── 📁 src/                    # Source code modules
│   ├── 📁 data/              # Data layer
│   │   ├── __init__.py
│   │   ├── models.py         # Data structures and validation
│   │   └── loader.py         # Data loading and processing
│   ├── 📁 analytics/         # Business logic and metrics
│   │   ├── __init__.py
│   │   └── metrics.py        # Performance calculations
│   ├── 📁 ui/                # User interface components
│   │   ├── __init__.py
│   │   ├── styles.py         # CSS styling and themes
│   │   └── components.py     # Reusable UI components
│   ├── 📁 visualizations/    # Chart and plotting functions
│   │   ├── __init__.py
│   │   └── charts.py         # Plotly visualizations
│   └── 📁 shared/            # Shared utilities
│       └── __init__.py
├── 📁 tests/                 # Test suite
│   └── __init__.py
├── 📁 config/                # Configuration files
├── 📁 docs/                  # Documentation
├── 📁 juliagustus/          # Legacy data files
├── 📁 agustusseptember/     # Legacy data files
├── 📄 satu.py              # Original monolithic file (legacy)
├── 📄 requirements.txt     # Python dependencies
└── 📄 README.md           # Documentation (this file)
```

### 🔄 Architecture Benefits

The restructured monorepo provides:
- **Clear separation of concerns** through modular components
- **Proper package boundaries** and shared libraries
- **Maintained existing functionality** throughout restructuring
- **Robust dependency management** between modules
- **Scalable and maintainable** codebase structure

## 🚀 Quick Start

### Prerequisites

- Python 3.8 atau lebih tinggi
- pip (Python package installer)

### Installation

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd daion
   ```

2. **Setup virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   streamlit run satu.py
   ```

5. **Access dashboard**
   - Open browser dan navigate ke: `http://localhost:8501`

## 📊 Dashboard Features

### 🎯 Key Performance Indicators (KPIs)

- **Overall Achievement** - Total pencapaian vs target keseluruhan
- **Average Performance** - Rata-rata performa individual dengan standard deviation
- **Top Performer** - Performer terbaik dengan achievement tertinggi
- **Team Size** - Jumlah anggota tim dan excellent performers
- **Needs Attention** - Jumlah yang memerlukan perhatian khusus

### 📈 Analytics Tabs

#### 1. **Overview Tab**
- 🏆 Achievement rate by area dengan color-coded visualization
- 📊 Performance distribution pie chart
- 📉 Sales vs Target analysis by sub-area
- 👥 Performance analysis by grade/role

#### 2. **Performers Tab**
- 🏅 Top 10 performers dengan highlighting
- ⚠️ Bottom 10 performers untuk improvement focus
- 📊 Performance scatter plot (Target vs Sales)
- 🌍 Performance distribution by area

#### 3. **Detailed Data Tab**
- 🔍 Advanced search dan filtering
- 📊 Sortable data table dengan color-coded performance
- 📤 Export functionality (CSV/Excel)
- 📈 Statistical summary dan breakdown

#### 4. **Recommendations Tab**
- 🚨 Priority actions untuk immediate intervention
- 🟢 Growth opportunities dan best practices
- 📅 Action timeline dengan expected impact
- 💹 ROI projections dari recommendations

### 🎨 Advanced Features

#### Smart Filtering System
- **Area Filter** - Dengan performance indicators
- **Grade Filter** - Dengan team size information
- **Performance Range** - Min/max achievement sliders
- **Category Filter** - Berdasarkan performance categories

#### Performance Categorization
- **🟢 Excellent** (≥120%) - Exceeds expectations significantly
- **🔵 Good** (100-119%) - Meets/exceeds target
- **🟡 Average** (80-99%) - Close to target
- **🟠 Below Average** (60-79%) - Needs improvement
- **🔴 Poor** (<60%) - Requires immediate attention

## 🛠️ Technical Stack

- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly, Matplotlib, Seaborn
- **Styling**: Custom CSS dengan responsive design
- **Data Storage**: Python dictionaries (dapat diintegrasikan dengan database)

## 📁 File Descriptions

### Core Files

- **`satu.py`** - 🚀 Main dashboard application dengan semua features
- **`main.py`** - Navigation hub dan entry point
- **`test.py`** - Testing environment untuk development

### Data Analysis Files

- **`juliagustus/`** - Contains area-specific analysis files untuk periode Juli-Agustus
- **`agustusseptember/`** - Data untuk periode Agustus-September

## 🎯 Usage Guide

### 1. **Navigation**
- Start dari `main.py` untuk navigation hub
- Pilih "Sales Performance Dashboard" untuk main analytics

### 2. **Filtering Data**
- Gunakan sidebar filters untuk customize view
- Combine multiple filters untuk detailed analysis
- Monitor filter summary untuk track applied filters

### 3. **Analyzing Performance**
- Review KPIs di top section untuk quick overview
- Explore tabs untuk detailed insights
- Focus pada recommendations tab untuk actionable insights

### 4. **Exporting Data**
- Gunakan Detailed Data tab untuk export functionality
- Choose format (CSV/Excel) sesuai kebutuhan
- Data exported includes all applied filters

## 🔧 Customization

### Adding New Areas
1. Create new analysis file di `juliagustus/` folder
2. Follow existing file structure dan naming convention
3. Update main data dictionary di `satu.py`

### Modifying Performance Categories
1. Edit `categorize_performance()` function di `satu.py`
2. Update thresholds sesuai business requirements
3. Adjust color schemes di CSS section

### Custom Metrics
1. Add new metrics di `calculate_team_metrics()` function
2. Update KPI display section
3. Include dalam recommendations logic

## 🚀 Performance Optimization

- **Caching**: Menggunakan `@st.cache_data` untuk efficient data loading
- **Lazy Loading**: Data processed only when needed
- **Responsive Design**: Optimized untuk berbagai screen sizes
- **Memory Management**: Efficient data structures dan processing

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

**Data Analytics Team**
- Dashboard Development & Analytics Implementation
- Performance Monitoring & Insights Generation
- Strategic Recommendations & Business Intelligence

## 📞 Support

Untuk support atau questions:
- Create issue di repository
- Contact development team
- Check documentation untuk troubleshooting

---

**🎯 Built with ❤️ for Sales Performance Excellence**

*Last Updated: January 2025*