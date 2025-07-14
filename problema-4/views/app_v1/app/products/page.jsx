"use client"

import { useState } from "react"
import { DashboardLayout } from "@/components/Layout/DashboardLayout"
import { ProductList } from "@/components/Products/ProductList"
import { ProductForm } from "@/components/Products/ProductForm"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

export default function ProductsPage() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)

  const handleProductCreated = (newProduct) => {
    setProducts((prev) => [...prev, newProduct])
    setIsCreateDialogOpen(false)
  }

  const handleProductUpdated = (updatedProduct) => {
    setProducts((prev) => prev.map((p) => (p.id === updatedProduct.id ? updatedProduct : p)))
  }

  const handleProductDeleted = (productId) => {
    setProducts((prev) => prev.filter((p) => p.id !== productId))
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Produtos</h1>
            <p className="text-muted-foreground">Gerencie os produtos do sistema</p>
          </div>

          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Novo Produto
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>Criar Novo Produto</DialogTitle>
                <DialogDescription>Preencha as informações do produto para começar a gerar histórias</DialogDescription>
              </DialogHeader>
              <ProductForm onSuccess={handleProductCreated} onCancel={() => setIsCreateDialogOpen(false)} />
            </DialogContent>
          </Dialog>
        </div>

        <ProductList
          products={products}
          setProducts={setProducts}
          loading={loading}
          setLoading={setLoading}
          onProductUpdated={handleProductUpdated}
          onProductDeleted={handleProductDeleted}
        />
      </div>
    </DashboardLayout>
  )
}
