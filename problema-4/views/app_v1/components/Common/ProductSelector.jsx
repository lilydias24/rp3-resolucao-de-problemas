"use client"

import { useState, useEffect } from "react"
import { useAuth } from "@/contexts/AuthContext"
import { useNotification } from "@/contexts/NotificationContext"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"

export function ProductSelector({ selectedProductId, onProductChange }) {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const { getAuthHeaders } = useAuth()
  const { showError } = useNotification()

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      const headers = getAuthHeaders()
      const response = await fetch("http://localhost:8000/dashboard/recent-products", {
        headers,
      })

      if (response.ok) {
        const data = await response.json()
        setProducts(data)
      } else {
        showError("Erro ao carregar produtos")
      }
    } catch (error) {
      showError("Erro de conexão")
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-2">
        <Label>Produto</Label>
        <div className="h-10 bg-muted animate-pulse rounded-md"></div>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <Label>Selecione um Produto</Label>
      <Select value={selectedProductId} onValueChange={onProductChange}>
        <SelectTrigger>
          <SelectValue placeholder="Escolha um produto..." />
        </SelectTrigger>
        <SelectContent>
          {products.map((product) => (
            <SelectItem key={product.id} value={product.id.toString()}>
              {product.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}
