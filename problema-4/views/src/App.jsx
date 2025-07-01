import React, { useState } from "react"
import { BrowserRouter, Routes, Route, useNavigate, Navigate } from "react-router-dom"
import LoginForm from "./components/loginForm"
import Dashboard from "./components/dashboard"
import ProductForm from "./components/productForm"

// Wrapper para usar hooks de navegação fora do App principal
function AppRoutes({ user, setUser }) {
  const navigate = useNavigate()

  // Simulação de login
  const handleLogin = async (email, password) => {
    if (email && password) {
      setUser({ email, name: email.split("@")[0] })
      navigate("/dashboard")
    } else {
      throw new Error("Credenciais inválidas")
    }
  }

  // Simulação de logout
  const handleLogout = () => {
    setUser(null)
    navigate("/login")
  }

  // Navegar para cadastro de produto
  const handleNavigateToProductForm = () => navigate("/produto-novo")
  // Voltar para dashboard
  const handleBackToDashboard = () => navigate("/dashboard")

  // Simulação de cadastro de produto
  const handleProductSubmit = async (productData) => {
    alert("Produto cadastrado com sucesso!\n" + JSON.stringify(productData, null, 2))
    navigate("/dashboard")
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={<LoginForm onLogin={handleLogin} />}
      />
      <Route
        path="/dashboard"
        element={user ? (
          <Dashboard
            user={user}
            onNavigateToProducts={() => {}}
            onNavigateToProductForm={handleNavigateToProductForm}
            onNavigateToProduct={() => {}}
            onLogout={handleLogout}
          />
        ) : (
          <Navigate to="/login" replace />
        )}
      />
      <Route
        path="/produto-novo"
        element={user ? (
          <ProductForm onSubmit={handleProductSubmit} onBack={handleBackToDashboard} />
        ) : (
          <Navigate to="/login" replace />
        )}
      />
      {/* Redirecionamento padrão */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}

function App() {
  const [user, setUser] = useState(null)
  return (
    <BrowserRouter>
      <AppRoutes user={user} setUser={setUser} />
      <div className="bg-red-500 text-white p-10">TESTE TAILWIND</div>
    </BrowserRouter>
  )
}

export default App
