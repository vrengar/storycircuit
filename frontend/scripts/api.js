// API Client for StoryCircuit

const API_BASE_URL = '/api/v1';

class APIClient {
    /**
     * Generate content
     */
    async generateContent(data) {
        return this._request('POST', '/content/generate', data);
    }

    /**
     * Get content history
     */
    async getContentHistory(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = `/content/history${queryString ? '?' + queryString : ''}`;
        return this._request('GET', url);
    }

    /**
     * Get content by ID
     */
    async getContentById(contentId) {
        return this._request('GET', `/content/${contentId}`);
    }

    /**
     * Delete content
     */
    async deleteContent(contentId) {
        return this._request('DELETE', `/content/${contentId}`);
    }

    /**
     * Export content
     */
    async exportContent(contentId, format = 'markdown', platform = 'all') {
        const url = `${API_BASE_URL}/content/${contentId}/export?format=${format}&platform=${platform}`;
        
        try {
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`Export failed: ${response.statusText}`);
            }
            
            // Get filename from headers
            const contentDisposition = response.headers.get('content-disposition');
            let filename = `storycircuit-export.${format === 'markdown' ? 'md' : 'json'}`;
            
            if (contentDisposition) {
                const matches = /filename="?([^"]+)"?/.exec(contentDisposition);
                if (matches && matches[1]) {
                    filename = matches[1];
                }
            }
            
            // Get blob
            const blob = await response.blob();
            
            return { blob, filename };
        } catch (error) {
            console.error('Export error:', error);
            throw error;
        }
    }

    /**
     * Health check
     */
    async healthCheck() {
        return this._request('GET', '/health');
    }

    /**
     * Internal request method
     */
    async _request(method, endpoint, data = null) {
        const url = `${API_BASE_URL}${endpoint}`;
        
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, options);
            
            // Handle different response types
            if (response.status === 204) {
                // No content
                return null;
            }
            
            const responseData = await response.json();
            
            if (!response.ok) {
                // API error
                throw new Error(responseData.detail || 'API request failed');
            }
            
            return responseData;
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }
}

// Create singleton instance
const apiClient = new APIClient();
