const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the chatbot directory
app.use(express.static(path.join(__dirname, '.')));

// Parse JSON bodies
app.use(express.json());

// Mock chatbot API endpoint
app.post('/api/chat', (req, res) => {
    const userMessage = req.body.message.toLowerCase();
    
    // Simple responses based on keywords
    let botResponse = "Thank you for your message. As an online doctor, I recommend consulting with a healthcare professional for medical advice.";
    
    if (userMessage.includes('hello') || userMessage.includes('hi')) {
        botResponse = "Hello! I'm your online doctor assistant. How can I help you today?";
    } else if (userMessage.includes('headache') || userMessage.includes('head pain')) {
        botResponse = "For headaches, try resting in a quiet, dark room. Stay hydrated and consider taking paracetamol if appropriate. If severe or persistent, consult a doctor.";
    } else if (userMessage.includes('fever') || userMessage.includes('temperature')) {
        botResponse = "For fever, rest and stay hydrated. You can take paracetamol to reduce temperature. Monitor your symptoms. Seek medical attention if it persists or worsens.";
    } else if (userMessage.includes('cold') || userMessage.includes('cough')) {
        botResponse = "For cold symptoms, rest, drink warm fluids, and maintain humidity in the air. Over-the-counter remedies may help. See a doctor if symptoms persist.";
    } else if (userMessage.includes('thank')) {
        botResponse = "You're welcome! Is there anything else I can assist you with?";
    } else if (userMessage.includes('bye') || userMessage.includes('goodbye')) {
        botResponse = "Take care! Remember, I'm here if you need any health advice. For serious conditions, always consult a healthcare professional.";
    }
    
    // Simulate processing delay
    setTimeout(() => {
        res.json({ response: botResponse });
    }, 1000);
});

// Serve the index.html file at the root
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
    console.log(`Visit http://localhost:${PORT} to see the chatbot UI`);
});