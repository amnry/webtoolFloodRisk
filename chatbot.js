// Chatbot functionality for flood risk dataset
class DatasetChatbot {
    constructor() {
        this.chatBtn = document.getElementById('chatBtn');
        this.chatWindow = document.getElementById('chatWindow');
        this.chatClose = document.getElementById('chatClose');
        this.chatInput = document.getElementById('chatInput');
        this.chatSend = document.getElementById('chatSend');
        this.chatMessages = document.getElementById('chatMessages');
        
        this.isOpen = false;
        this.messageHistory = [];
        
        this.initializeEventListeners();
    }
    
    initializeEventListeners() {
        // Toggle chat window
        this.chatBtn.addEventListener('click', () => this.toggleChat());
        
        // Close chat window
        this.chatClose.addEventListener('click', () => this.closeChat());
        
        // Send message on button click
        this.chatSend.addEventListener('click', () => this.sendMessage());
        
        // Send message on Enter key
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Close chat when clicking outside (optional)
        document.addEventListener('click', (e) => {
            if (this.isOpen && 
                !this.chatWindow.contains(e.target) && 
                !this.chatBtn.contains(e.target)) {
                this.closeChat();
            }
        });
    }
    
    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }
    
    openChat() {
        this.chatWindow.style.display = 'flex';
        this.chatInput.focus();
        this.isOpen = true;
        
        // Add welcome message if this is the first time opening
        if (this.messageHistory.length === 0) {
            this.addBotMessage("Hello! I'm here to help you learn more about Flood Risk modeling using CoastalDEM dataset. What would you like to know?");
        }
    }
    
    closeChat() {
        this.chatWindow.style.display = 'none';
        this.isOpen = false;
    }
    
    sendMessage() {
        const message = this.chatInput.value.trim();
        if (message) {
            this.addUserMessage(message);
            this.chatInput.value = '';
            
            // Process the message and generate response
            this.processMessage(message);
        }
    }
    
    addUserMessage(text) {
        this.addMessage(text, 'user');
        this.messageHistory.push({ type: 'user', text: text, timestamp: new Date() });
    }
    
    addBotMessage(text) {
        this.addMessage(text, 'bot');
        this.messageHistory.push({ type: 'bot', text: text, timestamp: new Date() });
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    processMessage(message) {
        const lowerMessage = message.toLowerCase();
        
        // Simulate processing delay
        setTimeout(() => {
            const response = this.generateResponse(lowerMessage);
            this.addBotMessage(response);
        }, 1000);
    }
    
    generateResponse(message) {
        // Simple keyword-based responses (can be expanded with more sophisticated NLP)
        if (message.includes('hello') || message.includes('hi') || message.includes('hey')) {
            return "Hello! How can I help you understand the flood risk dataset today?";
        }
        
        if (message.includes('dataset') || message.includes('data')) {
            return "This dataset contains flood risk analysis for coastal areas, including elevation data, flood frequency, and risk assessments. What specific aspect would you like to know more about?";
        }
        
        if (message.includes('flood') || message.includes('risk')) {
            return "The flood risk analysis is based on multiple factors including elevation data, historical flood events, and climate projections. The slider on the left allows you to visualize different flood levels from 0 to 3 meters.";
        }
        
        if (message.includes('method') || message.includes('how') || message.includes('calculate')) {
            return "The flood risk assessment uses digital elevation models (DEM), historical flood data, and statistical modeling to predict flood probabilities at different water levels. The methodology incorporates both physical and statistical approaches.";
        }
        
        if (message.includes('elevation') || message.includes('dem')) {
            return "The elevation data comes from high-resolution digital elevation models that provide detailed topographic information. This data is crucial for determining which areas would be affected at different flood levels.";
        }
        
        if (message.includes('coastal') || message.includes('coast')) {
            return "This dataset focuses on coastal flood risk, which is particularly important due to sea level rise and storm surge events. Coastal areas are vulnerable to both gradual sea level rise and extreme weather events.";
        }
        
        if (message.includes('help') || message.includes('what can you do')) {
            return "I can help you understand the flood risk dataset, explain the methodology, discuss coastal flood risks, and answer questions about the data sources and analysis techniques. Just ask me anything!";
        }
        
        if (message.includes('thank')) {
            return "You're welcome! Feel free to ask more questions about the dataset or flood risk analysis.";
        }
        
        // Default response for unrecognized queries
        return "That's an interesting question! While I'm currently providing basic information about the flood risk dataset, I can help you understand the data sources, methodology, and key findings. Could you try asking about the dataset, flood risk, methodology, or coastal analysis?";
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the chatbot
    window.datasetChatbot = new DatasetChatbot();
}); 