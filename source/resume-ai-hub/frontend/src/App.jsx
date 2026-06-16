import { useState } from 'react'
import ResumeBuilder from './components/ResumeBuilder'
import JobDescription from './components/JobDescription'
import ResumeAnalyzer from './components/ResumeAnalyzer'
import Chatbot from './components/Chatbot'
import './App.css'

const TABS = [
  { id: 'resume-builder', label: 'Resume Builder', icon: '📄' },
  { id: 'job-description', label: 'Job Description', icon: '💼' },
  { id: 'resume-analyzer', label: 'Resume Analyzer', icon: '🔍' },
  { id: 'chatbot', label: 'Career Chatbot', icon: '💬' },
]

export default function App() {
  const [activeTab, setActiveTab] = useState('resume-builder')

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🚀</span>
            <span className="logo-text">Resume AI Hub</span>
          </div>
          <p className="tagline">Powered by Claude AI</p>
        </div>
      </header>

      <nav className="tab-nav">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        ))}
      </nav>

      <main className="main-content">
        {activeTab === 'resume-builder' && <ResumeBuilder />}
        {activeTab === 'job-description' && <JobDescription />}
        {activeTab === 'resume-analyzer' && <ResumeAnalyzer />}
        {activeTab === 'chatbot' && <Chatbot />}
      </main>

      <footer className="footer">
        <p>Built with React + FastAPI + Claude AI</p>
      </footer>
    </div>
  )
}
