import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { Mail, Shield, User } from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { getMyInstitutionMemberships, type InstitutionMembership } from "@/client/institutions.api"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/profile")({
  component: ProfilePage,
})

function ProfilePage() {
  const { user } = useAuth()
  const accountTypeLabel =
    user?.account_type === "researcher" ? "Researcher" : "Student"
  const accessLabel = user?.is_superuser ? "Administrator" : "Member"

  const membershipsQuery = useQuery({
    queryKey: ["my-institution-memberships"],
    queryFn: getMyInstitutionMemberships,
  })

  const memberships = membershipsQuery.data || []
  const primaryMemberships = memberships.filter((membership) => membership.is_primary)
  const partnerMemberships = memberships.filter((membership) => !membership.is_primary)

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

      <Card>
        <CardHeader>
          <CardTitle>Your Institutions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {membershipsQuery.isLoading ? (
            <p className="text-sm text-muted-foreground">Loading your institution memberships…</p>
          ) : memberships.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              You are not a member of any institutions yet.
            </p>
          ) : (
            <div className="space-y-4">
              {primaryMemberships.length > 0 ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <span className="rounded-full bg-primary/10 px-2 py-1 text-xs font-semibold text-primary">
                      Primary institution
                    </span>
                  </div>
                  {primaryMemberships.map((membership: InstitutionMembership) => (
                    <MembershipBlock key={membership.id} membership={membership} />
                  ))}
                </div>
              ) : null}

              {partnerMemberships.length > 0 ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-700">
                      Partner institutions
                    </span>
                  </div>
                  {partnerMemberships.map((membership: InstitutionMembership) => (
                    <MembershipBlock key={membership.id} membership={membership} />
                  ))}
                </div>
              ) : null}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

function MembershipBlock({ membership }: { membership: InstitutionMembership }) {
  return (
    <div className="rounded-xl border p-4">
      <div className="flex flex-wrap items-center gap-2">
        <p className="font-medium">{membership.institution_name}</p>
        <span className="rounded-full bg-muted/10 px-2 py-1 text-xs font-semibold text-muted-foreground">
          {membership.role}
        </span>
        {membership.is_verified ? (
          <span className="rounded-full bg-emerald-100 px-2 py-1 text-xs font-semibold text-emerald-700">
            Verified
          </span>
        ) : null}
      </div>
      <p className="text-sm text-muted-foreground">
        {membership.department || "No department"} • {membership.title || "No title"}
      </p>
    </div>
  )
}
