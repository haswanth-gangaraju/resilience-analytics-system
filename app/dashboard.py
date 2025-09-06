#!/usr/bin/env python3
"""
Resilience Analytics System - Interactive Dashboard

A comprehensive Streamlit dashboard for water utility resilience analytics.
Provides interactive visualizations, risk assessment, and operational insights.

Author: Resilience Analytics Team
Date: 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from sqlalchemy import create_engine
import os
import sys
from pathlib import Path
import io
import base64
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Resilience Analytics Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79, #2e8b57);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 0.5rem 0;
    }
    .risk-high {
        border-left-color: #dc3545 !important;
    }
    .risk-medium {
        border-left-color: #ffc107 !important;
    }
    .risk-low {
        border-left-color: #28a745 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

class ResilienceDashboard:
    """
    Main dashboard class for Resilience Analytics System
    """
    
    def __init__(self):
        """Initialize dashboard with database connection"""
        self.db_path = '../data/resilience_analytics.db'
        self.engine = None
        self.data = None
        
    def connect_database(self):
        """Establish database connection"""
        try:
            if os.path.exists(self.db_path):
                self.engine = create_engine(f'sqlite:///{self.db_path}')
                return True
            else:
                st.error(f"Database not found: {self.db_path}")
                st.info("Please run the following steps first:")
                st.code("""
                1. Run notebooks/01_data_simulation.ipynb
                2. Run notebooks/02_resilience_metrics.ipynb  
                3. Run python app/db_setup.py
                """)
                return False
        except Exception as e:
            st.error(f"Database connection failed: {e}")
            return False
    
    def load_data(self, query="SELECT * FROM resilience_assets", use_cache=True):
        """Load data from database with caching"""
        try:
            if use_cache and 'cached_data' in st.session_state:
                return st.session_state.cached_data
            
            df = pd.read_sql_query(query, self.engine)
            
            if use_cache:
                st.session_state.cached_data = df
                
            return df
            
        except Exception as e:
            st.error(f"Data loading failed: {e}")
            return None
    
    def get_kpis(self):
        """Calculate key performance indicators"""
        try:
            query = """
            SELECT 
                COUNT(*) as total_assets,
                ROUND(AVG(resilience_score), 2) as avg_resilience_score,
                ROUND(SUM(downtime_hours_last_year), 0) as total_downtime_hours,
                COUNT(CASE WHEN risk_category = 'High' THEN 1 END) as high_risk_count,
                COUNT(CASE WHEN risk_category = 'Medium' THEN 1 END) as medium_risk_count,
                COUNT(CASE WHEN risk_category = 'Low' THEN 1 END) as low_risk_count,
                ROUND(SUM(annual_risk_cost), 0) as total_annual_risk_cost
            FROM resilience_assets
            """
            df = pd.read_sql_query(query, self.engine)
            return df.iloc[0].to_dict()
            
        except Exception as e:
            st.error(f"KPI calculation failed: {e}")
            return {}
    
    def create_overview_section(self):
        """Create overview section with KPIs"""
        st.markdown('<div class="main-header"><h1>🏭 Water Utility Resilience Analytics</h1></div>', 
                   unsafe_allow_html=True)
        
        # Get KPIs
        kpis = self.get_kpis()
        
        if kpis:
            # Main metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Assets", 
                    f"{kpis['total_assets']:,}",
                    help="Total number of assets in the system"
                )
            
            with col2:
                avg_resilience = kpis['avg_resilience_score']
                st.metric(
                    "Avg Resilience Score", 
                    f"{avg_resilience:.1f}",
                    delta=f"{avg_resilience - 65:.1f}" if avg_resilience else None,
                    help="Average resilience score across all assets (0-100)"
                )
            
            with col3:
                total_downtime = kpis['total_downtime_hours']
                st.metric(
                    "Total Downtime", 
                    f"{total_downtime:,.0f} hrs",
                    help="Total downtime hours across all assets last year"
                )
            
            with col4:
                annual_risk_cost = kpis['total_annual_risk_cost']
                st.metric(
                    "Annual Risk Cost", 
                    f"£{annual_risk_cost:,.0f}",
                    help="Total estimated annual risk cost"
                )
            
            # Risk distribution row
            st.markdown("### Risk Distribution")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card risk-high">
                    <h3 style="color: #dc3545; margin: 0;">High Risk Assets</h3>
                    <h2 style="margin: 0.5rem 0;">{kpis['high_risk_count']:,}</h2>
                    <p style="margin: 0; color: #6c757d;">Require immediate attention</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card risk-medium">
                    <h3 style="color: #ffc107; margin: 0;">Medium Risk Assets</h3>
                    <h2 style="margin: 0.5rem 0;">{kpis['medium_risk_count']:,}</h2>
                    <p style="margin: 0; color: #6c757d;">Monitor and plan maintenance</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card risk-low">
                    <h3 style="color: #28a745; margin: 0;">Low Risk Assets</h3>
                    <h2 style="margin: 0.5rem 0;">{kpis['low_risk_count']:,}</h2>
                    <p style="margin: 0; color: #6c757d;">Standard monitoring</p>
                </div>
                """, unsafe_allow_html=True)
    
    def create_filters_sidebar(self):
        """Create sidebar filters"""
        st.sidebar.header("🔍 Filters")
        
        # Load filter options from database
        data = self.load_data()
        if data is None:
            return {}
        
        filters = {}
        
        # Region filter
        regions = ['All'] + sorted(data['region'].unique().tolist())
        filters['region'] = st.sidebar.selectbox("Region", regions)
        
        # Asset type filter
        asset_types = ['All'] + sorted(data['asset_type'].unique().tolist())
        filters['asset_type'] = st.sidebar.selectbox("Asset Type", asset_types)
        
        # Risk category filter
        risk_categories = ['All'] + sorted(data['risk_category'].unique().tolist())
        filters['risk_category'] = st.sidebar.selectbox("Risk Category", risk_categories)
        
        # Resilience score range
        if 'resilience_score' in data.columns:
            min_score, max_score = float(data['resilience_score'].min()), float(data['resilience_score'].max())
            filters['resilience_range'] = st.sidebar.slider(
                "Resilience Score Range",
                min_value=min_score,
                max_value=max_score,
                value=(min_score, max_score),
                step=1.0
            )
        
        # Installation year filter
        if 'install_year' in data.columns:
            min_year, max_year = int(data['install_year'].min()), int(data['install_year'].max())
            filters['year_range'] = st.sidebar.slider(
                "Installation Year Range",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year)
            )
        
        return filters
    
    def apply_filters(self, data, filters):
        """Apply filters to data"""
        if data is None:
            return None
        
        filtered_data = data.copy()
        
        if filters.get('region') and filters['region'] != 'All':
            filtered_data = filtered_data[filtered_data['region'] == filters['region']]
        
        if filters.get('asset_type') and filters['asset_type'] != 'All':
            filtered_data = filtered_data[filtered_data['asset_type'] == filters['asset_type']]
        
        if filters.get('risk_category') and filters['risk_category'] != 'All':
            filtered_data = filtered_data[filtered_data['risk_category'] == filters['risk_category']]
        
        if filters.get('resilience_range'):
            min_res, max_res = filters['resilience_range']
            filtered_data = filtered_data[
                (filtered_data['resilience_score'] >= min_res) & 
                (filtered_data['resilience_score'] <= max_res)
            ]
        
        if filters.get('year_range'):
            min_year, max_year = filters['year_range']
            filtered_data = filtered_data[
                (filtered_data['install_year'] >= min_year) & 
                (filtered_data['install_year'] <= max_year)
            ]
        
        return filtered_data
    
    def create_regional_analysis(self, data):
        """Create regional analysis visualizations"""
        st.header("🗺️ Regional Analysis")
        
        if data is None or len(data) == 0:
            st.warning("No data available for regional analysis")
            return
        
        # Regional performance metrics
        regional_stats = data.groupby('region').agg({
            'asset_id': 'count',
            'resilience_score': 'mean',
            'risk_probability': 'mean',
            'downtime_hours_last_year': 'sum',
            'annual_risk_cost': 'sum'
        }).round(2)
        
        regional_stats.columns = ['Asset Count', 'Avg Resilience', 'Avg Risk Prob', 
                                'Total Downtime', 'Total Risk Cost']
        regional_stats = regional_stats.reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Regional resilience bar chart
            fig_resilience = px.bar(
                regional_stats,
                x='region',
                y='Avg Resilience',
                color='Avg Resilience',
                color_continuous_scale='RdYlGn',
                title='Average Resilience Score by Region',
                labels={'region': 'Region', 'Avg Resilience': 'Average Resilience Score'}
            )
            fig_resilience.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_resilience, use_container_width=True)
        
        with col2:
            # Regional risk cost pie chart
            fig_cost = px.pie(
                regional_stats,
                values='Total Risk Cost',
                names='region',
                title='Annual Risk Cost Distribution by Region'
            )
            fig_cost.update_layout(height=400)
            st.plotly_chart(fig_cost, use_container_width=True)
        
        # Regional performance table
        st.subheader("Regional Performance Summary")
        st.dataframe(
            regional_stats.style.format({
                'Avg Resilience': '{:.1f}',
                'Avg Risk Prob': '{:.3f}',
                'Total Downtime': '{:,.0f}',
                'Total Risk Cost': '£{:,.0f}'
            }).background_gradient(subset=['Avg Resilience'], cmap='RdYlGn'),
            use_container_width=True
        )
    
    def create_risk_analysis(self, data):
        """Create risk analysis visualizations"""
        st.header("⚠️ Risk Analysis")
        
        if data is None or len(data) == 0:
            st.warning("No data available for risk analysis")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk distribution donut chart
            risk_counts = data['risk_category'].value_counts()
            fig_risk = go.Figure(data=[go.Pie(
                labels=risk_counts.index,
                values=risk_counts.values,
                hole=0.4,
                marker_colors=['#dc3545', '#ffc107', '#28a745']
            )])
            fig_risk.update_layout(
                title='Risk Category Distribution',
                height=400,
                annotations=[dict(text='Risk<br>Categories', x=0.5, y=0.5, font_size=16, showarrow=False)]
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            # Risk probability vs Resilience scatter
            fig_scatter = px.scatter(
                data,
                x='resilience_score',
                y='risk_probability',
                color='risk_category',
                size='annual_risk_cost',
                hover_data=['asset_type', 'region'],
                title='Risk Probability vs Resilience Score',
                labels={
                    'resilience_score': 'Resilience Score',
                    'risk_probability': 'Risk Probability'
                },
                color_discrete_map={
                    'High': '#dc3545',
                    'Medium': '#ffc107',
                    'Low': '#28a745'
                }
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Top 10 high-risk assets table
        st.subheader("Top 10 High-Risk Assets")
        high_risk_assets = data.nlargest(10, 'risk_probability')[
            ['asset_id', 'asset_type', 'region', 'resilience_score', 
             'risk_probability', 'annual_risk_cost', 'downtime_hours_last_year']
        ]
        
        st.dataframe(
            high_risk_assets.style.format({
                'resilience_score': '{:.1f}',
                'risk_probability': '{:.4f}',
                'annual_risk_cost': '£{:,.0f}',
                'downtime_hours_last_year': '{:,.1f}'
            }),
            use_container_width=True
        )
    
    def create_asset_performance(self, data):
        """Create asset performance analysis"""
        st.header("🔧 Asset Performance")
        
        if data is None or len(data) == 0:
            st.warning("No data available for asset performance analysis")
            return
        
        # Asset type performance comparison
        asset_performance = data.groupby('asset_type').agg({
            'asset_id': 'count',
            'resilience_score': 'mean',
            'downtime_hours_last_year': 'mean',
            'failure_count_last_year': 'mean',
            'maintenance_compliance': 'mean',
            'annual_risk_cost': 'sum'
        }).round(2)
        
        asset_performance.columns = ['Count', 'Avg Resilience', 'Avg Downtime', 
                                   'Avg Failures', 'Avg Maintenance', 'Total Risk Cost']
        asset_performance = asset_performance.reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Asset type resilience comparison
            fig_performance = px.bar(
                asset_performance,
                x='asset_type',
                y='Avg Resilience',
                color='Avg Resilience',
                color_continuous_scale='RdYlGn',
                title='Average Resilience by Asset Type'
            )
            fig_performance.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_performance, use_container_width=True)
        
        with col2:
            # Downtime vs Maintenance compliance
            fig_maintenance = px.scatter(
                data,
                x='maintenance_compliance',
                y='downtime_hours_last_year',
                color='asset_type',
                title='Downtime vs Maintenance Compliance',
                labels={
                    'maintenance_compliance': 'Maintenance Compliance',
                    'downtime_hours_last_year': 'Downtime Hours (Last Year)'
                }
            )
            fig_maintenance.update_layout(height=400)
            st.plotly_chart(fig_maintenance, use_container_width=True)
        
        # Asset age analysis
        st.subheader("Asset Age Analysis")
        data['asset_age'] = 2024 - data['install_year']
        
        # Age vs Resilience
        fig_age = px.scatter(
            data,
            x='asset_age',
            y='resilience_score',
            color='asset_type',
            size='annual_risk_cost',
            title='Asset Age vs Resilience Score',
            labels={
                'asset_age': 'Asset Age (Years)',
                'resilience_score': 'Resilience Score'
            }
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    def create_forecasting_section(self, data):
        """Create forecasting and predictions section"""
        st.header("🔮 Forecasting & Predictions")
        
        if data is None or len(data) == 0:
            st.warning("No data available for forecasting")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Predicted Failures Next Year")
            
            # Simple failure prediction based on current trends
            high_risk_next_year = len(data[data['risk_probability'] > 0.6])
            medium_risk_next_year = len(data[(data['risk_probability'] > 0.3) & (data['risk_probability'] <= 0.6)])
            
            prediction_data = pd.DataFrame({
                'Risk Level': ['High Risk', 'Medium Risk', 'Low Risk'],
                'Predicted Failures': [
                    high_risk_next_year,
                    medium_risk_next_year, 
                    len(data) - high_risk_next_year - medium_risk_next_year
                ]
            })
            
            fig_prediction = px.bar(
                prediction_data,
                x='Risk Level',
                y='Predicted Failures',
                color='Risk Level',
                color_discrete_map={
                    'High Risk': '#dc3545',
                    'Medium Risk': '#ffc107',
                    'Low Risk': '#28a745'
                },
                title='Predicted Asset Failures Next Year'
            )
            st.plotly_chart(fig_prediction, use_container_width=True)
        
        with col2:
            st.subheader("Maintenance Recommendations")
            
            # Generate maintenance recommendations
            recommendations = []
            
            # Immediate action required
            immediate = data[
                (data['risk_probability'] > 0.8) & 
                (data['maintenance_compliance'] < 0.7)
            ]
            if len(immediate) > 0:
                recommendations.append(f"🚨 {len(immediate)} assets require immediate maintenance intervention")
            
            # Schedule maintenance
            schedule = data[
                (data['risk_probability'] > 0.6) & 
                (data['resilience_score'] < 50)
            ]
            if len(schedule) > 0:
                recommendations.append(f"📅 {len(schedule)} assets should have maintenance scheduled within 3 months")
            
            # Monitor closely
            monitor = data[
                (data['risk_probability'] > 0.4) & 
                (data['failure_count_last_year'] > 5)
            ]
            if len(monitor) > 0:
                recommendations.append(f"👀 {len(monitor)} assets require enhanced monitoring")
            
            # Replacement candidates
            old_assets = data[
                ((2024 - data['install_year']) > 25) & 
                (data['resilience_score'] < 60)
            ]
            if len(old_assets) > 0:
                recommendations.append(f"🔄 {len(old_assets)} old assets are candidates for replacement")
            
            for rec in recommendations:
                st.info(rec)
        
        # Investment priority matrix
        st.subheader("Investment Priority Matrix")
        
        # Calculate investment priority score
        data['investment_priority'] = (
            data['risk_probability'] * 0.3 +
            (1 - data['resilience_score']/100) * 0.3 +
            ((2024 - data['install_year'])/40) * 0.2 +
            (data['failure_count_last_year']/20) * 0.2
        ) * 100
        
        # Priority matrix scatter plot
        fig_priority = px.scatter(
            data,
            x='resilience_score',
            y='risk_probability',
            color='investment_priority',
            size='annual_risk_cost',
            hover_data=['asset_id', 'asset_type', 'region'],
            title='Investment Priority Matrix',
            labels={
                'resilience_score': 'Current Resilience Score',
                'risk_probability': 'Risk Probability'
            },
            color_continuous_scale='Reds'
        )
        
        # Add quadrant lines
        fig_priority.add_hline(y=0.5, line_dash="dash", line_color="gray")
        fig_priority.add_vline(x=50, line_dash="dash", line_color="gray")
        
        # Add quadrant annotations
        fig_priority.add_annotation(x=25, y=0.75, text="High Priority<br>Low Resilience + High Risk", 
                                  showarrow=False, bgcolor="rgba(255,0,0,0.1)")
        fig_priority.add_annotation(x=75, y=0.75, text="Monitor<br>Good Resilience + High Risk", 
                                  showarrow=False, bgcolor="rgba(255,255,0,0.1)")
        fig_priority.add_annotation(x=25, y=0.25, text="Replace/Upgrade<br>Low Resilience + Low Risk", 
                                  showarrow=False, bgcolor="rgba(255,165,0,0.1)")
        fig_priority.add_annotation(x=75, y=0.25, text="Maintain<br>Good Resilience + Low Risk", 
                                  showarrow=False, bgcolor="rgba(0,255,0,0.1)")
        
        st.plotly_chart(fig_priority, use_container_width=True)
    
    def create_export_section(self, data):
        """Create data export functionality"""
        st.header("📊 Export Data")
        
        if data is None or len(data) == 0:
            st.warning("No data available for export")
            return
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Export filtered data as CSV
            csv = data.to_csv(index=False)
            st.download_button(
                label="📁 Download CSV",
                data=csv,
                file_name=f"resilience_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export summary report
            summary_report = self.generate_summary_report(data)
            st.download_button(
                label="📋 Download Report",
                data=summary_report,
                file_name=f"resilience_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        with col3:
            # Display current filter summary
            st.info(f"Current dataset: {len(data):,} assets")
    
    def generate_summary_report(self, data):
        """Generate text summary report"""
        if data is None or len(data) == 0:
            return "No data available"
        
        report = f"""
RESILIENCE ANALYTICS SUMMARY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== OVERVIEW ===
Total Assets: {len(data):,}
Average Resilience Score: {data['resilience_score'].mean():.2f}
Total Annual Risk Cost: £{data['annual_risk_cost'].sum():,.0f}

=== RISK DISTRIBUTION ===
High Risk Assets: {len(data[data['risk_category'] == 'High']):,}
Medium Risk Assets: {len(data[data['risk_category'] == 'Medium']):,}
Low Risk Assets: {len(data[data['risk_category'] == 'Low']):,}

=== TOP REGIONS BY RISK COST ===
{data.groupby('region')['annual_risk_cost'].sum().sort_values(ascending=False).head().to_string()}

=== TOP ASSET TYPES BY RISK COST ===
{data.groupby('asset_type')['annual_risk_cost'].sum().sort_values(ascending=False).head().to_string()}

=== HIGH PRIORITY ACTIONS ===
Assets requiring immediate attention: {len(data[(data['risk_probability'] > 0.8) & (data['maintenance_compliance'] < 0.7)]):,}
Assets with poor resilience scores (<40): {len(data[data['resilience_score'] < 40]):,}
Assets with high downtime (>200 hours): {len(data[data['downtime_hours_last_year'] > 200]):,}
"""
        return report
    
    def run_dashboard(self):
        """Main dashboard runner"""
        # Initialize database connection
        if not self.connect_database():
            return
        
        # Create sidebar filters
        filters = self.create_filters_sidebar()
        
        # Load and filter data
        data = self.load_data()
        filtered_data = self.apply_filters(data, filters)
        
        # Create overview section
        self.create_overview_section()
        
        # Create main content tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🗺️ Regional", "⚠️ Risk Analysis", "🔧 Asset Performance", 
            "🔮 Forecasting", "📊 Export", "ℹ️ About"
        ])
        
        with tab1:
            self.create_regional_analysis(filtered_data)
        
        with tab2:
            self.create_risk_analysis(filtered_data)
        
        with tab3:
            self.create_asset_performance(filtered_data)
        
        with tab4:
            self.create_forecasting_section(filtered_data)
        
        with tab5:
            self.create_export_section(filtered_data)
        
        with tab6:
            self.create_about_section()
        
        # Footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #666; padding: 1rem;'>"
            "Water Utility Resilience Analytics System | "
            f"Data as of {datetime.now().strftime('%Y-%m-%d')} | "
            f"Showing {len(filtered_data) if filtered_data is not None else 0:,} assets"
            "</div>",
            unsafe_allow_html=True
        )
    
    def create_about_section(self):
        """Create about section with project information"""
        st.header("ℹ️ About")
        
        st.markdown("""
        ## Water Utility Resilience Analytics System
        
        This dashboard provides comprehensive analysis of water utility infrastructure resilience,
        helping identify risks, optimize maintenance, and improve operational efficiency.
        
        ### Key Features
        - **Real-time Risk Assessment**: Identify high-risk assets requiring immediate attention
        - **Regional Analysis**: Compare performance across different service areas
        - **Predictive Analytics**: Forecast potential failures and maintenance needs
        - **Cost Analysis**: Quantify financial impact of asset downtime and risks
        - **Interactive Filtering**: Drill down into specific asset types, regions, or risk levels
        
        ### Methodology
        - **Resilience Score**: Composite metric (0-100) based on reliability, maintainability, 
          redundancy, asset age, and criticality
        - **Risk Probability**: Machine learning model predicting likelihood of failure
        - **Impact Cost**: Financial cost calculation based on downtime and asset criticality
        
        ### Data Sources
        - Asset operational data
        - Maintenance records
        - Failure history
        - Performance metrics
        - Financial impact estimates
        
        ### Technology Stack
        - **Frontend**: Streamlit
        - **Database**: SQLite
        - **Analytics**: Python, Pandas, Scikit-learn
        - **Visualizations**: Plotly
        - **Data Processing**: Jupyter Notebooks
        
        ### Version Information
        - **Version**: 1.0.0
        - **Last Updated**: January 2025
        - **License**: MIT
        
        ---
        
        🔧 **System Requirements**
        - Python 3.8+
        - 8,000+ simulated assets
        - Real-time dashboard updates
        - Export capabilities (CSV, PDF)
        
        📧 **Support**: For technical support or questions, please contact the analytics team.
        """)


def main():
    """Main function to run the dashboard"""
    dashboard = ResilienceDashboard()
    dashboard.run_dashboard()


if __name__ == "__main__":
    main()