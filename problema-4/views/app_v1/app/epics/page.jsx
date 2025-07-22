"use client"

import { useState } from "react"
import { DashboardLayout } from "@/components/Layout/DashboardLayout"
import { EpicList } from "@/components/Epics/EpicList"
import { EpicForm } from "@/components/Epics/EpicForm"
import { ProductSelector } from "@/components/Common/ProductSelector"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

export default function EpicsPage() {
  const [selectedProductId, setSelectedProductId] = useState("")
  const [epics, setEpics] = useState([])
  const [loading, setLoading] = useState(false)
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)

  const handleEpicCreated = (newEpic) => {
    setEpics((prev) => [...prev, newEpic])
    setIsCreateDialogOpen(false)
  }

  const handleEpicUpdated = (updatedEpic) => {
    setEpics((prev) => prev.map((e) => (e.epic_id === updatedEpic.epic_id ? updatedEpic : e)))
  }

  const handleEpicDeleted = (epicId) => {
    setEpics((prev) => prev.filter((e) => e.epic_id !== epicId))
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Épicos</h1>
            <p className="text-muted-foreground">Gerencie os épicos dos seus produtos</p>
          </div>

          {selectedProductId && (
            <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  Novo Épico
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle>Criar Novo Épico</DialogTitle>
                  <DialogDescription>Crie um épico para o produto selecionado</DialogDescription>
                </DialogHeader>
                <EpicForm
                  productId={selectedProductId}
                  onSuccess={handleEpicCreated}
                  onCancel={() => setIsCreateDialogOpen(false)}
                />
              </DialogContent>
            </Dialog>
          )}
        </div>

        <ProductSelector selectedProductId={selectedProductId} onProductChange={setSelectedProductId} />

        {selectedProductId && (
          <EpicList
            productId={selectedProductId}
            epics={epics}
            setEpics={setEpics}
            loading={loading}
            setLoading={setLoading}
            onEpicUpdated={handleEpicUpdated}
            onEpicDeleted={handleEpicDeleted}
          />
        )}
      </div>
    </DashboardLayout>
  )
}
