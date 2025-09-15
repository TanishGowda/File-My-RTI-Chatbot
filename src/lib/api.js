// API client for Python backend
import { supabase } from './supabase'

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    
    // Get auth token from Supabase
    const token = await this.getAuthToken()
    console.log('Making API request to:', url, 'with token:', token ? 'present' : 'missing')
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers
      },
      ...options
    }
    
    // If no token, add a default test token for development
    if (!token) {
      config.headers.Authorization = 'Bearer test-token'
      console.log('Using test token for development')
    }

    try {
      console.log('Sending request with config:', config)
      console.log('Request URL:', url)
      console.log('Request headers:', config.headers)
      
      // Add timeout to prevent hanging (increased for AI responses)
      const controller = new AbortController()
      const timeoutId = setTimeout(() => {
        console.log('Request timed out after 30 seconds')
        controller.abort()
      }, 30000) // 30 second timeout for AI responses
      
      const response = await fetch(url, {
        ...config,
        signal: controller.signal
      })
      
      clearTimeout(timeoutId)
      console.log('API response status:', response.status)
      console.log('API response headers:', response.headers)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        console.error('API error response:', errorData)
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
      }
      
      const responseData = await response.json()
      console.log('API response data:', responseData)
      return responseData
    } catch (error) {
      console.error('API request error:', error)
      
      // Handle specific error types
      if (error.name === 'AbortError') {
        throw new Error('Request timed out. Please try again.')
      }
      
      throw error
    }
  }

  async getAuthToken() {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      console.log('Auth session:', session)
      return session?.access_token || null
    } catch (error) {
      console.error('Error getting auth token:', error)
      return null
    }
  }

  // Auth endpoints
  async verifyToken() {
    return this.request('/auth/verify', { method: 'GET' })
  }

  async refreshToken() {
    return this.request('/auth/refresh', { method: 'POST' })
  }

  async logout() {
    return this.request('/auth/logout', { method: 'POST' })
  }

  // Profile endpoints
  async getProfile() {
    return this.request('/profiles/me', { method: 'GET' })
  }

  async updateProfile(updates) {
    return this.request('/profiles/me', {
      method: 'PUT',
      body: JSON.stringify(updates)
    })
  }

  // Chat endpoints
  async getConversations() {
    try {
      console.log('API Client: Getting conversations...')
      const result = await this.request('/chat/conversations', { method: 'GET' })
      console.log('API Client: Got response:', result)
      return result
    } catch (error) {
      console.error('API Client: Error getting conversations:', error)
      throw error
    }
  }

  async createConversation(title) {
    return this.request('/chat/conversations', {
      method: 'POST',
      body: JSON.stringify({ title })
    })
  }

  async getMessages(conversationId) {
    return this.request(`/chat/conversations/${conversationId}/messages`, { method: 'GET' })
  }

  async sendMessage(message, conversationId = null) {
    return this.request('/chat/send', {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        user_id: "test-user-123" // Temporary user ID for development
      })
    })
  }

  async deleteConversation(conversationId) {
    return this.request(`/chat/conversations/${conversationId}`, { method: 'DELETE' })
  }

  // RTI endpoints
  async generateRTIDraft(message) {
    return this.request('/rti/generate-draft', {
      method: 'POST',
      body: JSON.stringify({ message })
    })
  }

  async getRTIDrafts() {
    return this.request('/rti/drafts', { method: 'GET' })
  }

  async getRTIDraft(draftId) {
    return this.request(`/rti/drafts/${draftId}`, { method: 'GET' })
  }

  async updateRTIDraft(draftId, updates) {
    return this.request(`/rti/drafts/${draftId}`, {
      method: 'PUT',
      body: JSON.stringify(updates)
    })
  }

  async deleteRTIDraft(draftId) {
    return this.request(`/rti/drafts/${draftId}`, { method: 'DELETE' })
  }

  async fileRTI(rtiDraftId, pioEmail = null, pioAddress = null) {
    return this.request('/rti/file', {
      method: 'POST',
      body: JSON.stringify({
        rti_draft_id: rtiDraftId,
        pio_email: pioEmail,
        pio_address: pioAddress
      })
    })
  }

  async getRTIFilings() {
    return this.request('/rti/filings', { method: 'GET' })
  }

  async getRTIFiling(filingId) {
    return this.request(`/rti/filings/${filingId}`, { method: 'GET' })
  }
}

// Create and export API client instance
export const apiClient = new ApiClient()
