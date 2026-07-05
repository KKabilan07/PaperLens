import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  FileText, 
  Trash2, 
  Upload, 
  Clock, 
  Layers, 
  Calendar 
} from 'lucide-react'
import { DotSpinner } from 'ldrs/react'
import 'ldrs/react/DotSpinner.css'
import Sidebar from '../Components/Sidebar'
import { getPapers, deletePaper, uploadPaper } from '../utils/paperService'
import './PapersListPage.css'

const PapersListPage = () => {
  const navigate = useNavigate()
  
  const [papers, setPapers] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState('')
  const [error, setError] = useState('')
  
  const fileInputRef = useRef(null)

  useEffect(() => {
    loadPapers()
  }, [])

  const loadPapers = async () => {
    try {
      setLoading(true)
      const data = await getPapers()
      setPapers(data || [])
    } catch (err) {
      setError('Failed to load papers.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    setUploadProgress('Uploading paper...')
    
    try {
      const title = file.name.replace('.pdf', '')
      const response = await uploadPaper(file, title)
      
      setUploadProgress('✓ Ingesting text embeddings...')
      await loadPapers()
      
      // Navigate directly to details page for the new paper
      if (response?.paper_id) {
        navigate(`/papers/${response.paper_id}`)
      }
      
      setUploadProgress('')
      setError('')
    } catch (err) {
      setError(`Upload failed: ${err.message}`)
      setUploadProgress('')
      console.error(err)
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleDelete = async (paperId, e) => {
    e.stopPropagation()
    if (!window.confirm('Are you sure you want to delete this paper and all associated history?')) return
    
    try {
      await deletePaper(paperId)
      setPapers(papers.filter(p => p.id !== paperId))
      setError('')
    } catch (err) {
      setError(`Failed to delete paper: ${err.message}`)
      console.error(err)
    }
  }

  const formatNumber = (num) => {
    if (!num) return '0'
    return num.toLocaleString()
  }

  const formatDate = (isoString) => {
    if (!isoString) return ''
    const date = new Date(isoString)
    return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
  }

  return (
    <div className="papers-layout">
      <Sidebar />
      
      <main className="papers-main">
        <header className="papers-header">
          <div className="header-title">
            <h1>My Papers</h1>
            <p>Upload, manage, and explore your research library.</p>
          </div>
          
          <button 
            className="btn-primary btn-upload"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
          >
            <Upload size={18} />
            <span>Upload Paper</span>
          </button>
          
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            style={{ display: 'none' }}
            disabled={uploading}
          />
        </header>

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        {uploading && (
          <div className="upload-progress-banner">
            <DotSpinner size="30" speed="0.9" color="var(--color-accent)" />
            <span>{uploadProgress}</span>
          </div>
        )}

        {loading ? (
          <div className="papers-loading">
            <div className="spinner"></div>
            <p>Loading your research library...</p>
          </div>
        ) : (
          <div className="papers-content animate-fade-in">
            {papers.length === 0 ? (
              <div className="papers-empty-state">
                <FileText size={64} className="empty-icon" />
                <h2>Library is Empty</h2>
                <p>Upload research papers (PDFs) to start querying, summarizing, and parsing sections.</p>
                <button 
                  className="btn-primary" 
                  onClick={() => fileInputRef.current?.click()}
                >
                  Upload First Paper
                </button>
              </div>
            ) : (
              <div className="papers-grid">
                {papers.map(paper => (
                  <div 
                    key={paper.id} 
                    className="paper-card"
                    onClick={() => navigate(`/papers/${paper.id}`)}
                  >
                    <div className="card-top">
                      <div className="paper-icon-wrapper">
                        <FileText size={24} />
                      </div>
                      <button 
                        className="btn-card-delete"
                        onClick={(e) => handleDelete(paper.id, e)}
                        title="Delete paper"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                    
                    <div className="card-body">
                      <h3>{paper.title}</h3>
                      <p className="card-description" title={paper.description}>
                        {paper.description || 'No description available'}
                      </p>
                    </div>
                    
                    <div className="card-footer">
                      <div className="card-meta-item">
                        <Layers size={14} />
                        <span>{paper.page_count || '?'} pages</span>
                      </div>
                      <div className="card-meta-item">
                        <Clock size={14} />
                        <span>{formatNumber(paper.word_count || 0)} words</span>
                      </div>
                      <div className="card-meta-item full-width">
                        <Calendar size={14} />
                        <span>Uploaded: {formatDate(paper.created_at)}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default PapersListPage
