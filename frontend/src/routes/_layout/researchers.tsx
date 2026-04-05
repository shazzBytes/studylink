import { createFileRoute } from "@tanstack/react-router"

import { SearchPage } from "./search"

export const Route = createFileRoute("/_layout/researchers")({
  component: ResearchersPage,
})

function ResearchersPage() {
  return <SearchPage />
}
