/**
 * Alerts Page Script
 * Handles alerts panel functionality
 */

const API_BASE = '/api';

let currentPage = 1;
let pageSize = 20;
let currentFilters = {};

// Initialize alerts page
async function initAlertsPage() {
    await loadStatistics();
    await loadAlerts();
    
    // Listen for real-time alert updates
    socket.on('new_alert', (alert) => {
        console.log('New alert received:', alert);
        // Refresh if on first page
        if (currentPage === 1) {
            loadAlerts();
            loadStatistics();
        }
    });
}

// Load alert statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/alerts/stats`);
        const data = await response.json();

        if (data.success) {
            document.getElementById('open-count').textContent = data.stats.open_alerts;
            document.getElementById('high-count').textContent = data.stats.critical_alerts;
            document.getElementById('total-count').textContent = data.stats.total_alerts;
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load alerts with current filters
async function loadAlerts() {
    try {
        const params = new URLSearchParams({
            page: currentPage,
            page_size: pageSize,
            ...currentFilters
        });

        const response = await fetch(`${API_BASE}/alerts?${params}`);
        const data = await response.json();

        if (data.success) {
            displayAlerts(data.alerts);
            updatePagination(data.pagination);
        } else {
            showError('Failed to load alerts');
        }
    } catch (error) {
        console.error('Error loading alerts:', error);
        showError('Error loading alerts');
    }
}

// Display alerts
function displayAlerts(alerts) {
    const container = document.getElementById('alerts-container');
    
    if (alerts.length === 0) {
        container.innerHTML = '<div class="text-center text-gray-500 py-8">No alerts found</div>';
        return;
    }

    container.innerHTML = alerts.map(alert => `
        <div class="alert-card ${alert.severity}">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <div class="flex items-center space-x-3 mb-2">
                        <span class="severity-badge severity-${alert.severity}">${alert.severity}</span>
                        <span class="text-sm text-gray-400">${formatTimestamp(alert.timestamp)}</span>
                        <span class="px-2 py-1 rounded text-xs ${getStatusClass(alert.status)}">${alert.status}</span>
                    </div>
                    <h4 class="font-semibold text-lg">${formatAlertType(alert.alert_type)}</h4>
                    <p class="text-sm text-gray-400 mt-1">${alert.description}</p>
                    <div class="flex items-center space-x-4 mt-3 text-xs text-gray-500">
                        <span>🔍 IP: ${alert.ip_address}</span>
                        <span>📊 Score: ${alert.score}/100</span>
                        <span>📝 Events: ${alert.event_count}</span>
                        ${alert.username ? `<span>👤 User: ${alert.username}</span>` : ''}
                    </div>
                </div>
                <div class="ml-4">
                    <select onchange="updateAlertStatus('${alert._id}', this.value)" class="input-field text-sm">
                        <option value="open" ${alert.status === 'open' ? 'selected' : ''}>Open</option>
                        <option value="investigating" ${alert.status === 'investigating' ? 'selected' : ''}>Investigating</option>
                        <option value="resolved" ${alert.status === 'resolved' ? 'selected' : ''}>Resolved</option>
                        <option value="false_positive" ${alert.status === 'false_positive' ? 'selected' : ''}>False Positive</option>
                    </select>
                </div>
            </div>
        </div>
    `).join('');
}

// Update pagination
function updatePagination(pagination) {
    document.getElementById('current-page').textContent = pagination.page;
    document.getElementById('alert-total-count').textContent = formatNumber(pagination.total_count);
    
    document.getElementById('btn-prev').disabled = pagination.page === 1;
    document.getElementById('btn-next').disabled = pagination.page >= pagination.total_pages;
}

// Apply filters
function applyFilters() {
    currentPage = 1;
    currentFilters = {};
    
    const status = document.getElementById('filter-status').value;
    const severity = document.getElementById('filter-severity').value;
    
    if (status) currentFilters.status = status;
    if (severity) currentFilters.severity = severity;
    
    loadAlerts();
}

// Pagination
function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        loadAlerts();
    }
}

function nextPage() {
    currentPage++;
    loadAlerts();
}

// Refresh alerts
function refreshAlerts() {
    loadAlerts();
    loadStatistics();
}

// Update alert status
async function updateAlertStatus(alertId, newStatus) {
    try {
        const response = await fetch(`${API_BASE}/alerts/${alertId}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });

        const data = await response.json();

        if (data.success) {
            console.log('Alert status updated');
            loadAlerts();
            loadStatistics();
        } else {
            showError('Failed to update alert status');
        }
    } catch (error) {
        console.error('Error updating alert status:', error);
        showError('Error updating alert status');
    }
}

// Helper functions
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return Math.floor(diff / 60000) + ' minutes ago';
    if (diff < 86400000) return Math.floor(diff / 3600000) + ' hours ago';
    
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function formatAlertType(type) {
    return type.replace(/_/g, ' ').toUpperCase();
}

function getStatusClass(status) {
    const classes = {
        'open': 'bg-orange-500 text-white',
        'investigating': 'bg-blue-500 text-white',
        'resolved': 'bg-green-500 text-white',
        'false_positive': 'bg-gray-500 text-white'
    };
    return classes[status] || 'bg-gray-500 text-white';
}

function formatNumber(num) {
    return num.toLocaleString();
}

function showError(message) {
    console.error(message);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    initAlertsPage();
});