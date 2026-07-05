import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const AuthCallback = () => {
  const navigate = useNavigate()

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/dashboard')
    }, 1000)

    return () => clearTimeout(timer)
  }, [navigate])

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      fontSize: '16px',
      color: 'var(--color-text-secondary)',
      fontFamily: 'var(--font-family-base)',
      backgroundColor: 'var(--color-bg-primary)'
    }}>
      Completing login...
    </div>
  )
}

export default AuthCallback
