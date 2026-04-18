import React, { useState, useEffect } from 'react'
import './ThemeSwitcher.css'

const ThemeSwitcher = () => {
  const [currentTheme, setCurrentTheme] = useState('sage')
  const [isOpen, setIsOpen] = useState(false)

  const themes = [
    { id: 'sage', name: 'Cool Sage', description: 'Calm & Research-Focused' },
    { id: 'warm', name: 'Warm Neutrals', description: 'Professional & Inviting' },
    { id: 'purple', name: 'Deep Purple', description: 'Elegant & Modern' },
  ]

  useEffect(() => {
    // Load saved theme from localStorage
    const savedTheme = localStorage.getItem('paperlens-theme') || 'sage'
    setCurrentTheme(savedTheme)
    applyTheme(savedTheme)
  }, [])

  const applyTheme = (themeId) => {
    if (themeId === 'sage') {
      document.documentElement.removeAttribute('data-theme')
    } else {
      document.documentElement.setAttribute('data-theme', themeId)
    }
    localStorage.setItem('paperlens-theme', themeId)
  }

  const handleThemeChange = (themeId) => {
    setCurrentTheme(themeId)
    applyTheme(themeId)
    setIsOpen(false)
  }

  return (
    <div className="theme-switcher">
      <button
        className="theme-switcher-btn"
        onClick={() => setIsOpen(!isOpen)}
        title="Switch Theme"
        aria-label="Theme switcher"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>
      </button>

      {isOpen && (
        <div className="theme-switcher-menu">
          {themes.map((theme) => (
            <button
              key={theme.id}
              className={`theme-option ${currentTheme === theme.id ? 'active' : ''}`}
              onClick={() => handleThemeChange(theme.id)}
            >
              <div className="theme-swatch">
                {theme.id === 'sage' && (
                  <div className="color-ring" style={{
                    background: 'linear-gradient(135deg, #2D7B4A 0%, #FAFBF9 50%, #DDE3D8 100%)'
                  }}></div>
                )}
                {theme.id === 'warm' && (
                  <div className="color-ring" style={{
                    background: 'linear-gradient(135deg, #A87537 0%, #FAF7F4 50%, #DDD3C7 100%)'
                  }}></div>
                )}
                {theme.id === 'purple' && (
                  <div className="color-ring" style={{
                    background: 'linear-gradient(135deg, #6B4B9C 0%, #FAF9FB 50%, #DDD4E8 100%)'
                  }}></div>
                )}
              </div>
              <div className="theme-info">
                <div className="theme-name">{theme.name}</div>
                <div className="theme-desc">{theme.description}</div>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default ThemeSwitcher
