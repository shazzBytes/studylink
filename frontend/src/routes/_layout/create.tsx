import { createFileRoute, redirect } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/create")({
  beforeLoad: () => {
    throw redirect({ to: "/projects/create" })
  },
})
