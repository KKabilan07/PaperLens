/**
 * Paper API Service
 * Handles all paper-related API calls
 */

import { apiGet, apiPost, apiDelete } from './api'

/**
 * Get all papers for current user
 * @returns {Promise<Array>} List of papers
 */
export const getPapers = async () => {
  try {
    const response = await apiGet('/papers')
    return response
  } catch (error) {
    console.error('Error fetching papers:', error)
    throw error
  }
}

/**
 * Upload a new paper
 * @param {File} file - PDF file to upload
 * @param {string} title - Paper title
 * @returns {Promise<Object>} Upload response
 */
export const uploadPaper = async (file, title = '') => {
  try {
    // Import supabase here to get the session
    const { supabase } = await import('../lib/supabase')
    const { data, error: sessionError } = await supabase.auth.getSession()
    
    if (sessionError || !data?.session) {
      console.error('Session error:', sessionError)
      throw new Error('No session found. Please log in.')
    }

    const token = data.session.access_token
    console.log('Upload token obtained:', token.substring(0, 20) + '...')

    const formData = new FormData()
    formData.append('file', file)
    if (title) {
      formData.append('title', title)
    }

    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    console.log('Uploading to:', `${API_BASE_URL}/api/v1/papers/upload`)
    
    const response = await fetch(
      `${API_BASE_URL}/api/v1/papers/upload`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      }
    )

    console.log('Upload response status:', response.status)

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Upload error response:', errorText)
      try {
        const error = JSON.parse(errorText)
        throw new Error(error.message || `Upload failed: ${response.status}`)
      } catch (e) {
        throw new Error(`Upload failed: ${response.status} - ${errorText}`)
      }
    }

    const result = await response.json()
    console.log('Upload successful:', result)
    return result
  } catch (error) {
    console.error('Error uploading paper:', error)
    throw error
  }
}

/**
 * Get paper details with sections
 * @param {string} paperId - Paper ID
 * @returns {Promise<Object>} Paper with sections
 */
export const getPaperDetails = async (paperId) => {
  try {
    const response = await apiGet(`/papers/${paperId}`)
    return response
  } catch (error) {
    console.error('Error fetching paper details:', error)
    throw error
  }
}

/**
 * Get paper sections
 * @param {string} paperId - Paper ID
 * @returns {Promise<Array>} List of sections
 */
export const getPaperSections = async (paperId) => {
  try {
    const response = await apiGet(`/papers/${paperId}/sections`)
    return response
  } catch (error) {
    console.error('Error fetching sections:', error)
    throw error
  }
}

/**
 * Delete a paper
 * @param {string} paperId - Paper ID
 * @returns {Promise<Object>} Delete response
 */
export const deletePaper = async (paperId) => {
  try {
    const response = await apiDelete(`/papers/${paperId}`)
    return response
  } catch (error) {
    console.error('Error deleting paper:', error)
    throw error
  }
}

/**
 * Compare two papers
 * @param {string} paperId - First paper ID
 * @param {string} comparePaperId - Second paper ID
 * @param {string} question - Comparison question
 * @returns {Promise<Object>} Comparison result
 */
export const comparePapers = async (paperId, comparePaperId, question) => {
  try {
    const response = await apiPost(`/papers/${paperId}/compare`, {
      compare_with: comparePaperId,
      question: question
    })
    return response
  } catch (error) {
    console.error('Error comparing papers:', error)
    throw error
  }
}

export default {
  getPapers,
  uploadPaper,
  getPaperDetails,
  getPaperSections,
  deletePaper,
  comparePapers
}
