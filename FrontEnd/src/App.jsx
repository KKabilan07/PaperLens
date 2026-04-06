import React from 'react'
import { useAuth } from './context/AuthContext'
import { AuthProvider } from './context/AuthContext'
import Sidebar from './Components/Sidebar/Sidebar'
import Main from './Components/Main/Main'
import './App.css'

const AppContent = () => {
  const { user } = useAuth()

  return (
    <div className="app">
      {user && <Sidebar />}
      <Main />
    </div>
  )
}

const App = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App