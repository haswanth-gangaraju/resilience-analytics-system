#!/usr/bin/env python3
"""
Resilience Analytics System - Database Setup

This script creates and populates a SQLite database with the resilience assets data.
Provides functions to load CSV data into SQLite for dashboard queries.

Author: Resilience Analytics Team
Date: 2025
"""

import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text
import os
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResilienceDatabase:
    """
    Database management class for Resilience Analytics System
    """
    
    def __init__(self, db_path='../data/resilience_analytics.db'):
        """
        Initialize database connection
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.engine = None
        
    def create_connection(self):
        """Create SQLAlchemy engine for database operations"""
        try:
            # Ensure database directory exists
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            # Create SQLAlchemy engine
            self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
            logger.info(f"Database connection created: {self.db_path}")
            return self.engine
            
        except Exception as e:
            logger.error(f"Failed to create database connection: {e}")
            raise
    
    def load_csv_to_database(self, csv_file, table_name='resilience_assets', if_exists='replace'):
        """
        Load CSV data into SQLite database
        
        Args:
            csv_file (str): Path to CSV file
            table_name (str): Name of database table
            if_exists (str): How to behave if table exists ('replace', 'append', 'fail')
        """
        try:
            # Check if CSV file exists
            if not os.path.exists(csv_file):
                raise FileNotFoundError(f"CSV file not found: {csv_file}")
            
            # Create database connection if not exists
            if not self.engine:
                self.create_connection()
            
            # Read CSV file
            logger.info(f"Loading CSV file: {csv_file}")
            df = pd.read_csv(csv_file)
            logger.info(f"Loaded {len(df):,} records from CSV")
            
            # Data validation
            self._validate_data(df)
            
            # Load data into database
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            logger.info(f"Data successfully loaded into table: {table_name}")
            
            # Create indexes for better query performance
            self._create_indexes(table_name)
            
            # Verify data loading
            self._verify_data_load(table_name, len(df))
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load CSV to database: {e}")
            raise
    
    def _validate_data(self, df):
        """
        Validate data quality before loading to database
        
        Args:
            df (pandas.DataFrame): Data to validate
        """
        logger.info("Validating data quality...")
        
        # Check for required columns
        required_columns = [
            'asset_id', 'region', 'asset_type', 'resilience_score',
            'risk_category', 'risk_probability', 'impact_cost'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check for null values in critical columns
        critical_nulls = df[required_columns].isnull().sum()
        if critical_nulls.any():
            logger.warning(f"Null values found in critical columns: {critical_nulls[critical_nulls > 0].to_dict()}")
        
        # Check data ranges
        if (df['resilience_score'] < 0).any() or (df['resilience_score'] > 100).any():
            raise ValueError("Resilience scores must be between 0 and 100")
        
        if (df['risk_probability'] < 0).any() or (df['risk_probability'] > 1).any():
            raise ValueError("Risk probabilities must be between 0 and 1")
        
        # Check for duplicate asset IDs
        if df['asset_id'].duplicated().any():
            raise ValueError("Duplicate asset IDs found")
        
        logger.info("Data validation completed successfully")
    
    def _create_indexes(self, table_name):
        """
        Create database indexes for improved query performance
        
        Args:
            table_name (str): Name of the table to index
        """
        try:
            with self.engine.connect() as conn:
                # Create indexes on commonly queried columns
                indexes = [
                    f"CREATE INDEX IF NOT EXISTS idx_{table_name}_asset_id ON {table_name} (asset_id)",
                    f"CREATE INDEX IF NOT EXISTS idx_{table_name}_region ON {table_name} (region)",
                    f"CREATE INDEX IF NOT EXISTS idx_{table_name}_asset_type ON {table_name} (asset_type)",
                    f"CREATE INDEX IF NOT EXISTS idx_{table_name}_risk_category ON {table_name} (risk_category)",
                    f"CREATE INDEX IF NOT EXISTS idx_{table_name}_resilience_score ON {table_name} (resilience_score)",
                    f"CREATE INDEX IF NOT EXISTS idx_{table_name}_risk_prob ON {table_name} (risk_probability)"
                ]
                
                for index_sql in indexes:
                    conn.execute(text(index_sql))
                    
                conn.commit()
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"Failed to create indexes: {e}")
    
    def _verify_data_load(self, table_name, expected_rows):
        """
        Verify that data was loaded correctly
        
        Args:
            table_name (str): Name of the table to verify
            expected_rows (int): Expected number of rows
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) as count FROM {table_name}"))
                actual_rows = result.fetchone()[0]
                
                if actual_rows == expected_rows:
                    logger.info(f"Data verification successful: {actual_rows:,} rows loaded")
                else:
                    logger.warning(f"Row count mismatch. Expected: {expected_rows}, Actual: {actual_rows}")
                
        except Exception as e:
            logger.error(f"Data verification failed: {e}")
    
    def execute_query(self, query, params=None):
        """
        Execute SQL query and return results
        
        Args:
            query (str): SQL query to execute
            params (dict, optional): Query parameters
            
        Returns:
            pandas.DataFrame: Query results
        """
        try:
            if not self.engine:
                self.create_connection()
            
            df = pd.read_sql_query(query, self.engine, params=params)
            return df
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def get_table_info(self, table_name='resilience_assets'):
        """
        Get table schema and basic statistics
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            dict: Table information
        """
        try:
            # Get table schema
            schema_query = f"PRAGMA table_info({table_name})"
            schema_df = self.execute_query(schema_query)
            
            # Get row count
            count_query = f"SELECT COUNT(*) as total_rows FROM {table_name}"
            count_df = self.execute_query(count_query)
            
            # Get sample data
            sample_query = f"SELECT * FROM {table_name} LIMIT 5"
            sample_df = self.execute_query(sample_query)
            
            return {
                'schema': schema_df,
                'row_count': count_df.iloc[0]['total_rows'],
                'sample_data': sample_df
            }
            
        except Exception as e:
            logger.error(f"Failed to get table info: {e}")
            return None
    
    def close_connection(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


def main():
    """
    Main function to set up the database with resilience assets data
    """
    try:
        logger.info("Starting Resilience Analytics Database Setup...")
        
        # Initialize database
        db = ResilienceDatabase()
        
        # Path to enhanced dataset
        enhanced_data_file = '../data/resilience_assets_enhanced.csv'
        
        # Check if enhanced data exists, otherwise use basic dataset
        if os.path.exists(enhanced_data_file):
            csv_file = enhanced_data_file
            logger.info("Using enhanced dataset with resilience scores")
        else:
            basic_data_file = '../data/resilience_assets.csv'
            if os.path.exists(basic_data_file):
                csv_file = basic_data_file
                logger.info("Using basic dataset (run notebooks first for enhanced features)")
            else:
                raise FileNotFoundError(
                    "No data files found. Please run the notebooks first:\n"
                    "1. 01_data_simulation.ipynb\n"
                    "2. 02_resilience_metrics.ipynb"
                )
        
        # Load data into database
        logger.info(f"Loading data from: {csv_file}")
        db.load_csv_to_database(csv_file, table_name='resilience_assets')
        
        # Display table information
        table_info = db.get_table_info()
        if table_info:
            logger.info(f"Database setup completed successfully!")
            logger.info(f"Total rows loaded: {table_info['row_count']:,}")
            logger.info(f"Columns: {len(table_info['schema'])} columns")
            
            print("\n=== DATABASE SETUP SUMMARY ===")
            print(f"Database: {db.db_path}")
            print(f"Table: resilience_assets")
            print(f"Rows: {table_info['row_count']:,}")
            print(f"Columns: {len(table_info['schema'])}")
            
            print("\n=== COLUMN SCHEMA ===")
            for _, row in table_info['schema'].iterrows():
                print(f"  {row['name']} ({row['type']})")
            
            print("\n=== SAMPLE DATA ===")
            print(table_info['sample_data'].head(3).to_string(index=False))
            
        # Close connection
        db.close_connection()
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()