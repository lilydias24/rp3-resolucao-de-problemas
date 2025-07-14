"use client"

import { useState } from "react"
import { useAuth } from "@/contexts/AuthContext"
import { useNotification } from "@/contexts/NotificationContext"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

export function EpicForm({ productId, epic, onSuccess, onCancel }) {
  const [formData, setFormData] = useState({
    title: epic?.title || "",
    description: epic?.description || "",
  })
  const [loading, setLoading] = useState(false)
  const { getAuthHeaders } = useAuth()
  const { showSuccess, showError } = useNotification()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const headers = {
        ...getAuthHeaders(),
        "Content-Type": "application/json",
      }

      const url = epic
        ? `http://localhost:8000/epics/${epic.epic_id}`
        : `http://localhost:8000/products/${productId}/epics`

      const method = epic ? "PUT" : "POST"

      const response = await fetch(url, {
        method,
        headers,
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        const result = await response.json()
        showSuccess(epic ? "Épico atualizado com sucesso!" : "Épico criado com sucesso!")
        onSuccess(result)
      } else {
        const error = await response.json()
        showError(error.detail || "Erro ao salvar épico")
      }
    } catch (error) {
      showError("Erro de conexão")
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="title">Título do Épico *</Label>
        <Input
          id="title"
          value={formData.title}
          onChange={(e) => setFormData((prev) => ({ ...prev, title: e.target.value }))}
          placeholder="Título do épico"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Descrição *</Label>
        <Textarea
          id="description"
          value={formData.description}
          onChange={(e) => setFormData((prev) => ({ ...prev, description: e.target.value }))}
          placeholder="Descrição detalhada do épico"
          rows={4}
          required
        />
      </div>

      <div className="flex gap-2 pt-4">
        <Button type="submit" disabled={loading}>
          {loading ? "Salvando..." : epic ? "Atualizar" : "Criar"}
        </Button>
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancelar
        </Button>
      </div>
    </form>
  )
}
