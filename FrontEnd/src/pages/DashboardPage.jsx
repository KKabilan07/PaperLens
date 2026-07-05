import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  FileText, 
  MessageSquare, 
  Database, 
  Plus, 
  ArrowRight,
  TrendingUp,
  Clock
} from 'lucide-react'
import { apiGet } from '../utils/api'
import { useAuth } from '../context/AuthContext'
import Sidebar from '../Components/Sidebar'
import './DashboardPage.css'

const DashboardPage = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  
  const [stats, setStats] = useState({ papers_uploaded: 0, questions_asked: 0, words_indexed: 0 })
  const [recentPapers, setRecentPapers] = useState([])
  const [recentChats, setRecentChats] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true)
        const [statsData, papersData, chatsData] = await Promise.all([
          apiGet('/dashboard/stats'),
          apiGet('/dashboard/recent-papers'),
          apiGet('/dashboard/recent-chats')
        ])
        
        setStats(statsData)
        setRecentPapers(papersData || [])
        setRecentChats(chatsData || [])
      } catch (err) {
        console.error('Error fetching dashboard data:', err)
        setError('Failed to load dashboard metrics. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    if (user) {
      fetchDashboardData()
    }
  }, [user])

  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M'
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K'
    }
    return num
  }

  const formatTime = (isoString) => {
    if (!isoString) return ''
    const date = new Date(isoString)
    return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
  }

  return (
    <div className="dashboard-layout">
      <Sidebar />
      
      <main className="dashboard-main">
        <header className="dashboard-header">
          <div className="header-greeting">
            <h1>Welcome, {user?.email?.split('@')[0]}</h1>
            <p>Here is your research summary for today.</p>
          </div>
          
          <button 
            className="btn-primary btn-add-paper"
            onClick={() => navigate('/papers')}
          >
            <Plus size={18} />
            <span>Upload Paper</span>
          </button>
        </header>

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        {loading ? (
          <div className="dashboard-loading">
            <div className="spinner"></div>
            <p>Assembling your analytics...</p>
          </div>
        ) : (
          <div className="dashboard-content animate-fade-in">
            {/* Stats Grid */}
            <section className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon-wrapper blue">
                  <FileText size={24} />
                </div>
                <div className="stat-info">
                  <h3>Papers Uploaded</h3>
                  <p className="stat-value">{stats.papers_uploaded}</p>
                </div>
                <div className="stat-trend positive">
                  <TrendingUp size={14} />
                  <span>Workspace</span>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon-wrapper green">
                  <MessageSquare size={24} />
                </div>
                <div className="stat-info">
                  <h3>Questions Asked</h3>
                  <p className="stat-value">{stats.questions_asked}</p>
                </div>
                <div className="stat-trend positive">
                  <TrendingUp size={14} />
                  <span>Total Chats</span>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon-wrapper purple">
                  <Database size={24} />
                </div>
                <div className="stat-info">
                  <h3>Words Indexed</h3>
                  <p className="stat-value">{formatNumber(stats.words_indexed)}</p>
                </div>
                <div className="stat-trend positive">
                  <TrendingUp size={14} />
                  <span>Tokens Ready</span>
                </div>
              </div>
            </section>

            {/* Dashboard Row: Recent Papers & Recent Chats */}
            <div className="dashboard-row">
              {/* Recent Papers */}
              <section className="dashboard-section recent-papers-section">
                <div className="section-header">
                  <h2>Recent Papers</h2>
                  <button className="btn-link" onClick={() => navigate('/papers')}>
                    <span>View all</span>
                    <ArrowRight size={16} />
                  </button>
                </div>

                <div className="papers-list-mini">
                  {recentPapers.length === 0 ? (
                    <div className="empty-state-mini">
                      <p>No papers uploaded yet.</p>
                      <button className="btn-secondary btn-sm" onClick={() => navigate('/papers')}>
                        Upload your first paper
                      </button>
                    </div>
                  ) : (
                    recentPapers.map(paper => (
                      <div 
                        key={paper.id} 
                        className="paper-row-item"
                        onClick={() => navigate(`/papers/${paper.id}`)}
                      >
                        <div className="paper-icon-small">
                          <FileText size={18} />
                        </div>
                        <div className="paper-details-small">
                          <h4>{paper.title}</h4>
                          <p>{paper.page_count || '?'} pages · {formatNumber(paper.word_count || 0)} words</p>
                        </div>
                        <span className="paper-date-small">
                          <Clock size={12} style={{ marginRight: '4px' }} />
                          {formatTime(paper.created_at)}
                        </span>
                      </div>
                    ))
                  )}
                </div>
              </section>

              {/* Recent Chats */}
              <section className="dashboard-section recent-chats-section">
                <div className="section-header">
                  <h2>Recent Questions</h2>
                </div>

                <div className="chats-list-mini">
                  {recentChats.length === 0 ? (
                    <div className="empty-state-mini">
                      <p>No questions asked yet.</p>
                      <p className="subtext">Select a paper to start chatting.</p>
                    </div>
                  ) : (
                    recentChats.map(chat => (
                      <div 
                        key={chat.id} 
                        className="chat-row-item"
                        onClick={() => navigate(`/papers/${chat.paper_id}`)}
                      >
                        <div className="chat-content-small">
                          <p className="chat-question">"{chat.question}"</p>
                          <p className="chat-paper-tag">Paper: {chat.paper_title}</p>
                        </div>
                        <span className="chat-date-small">
                          {formatTime(chat.created_at)}
                        </span>
                      </div>
                    ))
                  )}
                </div>
              </section>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default DashboardPage
