import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './LoginPage.css'
import { supabase } from '../lib/supabase'
import { assets } from '../assets/assets.js'

const LoginPage = ({ initialView = 'landing' }) => {
  const navigate = useNavigate()
  const [showAuthForm, setShowAuthForm] = useState(initialView === 'form')
  const [isLoginMode, setIsLoginMode] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [userName, setUserName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    setShowAuthForm(initialView === 'form')
  }, [initialView])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      if (isLoginMode) {
        // Login with email and password
        console.log('Attempting login with:', email)
        const { data, error: authError } = await supabase.auth.signInWithPassword({
          email,
          password,
        })

        if (authError) {
          console.error('Auth error:', authError)
          throw authError
        }

        console.log('Login successful, user:', data.user)
        // Navigate to chat on successful login
        setTimeout(() => navigate('/chat'), 500)
      } else {
        // Validate passwords match
        if (password !== confirmPassword) {
          throw new Error('Passwords do not match')
        }

        // Sign up with email and password
        const { data, error: authError } = await supabase.auth.signUp({
          email,
          password,
          options: {
            data: {
              full_name: userName,
            },
          },
        })

        if (authError) throw authError

        // Show success message
        setError('Check your email to confirm your account!')
      }
    } catch (err) {
      console.error('Auth error:', err)
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleOAuthLogin = async (provider) => {
    try {
      const redirectUrl = `${window.location.origin}/auth/callback`
      await supabase.auth.signInWithOAuth({
        provider: provider,
        options: {
          redirectTo: redirectUrl,
        },
      })
    } catch (err) {
      console.error('OAuth error:', err)
      setError(err.message || 'OAuth login failed')
    }
  }

  if (!showAuthForm) {
    return (
      <div className="landing-page">
        <div className="landing-header">
          <div className="landing-logo-container">
            <img src={assets.logo} alt="PaperLens" className="landing-logo" />
          </div>
        </div>

        <div className="landing-content">
          <div className="landing-hero">
            <h1 className="landing-title">
              <span className="highlight">Research Reimagined</span>
            </h1>
            
            <p className="landing-subtitle">
              Upload research papers and chat with AI to extract insights, find answers, and accelerate your research workflow.
            </p>

            <button 
              className="btn-cta"
              onClick={() => navigate('/login')}
            >
              Get Started
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </button>
          </div>

          <div className="landing-features">
            <div className="feature-grid">
              <div className="feature-card">
                <div className="feature-icon upload">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                  </svg>
                </div>
                <h3>Easy Upload</h3>
                <p>Upload PDF research papers in seconds</p>
              </div>

              <div className="feature-card">
                <div className="feature-icon chat">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>
                <h3>AI Chat</h3>
                <p>Ask questions and get instant insights</p>
              </div>

              <div className="feature-card">
                <div className="feature-icon insights">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="12 3 20 7.5 20 16.5 12 21 4 16.5 4 7.5 12 3"></polyline>
                    <line x1="12" y1="12" x2="20" y2="7.5"></line>
                    <line x1="12" y1="12" x2="12" y2="21"></line>
                    <line x1="12" y1="12" x2="4" y2="7.5"></line>
                  </svg>
                </div>
                <h3>Extract Insights</h3>
                <p>Find key information and patterns</p>
              </div>
            </div>
          </div>
        </div>

        <div className="landing-footer">
          <p>Powered by advanced AI · Secure & Private</p>
        </div>
      </div>
    )
  }

  return (
    <div className="login-page">
      <div className="login-header">
        <div className="login-header-content">
          <div className="login-logo">
            <img src={assets.logo} alt="PaperLens" />
          </div>
        </div>
      </div>

      <div className="login-main">
        <div className="login-card">
          <div className="login-form-wrapper">
            <div className="login-header-text">
              <h2>{isLoginMode ? 'Welcome Back' : 'Create Account'}</h2>
              <p className="login-subtitle">
                {isLoginMode
                  ? 'Sign in to continue using PaperLens'
                  : 'Join PaperLens and start researching'}
              </p>
            </div>

            {error && (
              <div className={`alert ${error.includes('Check your email') ? 'alert-success' : 'alert-error'}`}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  {error.includes('Check your email') ? (
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  ) : (
                    <circle cx="12" cy="12" r="10"></circle>
                  )}
                  <polyline points="12 8 12 12 16 14"></polyline>
                </svg>
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="auth-form">
              {!isLoginMode && (
                <div className="form-group">
                  <label htmlFor="name">Full Name</label>
                  <input
                    id="name"
                    type="text"
                    placeholder="Your name"
                    value={userName}
                    onChange={(e) => setUserName(e.target.value)}
                    required
                  />
                </div>
              )}

              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              {!isLoginMode && (
                <div className="form-group">
                  <label htmlFor="confirm-password">Confirm Password</label>
                  <input
                    id="confirm-password"
                    type="password"
                    placeholder="••••••••"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                  />
                </div>
              )}

              <button
                type="submit"
                className="btn-submit"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Loading...
                  </>
                ) : isLoginMode ? 'Sign In' : 'Create Account'}
              </button>
            </form>

            <div className="divider">
              <span>OR</span>
            </div>

            <button
              type="button"
              className="btn-oauth google"
              onClick={() => handleOAuthLogin('google')}
            >
              <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" width="20" height="20">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
              Continue with Google
            </button>

            <p className="toggle-auth">
              {isLoginMode ? "Don't have an account? " : 'Already have an account? '}
              <button
                type="button"
                onClick={() => {
                  setIsLoginMode(!isLoginMode)
                  setError('')
                }}
                className="toggle-link"
              >
                {isLoginMode ? 'Sign Up' : 'Sign In'}
              </button>
            </p>
          </div>
        </div>

        <div className="login-benefits">
          <h3>Why PaperLens?</h3>
          <ul>
            <li>
              <span className="benefit-icon">✓</span>
              <span>Upload and organize your research papers</span>
            </li>
            <li>
              <span className="benefit-icon">✓</span>
              <span>Ask AI questions and get instant answers</span>
            </li>
            <li>
              <span className="benefit-icon">✓</span>
              <span>Extract key insights and citations</span>
            </li>
            <li>
              <span className="benefit-icon">✓</span>
              <span>All conversations are secure and private</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
