import React from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import {
  LayoutDashboard,
  BookOpen,
  Search,
  User,
  Settings,
  LogOut,
  Sparkles
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { supabase } from '../lib/supabase'
import { assets } from '../assets/assets'
import './Sidebar.css'

const Sidebar = () => {
  const { user } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      await supabase.auth.signOut()
      navigate('/login')
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand" onClick={() => navigate('/dashboard')}>
        <img src={assets.logo || "/logo.png"} alt="PaperLens" className="brand-logo" />
      </div>

      <nav className="sidebar-nav">
        <NavLink
          to="/dashboard"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <LayoutDashboard size={20} />
          <span>Dashboard</span>
        </NavLink>

        <NavLink
          to="/papers"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <BookOpen size={20} />
          <span>My Papers</span>
        </NavLink>
      </nav>

      <div className="sidebar-footer">

        <div className="user-profile-widget">
          <div className="user-avatar">
            {user?.email?.charAt(0).toUpperCase() || 'U'}
          </div>
          <div className="user-meta">
            <p className="user-email" title={user?.email}>{user?.email}</p>
            <span className="user-role">Researcher</span>
          </div>
        </div>

        <div className="footer-links">
          <NavLink
            to="/profile"
            className={({ isActive }) => `footer-link-item ${isActive ? 'active' : ''}`}
            title="Profile"
          >
            <User size={18} />
          </NavLink>
          <NavLink
            to="/settings"
            className={({ isActive }) => `footer-link-item ${isActive ? 'active' : ''}`}
            title="Settings"
          >
            <Settings size={18} />
          </NavLink>
          <button
            className="footer-link-item logout-btn"
            onClick={handleLogout}
            title="Logout"
          >
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
