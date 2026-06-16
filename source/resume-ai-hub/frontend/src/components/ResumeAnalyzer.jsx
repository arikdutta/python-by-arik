import { useState } from 'react'

export default function ResumeAnalyzer() {
  const [resume, setResume] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setOutput('')
    try {
      const res = await fetch('/api/analyzer/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume, job_description: jobDescription }),
      })
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        setOutput((prev) => prev + decoder.decode(value))
      }
    } catch (err) {
      setOutput('Error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => navigator.clipboard.writeText(output)

  return (
    <div>
      <div className="card">
        <h2 className="card-title">Resume Analyzer</h2>
        <p className="card-desc">
          Paste your resume and a job description — Claude AI will score the match, identify gaps, and give actionable feedback.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="split-layout">
            <div className="form-group">
              <label>Your Resume *</label>
              <textarea
                value={resume}
                onChange={(e) => setResume(e.target.value)}
                rows={18}
                placeholder="Paste your resume text here...&#10;&#10;John Doe&#10;john@email.com | LinkedIn | GitHub&#10;&#10;EXPERIENCE&#10;Senior Engineer at XYZ Corp (2021-2024)&#10;- Led migration to microservices architecture&#10;- Reduced deployment time by 60%&#10;..."
                required
              />
            </div>
            <div className="form-group">
              <label>Job Description *</label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                rows={18}
                placeholder="Paste the job description here...&#10;&#10;Senior Software Engineer at TechCorp&#10;&#10;We are looking for a Senior Software Engineer to join our growing team...&#10;&#10;Responsibilities:&#10;- Design scalable distributed systems&#10;- Lead architecture decisions&#10;..."
                required
              />
            </div>
          </div>

          <div className="action-bar">
            <button type="submit" className="btn-primary" disabled={loading || !resume || !jobDescription}>
              {loading ? <><div className="spinner" /> Analyzing...</> : '🔍 Analyze Match'}
            </button>
            <button
              type="button"
              className="btn-secondary"
              onClick={() => { setResume(''); setJobDescription(''); setOutput('') }}
            >
              Clear
            </button>
          </div>
        </form>
      </div>

      {(output || loading) && (
        <div className="output-card">
          <div className="output-header">
            <span>Analysis Report</span>
            {output && <button className="btn-secondary" onClick={handleCopy}>Copy</button>}
          </div>
          <div className="output-body">
            {output || <span className="output-placeholder">Claude is analyzing your resume...</span>}
            {loading && <span className="streaming-cursor" />}
          </div>
        </div>
      )}
    </div>
  )
}
