"use client"

import { useState, useEffect } from "react"
import { useAuth } from "@/contexts/AuthContext"
import { useNotification } from "@/contexts/NotificationContext"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { CheckCircle, XCircle, AlertCircle, MessageSquare, History, Clock } from "lucide-react"

export function ReviewDialog({ entityType, entityId, entityTitle, isOpen, onClose, onStatusChange }) {
  const [reviewInfo, setReviewInfo] = useState(null)
  const [comments, setComments] = useState([])
  const [revisions, setRevisions] = useState([])
  const [newComment, setNewComment] = useState("")
  const [isSuggestion, setIsSuggestion] = useState(false)
  const [suggestedChanges, setSuggestedChanges] = useState("")
  const [actionReason, setActionReason] = useState("")
  const [loading, setLoading] = useState(false)
  const { getAuthHeaders } = useAuth()
  const { showSuccess, showError } = useNotification()

  useEffect(() => {
    if (isOpen && entityId) {
      fetchReviewInfo()
      fetchRevisions()
    }
  }, [isOpen, entityId])

  const fetchReviewInfo = async () => {
    try {
      const headers = getAuthHeaders()
      const response = await fetch(`http://localhost:8000/review/${entityType}/${entityId}/info`, {
        headers,
      })

      if (response.ok) {
        const data = await response.json()
        setReviewInfo(data)
      }
    } catch (error) {
      console.error("Erro ao buscar informações de revisão:", error)
    }
  }

  const fetchRevisions = async () => {
    try {
      const headers = getAuthHeaders()
      const response = await fetch(`http://localhost:8000/products/${entityType}s/${entityId}/revisions`, {
        headers,
      })

      if (response.ok) {
        const data = await response.json()
        setRevisions(data)
      }
    } catch (error) {
      console.error("Erro ao buscar revisões:", error)
    }
  }

  const handleAddComment = async () => {
    if (!newComment.trim()) return

    setLoading(true)
    try {
      const headers = {
        ...getAuthHeaders(),
        "Content-Type": "application/json",
      }

      const response = await fetch("http://localhost:8000/review/comments", {
        method: "POST",
        headers,
        body: JSON.stringify({
          entity_type: entityType,
          entity_id: Number.parseInt(entityId),
          comment: newComment,
          is_suggestion: isSuggestion,
          suggested_changes: isSuggestion ? suggestedChanges : "",
        }),
      })

      if (response.ok) {
        showSuccess("Comentário adicionado com sucesso!")
        setNewComment("")
        setSuggestedChanges("")
        setIsSuggestion(false)
        fetchReviewInfo()
      } else {
        const error = await response.json()
        showError(error.detail || "Erro ao adicionar comentário")
      }
    } catch (error) {
      showError("Erro de conexão")
    } finally {
      setLoading(false)
    }
  }

  const handleReviewAction = async (action) => {
    setLoading(true)
    try {
      const headers = {
        ...getAuthHeaders(),
        "Content-Type": "application/json",
      }

      const body = {
        action,
        reason: actionReason || null,
      }

      const response = await fetch(`http://localhost:8000/review/${entityType}/${entityId}/action`, {
        method: "POST",
        headers,
        body: JSON.stringify(body),
      })

      if (response.ok) {
        const actionMessages = {
          approve: "Item aprovado com sucesso!",
          reject: "Item rejeitado.",
          request_revision: "Solicitação de revisão enviada!",
          mark_implemented: "Item marcado como implementado!",
        }

        showSuccess(actionMessages[action] || "Ação executada com sucesso!")
        setActionReason("")
        fetchReviewInfo()

        // Notificar mudança de status
        if (onStatusChange) {
          const statusMap = {
            approve: "approved",
            reject: "rejected",
            request_revision: "needs_revision",
            mark_implemented: "implemented",
          }
          onStatusChange(statusMap[action])
        }
      } else {
        const error = await response.json()
        showError(error.detail || "Erro ao executar ação")
      }
    } catch (error) {
      showError("Erro de conexão")
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (status) => {
    const icons = {
      draft: <Clock className="h-4 w-4" />,
      in_review: <AlertCircle className="h-4 w-4" />,
      approved: <CheckCircle className="h-4 w-4" />,
      rejected: <XCircle className="h-4 w-4" />,
      needs_revision: <AlertCircle className="h-4 w-4" />,
      implemented: <CheckCircle className="h-4 w-4" />,
    }
    return icons[status] || <Clock className="h-4 w-4" />
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

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5" />
            Revisão: {entityTitle}
          </DialogTitle>
          <DialogDescription>Gerencie a revisão e aprovação do {entityType}</DialogDescription>
        </DialogHeader>

        <Tabs defaultValue="review" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="review">Revisão</TabsTrigger>
            <TabsTrigger value="comments">Comentários</TabsTrigger>
            <TabsTrigger value="history">Histórico</TabsTrigger>
          </TabsList>

          <TabsContent value="review" className="space-y-4">
            {reviewInfo && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    {getStatusIcon(reviewInfo.current_status)}
                    Status Atual
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-4 mb-4">
                    <Badge className={getStatusColor(reviewInfo.current_status)}>
                      {reviewInfo.current_status?.replace("_", " ") || "Draft"}
                    </Badge>
                    <span className="text-sm text-muted-foreground">{reviewInfo.total_comments} comentários</span>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <Button
                      onClick={() => handleReviewAction("approve")}
                      disabled={loading}
                      className="bg-green-600 hover:bg-green-700"
                    >
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Aprovar
                    </Button>
                    <Button onClick={() => handleReviewAction("reject")} disabled={loading} variant="destructive">
                      <XCircle className="h-4 w-4 mr-2" />
                      Rejeitar
                    </Button>
                    <Button onClick={() => handleReviewAction("request_revision")} disabled={loading} variant="outline">
                      <AlertCircle className="h-4 w-4 mr-2" />
                      Solicitar Revisão
                    </Button>
                    <Button
                      onClick={() => handleReviewAction("mark_implemented")}
                      disabled={loading}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Implementado
                    </Button>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="actionReason">Motivo da ação (opcional)</Label>
                    <Textarea
                      id="actionReason"
                      value={actionReason}
                      onChange={(e) => setActionReason(e.target.value)}
                      placeholder="Descreva o motivo da ação..."
                      rows={2}
                    />
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="comments" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Adicionar Comentário</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="newComment">Comentário</Label>
                  <Textarea
                    id="newComment"
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    placeholder="Adicione seu comentário..."
                    rows={3}
                  />
                </div>

                <div className="flex items-center space-x-2">
                  <Checkbox id="isSuggestion" checked={isSuggestion} onCheckedChange={setIsSuggestion} />
                  <Label htmlFor="isSuggestion">É uma sugestão de melhoria</Label>
                </div>

                {isSuggestion && (
                  <div className="space-y-2">
                    <Label htmlFor="suggestedChanges">Sugestões específicas</Label>
                    <Textarea
                      id="suggestedChanges"
                      value={suggestedChanges}
                      onChange={(e) => setSuggestedChanges(e.target.value)}
                      placeholder="Descreva as mudanças sugeridas..."
                      rows={2}
                    />
                  </div>
                )}

                <Button onClick={handleAddComment} disabled={loading || !newComment.trim()}>
                  {loading ? "Adicionando..." : "Adicionar Comentário"}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="history" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <History className="h-5 w-5" />
                  Histórico de Revisões
                </CardTitle>
              </CardHeader>
              <CardContent>
                {revisions.length > 0 ? (
                  <div className="space-y-4">
                    {revisions.map((revision, index) => (
                      <div key={index} className="border-l-2 border-muted pl-4">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-medium">{revision.field_changed}</span>
                          <Badge variant="outline" className="text-xs">
                            {new Date(revision.changed_at).toLocaleString("pt-BR")}
                          </Badge>
                        </div>
                        <div className="text-sm text-muted-foreground mb-2">
                          <span className="line-through">{revision.old_value}</span>
                          {" → "}
                          <span className="font-medium">{revision.new_value}</span>
                        </div>
                        {revision.change_reason && (
                          <p className="text-sm text-muted-foreground">Motivo: {revision.change_reason}</p>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-muted-foreground">Nenhuma revisão encontrada para este item.</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  )
}
