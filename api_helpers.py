import ee
import folium
import json

def generate_map_data(level):
    """Extract map data as JSON instead of HTML"""
    # Load the NY_coastline asset
    ny_coastline = ee.Image('projects/ee-amanarya1910/assets/NY_coastline')
    modis_land_mask = ee.Image('MODIS/006/MOD44W/2015_01_01').select('water_mask').eq(0)
    
    # Create flood mask
    flooded_land = ny_coastline.lte(level).And(modis_land_mask).selfMask()
    
    # Get map bounds and center
    map_center = [40.7128, -73.5060]
    
    return {
        'center': map_center,
        'zoom': 10.5,
        'flood_level': level,
        'layers': {
            'flood_mask': {
                'type': 'ee_layer',
                'image_id': 'projects/ee-amanarya1910/assets/NY_coastline',
                'vis_params': {
                    'palette': ['blue'],
                    'opacity': 0.6
                }
            }
        }
    }

def get_map_tile_url(level):
    """Get Earth Engine tile URL for flood data"""
    try:
        # Load the NY_coastline asset
        ny_coastline = ee.Image('projects/ee-amanarya1910/assets/NY_coastline')
        modis_land_mask = ee.Image('MODIS/006/MOD44W/2015_01_01').select('water_mask').eq(0)
        
        # Create flood mask
        flooded_land = ny_coastline.lte(level).And(modis_land_mask).selfMask()
        
        # Get tile URL from Earth Engine
        map_id = flooded_land.getMapId({
            'palette': ['blue'],
            'opacity': 0.6
        })
        
        return f"https://earthengine.googleapis.com/map/{{z}}/{{x}}/{{y}}?token={map_id['token']}"
    except Exception as e:
        print(f"Error getting tile URL: {str(e)}")
        return None

def calculate_flood_statistics(level):
    """Calculate flood statistics for given level"""
    try:
        # Load the NY_coastline asset
        ny_coastline = ee.Image('projects/ee-amanarya1910/assets/NY_coastline')
        modis_land_mask = ee.Image('MODIS/006/MOD44W/2015_01_01').select('water_mask').eq(0)
        
        # Create flood mask
        flooded_land = ny_coastline.lte(level).And(modis_land_mask).selfMask()
        
        # Calculate statistics (this is a simplified version)
        # In a real implementation, you would calculate actual area, population, etc.
        
        return {
            'affected_area_km2': level * 100,  # Placeholder calculation
            'population_at_risk': level * 50000,  # Placeholder calculation
            'infrastructure_affected': level * 25,  # Placeholder calculation
            'flood_level': level
        }
    except Exception as e:
        print(f"Error calculating statistics: {str(e)}")
        return {
            'affected_area_km2': 0,
            'population_at_risk': 0,
            'infrastructure_affected': 0,
            'flood_level': level
        } 