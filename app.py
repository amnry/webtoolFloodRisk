from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import sys
import openai
import json

# Import the generate_map function from the script
sys.path.append('.')
from NY_coastline_script import generate_map

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
        system_message = """You are a specialized AI assistant for CoastalDEM v3.0 dataset questions. Provide SHORT, CONCISE answers (1-2 sentences maximum).

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
    app.run(debug=True) 