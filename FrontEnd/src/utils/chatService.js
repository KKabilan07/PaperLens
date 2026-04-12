/**
 * Chat API Service
 * Handles all chat and RAG-related API calls
 */

import { apiGet, apiPost } from './api'

/**
 * Ask a question about a paper
 * Uses RAG pipeline for semantic search + LLM response
 * @param {string} paperId - Paper ID
 * @param {string} question - User's question
 * @returns {Promise<Object>} Question response with answer and chat ID
 */
export const askQuestion = async (paperId, question) => {
  try {
    const response = await apiPost('/chat', {
      paper_id: paperId,
      question: question
    })
    return response
  } catch (error) {
    console.error('Error asking question:', error)
    throw error
  }
}

/**
 * Get chat history for a paper
 * @param {string} paperId - Paper ID
 * @returns {Promise<Array>} Chat history
 */
export const getChatHistory = async (paperId) => {
  try {
    const response = await apiGet(`/chat/history/${paperId}`)
    return response
  } catch (error) {
    console.error('Error fetching chat history:', error)
    throw error
  }
}

/**
 * Get all chats for current user related to a paper
 * @param {string} paperId - Paper ID
 * @returns {Promise<Object>} User chats
 */
export const getUserChats = async (paperId) => {
  try {
    const response = await apiGet(`/chat/user/${paperId}`)
    return response
  } catch (error) {
    console.error('Error fetching user chats:', error)
    throw error
  }
}

export default {
  askQuestion,
  getChatHistory,
  getUserChats
}
