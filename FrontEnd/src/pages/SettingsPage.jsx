import React from 'react'
import Sidebar from '../Components/Sidebar'
import './SettingsPage.css'

const SettingsPage = () => {
  return (
    <div className="settings-layout">
      <Sidebar />
      <main className="settings-main animate-fade-in">
        <header className="settings-header">
          <h1>Application Settings</h1>
          <p>Customize your AI assistant configurations.</p>
        </header>
        
        <div className="settings-card">
          <h2 className="settings-card-title">LLM & Embeddings Configurations</h2>
          <div className="settings-fields">
            <div>
              <label className="settings-field-label">Active Generation Model</label>
              <div className="settings-field-value">Gemini 2.5 Flash</div>
            </div>
            <div>
              <label className="settings-field-label">Embeddings Model</label>
              <div className="settings-field-value">gemini-embedding-001 (768-dimensional)</div>
            </div>
            <div>
              <label className="settings-field-label">Chunking Strategy</label>
              <div className="settings-field-value">LlamaIndex SentenceSplitter (size: 500, overlap: 100)</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default SettingsPage
