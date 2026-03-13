import { Link, useLocation } from "@tanstack/react-router"
import {
  Bell,
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
import useAuth from "@/hooks/useAuth"
import { cn } from "@/lib/utils"

const navigationItems = [
  { icon: Home, label: "Home", to: "/" },
  { icon: Search, label: "Search", to: "/search" },
  { icon: MessageSquare, label: "Chats", to: "/chats" },
  { icon: FolderKanban, label: "Projects", to: "/projects" },
  { icon: PlusSquare, label: "Create", to: "/create" },
  { icon: Users, label: "Researchers", to: "/researchers" },
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
      <aside className="hidden md:fixed md:left-0 md:top-0 md:z-40 md:flex md:h-screen md:w-20 md:flex-col md:border-r md:bg-background md:py-6">
        <nav className="flex flex-1 flex-col items-center gap-4 px-2">
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
                    "h-12 w-12 rounded-xl transition-colors",
                    isActive
                      ? "bg-primary text-primary-foreground hover:bg-primary/90"
                      : "hover:bg-muted",
                  )}
                  title={item.label}
                >
                  <Icon className="h-6 w-6" />
                </Button>
              </Link>
            )
          })}
        </nav>
        <div className="flex justify-center px-2">
          <Button
            variant="ghost"
            size="icon"
            className="h-12 w-12 rounded-xl transition-colors hover:bg-muted"
            title="Log out"
            onClick={logout}
          >
            <LogOut className="h-6 w-6" />
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
