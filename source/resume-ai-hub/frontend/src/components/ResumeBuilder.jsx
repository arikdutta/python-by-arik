import { useState } from 'react'

const INITIAL = {
  name: '', email: '', phone: '', location: '',
  summary: '', experience: '', education: '', skills: '', certifications: '',
}

export default function ResumeBuilder() {
  const [form, setForm] = useState(INITIAL)
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setOutput('')
    try {
      const res = await fetch('/api/resume/build', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
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
        <h2 className="card-title">Resume Builder</h2>
        <p className="card-desc">Fill in your details and Claude AI will craft a polished, ATS-friendly resume for you.</p>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Full Name *</label>
              <input name="name" value={form.name} onChange={handleChange} placeholder="John Doe" required />
            </div>
            <div className="form-group">
              <label>Email *</label>
              <input name="email" type="email" value={form.email} onChange={handleChange} placeholder="john@example.com" required />
            </div>
            <div className="form-group">
              <label>Phone</label>
              <input name="phone" value={form.phone} onChange={handleChange} placeholder="+1 (555) 000-0000" />
            </div>
            <div className="form-group">
              <label>Location</label>
              <input name="location" value={form.location} onChange={handleChange} placeholder="New York, NY" />
            </div>
            <div className="form-group full-width">
              <label>Professional Summary *</label>
              <textarea name="summary" value={form.summary} onChange={handleChange}
                rows={3} placeholder="Brief overview of your background, expertise, and career goals..." required />
            </div>
            <div className="form-group full-width">
              <label>Work Experience *</label>
              <textarea name="experience" value={form.experience} onChange={handleChange}
                rows={5} placeholder="Company | Role | Duration&#10;- Key achievement 1&#10;- Key achievement 2&#10;&#10;Company | Role | Duration&#10;- Responsibilities..." required />
            </div>
            <div className="form-group full-width">
              <label>Education *</label>
              <textarea name="education" value={form.education} onChange={handleChange}
                rows={3} placeholder="University Name | Degree | Year&#10;GPA: 3.8/4.0 (optional)" required />
            </div>
            <div className="form-group">
              <label>Skills *</label>
              <textarea name="skills" value={form.skills} onChange={handleChange}
                rows={3} placeholder="Python, React, SQL, AWS, Docker..." required />
            </div>
            <div className="form-group">
              <label>Certifications</label>
              <textarea name="certifications" value={form.certifications} onChange={handleChange}
                rows={3} placeholder="AWS Solutions Architect | 2024&#10;PMP Certification | 2023" />
            </div>
          </div>

          <div className="action-bar">
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? <><div className="spinner" /> Generating...</> : '✨ Build Resume'}
            </button>
            <button type="button" className="btn-secondary" onClick={() => { setForm(INITIAL); setOutput('') }}>
              Clear
            </button>
          </div>
        </form>
      </div>

      {(output || loading) && (
        <div className="output-card">
          <div className="output-header">
            <span>Generated Resume</span>
            {output && <button className="btn-secondary" onClick={handleCopy}>Copy</button>}
          </div>
          <div className="output-body">
            {output || <span className="output-placeholder">Claude is writing your resume...</span>}
            {loading && <span className="streaming-cursor" />}
          </div>
        </div>
      )}
    </div>
  )
}
