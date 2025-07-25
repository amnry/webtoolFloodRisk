from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import sys
import openai
import json
from datetime import datetime

# Import the generate_map function from the script
sys.path.append('.')
from NY_coastline_script import generate_map
from tide_data_parser import generate_24_hour_tide_data, get_tide_statistics, generate_date_range_tide_data, get_date_range_statistics

app = Flask(__name__, static_folder='.', template_folder='.')

# Initialize OpenAI client (API key will be set via environment variable)
openai_client = None

@app.route('/')
def index():
    # Get flood level from query parameter, default to 2.0
    level = request.args.get('level', default=2.0, type=float)
    
    # Generate the map HTML
    map_html = generate_map(level)
    
    # Render the template with the map and slider
    return render_template('templates.html', map_html=map_html, flood_level=level)

@app.route('/tide-predictions')
def tide_predictions():
    return render_template('tide_predictions.html')

@app.route('/api/port-jefferson-tides')
def port_jefferson_tides():
    """API endpoint to get Port Jefferson tide data"""
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    single_date = request.args.get('date')
    
    try:
        if from_date and to_date:
            # Date range request
            tide_data = generate_date_range_tide_data(from_date, to_date, 'portjefferson')
            statistics = get_date_range_statistics(from_date, to_date, 'portjefferson')
            
            if tide_data and statistics:
                return jsonify({
                    'success': True,
                    'from_date': from_date,
                    'to_date': to_date,
                    'tide_data': tide_data,
                    'statistics': statistics
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'No tide data available for the specified date range'
                })
        elif single_date:
            # Single date request (backward compatibility)
            tide_data = generate_24_hour_tide_data(single_date, 'portjefferson')
            statistics = get_tide_statistics(single_date, 'portjefferson')
            
            if tide_data and statistics:
                return jsonify({
                    'success': True,
                    'date': single_date,
                    'tide_data': tide_data,
                    'statistics': statistics
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'No tide data available for the specified date'
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Please provide either date or from_date and to_date parameters'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving tide data: {str(e)}'
        })

@app.route('/api/miami-tides')
def miami_tides():
    """API endpoint to get Miami tide data"""
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    single_date = request.args.get('date')
    
    try:
        if from_date and to_date:
            # Date range request
            tide_data = generate_date_range_tide_data(from_date, to_date, 'miami')
            statistics = get_date_range_statistics(from_date, to_date, 'miami')
            
            if tide_data and statistics:
                return jsonify({
                    'success': True,
                    'from_date': from_date,
                    'to_date': to_date,
                    'tide_data': tide_data,
                    'statistics': statistics
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'No tide data available for the specified date range'
                })
        elif single_date:
            # Single date request (backward compatibility)
            tide_data = generate_24_hour_tide_data(single_date, 'miami')
            statistics = get_tide_statistics(single_date, 'miami')
            
            if tide_data and statistics:
                return jsonify({
                    'success': True,
                    'date': single_date,
                    'tide_data': tide_data,
                    'statistics': statistics
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'No tide data available for the specified date'
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Please provide either date or from_date and to_date parameters'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving tide data: {str(e)}'
        })

@app.route('/api/nyc-tides')
def nyc_tides():
    """API endpoint to get NYC Battery Park tide data"""
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    single_date = request.args.get('date')
    
    try:
        if from_date and to_date:
            # Date range request
            tide_data = generate_date_range_tide_data(from_date, to_date, 'nyc')
            statistics = get_date_range_statistics(from_date, to_date, 'nyc')
            
            if tide_data and statistics:
                return jsonify({
                    'success': True,
                    'from_date': from_date,
                    'to_date': to_date,
                    'tide_data': tide_data,
                    'statistics': statistics
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'No tide data available for the specified date range'
                })
        elif single_date:
            # Single date request (backward compatibility)
            tide_data = generate_24_hour_tide_data(single_date, 'nyc')
            statistics = get_tide_statistics(single_date, 'nyc')
            
            if tide_data and statistics:
                return jsonify({
                    'success': True,
                    'date': single_date,
                    'tide_data': tide_data,
                    'statistics': statistics
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'No tide data available for the specified date'
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Please provide either date or from_date and to_date parameters'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving tide data: {str(e)}'
        })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Initialize OpenAI client if not already done
        global openai_client
        if openai_client is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                return jsonify({'error': 'OpenAI API key not configured'}), 500
            openai_client = openai.OpenAI(api_key=api_key)
        
        # Create system message for context
        system_message = """You are a comprehensive AI assistant for the CoastalDEM v3.0 Web Application. You have complete knowledge of the codebase and can answer questions about all features, implementation, and usage. Provide SHORT, CONCISE answers (1-2 sentences maximum).

        APPLICATION OVERVIEW:
        - Name: CoastalDEM v3.0 Web Application with Specialized GPT-4 Chat & Tide Predictions
        - Purpose: Interactive flood risk visualization with AI chat assistant and tide predictions
        - URL: http://localhost:5000 (when running locally)

        COASTALDEM V3.0 DATASET INFORMATION:
        - Dataset: CoastalDEM v3.0
        - Purpose: High-accuracy digital elevation model (DEM) for coastal areas, designed to improve flood risk assessment and sea level rise modeling
        - Coverage: Global coastal areas (within 10km of coastlines)
        - Horizontal Resolution: ~90 meters (3 arc-seconds)
        - Vertical Accuracy: ±2-4 meters (RMSE) globally, ±1-2 meters in well-surveyed areas
        - Coordinate Reference System: WGS84 (EPSG:4326)
        - Data Format: GeoTIFF
        - Elevation Range: -10 to +100 meters above mean sea level
        - Processing Method: Machine learning-based error correction applied to SRTM and ASTER GDEM data
        - Validation: Verified against high-accuracy lidar and GPS measurements

        MAIN FEATURES:
        1. FLOOD RISK VISUALIZATION:
           - Interactive map with Google Satellite as default layer
           - Vertical slider (0-3m) for adjusting flood levels
           - Real-time flood overlay in blue
           - Layer controls to switch between satellite and street views
           - Removed land-sea filter for comprehensive analysis
           - Responsive design for all devices

        2. TIDE PREDICTIONS SYSTEM:
           - Available Stations: NYC (The Battery), Boston, Miami, Seattle, San Francisco, Galveston
           - Features: 24-hour tide predictions, interactive charts, high/low tide times
           - Data: Simulated tide data based on realistic tidal patterns
           - Chart Visualization: Uses Chart.js for interactive tide height graphs
           - Date Selection: Users can choose any date for predictions
           - Key Metrics: High tide, low tide, tidal range, next high tide timing
           - Access: Via "Tide Predictions" button below the flood level slider

        3. AI CHAT ASSISTANT:
           - GPT-4 powered specialized assistant
           - Real-time chat interface with loading states
           - Knowledge of CoastalDEM, tide predictions, and application features
           - Located in bottom-right corner with chat bubble icon

        TECHNICAL IMPLEMENTATION:
        - Backend: Flask (Python) with OpenAI API integration
        - Frontend: HTML5/CSS3/JavaScript with Bootstrap 5
        - Maps: Google Earth Engine with Folium for interactive maps
        - Charts: Chart.js for tide visualizations
        - Icons: Font Awesome for UI elements
        - Authentication: Google Earth Engine authentication required
        - API: OpenAI GPT-4 for chat responses

        FILE STRUCTURE:
        - app.py: Main Flask application with routes and chat endpoint
        - NY_coastline_script.py: Map generation with Earth Engine integration
        - templates.html: Main application interface with slider and map
        - tide_predictions.html: Tide predictions page with station selection
        - chatbot.js: Chat interface JavaScript functionality
        - requirements.txt: Python dependencies
        - README_CHAT.md: Comprehensive documentation

        ROUTES:
        - /: Main flood risk visualization page
        - /tide-predictions: Tide predictions page
        - /chat: AI chat endpoint (POST)
        - /<filename>: Static file serving

        MAP FEATURES:
        - Default: Google Satellite imagery
        - Alternative: OpenStreetMap street view
        - Flood overlay: Blue semi-transparent layer
        - Layer controls: Toggle between base maps
        - Zoom: 10.5x centered on NYC coordinates [40.7128, -73.5060]

        TIDE PREDICTIONS FEATURES:
        - 6 major coastal stations
        - Interactive Chart.js visualizations
        - 24-hour tide cycle predictions
        - Date picker for historical/future data
        - Key metrics cards (high/low tide, range, timing)
        - Responsive grid layout
        - Gradient design with smooth animations

        CHAT FEATURES:
        - Real-time message handling
        - Loading animations during AI processing
        - Error handling for API failures
        - Message history within session
        - Character limit: 500 tokens per message
        - Response limit: 150 tokens for concise answers

        IMPORTANT: Keep all responses brief and to the point. Use 1-2 sentences maximum. Be direct and avoid lengthy explanations."""
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content
        
        return jsonify({'response': bot_response})
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Failed to get response from AI'}), 500

# Optional: Serve other static files if needed
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 