import React from 'react'
import Sidebar from '../Components/Sidebar'
import { useAuth } from '../context/AuthContext'
import './ProfilePage.css'

const ProfilePage = () => {
  const { user } = useAuth()
  
  return (
    <div className="profile-layout">
      <Sidebar />
      <main className="profile-main animate-fade-in">
        <header className="profile-header">
          <h1>User Profile</h1>
          <p>Manage your account credentials and workspace.</p>
        </header>
        
        <div className="profile-card">
          <h2 className="profile-card-title">Account Settings</h2>
          <div className="profile-fields">
            <div>
              <label className="profile-field-label">Email Address</label>
              <div className="profile-field-value">{user?.email}</div>
            </div>
            <div>
              <label className="profile-field-label">User ID (UUID)</label>
              <div className="profile-field-value muted">{user?.id}</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default ProfilePage
