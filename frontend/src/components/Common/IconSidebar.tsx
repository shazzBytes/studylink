import { Link, useLocation } from "@tanstack/react-router"
import {
  BarChart3,
  Bell,
  Building2,
  FolderKanban,
  Home,
  LogOut,
  MessageSquare,
  PlusSquare,
  Search,
  Settings,
  User,
  Users,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import useAuth from "@/hooks/useAuth"
import { cn } from "@/lib/utils"

const navigationItems = [
  { icon: Home, label: "Home", to: "/" },
  { icon: Search, label: "Search", to: "/search" },
  { icon: MessageSquare, label: "Chats", to: "/chats" },
  { icon: FolderKanban, label: "Projects", to: "/projects" },
  { icon: PlusSquare, label: "Create", to: "/create" },
  { icon: Users, label: "Researchers", to: "/researchers" },
  { icon: Building2, label: "Institutions", to: "/institutions" },
  { icon: BarChart3, label: "Analytics", to: "/analytics" },
  { icon: Bell, label: "Notifications", to: "/notifications" },
  { icon: User, label: "Profile", to: "/profile" },
  { icon: Settings, label: "Settings", to: "/settings" },
]

export function IconSidebar() {
  const location = useLocation()
  const { logout } = useAuth()

  return (
    <>
      {/* Desktop Sidebar - Left Side */}
      <aside className="hidden md:fixed md:left-0 md:top-0 md:z-40 md:flex md:h-screen md:flex-col md:border-r md:bg-background md:py-6 md:w-20 md:hover:w-56 transition-[width] duration-200 ease-out group">
        <ScrollArea className="flex-1 overflow-hidden">
          <nav className="flex flex-col gap-4 px-2 py-3 items-center group-hover:items-start">
            {navigationItems.map((item) => {
              const Icon = item.icon
              const isActive =
                location.pathname === item.to ||
                (item.to !== "/" && location.pathname.startsWith(item.to))

              return (
                <Link key={item.to} to={item.to}>
                  <Button
                    variant="ghost"
                    size="icon"
                    className={cn(
                      "h-12 rounded-xl transition-all duration-200 overflow-hidden",
                      "w-12 justify-center group-hover:w-full group-hover:justify-start group-hover:px-4",
                      isActive
                        ? "bg-primary text-primary-foreground hover:bg-primary/90"
                        : "hover:bg-muted",
                    )}
                    title={item.label}
                  >
                    <Icon className="h-6 w-6" />
                    <span className="ml-3 hidden whitespace-nowrap text-sm font-medium transition-all duration-200 group-hover:inline-flex">
                      {item.label}
                    </span>
                  </Button>
                </Link>
              )
            })}
          </nav>
        </ScrollArea>
        <div className="flex flex-col gap-2 px-2 items-center group-hover:items-start pb-4">
          <Button
            variant="ghost"
            size="icon"
            className="h-12 rounded-xl transition-all duration-200 hover:bg-muted overflow-hidden w-12 justify-center group-hover:w-full group-hover:justify-start group-hover:px-4"
            title="Log out"
            onClick={logout}
          >
            <LogOut className="h-6 w-6" />
            <span className="ml-3 hidden whitespace-nowrap text-sm font-medium transition-all duration-200 group-hover:inline-flex">
              Log out
            </span>
          </Button>
        </div>
      </aside>

      {/* Mobile Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 z-40 flex h-16 items-center justify-around border-t bg-background px-2 md:hidden">
        {navigationItems.slice(0, 5).map((item) => {
          const Icon = item.icon
          const isActive =
            location.pathname === item.to ||
            (item.to !== "/" && location.pathname.startsWith(item.to))

          return (
            <Link key={item.to} to={item.to}>
              <Button
                variant="ghost"
                size="icon"
                className={cn(
                  "h-12 w-12 rounded-xl transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "hover:bg-muted",
                )}
              >
                <Icon className={cn("h-6 w-6", isActive && "fill-current")} />
              </Button>
            </Link>
          )
        })}
        <Button
          variant="ghost"
          size="icon"
          className="h-12 w-12 rounded-xl transition-colors hover:bg-muted"
          title="Log out"
          onClick={logout}
        >
          <LogOut className="h-6 w-6" />
        </Button>
      </nav>
    </>
  )
}
