import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Layout.css'

function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const isActive = (path: string) => location.pathname === path

  return (
    <div className="layout">
      <nav className="sidebar">
        <div className="sidebar-header">
          <h2>Job Search</h2>
          <span className="user-email">{user?.email}</span>
        </div>
        <ul className="nav-links">
          <li>
            <Link to="/" className={isActive('/') ? 'active' : ''}>
              📊 Dashboard
            </Link>
          </li>
          <li>
            <Link to="/jobs" className={isActive('/jobs') ? 'active' : ''}>
              💼 Jobs
            </Link>
          </li>
          <li>
            <Link to="/resumes" className={isActive('/resumes') ? 'active' : ''}>
              📄 Resumes
            </Link>
          </li>
          <li>
            <Link to="/schedules" className={isActive('/schedules') ? 'active' : ''}>
              ⏰ Schedules
            </Link>
          </li>
        </ul>
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </nav>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
