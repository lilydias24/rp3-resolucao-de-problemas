"use client"

import { useState } from "react"
import { useAuth } from "@/contexts/AuthContext"
import { useNotification } from "@/contexts/NotificationContext"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import Link from "next/link"
import { Eye, EyeOff, Code, Info } from "lucide-react"

export default function LoginPage() {
  const [email, setEmail] = useState("demo@exemplo.com")
  const [password, setPassword] = useState("123456")
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)

  const { login } = useAuth()
  const { showSuccess } = useNotification()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    // Simular delay de login
    setTimeout(async () => {
      await login(email, password)
      showSuccess("Login realizado com sucesso!")
      setLoading(false)
    }, 1000)
  }

  return (
    <div className="min-h-screen tech-gradient-matrix tech-grid tech-overlay flex items-center justify-center p-4 relative">
      <div className="absolute inset-0 tech-dots"></div>
      <Card className="w-full max-w-md bg-white/10 backdrop-blur-sm border-white/20 relative z-10">
        <CardHeader className="text-center">
          <div className="flex items-center justify-center mb-4">
            <div className="p-3 bg-white/10 backdrop-blur-sm rounded-xl border border-white/20">
              <Code className="h-8 w-8 text-white" />
            </div>
          </div>
          <CardTitle className="text-2xl text-white">Demo Login</CardTitle>
          <CardDescription className="text-white/70">Acesse o sistema de demonstração</CardDescription>
        </CardHeader>
        <CardContent>
          <Alert className="mb-4 border-blue-200 bg-blue-50/10 backdrop-blur-sm">
            <Info className="h-4 w-4 text-blue-300" />
            <AlertDescription className="text-blue-200">
              Este é um sistema de demonstração. Qualquer email/senha funcionará para acessar.
            </AlertDescription>
          </Alert>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-white">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-white/40"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-white">
                Senha
              </Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Sua senha"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-white/40 pr-10"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-white/10 text-white/70"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </Button>
              </div>
            </div>

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white border-0"
              disabled={loading}
            >
              {loading ? "Entrando..." : "Entrar"}
            </Button>
          </form>

          <div className="mt-6 text-center space-y-2">
            <p className="text-sm text-white/70">
              Não quer fazer login?{" "}
              <Link href="/dashboard" className="text-blue-300 hover:text-blue-200 hover:underline">
                Acessar diretamente
              </Link>
            </p>
            <p className="text-sm text-white/70">
              Ou{" "}
              <Link href="/register" className="text-green-300 hover:text-green-200 hover:underline">
                teste o registro
              </Link>
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
