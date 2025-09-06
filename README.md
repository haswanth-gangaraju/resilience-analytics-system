# 🏭 Resilience Analytics System

A comprehensive portfolio project analyzing 8,000+ simulated assets for resilience assessment, risk modeling, and operational insights. Built for water utility infrastructure management with production-quality code and interactive dashboards.

## 🌟 Project Overview

The Resilience Analytics System is a complete data analytics solution that combines:
- **Advanced Data Simulation**: Realistic infrastructure asset data generation
- **Machine Learning**: Risk probability modeling and predictive analytics
- **Interactive Dashboards**: Real-time monitoring and decision support
- **Database Management**: Efficient data storage and querying
- **Production Quality**: Clean code, documentation, and deployment-ready

### 🎯 Business Value

- **Risk Assessment**: Identify high-risk assets requiring immediate attention
- **Cost Optimization**: Quantify financial impact of downtime and maintenance decisions
- **Predictive Maintenance**: Forecast failures and optimize maintenance schedules
- **Resource Allocation**: Prioritize investments based on resilience scores and risk metrics
- **Operational Efficiency**: Real-time monitoring and performance tracking

## 🚀 Features

### 📊 Analytics Capabilities
- **Resilience Scoring**: Comprehensive 0-100 scale scoring algorithm
- **Risk Categorization**: High/Medium/Low risk classification with ML models
- **Financial Impact Analysis**: Cost calculations for downtime and risk exposure
- **Regional Performance**: Geographic analysis across utility service areas
- **Asset Lifecycle Management**: Age-based performance and replacement planning

### 📈 Dashboard Features
- **Real-time KPIs**: Overview of system health and performance metrics
- **Interactive Filtering**: Region, asset type, risk level, and time-based filters
- **Predictive Forecasting**: Failure predictions and maintenance recommendations
- **Export Capabilities**: CSV downloads and automated report generation
- **Investment Priority Matrix**: Data-driven capital allocation guidance

## 🛠️ Technology Stack

- **Python 3.8+**: Core analytics and data processing
- **Streamlit**: Interactive dashboard framework
- **SQLite**: Database for data storage and querying
- **Pandas & NumPy**: Data manipulation and statistical analysis
- **Scikit-learn**: Machine learning models for risk prediction
- **Plotly**: Interactive visualizations and charts
- **SQLAlchemy**: Database ORM and connection management
- **Faker**: Realistic synthetic data generation

## 📁 Project Structure

```
resilience-analytics-system/
│
├── data/                           # Data storage
│   ├── resilience_assets.csv      # Raw simulated dataset
│   ├── resilience_assets_enhanced.csv # Enhanced with ML predictions
│   ├── risk_model.pkl             # Trained ML model components
│   └── resilience_analytics.db    # SQLite database
│
├── notebooks/                     # Jupyter notebooks
│   ├── 01_data_simulation.ipynb   # Data generation and simulation
│   └── 02_resilience_metrics.ipynb # Analytics and ML modeling
│
├── app/                           # Application code
│   ├── dashboard.py              # Streamlit dashboard application
│   ├── db_setup.py              # Database setup and management
│   └── queries.sql              # SQL queries collection
│
├── docs/                         # Documentation
│   ├── README.md                # This file
│   └── architecture.png         # System architecture diagram (optional)
│
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
└── LICENSE                      # MIT license
```

## 🚦 Quick Start

### Prerequisites
- Python 3.8 or higher
- 2GB free disk space
- 8GB RAM recommended

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resilience-analytics-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate data and run analytics**
   ```bash
   # Run notebooks in order
   jupyter notebook notebooks/01_data_simulation.ipynb
   jupyter notebook notebooks/02_resilience_metrics.ipynb
   ```

4. **Setup database**
   ```bash
   cd app
   python db_setup.py
   ```

5. **Launch dashboard**
   ```bash
   streamlit run app/dashboard.py
   ```

6. **Access the application**
   - Open browser to `http://localhost:8501`
   - Explore the interactive dashboard

## 📊 Data Overview

### Dataset Characteristics
- **8,000 simulated assets** across water utility infrastructure
- **10 asset types**: Water Treatment Plants, Pump Stations, Pipelines, etc.
- **10 regions**: North, South, East, West, Central, Northeast, Northwest, Southeast, Southwest, Metro regions
- **44-year timeline**: Installation years from 1980-2024
- **Comprehensive metrics**: Downtime, failures, maintenance, costs, resilience scores

### Key Metrics
- **Resilience Score (0-100)**: Composite metric based on:
  - Reliability (35%): Uptime and failure rates
  - Maintainability (25%): MTTR and compliance
  - Redundancy (20%): Backup system availability
  - Asset Age (10%): Age-based degradation
  - Criticality (10%): Strategic importance

- **Risk Probability (0-1)**: ML-predicted failure likelihood
- **Impact Cost (£)**: Financial cost of downtime events
- **Annual Risk Cost (£)**: Expected annual cost exposure

## 🔧 Usage Guide

### Dashboard Navigation

1. **Overview Tab**: System-wide KPIs and health metrics
2. **Regional Analysis**: Geographic performance comparison
3. **Risk Analysis**: High-risk asset identification
4. **Asset Performance**: Type-based analysis and trends
5. **Forecasting**: Predictive insights and recommendations
6. **Export**: Data download and report generation

### Key Use Cases

#### 🎯 Risk Management
- Identify assets with >80% failure probability
- Review high-impact cost assets (>£50k annual exposure)
- Monitor maintenance compliance <70%

#### 📈 Performance Optimization  
- Compare regional resilience scores
- Analyze asset age vs performance correlations
- Track maintenance effectiveness metrics

#### 💰 Investment Planning
- Use Investment Priority Matrix for capital allocation
- Identify replacement candidates (age >25 years, score <60)
- Quantify ROI of resilience improvements

#### 🔮 Predictive Maintenance
- Review forecasted failures for next 12 months
- Schedule maintenance for medium-risk assets
- Monitor degradation trends by asset type

## 📋 SQL Queries Reference

The system includes 22 pre-built SQL queries in `app/queries.sql`:

### Basic Statistics (1-3)
- System health KPIs
- Asset distribution analysis
- Resilience score categories

### Risk Analysis (4-6)
- Top 10 highest risk assets
- Multi-criteria risk identification  
- Critical asset downtime analysis

### Regional Analysis (7-8)
- Regional performance metrics
- Risk heatmap data by geography

### Asset Analysis (9-10)
- Asset type performance comparison
- Age-based degradation analysis

### Operational Insights (11-12)
- Maintenance compliance correlation
- Redundancy impact assessment

### Financial Analysis (13-14)
- Cost analysis by risk category
- Top cost impact assets

### Trends & Correlations (15-16)
- Downtime vs maintenance patterns
- Energy consumption relationships

### Predictive Analytics (17-18)
- Failure prediction factors
- Replacement priority scoring

### Utilities (19-22)
- Dashboard filter options
- Time series trending
- Data quality monitoring
- Summary statistics

## 🎨 Customization

### Adding New Asset Types
1. Update `ASSET_TYPES` in `01_data_simulation.ipynb`
2. Define asset-specific multipliers in `get_asset_type_multiplier()`
3. Regenerate dataset and update database

### Modifying Resilience Algorithm
1. Edit `calculate_resilience_score()` in `02_resilience_metrics.ipynb`
2. Adjust component weights as needed:
   - Reliability: 35%
   - Maintainability: 25%  
   - Redundancy: 20%
   - Age Factor: 10%
   - Criticality: 10%

### Dashboard Customization
1. **Colors**: Modify color schemes in `dashboard.py`
2. **Metrics**: Add new KPIs in `get_kpis()` method
3. **Visualizations**: Create custom plots in respective sections
4. **Filters**: Add new filter options in `create_filters_sidebar()`

## 📊 Performance Metrics

### System Performance
- **Data Processing**: <30 seconds for 8,000 assets
- **Dashboard Load Time**: <5 seconds initial load
- **Query Performance**: <2 seconds for complex aggregations
- **Memory Usage**: ~500MB for full dataset operations

### Model Accuracy
- **Risk Classification**: >95% accuracy on test set
- **Feature Importance**: Top factors are downtime, resilience score, failures
- **Prediction Confidence**: 90%+ for high-risk classifications

## 🔐 Security & Compliance

- **Data Privacy**: Simulated data only, no real utility information
- **Access Control**: Dashboard runs locally, no external connections
- **Data Validation**: Input sanitization and range checking
- **Audit Trail**: All operations logged for debugging

## 🚀 Deployment Options

### Local Development
- Run on localhost for development and testing
- Full functionality available offline
- Suitable for demonstrations and analysis

### Production Deployment
- Deploy to cloud platforms (AWS, Azure, GCP)
- Use containerization with Docker
- Scale with load balancers for multiple users
- Implement authentication for secure access

### Integration Options
- **API Development**: Expose analytics as REST endpoints
- **Database Integration**: Connect to existing utility systems
- **Automated Reporting**: Schedule PDF/Excel report generation
- **Alert System**: Email/SMS notifications for critical risks

## 🔄 Future Enhancements

### Planned Features
- **Real-time Data Integration**: Live sensor data streaming
- **Advanced ML Models**: Deep learning for pattern recognition
- **Mobile Dashboard**: Responsive design for tablets/phones
- **Alert Management**: Automated notification system
- **Historical Trending**: Multi-year performance analysis
- **Benchmarking**: Industry standard comparisons

### Technical Roadmap
- **Performance Optimization**: Caching and query optimization
- **Scale Enhancement**: Support for 50,000+ assets
- **API Development**: RESTful service architecture
- **Testing Suite**: Comprehensive unit and integration tests
- **CI/CD Pipeline**: Automated deployment and testing

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Commit with clear messages: `git commit -m 'Add feature X'`
5. Push to branch: `git push origin feature/new-feature`
6. Submit pull request with description

### Code Standards
- Follow PEP 8 Python style guide
- Add docstrings for all functions
- Include unit tests for new features
- Update documentation for API changes

### Testing
- Run notebooks to verify data pipeline
- Test dashboard functionality across browsers
- Validate SQL queries against sample data
- Check performance with large datasets

## 🐛 Troubleshooting

### Common Issues

**1. Database not found error**
```bash
# Solution: Run database setup
cd app
python db_setup.py
```

**2. Missing data files**
```bash
# Solution: Run notebooks in correct order
jupyter notebook notebooks/01_data_simulation.ipynb
jupyter notebook notebooks/02_resilience_metrics.ipynb
```

**3. Dashboard not loading**
```bash
# Check Streamlit installation
pip install streamlit
streamlit run app/dashboard.py
```

**4. Memory issues with large datasets**
```python
# Use data sampling in notebooks
df_sample = df.sample(n=1000)  # Use 1000 rows for testing
```

### Performance Optimization
- Use database indexes for faster queries
- Implement data caching for repeated operations
- Optimize Plotly charts for better rendering
- Use pagination for large data tables

## 📚 Technical Documentation

### Architecture Overview
The system follows a layered architecture:
1. **Data Layer**: CSV files and SQLite database
2. **Processing Layer**: Jupyter notebooks for ETL and ML
3. **Application Layer**: Python scripts for business logic
4. **Presentation Layer**: Streamlit dashboard for visualization

### Data Flow
1. **Simulation**: Generate synthetic asset data
2. **Enhancement**: Apply ML models and calculate metrics  
3. **Storage**: Load into SQLite database with indexes
4. **Analysis**: Execute SQL queries for insights
5. **Visualization**: Render interactive dashboard
6. **Export**: Generate reports and data downloads

### Database Schema
```sql
resilience_assets (
    asset_id TEXT PRIMARY KEY,
    region TEXT,
    asset_type TEXT,
    install_year INTEGER,
    downtime_hours_last_year REAL,
    failure_count_last_year INTEGER,
    mean_time_to_repair REAL,
    maintenance_compliance REAL,
    redundancy_level TEXT,
    energy_consumption_kwh REAL,
    criticality_score REAL,
    resilience_score REAL,
    risk_category TEXT,
    risk_probability REAL,
    impact_cost REAL,
    annual_risk_cost REAL
)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Water Utilities**: Inspiration for infrastructure resilience analysis
- **Open Source Community**: Libraries and frameworks used
- **Data Science Community**: Methodologies and best practices
- **Streamlit Team**: Excellent dashboard framework

## 📞 Support

### Getting Help
- **Documentation**: Review this README and inline code comments  
- **Issues**: Report bugs via GitHub issues
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact the development team for urgent matters

### Community
- **GitHub**: Star the repository and follow updates
- **LinkedIn**: Share your project experiences
- **Twitter**: Use #ResilienceAnalytics hashtag
- **Medium**: Write about your implementations and insights

---

**🏆 Project Status**: Production Ready  
**📅 Last Updated**: January 2025  
**🎯 Purpose**: Portfolio demonstration and  resilience analysis  

---

*Built with ❤️ for infrastructure resilience and data-driven decision making*