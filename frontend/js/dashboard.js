/**
 * Dashboard Page Script
 * Handles overview dashboard functionality
 */

const API_BASE = '/api';

let logsChart, eventsChart;

// Initialize dashboard
async function initDashboard() {
    await loadStatistics();
    await initializeCharts(); // Changed to async
    await loadRecentAlerts();

    // Listen for real-time updates
    socket.on('new_log', (log) => {
        console.log('New log received:', log);
        updateStatsIncremental('logs');
        refreshCharts(); // Refresh charts with new data
    });

    socket.on('new_alert', (alert) => {
        console.log('New alert received:', alert);
        showAlertNotification(alert);
        updateStatsIncremental('alerts');
        addAlertToRecentList(alert);
    });

    // Refresh data every 30 seconds
    setInterval(async () => {
        await loadStatistics();
        await refreshCharts();
    }, 30000);
}

// Load statistics
async function loadStatistics() {
    try {
        // Load log stats
        const logResponse = await fetch(`${API_BASE}/logs/stats`);
        const logData = await logResponse.json();

        if (logData.success) {
            document.getElementById('total-logs').textContent = 
                formatNumber(logData.stats.total_logs);
        }

        // Load alert stats
        const alertResponse = await fetch(`${API_BASE}/alerts/stats`);
        const alertData = await alertResponse.json();

        if (alertData.success) {
            document.getElementById('total-alerts').textContent = 
                formatNumber(alertData.stats.total_alerts);
            document.getElementById('open-alerts').textContent = 
                formatNumber(alertData.stats.open_alerts);
            document.getElementById('critical-alerts').textContent = 
                formatNumber(alertData.stats.critical_alerts);
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Initialize charts with REAL data from MongoDB
async function initializeCharts() {
    try {
        // Fetch real logs over time data
        const logsTimeResponse = await fetch(`${API_BASE}/logs/chart/over-time?hours=24`);
        const logsTimeData = await logsTimeResponse.json();
        
        // Fetch real events by type data
        const eventsTypeResponse = await fetch(`${API_BASE}/logs/chart/by-type`);
        const eventsTypeData = await eventsTypeResponse.json();
        
        // Logs over time chart (LINE CHART - REAL DATA)
        const logsCtx = document.getElementById('logsChart').getContext('2d');
        logsChart = new Chart(logsCtx, {
            type: 'line',
            data: {
                labels: logsTimeData.success ? logsTimeData.labels : [],
                datasets: [{
                    label: 'Logs',
                    data: logsTimeData.success ? logsTimeData.data : [],
                    borderColor: '#06B6D4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Logs Over Time (Last 24 Hours) - LIVE DATA',
                        color: '#9CA3AF',
                        font: { size: 12 }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#374151'
                        },
                        ticks: {
                            color: '#9CA3AF',
                            stepSize: 1
                        }
                    },
                    x: {
                        grid: {
                            color: '#374151'
                        },
                        ticks: {
                            color: '#9CA3AF',
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });

        // Events by type chart (DOUGHNUT CHART - REAL DATA)
        const eventsCtx = document.getElementById('eventsChart').getContext('2d');
        
        // Define colors for event types
        const colors = [
            '#EF4444', // Red
            '#10B981', // Green
            '#F59E0B', // Yellow
            '#8B5CF6', // Purple
            '#06B6D4', // Cyan
            '#EC4899', // Pink
            '#F97316', // Orange
            '#14B8A6', // Teal
            '#6366F1', // Indigo
            '#6B7280'  // Gray
        ];
        
        eventsChart = new Chart(eventsCtx, {
            type: 'doughnut',
            data: {
                labels: eventsTypeData.success ? eventsTypeData.labels : ['No Data'],
                datasets: [{
                    data: eventsTypeData.success && eventsTypeData.data.length > 0 ? eventsTypeData.data : [1],
                    backgroundColor: eventsTypeData.success && eventsTypeData.data.length > 0 ? colors.slice(0, eventsTypeData.data.length) : ['#6B7280']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#9CA3AF',
                            padding: 15,
                            font: { size: 11 }
                        }
                    },
                    title: {
                        display: true,
                        text: 'Events by Type - LIVE DATA',
                        color: '#9CA3AF',
                        font: { size: 12 }
                    }
                }
            }
        });
        
        console.log('✅ Charts initialized with REAL data from MongoDB');
    } catch (error) {
        console.error('Error initializing charts:', error);
        // Fallback to empty charts if API fails
        initializeEmptyCharts();
    }
}

// Refresh charts with latest data
async function refreshCharts() {
    try {
        // Fetch updated data
        const logsTimeResponse = await fetch(`${API_BASE}/logs/chart/over-time?hours=24`);
        const logsTimeData = await logsTimeResponse.json();
        
        const eventsTypeResponse = await fetch(`${API_BASE}/logs/chart/by-type`);
        const eventsTypeData = await eventsTypeResponse.json();
        
        // Update logs over time chart
        if (logsTimeData.success && logsChart) {
            logsChart.data.labels = logsTimeData.labels;
            logsChart.data.datasets[0].data = logsTimeData.data;
            logsChart.update();
        }
        
        // Update events by type chart
        if (eventsTypeData.success && eventsChart) {
            const colors = [
                '#EF4444', '#10B981', '#F59E0B', '#8B5CF6', '#06B6D4',
                '#EC4899', '#F97316', '#14B8A6', '#6366F1', '#6B7280'
            ];
            
            eventsChart.data.labels = eventsTypeData.labels;
            eventsChart.data.datasets[0].data = eventsTypeData.data;
            eventsChart.data.datasets[0].backgroundColor = colors.slice(0, eventsTypeData.data.length);
            eventsChart.update();
        }
        
        console.log('✅ Charts refreshed with latest data');
    } catch (error) {
        console.error('Error refreshing charts:', error);
    }
}

// Fallback: Initialize empty charts if data fetch fails
function initializeEmptyCharts() {
    const logsCtx = document.getElementById('logsChart').getContext('2d');
    logsChart = new Chart(logsCtx, {
        type: 'line',
        data: {
            labels: ['No data'],
            datasets: [{
                label: 'Logs',
                data: [0],
                borderColor: '#06B6D4',
                backgroundColor: 'rgba(6, 182, 212, 0.1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'Logs Over Time - Send test data to populate',
                    color: '#9CA3AF'
                }
            }
        }
    });
    
    const eventsCtx = document.getElementById('eventsChart').getContext('2d');
    eventsChart = new Chart(eventsCtx, {
        type: 'doughnut',
        data: {
            labels: ['No Data'],
            datasets: [{
                data: [1],
                backgroundColor: ['#6B7280']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { color: '#9CA3AF' } },
                title: {
                    display: true,
                    text: 'Events by Type - Send test data to populate',
                    color: '#9CA3AF'
                }
            }
        }
    });
}

// Load recent alerts
async function loadRecentAlerts() {
    try {
        const response = await fetch(`${API_BASE}/alerts?page=1&page_size=5&status=open`);
        const data = await response.json();

        if (data.success && data.alerts.length > 0) {
            displayRecentAlerts(data.alerts);
        } else {
            document.getElementById('recent-alerts').innerHTML = 
                '<div class="text-center text-gray-500 py-8">No recent alerts</div>';
        }
    } catch (error) {
        console.error('Error loading recent alerts:', error);
    }
}

// Display recent alerts
function displayRecentAlerts(alerts) {
    const container = document.getElementById('recent-alerts');
    container.innerHTML = '';

    alerts.forEach(alert => {
        const alertCard = createAlertCard(alert);
        container.appendChild(alertCard);
    });
}

// Create alert card element
function createAlertCard(alert) {
    const card = document.createElement('div');
    card.className = `alert-card ${alert.severity}`;
    
    card.innerHTML = `
        <div class="flex items-start justify-between">
            <div class="flex-1">
                <div class="flex items-center space-x-3">
                    <span class="severity-badge severity-${alert.severity}">${alert.severity}</span>
                    <span class="text-sm text-gray-400">${formatTimestamp(alert.timestamp)}</span>
                </div>
                <h4 class="font-semibold mt-2">${alert.alert_type.replace(/_/g, ' ').toUpperCase()}</h4>
                <p class="text-sm text-gray-400 mt-1">${alert.description}</p>
                <div class="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                    <span>IP: ${alert.ip_address}</span>
                    <span>Score: ${alert.score}/100</span>
                    <span>${alert.event_count} events</span>
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// Add new alert to recent list
function addAlertToRecentList(alert) {
    const container = document.getElementById('recent-alerts');
    
    // Remove "no alerts" message if present
    if (container.querySelector('.text-center')) {
        container.innerHTML = '';
    }
    
    // Add new alert at the top
    const alertCard = createAlertCard(alert);
    container.insertBefore(alertCard, container.firstChild);
    
    // Keep only 5 alerts
    while (container.children.length > 5) {
        container.removeChild(container.lastChild);
    }
}

// Show alert notification
function showAlertNotification(alert) {
    console.log('🚨 New Alert:', alert);
}

// Update stats incrementally
function updateStatsIncremental(type) {
    if (type === 'logs') {
        const element = document.getElementById('total-logs');
        const current = parseInt(element.textContent.replace(/,/g, ''));
        element.textContent = formatNumber(current + 1);
    } else if (type === 'alerts') {
        const totalElement = document.getElementById('total-alerts');
        const openElement = document.getElementById('open-alerts');
        
        const currentTotal = parseInt(totalElement.textContent.replace(/,/g, ''));
        const currentOpen = parseInt(openElement.textContent.replace(/,/g, ''));
        
        totalElement.textContent = formatNumber(currentTotal + 1);
        openElement.textContent = formatNumber(currentOpen + 1);
    }
}

// Utility functions
function formatNumber(num) {
    return num.toLocaleString();
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return Math.floor(diff / 60000) + ' minutes ago';
    if (diff < 86400000) return Math.floor(diff / 3600000) + ' hours ago';
    
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
});
