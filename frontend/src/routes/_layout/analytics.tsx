import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { BarChart3, Download, Eye, Quote, Share2, Star } from "lucide-react"
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"

import { getMyResearcherAnalytics } from "@/client/publications.api"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export const Route = createFileRoute("/_layout/analytics")({
  component: AnalyticsPage,
})

function StatCard({
  title,
  value,
  icon: Icon,
}: {
  title: string
  value: number
  icon: typeof BarChart3
}) {
  return (
    <Card>
      <CardContent className="flex items-center justify-between p-5">
        <div>
          <p className="text-sm text-muted-foreground">{title}</p>
          <p className="mt-1 text-2xl font-semibold">{value.toLocaleString()}</p>
        </div>
        <div className="rounded-full bg-primary/10 p-3 text-primary">
          <Icon className="h-5 w-5" />
        </div>
      </CardContent>
    </Card>
  )
}

function AnalyticsPage() {
  const { data, error, isLoading } = useQuery({
    queryKey: ["researcher-analytics"],
    queryFn: getMyResearcherAnalytics,
    retry: false,
  })

  if (isLoading) {
    return <div className="py-10 text-center text-muted-foreground">Loading analytics...</div>
  }

  if (error || !data) {
    return (
      <div className="space-y-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Research Analytics</h1>
          <p className="text-muted-foreground">
            Publication metrics, citation tracking, and engagement trends.
          </p>
        </div>
        <Card>
          <CardContent className="p-6">
            <p className="font-medium">Create a researcher profile to unlock analytics.</p>
            <p className="mt-2 text-sm text-muted-foreground">
              Once your account is linked to a researcher profile and publications,
              StudyLink will surface citations, downloads, saves, shares, and engagement
              history here.
            </p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Research Analytics</h1>
        <p className="text-muted-foreground">
          Monitor how your publications are performing across StudyLink.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <StatCard title="Citations" value={data.total_citations} icon={Quote} />
        <StatCard title="Downloads" value={data.total_downloads} icon={Download} />
        <StatCard title="Views" value={data.total_views} icon={Eye} />
        <StatCard title="Saves" value={data.total_saves} icon={Star} />
        <StatCard title="Shares" value={data.total_shares} icon={Share2} />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>30-Day Engagement</CardTitle>
          </CardHeader>
          <CardContent className="h-[320px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.engagement_last_30_days}>
                <XAxis dataKey="date" tickFormatter={(value) => value.slice(5)} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="hsl(var(--primary))"
                  strokeWidth={2.5}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Portfolio Snapshot</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-xl border bg-muted/30 p-4">
              <p className="text-sm text-muted-foreground">Tracked publications</p>
              <p className="mt-1 text-3xl font-semibold">{data.publication_count}</p>
            </div>
            <div className="space-y-3">
              {data.publications.slice(0, 5).map((publication) => (
                <div key={publication.publication_id} className="rounded-xl border p-4">
                  <p className="font-medium">{publication.title}</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {publication.year || "Year unavailable"} • {publication.citation_count} citations
                  </p>
                  <p className="mt-2 text-xs text-muted-foreground">
                    {publication.view_count} views • {publication.download_count} downloads •{" "}
                    {publication.save_count} saves • {publication.share_count} shares
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
