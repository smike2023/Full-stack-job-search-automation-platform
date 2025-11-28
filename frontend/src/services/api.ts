import axios from 'axios'

const API_URL = '/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  register: (data: { email: string; password: string; full_name?: string; skills?: string; keywords?: string }) =>
    api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login/json', data),
}

// User API
export const userApi = {
  getMe: () => api.get('/users/me'),
  updateMe: (data: { full_name?: string; skills?: string; keywords?: string }) =>
    api.put('/users/me', data),
}

// Jobs API
export const jobsApi = {
  search: (data: { query: string; location?: string; sources?: string[] }) =>
    api.post('/jobs/search', data),
  getAll: (params?: { status?: string; min_score?: number }) =>
    api.get('/jobs', { params }),
  get: (id: number) => api.get(`/jobs/${id}`),
  update: (id: number, data: { status?: string }) =>
    api.patch(`/jobs/${id}`, data),
  delete: (id: number) => api.delete(`/jobs/${id}`),
}

// Resumes API
export const resumesApi = {
  generate: (data: {
    target_role: string
    target_company?: string
    user_experience: string
    user_skills: string
    user_education?: string
    job_id?: number
    job_description?: string
  }) => api.post('/resumes/generate', data),
  getAll: () => api.get('/resumes'),
  get: (id: number) => api.get(`/resumes/${id}`),
  update: (id: number, data: { title?: string; content?: string }) =>
    api.put(`/resumes/${id}`, data),
  delete: (id: number) => api.delete(`/resumes/${id}`),
}

// Schedules API
export const schedulesApi = {
  create: (data: {
    name: string
    search_query: string
    location?: string
    sources?: string
    cron_expression: string
  }) => api.post('/schedules', data),
  getAll: () => api.get('/schedules'),
  get: (id: number) => api.get(`/schedules/${id}`),
  update: (id: number, data: {
    name?: string
    search_query?: string
    location?: string
    sources?: string
    cron_expression?: string
    is_active?: boolean
  }) => api.put(`/schedules/${id}`, data),
  delete: (id: number) => api.delete(`/schedules/${id}`),
  activate: (id: number) => api.post(`/schedules/${id}/activate`),
  deactivate: (id: number) => api.post(`/schedules/${id}/deactivate`),
}

export default api
