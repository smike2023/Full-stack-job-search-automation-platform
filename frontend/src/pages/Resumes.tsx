import { useState, useEffect } from 'react'
import { resumesApi } from '../services/api'
import './Resumes.css'

interface Resume {
  id: number
  title: string
  content: string
  target_role: string | null
  target_company: string | null
  created_at: string
  updated_at: string
}

function Resumes() {
  const [resumes, setResumes] = useState<Resume[]>([])
  const [selectedResume, setSelectedResume] = useState<Resume | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    targetRole: '',
    targetCompany: '',
    userExperience: '',
    userSkills: '',
    userEducation: '',
    jobDescription: '',
  })

  useEffect(() => {
    loadResumes()
  }, [])

  const loadResumes = async () => {
    try {
      const response = await resumesApi.getAll()
      setResumes(response.data)
    } catch (error) {
      console.error('Failed to load resumes:', error)
    }
  }

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.targetRole || !formData.userExperience || !formData.userSkills) {
      return
    }

    setIsGenerating(true)
    try {
      const response = await resumesApi.generate({
        target_role: formData.targetRole,
        target_company: formData.targetCompany || undefined,
        user_experience: formData.userExperience,
        user_skills: formData.userSkills,
        user_education: formData.userEducation || undefined,
        job_description: formData.jobDescription || undefined,
      })
      setResumes([response.data, ...resumes])
      setSelectedResume(response.data)
      setShowForm(false)
      setFormData({
        targetRole: '',
        targetCompany: '',
        userExperience: '',
        userSkills: '',
        userEducation: '',
        jobDescription: '',
      })
    } catch (error) {
      console.error('Failed to generate resume:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this resume?')) return
    try {
      await resumesApi.delete(id)
      setResumes(resumes.filter((r) => r.id !== id))
      if (selectedResume?.id === id) setSelectedResume(null)
    } catch (error) {
      console.error('Failed to delete resume:', error)
    }
  }

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  return (
    <div className="resumes-page">
      <div className="resumes-header">
        <h1>Resumes</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Generate New Resume'}
        </button>
      </div>

      {showForm && (
        <form className="generate-form card" onSubmit={handleGenerate}>
          <h3>Generate AI-Tailored Resume</h3>
          <div className="form-grid">
            <div className="form-group">
              <label>Target Role *</label>
              <input
                type="text"
                value={formData.targetRole}
                onChange={(e) =>
                  setFormData({ ...formData, targetRole: e.target.value })
                }
                placeholder="e.g., Senior Software Engineer"
                required
              />
            </div>
            <div className="form-group">
              <label>Target Company</label>
              <input
                type="text"
                value={formData.targetCompany}
                onChange={(e) =>
                  setFormData({ ...formData, targetCompany: e.target.value })
                }
                placeholder="e.g., Google"
              />
            </div>
            <div className="form-group full-width">
              <label>Your Experience *</label>
              <textarea
                value={formData.userExperience}
                onChange={(e) =>
                  setFormData({ ...formData, userExperience: e.target.value })
                }
                placeholder="Describe your work experience..."
                rows={4}
                required
              />
            </div>
            <div className="form-group full-width">
              <label>Your Skills *</label>
              <textarea
                value={formData.userSkills}
                onChange={(e) =>
                  setFormData({ ...formData, userSkills: e.target.value })
                }
                placeholder="List your skills..."
                rows={2}
                required
              />
            </div>
            <div className="form-group">
              <label>Education</label>
              <input
                type="text"
                value={formData.userEducation}
                onChange={(e) =>
                  setFormData({ ...formData, userEducation: e.target.value })
                }
                placeholder="e.g., BS in Computer Science"
              />
            </div>
            <div className="form-group full-width">
              <label>Job Description (optional)</label>
              <textarea
                value={formData.jobDescription}
                onChange={(e) =>
                  setFormData({ ...formData, jobDescription: e.target.value })
                }
                placeholder="Paste job description to tailor your resume..."
                rows={3}
              />
            </div>
          </div>
          <button type="submit" className="btn-primary" disabled={isGenerating}>
            {isGenerating ? 'Generating...' : 'Generate Resume'}
          </button>
        </form>
      )}

      <div className="resumes-container">
        <div className="resumes-list">
          {resumes.length === 0 ? (
            <div className="no-resumes card">
              <p>No resumes yet. Generate your first AI-tailored resume!</p>
            </div>
          ) : (
            resumes.map((resume) => (
              <div
                key={resume.id}
                className={`resume-card card ${
                  selectedResume?.id === resume.id ? 'selected' : ''
                }`}
                onClick={() => setSelectedResume(resume)}
              >
                <h3>{resume.title}</h3>
                {resume.target_company && (
                  <p className="target">For: {resume.target_company}</p>
                )}
                <p className="date">Created: {formatDate(resume.created_at)}</p>
              </div>
            ))
          )}
        </div>

        {selectedResume && (
          <div className="resume-detail card">
            <div className="detail-header">
              <h2>{selectedResume.title}</h2>
              <button
                className="btn-danger"
                onClick={() => handleDelete(selectedResume.id)}
              >
                Delete
              </button>
            </div>
            {selectedResume.target_role && (
              <p className="meta">Role: {selectedResume.target_role}</p>
            )}
            {selectedResume.target_company && (
              <p className="meta">Company: {selectedResume.target_company}</p>
            )}
            <div className="resume-content">
              <pre>{selectedResume.content}</pre>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Resumes
