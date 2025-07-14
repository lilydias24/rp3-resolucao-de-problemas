"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import {
  LayoutDashboard,
  Package,
  BookOpen,
  FileText,
  CheckSquare,
  List,
  Zap,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Brain,
  Rocket,
  Target,
} from "lucide-react"

const navigation = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
    description: "Visão geral",
    color: "from-blue-500 to-cyan-500",
    badge: null,
  },
  {
    name: "Produtos",
    href: "/products",
    icon: Package,
    description: "Gestão de produtos",
    color: "from-emerald-500 to-teal-500",
    badge: "3",
  },
  {
    name: "Épicos",
    href: "/epics",
    icon: BookOpen,
    description: "Grandes funcionalidades",
    color: "from-purple-500 to-violet-500",
    badge: "8",
  },
  {
    name: "Histórias",
    href: "/stories",
    icon: FileText,
    description: "User Stories",
    color: "from-orange-500 to-red-500",
    badge: "24",
  },
  {
    name: "Requisitos",
    href: "/requirements",
    icon: CheckSquare,
    description: "Requisitos funcionais",
    color: "from-pink-500 to-rose-500",
    badge: "16",
  },
  {
    name: "Backlogs",
    href: "/backlogs",
    icon: List,
    description: "Sprints e tarefas",
    color: "from-indigo-500 to-blue-500",
    badge: "2",
  },
  {
    name: "Geração LLM",
    href: "/llm-generation",
    icon: Zap,
    description: "IA Generativa",
    color: "from-yellow-500 to-orange-500",
    badge: "AI",
    special: true,
  },
]

const quickActions = [
  {
    name: "Gerar com IA",
    icon: Brain,
    color: "from-cyan-500 to-blue-500",
    href: "/llm-generation",
  },
  {
    name: "Novo Produto",
    icon: Rocket,
    color: "from-green-500 to-emerald-500",
    href: "/products",
  },
  {
    name: "Análise",
    icon: Target,
    color: "from-purple-500 to-pink-500",
    href: "/dashboard",
  },
]

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const pathname = usePathname()

  return (
    <div
      className={cn(
        "flex flex-col h-full bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 border-r border-slate-700/50 transition-all duration-300 relative overflow-hidden",
        collapsed ? "w-20" : "w-72",
      )}
    >
      {/* Background Effects */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/5 to-cyan-500/5"></div>
      <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-blue-500/10 to-transparent"></div>
      <div className="absolute bottom-0 right-0 w-24 h-24 bg-gradient-to-tl from-purple-500/20 to-transparent rounded-full blur-xl"></div>

      {/* Header */}
      <div className="relative z-10 flex items-center justify-between p-4 border-b border-slate-700/50">
        {!collapsed && (
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl shadow-lg">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">StoryGen</h2>
              <p className="text-xs text-slate-400">AI-Powered</p>
            </div>
          </div>
        )}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setCollapsed(!collapsed)}
          className="text-slate-400 hover:text-white hover:bg-slate-700/50 relative z-10"
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>
      </div>

      <ScrollArea className="flex-1 px-3 py-4 relative z-10">
        {/* Main Navigation */}
        <nav className="space-y-2">
          <div className={cn("mb-4", collapsed && "hidden")}>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3">Navegação</p>
          </div>

          {navigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link key={item.name} href={item.href}>
                <div
                  className={cn(
                    "group relative flex items-center rounded-xl transition-all duration-200 overflow-hidden",
                    collapsed ? "p-3 justify-center" : "p-3",
                    isActive
                      ? "bg-gradient-to-r from-slate-700/80 to-slate-600/80 shadow-lg border border-slate-600/50"
                      : "hover:bg-slate-700/50 hover:shadow-md",
                  )}
                >
                  {/* Active indicator */}
                  {isActive && (
                    <div className={cn("absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b", item.color)}></div>
                  )}

                  {/* Icon with gradient background */}
                  <div
                    className={cn(
                      "flex items-center justify-center rounded-lg p-2 transition-all duration-200",
                      isActive
                        ? `bg-gradient-to-br ${item.color} shadow-lg`
                        : "bg-slate-700/50 group-hover:bg-slate-600/50",
                    )}
                  >
                    <item.icon
                      className={cn("h-5 w-5 transition-colors", isActive ? "text-white" : "text-slate-300")}
                    />
                  </div>

                  {!collapsed && (
                    <div className="ml-3 flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <div>
                          <p
                            className={cn(
                              "text-sm font-medium transition-colors",
                              isActive ? "text-white" : "text-slate-200 group-hover:text-white",
                            )}
                          >
                            {item.name}
                          </p>
                          <p className="text-xs text-slate-400">{item.description}</p>
                        </div>
                        {item.badge && (
                          <Badge
                            variant={item.special ? "default" : "secondary"}
                            className={cn(
                              "text-xs",
                              item.special
                                ? "bg-gradient-to-r from-yellow-500 to-orange-500 text-white border-0 shadow-lg"
                                : "bg-slate-600 text-slate-200 border-slate-500",
                            )}
                          >
                            {item.badge}
                          </Badge>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Hover effect */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </div>
              </Link>
            )
          })}
        </nav>

        {/* Quick Actions */}
        {!collapsed && (
          <div className="mt-8">
            <div className="mb-4">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3">Ações Rápidas</p>
            </div>
            <div className="space-y-2">
              {quickActions.map((action) => (
                <Link key={action.name} href={action.href}>
                  <div className="group flex items-center p-2 rounded-lg hover:bg-slate-700/50 transition-all duration-200">
                    <div className={cn("p-2 rounded-lg bg-gradient-to-br", action.color, "shadow-md")}>
                      <action.icon className="h-4 w-4 text-white" />
                    </div>
                    <span className="ml-3 text-sm text-slate-300 group-hover:text-white transition-colors">
                      {action.name}
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* AI Status */}
        {!collapsed && (
          <div className="mt-8">
            <div className="bg-gradient-to-br from-slate-800/80 to-slate-700/80 rounded-xl p-4 border border-slate-600/50">
              <div className="flex items-center space-x-3 mb-2">
                <div className="p-1.5 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg">
                  <Brain className="h-4 w-4 text-white" />
                </div>
                <div>
                  <p className="text-sm font-medium text-white">IA Ativa</p>
                  <p className="text-xs text-slate-400">Sistema operacional</p>
                </div>
              </div>
              <div className="w-full bg-slate-600 rounded-full h-1.5">
                <div className="bg-gradient-to-r from-green-500 to-emerald-500 h-1.5 rounded-full w-4/5"></div>
              </div>
            </div>
          </div>
        )}
      </ScrollArea>

      {/* Footer */}
      <div className="relative z-10 p-4 border-t border-slate-700/50">
        {!collapsed ? (
          <div className="text-center">
            <p className="text-xs text-slate-400">v2.0.1 • AI-Enhanced</p>
            <div className="flex items-center justify-center mt-2 space-x-1">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <p className="text-xs text-slate-400">Sistema Online</p>
            </div>
          </div>
        ) : (
          <div className="flex justify-center">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          </div>
        )}
      </div>
    </div>
  )
}
