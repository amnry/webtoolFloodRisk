from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys
import logging

# Import the generate_map function from the script
sys.path.append('.')
from NY_coastline_script import generate_map
from api_helpers import generate_map_data, calculate_flood_statistics

app = Flask(__name__, static_folder='.', template_folder='.')
# Allow CORS for your frontend origin
CORS(app, origins=["http://127.0.0.1:5001", "http://localhost:5001"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Endpoints
@app.route('/api/flood-level/<float:level>')
def get_flood_data(level):
    """Return flood data as JSON"""
    try:
        # Generate map data
        map_data = generate_map_data(level)
        return jsonify({
            'status': 'success',
            'flood_level': level,
            'map_data': map_data,
            'statistics': calculate_flood_statistics(level)
        })
    except Exception as e:
        logger.error(f"Error in get_flood_data: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/map/<float:level>')
def get_map_html(level):
    """Return map HTML file URL as string"""
    try:
        map_html = generate_map(level)
        # Save the map HTML to a static file
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        map_filename = f'folium_map_{level}.html'
        map_filepath = os.path.join(static_dir, map_filename)
        with open(map_filepath, 'w', encoding='utf-8') as f:
            f.write(map_html)
        map_url = f'/static/{map_filename}'
        return jsonify({
            'status': 'success',
            'map_url': map_url,
            'flood_level': level
        })
    except Exception as e:
        logger.error(f"Error in get_map_html: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/statistics/<float:level>')
def get_statistics(level):
    """Return flood statistics"""
    try:
        stats = calculate_flood_statistics(level)
        return jsonify({
            'status': 'success',
            'flood_level': level,
            'statistics': stats
        })
    except Exception as e:
        logger.error(f"Error in get_statistics: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/tile-url/<float:level>')
def get_tile_url(level):
    """Return Earth Engine tile URL for flood data"""
    try:
        from api_helpers import get_map_tile_url
        tile_url = get_map_tile_url(level)
        return jsonify({
            'status': 'success',
            'flood_level': level,
            'tile_url': tile_url
        })
    except Exception as e:
        logger.error(f"Error in get_tile_url: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Serve static files (HTML, CSS, JS)
@app.route('/')
def index():
    return send_from_directory('.', 'templates.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# Helper functions are now imported from api_helpers.py

# Error handlers
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Error: {str(error)}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Resource not found'
    }), 404

if __name__ == '__main__':
    app.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5001)),
        debug=os.environ.get('DEBUG', True)
    ) 