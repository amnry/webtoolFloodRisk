// Main Application Logic for Flood Viewer
class FloodViewerApp {
    constructor() {
        this.mapManager = new MapManager();
        this.apiClient = new APIClient();
        this.currentLevel = 2.0;
        this.initializeEventListeners();
    }
    
    async initialize() {
        // Get initial level from URL or default
        this.currentLevel = this.mapManager.getCurrentLevel();
        
        // Initialize map
        await this.mapManager.initializeMap(this.currentLevel);
        
        // Initialize chatbot
        if (typeof DatasetChatbot !== 'undefined') {
            window.datasetChatbot = new DatasetChatbot();
        }
        
        // Set initial slider value
        this.updateSliderValue(this.currentLevel);
        
        console.log('Flood Viewer App initialized with level:', this.currentLevel);
    }
    
    initializeEventListeners() {
        const slider = document.getElementById('floodSlider');
        const valueLabel = document.getElementById('floodValue');
        
        if (slider && valueLabel) {
            // Update display on slider input
            slider.addEventListener('input', (e) => {
                valueLabel.textContent = e.target.value;
            });
            
            // Update map on slider change
            slider.addEventListener('change', async (e) => {
                const newLevel = parseFloat(e.target.value);
                await this.updateFloodLevel(newLevel);
            });
        }
        
        // Handle URL parameters
        this.handleURLParameters();
    }
    
    async updateFloodLevel(level) {
        this.currentLevel = level;
        
        // Update URL without page reload
        this.mapManager.setLevel(level);
        
        // Update map using HTML injection method for identical rendering
        await this.mapManager.updateMapWithLevel(level);
        
        // Update statistics (if needed)
        await this.updateStatistics(level);
        
        console.log('Updated flood level to:', level);
    }
    
    async updateStatistics(level) {
        try {
            const stats = await this.apiClient.getStatistics(level);
            if (stats.status === 'success') {
                console.log('Updated statistics:', stats.statistics);
                // You can add UI elements to display statistics here
            }
        } catch (error) {
            console.error('Error updating statistics:', error);
        }
    }
    
    handleURLParameters() {
        const urlParams = new URLSearchParams(window.location.search);
        const levelParam = urlParams.get('level');
        
        if (levelParam) {
            const level = parseFloat(levelParam);
            this.currentLevel = level;
            this.updateSliderValue(level);
        }
    }
    
    updateSliderValue(level) {
        const slider = document.getElementById('floodSlider');
        const valueLabel = document.getElementById('floodValue');
        
        if (slider && valueLabel) {
            slider.value = level;
            valueLabel.textContent = level;
        }
    }
    
    // Method to check if the app is working correctly
    async testAPI() {
        try {
            const testResponse = await this.apiClient.getMapHTML(2.0);
            console.log('API test successful:', testResponse.status === 'success');
            return testResponse.status === 'success';
        } catch (error) {
            console.error('API test failed:', error);
            return false;
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    console.log('DOM loaded, initializing Flood Viewer App...');
    const app = new FloodViewerApp();
    await app.initialize();
    
    // Test API connection
    await app.testAPI();
}); 