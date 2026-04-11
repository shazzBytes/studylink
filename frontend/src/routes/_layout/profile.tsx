import { createFileRoute } from "@tanstack/react-router"
import { Mail, Shield, User } from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/profile")({
  component: ProfilePage,
})

function ProfilePage() {
  const { user } = useAuth()
  const accountTypeLabel =
    user?.account_type === "researcher" ? "Researcher" : "Student"
  const accessLabel = user?.is_superuser ? "Administrator" : "Member"

  return (
    <div className="container mx-auto max-w-3xl space-y-6 p-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Profile</h1>
        <p className="text-muted-foreground">
          View your account details and current access level.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Account Overview</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-3">
            <User className="h-5 w-5 text-muted-foreground" />
            <div>
              <p className="text-sm text-muted-foreground">Name</p>
              <p className="font-medium">{user?.full_name || "Not set"}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Mail className="h-5 w-5 text-muted-foreground" />
            <div>
              <p className="text-sm text-muted-foreground">Email</p>
              <p className="font-medium">{user?.email || "Unknown"}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Shield className="h-5 w-5 text-muted-foreground" />
            <div>
              <p className="text-sm text-muted-foreground">Role</p>
              <p className="font-medium">{accountTypeLabel}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Shield className="h-5 w-5 text-muted-foreground" />
            <div>
              <p className="text-sm text-muted-foreground">Access</p>
              <p className="font-medium">{accessLabel}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
