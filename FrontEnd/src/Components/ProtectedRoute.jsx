import React from 'react'
import { useAuth } from '../context/AuthContext'

/**
 * ProtectedRoute component - redirects to login if not authenticated
 * @param {React.Component} Component - Component to render if authenticated
 * @param {object} props - Props to pass to the component
 */
export const ProtectedRoute = ({ Component, ...props }) => {
  const { user, loading } = useAuth()

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

  if (!user) {
    // Redirect to home/login page
    window.location.href = '/'
    return null
  }

  return <Component {...props} />
}

export default ProtectedRoute
