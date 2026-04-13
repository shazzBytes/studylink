import { createFileRoute, Link } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useEffect, useRef, useState } from "react"
import { Download, Eye, Quote, Share2, Star } from "lucide-react"
import {
  getPublication,
  getPublicationAnalytics,
  trackPublicationEvent,
  updatePublicationAnalytics,
} from "@/client/publications.api"
import { ResearchersService } from "@/client"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/publications/$id")({
  component: PublicationDetailPage,
})

function MetricCard({
  label,
  value,
  icon: Icon,
}: {
  label: string
  value: number
  icon: typeof Eye
}) {
  return (
    <div className="rounded-2xl border bg-muted/20 p-4">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Icon className="h-4 w-4" />
        {label}
      </div>
      <p className="mt-2 text-2xl font-semibold">{value.toLocaleString()}</p>
    </div>
  )
}

function PublicationDetailPage() {
  const { id } = Route.useParams()
  const queryClient = useQueryClient()
  const { user } = useAuth()
  const trackedView = useRef(false)
  const [citationCount, setCitationCount] = useState("")

  const publicationQuery = useQuery({
    queryKey: ["publication", id],
    queryFn: () => getPublication(id),
  })
  const analyticsQuery = useQuery({
    queryKey: ["publication-analytics", id],
    queryFn: () => getPublicationAnalytics(id),
    enabled: publicationQuery.isSuccess,
  })
  const researcherQuery = useQuery({
    queryKey: ["publication-researcher", publicationQuery.data?.researcher_id],
    queryFn: () =>
      ResearchersService.getResearcherRoute({
        researcherId: publicationQuery.data?.researcher_id || "",
      }),
    enabled: !!publicationQuery.data?.researcher_id,
  })

  const trackMutation = useMutation({
    mutationFn: (eventType: "download" | "save" | "share" | "citation") =>
      trackPublicationEvent(id, eventType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["publication", id] })
      queryClient.invalidateQueries({ queryKey: ["publication-analytics", id] })
      queryClient.invalidateQueries({ queryKey: ["researcher-analytics"] })
    },
  })

  const updateMutation = useMutation({
    mutationFn: () => updatePublicationAnalytics(id, { citation_count: Number(citationCount) }),
    onSuccess: () => {
      setCitationCount("")
      queryClient.invalidateQueries({ queryKey: ["publication", id] })
      queryClient.invalidateQueries({ queryKey: ["publication-analytics", id] })
      queryClient.invalidateQueries({ queryKey: ["researcher-analytics"] })
    },
  })

  useEffect(() => {
    if (!publicationQuery.isSuccess || trackedView.current) {
      return
    }
    trackedView.current = true
    trackPublicationEvent(id, "view").then(() => {
      queryClient.invalidateQueries({ queryKey: ["publication", id] })
      queryClient.invalidateQueries({ queryKey: ["publication-analytics", id] })
      queryClient.invalidateQueries({ queryKey: ["researcher-analytics"] })
    })
  }, [id, publicationQuery.isSuccess, queryClient])

  if (publicationQuery.isLoading) {
    return <div className="py-10 text-center text-muted-foreground">Loading publication...</div>
  }

  const publication = publicationQuery.data
  if (!publication) {
    return <div className="py-10 text-center text-muted-foreground">Publication not found.</div>
  }

  const researcher = researcherQuery.data
  const canManage = Boolean(
    user?.is_superuser || (researcher && user?.email === researcher.email),
  )

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="space-y-2">
          <Link to="/researchers/$id" params={{ id: publication.researcher_id }}>
            <Button variant="ghost" size="sm">
              Back to Researcher
            </Button>
          </Link>
          <h1 className="text-3xl font-bold tracking-tight">{publication.title}</h1>
          <p className="text-muted-foreground">
            {researcher?.full_name || "Researcher"} • {publication.publisher}
            {publication.year ? ` • ${publication.year}` : ""}
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <Button onClick={() => trackMutation.mutate("download")}>
            <Download className="mr-2 h-4 w-4" />
            Record download
          </Button>
          <Button variant="outline" onClick={() => trackMutation.mutate("save")}>
            <Star className="mr-2 h-4 w-4" />
            Save
          </Button>
          <Button variant="outline" onClick={() => trackMutation.mutate("share")}>
            <Share2 className="mr-2 h-4 w-4" />
            Share
          </Button>
          <Button variant="outline" onClick={() => trackMutation.mutate("citation")}>
            <Quote className="mr-2 h-4 w-4" />
            Record citation
          </Button>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {publication.domains.map((domain) => (
          <Badge key={domain} variant="secondary">
            {domain}
          </Badge>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <MetricCard label="Views" value={publication.view_count} icon={Eye} />
        <MetricCard label="Downloads" value={publication.download_count} icon={Download} />
        <MetricCard label="Citations" value={publication.citation_count} icon={Quote} />
        <MetricCard label="Saves" value={publication.save_count} icon={Star} />
        <MetricCard label="Shares" value={publication.share_count} icon={Share2} />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <CardHeader>
            <CardTitle>Abstract</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="leading-7 text-muted-foreground">
              {publication.description || "No abstract or summary has been added yet."}
            </p>
            <div className="rounded-2xl border bg-muted/20 p-4">
              <p className="text-sm text-muted-foreground">Last engagement</p>
              <p className="mt-1 font-medium">
                {analyticsQuery.data?.last_engagement_at
                  ? new Date(analyticsQuery.data.last_engagement_at).toLocaleString()
                  : "No engagement recorded yet"}
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>7-Day Activity</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {(analyticsQuery.data?.engagement_last_7_days || []).map((point) => (
                <div key={point.date} className="flex items-center justify-between rounded-xl border p-3">
                  <span className="text-sm text-muted-foreground">{point.date}</span>
                  <span className="font-medium">{point.value}</span>
                </div>
              ))}
            </CardContent>
          </Card>

          {canManage ? (
            <Card>
              <CardHeader>
                <CardTitle>Manage Citation Count</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Input
                  type="number"
                  min={0}
                  value={citationCount}
                  onChange={(event) => setCitationCount(event.target.value)}
                  placeholder="Set citation count"
                />
                <Button
                  onClick={() => updateMutation.mutate()}
                  disabled={!citationCount || updateMutation.isPending}
                >
                  Update metrics
                </Button>
              </CardContent>
            </Card>
          ) : null}
        </div>
      </div>
    </div>
  )
}
