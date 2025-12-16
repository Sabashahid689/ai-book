// Chat Widget JavaScript Implementation
class BookChatWidget {
  constructor(options = {}) {
    this.apiEndpoint = options.apiEndpoint || 'http://localhost:8000/api/v1/chat';
    this.title = options.title || 'Book Assistant';
    this.containerId = options.containerId || 'book-chat-widget';
    
    this.initializeWidget();
    this.attachEventListeners();
  }
  
  initializeWidget() {
    // Get DOM elements
    this.container = document.getElementById(this.containerId);
    this.toggleBtn = document.getElementById('chat-widget-toggle');
    this.chatBody = document.getElementById('chat-widget-body');
    this.messagesContainer = document.getElementById('chat-messages');
    this.inputField = document.getElementById('chat-input');
    this.sendBtn = document.getElementById('chat-send-btn');
    
    // Update title if provided
    const titleElement = this.container.querySelector('.chat-header-title');
    if (titleElement) {
      titleElement.textContent = this.title;
    }
    
    // Initially hide the chat body
    this.chatBody.style.display = 'none';
  }
  
  attachEventListeners() {
    // Toggle chat visibility
    this.toggleBtn.addEventListener('click', () => {
      this.toggleChatVisibility();
    });
    
    // Send message on button click
    this.sendBtn.addEventListener('click', () => {
      this.sendMessage();
    });
    
    // Send message on Enter key
    this.inputField.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.sendMessage();
      }
    });
  }
  
  toggleChatVisibility() {
    const isVisible = this.chatBody.style.display !== 'none';
    
    if (isVisible) {
      this.chatBody.style.display = 'none';
      this.toggleBtn.textContent = '💬';
    } else {
      this.chatBody.style.display = 'flex';
      this.toggleBtn.textContent = '×';
      // Focus input when showing
      this.inputField.focus();
    }
  }
  
  async sendMessage() {
    const message = this.inputField.value.trim();
    if (!message) return;
    
    // Add user message to UI
    this.addMessageToUI(message, 'user');
    this.inputField.value = '';
    
    try {
      // Show typing indicator
      const typingIndicator = this.addTypingIndicator();
      
      // Send message to backend
      const response = await this.callBackendAPI(message);
      
      // Remove typing indicator
      this.messagesContainer.removeChild(typingIndicator);
      
      // Add bot response to UI
      this.addMessageToUI(response, 'bot');
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Remove typing indicator
      if (this.messagesContainer.lastChild.classList.contains('typing-indicator')) {
        this.messagesContainer.removeChild(this.messagesContainer.lastChild);
      }
      
      // Show error message
      this.addMessageToUI('Sorry, I encountered an error processing your request. Please try again.', 'bot');
    }
  }
  
  addMessageToUI(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(sender + '-message');
    
    const contentElement = document.createElement('div');
    contentElement.classList.add('message-content');
    contentElement.textContent = message;
    
    messageElement.appendChild(contentElement);
    this.messagesContainer.appendChild(messageElement);
    
    // Scroll to bottom
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }
  
  addTypingIndicator() {
    const typingElement = document.createElement('div');
    typingElement.classList.add('message', 'bot-message', 'typing-indicator');
    
    const contentElement = document.createElement('div');
    contentElement.classList.add('message-content');
    contentElement.innerHTML = '...';
    
    typingElement.appendChild(contentElement);
    this.messagesContainer.appendChild(typingElement);
    
    // Scroll to bottom
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    
    return typingElement;
  }
  
  async callBackendAPI(message) {
    const response = await fetch(this.apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: message
      })
    });
    
    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.response || data.content || 'No response from backend';
  }
}

// Initialize the chat widget when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Default options can be overridden by data attributes or global config
  const options = {
    apiEndpoint: window.BOOK_CHAT_API_ENDPOINT || 'http://localhost:8000/api/v1/chat',
    title: 'Book Assistant'
  };
  
  // Initialize the widget
  window.bookChatWidget = new BookChatWidget(options);
});

// Export for use in other modules if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BookChatWidget;
}