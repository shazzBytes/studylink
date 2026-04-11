import { createFileRoute, Link, notFound } from "@tanstack/react-router"
import {
  ArrowLeft,
  BadgeCheck,
  BookOpenText,
  CalendarDays,
  Download,
  Eye,
  FileText,
  GraduationCap,
  Printer,
  Quote,
} from "lucide-react"

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
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <Link to="/">
        <Button variant="ghost" size="sm" className="gap-2 rounded-full px-4">
          <ArrowLeft className="h-4 w-4" />
          Back to Feed
        </Button>
      </Link>

      <div className="overflow-hidden rounded-[2rem] border border-border/70 bg-[linear-gradient(180deg,rgba(248,250,252,0.9),rgba(255,255,255,0.96))] shadow-[0_30px_70px_-45px_rgba(15,23,42,0.45)] dark:bg-[linear-gradient(180deg,rgba(15,23,42,0.88),rgba(2,6,23,0.98))]">
        <div className="grid gap-0 lg:grid-cols-[280px_1fr]">
          <aside className="border-b border-border/60 bg-muted/35 p-6 lg:border-b-0 lg:border-r">
            <div className="space-y-6 lg:sticky lg:top-6">
              <img
                src={paper.coverImageUrl}
                alt={`Cover for ${paper.title}`}
                className="mx-auto w-full max-w-[220px] rounded-[1.5rem] border bg-card object-cover shadow-sm"
              />

              <div className="space-y-4">
                <div className="space-y-1">
                  <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-muted-foreground">
                    Publication
                  </p>
                  <p className="font-semibold">{paper.journal}</p>
                  <p className="text-sm text-muted-foreground">
                    {paper.volume} • {paper.issue}
                  </p>
                  <p className="text-sm text-muted-foreground">{paper.pages}</p>
                </div>

                <div className="grid gap-3 text-sm">
                  <div className="rounded-2xl border bg-background/70 p-3">
                    <p className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
                      DOI
                    </p>
                    <p className="mt-1 font-mono text-xs">{paper.doi}</p>
                  </div>
                  <div className="rounded-2xl border bg-background/70 p-3">
                    <p className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
                      Reading time
                    </p>
                    <p className="mt-1 font-medium">{paper.readTime}</p>
                  </div>
                  <div className="rounded-2xl border bg-background/70 p-3">
                    <p className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
                      Citations
                    </p>
                    <div className="mt-1 flex items-center gap-2 font-medium">
                      <Quote className="h-4 w-4 text-muted-foreground" />
                      {paper.citationCount}
                    </div>
                  </div>
                  {paper.impressions !== undefined && (
                    <div className="rounded-2xl border bg-background/70 p-3">
                      <p className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
                        Views
                      </p>
                      <div className="mt-1 flex items-center gap-2 font-medium">
                        <Eye className="h-4 w-4 text-muted-foreground" />
                        {paper.impressions.toLocaleString()}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </aside>

          <article className="space-y-8 p-6 md:p-10 lg:p-12">
            <header className="space-y-6 border-b border-border/60 pb-8">
              <div className="flex flex-wrap items-center gap-3">
                <Badge variant="secondary" className="rounded-full px-3 py-1">
                  Research Article
                </Badge>
                <Badge variant="outline" className="rounded-full px-3 py-1">
                  <BookOpenText className="mr-1 h-3.5 w-3.5" />
                  Peer-style Demo
                </Badge>
                {paper.isVerified && (
                  <Badge className="rounded-full px-3 py-1">
                    <BadgeCheck className="mr-1 h-3.5 w-3.5" />
                    Verified Author
                  </Badge>
                )}
              </div>

              <div className="flex flex-wrap gap-3">
                <Button asChild className="rounded-full px-5">
                  <Link to="/papers/$id/pdf" params={{ id: paper.id }}>
                    <FileText className="h-4 w-4" />
                    Read PDF
                  </Link>
                </Button>
                <Button variant="outline" asChild className="rounded-full px-5">
                  <Link to="/papers/$id/pdf" params={{ id: paper.id }}>
                    <Download className="h-4 w-4" />
                    Download PDF
                  </Link>
                </Button>
                <Button
                  variant="ghost"
                  className="rounded-full px-5"
                  onClick={() => window.print()}
                >
                  <Printer className="h-4 w-4" />
                  Print
                </Button>
              </div>

              <div className="space-y-4">
                <h1 className="max-w-4xl text-4xl font-semibold leading-tight tracking-tight md:text-5xl">
                  {paper.title}
                </h1>
                <p className="max-w-4xl text-lg leading-8 text-muted-foreground">
                  {paper.summary}
                </p>
              </div>

              <div className="grid gap-6 rounded-[1.75rem] border border-border/60 bg-muted/20 p-5 md:grid-cols-[1.3fr_0.9fr]">
                <div className="space-y-4">
                  <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-muted-foreground">
                    Authors and Affiliations
                  </p>
                  <div className="space-y-3">
                    {paper.authors.map((author) => (
                      <div key={author.name} className="rounded-2xl bg-background/80 p-4">
                        <p className="font-medium">{author.name}</p>
                        <p className="mt-1 text-sm leading-6 text-muted-foreground">
                          {author.affiliation}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-4">
                  <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-muted-foreground">
                    Article Details
                  </p>
                  <div className="space-y-3 text-sm">
                    <div className="flex items-center gap-3 rounded-2xl bg-background/80 p-4">
                      <CalendarDays className="h-4 w-4 text-muted-foreground" />
                      <div>
                        <p className="font-medium">{paper.publishedDate}</p>
                        <p className="text-muted-foreground">Published online</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 rounded-2xl bg-background/80 p-4">
                      <GraduationCap className="h-4 w-4 text-muted-foreground" />
                      <div>
                        <p className="font-medium">{paper.journal}</p>
                        <p className="text-muted-foreground">
                          {paper.volume} • {paper.issue}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 rounded-2xl bg-background/80 p-4">
                      <FileText className="h-4 w-4 text-muted-foreground" />
                      <div>
                        <p className="font-medium">{paper.pages}</p>
                        <p className="text-muted-foreground">{paper.doi}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap gap-2">
                {paper.keywords.map((keyword) => (
                  <Badge key={keyword} variant="outline" className="rounded-full px-3 py-1">
                    {keyword}
                  </Badge>
                ))}
              </div>
            </header>

            <div className="grid gap-8 xl:grid-cols-[minmax(0,1fr)_260px]">
              <div className="space-y-8">
                <Card className="rounded-[1.75rem] border-border/60 shadow-none">
                  <CardContent className="p-6 md:p-8">
                    <div className="space-y-4">
                      <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-muted-foreground">
                        Abstract
                      </p>
                      <p className="text-[1.04rem] leading-8 text-foreground/90">
                        {paper.abstract}
                      </p>
                    </div>
                  </CardContent>
                </Card>

                {paper.sections.map((section, index) => (
                  <section key={section.heading} className="space-y-4">
                    <div className="flex items-center gap-3">
                      <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10 text-sm font-semibold text-primary">
                        {index + 1}
                      </div>
                      <h2 className="text-2xl font-semibold tracking-tight">
                        {section.heading}
                      </h2>
                    </div>
                    <Card className="rounded-[1.75rem] border-border/60 shadow-none">
                      <CardContent className="p-6 md:p-8">
                        <p className="text-base leading-8 text-foreground/85">
                          {section.content}
                        </p>
                      </CardContent>
                    </Card>
                  </section>
                ))}
              </div>

              <aside className="space-y-4 xl:sticky xl:top-8 xl:self-start">
                <Card className="rounded-[1.75rem] border-border/60 shadow-none">
                  <CardContent className="space-y-4 p-6">
                    <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-muted-foreground">
                      How to Cite
                    </p>
                    <p className="text-sm leading-7 text-muted-foreground">
                      {paper.authors[0]?.name} et al. ({paper.publishedDate.slice(-4)}).{" "}
                      <span className="font-medium text-foreground">{paper.title}</span>.{" "}
                      {paper.journal}, {paper.volume}, {paper.pages}. {paper.doi}
                    </p>
                  </CardContent>
                </Card>

                <Card className="rounded-[1.75rem] border-border/60 shadow-none">
                  <CardContent className="space-y-4 p-6">
                    <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-muted-foreground">
                      Reader Notes
                    </p>
                    <ul className="space-y-3 text-sm leading-6 text-muted-foreground">
                      <li>This article is part of the demo publication experience.</li>
                      <li>The metadata, abstract, and sections are intentionally written to feel publication-like.</li>
                      <li>Use this page in the demo to show realistic reading depth and navigation.</li>
                    </ul>
                  </CardContent>
                </Card>
              </aside>
            </div>
          </article>
        </div>
      </div>
    </div>
  )
}
