import { useState } from 'react'

const INITIAL = {
  job_title: '', company_name: '', department: '',
  employment_type: 'Full-time', location: '', salary_range: '',
  about_company: '', responsibilities: '', requirements: '', nice_to_have: '',
}

export default function JobDescription() {
  const [form, setForm] = useState(INITIAL)
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setOutput('')
    try {
      const res = await fetch('/api/job-description/create', {
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
        <h2 className="card-title">Job Description Creator</h2>
        <p className="card-desc">Provide role details and Claude AI will generate a compelling, professional job description.</p>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Job Title *</label>
              <input name="job_title" value={form.job_title} onChange={handleChange}
                placeholder="Senior Software Engineer" required />
            </div>
            <div className="form-group">
              <label>Company Name *</label>
              <input name="company_name" value={form.company_name} onChange={handleChange}
                placeholder="Acme Corp" required />
            </div>
            <div className="form-group">
              <label>Department</label>
              <input name="department" value={form.department} onChange={handleChange}
                placeholder="Engineering" />
            </div>
            <div className="form-group">
              <label>Employment Type</label>
              <select name="employment_type" value={form.employment_type} onChange={handleChange}>
                <option>Full-time</option>
                <option>Part-time</option>
                <option>Contract</option>
                <option>Internship</option>
                <option>Remote</option>
              </select>
            </div>
            <div className="form-group">
              <label>Location</label>
              <input name="location" value={form.location} onChange={handleChange}
                placeholder="San Francisco, CA / Remote" />
            </div>
            <div className="form-group">
              <label>Salary Range</label>
              <input name="salary_range" value={form.salary_range} onChange={handleChange}
                placeholder="$120,000 - $160,000" />
            </div>
            <div className="form-group full-width">
              <label>About the Company</label>
              <textarea name="about_company" value={form.about_company} onChange={handleChange}
                rows={3} placeholder="Brief description of the company, culture, mission..." />
            </div>
            <div className="form-group full-width">
              <label>Key Responsibilities *</label>
              <textarea name="responsibilities" value={form.responsibilities} onChange={handleChange}
                rows={5} placeholder="- Design and develop scalable backend services&#10;- Lead code reviews and mentor junior engineers&#10;- Collaborate with product teams..." required />
            </div>
            <div className="form-group full-width">
              <label>Required Qualifications *</label>
              <textarea name="requirements" value={form.requirements} onChange={handleChange}
                rows={4} placeholder="- 5+ years of experience in backend development&#10;- Proficiency in Python or Go&#10;- Experience with cloud platforms (AWS/GCP)..." required />
            </div>
            <div className="form-group full-width">
              <label>Nice to Have</label>
              <textarea name="nice_to_have" value={form.nice_to_have} onChange={handleChange}
                rows={3} placeholder="- Experience with Kubernetes&#10;- Open source contributions&#10;- Startup experience..." />
            </div>
          </div>

          <div className="action-bar">
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? <><div className="spinner" /> Generating...</> : '✨ Create Job Description'}
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
            <span>Generated Job Description</span>
            {output && <button className="btn-secondary" onClick={handleCopy}>Copy</button>}
          </div>
          <div className="output-body">
            {output || <span className="output-placeholder">Claude is crafting the job description...</span>}
            {loading && <span className="streaming-cursor" />}
          </div>
        </div>
      )}
    </div>
  )
}
