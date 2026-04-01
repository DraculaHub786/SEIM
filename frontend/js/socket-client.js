/**
 * Socket.IO Client
 * Handles real-time communication with backend
 */

let socket;
let connectionStatus = document.getElementById('connection-status');

// Auto-detect backend URL
const BACKEND_URL = window.location.origin;

// Initialize Socket.IO connection
function initSocket() {
    socket = io(BACKEND_URL, {
        transports: ['websocket', 'polling']
    });

    // Connection events
    socket.on('connect', () => {
        console.log('✓ Connected to server');
        updateConnectionStatus('connected');
    });

    socket.on('disconnect', () => {
        console.log('✗ Disconnected from server');
        updateConnectionStatus('disconnected');
    });

    socket.on('connect_error', (error) => {
        console.error('Connection error:', error);
        updateConnectionStatus('disconnected');
    });

    socket.on('connection_response', (data) => {
        console.log('Connection response:', data);
    });

    // Pong response
    socket.on('pong', (data) => {
        console.log('Pong received:', data);
    });

    return socket;
}

// Update connection status indicator
function updateConnectionStatus(status) {
    if (!connectionStatus) return;

    connectionStatus.classList.remove('status-connected', 'status-connecting', 'status-disconnected');

    switch (status) {
        case 'connected':
            connectionStatus.classList.add('status-connected');
            connectionStatus.textContent = 'Connected';
            break;
        case 'connecting':
            connectionStatus.classList.add('status-connecting');
            connectionStatus.textContent = 'Connecting...';
            break;
        case 'disconnected':
            connectionStatus.classList.add('status-disconnected');
            connectionStatus.textContent = 'Disconnected';
            break;
    }
}

// Update current time display
function updateCurrentTime() {
    const timeElement = document.getElementById('current-time');
    if (timeElement) {
        const now = new Date();
        timeElement.textContent = now.toLocaleTimeString();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initSocket();
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
});
