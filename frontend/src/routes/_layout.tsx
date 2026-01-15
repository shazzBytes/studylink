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
    <div className="flex min-h-screen flex-col">
      <IconSidebar />
      
      {/* Main Content Area with left padding for sidebar on desktop */}
      <div className="flex min-h-screen flex-col md:ml-20">
        <main className="flex-1 pb-16 md:pb-0">
          <Outlet />
        </main>
        <Footer />
      </div>
    </div>
  )
}

export default Layout
