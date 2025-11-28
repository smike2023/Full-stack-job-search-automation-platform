import { useState, useEffect } from 'react'
import { schedulesApi } from '../services/api'
import './Schedules.css'

interface Schedule {
  id: number
  name: string
  search_query: string
  location: string | null
  sources: string
  cron_expression: string
  is_active: boolean
  last_run: string | null
  next_run: string | null
  created_at: string
}

function Schedules() {
  const [schedules, setSchedules] = useState<Schedule[]>([])
  const [showForm, setShowForm] = useState(false)
  const [isCreating, setIsCreating] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    searchQuery: '',
    location: '',
    sources: 'all',
    cronExpression: '0 9 * * *', // Daily at 9 AM
  })

  useEffect(() => {
    loadSchedules()
  }, [])

  const loadSchedules = async () => {
    try {
      const response = await schedulesApi.getAll()
      setSchedules(response.data)
    } catch (error) {
      console.error('Failed to load schedules:', error)
    }
  }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.name || !formData.searchQuery || !formData.cronExpression) {
      return
    }

    setIsCreating(true)
    try {
      const response = await schedulesApi.create({
        name: formData.name,
        search_query: formData.searchQuery,
        location: formData.location || undefined,
        sources: formData.sources,
        cron_expression: formData.cronExpression,
      })
      setSchedules([response.data, ...schedules])
      setShowForm(false)
      setFormData({
        name: '',
        searchQuery: '',
        location: '',
        sources: 'all',
        cronExpression: '0 9 * * *',
      })
    } catch (error) {
      console.error('Failed to create schedule:', error)
    } finally {
      setIsCreating(false)
    }
  }

  const handleToggleActive = async (schedule: Schedule) => {
    try {
      if (schedule.is_active) {
        await schedulesApi.deactivate(schedule.id)
      } else {
        await schedulesApi.activate(schedule.id)
      }
      setSchedules(
        schedules.map((s) =>
          s.id === schedule.id ? { ...s, is_active: !s.is_active } : s
        )
      )
    } catch (error) {
      console.error('Failed to toggle schedule:', error)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this schedule?')) return
    try {
      await schedulesApi.delete(id)
      setSchedules(schedules.filter((s) => s.id !== id))
    } catch (error) {
      console.error('Failed to delete schedule:', error)
    }
  }

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return 'Never'
    return new Date(dateStr).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const cronPresets = [
    { label: 'Every hour', value: '0 * * * *' },
    { label: 'Daily at 9 AM', value: '0 9 * * *' },
    { label: 'Every 6 hours', value: '0 */6 * * *' },
    { label: 'Weekdays at 8 AM', value: '0 8 * * 1-5' },
    { label: 'Weekly on Monday', value: '0 9 * * 1' },
  ]

  return (
    <div className="schedules-page">
      <div className="schedules-header">
        <h1>Search Schedules</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Create Schedule'}
        </button>
      </div>

      <p className="description">
        Set up automated job searches that run on a schedule. New jobs will be
        automatically added to your job list.
      </p>

      {showForm && (
        <form className="schedule-form card" onSubmit={handleCreate}>
          <h3>Create New Schedule</h3>
          <div className="form-grid">
            <div className="form-group">
              <label>Schedule Name *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
                placeholder="e.g., Daily Python Jobs"
                required
              />
            </div>
            <div className="form-group">
              <label>Search Query *</label>
              <input
                type="text"
                value={formData.searchQuery}
                onChange={(e) =>
                  setFormData({ ...formData, searchQuery: e.target.value })
                }
                placeholder="e.g., Python Developer"
                required
              />
            </div>
            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                value={formData.location}
                onChange={(e) =>
                  setFormData({ ...formData, location: e.target.value })
                }
                placeholder="e.g., Remote"
              />
            </div>
            <div className="form-group">
              <label>Schedule Frequency</label>
              <select
                value={formData.cronExpression}
                onChange={(e) =>
                  setFormData({ ...formData, cronExpression: e.target.value })
                }
              >
                {cronPresets.map((preset) => (
                  <option key={preset.value} value={preset.value}>
                    {preset.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <button type="submit" className="btn-primary" disabled={isCreating}>
            {isCreating ? 'Creating...' : 'Create Schedule'}
          </button>
        </form>
      )}

      <div className="schedules-list">
        {schedules.length === 0 ? (
          <div className="no-schedules card">
            <p>
              No schedules yet. Create one to automate your job search!
            </p>
          </div>
        ) : (
          schedules.map((schedule) => (
            <div key={schedule.id} className="schedule-card card">
              <div className="schedule-header">
                <div>
                  <h3>{schedule.name}</h3>
                  <p className="query">Search: "{schedule.search_query}"</p>
                  {schedule.location && (
                    <p className="location">📍 {schedule.location}</p>
                  )}
                </div>
                <div className="schedule-status">
                  <span
                    className={`status-badge ${
                      schedule.is_active ? 'active' : 'inactive'
                    }`}
                  >
                    {schedule.is_active ? 'Active' : 'Paused'}
                  </span>
                </div>
              </div>

              <div className="schedule-times">
                <div className="time-info">
                  <span className="label">Cron:</span>
                  <span className="value">{schedule.cron_expression}</span>
                </div>
                <div className="time-info">
                  <span className="label">Last Run:</span>
                  <span className="value">{formatDate(schedule.last_run)}</span>
                </div>
                <div className="time-info">
                  <span className="label">Next Run:</span>
                  <span className="value">{formatDate(schedule.next_run)}</span>
                </div>
              </div>

              <div className="schedule-actions">
                <button
                  className={schedule.is_active ? '' : 'btn-primary'}
                  onClick={() => handleToggleActive(schedule)}
                >
                  {schedule.is_active ? 'Pause' : 'Activate'}
                </button>
                <button
                  className="btn-danger"
                  onClick={() => handleDelete(schedule.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Schedules
