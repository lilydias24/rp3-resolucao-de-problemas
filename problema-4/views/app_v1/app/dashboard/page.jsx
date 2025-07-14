"use client"

import { useState, useEffect } from "react"
import { DashboardLayout } from "@/components/Layout/DashboardLayout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuth } from "@/contexts/AuthContext"
import { Package, BookOpen, FileText, CheckSquare, List, TrendingUp, AlertCircle } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

export default function DashboardPage() {
  const [stats, setStats] = useState({
    products: 0,
    epics: 0,
    stories: 0,
    requirements: 0,
    backlogs: 0,
  })
  const [recentProducts, setRecentProducts] = useState([])
  const [recentActivity, setRecentActivity] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const { getAuthHeaders } = useAuth()

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const headers = getAuthHeaders()

      // Tentar buscar dados reais da API
      try {
        const productsResponse = await fetch("http://localhost:8000/dashboard/recent-products", {
          headers,
        })

        if (productsResponse.ok) {
          const products = await productsResponse.json()
          setRecentProducts(products)
          setStats((prev) => ({ ...prev, products: products.length }))
        } else {
          throw new Error("API não disponível")
        }
      } catch (apiError) {
        console.warn("API não disponível, usando dados mock:", apiError)

        // Usar dados mock quando a API não estiver disponível
        const mockProducts = [
          {
            id: 1,
            name: "Sistema de E-commerce",
            description: "Plataforma completa para vendas online",
            value_proposition: "Facilitar vendas para pequenos comerciantes",
            platforms: ["web", "mobile"],
            created_at: new Date().toISOString(),
          },
          {
            id: 2,
            name: "App de Delivery",
            description: "Aplicativo para entrega de comida",
            value_proposition: "Conectar restaurantes e clientes",
            platforms: ["mobile"],
            created_at: new Date().toISOString(),
          },
          {
            id: 3,
            name: "Sistema de Gestão",
            description: "ERP para pequenas empresas",
            value_proposition: "Automatizar processos empresariais",
            platforms: ["web", "desktop"],
            created_at: new Date().toISOString(),
          },
        ]

        const mockStats = {
          products: 3,
          epics: 8,
          stories: 24,
          requirements: 16,
          backlogs: 2,
        }

        const mockActivity = [
          {
            id: 1,
            type: "product",
            title: "Sistema de E-commerce criado",
            timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 min atrás
            user: "Usuário Demo",
          },
          {
            id: 2,
            type: "epic",
            title: "Épico de Pagamentos aprovado",
            timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2h atrás
            user: "Usuário Demo",
          },
          {
            id: 3,
            type: "story",
            title: "História de login implementada",
            timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString(), // 4h atrás
            user: "Usuário Demo",
          },
        ]

        setRecentProducts(mockProducts)
        setStats(mockStats)
        setRecentActivity(mockActivity)
        setError("Usando dados de demonstração (API não conectada)")
      }
    } catch (error) {
      console.error("Erro ao buscar dados do dashboard:", error)
      setError("Erro ao carregar dados do dashboard")
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
      bgColor: "bg-blue-50",
    },
    {
      title: "Épicos",
      value: stats.epics,
      icon: BookOpen,
      description: "Épicos criados",
      color: "text-green-600",
      bgColor: "bg-green-50",
    },
    {
      title: "Histórias",
      value: stats.stories,
      icon: FileText,
      description: "Histórias de usuário",
      color: "text-purple-600",
      bgColor: "bg-purple-50",
    },
    {
      title: "Requisitos",
      value: stats.requirements,
      icon: CheckSquare,
      description: "Requisitos funcionais",
      color: "text-orange-600",
      bgColor: "bg-orange-50",
    },
    {
      title: "Backlogs",
      value: stats.backlogs,
      icon: List,
      description: "Backlogs gerados",
      color: "text-red-600",
      bgColor: "bg-red-50",
    },
  ]

  const getActivityIcon = (type) => {
    const icons = {
      product: Package,
      epic: BookOpen,
      story: FileText,
      requirement: CheckSquare,
      backlog: List,
    }
    return icons[type] || TrendingUp
  }

  const getActivityColor = (type) => {
    const colors = {
      product: "text-blue-600",
      epic: "text-green-600",
      story: "text-purple-600",
      requirement: "text-orange-600",
      backlog: "text-red-600",
    }
    return colors[type] || "text-gray-600"
  }

  const formatTimeAgo = (timestamp) => {
    const now = new Date()
    const time = new Date(timestamp)
    const diffInMinutes = Math.floor((now - time) / (1000 * 60))

    if (diffInMinutes < 60) {
      return `${diffInMinutes}m atrás`
    } else if (diffInMinutes < 1440) {
      return `${Math.floor(diffInMinutes / 60)}h atrás`
    } else {
      return `${Math.floor(diffInMinutes / 1440)}d atrás`
    }
  }

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
        {/* Header tecnológico */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 p-8 text-white">
          <div className="absolute inset-0 bg-black/20"></div>
          <div className="relative z-10">
            <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
            <p className="text-white/80">Visão geral do sistema de gerenciamento de histórias</p>
          </div>
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/10 rounded-full translate-y-12 -translate-x-12"></div>
        </div>

        {/* Alerta de status da API */}
        {error && (
          <Alert className="border-yellow-200 bg-yellow-50">
            <AlertCircle className="h-4 w-4 text-yellow-600" />
            <AlertDescription className="text-yellow-800">{error}</AlertDescription>
          </Alert>
        )}

        {/* Cards de estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          {statCards.map((stat) => (
            <Card key={stat.title} className="hover:shadow-lg transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <stat.icon className={`h-4 w-4 ${stat.color}`} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-muted-foreground">{stat.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Grid principal */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Produtos Recentes */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package className="h-5 w-5" />
                Produtos Recentes
              </CardTitle>
              <CardDescription>Últimos produtos cadastrados no sistema</CardDescription>
            </CardHeader>
            <CardContent>
              {recentProducts.length > 0 ? (
                <div className="space-y-4">
                  {recentProducts.slice(0, 5).map((product) => (
                    <div
                      key={product.id}
                      className="flex items-start space-x-4 p-3 rounded-lg hover:bg-muted/50 transition-colors"
                    >
                      <div className="p-2 bg-blue-50 rounded-lg">
                        <Package className="h-4 w-4 text-blue-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">{product.name}</p>
                        <p className="text-sm text-muted-foreground truncate">{product.description}</p>
                        {product.platforms && (
                          <div className="flex gap-1 mt-1">
                            {product.platforms.slice(0, 2).map((platform) => (
                              <span
                                key={platform}
                                className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800"
                              >
                                {platform}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                      <div className="flex-shrink-0">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          ID: {product.id}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <Package className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-sm text-muted-foreground">Nenhum produto cadastrado ainda</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Atividade Recente */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Atividade Recente
              </CardTitle>
              <CardDescription>Últimas ações realizadas no sistema</CardDescription>
            </CardHeader>
            <CardContent>
              {recentActivity.length > 0 ? (
                <div className="space-y-4">
                  {recentActivity.map((activity) => {
                    const ActivityIcon = getActivityIcon(activity.type)
                    return (
                      <div
                        key={activity.id}
                        className="flex items-start space-x-4 p-3 rounded-lg hover:bg-muted/50 transition-colors"
                      >
                        <div className="p-2 bg-gray-50 rounded-lg">
                          <ActivityIcon className={`h-4 w-4 ${getActivityColor(activity.type)}`} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium">{activity.title}</p>
                          <p className="text-sm text-muted-foreground">por {activity.user}</p>
                        </div>
                        <div className="flex-shrink-0">
                          <span className="text-xs text-muted-foreground">{formatTimeAgo(activity.timestamp)}</span>
                        </div>
                      </div>
                    )
                  })}
                </div>
              ) : (
                <div className="text-center py-8">
                  <TrendingUp className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-sm text-muted-foreground">Nenhuma atividade recente</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Cards de ação rápida */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardContent className="p-6 text-center">
              <div className="p-3 bg-blue-50 rounded-lg w-fit mx-auto mb-3">
                <Package className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="font-medium mb-1">Criar Produto</h3>
              <p className="text-sm text-muted-foreground">Cadastre um novo produto</p>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardContent className="p-6 text-center">
              <div className="p-3 bg-green-50 rounded-lg w-fit mx-auto mb-3">
                <BookOpen className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="font-medium mb-1">Gerar Épicos</h3>
              <p className="text-sm text-muted-foreground">Use IA para criar épicos</p>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardContent className="p-6 text-center">
              <div className="p-3 bg-purple-50 rounded-lg w-fit mx-auto mb-3">
                <FileText className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="font-medium mb-1">Criar Histórias</h3>
              <p className="text-sm text-muted-foreground">Gere histórias de usuário</p>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardContent className="p-6 text-center">
              <div className="p-3 bg-orange-50 rounded-lg w-fit mx-auto mb-3">
                <CheckSquare className="h-6 w-6 text-orange-600" />
              </div>
              <h3 className="font-medium mb-1">Gerar Requisitos</h3>
              <p className="text-sm text-muted-foreground">Crie requisitos funcionais</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
