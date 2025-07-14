"use client"

import { useState } from "react"
import LoginForm from "../components/loginForm"
import ProductForm from "../components/productForm"
import Dashboard from "../components/dashboard"

export default function Home() {
  const [currentScreen, setCurrentScreen] = useState("login") // "login" | "product-form" | "dashboard" | "products"
  const [user, setUser] = useState(null)

  const handleLogin = async (email, password) => {
    await new Promise((resolve) => setTimeout(resolve, 1000))
    if (email && password) {
      setUser({ email })
      setCurrentScreen("dashboard")
    } else {
      throw new Error("Credenciais inválidas")
    }
  }

  const handleProductSubmit = async (productData) => {
    await new Promise((resolve) => setTimeout(resolve, 1500))
    alert("Produto cadastrado com sucesso!")
    setCurrentScreen("dashboard")
  }

  const handleLogout = () => {
    setUser(null)
    setCurrentScreen("login")
  }

  const handleNavigateToProducts = () => setCurrentScreen("products")
  const handleNavigateToProductForm = () => setCurrentScreen("product-form")
  const handleNavigateToProduct = (productId) => {
    console.log("Navigate to product:", productId)
    // Implement navigation to product details
  }

  if (currentScreen === "login") {
    return <LoginForm onLogin={handleLogin} />
  }

  if (currentScreen === "product-form") {
    return <ProductForm onSubmit={handleProductSubmit} onBack={() => setCurrentScreen("dashboard")} />
  }

  if (currentScreen === "dashboard") {
    return (
      <Dashboard
        user={user}
        onNavigateToProducts={handleNavigateToProducts}
        onNavigateToProductForm={handleNavigateToProductForm}
        onNavigateToProduct={handleNavigateToProduct}
        onLogout={handleLogout}
      />
    )
  }

  // Dashboard placeholder
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold">Dashboard - Sistema PO</h1>
            <button onClick={handleLogout} className="text-blue-600 hover:text-blue-800">
              Sair
            </button>
          </div>
          <p className="text-gray-600">
            Bem-vindo, {user?.email}! Aqui você poderá gerenciar seus produtos e histórias de usuário.
          </p>
          <div className="mt-4">
            <button
              onClick={() => setCurrentScreen("product-form")}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Cadastrar Novo Produto
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
