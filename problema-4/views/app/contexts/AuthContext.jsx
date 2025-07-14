"use client"

import { createContext, useContext, useState, useEffect } from "react"
import { useRouter } from "next/navigation"

const AuthContext = createContext({})

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Simular carregamento e definir usuário mock
    setTimeout(() => {
      setUser({
        id: 1,
        name: "Usuário Demo",
        email: "demo@exemplo.com",
        avatar: null,
      })
      setLoading(false)
    }, 1000)
  }, [])

  const login = async (email, password) => {
    // Simular login sempre bem-sucedido
    setUser({
      id: 1,
      name: "Usuário Demo",
      email: email,
      avatar: null,
    })
    router.push("/dashboard")
    return { success: true }
  }

  const register = async (name, email, password) => {
    // Simular registro sempre bem-sucedido
    return { success: true }
  }

  const logout = () => {
    setUser(null)
    router.push("/")
  }

  const getAuthHeaders = () => {
    // Retornar headers mock
    return { Authorization: "Bearer mock-token" }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        getAuthHeaders,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth deve ser usado dentro de AuthProvider")
  }
  return context
}
