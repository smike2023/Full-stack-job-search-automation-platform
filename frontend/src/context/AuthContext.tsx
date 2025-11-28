import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { authApi, userApi } from '../services/api'

interface User {
  id: number
  email: string
  full_name?: string
  skills?: string
  keywords?: string
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, fullName?: string, skills?: string, keywords?: string) => Promise<void>
  logout: () => void
  updateUser: (data: { full_name?: string; skills?: string; keywords?: string }) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      userApi.getMe()
        .then(response => setUser(response.data))
        .catch(() => localStorage.removeItem('token'))
        .finally(() => setIsLoading(false))
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    const response = await authApi.login({ email, password })
    localStorage.setItem('token', response.data.access_token)
    const userResponse = await userApi.getMe()
    setUser(userResponse.data)
  }

  const register = async (
    email: string,
    password: string,
    fullName?: string,
    skills?: string,
    keywords?: string
  ) => {
    await authApi.register({
      email,
      password,
      full_name: fullName,
      skills,
      keywords,
    })
    await login(email, password)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  const updateUser = async (data: { full_name?: string; skills?: string; keywords?: string }) => {
    const response = await userApi.updateMe(data)
    setUser(response.data)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
