// Map Manager for handling map operations
class MapManager {
    constructor() {
        this.apiClient = new APIClient();
    }
    
    async initializeMap(level = 2.0) {
        await this.loadMapHTML(level);
    }
    
    async loadMapHTML(level) {
        try {
            const response = await this.apiClient.getMapHTML(level);
            if (response.status === 'success') {
                // Use an iframe to render the Folium map HTML file
                let mapDiv = document.getElementById('map');
                // Remove any existing iframe
                let oldIframe = document.getElementById('folium-map-iframe');
                if (oldIframe) {
                    mapDiv.removeChild(oldIframe);
                }
                let iframe = document.createElement('iframe');
                iframe.id = 'folium-map-iframe';
                iframe.style.width = '100%';
                iframe.style.height = '100vh';
                iframe.style.border = 'none';
                iframe.src = response.map_url; // Use src instead of srcdoc
                mapDiv.appendChild(iframe);
            } else {
                console.error('Failed to load map HTML:', response.message);
            }
        } catch (error) {
            console.error('Error loading map HTML:', error);
        }
    }
    
    async updateMapWithLevel(level) {
        // Reload the map HTML for the new level
        await this.loadMapHTML(level);
    }
    
    getCurrentLevel() {
        // Get current level from URL or default
        const urlParams = new URLSearchParams(window.location.search);
        return parseFloat(urlParams.get('level') || '2.0');
    }
    
    setLevel(level) {
        // Update URL without page reload
        const url = new URL(window.location.href);
        url.searchParams.set('level', level);
        window.history.pushState({}, '', url);
    }
} 