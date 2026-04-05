import { createFileRoute, Link, notFound } from "@tanstack/react-router"
import { ArrowLeft, BadgeCheck, CalendarDays, Eye, UserRound } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { getDummyPaperById } from "@/lib/dummy-papers"

export const Route = createFileRoute("/_layout/papers/$id")({
  component: PaperDetailPage,
  loader: ({ params }) => {
    const paper = getDummyPaperById(params.id)
    if (!paper) {
      throw notFound()
    }
    return paper
  },
})

function PaperDetailPage() {
  const paper = Route.useLoaderData()

  return (
    <div className="mx-auto w-full max-w-5xl space-y-8">
      <div className="space-y-4">
        <Link to="/">
          <Button variant="ghost" size="sm" className="gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Feed
          </Button>
        </Link>

        <div className="overflow-hidden rounded-[2rem] border bg-card shadow-sm">
          <div className="grid gap-8 p-6 md:grid-cols-[240px_1fr] md:p-8">
            <img
              src={paper.coverImageUrl}
              alt={`Cover for ${paper.title}`}
              className="mx-auto w-full max-w-[240px] rounded-2xl border object-cover shadow-sm"
            />

            <div className="space-y-5">
              <div className="flex flex-wrap items-center gap-3">
                <Badge variant="secondary">Dummy Paper</Badge>
                {paper.isVerified && (
                  <Badge className="gap-1">
                    <BadgeCheck className="h-3.5 w-3.5" />
                    Verified Author
                  </Badge>
                )}
              </div>

              <div className="space-y-3">
                <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
                  {paper.title}
                </h1>
                <p className="text-base leading-7 text-muted-foreground">
                  {paper.abstract}
                </p>
              </div>

              <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <UserRound className="h-4 w-4" />
                  <span>{paper.author}</span>
                </div>
                <div className="flex items-center gap-2">
                  <CalendarDays className="h-4 w-4" />
                  <span>{paper.publishedDate}</span>
                </div>
                {paper.impressions !== undefined && (
                  <div className="flex items-center gap-2">
                    <Eye className="h-4 w-4" />
                    <span>{paper.impressions.toLocaleString()} views</span>
                  </div>
                )}
              </div>

              <div className="flex flex-wrap gap-2">
                {paper.keywords.map((keyword) => (
                  <Badge key={keyword} variant="outline">
                    {keyword}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <Card className="rounded-[2rem]">
        <CardContent className="space-y-8 p-6 md:p-8">
          <section className="space-y-3">
            <h2 className="text-2xl font-semibold tracking-tight">Abstract</h2>
            <p className="leading-8 text-muted-foreground">{paper.abstract}</p>
          </section>

          {paper.sections.map((section) => (
            <section key={section.heading} className="space-y-3">
              <h3 className="text-xl font-semibold tracking-tight">
                {section.heading}
              </h3>
              <p className="leading-8 text-muted-foreground">
                {section.content}
              </p>
            </section>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
