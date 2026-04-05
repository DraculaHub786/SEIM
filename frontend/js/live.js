/**
 * Live Monitor Page Script
 * Handles real-time log monitoring
 */

const API_BASE = '/api';

let liveLogs = [];
let isMonitoring = true;
let maxLogs = 100;
let logsPerMinute = 0;
let logTimestamps = [];

// Initialize live monitor
async function initLiveMonitor() {
    // Load recent logs from database first
    await loadRecentLogs();
    
    // Listen for real-time logs
    socket.on('new_log', (log) => {
        if (isMonitoring) {
            addLiveLog(log);
            updateStats();
        }
    });

    // Listen for real-time alerts
    socket.on('new_alert', (alert) => {
        showAlertNotification(alert);
        updateAlertCount();
    });

    // Update stats every second
    setInterval(() => {
        calculateLogsPerMinute();
    }, 1000);

    // Load initial stats
    loadInitialStats();
    
    console.log('✅ Live monitor initialized');
}

// Load recent logs from database
async function loadRecentLogs() {
    try {
        const response = await fetch(`${API_BASE}/logs?page=1&page_size=50&sort_by=timestamp&sort_order=desc`, {
            headers: window.getAuthHeaders()
        });
        const data = await response.json();

        if (data.success && data.logs.length > 0) {
            console.log(`✅ Loaded ${data.logs.length} recent logs`);
            liveLogs = data.logs;
            displayLiveLogs();
        } else {
            console.log('⚠️ No logs found in database');
            displayLiveLogs(); // Show "waiting" message
        }
    } catch (error) {
        console.error('❌ Error loading recent logs:', error);
        displayLiveLogs(); // Show "waiting" message
    }
}

// Add log to live feed
function addLiveLog(log) {
    liveLogs.unshift(log);
    logTimestamps.push(Date.now());
    
    // Keep only last N logs
    if (liveLogs.length > maxLogs) {
        liveLogs.pop();
    }

    displayLiveLogs();
}

// Display live logs
function displayLiveLogs() {
    const feed = document.getElementById('live-feed');
    
    if (liveLogs.length === 0) {
        feed.innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <div class="text-6xl mb-4">📡</div>
                <p class="text-lg mb-2">Waiting for incoming logs...</p>
                <p class="text-sm text-gray-600">Send test logs to see them here in real-time</p>
                <p class="text-xs text-gray-700 mt-2">Run: <code class="bg-gray-800 px-2 py-1 rounded">python test_siem.py</code></p>
            </div>
        `;
        return;
    }

    feed.innerHTML = liveLogs.map(log => `
        <div class="live-log-item ${getSeverityClass(log.severity || log.event_type)}" style="animation: slideIn 0.3s ease-out;">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <div class="flex items-center space-x-3 mb-1">
                        <span class="text-xs text-gray-400">${formatTime(log.timestamp)}</span>
                        <span class="px-2 py-1 rounded text-xs ${getSeverityBadge(log.severity)}">${log.event_type}</span>
                        <span class="text-xs text-gray-500">${log.source}</span>
                    </div>
                    <div class="flex items-center space-x-4 text-sm">
                        <span class="font-mono text-cyan-400">${log.ip_address}</span>
                        ${log.username ? `<span class="text-gray-400">👤 ${log.username}</span>` : ''}
                        ${log.process_name ? `<span class="text-gray-400">⚙️ ${log.process_name}</span>` : ''}
                    </div>
                    ${log.message ? `<p class="text-xs text-gray-400 mt-1">${log.message}</p>` : ''}
                </div>
                <div class="ml-4">
                    ${getEventIcon(log.event_type)}
                </div>
            </div>
        </div>
    `).join('');

    // Auto-scroll if enabled
    if (document.getElementById('auto-scroll') && document.getElementById('auto-scroll').checked) {
        feed.scrollTop = 0;
    }

    // Update count
    document.getElementById('log-count').textContent = liveLogs.length;
}

// Calculate logs per minute
function calculateLogsPerMinute() {
    const oneMinuteAgo = Date.now() - 60000;
    logTimestamps = logTimestamps.filter(ts => ts > oneMinuteAgo);
    logsPerMinute = logTimestamps.length;
    
    document.getElementById('logs-per-min').textContent = logsPerMinute;
}

// Toggle monitoring
function toggleMonitoring() {
    isMonitoring = !isMonitoring;
    const btn = document.getElementById('monitor-text');
    
    if (isMonitoring) {
        btn.textContent = '⏸ Pause';
    } else {
        btn.textContent = '▶ Resume';
    }
}

// Clear logs
function clearLogs() {
    liveLogs = [];
    logTimestamps = [];
    displayLiveLogs();
}

// Show alert notification
function showAlertNotification(alert) {
    const notification = document.createElement('div');
    notification.className = `alert-notification alert-${alert.severity}`;
    notification.innerHTML = `
        <div class="flex items-center space-x-3">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <div>
                <p class="font-semibold">${alert.alert_type.replace(/_/g, ' ').toUpperCase()}</p>
                <p class="text-sm">${alert.description}</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 500);
    }, 5000);
}

// Load initial statistics
async function loadInitialStats() {
    try {
        const response = await fetch(`${API_BASE}/alerts/stats`, {
            headers: window.getAuthHeaders()
        });
        const data = await response.json();

        if (data.success) {
            document.getElementById('recent-alerts').textContent = data.stats.recent_alerts || 0;
            document.getElementById('active-sessions').textContent = Math.floor(Math.random() * 50) + 10;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Update alert count
function updateAlertCount() {
    const current = parseInt(document.getElementById('recent-alerts').textContent);
    document.getElementById('recent-alerts').textContent = current + 1;
}

// Update stats periodically
function updateStats() {
    // Simulate active sessions (in production, get from backend)
    const sessions = Math.floor(Math.random() * 50) + 10;
    document.getElementById('active-sessions').textContent = sessions;
}

// Helper functions
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
}

function getSeverityClass(severity) {
    if (!severity) return 'border-blue-500';
    
    const severityLower = severity.toLowerCase();
    if (severityLower === 'high' || severityLower.includes('critical')) {
        return 'border-red-500';
    } else if (severityLower === 'medium') {
        return 'border-yellow-500';
    } else if (severityLower === 'low') {
        return 'border-green-500';
    }
    return 'border-blue-500';
}

function getSeverityBadge(severity) {
    if (!severity) return 'bg-gray-700';
    
    const severityLower = severity.toLowerCase();
    if (severityLower === 'high') {
        return 'bg-red-600 text-white';
    } else if (severityLower === 'medium') {
        return 'bg-yellow-600 text-white';
    } else if (severityLower === 'low') {
        return 'bg-green-600 text-white';
    }
    return 'bg-gray-700';
}

function getEventIcon(eventType) {
    const icons = {
        'failed_login': '❌',
        'successful_login': '✅',
        'file_access': '📁',
        'firewall_block': '🛡️',
        'network_connection': '🌐',
        'process_execution': '⚙️',
        'sql_injection': '💉',
        'port_scan': '🔍',
        'dos_attack': '💥',
        'unauthorized_access': '🚫',
        'brute_force': '🔨',
        'malware': '🦠',
        'phishing': '🎣',
        'data_exfiltration': '📤'
    };
    
    return `<span class="text-2xl">${icons[eventType] || '📋'}</span>`;
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    initLiveMonitor();
});