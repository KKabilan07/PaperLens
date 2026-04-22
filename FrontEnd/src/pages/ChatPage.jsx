import React, { useState, useEffect, useRef } from 'react'
import '../Components/Main/Main.css'
import { useAuth } from '../context/AuthContext'
import { supabase } from '../lib/supabase'
import { assets } from '../assets/assets'
import { uploadPaper, getPapers, deletePaper } from '../utils/paperService'
import { askQuestion, getChatHistory } from '../utils/chatService'

const ChatPage = () => {
  const { user, loading } = useAuth()
  
  // Paper management state
  const [papers, setPapers] = useState([])
  const [selectedPaper, setSelectedPaper] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState('')
  
  // Chat state
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [loading_chat, setLoadingChat] = useState(false)
  const [chatHistory, setChatHistory] = useState([])
  const [error, setError] = useState('')
  
  // File upload state
  const fileInputRef = useRef(null)

  const handleLogout = async () => {
    try {
      await supabase.auth.signOut()
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  // Load papers on component mount
  useEffect(() => {
    if (user) {
      loadPapers()
    }
  }, [user])

  // Load chat history when paper is selected
  useEffect(() => {
    if (selectedPaper) {
      loadChatHistory(selectedPaper.id)
    }
  }, [selectedPaper])

  const loadPapers = async () => {
    try {
      const data = await getPapers()
      setPapers(data || [])
    } catch (err) {
      setError('Failed to load papers')
      console.error('Error loading papers:', err)
    }
  }

  const loadChatHistory = async (paperId) => {
    try {
      const history = await getChatHistory(paperId)
      setChatHistory(history || [])
      // Create separate messages for user questions and bot answers
      const messages = []
      history?.forEach((chat, index) => {
        messages.push({
          id: `${chat.id}-user`,
          type: 'user',
          text: chat.question,
          timestamp: chat.created_at
        })
        messages.push({
          id: `${chat.id}-bot`,
          type: 'bot',
          text: chat.answer,
          provider: chat.provider_used || 'Unknown',
          sources: chat.sources || [],
          timestamp: chat.created_at
        })
      })
      setMessages(messages)
    } catch (err) {
      console.error('Error loading chat history:', err)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    setUploadProgress('Uploading...')
    
    try {
      const title = file.name.replace('.pdf', '')
      const response = await uploadPaper(file, title)
      
      console.log('Upload response:', response)
      
      setUploadProgress(`✓ Paper uploaded! Processing embeddings...`)
      
      // Reload papers list
      await loadPapers()
      
      // Select the newly uploaded paper (response has paper_id, not id)
      if (response?.paper_id) {
        setSelectedPaper({
          id: response.paper_id,
          title: response.title,
          word_count: response.word_count,
          page_count: response.sections_count
        })
      }
      
      setUploadProgress('')
      setError('')
    } catch (err) {
      setError(`Upload failed: ${err.message}`)
      setUploadProgress('')
      console.error('Error uploading paper:', err)
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleDeletePaper = async (paperId, e) => {
    e.stopPropagation()
    
    if (!window.confirm('Are you sure you want to delete this paper?')) return
    
    try {
      await deletePaper(paperId)
      setPapers(papers.filter(p => p.id !== paperId))
      
      if (selectedPaper?.id === paperId) {
        setSelectedPaper(null)
        setMessages([])
        setChatHistory([])
      }
      
      setError('')
    } catch (err) {
      setError(`Failed to delete paper: ${err.message}`)
      console.error('Error deleting paper:', err)
    }
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    
    if (!inputValue.trim() || !selectedPaper) {
      setError('Please select a paper and enter a question')
      return
    }

    const userQuestion = inputValue
    setInputValue('')
    setLoadingChat(true)
    setError('')

    try {
      // Add user message immediately
      setMessages([
        ...messages,
        {
          id: Date.now(),
          type: 'user',
          text: userQuestion,
          timestamp: new Date().toISOString()
        }
      ])

      // Get RAG response
      const response = await askQuestion(selectedPaper.id, userQuestion)

      // Add bot response
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          type: 'bot',
          text: response.answer,
          provider: response.provider_used || 'Unknown',
          sources: response.sources || [],
          timestamp: new Date().toISOString()
        }
      ])

      // Reload chat history to stay in sync
      await loadChatHistory(selectedPaper.id)

    } catch (err) {
      setError(`Failed to get response: ${err.message}`)
      console.error('Error asking question:', err)
      
      // Remove the user message if request failed
      setMessages(prev => prev.slice(0, -1))
    } finally {
      setLoadingChat(false)
    }
  }

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        fontSize: '18px',
        color: '#666'
      }}>
        Loading...
      </div>
    )
  }

  return (
    <div className="main">
      <div className="nav">
        <div className="nav-logo">
          <img src={assets.logo} alt="PaperLens" style={{ height: '32px', width: 'auto' }} />
        </div>
        <div className="user-info">
          <span>{user.email}</span>
          <button className="user-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      <div className="main-container-full">
        {/* Sidebar with papers list */}
        <div className="sidebar-papers">
          <div className="papers-header">
            <h3>My Papers</h3>
            <button 
              className="btn-upload"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
            >
              {uploading ? '⏳' : '➕ Upload'}
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
              disabled={uploading}
            />
          </div>

          {uploadProgress && (
            <div className="upload-status">
              {uploadProgress}
            </div>
          )}

          <div className="papers-list">
            {papers.length === 0 ? (
              <p className="no-papers">No papers yet. Upload one to get started!</p>
            ) : (
              papers.map(paper => (
                <div
                  key={paper.id}
                  className={`paper-item ${selectedPaper?.id === paper.id ? 'active' : ''}`}
                  onClick={() => {
                    setSelectedPaper(paper)
                    setMessages([])
                  }}
                >
                  <div className="paper-info">
                    <p className="paper-title">{paper.title}</p>
                    <p className="paper-meta">
                      {paper.page_count || '?'} pages · {paper.word_count || '?'} words
                    </p>
                  </div>
                  <button
                    className="btn-delete"
                    onClick={(e) => handleDeletePaper(paper.id, e)}
                  >
                    🗑️
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Main chat area */}
        <div className="chat-area">
          {!selectedPaper ? (
            <div className="no-paper-selected">
              <div className="greet">
                <p><span>Hello!</span></p>
                <p>Select a paper or upload one to get started</p>
              </div>
            </div>
          ) : (
            <>
              <div className="chat-header">
                <h2>{selectedPaper.title}</h2>
              </div>

              <div className="messages-container">
                {messages.length === 0 ? (
                  <div className="no-messages">
                    <p>Start by asking a question about this paper</p>
                  </div>
                ) : (
                  messages.map(msg => (
                    <div key={msg.id} className={`message ${msg.type}`}>
                      <div className="message-content">
                        {msg.type === 'user' ? (
                          <p>{msg.text}</p>
                        ) : (
                          <>
                            <p>{msg.text}</p>
                            {msg.provider && (
                              <span className="provider-badge">
                                Answered by: {msg.provider}
                              </span>
                            )}
                            {msg.sources && msg.sources.length > 0 && (
                              <div className="sources">
                                <strong>Sources:</strong>
                                {msg.sources.map((source, idx) => (
                                  <p key={idx} className="source">{source}</p>
                                ))}
                              </div>
                            )}
                          </>
                        )}
                      </div>
                    </div>
                  ))
                )}
                {loading_chat && (
                  <div className="message bot loading">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                )}
              </div>

              {error && (
                <div className="error-message">
                  {error}
                </div>
              )}

              <form onSubmit={handleSendMessage} className="chat-input-form">
                <div className="search-box">
                  <input
                    type="text"
                    placeholder="Ask a question about this paper..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    disabled={loading_chat}
                  />
                  <button
                    type="submit"
                    disabled={loading_chat || !inputValue.trim()}
                    className="btn-send"
                  >
                    <img src={assets.send_icon} alt="send" />
                  </button>
                </div>
              </form>

              <p className="bottom-info">
                PaperLens uses RAG (Retrieval Augmented Generation) to answer questions based on paper content. Results are verified with AI providers (Gemini/Claude/Groq).
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default ChatPage
