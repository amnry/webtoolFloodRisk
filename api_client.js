// API Client for communicating with the REST API
class APIClient {
    constructor(baseURL = 'http://127.0.0.1:5001') {
        this.baseURL = baseURL;
    }
    
    async getFloodData(level) {
        try {
            const response = await fetch(`${this.baseURL}/api/flood-level/${level}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching flood data:', error);
            throw error;
        }
    }
    
    async getMapHTML(level) {
        try {
            const response = await fetch(`${this.baseURL}/api/map/${level}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching map HTML:', error);
            throw error;
        }
    }
    
    async getStatistics(level) {
        try {
            const response = await fetch(`${this.baseURL}/api/statistics/${level}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching statistics:', error);
            throw error;
        }
    }
    
    async getTileUrl(level) {
        try {
            const response = await fetch(`${this.baseURL}/api/tile-url/${level}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching tile URL:', error);
            throw error;
        }
    }
} 