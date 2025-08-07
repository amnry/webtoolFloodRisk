#!/usr/bin/env python3
"""
Demo script for MindsDB Integration
Simple example showing how to use the coastal data MindsDB integration.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mindsdb_integration import CoastalDataMindsDB

def demo_basic_usage():
    """Demo basic MindsDB integration usage"""
    print("🌊 MindsDB Integration Demo")
    print("=" * 40)
    
    # Initialize MindsDB integration
    coastal_mindsdb = CoastalDataMindsDB()
    
    # Demo 1: Load tide data only (fastest)
    print("\n📊 Demo 1: Loading Tide Data")
    print("-" * 30)
    coastal_mindsdb.load_tide_data()
    
    # Demo 2: Create a simple tide prediction model
    print("\n🤖 Demo 2: Creating Tide Prediction Model")
    print("-" * 40)
    try:
        # Create a simple tide predictor
        tide_model = coastal_mindsdb.connection.query("""
            CREATE MODEL tide_demo_predictor
            FROM tide_predictions
            PREDICT prediction
            USING 
                engine = 'lightwood',
                timeseries_settings = {
                    'is_timeseries': True,
                    'order_by': 'date',
                    'window': 24
                }
        """)
        print("✅ Created tide prediction model")
    except Exception as e:
        print(f"❌ Could not create model: {e}")
    
    # Demo 3: Generate some insights
    print("\n💡 Demo 3: Generating Insights")
    print("-" * 30)
    try:
        # Analyze tide patterns
        tide_analysis = coastal_mindsdb.connection.query("""
            SELECT 
                station, 
                type,
                AVG(prediction) as avg_prediction,
                COUNT(*) as data_points
            FROM tide_predictions
            WHERE prediction IS NOT NULL
            GROUP BY station, type
        """)
        
        if tide_analysis:
            print("📊 Tide Analysis Results:")
            for row in tide_analysis[:5]:  # Show first 5 results
                print(f"   Station: {row.get('station', 'N/A')}")
                print(f"   Type: {row.get('type', 'N/A')}")
                print(f"   Avg Prediction: {row.get('avg_prediction', 'N/A'):.2f}")
                print(f"   Data Points: {row.get('data_points', 'N/A')}")
                print()
    except Exception as e:
        print(f"❌ Could not generate insights: {e}")
    
    # Demo 4: Export results
    print("\n📁 Demo 4: Exporting Results")
    print("-" * 30)
    try:
        coastal_mindsdb.export_results("demo_results")
        print("✅ Results exported to demo_results/ directory")
    except Exception as e:
        print(f"❌ Could not export results: {e}")

def demo_satellite_data():
    """Demo satellite data processing (limited for performance)"""
    print("\n🛰️ Demo: Satellite Data Processing")
    print("=" * 40)
    
    coastal_mindsdb = CoastalDataMindsDB()
    
    # Load limited satellite data for demo
    print("📊 Loading satellite data (limited to 2 files for demo)...")
    coastal_mindsdb.load_satellite_data(limit_files=2)
    
    # Show what data was loaded
    try:
        satellite_data = coastal_mindsdb.connection.query("""
            SELECT 
                COUNT(*) as total_records,
                MIN(date) as earliest_date,
                MAX(date) as latest_date,
                AVG(sea_level_anomaly) as avg_sea_level
            FROM satellite_sea_level
            WHERE sea_level_anomaly IS NOT NULL
        """)
        
        if satellite_data:
            print("📈 Satellite Data Summary:")
            for row in satellite_data:
                print(f"   Total Records: {row.get('total_records', 'N/A')}")
                print(f"   Date Range: {row.get('earliest_date', 'N/A')} to {row.get('latest_date', 'N/A')}")
                print(f"   Avg Sea Level Anomaly: {row.get('avg_sea_level', 'N/A'):.4f}")
    except Exception as e:
        print(f"❌ Could not query satellite data: {e}")

def demo_combined_analysis():
    """Demo combined analysis of multiple datasets"""
    print("\n🔗 Demo: Combined Data Analysis")
    print("=" * 35)
    
    coastal_mindsdb = CoastalDataMindsDB()
    
    # Load both tide and satellite data
    print("📊 Loading combined datasets...")
    coastal_mindsdb.load_tide_data()
    coastal_mindsdb.load_satellite_data(limit_files=1)
    
    # Perform combined analysis
    try:
        combined_analysis = coastal_mindsdb.connection.query("""
            SELECT 
                'Tide Data' as data_type,
                COUNT(*) as record_count,
                AVG(prediction) as avg_value
            FROM tide_predictions
            WHERE prediction IS NOT NULL
            UNION ALL
            SELECT 
                'Satellite Data' as data_type,
                COUNT(*) as record_count,
                AVG(sea_level_anomaly) as avg_value
            FROM satellite_sea_level
            WHERE sea_level_anomaly IS NOT NULL
        """)
        
        if combined_analysis:
            print("📊 Combined Dataset Summary:")
            for row in combined_analysis:
                print(f"   {row.get('data_type', 'N/A')}:")
                print(f"     Records: {row.get('record_count', 'N/A')}")
                print(f"     Avg Value: {row.get('avg_value', 'N/A'):.4f}")
                print()
    except Exception as e:
        print(f"❌ Could not perform combined analysis: {e}")

def demo_prediction_queries():
    """Demo prediction queries"""
    print("\n🔮 Demo: Prediction Queries")
    print("=" * 30)
    
    coastal_mindsdb = CoastalDataMindsDB()
    
    # Load data first
    coastal_mindsdb.load_tide_data()
    
    # Demo prediction queries
    try:
        # Simple tide prediction query
        print("📈 Sample Tide Prediction Query:")
        print("SELECT * FROM tide_predictions WHERE station = 'portjefferson' LIMIT 5;")
        
        sample_predictions = coastal_mindsdb.connection.query("""
            SELECT date, time, prediction, type, station
            FROM tide_predictions 
            WHERE station = 'portjefferson' 
            LIMIT 5
        """)
        
        if sample_predictions:
            print("Results:")
            for row in sample_predictions:
                print(f"   {row.get('date', 'N/A')} {row.get('time', 'N/A')}: "
                      f"{row.get('prediction', 'N/A'):.2f}m ({row.get('type', 'N/A')})")
        
        print("\n📊 Statistical Query:")
        print("SELECT station, AVG(prediction) FROM tide_predictions GROUP BY station;")
        
        station_stats = coastal_mindsdb.connection.query("""
            SELECT station, AVG(prediction) as avg_prediction
            FROM tide_predictions 
            WHERE prediction IS NOT NULL
            GROUP BY station
        """)
        
        if station_stats:
            print("Results:")
            for row in station_stats:
                print(f"   {row.get('station', 'N/A')}: {row.get('avg_prediction', 'N/A'):.2f}m")
                
    except Exception as e:
        print(f"❌ Could not run prediction queries: {e}")

def main():
    """Run all demos"""
    print("🚀 MindsDB Integration Demo Suite")
    print("=" * 40)
    
    # Check if MindsDB is available
    try:
        import mindsdb
        print("✅ MindsDB is available")
    except ImportError:
        print("❌ MindsDB not available. Please install first:")
        print("pip install mindsdb")
        return
    
    # Run demos
    try:
        # Basic usage demo
        demo_basic_usage()
        
        # Satellite data demo (limited)
        demo_satellite_data()
        
        # Combined analysis demo
        demo_combined_analysis()
        
        # Prediction queries demo
        demo_prediction_queries()
        
        print("\n✅ All demos completed successfully!")
        print("\n📚 Next Steps:")
        print("   1. Review the demo_results/ directory for exported data")
        print("   2. Try running the full pipeline: python mindsdb_integration.py")
        print("   3. Explore the MINDSDB_INTEGRATION_README.md for detailed usage")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Please check that MindsDB server is running and all dependencies are installed.")

if __name__ == "__main__":
    main()
