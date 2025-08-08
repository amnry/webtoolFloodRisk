#!/usr/bin/env python3
"""
Test script for tide chatbot functionality
Demonstrates how to query the chatbot for tide information
"""

import requests
import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_tide_queries():
    """Test various tide queries with the chatbot"""
    
    # Base URL for the Flask app
    base_url = "http://localhost:5001"
    
    # Test queries
    test_queries = [
        "What is the highest tide in January at NYC?",
        "What is the lowest tide at Miami?",
        "What is the highest tide in March at Boston?",
        "Tell me about tides at Seattle",
        "What is the average tide at Port Jefferson?",
        "What is the highest tide at San Francisco in December?",
        "What is the lowest tide in July at Galveston?"
    ]
    
    print("🌊 Testing Tide Chatbot Queries")
    print("=" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 50)
        
        try:
            # Make POST request to chat endpoint
            response = requests.post(
                f"{base_url}/chat",
                json={"message": query},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data:
                    print(f"✅ Response: {data['response']}")
                else:
                    print(f"❌ No response in data: {data}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to Flask app. Make sure it's running on port 5001")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_mindsdb_connection():
    """Test MindsDB connection directly"""
    print("\n🔗 Testing MindsDB Connection")
    print("=" * 30)
    
    try:
        from mindsdb_integration import CoastalDataMindsDB
        
        coastal_mindsdb = CoastalDataMindsDB()
        
        if coastal_mindsdb.connection:
            print("✅ MindsDB connection successful")
            
            # Test a simple query
            try:
                result = coastal_mindsdb.connection.query("SELECT COUNT(*) as count FROM tide_predictions")
                if result:
                    print(f"✅ Tide data available: {result[0]['count']} records")
                else:
                    print("⚠️ No tide data found in MindsDB")
            except Exception as e:
                print(f"❌ Query error: {str(e)}")
        else:
            print("❌ MindsDB connection failed")
            
    except ImportError:
        print("❌ Mindsdb_integration module not found")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 Tide Chatbot Test Suite")
    print("=" * 40)
    
    # Test MindsDB connection first
    test_mindsdb_connection()
    
    # Test chatbot queries
    test_tide_queries()
    
    print("\n📚 Usage Examples:")
    print("1. Start the Flask app: python app.py")
    print("2. Open http://localhost:5001 in your browser")
    print("3. Click the chat bubble (💬) in the bottom right")
    print("4. Ask questions like:")
    print("   - 'What is the highest tide in January at NYC?'")
    print("   - 'What is the lowest tide at Miami?'")
    print("   - 'Tell me about tides at Seattle'")

if __name__ == "__main__":
    main()
