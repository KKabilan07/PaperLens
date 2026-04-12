import { supabase } from '../lib/supabase'

// Base URL for your backend API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Make authenticated API call with JWT token from Supabase
 * @param {string} endpoint - API endpoint path (e.g., '/api/papers')
 * @param {object} options - fetch options
 * @returns {Promise} API response
 */
export const authenticatedFetch = async (endpoint, options = {}) => {
  try {
    // Get current JWT token
    const { data: { session } } = await supabase.auth.getSession()
    
    if (!session) {
      throw new Error('No session found. Please log in.')
    }

    const token = session.access_token

    // Set up headers with Authorization token
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    }

    // Make the request with /api/v1 prefix
    const response = await fetch(`${API_BASE_URL}/api/v1${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.message || `API Error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Authenticated fetch error:', error)
    throw error
  }
}

/**
 * GET request helper
 */
export const apiGet = (endpoint) => {
  return authenticatedFetch(endpoint, {
    method: 'GET',
  })
}

/**
 * POST request helper
 */
export const apiPost = (endpoint, data) => {
  return authenticatedFetch(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

/**
 * PUT request helper
 */
export const apiPut = (endpoint, data) => {
  return authenticatedFetch(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

/**
 * DELETE request helper
 */
export const apiDelete = (endpoint) => {
  return authenticatedFetch(endpoint, {
    method: 'DELETE',
  })
}
