"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/contexts/AuthContext"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BookOpen, Users, Zap, BarChart3, Code, Cpu, Database, Globe } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && user) {
      router.push("/dashboard")
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="min-h-screen tech-gradient-cyber tech-dots flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen tech-gradient-cyber tech-dots tech-overlay relative">
      <div className="container mx-auto px-4 py-16 relative z-10">
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-6">
            <div className="p-4 bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20">
              <Code className="h-12 w-12 text-white" />
            </div>
          </div>
          <h1 className="text-5xl font-bold text-white mb-4 tracking-tight">Sistema de Gerenciamento de Histórias</h1>
          <p className="text-xl text-white/80 mb-8 max-w-2xl mx-auto">
            API para geração e gestão de histórias de usuário com LLMs avançados
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/login">
              <Button
                size="lg"
                className="bg-white/20 backdrop-blur-sm border border-white/30 text-white hover:bg-white/30 transition-all duration-300"
              >
                Fazer Login
              </Button>
            </Link>
            <Link href="/register">
              <Button
                variant="outline"
                size="lg"
                className="border-white/30 text-white hover:bg-white/10 transition-all duration-300 bg-transparent"
              >
                Registrar-se
              </Button>
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20 transition-all duration-300">
            <CardHeader>
              <BookOpen className="h-8 w-8 text-blue-300 mb-2" />
              <CardTitle className="text-white">Histórias de Usuário</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-white/70">
                Geração automática de histórias de usuário usando LLMs avançados
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20 transition-all duration-300">
            <CardHeader>
              <Users className="h-8 w-8 text-green-300 mb-2" />
              <CardTitle className="text-white">Gestão de Produtos</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-white/70">
                Cadastro e gerenciamento completo de produtos e suas funcionalidades
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20 transition-all duration-300">
            <CardHeader>
              <Zap className="h-8 w-8 text-yellow-300 mb-2" />
              <CardTitle className="text-white">Geração Automática</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-white/70">
                Épicos, requisitos e backlogs gerados automaticamente com IA
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20 transition-all duration-300">
            <CardHeader>
              <BarChart3 className="h-8 w-8 text-purple-300 mb-2" />
              <CardTitle className="text-white">Sistema de Revisão</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-white/70">
                Workflow completo de aprovação e rastreamento de mudanças
              </CardDescription>
            </CardContent>
          </Card>
        </div>

        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-8">Tecnologia de Ponta</h2>
          <div className="grid md:grid-cols-2 gap-8 text-left">
            <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
              <h3 className="text-xl font-semibold mb-4 text-white flex items-center">
                <Cpu className="h-6 w-6 mr-2 text-blue-300" />
                Para Product Owners
              </h3>
              <ul className="space-y-3 text-white/80">
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-blue-300 rounded-full mr-3"></div>
                  Cadastro de produtos com informações detalhadas
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-green-300 rounded-full mr-3"></div>
                  Geração automática de épicos e histórias
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-yellow-300 rounded-full mr-3"></div>
                  Sistema de revisão e aprovação
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-purple-300 rounded-full mr-3"></div>
                  Geração de backlogs inteligentes
                </li>
              </ul>
            </div>
            <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
              <h3 className="text-xl font-semibold mb-4 text-white flex items-center">
                <Database className="h-6 w-6 mr-2 text-green-300" />
                Para Equipes
              </h3>
              <ul className="space-y-3 text-white/80">
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-blue-300 rounded-full mr-3"></div>
                  Rastreamento completo de mudanças
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-green-300 rounded-full mr-3"></div>
                  Múltiplas estratégias de priorização
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-yellow-300 rounded-full mr-3"></div>
                  Interface intuitiva e responsiva
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-purple-300 rounded-full mr-3"></div>
                  Integração com LLMs avançados
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="text-center">
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 max-w-md mx-auto">
            <Globe className="h-16 w-16 text-white mx-auto mb-4 tech-glow" />
            <h3 className="text-2xl font-bold text-white mb-4">Pronto para começar?</h3>
            <p className="text-white/70 mb-6">Transforme sua gestão de produtos com inteligência artificial</p>
            <div className="space-y-3">
              <Link href="/register" className="block">
                <Button className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white border-0">
                  Criar Conta Gratuita
                </Button>
              </Link>
              <Link href="/login" className="block">
                <Button
                  variant="outline"
                  className="w-full border-white/30 text-white hover:bg-white/10 bg-transparent"
                >
                  Já tenho uma conta
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
