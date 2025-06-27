from flask import Flask, render_template, send_from_directory, request
import os
import sys

# Import the generate_map function from the script
sys.path.append('.')
from NY_coastline_script import generate_map

app = Flask(__name__, static_folder='.', template_folder='.')

@app.route('/')
def index():
    # Get flood level from query parameter, default to 2.0
    level = request.args.get('level', default=2.0, type=float)
    
    # Generate the map HTML
    map_html = generate_map(level)
    
    # Render the template with the map and slider
    return render_template('templates.html', map_html=map_html, flood_level=level)

# Optional: Serve other static files if needed
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True) 