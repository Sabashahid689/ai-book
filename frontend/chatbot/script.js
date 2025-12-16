// DOM elements
const chatMessages = document.getElementById('chatMessages');
const messageForm = document.getElementById('messageForm');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const loadingIndicator = document.getElementById('loadingIndicator');

// API endpoint - replace with your actual backend API URL
const API_URL = '/api/chat'; // Using relative path for the mock server

/**
 * Adds a message to the chat interface
 * @param {string} content - Message content
 * @param {string} sender - 'user' or 'bot'
 */
function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    
    const avatarDiv = document.createElement('div');
    avatarDiv.classList.add('avatar');
    
    if (sender === 'user') {
        avatarDiv.innerHTML = '<i class="fas fa-user"></i>';
    } else {
        avatarDiv.innerHTML = '<i class="fas fa-user-md"></i>';
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    
    const contentPara = document.createElement('p');
    contentPara.textContent = content;
    
    contentDiv.appendChild(contentPara);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom after adding message
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Shows/hides the loading indicator
 * @param {boolean} show - Whether to show or hide the loading indicator
 */
function toggleLoading(show) {
    loadingIndicator.style.display = show ? 'flex' : 'none';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Sends message to backend API
 * @param {string} message - Message to send
 */
async function sendMessageToBackend(message) {
    try {
        // Show loading indicator
        toggleLoading(true);
        
        // Send message to backend
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loading indicator
        toggleLoading(false);
        
        // Add bot response to chat
        addMessage(data.response, 'bot'); // Assuming backend returns { response: 'message' }
    } catch (error) {
        console.error('Error sending message:', error);
        
        // Hide loading indicator
        toggleLoading(false);
        
        // Add error message to chat
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    }
}

/**
 * Handles form submission
 * @param {Event} e - Form submit event
 */
function handleSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    
    if (message) {
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        messageInput.value = '';
        
        // Send to backend
        sendMessageToBackend(message);
    }
}

// Event listeners
messageForm.addEventListener('submit', handleSubmit);

// Allow sending with Enter key (without Shift)
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        messageForm.requestSubmit();
    }
});

// Add welcome message when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Scroll to bottom after initial load
    chatMessages.scrollTop = chatMessages.scrollHeight;
});