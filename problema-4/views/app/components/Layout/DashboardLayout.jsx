"use client"

import { useAuth } from "@/contexts/AuthContext"
import { Header } from "./Header"
import { Sidebar } from "./Sidebar"

export function DashboardLayout({ children }) {
  const { loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="relative">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
          <div className="absolute inset-0 animate-ping rounded-full h-32 w-32 border border-purple-500 opacity-20"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto bg-gradient-to-br from-slate-900/50 via-slate-800/50 to-slate-900/50 relative">
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-5">
            <div
              className="absolute inset-0"
              style={{
                backgroundImage: `radial-gradient(circle at 1px 1px, rgba(255,255,255,0.15) 1px, transparent 0)`,
                backgroundSize: "20px 20px",
              }}
            ></div>
          </div>
          <div className="relative z-10 p-6">{children}</div>
        </main>
      </div>
    </div>
  )
}
