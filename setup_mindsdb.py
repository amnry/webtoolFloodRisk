#!/usr/bin/env python3
"""
Setup script for MindsDB Integration
Helps install and configure MindsDB for coastal data analysis.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_virtual_environment():
    """Check if running in virtual environment"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
        return True
    else:
        print("⚠️  Not running in virtual environment")
        print("   Consider using: source ams585venv/bin/activate")
        return False

def install_package(package_name, upgrade=False):
    """Install a Python package"""
    try:
        cmd = [sys.executable, "-m", "pip", "install"]
        if upgrade:
            cmd.append("--upgrade")
        cmd.append(package_name)
        
        print(f"📦 Installing {package_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully installed {package_name}")
            return True
        else:
            print(f"❌ Failed to install {package_name}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing {package_name}: {e}")
        return False

def install_mindsdb():
    """Install MindsDB"""
    print("\n🤖 Installing MindsDB...")
    
    # Install MindsDB
    if not install_package("mindsdb"):
        return False
    
    # Install additional dependencies
    dependencies = [
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "xarray>=2022.12.0",
        "netCDF4>=1.6.0",
        "tqdm>=4.64.0",
        "scikit-learn>=1.1.0"
    ]
    
    for dep in dependencies:
        if not install_package(dep):
            print(f"⚠️  Warning: Failed to install {dep}")
    
    return True

def check_mindsdb_installation():
    """Check if MindsDB is properly installed"""
    try:
        import mindsdb
        print("✅ MindsDB is installed and importable")
        return True
    except ImportError as e:
        print(f"❌ MindsDB import failed: {e}")
        return False

def start_mindsdb_server():
    """Start MindsDB server"""
    print("\n🚀 Starting MindsDB server...")
    
    try:
        # Check if MindsDB server is already running
        import requests
        try:
            response = requests.get("http://localhost:47334/api/v1/status", timeout=5)
            if response.status_code == 200:
                print("✅ MindsDB server is already running")
                return True
        except:
            pass
        
        # Start MindsDB server
        print("Starting MindsDB server in background...")
        subprocess.Popen([sys.executable, "-m", "mindsdb", "start"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait a moment for server to start
        import time
        time.sleep(5)
        
        # Check if server started successfully
        try:
            response = requests.get("http://localhost:47334/api/v1/status", timeout=10)
            if response.status_code == 200:
                print("✅ MindsDB server started successfully")
                return True
            else:
                print("❌ MindsDB server failed to start")
                return False
        except:
            print("❌ Could not connect to MindsDB server")
            return False
            
    except Exception as e:
        print(f"❌ Error starting MindsDB server: {e}")
        return False

def check_data_files():
    """Check if required data files exist"""
    print("\n📁 Checking data files...")
    
    data_files = {
        "Tide Data": [
            "HighTide/portJeff.txt",
            "HighTide/miami.txt", 
            "HighTide/nycBatteryPark.txt"
        ],
        "Satellite Data": [
            "jiayou_sat_data/monthly_raw/"
        ],
        "Processing Scripts": [
            "tide_data_parser.py",
            "jiayou_sat_data/sa_data.py"
        ]
    }
    
    all_files_exist = True
    
    for category, files in data_files.items():
        print(f"\n{category}:")
        for file_path in files:
            if os.path.exists(file_path):
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} (missing)")
                all_files_exist = False
    
    return all_files_exist

def create_test_script():
    """Create a simple test script"""
    test_script = """#!/usr/bin/env python3
\"\"\"
Simple test script for MindsDB integration
\"\"\"

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from mindsdb_integration import CoastalDataMindsDB
    
    print("🌊 Testing MindsDB Integration...")
    
    # Initialize
    coastal_mindsdb = CoastalDataMindsDB()
    
    if coastal_mindsdb.connection:
        print("✅ MindsDB connection successful")
        
        # Test tide data loading
        print("📊 Testing tide data loading...")
        coastal_mindsdb.load_tide_data()
        
        print("✅ All tests passed!")
    else:
        print("❌ MindsDB connection failed")
        
except Exception as e:
    print(f"❌ Test failed: {e}")
"""
    
    with open("test_mindsdb.py", "w") as f:
        f.write(test_script)
    
    print("✅ Created test_mindsdb.py")

def main():
    """Main setup function"""
    print("🔧 MindsDB Integration Setup")
    print("=" * 40)
    
    # Step 1: Check Python version
    print("\n📋 Step 1: Checking Python version...")
    if not check_python_version():
        return False
    
    # Step 2: Check virtual environment
    print("\n📋 Step 2: Checking virtual environment...")
    check_virtual_environment()
    
    # Step 3: Install MindsDB
    print("\n📋 Step 3: Installing MindsDB...")
    if not install_mindsdb():
        print("❌ Failed to install MindsDB")
        return False
    
    # Step 4: Verify installation
    print("\n📋 Step 4: Verifying installation...")
    if not check_mindsdb_installation():
        print("❌ MindsDB installation verification failed")
        return False
    
    # Step 5: Start MindsDB server
    print("\n📋 Step 5: Starting MindsDB server...")
    if not start_mindsdb_server():
        print("❌ Failed to start MindsDB server")
        print("You may need to start it manually: mindsdb start")
    
    # Step 6: Check data files
    print("\n📋 Step 6: Checking data files...")
    data_files_ok = check_data_files()
    
    # Step 7: Create test script
    print("\n📋 Step 7: Creating test script...")
    create_test_script()
    
    # Summary
    print("\n" + "=" * 40)
    print("🎉 Setup Complete!")
    print("=" * 40)
    
    print("\n📚 Next Steps:")
    print("1. Test the installation:")
    print("   python test_mindsdb.py")
    print("\n2. Run the demo:")
    print("   python demo_mindsdb.py")
    print("\n3. Run the full integration:")
    print("   python mindsdb_integration.py")
    print("\n4. Read the documentation:")
    print("   MINDSDB_INTEGRATION_README.md")
    
    if not data_files_ok:
        print("\n⚠️  Warning: Some data files are missing.")
        print("   The integration may not work properly without all data files.")
    
    print("\n🚀 Happy analyzing!")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
