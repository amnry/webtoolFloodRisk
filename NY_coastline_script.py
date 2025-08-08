import sys
import ee
import os

# Check if credentials exist and use persistent authentication
credentials_path = os.path.expanduser('~/.config/earthengine/credentials')
if os.path.exists(credentials_path):
    # Use existing credentials - no need to authenticate again
    ee.Initialize(project='ee-amanarya1910')
else:
    # Only authenticate if credentials don't exist
    ee.Authenticate(scopes=['https://www.googleapis.com/auth/earthengine', 
                            'https://www.googleapis.com/auth/devstorage.full_control',
                            'https://www.googleapis.com/auth/cloud-platform'])
    ee.Initialize(project='ee-amanarya1910')
import folium

def generate_map(flood_level=2.0):
    """Generate map with specified flood level and return HTML as string"""
    # Load the NY_coastline asset (elevation image)
    ny_coastline = ee.Image('projects/ee-amanarya1910/assets/NY_coastline')

    # Use MODIS land-water mask (0 = water, 1 = land)
    # modis_land_mask = ee.Image('MODIS/006/MOD44W/2015_01_01').select('water_mask').eq(0)

    # Create flood mask: areas ≤ flood_level AND on land
    # flooded_land = ny_coastline.lte(flood_level).And(modis_land_mask).selfMask()
    
    # Create flood mask: areas ≤ flood_level (without land sea filter)
    flooded_land = ny_coastline.lte(flood_level).selfMask()

    # Visualization parameters
    flood_vis_params = {
        'palette': ['blue'],
        'opacity': 0.6
    }

    # Define add_ee_layer if not already defined
    if not hasattr(folium.Map, 'add_ee_layer'):
        def add_ee_layer(self, ee_image_object, vis_params, name):
            map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name=name,
                overlay=True,
                control=True
            ).add_to(self)
        folium.Map.add_ee_layer = add_ee_layer

    # Create a folium map centered on New York with Google Satellite as default
    map_center = [40.7128, -73.5060] # [41.7128, -73.5060]  # NYC coordinates (Manhattan)
    coast_map = folium.Map(
        location=map_center, 
        zoom_start=10.5,
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite'
    )

    # Add OpenStreetMap as an alternative base layer
    folium.TileLayer(
        tiles='https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        name='OpenStreetMap',
        attr='OpenStreetMap',
        overlay=False,
        control=True
    ).add_to(coast_map)

    # Add flood mask layer with dynamic label
    layer_label = f'Flooded Land'
    coast_map.add_ee_layer(flooded_land, flood_vis_params, layer_label)

    # Add layer control
    coast_map.add_child(folium.LayerControl())

    # Return the map HTML as string
    return coast_map._repr_html_()

# Get flood level from command-line argument, default to 2.0
if __name__ == "__main__":
    try:
        flood_level = float(sys.argv[1])
    except (IndexError, ValueError):
        flood_level = 2.0
    
    # Generate and save the map
    map_html = generate_map(flood_level)
    with open("NY_coastline_script.html", "w") as f:
        f.write(map_html)
