"use client"

import { useState } from "react"
import { DashboardLayout } from "@/components/Layout/DashboardLayout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { useAuth } from "@/contexts/AuthContext"
import { useNotification } from "@/contexts/NotificationContext"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Zap, BookOpen, FileText, CheckSquare, Loader2 } from "lucide-react"

export default function LLMGenerationPage() {
  const [activeTab, setActiveTab] = useState("epics")
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState({})
  const { getAuthHeaders } = useAuth()
  const { showSuccess, showError } = useNotification()

  const [formData, setFormData] = useState({
    epics: {
      prompt: "",
      customPrompt: "",
    },
    stories: {
      prompt: "",
      customPrompt: "",
    },
    requirements: {
      prompt: "",
      customPrompt: "",
    },
  })

  const handleGenerate = async (type) => {
    const data = formData[type]
    if (!data.prompt.trim()) {
      showError("Por favor, preencha o prompt principal")
      return
    }

    setLoading(true)
    try {
      const headers = {
        ...getAuthHeaders(),
        "Content-Type": "application/json",
      }

      const endpoints = {
        epics: "generate-epics",
        stories: "generate-user-stories",
        requirements: "generate-requirements",
      }

      const response = await fetch(`http://localhost:8000/llm-project/${endpoints[type]}`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          prompt: data.prompt,
          custom_prompt: data.customPrompt || null,
        }),
      })

      if (response.ok) {
        const result = await response.json()
        setResults((prev) => ({ ...prev, [type]: result }))
        showSuccess(
          `${type === "epics" ? "Épicos" : type === "stories" ? "Histórias" : "Requisitos"} gerados com sucesso!`,
        )
      } else {
        const error = await response.json()
        showError(error.detail || "Erro na geração")
      }
    } catch (error) {
      showError("Erro de conexão")
    } finally {
      setLoading(false)
    }
  }

  const updateFormData = (type, field, value) => {
    setFormData((prev) => ({
      ...prev,
      [type]: {
        ...prev[type],
        [field]: value,
      },
    }))
  }

  const GenerationForm = ({ type, icon: Icon, title, description, placeholder }) => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Icon className="h-5 w-5" />
            {title}
          </CardTitle>
          <CardDescription>{description}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor={`${type}-prompt`}>Prompt Principal *</Label>
            <Textarea
              id={`${type}-prompt`}
              value={formData[type].prompt}
              onChange={(e) => updateFormData(type, "prompt", e.target.value)}
              placeholder={placeholder}
              rows={6}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor={`${type}-custom`}>Prompt Customizado (opcional)</Label>
            <Textarea
              id={`${type}-custom`}
              value={formData[type].customPrompt}
              onChange={(e) => updateFormData(type, "customPrompt", e.target.value)}
              placeholder="Instruções adicionais para personalizar a geração..."
              rows={3}
            />
          </div>

          <Button
            onClick={() => handleGenerate(type)}
            disabled={loading || !formData[type].prompt.trim()}
            className="w-full"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Gerando...
              </>
            ) : (
              <>
                <Zap className="h-4 w-4 mr-2" />
                Gerar {title}
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {results[type] && (
        <Card>
          <CardHeader>
            <CardTitle>Resultado da Geração</CardTitle>
            <CardDescription>
              {results[type].tokens_used && `Tokens utilizados: ${results[type].tokens_used}`}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="bg-muted p-4 rounded-lg">
              <pre className="whitespace-pre-wrap text-sm">{results[type].response}</pre>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header tecnológico */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 p-8 text-white">
          <div className="absolute inset-0 bg-black/20"></div>
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-white/20 backdrop-blur-sm rounded-lg">
                <Zap className="h-8 w-8" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">Geração via LLM</h1>
                <p className="text-white/80">Use inteligência artificial para gerar épicos, histórias e requisitos</p>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
                <BookOpen className="h-6 w-6 mx-auto mb-1" />
                <div className="text-sm font-medium">Épicos</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
                <FileText className="h-6 w-6 mx-auto mb-1" />
                <div className="text-sm font-medium">Histórias</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
                <CheckSquare className="h-6 w-6 mx-auto mb-1" />
                <div className="text-sm font-medium">Requisitos</div>
              </div>
            </div>
          </div>
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full -translate-y-16 translate-x-16"></div>
          <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/5 rounded-full translate-y-12 -translate-x-12"></div>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="epics" className="flex items-center gap-2">
              <BookOpen className="h-4 w-4" />
              Épicos
            </TabsTrigger>
            <TabsTrigger value="stories" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Histórias
            </TabsTrigger>
            <TabsTrigger value="requirements" className="flex items-center gap-2">
              <CheckSquare className="h-4 w-4" />
              Requisitos
            </TabsTrigger>
          </TabsList>

          <TabsContent value="epics">
            <GenerationForm
              type="epics"
              icon={BookOpen}
              title="Épicos"
              description="Gere épicos para um produto baseado em suas informações"
              placeholder="Descreva o produto, suas funcionalidades principais, público-alvo e objetivos. Exemplo:

Produto: Sistema de E-commerce
Descrição: Plataforma online para venda de produtos
Público-alvo: Pequenos e médios comerciantes
Funcionalidades: Catálogo de produtos, carrinho de compras, pagamentos, gestão de pedidos
Plataformas: Web e Mobile"
            />
          </TabsContent>

          <TabsContent value="stories">
            <GenerationForm
              type="stories"
              icon={FileText}
              title="Histórias de Usuário"
              description="Gere histórias de usuário baseadas em épicos existentes"
              placeholder="Descreva os épicos existentes e o contexto do produto. Exemplo:

Épicos:
1. Gestão de Produtos - Permitir que vendedores cadastrem e gerenciem seus produtos
2. Carrinho de Compras - Funcionalidade para clientes adicionarem produtos e finalizarem compras
3. Sistema de Pagamentos - Processar pagamentos de forma segura

Contexto: E-commerce para pequenos comerciantes com foco em usabilidade"
            />
          </TabsContent>

          <TabsContent value="requirements">
            <GenerationForm
              type="requirements"
              icon={CheckSquare}
              title="Requisitos Funcionais"
              description="Gere requisitos funcionais baseados em histórias de usuário"
              placeholder="Descreva as histórias de usuário existentes. Exemplo:

Histórias de Usuário:
1. Como vendedor, quero cadastrar produtos para disponibilizá-los na loja
2. Como cliente, quero adicionar produtos ao carrinho para comprá-los depois
3. Como cliente, quero finalizar minha compra com pagamento seguro
4. Como vendedor, quero acompanhar meus pedidos para gerenciar entregas

Contexto: Sistema deve ser responsivo e intuitivo"
            />
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  )
}
