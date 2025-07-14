"use client"

import { useState, useEffect } from "react"
import { useAuth } from "@/contexts/AuthContext"
import { useNotification } from "@/contexts/NotificationContext"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { EpicForm } from "./EpicForm"
import { ReviewDialog } from "@/components/Review/ReviewDialog"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { Edit, Trash2, Eye, BookOpen, MessageSquare } from "lucide-react"

export function EpicList({ productId, epics, setEpics, loading, setLoading, onEpicUpdated, onEpicDeleted }) {
  const [editingEpic, setEditingEpic] = useState(null)
  const [deletingEpic, setDeletingEpic] = useState(null)
  const [viewingEpic, setViewingEpic] = useState(null)
  const [reviewingEpic, setReviewingEpic] = useState(null)
  const { getAuthHeaders } = useAuth()
  const { showSuccess, showError } = useNotification()

  useEffect(() => {
    if (productId) {
      fetchEpics()
    }
  }, [productId])

  const fetchEpics = async () => {
    setLoading(true)
    try {
      const headers = getAuthHeaders()
      const response = await fetch(`http://localhost:8000/products/${productId}/epics`, {
        headers,
      })

      if (response.ok) {
        const data = await response.json()
        setEpics(data)
      } else {
        showError("Erro ao carregar épicos")
      }
    } catch (error) {
      showError("Erro de conexão")
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (epicId) => {
    try {
      const headers = getAuthHeaders()
      const response = await fetch(`http://localhost:8000/epics/${epicId}`, {
        method: "DELETE",
        headers,
      })

      if (response.ok) {
        showSuccess("Épico removido com sucesso!")
        onEpicDeleted(epicId)
      } else {
        showError("Erro ao remover épico")
      }
    } catch (error) {
      showError("Erro de conexão")
    }
    setDeletingEpic(null)
  }

  const getStatusColor = (status) => {
    const colors = {
      draft: "bg-gray-100 text-gray-800",
      in_review: "bg-yellow-100 text-yellow-800",
      approved: "bg-green-100 text-green-800",
      rejected: "bg-red-100 text-red-800",
      needs_revision: "bg-orange-100 text-orange-800",
      implemented: "bg-blue-100 text-blue-800",
    }
    return colors[status] || "bg-gray-100 text-gray-800"
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (epics.length === 0) {
    return (
      <Card>
        <CardContent className="flex flex-col items-center justify-center py-16">
          <BookOpen className="h-16 w-16 text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">Nenhum épico encontrado</h3>
          <p className="text-muted-foreground text-center mb-4">
            Crie épicos para organizar as funcionalidades do produto
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {epics.map((epic) => (
          <Card key={epic.epic_id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg">{epic.title}</CardTitle>
                  <CardDescription className="mt-1">{epic.description}</CardDescription>
                </div>
                <div className="flex flex-col gap-2">
                  <Badge variant="secondary">ID: {epic.epic_id}</Badge>
                  {epic.status && (
                    <Badge className={getStatusColor(epic.status)}>{epic.status.replace("_", " ")}</Badge>
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2 flex-wrap">
                <Button variant="outline" size="sm" onClick={() => setViewingEpic(epic)}>
                  <Eye className="h-4 w-4 mr-1" />
                  Ver
                </Button>
                <Button variant="outline" size="sm" onClick={() => setEditingEpic(epic)}>
                  <Edit className="h-4 w-4 mr-1" />
                  Editar
                </Button>
                <Button variant="outline" size="sm" onClick={() => setReviewingEpic(epic)}>
                  <MessageSquare className="h-4 w-4 mr-1" />
                  Revisar
                </Button>
                <Button variant="outline" size="sm" onClick={() => setDeletingEpic(epic)}>
                  <Trash2 className="h-4 w-4 mr-1" />
                  Excluir
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Dialog de Edição */}
      <Dialog open={!!editingEpic} onOpenChange={() => setEditingEpic(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Editar Épico</DialogTitle>
            <DialogDescription>Atualize as informações do épico</DialogDescription>
          </DialogHeader>
          {editingEpic && (
            <EpicForm
              productId={productId}
              epic={editingEpic}
              onSuccess={(updatedEpic) => {
                onEpicUpdated(updatedEpic)
                setEditingEpic(null)
              }}
              onCancel={() => setEditingEpic(null)}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Dialog de Visualização */}
      <Dialog open={!!viewingEpic} onOpenChange={() => setViewingEpic(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Detalhes do Épico</DialogTitle>
          </DialogHeader>
          {viewingEpic && (
            <div className="space-y-4">
              <div>
                <h4 className="font-medium">Título:</h4>
                <p className="text-muted-foreground">{viewingEpic.title}</p>
              </div>
              <div>
                <h4 className="font-medium">Descrição:</h4>
                <p className="text-muted-foreground">{viewingEpic.description}</p>
              </div>
              {viewingEpic.status && (
                <div>
                  <h4 className="font-medium">Status:</h4>
                  <Badge className={getStatusColor(viewingEpic.status)}>{viewingEpic.status.replace("_", " ")}</Badge>
                </div>
              )}
              <div>
                <h4 className="font-medium">ID:</h4>
                <p className="text-muted-foreground">{viewingEpic.epic_id}</p>
              </div>
              {viewingEpic.created_at && (
                <div>
                  <h4 className="font-medium">Criado em:</h4>
                  <p className="text-muted-foreground">{new Date(viewingEpic.created_at).toLocaleString("pt-BR")}</p>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Dialog de Revisão */}
      {reviewingEpic && (
        <ReviewDialog
          entityType="epic"
          entityId={reviewingEpic.epic_id}
          entityTitle={reviewingEpic.title}
          isOpen={!!reviewingEpic}
          onClose={() => setReviewingEpic(null)}
          onStatusChange={(newStatus) => {
            const updatedEpic = { ...reviewingEpic, status: newStatus }
            onEpicUpdated(updatedEpic)
          }}
        />
      )}

      {/* Dialog de Confirmação de Exclusão */}
      <AlertDialog open={!!deletingEpic} onOpenChange={() => setDeletingEpic(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Confirmar Exclusão</AlertDialogTitle>
            <AlertDialogDescription>
              Tem certeza que deseja excluir o épico "{deletingEpic?.title}"? Esta ação não pode ser desfeita.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => handleDelete(deletingEpic.epic_id)}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Excluir
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  )
}
