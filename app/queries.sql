-- Resilience Analytics System - SQL Queries
-- Collection of analytical queries for the resilience dashboard
-- Database: SQLite (resilience_analytics.db)
-- Table: resilience_assets

-- =============================================================================
-- BASIC STATISTICS AND OVERVIEW QUERIES
-- =============================================================================

-- Query 1: Overall System Health Dashboard KPIs
SELECT 
    COUNT(*) as total_assets,
    ROUND(AVG(resilience_score), 2) as avg_resilience_score,
    ROUND(SUM(downtime_hours_last_year), 0) as total_downtime_hours,
    COUNT(CASE WHEN risk_category = 'High' THEN 1 END) as high_risk_count,
    COUNT(CASE WHEN risk_category = 'Medium' THEN 1 END) as medium_risk_count,
    COUNT(CASE WHEN risk_category = 'Low' THEN 1 END) as low_risk_count,
    ROUND(SUM(annual_risk_cost), 0) as total_annual_risk_cost
FROM resilience_assets;

-- Query 2: Asset Distribution by Type and Region
SELECT 
    asset_type,
    region,
    COUNT(*) as asset_count,
    ROUND(AVG(resilience_score), 2) as avg_resilience_score,
    ROUND(AVG(risk_probability), 3) as avg_risk_probability
FROM resilience_assets
GROUP BY asset_type, region
ORDER BY avg_risk_probability DESC;

-- Query 3: Resilience Score Distribution
SELECT 
    CASE 
        WHEN resilience_score >= 80 THEN 'Excellent (80-100)'
        WHEN resilience_score >= 65 THEN 'Good (65-79)'
        WHEN resilience_score >= 50 THEN 'Average (50-64)'
        WHEN resilience_score >= 35 THEN 'Poor (35-49)'
        ELSE 'Critical (<35)'
    END as resilience_category,
    COUNT(*) as asset_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM resilience_assets), 2) as percentage
FROM resilience_assets
GROUP BY resilience_category
ORDER BY 
    CASE 
        WHEN resilience_score >= 80 THEN 1
        WHEN resilience_score >= 65 THEN 2
        WHEN resilience_score >= 50 THEN 3
        WHEN resilience_score >= 35 THEN 4
        ELSE 5
    END;

-- =============================================================================
-- HIGH-RISK ASSET IDENTIFICATION
-- =============================================================================

-- Query 4: Top 10 Highest Risk Assets
SELECT 
    asset_id,
    asset_type,
    region,
    ROUND(resilience_score, 2) as resilience_score,
    risk_category,
    ROUND(risk_probability, 4) as risk_probability,
    downtime_hours_last_year,
    failure_count_last_year,
    ROUND(annual_risk_cost, 0) as annual_risk_cost,
    ROUND(criticality_score, 1) as criticality_score
FROM resilience_assets
WHERE risk_category = 'High'
ORDER BY risk_probability DESC, annual_risk_cost DESC
LIMIT 10;

-- Query 5: Assets Requiring Immediate Attention (Multi-criteria)
SELECT 
    asset_id,
    asset_type,
    region,
    resilience_score,
    risk_probability,
    downtime_hours_last_year,
    failure_count_last_year,
    maintenance_compliance,
    annual_risk_cost,
    'Multiple Risk Factors' as alert_reason
FROM resilience_assets
WHERE 
    risk_category = 'High' 
    AND resilience_score < 50 
    AND maintenance_compliance < 0.8
ORDER BY annual_risk_cost DESC;

-- Query 6: Critical Assets with High Downtime
SELECT 
    asset_id,
    asset_type,
    region,
    resilience_score,
    downtime_hours_last_year,
    criticality_score,
    annual_risk_cost,
    ROUND(downtime_hours_last_year / 8760.0 * 100, 2) as downtime_percentage
FROM resilience_assets
WHERE 
    criticality_score >= 7 
    AND downtime_hours_last_year > 100
ORDER BY downtime_hours_last_year DESC;

-- =============================================================================
-- REGIONAL AND GEOGRAPHIC ANALYSIS
-- =============================================================================

-- Query 7: Regional Resilience Performance
SELECT 
    region,
    COUNT(*) as total_assets,
    ROUND(AVG(resilience_score), 2) as avg_resilience_score,
    ROUND(AVG(risk_probability), 4) as avg_risk_probability,
    COUNT(CASE WHEN risk_category = 'High' THEN 1 END) as high_risk_assets,
    ROUND(SUM(annual_risk_cost), 0) as total_annual_risk_cost,
    ROUND(AVG(downtime_hours_last_year), 1) as avg_downtime_hours,
    ROUND(AVG(maintenance_compliance), 3) as avg_maintenance_compliance
FROM resilience_assets
GROUP BY region
ORDER BY avg_resilience_score DESC;

-- Query 8: Regional Risk Heatmap Data
SELECT 
    region,
    asset_type,
    COUNT(*) as asset_count,
    AVG(risk_probability) as avg_risk_prob,
    CASE 
        WHEN AVG(risk_probability) >= 0.7 THEN 'Very High'
        WHEN AVG(risk_probability) >= 0.5 THEN 'High'
        WHEN AVG(risk_probability) >= 0.3 THEN 'Medium'
        ELSE 'Low'
    END as risk_level
FROM resilience_assets
GROUP BY region, asset_type
ORDER BY region, avg_risk_prob DESC;

-- =============================================================================
-- ASSET TYPE AND PERFORMANCE ANALYSIS
-- =============================================================================

-- Query 9: Asset Type Performance Comparison
SELECT 
    asset_type,
    COUNT(*) as total_count,
    ROUND(AVG(resilience_score), 2) as avg_resilience,
    ROUND(AVG(downtime_hours_last_year), 1) as avg_downtime,
    ROUND(AVG(failure_count_last_year), 1) as avg_failures,
    ROUND(AVG(mean_time_to_repair), 1) as avg_mttr,
    ROUND(AVG(maintenance_compliance), 3) as avg_maintenance,
    ROUND(SUM(annual_risk_cost), 0) as total_risk_cost
FROM resilience_assets
GROUP BY asset_type
ORDER BY avg_resilience DESC;

-- Query 10: Asset Age Analysis
SELECT 
    CASE 
        WHEN (2024 - install_year) <= 5 THEN 'New (0-5 years)'
        WHEN (2024 - install_year) <= 15 THEN 'Modern (6-15 years)'
        WHEN (2024 - install_year) <= 25 THEN 'Mature (16-25 years)'
        WHEN (2024 - install_year) <= 35 THEN 'Old (26-35 years)'
        ELSE 'Legacy (35+ years)'
    END as age_category,
    COUNT(*) as asset_count,
    ROUND(AVG(resilience_score), 2) as avg_resilience,
    ROUND(AVG(failure_count_last_year), 2) as avg_failures,
    ROUND(AVG(maintenance_compliance), 3) as avg_maintenance
FROM resilience_assets
GROUP BY age_category
ORDER BY 
    CASE 
        WHEN (2024 - install_year) <= 5 THEN 1
        WHEN (2024 - install_year) <= 15 THEN 2
        WHEN (2024 - install_year) <= 25 THEN 3
        WHEN (2024 - install_year) <= 35 THEN 4
        ELSE 5
    END;

-- =============================================================================
-- MAINTENANCE AND OPERATIONAL INSIGHTS
-- =============================================================================

-- Query 11: Maintenance Compliance vs Performance
SELECT 
    CASE 
        WHEN maintenance_compliance >= 0.9 THEN 'Excellent (90-100%)'
        WHEN maintenance_compliance >= 0.8 THEN 'Good (80-89%)'
        WHEN maintenance_compliance >= 0.7 THEN 'Average (70-79%)'
        WHEN maintenance_compliance >= 0.6 THEN 'Poor (60-69%)'
        ELSE 'Critical (<60%)'
    END as maintenance_category,
    COUNT(*) as asset_count,
    ROUND(AVG(resilience_score), 2) as avg_resilience,
    ROUND(AVG(downtime_hours_last_year), 1) as avg_downtime,
    ROUND(AVG(failure_count_last_year), 2) as avg_failures
FROM resilience_assets
GROUP BY maintenance_category
ORDER BY AVG(maintenance_compliance) DESC;

-- Query 12: Redundancy Impact Analysis
SELECT 
    redundancy_level,
    COUNT(*) as asset_count,
    ROUND(AVG(resilience_score), 2) as avg_resilience,
    ROUND(AVG(downtime_hours_last_year), 1) as avg_downtime,
    COUNT(CASE WHEN risk_category = 'High' THEN 1 END) as high_risk_count,
    ROUND(AVG(annual_risk_cost), 0) as avg_annual_risk_cost
FROM resilience_assets
GROUP BY redundancy_level
ORDER BY 
    CASE redundancy_level
        WHEN 'N+2' THEN 1
        WHEN 'N+1' THEN 2
        WHEN 'Full' THEN 3
        WHEN 'Partial' THEN 4
        WHEN 'None' THEN 5
    END;

-- =============================================================================
-- FINANCIAL AND COST ANALYSIS
-- =============================================================================

-- Query 13: Cost Analysis by Risk Category
SELECT 
    risk_category,
    COUNT(*) as asset_count,
    ROUND(SUM(impact_cost), 0) as total_impact_cost,
    ROUND(SUM(annual_risk_cost), 0) as total_annual_risk_cost,
    ROUND(AVG(impact_cost), 0) as avg_impact_cost,
    ROUND(AVG(annual_risk_cost), 0) as avg_annual_risk_cost
FROM resilience_assets
GROUP BY risk_category
ORDER BY total_annual_risk_cost DESC;

-- Query 14: Top Cost Impact Assets
SELECT 
    asset_id,
    asset_type,
    region,
    resilience_score,
    downtime_hours_last_year,
    ROUND(impact_cost, 0) as impact_cost,
    ROUND(annual_risk_cost, 0) as annual_risk_cost,
    risk_category
FROM resilience_assets
ORDER BY annual_risk_cost DESC
LIMIT 20;

-- =============================================================================
-- TREND ANALYSIS AND CORRELATIONS
-- =============================================================================

-- Query 15: Downtime vs Maintenance Correlation
SELECT 
    CASE 
        WHEN downtime_hours_last_year < 10 THEN 'Very Low (<10h)'
        WHEN downtime_hours_last_year < 50 THEN 'Low (10-50h)'
        WHEN downtime_hours_last_year < 100 THEN 'Medium (50-100h)'
        WHEN downtime_hours_last_year < 200 THEN 'High (100-200h)'
        ELSE 'Very High (200h+)'
    END as downtime_category,
    COUNT(*) as asset_count,
    ROUND(AVG(maintenance_compliance), 3) as avg_maintenance_compliance,
    ROUND(AVG(failure_count_last_year), 2) as avg_failures,
    ROUND(AVG(mean_time_to_repair), 1) as avg_mttr
FROM resilience_assets
GROUP BY downtime_category
ORDER BY AVG(downtime_hours_last_year);

-- Query 16: Energy Consumption vs Performance
SELECT 
    asset_type,
    ROUND(AVG(energy_consumption_kwh), 0) as avg_energy_consumption,
    ROUND(AVG(resilience_score), 2) as avg_resilience_score,
    ROUND(AVG(downtime_hours_last_year), 1) as avg_downtime,
    COUNT(*) as asset_count
FROM resilience_assets
WHERE energy_consumption_kwh > 0
GROUP BY asset_type
ORDER BY avg_energy_consumption DESC;

-- =============================================================================
-- PREDICTIVE AND FORECASTING QUERIES
-- =============================================================================

-- Query 17: Failure Prediction Risk Factors
SELECT 
    asset_id,
    asset_type,
    region,
    resilience_score,
    risk_probability,
    (2024 - install_year) as asset_age,
    maintenance_compliance,
    failure_count_last_year,
    downtime_hours_last_year,
    CASE 
        WHEN risk_probability >= 0.8 AND maintenance_compliance < 0.7 THEN 'Immediate Action Required'
        WHEN risk_probability >= 0.6 AND resilience_score < 50 THEN 'Schedule Maintenance'
        WHEN risk_probability >= 0.4 AND failure_count_last_year > 5 THEN 'Monitor Closely'
        ELSE 'Standard Monitoring'
    END as recommendation
FROM resilience_assets
WHERE risk_probability >= 0.4
ORDER BY risk_probability DESC;

-- Query 18: Asset Replacement Priority Score
SELECT 
    asset_id,
    asset_type,
    region,
    (2024 - install_year) as asset_age,
    resilience_score,
    risk_probability,
    annual_risk_cost,
    -- Replacement priority calculation
    ROUND(
        (risk_probability * 0.3 + 
         (1 - resilience_score/100) * 0.3 + 
         ((2024 - install_year)/40) * 0.2 + 
         (failure_count_last_year/20) * 0.2) * 100, 2
    ) as replacement_priority_score
FROM resilience_assets
WHERE (2024 - install_year) > 20 OR resilience_score < 60
ORDER BY replacement_priority_score DESC
LIMIT 50;

-- =============================================================================
-- UTILITY QUERIES FOR DASHBOARD FILTERS
-- =============================================================================

-- Query 19: Get Distinct Values for Filters
SELECT 'regions' as filter_type, region as filter_value FROM resilience_assets GROUP BY region
UNION ALL
SELECT 'asset_types' as filter_type, asset_type as filter_value FROM resilience_assets GROUP BY asset_type
UNION ALL
SELECT 'risk_categories' as filter_type, risk_category as filter_value FROM resilience_assets GROUP BY risk_category
UNION ALL
SELECT 'redundancy_levels' as filter_type, redundancy_level as filter_value FROM resilience_assets GROUP BY redundancy_level;

-- Query 20: Time Series Data for Trends (by installation year)
SELECT 
    install_year,
    COUNT(*) as assets_installed,
    ROUND(AVG(resilience_score), 2) as avg_resilience,
    ROUND(AVG(maintenance_compliance), 3) as avg_maintenance,
    COUNT(CASE WHEN risk_category = 'High' THEN 1 END) as high_risk_count
FROM resilience_assets
WHERE install_year >= 2000
GROUP BY install_year
ORDER BY install_year;

-- =============================================================================
-- DATA QUALITY AND MONITORING QUERIES
-- =============================================================================

-- Query 21: Data Quality Check
SELECT 
    'Total Records' as metric,
    COUNT(*) as value
FROM resilience_assets
UNION ALL
SELECT 
    'Records with Null Resilience Score' as metric,
    COUNT(*) as value
FROM resilience_assets
WHERE resilience_score IS NULL
UNION ALL
SELECT 
    'Records with Invalid Risk Probability' as metric,
    COUNT(*) as value
FROM resilience_assets
WHERE risk_probability < 0 OR risk_probability > 1
UNION ALL
SELECT 
    'Duplicate Asset IDs' as metric,
    COUNT(*) - COUNT(DISTINCT asset_id) as value
FROM resilience_assets;

-- Query 22: Summary Statistics for Dashboard
SELECT 
    MIN(resilience_score) as min_resilience,
    MAX(resilience_score) as max_resilience,
    ROUND(AVG(resilience_score), 2) as avg_resilience,
    MIN(risk_probability) as min_risk_prob,
    MAX(risk_probability) as max_risk_prob,
    ROUND(AVG(risk_probability), 4) as avg_risk_prob,
    MIN(install_year) as oldest_asset_year,
    MAX(install_year) as newest_asset_year,
    ROUND(SUM(annual_risk_cost), 0) as total_annual_risk_cost
FROM resilience_assets;