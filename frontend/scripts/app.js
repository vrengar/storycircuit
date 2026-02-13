// StoryCircuit Application Logic

// State
let currentContentId = null;
let currentPage = 0;
const historyLimit = 10;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeGenerateForm();
    initializeHistoryTab();
});

// Tab Navigation
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            
            // Update active states
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            button.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            // Load history when switching to history tab
            if (tabName === 'history') {
                loadHistory();
            }
        });
    });
}

// Generate Form
function initializeGenerateForm() {
    const form = document.getElementById('generate-form');
    const generateBtn = document.getElementById('generate-btn');
    const btnText = generateBtn.querySelector('.btn-text');
    const btnLoading = generateBtn.querySelector('.btn-loading');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(form);
        const topic = formData.get('topic');
        const platforms = formData.getAll('platforms');
        const audience = formData.get('audience');
        const additionalContext = formData.get('additional_context');
        
        // Validation
        if (!topic || topic.trim().length < 3) {
            showToast('Please enter a valid topic (at least 3 characters)', 'error');
            return;
        }
        
        if (platforms.length === 0) {
            showToast('Please select at least one platform', 'error');
            return;
        }
        
        // Disable form
        generateBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        
        try {
            // Call API
            const result = await apiClient.generateContent({
                topic: topic.trim(),
                platforms: platforms,
                audience: audience?.trim() || null,
                additional_context: additionalContext?.trim() || null
            });
            
            // Store content ID
            currentContentId = result.id;
            
            // Display results
            displayResults(result);
            
            // Show success message
            showToast('Content generated successfully!', 'success');
            
            // Scroll to results
            document.getElementById('results-section').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
            
        } catch (error) {
            console.error('Generation error:', error);
            showToast(error.message || 'Failed to generate content. Please try again.', 'error');
        } finally {
            // Re-enable form
            generateBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
        }
    });
    
    // Export buttons
    document.getElementById('export-md-btn').addEventListener('click', () => {
        if (currentContentId) {
            exportContent('markdown');
        }
    });
    
    document.getElementById('export-json-btn').addEventListener('click', () => {
        if (currentContentId) {
            exportContent('json');
        }
    });
}

// Display Results
function displayResults(result) {
    const resultsSection = document.getElementById('results-section');
    const resultsContainer = document.getElementById('results-container');
    
    let html = '';
    
    // Plan Section
    if (result.content.plan) {
        const plan = result.content.plan;
        html += `
            <div class="result-section">
                <h3>Content Plan</h3>
                <div class="result-content">
                    <div class="result-label">Hook:</div>
                    <div class="result-text">${escapeHtml(plan.hook || 'N/A')}</div>
                </div>
                <div class="result-content">
                    <div class="result-label">Narrative Frame:</div>
                    <div class="result-text">${escapeHtml(plan.narrative_frame || plan.narrativeFrame || 'N/A')}</div>
                </div>
                <div class="result-content">
                    <div class="result-label">Key Points:</div>
                    <div class="result-text">${formatKeyPoints(plan.key_points || plan.keyPoints)}</div>
                </div>
                <div class="result-content">
                    <div class="result-label">Example:</div>
                    <div class="result-text">${escapeHtml(plan.example || 'N/A')}</div>
                </div>
                <div class="result-content">
                    <div class="result-label">Call-to-Action:</div>
                    <div class="result-text">${escapeHtml(plan.cta || 'N/A')}</div>
                </div>
            </div>
        `;
    }
    
    // Platform Outputs
    if (result.content.outputs) {
        const outputs = result.content.outputs;
        
        for (const [platform, output] of Object.entries(outputs)) {
            // Skip null outputs (platforms not selected)
            if (output === null || output === undefined) {
                continue;
            }
            
            html += `
                <div class="result-section">
                    <h3>${capitalize(platform)} Output</h3>
                    ${formatPlatformOutput(platform, output)}
                </div>
            `;
        }
    }
    
    // Notes
    if (result.content.notes) {
        html += `
            <div class="result-section">
                <h3>Notes</h3>
                <div class="result-content">
                    <div class="result-text">${escapeHtml(result.content.notes)}</div>
                </div>
            </div>
        `;
    }
    
    resultsContainer.innerHTML = html;
    resultsSection.style.display = 'block';
}

// Format platform output
function formatPlatformOutput(platform, output) {
    let html = '';
    
    // Safety check for null/undefined output
    if (!output) {
        return '<div class="result-content"><div class="result-text">No content generated</div></div>';
    }
    
    if (platform === 'twitter' && output.tweets) {
        html += '<div class="result-content">';
        html += `<div class="result-label">Thread Structure: ${escapeHtml(output.thread_structure || output.threadStructure || 'Unknown')}</div>`;
        html += '<div class="result-label" style="margin-top: 1rem;">Tweets:</div>';
        output.tweets.forEach(tweet => {
            html += `<div style="margin: 1rem 0; padding: 1rem; background: #f9f9f9; border-left: 3px solid var(--primary-color);">`;
            html += `<strong>Tweet ${tweet.order}:</strong><br>`;
            html += `${escapeHtml(tweet.content)}<br>`;
            html += `<small style="color: var(--text-secondary);">(${tweet.character_count || tweet.characterCount} characters)</small>`;
            html += `</div>`;
        });
        html += '</div>';
    } else {
        // Generic output display
        html += '<div class="result-content">';
        html += `<pre class="result-text">${escapeHtml(JSON.stringify(output, null, 2))}</pre>`;
        html += '</div>';
    }
    
    return html;
}

// History Tab
function initializeHistoryTab() {
    document.getElementById('refresh-history-btn').addEventListener('click', () => {
        currentPage = 0;
        loadHistory();
    });
}

async function loadHistory() {
    const loadingEl = document.getElementById('history-loading');
    const containerEl = document.getElementById('history-container');
    
    loadingEl.style.display = 'block';
    containerEl.innerHTML = '';
    
    try {
        const result = await apiClient.getContentHistory({
            limit: historyLimit,
            offset: currentPage * historyLimit
        });
        
        if (result.items.length === 0) {
            containerEl.innerHTML = '<p style="text-align: center; color: var(--text-secondary); padding: 2rem;">No content history found. Generate some content to get started!</p>';
        } else {
            displayHistory(result.items);
            displayPagination(result.pagination);
        }
    } catch (error) {
        console.error('History load error:', error);
        showToast('Failed to load history', 'error');
    } finally {
        loadingEl.style.display = 'none';
    }
}

function displayHistory(items) {
    const container = document.getElementById('history-container');
    
    const html = items.map(item => `
        <div class="history-item" onclick="viewHistoryItem('${item.id}')">
            <div class="history-item-header">
                <div class="history-item-topic">${escapeHtml(item.topic)}</div>
                <div class="history-item-date">${formatDate(item.generated_at)}</div>
            </div>
            <div class="history-item-platforms">
                ${item.platforms.map(p => `<span class="platform-badge">${capitalize(p)}</span>`).join('')}
            </div>
            <div class="history-item-summary">${escapeHtml(item.summary)}</div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

function displayPagination(pagination) {
    const container = document.getElementById('history-pagination');
    
    const totalPages = Math.ceil(pagination.total / pagination.limit);
    
    let html = '';
    
    // Previous button
    html += `<button ${currentPage === 0 ? 'disabled' : ''} onclick="changePage(${currentPage - 1})">Previous</button>`;
    
    // Page numbers (show max 5)
    const startPage = Math.max(0, currentPage - 2);
    const endPage = Math.min(totalPages, startPage + 5);
    
    for (let i = startPage; i < endPage; i++) {
        html += `<button class="${i === currentPage ? 'active' : ''}" onclick="changePage(${i})">${i + 1}</button>`;
    }
    
    // Next button
    html += `<button ${!pagination.has_more ? 'disabled' : ''} onclick="changePage(${currentPage + 1})">Next</button>`;
    
    container.innerHTML = html;
}

function changePage(page) {
    currentPage = page;
    loadHistory();
}

async function viewHistoryItem(contentId) {
    try {
        const result = await apiClient.getContentById(contentId);
        currentContentId = contentId;
        
        // Switch to generate tab and show results
        document.querySelector('.tab-button[data-tab="generate"]').click();
        
        // Display results
        displayResults({
            id: result.id,
            status: 'success',
            content: result.content,
            metadata: result.metadata
        });
        
        showToast('Content loaded from history', 'success');
    } catch (error) {
        console.error('View history error:', error);
        showToast('Failed to load content', 'error');
    }
}

// Export Content
async function exportContent(format) {
    if (!currentContentId) {
        showToast('No content to export', 'error');
        return;
    }
    
    try {
        const { blob, filename } = await apiClient.exportContent(currentContentId, format);
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showToast(`Content exported as ${format}`, 'success');
    } catch (error) {
        console.error('Export error:', error);
        showToast('Failed to export content', 'error');
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatKeyPoints(points) {
    if (!points || !Array.isArray(points)) return 'N/A';
    return '<ul style="margin: 0.5rem 0; padding-left: 1.5rem;">' + 
           points.map(p => `<li>${escapeHtml(p)}</li>`).join('') + 
           '</ul>';
}
