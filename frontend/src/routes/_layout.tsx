import { createFileRoute, Outlet, redirect } from "@tanstack/react-router"

import { Footer } from "@/components/Common/Footer"
import { IconSidebar } from "@/components/Common/IconSidebar"
import { isLoggedIn } from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout")({
  component: Layout,
  beforeLoad: async () => {
    if (!isLoggedIn()) {
      throw redirect({
        to: "/login",
      })
    }
  },
})

function Layout() {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <IconSidebar />

      <div className="flex min-h-screen flex-col md:ml-20">
        <main className="flex-1 pb-16 md:pb-0">
          <div className="min-h-full bg-[radial-gradient(circle_at_top,rgba(52,211,153,0.12),transparent_28%),radial-gradient(circle_at_85%_10%,rgba(59,130,246,0.1),transparent_22%)]">
            <div className="mx-auto w-full max-w-[1500px] px-3 py-4 sm:px-6 sm:py-6 lg:px-10 lg:py-8">
              <Outlet />
            </div>
          </div>
        </main>
        <Footer />
      </div>
    </div>
  )
}

export default Layout
