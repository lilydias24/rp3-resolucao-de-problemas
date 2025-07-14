"use client"

import React from "react"

import { useState } from "react"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Label } from "./ui/label"
// import { Textarea } from "./ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { Alert, AlertDescription } from "./ui/alert"
import { Badge } from "./ui/badge"
import { Checkbox } from "./ui/checkbox"
import { X, Plus, Package, Users, Smartphone, Monitor, Tablet } from "lucide-react"

export default function ProductForm({ onSubmit, onBack }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    personas: [],
    valueProposition: "",
    channels: [],
  })
  const [newPersona, setNewPersona] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")

    if (formData.personas.length === 0) {
      setError("Adicione pelo menos uma persona")
      return
    }

    if (formData.channels.length === 0) {
      setError("Selecione pelo menos um canal/plataforma")
      return
    }

    setIsLoading(true)

    try {
      await onSubmit(formData)
    } catch (err) {
      setError("Erro ao cadastrar produto. Tente novamente.")
    } finally {
      setIsLoading(false)
    }
  }

  const addPersona = () => {
    if (newPersona.trim() && !formData.personas.includes(newPersona.trim())) {
      setFormData((prev) => ({
        ...prev,
        personas: [...prev.personas, newPersona.trim()],
      }))
      setNewPersona("")
    }
  }

  const removePersona = (persona) => {
    setFormData((prev) => ({
      ...prev,
      personas: prev.personas.filter((p) => p !== persona),
    }))
  }

  const handleChannelChange = (channelId, checked) => {
    setFormData((prev) => ({
      ...prev,
      channels: checked ? [...prev.channels, channelId] : prev.channels.filter((c) => c !== channelId),
    }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-2xl mx-auto">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Package className="h-6 w-6 text-blue-600" />
              <CardTitle className="text-2xl">Cadastrar Novo Produto</CardTitle>
            </div>
            <CardDescription>
              Preencha as informações básicas do produto para iniciar a geração de histórias de usuário
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Nome do Produto */}
              <div className="space-y-2">
                <Label htmlFor="name">Nome do Produto *</Label>
                <Input
                  id="name"
                  placeholder="Ex: Sistema de E-commerce"
                  value={formData.name}
                  onChange={(e) => setFormData((prev) => ({ ...prev, name: e.target.value }))}
                  required
                />
              </div>

              {/* Descrição */}
              <div className="space-y-2">
                <Label htmlFor="description">Descrição *</Label>
                <Textarea
                  id="description"
                  placeholder="Descreva brevemente o que é o produto e suas principais funcionalidades..."
                  value={formData.description}
                  onChange={(e) => setFormData((prev) => ({ ...prev, description: e.target.value }))}
                  rows={4}
                  required
                />
              </div>

              {/* Personas */}
              <div className="space-y-2">
                <Label>Personas Envolvidas *</Label>
                <div className="flex gap-2">
                  <Input
                    placeholder="Ex: Administrador, Cliente, Vendedor"
                    value={newPersona}
                    onChange={(e) => setNewPersona(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && (e.preventDefault(), addPersona())}
                  />
                  <Button type="button" onClick={addPersona} size="sm">
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {formData.personas.map((persona) => (
                    <Badge key={persona} variant="secondary" className="flex items-center gap-1">
                      <Users className="h-3 w-3" />
                      {persona}
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="h-4 w-4 p-0 hover:bg-transparent"
                        onClick={() => removePersona(persona)}
                      >
                        <X className="h-3 w-3" />
                      </Button>
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Proposta de Valor */}
              <div className="space-y-2">
                <Label htmlFor="valueProposition">Proposta de Valor *</Label>
                <Textarea
                  id="valueProposition"
                  placeholder="Que problema este produto resolve? Qual valor ele entrega aos usuários?"
                  value={formData.valueProposition}
                  onChange={(e) => setFormData((prev) => ({ ...prev, valueProposition: e.target.value }))}
                  rows={3}
                  required
                />
              </div>

              {/* Canais/Plataformas */}
              <div className="space-y-2">
                <Label>Canais/Plataformas *</Label>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {availableChannels.map((channel) => {
                    const Icon = channel.icon
                    return (
                      <div key={channel.id} className="flex items-center space-x-2">
                        <Checkbox
                          id={channel.id}
                          checked={formData.channels.includes(channel.id)}
                          onCheckedChange={(checked) => handleChannelChange(channel.id, !!checked)}
                        />
                        <Label htmlFor={channel.id} className="flex items-center gap-2 cursor-pointer">
                          <Icon className="h-4 w-4" />
                          {channel.label}
                        </Label>
                      </div>
                    )
                  })}
                </div>
              </div>

              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="flex gap-4">
                {onBack && (
                  <Button type="button" variant="outline" onClick={onBack}>
                    Voltar
                  </Button>
                )}
                <Button type="submit" className="flex-1" disabled={isLoading}>
                  {isLoading ? "Cadastrando..." : "Cadastrar Produto"}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
