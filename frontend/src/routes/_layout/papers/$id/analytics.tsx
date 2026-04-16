import { createFileRoute, Link } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { ArrowLeft, TrendingUp, Eye, Download, Share2, BookmarkIcon } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { getDummyPaperById } from "@/lib/dummy-papers"

export const Route = createFileRoute("/_layout/papers/$id/analytics")({
  component: PaperAnalyticsPage,
  loader: ({ params }) => {
    const paper = getDummyPaperById(params.id)
    if (!paper) {
      throw new Error("Paper not found")
    }
    return paper
  },
})

function PaperAnalyticsPage() {
  const paper = Route.useLoaderData()

  // Mock analytics data
  const analyticsData = {
    totalViews: paper.impressions || 0,
    totalDownloads: Math.floor((paper.impressions || 0) * 0.15),
    totalShares: Math.floor((paper.impressions || 0) * 0.08),
    totalBookmarks: Math.floor((paper.impressions || 0) * 0.12),
    citations: paper.citationCount || 0,
    viewsThisWeek: Math.floor((paper.impressions || 0) * 0.25),
    viewsThisMonth: Math.floor((paper.impressions || 0) * 0.6),
  }

  const timeSeriesData = [
    { date: "Mon", views: 120 },
    { date: "Tue", views: 190 },
    { date: "Wed", views: 150 },
    { date: "Thu", views: 220 },
    { date: "Fri", views: 250 },
    { date: "Sat", views: 180 },
    { date: "Sun", views: 210 },
  ]

  return (
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <Link to={`/papers/${paper.id}`}>
        <Button variant="ghost" size="sm" className="gap-2 rounded-full px-4">
          <ArrowLeft className="h-4 w-4" />
          Back to Paper
        </Button>
      </Link>

      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Publication Analytics</h1>
        <p className="text-muted-foreground">{paper.title}</p>
      </div>

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Views</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analyticsData.totalViews.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              {analyticsData.viewsThisWeek} this week
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Downloads</CardTitle>
            <Download className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analyticsData.totalDownloads.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              {Math.round((analyticsData.totalDownloads / analyticsData.totalViews) * 100)}% of views
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Shares</CardTitle>
            <Share2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analyticsData.totalShares.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              {Math.round((analyticsData.totalShares / analyticsData.totalViews) * 100)}% of views
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Bookmarks</CardTitle>
            <BookmarkIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analyticsData.totalBookmarks.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              {Math.round((analyticsData.totalBookmarks / analyticsData.totalViews) * 100)}% of views
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Citations</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analyticsData.citations.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">Total citations</p>
          </CardContent>
        </Card>
      </div>

      {/* Weekly Trend */}
      <Card>
        <CardHeader>
          <CardTitle>Weekly View Trend</CardTitle>
          <CardDescription>Views over the last 7 days</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {timeSeriesData.map((data) => (
              <div key={data.date} className="flex items-center justify-between">
                <div className="text-sm font-medium">{data.date}</div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-32 overflow-hidden rounded-full bg-muted">
                    <div
                      className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                      style={{
                        width: `${(data.views / 300) * 100}%`,
                      }}
                    />
                  </div>
                  <div className="text-right text-sm text-muted-foreground">
                    {data.views}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Engagement Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle>Engagement Breakdown</CardTitle>
          <CardDescription>How readers interact with your paper</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium">Views</span>
                <span className="text-muted-foreground">{analyticsData.totalViews}</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-muted">
                <div className="h-full w-full bg-blue-500" />
              </div>
            </div>
            <div>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium">Downloads</span>
                <span className="text-muted-foreground">{analyticsData.totalDownloads}</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-muted">
                <div
                  className="h-full bg-green-500"
                  style={{
                    width: `${(analyticsData.totalDownloads / analyticsData.totalViews) * 100}%`,
                  }}
                />
              </div>
            </div>
            <div>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium">Shares</span>
                <span className="text-muted-foreground">{analyticsData.totalShares}</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-muted">
                <div
                  className="h-full bg-purple-500"
                  style={{
                    width: `${(analyticsData.totalShares / analyticsData.totalViews) * 100}%`,
                  }}
                />
              </div>
            </div>
            <div>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium">Bookmarks</span>
                <span className="text-muted-foreground">{analyticsData.totalBookmarks}</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-muted">
                <div
                  className="h-full bg-orange-500"
                  style={{
                    width: `${(analyticsData.totalBookmarks / analyticsData.totalViews) * 100}%`,
                  }}
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
