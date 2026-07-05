import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Search, 
  MessageSquare, 
  BookOpen, 
  FileText, 
  CheckSquare, 
  Square,
  Sparkles,
  Send,
  HelpCircle,
  TrendingUp
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import Sidebar from '../Components/Sidebar'
import { getPapers } from '../utils/paperService'
import { apiGet, apiPost } from '../utils/api'
import './SearchPage.css'

const SearchPage = () => {
  const navigate = useNavigate()
  
  const [papers, setPapers] = useState([])
  const [selectedPaperIds, setSelectedPaperIds] = useState([])
  
  // Search state
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [searchLoading, setSearchLoading] = useState(false)
  
  // Multi-chat state
  const [chatMode, setChatMode] = useState('semantic') // semantic, multichat
  const [chatQuestion, setChatQuestion] = useState('')
  const [chatMessages, setChatMessages] = useState([])
  const [chatLoading, setChatLoading] = useState(false)
  
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const chatBottomRef = useRef(null)

  useEffect(() => {
    loadPapers()
  }, [])

  useEffect(() => {
    if (chatBottomRef.current) {
      chatBottomRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [chatMessages])

  const loadPapers = async () => {
    try {
      setLoading(true)
      const data = await getPapers()
      setPapers(data || [])
    } catch (err) {
      console.error(err)
      setError('Could not load paper list.')
    } finally {
      setLoading(false)
    }
  }

  const handleSearchSubmit = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return
    
    setSearchLoading(true)
    setError('')
    setSearchResults([])
    
    try {
      const results = await apiGet(`/search/semantic-search?query=${encodeURIComponent(searchQuery)}`)
      setSearchResults(results || [])
    } catch (err) {
      console.error(err)
      setError('Semantic search failed. Verify your backend or model settings.')
    } finally {
      setSearchLoading(false)
    }
  }

  const togglePaperSelection = (id) => {
    if (selectedPaperIds.includes(id)) {
      setSelectedPaperIds(selectedPaperIds.filter(pid => pid !== id))
    } else {
      setSelectedPaperIds([...selectedPaperIds, id])
    }
  }

  const selectAllPapers = () => {
    if (selectedPaperIds.length === papers.length) {
      setSelectedPaperIds([])
    } else {
      setSelectedPaperIds(papers.map(p => p.id))
    }
  }

  const handleMultiChatSubmit = async (e) => {
    e.preventDefault()
    if (!chatQuestion.trim() || selectedPaperIds.length === 0 || chatLoading) return
    
    const questionText = chatQuestion
    setChatQuestion('')
    setChatLoading(true)
    setError('')
    
    const userMsgId = Date.now()
    const thinkingMsgId = Date.now() + 1
    
    setChatMessages(prev => [
      ...prev,
      {
        id: userMsgId,
        type: 'user',
        text: questionText
      },
      {
        id: thinkingMsgId,
        type: 'bot',
        text: 'Thinking across multiple papers...',
        isThinking: true
      }
    ])
    
    try {
      const response = await apiPost('/papers/multi-chat', {
        paper_ids: selectedPaperIds,
        question: questionText
      })
      
      const botMsgId = Date.now() + 2
      setChatMessages(prev => [
        ...prev.filter(m => m.id !== thinkingMsgId),
        {
          id: botMsgId,
          type: 'bot',
          text: response.answer,
          provider: response.provider_used || 'Gemini 2.5 Flash',
          sources: response.sources || []
        }
      ])
    } catch (err) {
      console.error(err)
      setError(`Multi-paper chat failed: ${err.message}`)
      setChatMessages(prev => prev.filter(m => m.id !== thinkingMsgId))
    } finally {
      setChatLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="search-layout">
        <Sidebar />
        <div className="search-loading">
          <div className="spinner"></div>
          <p>Analyzing library corpus...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="search-layout">
      <Sidebar />
      
      <main className="search-main">
        <header className="search-header">
          <div className="header-title">
            <h1>Semantic Search & Cross-Chat</h1>
            <p>Query concepts semantically or converse with multiple papers simultaneously.</p>
          </div>
          
          <div className="mode-toggle-pills">
            <button 
              className={`mode-pill ${chatMode === 'semantic' ? 'active' : ''}`}
              onClick={() => setChatMode('semantic')}
            >
              <Search size={16} />
              <span>Semantic Search</span>
            </button>
            <button 
              className={`mode-pill ${chatMode === 'multichat' ? 'active' : ''}`}
              onClick={() => setChatMode('multichat')}
            >
              <MessageSquare size={16} />
              <span>Multi-Paper Chat</span>
            </button>
          </div>
        </header>

        {error && (
          <div className="error-banner">
            <span>{error}</span>
          </div>
        )}

        {/* SEMANTIC SEARCH MODE */}
        {chatMode === 'semantic' && (
          <div className="search-mode-container animate-fade-in">
            <form onSubmit={handleSearchSubmit} className="search-box-row">
              <input
                type="text"
                placeholder="Enter query (e.g. 'cable driven robots' or 'reinforcement learning methodology')..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                disabled={searchLoading}
              />
              <button type="submit" disabled={searchLoading || !searchQuery.trim()} className="btn-search-trigger">
                {searchLoading ? 'Searching...' : 'Search'}
              </button>
            </form>

            <div className="results-wrapper">
              {searchLoading ? (
                <div className="results-loader">
                  <div className="spinner"></div>
                  <p>Searching embeddings across all papers...</p>
                </div>
              ) : searchResults.length === 0 ? (
                <div className="empty-results-state">
                  <HelpCircle size={48} className="help-icon" />
                  <h3>No results to display</h3>
                  <p>Type a semantic concept above to search text chunks across all uploaded papers using vector embeddings.</p>
                </div>
              ) : (
                <div className="results-list">
                  <div className="results-count-badge">
                    Found {searchResults.length} matching text chunks in database:
                  </div>
                  {searchResults.map((result, idx) => (
                    <div 
                      key={idx} 
                      className="result-item"
                      onClick={() => navigate(`/papers/${result.paper_id}`)}
                    >
                      <div className="result-header">
                        <div className="result-paper-info">
                          <FileText size={16} />
                          <h4>{result.paper_title}</h4>
                        </div>
                        <span className="result-sec-badge">{result.section_name}</span>
                        <span className="result-score-badge">
                          <TrendingUp size={12} style={{ marginRight: '4px' }} />
                          {Math.round(result.score * 100)}% Match
                        </span>
                      </div>
                      
                      <div className="result-snippet">
                        <p>{result.content}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* MULTI PAPER CHAT MODE */}
        {chatMode === 'multichat' && (
          <div className="multichat-mode-container animate-fade-in">
            <div className="multichat-workspace-grid">
              
              {/* Left Selector Panel */}
              <div className="selector-panel">
                <div className="selector-header">
                  <h3>Select Target Papers ({selectedPaperIds.length})</h3>
                  <button className="btn-link btn-xs" onClick={selectAllPapers}>
                    {selectedPaperIds.length === papers.length ? 'Deselect All' : 'Select All'}
                  </button>
                </div>
                
                <div className="selector-papers-list">
                  {papers.length === 0 ? (
                    <p className="no-papers-warning">No papers in library. Upload PDFs first.</p>
                  ) : (
                    papers.map(paper => {
                      const isSelected = selectedPaperIds.includes(paper.id)
                      return (
                        <div 
                          key={paper.id}
                          className={`selector-paper-row ${isSelected ? 'selected' : ''}`}
                          onClick={() => togglePaperSelection(paper.id)}
                        >
                          {isSelected ? (
                            <CheckSquare size={18} className="checkbox-icon checked" />
                          ) : (
                            <Square size={18} className="checkbox-icon" />
                          )}
                          <span className="paper-title-span" title={paper.title}>{paper.title}</span>
                        </div>
                      )
                    })
                  )}
                </div>
              </div>

              {/* Right Chat Panel */}
              <div className="chat-workspace-panel">
                <div className="chat-workspace-messages">
                  {selectedPaperIds.length === 0 ? (
                    <div className="chat-empty-state">
                      <BookOpen size={44} className="empty-chat-icon" />
                      <h3>Select papers to get started</h3>
                      <p>Check the papers you want to compare on the left sidebar to initialize the cross-document RAG context.</p>
                    </div>
                  ) : chatMessages.length === 0 ? (
                    <div className="chat-empty-state">
                      <Sparkles size={44} className="empty-chat-icon" />
                      <h3>Converse with selected papers</h3>
                      <p>Ask comparative questions such as "Compare the methodologies used" or "Synthesize the results across these papers".</p>
                    </div>
                  ) : (
                    chatMessages.map(msg => (
                      <div key={msg.id} className={`chat-message ${msg.type}`}>
                        <div className="chat-msg-avatar">
                          {msg.type === 'user' ? 'U' : 'AI'}
                        </div>
                        
                        <div className="chat-msg-body">
                          <div className="msg-bubble">
                            {msg.isThinking ? (
                              <div className="thinking-dots">
                                <span>Thinking</span>
                                <span className="dot">.</span>
                                <span className="dot">.</span>
                                <span className="dot">.</span>
                              </div>
                            ) : msg.type === 'user' ? (
                              <p>{msg.text}</p>
                            ) : (
                              <ReactMarkdown>{msg.text}</ReactMarkdown>
                            )}
                          </div>
                          
                          {msg.type === 'bot' && !msg.isThinking && (
                            <div className="msg-meta-details">
                              <span className="meta-item badge-provider">{msg.provider}</span>
                              {msg.sources && msg.sources.length > 0 && (
                                <div className="sources-list-row">
                                  <span className="sources-label">Citations:</span>
                                  {msg.sources.map((src, index) => (
                                    <span key={index} className="source-pill" title={src}>
                                      {src}
                                    </span>
                                  ))}
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                  <div ref={chatBottomRef} />
                </div>
                
                <form onSubmit={handleMultiChatSubmit} className="chat-workspace-input-row">
                  <input
                    type="text"
                    placeholder="Compare methodologies or ask a question..."
                    value={chatQuestion}
                    onChange={(e) => setChatQuestion(e.target.value)}
                    disabled={selectedPaperIds.length === 0 || chatLoading}
                  />
                  <button 
                    type="submit" 
                    disabled={selectedPaperIds.length === 0 || chatLoading || !chatQuestion.trim()} 
                    className="chat-send-btn"
                  >
                    <Send size={18} />
                  </button>
                </form>
              </div>

            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default SearchPage
