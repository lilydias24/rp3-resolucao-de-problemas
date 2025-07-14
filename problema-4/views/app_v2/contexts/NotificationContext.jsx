"use client"

import { createContext, useContext } from "react"
import { useToast } from "@/hooks/use-toast"

const NotificationContext = createContext({})

export function NotificationProvider({ children }) {
  const { toast } = useToast()

  const showSuccess = (message) => {
    toast({
      title: "Sucesso",
      description: message,
      variant: "default",
    })
  }

  const showError = (message) => {
    toast({
      title: "Erro",
      description: message,
      variant: "destructive",
    })
  }

  const showWarning = (message) => {
    toast({
      title: "Aviso",
      description: message,
      variant: "default",
    })
  }

  const showInfo = (message) => {
    toast({
      title: "Informação",
      description: message,
      variant: "default",
    })
  }

  return (
    <NotificationContext.Provider
      value={{
        showSuccess,
        showError,
        showWarning,
        showInfo,
      }}
    >
      {children}
    </NotificationContext.Provider>
  )
}

export const useNotification = () => {
  const context = useContext(NotificationContext)
  if (!context) {
    throw new Error("useNotification deve ser usado dentro de NotificationProvider")
  }
  return context
}
