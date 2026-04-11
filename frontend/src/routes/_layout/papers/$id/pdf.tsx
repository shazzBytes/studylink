import { createFileRoute, Link, notFound } from "@tanstack/react-router"
import {
  ArrowLeft,
  CalendarDays,
  Download,
  ExternalLink,
  FileText,
  Printer,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { getDummyPaperById } from "@/lib/dummy-papers"

export const Route = createFileRoute("/_layout/papers/$id/pdf")({
  component: PaperPdfPage,
  loader: ({ params }) => {
    const paper = getDummyPaperById(params.id)
    if (!paper) {
      throw notFound()
    }
    return paper
  },
})

function PaperPdfPage() {
  const paper = Route.useLoaderData()

  return (
    <div className="mx-auto w-full max-w-6xl space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <Link to="/papers/$id" params={{ id: paper.id }}>
          <Button variant="ghost" size="sm" className="gap-2 rounded-full px-4">
            <ArrowLeft className="h-4 w-4" />
            Back to Article
          </Button>
        </Link>

        <div className="flex flex-wrap gap-2">
          <Button variant="outline" className="rounded-full" onClick={() => window.print()}>
            <Printer className="h-4 w-4" />
            Print PDF
          </Button>
          <Button className="rounded-full">
            <Download className="h-4 w-4" />
            Download
          </Button>
        </div>
      </div>

      <div className="rounded-[2rem] border border-border/70 bg-muted/25 p-3 shadow-[0_20px_60px_-40px_rgba(15,23,42,0.45)] md:p-5">
        <div className="mx-auto max-w-4xl rounded-[1.5rem] border bg-white text-slate-900 shadow-sm">
          <div className="border-b px-8 py-6 md:px-12">
            <div className="flex flex-wrap items-center justify-between gap-3 text-xs uppercase tracking-[0.24em] text-slate-500">
              <span>{paper.journal}</span>
              <span>
                {paper.volume} • {paper.issue}
              </span>
            </div>

            <div className="mt-6 space-y-4">
              <h1 className="font-serif text-3xl font-semibold leading-tight md:text-4xl">
                {paper.title}
              </h1>

              <div className="space-y-2 text-sm">
                {paper.authors.map((author) => (
                  <div key={author.name}>
                    <p className="font-medium">{author.name}</p>
                    <p className="text-slate-600">{author.affiliation}</p>
                  </div>
                ))}
              </div>

              <div className="flex flex-wrap gap-5 text-sm text-slate-600">
                <div className="flex items-center gap-2">
                  <CalendarDays className="h-4 w-4" />
                  <span>{paper.publishedDate}</span>
                </div>
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  <span>{paper.pages}</span>
                </div>
                <div className="flex items-center gap-2">
                  <ExternalLink className="h-4 w-4" />
                  <span>{paper.doi}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-8 px-8 py-8 md:px-12 md:py-10">
            <section className="space-y-3">
              <h2 className="font-serif text-xl font-semibold">Abstract</h2>
              <p className="text-[15px] leading-8 text-slate-700">{paper.abstract}</p>
            </section>

            {paper.sections.map((section) => (
              <section key={section.heading} className="space-y-3">
                <h3 className="font-serif text-xl font-semibold">{section.heading}</h3>
                <p className="text-[15px] leading-8 text-slate-700">
                  {section.content}
                </p>
              </section>
            ))}

            <section className="space-y-3 border-t pt-6">
              <h3 className="font-serif text-xl font-semibold">Keywords</h3>
              <p className="text-[15px] leading-8 text-slate-700">
                {paper.keywords.join("; ")}.
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  )
}
