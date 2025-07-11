// Chatbot functionality for flood risk dataset with GPT-4 integration
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
        this.isProcessing = false;
        
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
            if (e.key === 'Enter' && !this.isProcessing) {
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
            this.addBotMessage("Hello! I'm your AI assistant for the flood risk assessment application. I can help you understand the dataset, methodology, and coastal flood risks. What would you like to know?");
        }
    }
    
    closeChat() {
        this.chatWindow.style.display = 'none';
        this.isOpen = false;
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (message && !this.isProcessing) {
            this.addUserMessage(message);
            this.chatInput.value = '';
            
            // Process the message and generate response
            await this.processMessage(message);
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
    
    addLoadingMessage() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot loading';
        loadingDiv.innerHTML = '<span class="loading-dots">Thinking...</span>';
        this.chatMessages.appendChild(loadingDiv);
        this.scrollToBottom();
        return loadingDiv;
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    async processMessage(message) {
        this.isProcessing = true;
        this.chatSend.disabled = true;
        this.chatInput.disabled = true;
        
        // Add loading indicator
        const loadingElement = this.addLoadingMessage();
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Remove loading message
            loadingElement.remove();
            
            if (response.ok) {
                this.addBotMessage(data.response);
            } else {
                this.addBotMessage(`Sorry, I encountered an error: ${data.error || 'Unknown error'}. Please try again.`);
            }
        } catch (error) {
            // Remove loading message
            loadingElement.remove();
            this.addBotMessage("Sorry, I'm having trouble connecting right now. Please check your internet connection and try again.");
            console.error('Chat error:', error);
        } finally {
            this.isProcessing = false;
            this.chatSend.disabled = false;
            this.chatInput.disabled = false;
            this.chatInput.focus();
        }
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the chatbot
    window.datasetChatbot = new DatasetChatbot();
}); 