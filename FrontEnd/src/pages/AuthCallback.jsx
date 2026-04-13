import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const AuthCallback = () => {
  const navigate = useNavigate()

  useEffect(() => {
    // The OAuth callback will automatically set the session in Supabase
    // Just redirect to chat after a brief pause to ensure session is set
    const timer = setTimeout(() => {
      navigate('/chat')
    }, 1000)

    return () => clearTimeout(timer)
  }, [navigate])

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      fontSize: '18px',
      color: '#666'
    }}>
      Completing login...
    </div>
  )
}

export default AuthCallback
