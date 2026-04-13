import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './LoginPage.css'
import { supabase } from '../lib/supabase'

const LoginPage = () => {
  const navigate = useNavigate()
  const [showAuthForm, setShowAuthForm] = useState(false)
  const [isLoginMode, setIsLoginMode] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [userName, setUserName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

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
        <div className="landing-content">
          <h1>PaperLens</h1>
          <p className="landing-subtitle">Your AI-Powered Research Assistant</p>
          <p className="landing-description">
            Upload research papers and chat with AI to extract insights, find answers, and accelerate your research workflow.
          </p>
          <button className="btn-getstarted" onClick={() => setShowAuthForm(true)}>
            Get Started
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="login-page">
      <button className="btn-back" onClick={() => setShowAuthForm(false)}>← Back</button>
      
      <div className="login-card">
        <h2>{isLoginMode ? 'Welcome Back' : 'Create Account'}</h2>
        <p className="subtitle">
          {isLoginMode 
            ? 'Sign in to continue to PaperLens' 
            : 'Sign up to get started with PaperLens'}
        </p>

        {error && (
          <div className={`message ${error.includes('Check your email') ? 'success' : 'error'}`}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {!isLoginMode && (
            <div className="form-group">
              <input
                type="text"
                placeholder="Full Name"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                required
              />
            </div>
          )}

          <div className="form-group">
            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {!isLoginMode && (
            <div className="form-group">
              <input
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
          )}

          <button 
            type="submit" 
            className="submit-btn"
            disabled={loading}
          >
            {loading ? 'Loading...' : isLoginMode ? 'Sign In' : 'Sign Up'}
          </button>
        </form>

        <div className="divider">OR</div>

        <div className="social-buttons">
          <button
            type="button"
            className="social-btn google-btn"
            onClick={() => handleOAuthLogin('google')}
          >
            Sign in with Google
          </button>
          <button
            type="button"
            className="social-btn github-btn"
            onClick={() => handleOAuthLogin('github')}
          >
            Sign in with GitHub
          </button>
        </div>

        <p className="toggle-mode">
          {isLoginMode ? "Don't have an account? " : 'Already have an account? '}
          <button
            type="button"
            onClick={() => {
              setIsLoginMode(!isLoginMode)
              setError('')
            }}
            className="toggle-btn"
          >
            {isLoginMode ? 'Sign Up' : 'Sign In'}
          </button>
        </p>
      </div>
    </div>
  )
}

export default LoginPage
