"use client"
import { Activity } from "lucide-react" // Import Activity icon

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "./ui/card"
import { Button } from "./ui/button"
import { Badge } from "./ui/badge"
import { Progress } from "@/components/ui/progress"
import { Avatar, AvatarFallback } from "./ui/avatar"
import {
  Package,
  BookOpen,
  FileText,
  CheckCircle,
  Clock,
  TrendingUp,
  Plus,
  Eye,
  Edit,
  BarChart3,
  Users,
  Zap,
  ArrowRight,
} from "lucide-react"
//import { User, Product } from "@/types"
import { Input } from "./ui/input"
import { Label } from "./ui/label"
import { Alert, AlertDescription } from "./ui/alert"
import { Checkbox } from "./ui/checkbox"
//import { Textarea } from "./ui/textarea"

export default function Dashboard({
  user,
  onNavigateToProducts,
  onNavigateToProductForm,
  onNavigateToProduct,
  onLogout,
}) {
  const [metrics, setMetrics] = useState({
    totalProducts: 0,
    totalEpics: 0,
    totalStories: 0,
    totalRequirements: 0,
    pendingReviews: 0,
    completedThisWeek: 0,
  })

  const [recentProducts, setRecentProducts] = useState([])
  const [recentActivities, setRecentActivities] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  // Simular carregamento de dados
  useEffect(() => {
    const loadDashboardData = async () => {
      setIsLoading(true)
      // Troque para o endereço real da sua API
      const apiBase = "http://localhost:8000/dashboard"

      const [metricsRes, productsRes, activitiesRes] = await Promise.all([
        fetch(`${apiBase}/metrics`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }),
        fetch(`${apiBase}/recent-products`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }),
        fetch(`${apiBase}/recent-activities`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }),
      ])

      setMetrics(await metricsRes.json())
      setRecentProducts(await productsRes.json())
      setRecentActivities(await activitiesRes.json())
      setIsLoading(false)
    }
    loadDashboardData()
  }, [])

  const getStatusColor = (status) => {
    switch (status) {
      case "active":
        return "bg-green-100 text-green-800"
      case "draft":
        return "bg-yellow-100 text-yellow-800"
      case "completed":
        return "bg-blue-100 text-blue-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getStatusLabel = (status) => {
    switch (status) {
      case "active":
        return "Ativo"
      case "draft":
        return "Rascunho"
      case "completed":
        return "Concluído"
      default:
        return status
    }
  }

  const getActivityIcon = (type) => {
    switch (type) {
      case "epic_generated":
        return <Zap className="h-4 w-4 text-purple-600" />
      case "story_approved":
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case "requirement_created":
        return <FileText className="h-4 w-4 text-blue-600" />
      case "product_created":
        return <Package className="h-4 w-4 text-orange-600" />
      default:
        return <Activity className="h-4 w-4 text-gray-600" />
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <Package className="h-8 w-8 text-blue-600" />
              <h1 className="text-xl font-bold text-gray-900">Sistema PO</h1>
            </div>

            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">Olá, {user.name || user.email}</span>
              <Avatar>
                <AvatarFallback>
                  {user.name ? user.name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <Button variant="outline" size="sm" onClick={onLogout}>
                Sair
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Bem-vindo ao seu Dashboard</h2>
          <p className="text-gray-600">Gerencie seus produtos, épicos e histórias de usuário em um só lugar.</p>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-4">
            <Button onClick={onNavigateToProductForm} className="flex items-center gap-2">
              <Plus className="h-4 w-4" />
              Novo Produto
            </Button>
            <Button variant="outline" onClick={onNavigateToProducts} className="flex items-center gap-2 bg-transparent">
              <Eye className="h-4 w-4" />
              Ver Todos os Produtos
            </Button>
            <Button variant="outline" className="flex items-center gap-2 bg-transparent">
              <BarChart3 className="h-4 w-4" />
              Relatórios
            </Button>
          </div>
        </div>

        {/* Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total de Produtos</CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metrics.totalProducts}</div>
              <p className="text-xs text-muted-foreground">+2 desde o mês passado</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Épicos Criados</CardTitle>
              <BookOpen className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metrics.totalEpics}</div>
              <p className="text-xs text-muted-foreground">+12 esta semana</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Histórias de Usuário</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metrics.totalStories}</div>
              <p className="text-xs text-muted-foreground">+{metrics.completedThisWeek} aprovadas esta semana</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pendentes de Revisão</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">{metrics.pendingReviews}</div>
              <p className="text-xs text-muted-foreground">Requer sua atenção</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Products */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Package className="h-5 w-5" />
                  Produtos Recentes
                </CardTitle>
                <Button variant="ghost" size="sm" onClick={onNavigateToProducts}>
                  Ver todos
                  <ArrowRight className="h-4 w-4 ml-1" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {recentProducts.map((product) => (
                <div key={product.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{product.name}</h4>
                      <p className="text-sm text-gray-600 mt-1">{product.description}</p>
                    </div>
                    <Badge className={getStatusColor(product.status)}>{getStatusLabel(product.status)}</Badge>
                  </div>

                  <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
                    <div className="flex gap-4">
                      <span>{product.epicsCount} épicos</span>
                      <span>{product.storiesCount} histórias</span>
                      <span>{product.requirementsCount} requisitos</span>
                    </div>
                    <span>{product.lastActivity}</span>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span>Progresso</span>
                      <span>{product.progress}%</span>
                    </div>
                    <Progress value={product.progress} className="h-2" />
                  </div>

                  <div className="flex gap-2 mt-3">
                    <Button size="sm" variant="outline" onClick={() => onNavigateToProduct(product.id)}>
                      <Eye className="h-3 w-3 mr-1" />
                      Ver
                    </Button>
                    <Button size="sm" variant="outline">
                      <Edit className="h-3 w-3 mr-1" />
                      Editar
                    </Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Recent Activities */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5" />
                Atividades Recentes
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentActivities.map((activity) => (
                  <div
                    key={activity.id}
                    className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex-shrink-0 mt-0.5">{getActivityIcon(activity.type)}</div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">{activity.description}</p>
                      <p className="text-sm text-gray-500">
                        {activity.productName} • {activity.timestamp}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-4 pt-4 border-t">
                <Button variant="ghost" size="sm" className="w-full">
                  Ver todas as atividades
                  <ArrowRight className="h-4 w-4 ml-1" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Stats */}
        <div className="mt-8">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Estatísticas Rápidas
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">{metrics.totalRequirements}</div>
                  <p className="text-sm text-gray-600">Requisitos Funcionais</p>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">
                    {Math.round((metrics.totalStories / metrics.totalEpics) * 10) / 10}
                  </div>
                  <p className="text-sm text-gray-600">Histórias por Épico (média)</p>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">{metrics.completedThisWeek}</div>
                  <p className="text-sm text-gray-600">Itens Concluídos esta Semana</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
