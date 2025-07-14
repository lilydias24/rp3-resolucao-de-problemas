"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
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
} from "lucide-react"

const navigation = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Produtos",
    href: "/products",
    icon: Package,
  },
  {
    name: "Épicos",
    href: "/epics",
    icon: BookOpen,
  },
  {
    name: "Histórias",
    href: "/stories",
    icon: FileText,
  },
  {
    name: "Requisitos",
    href: "/requirements",
    icon: CheckSquare,
  },
  {
    name: "Backlogs",
    href: "/backlogs",
    icon: List,
  },
  {
    name: "Geração LLM",
    href: "/llm-generation",
    icon: Zap,
  },
]

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const pathname = usePathname()

  return (
    <div
      className={cn("flex flex-col h-full bg-card border-r transition-all duration-300", collapsed ? "w-16" : "w-64")}
    >
      <div className="flex items-center justify-between p-4 border-b">
        {!collapsed && <h2 className="text-lg font-semibold">Sistema de Histórias</h2>}
        <Button variant="ghost" size="sm" onClick={() => setCollapsed(!collapsed)}>
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>
      </div>

      <ScrollArea className="flex-1 px-3 py-4">
        <nav className="space-y-2">
          {navigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link key={item.name} href={item.href}>
                <Button
                  variant={isActive ? "secondary" : "ghost"}
                  className={cn("w-full justify-start", collapsed && "px-2")}
                >
                  <item.icon className="h-4 w-4" />
                  {!collapsed && <span className="ml-2">{item.name}</span>}
                </Button>
              </Link>
            )
          })}
        </nav>
      </ScrollArea>
    </div>
  )
}
