/**
 * AnalyticsView.js - Advanced Analytics View
 * 
 * Features:
 * - Usage statistics and charts
 * - Prompt popularity analysis
 * - Project progress tracking
 * - Category breakdown
 * - Time-based trends
 * - Export statistics
 */

export default function createAnalyticsView() {
    const container = document.createElement('div');
    container.className = 'analytics-view';
    
    // ==================== HEADER ====================
    const header = document.createElement('div');
    header.className = 'view-header';
    header.innerHTML = `
        <div class="header-content">
            <h1 class="view-title">📊 Analytics</h1>
            <p class="view-subtitle">Insights and statistics about your prompts and projects</p>
        </div>
    `;
    container.appendChild(header);
    
    // ==================== FILTERS ====================
    const filters = document.createElement('div');
    filters.className = 'analytics-filters';
    filters.innerHTML = `
        <div class="filter-group">
            <label for="analytics-period">Time Period:</label>
            <select id="analytics-period" class="filter-select">
                <option value="7days">Last 7 Days</option>
                <option value="30days">Last 30 Days</option>
                <option value="90days">Last 90 Days</option>
                <option value="all">All Time</option>
            </select>
        </div>
        <button id="btn-export-stats" class="btn btn-secondary">📥 Export Stats</button>
    `;
    container.appendChild(filters);
    
    // ==================== DASHBOARD GRID ====================
    const dashboard = document.createElement('div');
    dashboard.className = 'analytics-dashboard';
    dashboard.innerHTML = `
        <!-- Stats Cards -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📝</div>
                <div class="stat-content">
                    <h3>Total Prompts</h3>
                    <p class="stat-value" id="total-prompts">0</p>
                    <small class="stat-change">+0% this month</small>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">📁</div>
                <div class="stat-content">
                    <h3>Active Projects</h3>
                    <p class="stat-value" id="total-projects">0</p>
                    <small class="stat-change">2 in progress</small>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">⚡</div>
                <div class="stat-content">
                    <h3>Total Uses</h3>
                    <p class="stat-value" id="total-uses">0</p>
                    <small class="stat-change">+0% this month</small>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">⭐</div>
                <div class="stat-content">
                    <h3>Avg. Rating</h3>
                    <p class="stat-value" id="avg-rating">0.0</p>
                    <small class="stat-change">Based on feedback</small>
                </div>
            </div>
        </div>
        
        <!-- Charts Section -->
        <div class="charts-section">
            <div class="chart-container">
                <h3>Usage Over Time</h3>
                <div class="chart-placeholder" id="usage-chart">
                    <svg viewBox="0 0 400 200" class="simple-chart">
                        <polyline points="10,180 50,150 90,120 130,140 170,100 210,120 250,80 290,100 330,70 370,90" 
                                  fill="none" stroke="currentColor" stroke-width="2"/>
                        <line x1="10" y1="185" x2="370" y2="185" stroke="currentColor" stroke-width="1" opacity="0.3"/>
                    </svg>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Top 5 Prompts</h3>
                <div class="top-list" id="top-prompts">
                    <div class="loading-small">Loading...</div>
                </div>
            </div>
        </div>
        
        <!-- Category Breakdown -->
        <div class="category-section">
            <h3>Prompts by Category</h3>
            <div class="category-breakdown" id="category-breakdown">
                <div class="loading-small">Loading...</div>
            </div>
        </div>
        
        <!-- Recent Activity -->
        <div class="activity-section">
            <h3>Recent Activity</h3>
            <div class="activity-list" id="activity-list">
                <div class="loading-small">Loading...</div>
            </div>
        </div>
    `;
    container.appendChild(dashboard);
    
    // ==================== DATA STATE ====================
    let analyticsPeriod = '7days';
    let analyticsData = {
        summary: {},
        topPrompts: [],
        categories: {},
        activity: []
    };
    
    // ==================== FUNCTIONS ====================
    
    /**
     * Load analytics data
     */
    async function loadAnalytics() {
        try {
            if (!window.http) {
                throw new Error('HTTP client not available');
            }
            
            const response = await window.http.get('/api/analytics/dashboard', {
                params: { period: analyticsPeriod }
            });
            
            analyticsData = response.data || response;
            renderAnalytics();
            
        } catch (error) {
            console.error('Failed to load analytics:', error);
            dashboard.innerHTML = `
                <div class="error-message">
                    <p>Failed to load analytics</p>
                    <small>${error.message}</small>
                </div>
            `;
        }
    }
    
    /**
     * Render analytics dashboard
     */
    function renderAnalytics() {
        const summary = analyticsData.summary || {};
        
        // Update stat cards
        document.getElementById('total-prompts').textContent = summary.total_prompts || 0;
        document.getElementById('total-projects').textContent = summary.total_projects || 0;
        document.getElementById('total-uses').textContent = summary.total_uses || 0;
        document.getElementById('avg-rating').textContent = (summary.avg_rating || 0).toFixed(1);
        
        // Render top prompts
        renderTopPrompts(analyticsData.topPrompts || []);
        
        // Render category breakdown
        renderCategoryBreakdown(analyticsData.categories || {});
        
        // Render activity
        renderActivity(analyticsData.activity || []);
    }
    
    /**
     * Render top prompts list
     */
    function renderTopPrompts(prompts) {
        const topList = document.getElementById('top-prompts');
        
        if (!prompts || prompts.length === 0) {
            topList.innerHTML = '<p class="no-data">No data available</p>';
            return;
        }
        
        topList.innerHTML = prompts.slice(0, 5).map((prompt, idx) => `
            <div class="top-item">
                <span class="rank">#${idx + 1}</span>
                <div class="item-info">
                    <h4>${escapeHtml(prompt.name || 'Untitled')}</h4>
                    <small>${prompt.uses || 0} uses</small>
                </div>
                <span class="item-value">${prompt.rating ? prompt.rating.toFixed(1) : 'N/A'} ⭐</span>
            </div>
        `).join('');
    }
    
    /**
     * Render category breakdown
     */
    function renderCategoryBreakdown(categories) {
        const breakdown = document.getElementById('category-breakdown');
        
        const entries = Object.entries(categories).filter(([_, count]) => count > 0);
        
        if (entries.length === 0) {
            breakdown.innerHTML = '<p class="no-data">No data available</p>';
            return;
        }
        
        const total = entries.reduce((sum, [_, count]) => sum + count, 0);
        
        breakdown.innerHTML = entries.map(([category, count]) => {
            const percentage = (count / total * 100).toFixed(0);
            return `
                <div class="category-item">
                    <div class="category-bar">
                        <div class="bar-fill" style="width: ${percentage}%"></div>
                    </div>
                    <div class="category-info">
                        <span class="category-name">${escapeHtml(category)}</span>
                        <span class="category-count">${count} (${percentage}%)</span>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    /**
     * Render activity log
     */
    function renderActivity(activity) {
        const activityList = document.getElementById('activity-list');
        
        if (!activity || activity.length === 0) {
            activityList.innerHTML = '<p class="no-data">No recent activity</p>';
            return;
        }
        
        activityList.innerHTML = activity.slice(0, 10).map(item => {
            const emoji = getActivityEmoji(item.action);
            return `
                <div class="activity-item">
                    <span class="activity-emoji">${emoji}</span>
                    <div class="activity-content">
                        <p>${escapeHtml(item.description || 'Unknown action')}</p>
                        <small>${formatTime(item.timestamp)}</small>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    /**
     * Get emoji for activity
     */
    function getActivityEmoji(action) {
        const map = {
            'create': '✨',
            'edit': '✏️',
            'delete': '🗑️',
            'use': '⚡',
            'share': '📤',
            'rate': '⭐'
        };
        return map[action] || '📌';
    }
    
    /**
     * Format time
     */
    function formatTime(timestamp) {
        if (!timestamp) return '';
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);
        
        if (minutes < 1) return 'just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        if (days < 7) return `${days}d ago`;
        
        return date.toLocaleDateString();
    }
    
    /**
     * Export statistics
     */
    async function exportStats() {
        try {
            const csv = `PANDORA Analytics Report
Generated: ${new Date().toISOString()}

Summary
-------
Total Prompts: ${analyticsData.summary?.total_prompts || 0}
Total Projects: ${analyticsData.summary?.total_projects || 0}
Total Uses: ${analyticsData.summary?.total_uses || 0}
Average Rating: ${(analyticsData.summary?.avg_rating || 0).toFixed(1)}

Top Prompts
-----------
${(analyticsData.topPrompts || []).map((p, i) => 
    `${i + 1}. ${p.name} (${p.uses} uses, ${p.rating?.toFixed(1) || 'N/A'} ⭐)`
).join('\n')}

Categories
----------
${Object.entries(analyticsData.categories || {}).map(([cat, count]) => 
    `${cat}: ${count}`
).join('\n')}
`;
            
            // Download CSV
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `PANDORA_analytics_${new Date().getTime()}.csv`;
            link.click();
            
            showToast('Analytics exported successfully!');
        } catch (error) {
            console.error('Export failed:', error);
            showToast('Failed to export analytics');
        }
    }
    
    // ==================== EVENT LISTENERS ====================
    
    document.getElementById('analytics-period').addEventListener('change', (e) => {
        analyticsPeriod = e.target.value;
        loadAnalytics();
    });
    
    document.getElementById('btn-export-stats').addEventListener('click', exportStats);
    
    // ==================== INITIAL LOAD ====================
    loadAnalytics();
    
    return container;
}

/**
 * Utility: Escape HTML
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return (text || '').replace(/[&<>"']/g, m => map[m]);
}

/**
 * Utility: Show toast
 */
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}
