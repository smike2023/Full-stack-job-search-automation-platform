import { useState, useEffect } from 'react'
import { jobsApi } from '../services/api'
import './Jobs.css'

interface Job {
  id: number
  title: string
  company: string
  location: string
  description: string
  url: string
  source: string
  salary_min: number | null
  salary_max: number | null
  match_score: number
  matched_skills: string | null
  matched_keywords: string | null
  status: string
  created_at: string
}

function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [query, setQuery] = useState('')
  const [location, setLocation] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [selectedJob, setSelectedJob] = useState<Job | null>(null)

  useEffect(() => {
    loadJobs()
  }, [statusFilter])

  const loadJobs = async () => {
    try {
      const params: { status?: string } = {}
      if (statusFilter) params.status = statusFilter
      const response = await jobsApi.getAll(params)
      setJobs(response.data)
    } catch (error) {
      console.error('Failed to load jobs:', error)
    }
  }

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setIsSearching(true)
    try {
      await jobsApi.search({
        query: query.trim(),
        location: location.trim() || undefined,
        sources: ['mock'],
      })
      await loadJobs()
      setQuery('')
      setLocation('')
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setIsSearching(false)
    }
  }

  const handleStatusChange = async (jobId: number, newStatus: string) => {
    try {
      await jobsApi.update(jobId, { status: newStatus })
      setJobs(jobs.map((j) => (j.id === jobId ? { ...j, status: newStatus } : j)))
      if (selectedJob?.id === jobId) {
        setSelectedJob({ ...selectedJob, status: newStatus })
      }
    } catch (error) {
      console.error('Failed to update status:', error)
    }
  }

  const handleDelete = async (jobId: number) => {
    if (!confirm('Are you sure you want to delete this job?')) return
    try {
      await jobsApi.delete(jobId)
      setJobs(jobs.filter((j) => j.id !== jobId))
      if (selectedJob?.id === jobId) setSelectedJob(null)
    } catch (error) {
      console.error('Failed to delete job:', error)
    }
  }

  const getStatusBadge = (status: string) => {
    const classes: Record<string, string> = {
      new: 'badge-info',
      applied: 'badge-success',
      interview: 'badge-warning',
      rejected: 'badge-danger',
    }
    return `badge ${classes[status] || 'badge-info'}`
  }

  const getScoreColor = (score: number) => {
    if (score >= 70) return '#2ed573'
    if (score >= 40) return '#ffa502'
    return '#ff4757'
  }

  return (
    <div className="jobs-page">
      <h1>Jobs</h1>

      <form className="search-form card" onSubmit={handleSearch}>
        <div className="search-inputs">
          <input
            type="text"
            placeholder="Job title or keywords"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <input
            type="text"
            placeholder="Location (optional)"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
          <button type="submit" className="btn-primary" disabled={isSearching}>
            {isSearching ? 'Searching...' : 'Search Jobs'}
          </button>
        </div>
      </form>

      <div className="jobs-filters">
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All Status</option>
          <option value="new">New</option>
          <option value="applied">Applied</option>
          <option value="interview">Interview</option>
          <option value="rejected">Rejected</option>
        </select>
      </div>

      <div className="jobs-container">
        <div className="jobs-list">
          {jobs.length === 0 ? (
            <div className="no-jobs card">
              <p>No jobs found. Start by searching for jobs above!</p>
            </div>
          ) : (
            jobs.map((job) => (
              <div
                key={job.id}
                className={`job-card card ${selectedJob?.id === job.id ? 'selected' : ''}`}
                onClick={() => setSelectedJob(job)}
              >
                <div className="job-header">
                  <h3>{job.title}</h3>
                  <span className={getStatusBadge(job.status)}>{job.status}</span>
                </div>
                <p className="company">{job.company}</p>
                <p className="location">📍 {job.location}</p>
                <div className="job-meta">
                  <span
                    className="score"
                    style={{ color: getScoreColor(job.match_score) }}
                  >
                    Match: {job.match_score}%
                  </span>
                  {job.salary_min && job.salary_max && (
                    <span className="salary">
                      ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

        {selectedJob && (
          <div className="job-detail card">
            <h2>{selectedJob.title}</h2>
            <p className="company">{selectedJob.company}</p>
            <p className="location">📍 {selectedJob.location}</p>

            <div className="match-info">
              <div
                className="match-score"
                style={{ borderColor: getScoreColor(selectedJob.match_score) }}
              >
                <span style={{ color: getScoreColor(selectedJob.match_score) }}>
                  {selectedJob.match_score}%
                </span>
                <small>Match</small>
              </div>
              {selectedJob.matched_skills && (
                <div className="matched-items">
                  <strong>Matched Skills:</strong>
                  <p>{selectedJob.matched_skills}</p>
                </div>
              )}
              {selectedJob.matched_keywords && (
                <div className="matched-items">
                  <strong>Matched Keywords:</strong>
                  <p>{selectedJob.matched_keywords}</p>
                </div>
              )}
            </div>

            {selectedJob.salary_min && selectedJob.salary_max && (
              <p className="salary-detail">
                💰 ${selectedJob.salary_min.toLocaleString()} - $
                {selectedJob.salary_max.toLocaleString()}
              </p>
            )}

            <div className="description">
              <h4>Description</h4>
              <p>{selectedJob.description}</p>
            </div>

            <div className="job-actions">
              <select
                value={selectedJob.status}
                onChange={(e) => handleStatusChange(selectedJob.id, e.target.value)}
              >
                <option value="new">New</option>
                <option value="applied">Applied</option>
                <option value="interview">Interview</option>
                <option value="rejected">Rejected</option>
              </select>
              <a
                href={selectedJob.url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary"
              >
                View Job
              </a>
              <button
                className="btn-danger"
                onClick={() => handleDelete(selectedJob.id)}
              >
                Delete
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Jobs
