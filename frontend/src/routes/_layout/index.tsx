import { createFileRoute } from "@tanstack/react-router"
import { PaperCard } from "@/components/Common/PaperCard"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { dummyPapers } from "@/lib/dummy-papers"
import { TrendingUp, Clock, Star } from "lucide-react"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const papers = dummyPapers

  return (
    <div className="container mx-auto max-w-3xl space-y-6 p-6">
      {/* Header Section */}
      <div className="space-y-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Research Paper Feed</h1>
          <p className="text-muted-foreground">
            Discover the latest research papers from leading researchers worldwide
          </p>
        </div>

        {/* Tabs for filtering */}
        <Tabs defaultValue="trending" className="w-full">
          <TabsList className="grid w-full max-w-md grid-cols-3">
            <TabsTrigger value="trending" className="gap-2">
              <TrendingUp className="h-4 w-4" />
              Trending
            </TabsTrigger>
            <TabsTrigger value="recent" className="gap-2">
              <Clock className="h-4 w-4" />
              Recent
            </TabsTrigger>
            <TabsTrigger value="following" className="gap-2">
              <Star className="h-4 w-4" />
              Following
            </TabsTrigger>
          </TabsList>

          {/* Trending Papers */}
          <TabsContent value="trending" className="space-y-4 mt-6">
            {papers
              .sort((a, b) => (b.impressions ?? 0) - (a.impressions ?? 0))
              .map((paper) => (
                <PaperCard
                  key={paper.id}
                  paperId={paper.id}
                  title={paper.title}
                  author={paper.author}
                  publishedDate={paper.publishedDate}
                  summary={paper.summary}
                  coverImageUrl={paper.coverImageUrl}
                  impressions={paper.impressions}
                  isVerified={paper.isVerified}
                />
              ))}
          </TabsContent>

          {/* Recent Papers */}
          <TabsContent value="recent" className="space-y-4 mt-6">
            {papers.map((paper) => (
              <PaperCard
                key={paper.id}
                paperId={paper.id}
                title={paper.title}
                author={paper.author}
                publishedDate={paper.publishedDate}
                summary={paper.summary}
                coverImageUrl={paper.coverImageUrl}
                impressions={paper.impressions}
                isVerified={paper.isVerified}
              />
            ))}
          </TabsContent>

          {/* Following Papers */}
          <TabsContent value="following" className="space-y-4 mt-6">
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Star className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No papers yet</h3>
              <p className="text-muted-foreground mb-4 max-w-sm">
                Follow researchers to see their latest papers here
              </p>
              <Button>Discover Researchers</Button>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
