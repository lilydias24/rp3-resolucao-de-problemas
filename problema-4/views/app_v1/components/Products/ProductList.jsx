"use client"

import { useState, useEffect } from "react"
import { useAuth } from "@/contexts/AuthContext"
import { useNotification } from "@/contexts/NotificationContext"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ProductForm } from "./ProductForm"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { Edit, Trash2, Eye, Package, AlertCircle } from "lucide-react"

export function ProductList({ products, setProducts, loading, setLoading, onProductUpdated, onProductDeleted }) {
  const [editingProduct, setEditingProduct] = useState(null)
  const [deletingProduct, setDeletingProduct] = useState(null)
  const [viewingProduct, setViewingProduct] = useState(null)
  const [error, setError] = useState("")
  const { getAuthHeaders } = useAuth()
  const { showSuccess, showError } = useNotification()

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      const headers = getAuthHeaders()

      try {
        const response = await fetch("http://localhost:8000/dashboard/recent-products", {
          headers,
        })

        if (response.ok) {
          const data = await response.json()
          setProducts(data)
          setError("")
        } else {
          throw new Error("API não disponível")
        }
      } catch (apiError) {
        console.warn("API não disponível, usando dados mock:", apiError)

        // Dados mock para demonstração
        const mockProducts = [
          {
            id: 1,
            name: "Sistema de E-commerce",
            description: "Plataforma completa para vendas online com carrinho, pagamentos e gestão de produtos",
            value_proposition: "Facilitar vendas online para pequenos e médios comerciantes",
            platforms: ["web", "mobile"],
            created_at: new Date().toISOString(),
          },
          {
            id: 2,
            name: "App de Delivery",
            description: "Aplicativo para entrega de comida conectando restaurantes e clientes",
            value_proposition: "Conectar restaurantes e clientes de forma eficiente",
            platforms: ["mobile"],
            created_at: new Date().toISOString(),
          },
          {
            id: 3,
            name: "Sistema de Gestão Empresarial",
            description: "ERP completo para pequenas empresas com módulos financeiro, estoque e vendas",
            value_proposition: "Automatizar processos empresariais e aumentar produtividade",
            platforms: ["web", "desktop"],
            created_at: new Date().toISOString(),
          },
        ]

        setProducts(mockProducts)
        setError("Usando dados de demonstração (API não conectada)")
      }
    } catch (error) {
      showError("Erro de conexão")
      setError("Erro ao carregar produtos")
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (productId) => {
    try {
      const headers = getAuthHeaders()

      try {
        const response = await fetch(`http://localhost:8000/products/${productId}`, {
          method: "DELETE",
          headers,
        })

        if (response.ok) {
          showSuccess("Produto removido com sucesso!")
          onProductDeleted(productId)
        } else {
          throw new Error("API não disponível")
        }
      } catch (apiError) {
        // Simular exclusão nos dados mock
        showSuccess("Produto removido com sucesso! (modo demonstração)")
        onProductDeleted(productId)
      }
    } catch (error) {
      showError("Erro de conexão")
    }
    setDeletingProduct(null)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <>
      {error && (
        <Alert className="mb-6 border-yellow-200 bg-yellow-50">
          <AlertCircle className="h-4 w-4 text-yellow-600" />
          <AlertDescription className="text-yellow-800">{error}</AlertDescription>
        </Alert>
      )}

      {products.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16">
            <Package className="h-16 w-16 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">Nenhum produto encontrado</h3>
            <p className="text-muted-foreground text-center mb-4">
              Comece criando seu primeiro produto para gerar histórias de usuário
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <Card key={product.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg">{product.name}</CardTitle>
                    <CardDescription className="mt-1">{product.description}</CardDescription>
                  </div>
                  <Badge variant="secondary">ID: {product.id}</Badge>
                </div>
              </CardHeader>
              <CardContent>
                {product.value_proposition && (
                  <div className="mb-4">
                    <h4 className="text-sm font-medium mb-1">Proposta de Valor:</h4>
                    <p className="text-sm text-muted-foreground">{product.value_proposition}</p>
                  </div>
                )}

                {product.platforms && product.platforms.length > 0 && (
                  <div className="mb-4">
                    <h4 className="text-sm font-medium mb-2">Plataformas:</h4>
                    <div className="flex flex-wrap gap-1">
                      {product.platforms.map((platform) => (
                        <Badge key={platform} variant="outline" className="text-xs">
                          {platform}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex gap-2 mt-4">
                  <Button variant="outline" size="sm" onClick={() => setViewingProduct(product)}>
                    <Eye className="h-4 w-4 mr-1" />
                    Ver
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => setEditingProduct(product)}>
                    <Edit className="h-4 w-4 mr-1" />
                    Editar
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => setDeletingProduct(product)}>
                    <Trash2 className="h-4 w-4 mr-1" />
                    Excluir
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Dialog de Edição */}
      <Dialog open={!!editingProduct} onOpenChange={() => setEditingProduct(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Editar Produto</DialogTitle>
            <DialogDescription>Atualize as informações do produto</DialogDescription>
          </DialogHeader>
          {editingProduct && (
            <ProductForm
              product={editingProduct}
              onSuccess={(updatedProduct) => {
                onProductUpdated(updatedProduct)
                setEditingProduct(null)
              }}
              onCancel={() => setEditingProduct(null)}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Dialog de Visualização */}
      <Dialog open={!!viewingProduct} onOpenChange={() => setViewingProduct(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Detalhes do Produto</DialogTitle>
          </DialogHeader>
          {viewingProduct && (
            <div className="space-y-4">
              <div>
                <h4 className="font-medium">Nome:</h4>
                <p className="text-muted-foreground">{viewingProduct.name}</p>
              </div>
              <div>
                <h4 className="font-medium">Descrição:</h4>
                <p className="text-muted-foreground">{viewingProduct.description}</p>
              </div>
              {viewingProduct.value_proposition && (
                <div>
                  <h4 className="font-medium">Proposta de Valor:</h4>
                  <p className="text-muted-foreground">{viewingProduct.value_proposition}</p>
                </div>
              )}
              {viewingProduct.platforms && (
                <div>
                  <h4 className="font-medium">Plataformas:</h4>
                  <div className="flex flex-wrap gap-2 mt-1">
                    {viewingProduct.platforms.map((platform) => (
                      <Badge key={platform} variant="outline">
                        {platform}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
              <div>
                <h4 className="font-medium">ID:</h4>
                <p className="text-muted-foreground">{viewingProduct.id}</p>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Dialog de Confirmação de Exclusão */}
      <AlertDialog open={!!deletingProduct} onOpenChange={() => setDeletingProduct(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Confirmar Exclusão</AlertDialogTitle>
            <AlertDialogDescription>
              Tem certeza que deseja excluir o produto "{deletingProduct?.name}"? Esta ação não pode ser desfeita.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => handleDelete(deletingProduct.id)}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Excluir
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  )
}
