import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { jobsApi, resumesApi, schedulesApi } from '../services/api'
import './Dashboard.css'

interface Stats {
  totalJobs: number
  appliedJobs: number
  totalResumes: number
  activeSchedules: number
}

function Dashboard() {
  const { user, updateUser } = useAuth()
  const [stats, setStats] = useState<Stats>({
    totalJobs: 0,
    appliedJobs: 0,
    totalResumes: 0,
    activeSchedules: 0,
  })
  const [isEditing, setIsEditing] = useState(false)
  const [skills, setSkills] = useState(user?.skills || '')
  const [keywords, setKeywords] = useState(user?.keywords || '')
  const [fullName, setFullName] = useState(user?.full_name || '')

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const [jobsRes, resumesRes, schedulesRes] = await Promise.all([
        jobsApi.getAll(),
        resumesApi.getAll(),
        schedulesApi.getAll(),
      ])

      const jobs = jobsRes.data
      setStats({
        totalJobs: jobs.length,
        appliedJobs: jobs.filter((j: { status: string }) => j.status === 'applied').length,
        totalResumes: resumesRes.data.length,
        activeSchedules: schedulesRes.data.filter((s: { is_active: boolean }) => s.is_active).length,
      })
    } catch (error) {
      console.error('Failed to load stats:', error)
    }
  }

  const handleSaveProfile = async () => {
    try {
      await updateUser({ full_name: fullName, skills, keywords })
      setIsEditing(false)
    } catch (error) {
      console.error('Failed to update profile:', error)
    }
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">💼</div>
          <div className="stat-info">
            <span className="stat-value">{stats.totalJobs}</span>
            <span className="stat-label">Total Jobs</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-info">
            <span className="stat-value">{stats.appliedJobs}</span>
            <span className="stat-label">Applied</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📄</div>
          <div className="stat-info">
            <span className="stat-value">{stats.totalResumes}</span>
            <span className="stat-label">Resumes</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⏰</div>
          <div className="stat-info">
            <span className="stat-value">{stats.activeSchedules}</span>
            <span className="stat-label">Active Schedules</span>
          </div>
        </div>
      </div>

      <div className="profile-section card">
        <div className="flex flex-between flex-center mb-4">
          <h2>Your Profile</h2>
          {!isEditing && (
            <button onClick={() => setIsEditing(true)}>Edit Profile</button>
          )}
        </div>

        {isEditing ? (
          <div className="profile-form">
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Your full name"
              />
            </div>
            <div className="form-group">
              <label>Skills (comma-separated)</label>
              <input
                type="text"
                value={skills}
                onChange={(e) => setSkills(e.target.value)}
                placeholder="e.g., Python, JavaScript, React"
              />
            </div>
            <div className="form-group">
              <label>Keywords (comma-separated)</label>
              <input
                type="text"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                placeholder="e.g., remote, startup, full-time"
              />
            </div>
            <div className="flex gap-2">
              <button className="btn-primary" onClick={handleSaveProfile}>
                Save Changes
              </button>
              <button onClick={() => setIsEditing(false)}>Cancel</button>
            </div>
          </div>
        ) : (
          <div className="profile-info">
            <p><strong>Email:</strong> {user?.email}</p>
            <p><strong>Name:</strong> {user?.full_name || 'Not set'}</p>
            <p><strong>Skills:</strong> {user?.skills || 'Not set'}</p>
            <p><strong>Keywords:</strong> {user?.keywords || 'Not set'}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard
