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
        const logResponse = await fetch(`${API_BASE}/logs/stats`, { headers: window.getAuthHeaders() });
        const logData = await logResponse.json();

        if (logData.success) {
            document.getElementById('total-logs').textContent = 
                formatNumber(logData.stats.total_logs);
        }

        // Load alert stats
        const alertResponse = await fetch(`${API_BASE}/alerts/stats`, { headers: window.getAuthHeaders() });
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
        const logsTimeResponse = await fetch(`${API_BASE}/logs/chart/over-time?hours=24`, { headers: window.getAuthHeaders() });
        const logsTimeData = await logsTimeResponse.json();
        
        // Fetch real events by type data
        const eventsTypeResponse = await fetch(`${API_BASE}/logs/chart/by-type`, { headers: window.getAuthHeaders() });
        const eventsTypeData = await eventsTypeResponse.json();

        // Chart.js Global Defaults for Figma-style UI
        Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.scale.grid.color = 'rgba(255, 255, 255, 0.03)';
        
        // Logs over time chart (LINE CHART)
        const logsCtx = document.getElementById('logsChart').getContext('2d');
        let logsGradient = logsCtx.createLinearGradient(0, 0, 0, 300);
        logsGradient.addColorStop(0, 'rgba(56, 189, 248, 0.3)');
        logsGradient.addColorStop(1, 'rgba(56, 189, 248, 0.0)');

        logsChart = new Chart(logsCtx, {
            type: 'line',
            data: {
                labels: logsTimeData.success ? logsTimeData.labels : [],
                datasets: [{
                    label: 'Logs',
                    data: logsTimeData.success ? logsTimeData.data : [],
                    borderColor: '#38bdf8',
                    borderWidth: 2,
                    backgroundColor: logsGradient,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#0f172a',
                    pointBorderColor: '#38bdf8',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: 'Logs Over Time (Last 24 Hours)',
                        color: '#cbd5e1',
                        font: { size: 13, weight: '500' },
                        padding: { bottom: 20 }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#f8fafc',
                        bodyColor: '#cbd5e1',
                        borderColor: 'rgba(56, 189, 248, 0.2)',
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { borderDash: [4, 4], drawBorder: false },
                        ticks: { stepSize: 1, padding: 10 }
                    },
                    x: {
                        grid: { display: false, drawBorder: false },
                        ticks: { maxRotation: 45, minRotation: 45, padding: 10, maxTicksLimit: 12 }
                    }
                }
            }
        });

        // Events by type chart (DOUGHNUT CHART)
        const eventsCtx = document.getElementById('eventsChart').getContext('2d');
        const colors = ['#f43f5e', '#10b981', '#f59e0b', '#8b5cf6', '#0ea5e9', '#ec4899', '#f97316', '#14b8a6', '#6366f1', '#64748b'];

        // Plugin to draw text in the center of the doughnut
        const centerTextPlugin = {
            id: 'centerText',
            beforeDraw: function(chart) {
                if (chart.config.type !== 'doughnut') return;
                const {ctx, chartArea: {top, bottom, left, right}} = chart;
                const centerX = (left + right) / 2;
                const centerY = (top + bottom) / 2;
                
                ctx.restore();
                
                // Calculate font size relative to doughnut inner height
                const innerHeight = bottom - top;
                const fontSize = (innerHeight / 120).toFixed(2);
                ctx.font = '700 ' + fontSize + "em Inter";
                ctx.textBaseline = "middle";
                ctx.fillStyle = "#f8fafc";
                
                let sum = 0;
                if(chart.data.datasets.length > 0) {
                    chart.data.datasets[0].data.forEach(d => { sum += Number(d) || 0; });
                }
                
                const text = sum.toString(),
                      textX = centerX - (ctx.measureText(text).width / 2),
                      textY = centerY - (innerHeight * 0.05); // slightly above exact center
        
                ctx.fillText(text, textX, textY);
                
                ctx.font = '500 ' + (fontSize * 0.35).toFixed(2) + "em Inter";
                ctx.fillStyle = "#94a3b8";
                const subText = "Total Events",
                      subTextX = centerX - (ctx.measureText(subText).width / 2);
                ctx.fillText(subText, subTextX, textY + (innerHeight * 0.15));
                ctx.save();
            }
        };

        eventsChart = new Chart(eventsCtx, {
            type: 'doughnut',
            data: {
                labels: eventsTypeData.success ? eventsTypeData.labels : ['No Data'],
                datasets: [{
                    data: eventsTypeData.success && eventsTypeData.data.length > 0 ? eventsTypeData.data : [1],
                    backgroundColor: eventsTypeData.success && eventsTypeData.data.length > 0 ? colors.slice(0, eventsTypeData.data.length) : ['#334155'],
                    borderWidth: 0,
                    borderRadius: 5,
                    spacing: 5
                }]
            },
            plugins: [centerTextPlugin],
            options: {
                cutout: '78%',
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: { bottom: 10 }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: { size: 12 }
                        }
                    },
                    title: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#f8fafc',
                        bodyColor: '#cbd5e1',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8
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
        const logsTimeResponse = await fetch(`${API_BASE}/logs/chart/over-time?hours=24`, { headers: window.getAuthHeaders() });
        const logsTimeData = await logsTimeResponse.json();
        
        const eventsTypeResponse = await fetch(`${API_BASE}/logs/chart/by-type`, { headers: window.getAuthHeaders() });
        const eventsTypeData = await eventsTypeResponse.json();
        
        // Update logs over time chart
        if (logsTimeData.success && logsChart) {
            logsChart.data.labels = logsTimeData.labels;
            logsChart.data.datasets[0].data = logsTimeData.data;
            logsChart.update();
        }
        
        // Update events by type chart
        if (eventsTypeData.success && eventsChart) {
            const colors = ['#f43f5e', '#10b981', '#f59e0b', '#8b5cf6', '#0ea5e9', '#ec4899', '#f97316', '#14b8a6', '#6366f1', '#64748b'];
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
    Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.scale.grid.color = 'rgba(255, 255, 255, 0.03)';

    const logsCtx = document.getElementById('logsChart').getContext('2d');
    logsChart = new Chart(logsCtx, {
        type: 'line',
        data: {
            labels: ['No data'],
            datasets: [{
                label: 'Logs',
                data: [0],
                borderColor: '#38bdf8',
                borderWidth: 2,
                backgroundColor: 'rgba(56, 189, 248, 0.1)',
                tension: 0.4, fill: true, pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: { display: true, text: 'Logs Over Time - Send test data to populate', color: '#cbd5e1' }
            },
            scales: {
                y: { grid: { borderDash: [4, 4], drawBorder: false } },
                x: { grid: { display: false, drawBorder: false } }
            }
        }
    });
    
    // Plugin to draw text in the center of the doughnut
    const centerTextPlugin = {
        id: 'centerText',
        beforeDraw: function(chart) {
            if (chart.config.type !== 'doughnut') return;
            const {ctx, chartArea: {top, bottom, left, right}} = chart;
            const centerX = (left + right) / 2;
            const centerY = (top + bottom) / 2;
            ctx.restore();
            
            const innerHeight = bottom - top;
            const fontSize = (innerHeight / 120).toFixed(2);
            ctx.font = '700 ' + fontSize + "em Inter";
            ctx.textBaseline = "middle";
            ctx.fillStyle = "#f8fafc";
            const text = "0", textX = centerX - (ctx.measureText(text).width / 2), textY = centerY - (innerHeight * 0.05);
            ctx.fillText(text, textX, textY);
            
            ctx.font = '500 ' + (fontSize * 0.35).toFixed(2) + "em Inter";
            ctx.fillStyle = "#94a3b8";
            const subText = "Total Events", subTextX = centerX - (ctx.measureText(subText).width / 2);
            ctx.fillText(subText, subTextX, textY + (innerHeight * 0.15));
            ctx.save();
        }
    };

    const eventsCtx = document.getElementById('eventsChart').getContext('2d');
    eventsChart = new Chart(eventsCtx, {
        type: 'doughnut',
        data: {
            labels: ['No Data'],
            datasets: [{ 
                data: [1], 
                backgroundColor: ['#334155'], 
                borderWidth: 0, 
                borderRadius: 5, 
                spacing: 5 
            }]
        },
        plugins: [centerTextPlugin],
        options: {
            cutout: '78%',
            responsive: true,
            maintainAspectRatio: false,
            layout: { padding: { bottom: 10 } },
            plugins: {
                legend: { position: 'bottom', labels: { usePointStyle: true, padding: 20 } },
                title: { display: false }
            }
        }
    });
}

// Load recent alerts
async function loadRecentAlerts() {
    try {
        const response = await fetch(`${API_BASE}/alerts?page=1&page_size=5&status=open`, { headers: window.getAuthHeaders() });
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
