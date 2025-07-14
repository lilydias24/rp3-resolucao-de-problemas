"use client"

import { useState } from "react"
import { useAuth } from "@/contexts/AuthContext"
import { useNotification } from "@/contexts/NotificationContext"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Checkbox } from "@/components/ui/checkbox"

const PLATFORM_OPTIONS = [
  { id: "web", label: "Web" },
  { id: "mobile", label: "Mobile" },
  { id: "desktop", label: "Desktop" },
  { id: "api", label: "API" },
]

export function ProductForm({ product, onSuccess, onCancel }) {
  const [formData, setFormData] = useState({
    name: product?.name || "",
    description: product?.description || "",
    valueProposition: product?.value_proposition || "",
    platforms: product?.platforms || [],
  })
  const [loading, setLoading] = useState(false)
  const { getAuthHeaders } = useAuth()
  const { showSuccess, showError } = useNotification()

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.name.includes(" ")) {
      showError("O nome do produto deve conter pelo menos um espaço")
      return
    }

    setLoading(true)

    try {
      const headers = {
        ...getAuthHeaders(),
        "Content-Type": "application/json",
      }

      const url = product ? `http://localhost:8000/products/${product.id}` : "http://localhost:8000/products/"

      const method = product ? "PUT" : "POST"

      const response = await fetch(url, {
        method,
        headers,
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        const result = await response.json()
        showSuccess(product ? "Produto atualizado com sucesso!" : "Produto criado com sucesso!")
        onSuccess(result)
      } else {
        const error = await response.json()
        showError(error.detail || "Erro ao salvar produto")
      }
    } catch (error) {
      showError("Erro de conexão")
    } finally {
      setLoading(false)
    }
  }

  const handlePlatformChange = (platformId, checked) => {
    setFormData((prev) => ({
      ...prev,
      platforms: checked ? [...prev.platforms, platformId] : prev.platforms.filter((p) => p !== platformId),
    }))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Nome do Produto *</Label>
        <Input
          id="name"
          value={formData.name}
          onChange={(e) => setFormData((prev) => ({ ...prev, name: e.target.value }))}
          placeholder="Nome do produto (deve conter espaço)"
          required
        />
        <p className="text-xs text-muted-foreground">O nome deve conter pelo menos um espaço</p>
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Descrição *</Label>
        <Textarea
          id="description"
          value={formData.description}
          onChange={(e) => setFormData((prev) => ({ ...prev, description: e.target.value }))}
          placeholder="Descrição detalhada do produto"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="valueProposition">Proposta de Valor *</Label>
        <Textarea
          id="valueProposition"
          value={formData.valueProposition}
          onChange={(e) => setFormData((prev) => ({ ...prev, valueProposition: e.target.value }))}
          placeholder="Qual problema o produto resolve?"
          required
        />
      </div>

      <div className="space-y-3">
        <Label>Plataformas *</Label>
        <div className="grid grid-cols-2 gap-3">
          {PLATFORM_OPTIONS.map((platform) => (
            <div key={platform.id} className="flex items-center space-x-2">
              <Checkbox
                id={platform.id}
                checked={formData.platforms.includes(platform.id)}
                onCheckedChange={(checked) => handlePlatformChange(platform.id, checked)}
              />
              <Label htmlFor={platform.id} className="text-sm font-normal">
                {platform.label}
              </Label>
            </div>
          ))}
        </div>
        {formData.platforms.length === 0 && (
          <p className="text-xs text-destructive">Selecione pelo menos uma plataforma</p>
        )}
      </div>

      <div className="flex gap-2 pt-4">
        <Button type="submit" disabled={loading || formData.platforms.length === 0}>
          {loading ? "Salvando..." : product ? "Atualizar" : "Criar"}
        </Button>
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancelar
        </Button>
      </div>
    </form>
  )
}
