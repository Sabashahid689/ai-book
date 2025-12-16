# Online Doctor Chatbot UI

A modern, responsive frontend for an online doctor chatbot with clean medical-themed design and smooth animations.

## Features

- Clean, professional medical-themed UI (blue/white/light green colors)
- Responsive layout (mobile, tablet, desktop compatible)
- Smooth message animations (fade/slide effects)
- User messages on the right, bot messages on the left
- Doctor avatar icon in header and message bubbles
- Loading animation while waiting for backend response
- Enter key and button support for sending messages

## Files Included

- `index.html` - Main HTML structure with chat interface
- `style.css` - Styling and responsive design
- `script.js` - Client-side functionality for sending/receiving messages

## Setup Instructions

1. Place all files in your web server directory
2. Open `index.html` in a browser
3. Update the API endpoint in `script.js` (see below)

## Backend Integration

1. Update the API_URL variable in `script.js` with your actual backend endpoint
2. The frontend sends POST requests with the message in JSON format: `{ message: "user input" }`
3. The backend should return responses in JSON format: `{ response: "bot reply" }`

Example:
```javascript
const API_URL = 'https://your-backend-domain.com/api/chat'; // Replace with your actual API endpoint
```

## Design Elements

- Medical-themed color scheme (blues and greens)
- Rounded chat bubbles with subtle shadows
- Modern Roboto font
- Smooth animations for message transitions
- Typing indicators when waiting for responses
- Responsive layout that works on all devices