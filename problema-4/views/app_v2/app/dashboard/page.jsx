"use client"

import { useState, useEffect } from "react"
import { DashboardLayout } from "@/components/Layout/DashboardLayout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuth } from "@/contexts/AuthContext"
import { Package, BookOpen, FileText, CheckSquare, List, TrendingUp } from "lucide-react"

export default function DashboardPage() {
  const [stats, setStats] = useState({
    products: 0,
    epics: 0,
    stories: 0,
    requirements: 0,
    backlogs: 0,
  })
  const [recentProducts, setRecentProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const { getAuthHeaders } = useAuth()

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const headers = getAuthHeaders()

      // Buscar produtos recentes
      const productsResponse = await fetch("http://localhost:8000/dashboard/recent-products", {
        headers,
      })

      if (productsResponse.ok) {
        const products = await productsResponse.json()
        setRecentProducts(products)
        setStats((prev) => ({ ...prev, products: products.length }))
      }
    } catch (error) {
      console.error("Erro ao buscar dados do dashboard:", error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: "Produtos",
      value: stats.products,
      icon: Package,
      description: "Total de produtos cadastrados",
      color: "text-blue-600",
    },
    {
      title: "Épicos",
      value: stats.epics,
      icon: BookOpen,
      description: "Épicos criados",
      color: "text-green-600",
    },
    {
      title: "Histórias",
      value: stats.stories,
      icon: FileText,
      description: "Histórias de usuário",
      color: "text-purple-600",
    },
    {
      title: "Requisitos",
      value: stats.requirements,
      icon: CheckSquare,
      description: "Requisitos funcionais",
      color: "text-orange-600",
    },
    {
      title: "Backlogs",
      value: stats.backlogs,
      icon: List,
      description: "Backlogs gerados",
      color: "text-red-600",
    },
  ]

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Visão geral do sistema de gerenciamento de histórias</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          {statCards.map((stat) => (
            <Card key={stat.title}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <stat.icon className={`h-4 w-4 ${stat.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-muted-foreground">{stat.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Produtos Recentes</CardTitle>
              <CardDescription>Últimos produtos cadastrados no sistema</CardDescription>
            </CardHeader>
            <CardContent>
              {recentProducts.length > 0 ? (
                <div className="space-y-4">
                  {recentProducts.slice(0, 5).map((product) => (
                    <div key={product.id} className="flex items-center space-x-4">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">{product.name}</p>
                        <p className="text-sm text-muted-foreground truncate">{product.description}</p>
                      </div>
                      <div className="flex-shrink-0">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          ID: {product.id}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">Nenhum produto cadastrado ainda</p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Atividade Recente</CardTitle>
              <CardDescription>Últimas ações realizadas no sistema</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  <TrendingUp className="h-4 w-4 text-green-600" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium">Sistema iniciado</p>
                    <p className="text-sm text-muted-foreground">Dashboard carregado com sucesso</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
