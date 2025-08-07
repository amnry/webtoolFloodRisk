#!/usr/bin/env python3
"""
MindsDB Integration for Coastal Data Analysis
Connects all datasets in the webtool folder to MindsDB for AI-powered analysis.
"""

import os
import sys
import pandas as pd
import numpy as np
import xarray as xr
from datetime import datetime, timedelta
import json
import sqlite3
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import local modules
from tide_data_parser import parse_tide_data
from jiayou_sat_data.sa_data import read_satellite_data_station

try:
    import mindsdb
    from mindsdb import Predictor
    from mindsdb.libs.controllers.storage import FileStorage
    MINDSDB_AVAILABLE = True
except ImportError:
    print("MindsDB not installed. Installing...")
    MINDSDB_AVAILABLE = False

class CoastalDataMindsDB:
    """
    MindsDB integration for coastal data analysis.
    Connects satellite data, tide predictions, and processed data to MindsDB.
    """
    
    def __init__(self, mindsdb_host='localhost', mindsdb_port=47334):
        self.mindsdb_host = mindsdb_host
        self.mindsdb_port = mindsdb_port
        self.connection = None
        self.predictor = None
        
        if MINDSDB_AVAILABLE:
            self._connect_mindsdb()
    
    def _connect_mindsdb(self):
        """Connect to MindsDB instance"""
        try:
            self.connection = mindsdb.connect(
                host=self.mindsdb_host,
                port=self.mindsdb_port
            )
            print("✅ Connected to MindsDB successfully")
        except Exception as e:
            print(f"❌ Failed to connect to MindsDB: {e}")
            self.connection = None
    
    def load_satellite_data(self, station_ids=None, limit_files=10):
        """
        Load satellite data into MindsDB
        
        Args:
            station_ids: List of station IDs to process (None for all)
            limit_files: Limit number of NetCDF files to process (for testing)
        """
        if not self.connection:
            print("❌ MindsDB connection not available")
            return
        
        print("🛰️ Loading satellite data into MindsDB...")
        
        # Get satellite data files
        satellite_dir = Path("jiayou_sat_data/monthly_raw")
        if not satellite_dir.exists():
            print(f"❌ Satellite data directory not found: {satellite_dir}")
            return
        
        nc_files = list(satellite_dir.glob("*.nc"))
        if limit_files:
            nc_files = nc_files[:limit_files]
        
        print(f"📊 Found {len(nc_files)} satellite data files")
        
        # Process each file and extract data
        all_satellite_data = []
        
        for file_path in nc_files[:5]:  # Process first 5 files for demo
            try:
                print(f"Processing {file_path.name}...")
                
                # Read NetCDF file
                ds = xr.open_dataset(file_path)
                
                # Extract time information
                time_coords = ds.time.values
                
                # Extract sea level anomaly data
                if 'sla' in ds.variables:
                    sla_data = ds.sla.values
                    
                    # Get coordinates
                    lats = ds.lat.values if 'lat' in ds.coords else None
                    lons = ds.lon.values if 'lon' in ds.coords else None
                    
                    # Create sample data points (for demo purposes)
                    # In production, you'd want to extract all valid data points
                    sample_indices = np.random.choice(len(time_coords), min(100, len(time_coords)), replace=False)
                    
                    for idx in sample_indices:
                        time_val = pd.to_datetime(time_coords[idx])
                        
                        # Sample some spatial points
                        if sla_data.ndim >= 3:
                            # Take a sample from the spatial grid
                            lat_idx = np.random.randint(0, sla_data.shape[1] if sla_data.shape[1] > 0 else 1)
                            lon_idx = np.random.randint(0, sla_data.shape[2] if sla_data.shape[2] > 0 else 1)
                            
                            sla_value = float(sla_data[idx, lat_idx, lon_idx])
                            lat_value = float(lats[lat_idx]) if lats is not None else 0.0
                            lon_value = float(lons[lon_idx]) if lons is not None else 0.0
                        else:
                            sla_value = float(sla_data[idx]) if sla_data.ndim == 1 else 0.0
                            lat_value = 0.0
                            lon_value = 0.0
                        
                        # Skip NaN values
                        if not np.isnan(sla_value):
                            all_satellite_data.append({
                                'timestamp': time_val.isoformat(),
                                'date': time_val.strftime('%Y-%m-%d'),
                                'year': time_val.year,
                                'month': time_val.month,
                                'day': time_val.day,
                                'sea_level_anomaly': sla_value,
                                'latitude': lat_value,
                                'longitude': lon_value,
                                'data_source': 'satellite_altimetry',
                                'file_name': file_path.name
                            })
                
                ds.close()
                
            except Exception as e:
                print(f"❌ Error processing {file_path.name}: {e}")
                continue
        
        if all_satellite_data:
            # Create DataFrame
            satellite_df = pd.DataFrame(all_satellite_data)
            
            # Save to CSV for MindsDB
            satellite_csv_path = "satellite_data_for_mindsdb.csv"
            satellite_df.to_csv(satellite_csv_path, index=False)
            
            # Upload to MindsDB
            try:
                self.connection.upload_file(
                    satellite_csv_path,
                    'satellite_data',
                    'satellite_sea_level'
                )
                print(f"✅ Uploaded {len(satellite_df)} satellite data records to MindsDB")
            except Exception as e:
                print(f"❌ Failed to upload satellite data: {e}")
            
            # Clean up
            if os.path.exists(satellite_csv_path):
                os.remove(satellite_csv_path)
    
    def load_tide_data(self):
        """Load tide prediction data into MindsDB"""
        if not self.connection:
            print("❌ MindsDB connection not available")
            return
        
        print("🌊 Loading tide prediction data into MindsDB...")
        
        # Available stations
        stations = ['portjefferson', 'miami', 'nyc']
        all_tide_data = []
        
        for station in stations:
            try:
                print(f"Processing tide data for {station}...")
                
                # Parse tide data
                tide_data = parse_tide_data(station)
                
                for record in tide_data:
                    record['station'] = station
                    all_tide_data.append(record)
                
                print(f"✅ Processed {len(tide_data)} records for {station}")
                
            except Exception as e:
                print(f"❌ Error processing tide data for {station}: {e}")
                continue
        
        if all_tide_data:
            # Create DataFrame
            tide_df = pd.DataFrame(all_tide_data)
            
            # Convert datetime string to separate date and time columns
            tide_df['datetime'] = pd.to_datetime(tide_df['datetime'])
            tide_df['date'] = tide_df['datetime'].dt.strftime('%Y-%m-%d')
            tide_df['time'] = tide_df['datetime'].dt.strftime('%H:%M:%S')
            tide_df['year'] = tide_df['datetime'].dt.year
            tide_df['month'] = tide_df['datetime'].dt.month
            tide_df['day'] = tide_df['datetime'].dt.day
            tide_df['hour'] = tide_df['datetime'].dt.hour
            tide_df['minute'] = tide_df['datetime'].dt.minute
            
            # Drop original datetime column
            tide_df = tide_df.drop('datetime', axis=1)
            
            # Save to CSV for MindsDB
            tide_csv_path = "tide_data_for_mindsdb.csv"
            tide_df.to_csv(tide_csv_path, index=False)
            
            # Upload to MindsDB
            try:
                self.connection.upload_file(
                    tide_csv_path,
                    'tide_data',
                    'tide_predictions'
                )
                print(f"✅ Uploaded {len(tide_df)} tide prediction records to MindsDB")
            except Exception as e:
                print(f"❌ Failed to upload tide data: {e}")
            
            # Clean up
            if os.path.exists(tide_csv_path):
                os.remove(tide_csv_path)
    
    def load_processed_satellite_data(self, station_ids=None):
        """
        Load processed satellite data for specific stations
        
        Args:
            station_ids: List of station IDs to process
        """
        if not self.connection:
            print("❌ MindsDB connection not available")
            return
        
        print("📈 Loading processed satellite data into MindsDB...")
        
        # Default station IDs if none provided
        if station_ids is None:
            station_ids = [1, 2, 3, 4, 5]  # Sample station IDs
        
        all_processed_data = []
        
        for station_id in station_ids:
            try:
                print(f"Processing station {station_id}...")
                
                # Read processed satellite data
                processed_data = read_satellite_data_station(station_id, from_file=True)
                
                if processed_data is not None and not processed_data.empty:
                    # Add station information
                    processed_data['station_id'] = station_id
                    processed_data['data_source'] = 'processed_satellite'
                    
                    # Convert date column
                    processed_data['date'] = pd.to_datetime(processed_data['date'])
                    processed_data['year'] = processed_data['date'].dt.year
                    processed_data['month'] = processed_data['date'].dt.month
                    processed_data['day'] = processed_data['date'].dt.day
                    
                    # Convert date back to string for CSV
                    processed_data['date'] = processed_data['date'].dt.strftime('%Y-%m-%d')
                    
                    all_processed_data.append(processed_data)
                    print(f"✅ Processed {len(processed_data)} records for station {station_id}")
                
            except Exception as e:
                print(f"❌ Error processing station {station_id}: {e}")
                continue
        
        if all_processed_data:
            # Combine all processed data
            combined_df = pd.concat(all_processed_data, ignore_index=True)
            
            # Save to CSV for MindsDB
            processed_csv_path = "processed_satellite_data_for_mindsdb.csv"
            combined_df.to_csv(processed_csv_path, index=False)
            
            # Upload to MindsDB
            try:
                self.connection.upload_file(
                    processed_csv_path,
                    'processed_satellite_data',
                    'processed_satellite'
                )
                print(f"✅ Uploaded {len(combined_df)} processed satellite records to MindsDB")
            except Exception as e:
                print(f"❌ Failed to upload processed satellite data: {e}")
            
            # Clean up
            if os.path.exists(processed_csv_path):
                os.remove(processed_csv_path)
    
    def create_ai_models(self):
        """Create AI models for different predictions"""
        if not self.connection:
            print("❌ MindsDB connection not available")
            return
        
        print("🤖 Creating AI models for predictions...")
        
        # Model 1: Sea Level Prediction
        try:
            sea_level_model = Predictor(
                name='sea_level_predictor',
                predict='sea_level_anomaly',
                select_data_query="""
                    SELECT 
                        timestamp, date, year, month, day,
                        latitude, longitude, sea_level_anomaly
                    FROM satellite_sea_level
                    WHERE sea_level_anomaly IS NOT NULL
                """,
                training_options={
                    'timeseries_settings': {
                        'is_timeseries': True,
                        'order_by': 'timestamp',
                        'window': 12  # 12 months window
                    }
                }
            )
            print("✅ Created sea level prediction model")
        except Exception as e:
            print(f"❌ Failed to create sea level model: {e}")
        
        # Model 2: Tide Prediction
        try:
            tide_model = Predictor(
                name='tide_predictor',
                predict='prediction',
                select_data_query="""
                    SELECT 
                        date, time, year, month, day, hour, minute,
                        station, prediction, type
                    FROM tide_predictions
                    WHERE prediction IS NOT NULL
                """,
                training_options={
                    'timeseries_settings': {
                        'is_timeseries': True,
                        'order_by': 'date',
                        'window': 24  # 24 hours window
                    }
                }
            )
            print("✅ Created tide prediction model")
        except Exception as e:
            print(f"❌ Failed to create tide model: {e}")
        
        # Model 3: Combined Coastal Analysis
        try:
            coastal_model = Predictor(
                name='coastal_analysis_predictor',
                predict='sea_level_anomaly',
                select_data_query="""
                    SELECT 
                        s.timestamp, s.date, s.year, s.month, s.day,
                        s.latitude, s.longitude, s.sea_level_anomaly,
                        t.prediction as tide_prediction, t.station
                    FROM satellite_sea_level s
                    LEFT JOIN tide_predictions t 
                    ON s.date = t.date AND s.latitude BETWEEN 40.5 AND 40.8
                    WHERE s.sea_level_anomaly IS NOT NULL
                """,
                training_options={
                    'timeseries_settings': {
                        'is_timeseries': True,
                        'order_by': 'timestamp',
                        'window': 12
                    }
                }
            )
            print("✅ Created combined coastal analysis model")
        except Exception as e:
            print(f"❌ Failed to create coastal analysis model: {e}")
    
    def run_predictions(self):
        """Run predictions using the trained models"""
        if not self.connection:
            print("❌ MindsDB connection not available")
            return
        
        print("🔮 Running predictions...")
        
        # Example predictions
        try:
            # Sea level prediction for next month
            sea_level_prediction = self.connection.query("""
                SELECT * FROM mindsdb.sea_level_predictor 
                WHERE timestamp > '2024-01-01'
                LIMIT 10
            """)
            print("✅ Sea level predictions generated")
            
            # Tide prediction for next week
            tide_prediction = self.connection.query("""
                SELECT * FROM mindsdb.tide_predictor 
                WHERE date > '2024-01-01'
                LIMIT 10
            """)
            print("✅ Tide predictions generated")
            
        except Exception as e:
            print(f"❌ Error running predictions: {e}")
    
    def generate_insights(self):
        """Generate insights from the data"""
        if not self.connection:
            print("❌ MindsDB connection not available")
            return
        
        print("💡 Generating insights...")
        
        insights = []
        
        try:
            # Analyze sea level trends
            sea_level_trends = self.connection.query("""
                SELECT 
                    year, month,
                    AVG(sea_level_anomaly) as avg_sea_level,
                    COUNT(*) as data_points
                FROM satellite_sea_level
                WHERE sea_level_anomaly IS NOT NULL
                GROUP BY year, month
                ORDER BY year, month
            """)
            
            if sea_level_trends:
                insights.append("📊 Sea level trend analysis completed")
            
            # Analyze tide patterns
            tide_patterns = self.connection.query("""
                SELECT 
                    station, type, 
                    AVG(prediction) as avg_prediction,
                    COUNT(*) as data_points
                FROM tide_predictions
                WHERE prediction IS NOT NULL
                GROUP BY station, type
            """)
            
            if tide_patterns:
                insights.append("🌊 Tide pattern analysis completed")
            
            # Seasonal analysis
            seasonal_analysis = self.connection.query("""
                SELECT 
                    month,
                    AVG(sea_level_anomaly) as avg_sea_level,
                    AVG(prediction) as avg_tide
                FROM satellite_sea_level s
                LEFT JOIN tide_predictions t ON s.date = t.date
                WHERE s.sea_level_anomaly IS NOT NULL
                GROUP BY month
                ORDER BY month
            """)
            
            if seasonal_analysis:
                insights.append("🌍 Seasonal analysis completed")
            
            print("✅ Generated insights:")
            for insight in insights:
                print(f"   {insight}")
                
        except Exception as e:
            print(f"❌ Error generating insights: {e}")
    
    def export_results(self, output_dir="mindsdb_results"):
        """Export results and insights to files"""
        if not self.connection:
            print("❌ MindsDB connection not available")
            return
        
        print(f"📁 Exporting results to {output_dir}...")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Export sea level predictions
            sea_level_results = self.connection.query("""
                SELECT * FROM mindsdb.sea_level_predictor 
                WHERE timestamp > '2024-01-01'
            """)
            
            if sea_level_results:
                sea_level_df = pd.DataFrame(sea_level_results)
                sea_level_df.to_csv(f"{output_dir}/sea_level_predictions.csv", index=False)
                print("✅ Exported sea level predictions")
            
            # Export tide predictions
            tide_results = self.connection.query("""
                SELECT * FROM mindsdb.tide_predictor 
                WHERE date > '2024-01-01'
            """)
            
            if tide_results:
                tide_df = pd.DataFrame(tide_results)
                tide_df.to_csv(f"{output_dir}/tide_predictions.csv", index=False)
                print("✅ Exported tide predictions")
            
            # Export insights summary
            insights_summary = {
                "timestamp": datetime.now().isoformat(),
                "datasets_loaded": [
                    "satellite_sea_level",
                    "tide_predictions", 
                    "processed_satellite"
                ],
                "models_created": [
                    "sea_level_predictor",
                    "tide_predictor",
                    "coastal_analysis_predictor"
                ],
                "total_records_processed": len(sea_level_results) + len(tide_results) if sea_level_results and tide_results else 0
            }
            
            with open(f"{output_dir}/insights_summary.json", 'w') as f:
                json.dump(insights_summary, f, indent=2)
            
            print("✅ Exported insights summary")
            
        except Exception as e:
            print(f"❌ Error exporting results: {e}")
    
    def run_full_pipeline(self):
        """Run the complete MindsDB integration pipeline"""
        print("🚀 Starting MindsDB Integration Pipeline")
        print("=" * 50)
        
        # Step 1: Load all datasets
        print("\n📊 Step 1: Loading datasets...")
        self.load_satellite_data(limit_files=5)  # Limit for demo
        self.load_tide_data()
        self.load_processed_satellite_data()
        
        # Step 2: Create AI models
        print("\n🤖 Step 2: Creating AI models...")
        self.create_ai_models()
        
        # Step 3: Run predictions
        print("\n🔮 Step 3: Running predictions...")
        self.run_predictions()
        
        # Step 4: Generate insights
        print("\n💡 Step 4: Generating insights...")
        self.generate_insights()
        
        # Step 5: Export results
        print("\n📁 Step 5: Exporting results...")
        self.export_results()
        
        print("\n✅ MindsDB Integration Pipeline Complete!")
        print("=" * 50)

def install_mindsdb():
    """Install MindsDB if not available"""
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mindsdb"])
        print("✅ MindsDB installed successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to install MindsDB: {e}")
        return False

def main():
    """Main function to run the MindsDB integration"""
    print("🌊 Coastal Data MindsDB Integration")
    print("=" * 40)
    
    # Check if MindsDB is available
    global MINDSDB_AVAILABLE
    if not MINDSDB_AVAILABLE:
        print("Installing MindsDB...")
        if install_mindsdb():
            MINDSDB_AVAILABLE = True
            # Re-import after installation
            import mindsdb
            from mindsdb import Predictor
        else:
            print("❌ Could not install MindsDB. Please install manually:")
            print("pip install mindsdb")
            return
    
    # Initialize MindsDB integration
    coastal_mindsdb = CoastalDataMindsDB()
    
    # Run the full pipeline
    coastal_mindsdb.run_full_pipeline()

if __name__ == "__main__":
    main()
