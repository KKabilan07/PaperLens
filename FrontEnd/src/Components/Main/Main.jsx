import React, { useState } from 'react'
import './Main.css'
import Login from './Login'
import { useAuth } from '../../context/AuthContext'
import { supabase } from '../../lib/supabase'

const Main = () => {
  const [showAuthModal, setShowAuthModal] = useState(false)
  const { user, loading } = useAuth()

  const handleClose = () => {
    setShowAuthModal(false)
  }

  const handleLogout = async () => {
    try {
      await supabase.auth.signOut()
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  if (loading) {
    return (
      <div className="main">
        <div className="nav">
          <p>IntelliChat</p>
        </div>
        <div className="main-container">
          <div className="greet">
            <p><span>Welcome to IntelliChat</span></p>
            <p>Your AI-Powered Research Assistant</p>
          </div>
          <button className="btn btn-getstarted" onClick={() => setShowAuthModal(true)}>
            Get Started
          </button>
        </div>
        {showAuthModal && <Login onClose={handleClose} isLogin={false} />}
      </div>
    )
  }

  // If not authenticated, show login/signup buttons
  if (!user) {
    return (
      <div className="main">
        <div className="nav">
          <p>IntelliChat</p>
        </div>

        <div className="main-container">
          <div className="greet">
            <p><span>Welcome to IntelliChat</span></p>
            <p>Your AI-Powered Research Assistant</p>
          </div>

          <div className="auth-buttons">
            <button className="btn btn-getstarted" onClick={() => setShowAuthModal(true)}>
              Getting Started
            </button>
          </div>
        </div>

        {showAuthModal && <Login onClose={handleClose} isLogin={false} />}
      </div>
    )
  }

  // If authenticated, show main chat interface
  return (
    <div className="main">
      <div className="nav">
        <p>IntelliChat</p>
        <div className="user-info">
          <span>{user.email}</span>
          <button className="user-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      <div className="main-container">
        <div className="greet">
          <p><span>Hello!</span></p>
          <p>How can I help you today?</p>
        </div>

        <div className="main-bottom">
          <div className="search-box">
            <input type="text" placeholder='Enter a prompt here' />
            <div>
              <img src="/gallery.svg" alt="upload" />
              <img src="/mic.svg" alt="voice" />
              <img src="/send.svg" alt="send" />
            </div>
          </div>
          <p className="bottom-info">
            IntelliChat may sometimes be inaccurate, so please verify important info.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Main