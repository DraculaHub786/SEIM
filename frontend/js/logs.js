/**
 * Logs Page Script
 * Handles logs viewer functionality
 */

const API_BASE = '/api';

let currentPage = 1;
let pageSize = 100;
let currentFilters = {};

// Initialize logs page
async function initLogsPage() {
    await loadLogs();
    
    // Listen for real-time log updates
    socket.on('new_log', (log) => {
        console.log('New log received:', log);
        // Refresh if on first page
        if (currentPage === 1) {
            loadLogs();
        }
    });
}

// Load logs with current filters
async function loadLogs() {
    try {
        // Build query string
        const params = new URLSearchParams({
            page: currentPage,
            page_size: pageSize,
            ...currentFilters
        });

        const response = await fetch(`${API_BASE}/logs?${params}`);
        const data = await response.json();

        if (data.success) {
            displayLogs(data.logs);
            updatePagination(data.pagination);
        } else {
            showError('Failed to load logs');
        }
    } catch (error) {
        console.error('Error loading logs:', error);
        showError('Error loading logs');
    }
}

// Display logs in table
function displayLogs(logs) {
    const tbody = document.getElementById('logs-table-body');
    
    if (logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-gray-500 py-8">No logs found</td></tr>';
        return;
    }

    tbody.innerHTML = logs.map(log => `
        <tr onclick="viewLogDetails('${log._id}', ${JSON.stringify(log).replace(/"/g, '&quot;')})">
            <td class="text-sm">${formatTimestamp(log.timestamp)}</td>
            <td class="text-sm">${log.source}</td>
            <td><span class="px-2 py-1 bg-gray-700 rounded text-xs">${log.event_type}</span></td>
            <td class="text-sm font-mono">${log.ip_address}</td>
            <td class="text-sm">${log.username || '-'}</td>
            <td><span class="severity-badge severity-${log.severity || 'low'}">${log.severity || 'low'}</span></td>
            <td>
                <button onclick="event.stopPropagation(); viewLogDetails('${log._id}', ${JSON.stringify(log).replace(/"/g, '&quot;')})" class="text-cyan-400 hover:text-cyan-300 text-sm">
                    View
                </button>
            </td>
        </tr>
    `).join('');
}

// Update pagination controls
function updatePagination(pagination) {
    document.getElementById('current-page').textContent = pagination.page;
    document.getElementById('total-pages').textContent = pagination.total_pages;
    document.getElementById('total-count').textContent = formatNumber(pagination.total_count);
    
    const showingFrom = (pagination.page - 1) * pagination.page_size + 1;
    const showingTo = Math.min(pagination.page * pagination.page_size, pagination.total_count);
    
    document.getElementById('showing-from').textContent = showingFrom;
    document.getElementById('showing-to').textContent = showingTo;
    document.getElementById('showing-total').textContent = formatNumber(pagination.total_count);
    
    // Enable/disable pagination buttons
    document.getElementById('btn-prev').disabled = pagination.page === 1;
    document.getElementById('btn-next').disabled = pagination.page >= pagination.total_pages;
}

// Apply filters
function applyFilters() {
    currentPage = 1;
    currentFilters = {};
    
    const ipAddress = document.getElementById('filter-ip').value;
    const eventType = document.getElementById('filter-event-type').value;
    const source = document.getElementById('filter-source').value;
    
    if (ipAddress) currentFilters.ip_address = ipAddress;
    if (eventType) currentFilters.event_type = eventType;
    if (source) currentFilters.source = source;
    
    loadLogs();
}

// Pagination controls
function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        loadLogs();
    }
}

function nextPage() {
    currentPage++;
    loadLogs();
}

// Refresh logs
function refreshLogs() {
    loadLogs();
}

// View log details
function viewLogDetails(logId, logData) {
    const modal = document.getElementById('log-modal');
    const content = document.getElementById('log-detail-content');
    
    content.textContent = JSON.stringify(logData, null, 2);
    modal.classList.remove('hidden');
}

// Close modal
function closeModal() {
    document.getElementById('log-modal').classList.add('hidden');
}

// Export logs as CSV
async function exportLogs() {
    try {
        const params = new URLSearchParams({
            page: 1,
            page_size: 10000,
            ...currentFilters
        });

        const response = await fetch(`${API_BASE}/logs?${params}`);
        const data = await response.json();

        if (data.success) {
            downloadCSV(data.logs);
        }
    } catch (error) {
        console.error('Error exporting logs:', error);
    }
}

// Download logs as CSV
function downloadCSV(logs) {
    const headers = ['Timestamp', 'Source', 'Event Type', 'IP Address', 'Username', 'Severity'];
    const rows = logs.map(log => [
        log.timestamp,
        log.source,
        log.event_type,
        log.ip_address,
        log.username || '',
        log.severity || ''
    ]);

    let csv = headers.join(',') + '\n';
    rows.forEach(row => {
        csv += row.map(field => `"${field}"`).join(',') + '\n';
    });

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `siem-logs-${new Date().toISOString()}.csv`;
    a.click();
}

// Utility functions
function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString();
}

function formatNumber(num) {
    return num.toLocaleString();
}

function showError(message) {
    console.error(message);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    initLogsPage();
});