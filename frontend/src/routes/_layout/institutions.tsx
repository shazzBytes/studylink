import { createFileRoute } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { Building2, CheckCircle2, Plus, Users } from "lucide-react"

import {
  bulkOnboardInstitutionMembers,
  createInstitution,
  getInstitutionMembers,
  getInstitutions,
  getMyInstitutionMemberships,
  type BulkOnboardMemberPayload,
  type Institution,
} from "@/client/institutions.api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/institutions")({
  component: InstitutionsPage,
})

type OnboardDraft = BulkOnboardMemberPayload

const emptyDraft = (): OnboardDraft => ({
  email: "",
  password: "",
  full_name: "",
  account_type: "student",
  role: "student",
  department: "",
  title: "",
  is_primary: true,
  is_verified: true,
})

function InstitutionManager({ institution }: { institution: Institution }) {
  const queryClient = useQueryClient()
  const [rows, setRows] = useState<OnboardDraft[]>([emptyDraft()])
  const membersQuery = useQuery({
    queryKey: ["institution-members", institution.id],
    queryFn: () => getInstitutionMembers(institution.id),
  })

  const onboardMutation = useMutation({
    mutationFn: () =>
      bulkOnboardInstitutionMembers(
        institution.id,
        rows.filter((row) => row.email && row.password),
      ),
    onSuccess: () => {
      setRows([emptyDraft()])
      queryClient.invalidateQueries({ queryKey: ["institutions"] })
      queryClient.invalidateQueries({ queryKey: ["institution-members", institution.id] })
      queryClient.invalidateQueries({ queryKey: ["my-institution-memberships"] })
    },
  })

  return (
    <Card className="border-dashed">
      <CardHeader>
        <CardTitle className="text-lg">Institution Onboarding</CardTitle>
      </CardHeader>
      <CardContent className="space-y-5">
        <div className="space-y-3">
          {rows.map((row, index) => (
            <div key={`${institution.id}-${index}`} className="grid gap-3 rounded-xl border p-4 md:grid-cols-2 xl:grid-cols-4">
              <Input
                placeholder="Email"
                value={row.email}
                onChange={(event) => {
                  const next = [...rows]
                  next[index] = { ...row, email: event.target.value }
                  setRows(next)
                }}
              />
              <Input
                placeholder="Temporary password"
                value={row.password}
                onChange={(event) => {
                  const next = [...rows]
                  next[index] = { ...row, password: event.target.value }
                  setRows(next)
                }}
              />
              <Input
                placeholder="Full name"
                value={row.full_name}
                onChange={(event) => {
                  const next = [...rows]
                  next[index] = { ...row, full_name: event.target.value }
                  setRows(next)
                }}
              />
              <Input
                placeholder="Title or role"
                value={row.title}
                onChange={(event) => {
                  const next = [...rows]
                  next[index] = { ...row, title: event.target.value }
                  setRows(next)
                }}
              />
              <Input
                placeholder="Department"
                value={row.department}
                onChange={(event) => {
                  const next = [...rows]
                  next[index] = { ...row, department: event.target.value }
                  setRows(next)
                }}
              />
              <Input
                placeholder="Institution role: student, faculty, researcher..."
                value={row.role}
                onChange={(event) => {
                  const next = [...rows]
                  next[index] = {
                    ...row,
                    role: event.target.value as OnboardDraft["role"],
                  }
                  setRows(next)
                }}
              />
              <Input
                placeholder="Account type: student or researcher"
                value={row.account_type}
                onChange={(event) => {
                  const next = [...rows]
                  next[index] = {
                    ...row,
                    account_type: event.target.value as OnboardDraft["account_type"],
                  }
                  setRows(next)
                }}
              />
              <div className="flex items-center gap-2">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    const next = rows.filter((_, rowIndex) => rowIndex !== index)
                    setRows(next.length > 0 ? next : [emptyDraft()])
                  }}
                >
                  Remove
                </Button>
              </div>
            </div>
          ))}
        </div>

        <div className="flex flex-wrap gap-2">
          <Button
            type="button"
            variant="outline"
            onClick={() => setRows((current) => [...current, emptyDraft()])}
          >
            <Plus className="mr-2 h-4 w-4" />
            Add row
          </Button>
          <Button
            type="button"
            onClick={() => onboardMutation.mutate()}
            disabled={onboardMutation.isPending}
          >
            Onboard members
          </Button>
        </div>

        <div className="space-y-3">
          <div className="flex items-center gap-2 text-sm font-medium">
            <Users className="h-4 w-4" />
            Current members
          </div>
          <div className="space-y-2">
            {(membersQuery.data || []).map((member) => (
              <div key={member.id} className="rounded-xl border p-3">
                <p className="font-medium">{member.user_full_name || member.user_email}</p>
                <p className="text-sm text-muted-foreground">
                  {member.role} • {member.department || "No department"} • {member.title || "No title"}
                </p>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function InstitutionsPage() {
  const queryClient = useQueryClient()
  const { user } = useAuth()
  const [form, setForm] = useState({
    name: "",
    domain: "",
    institution_type: "university" as Institution["institution_type"],
    description: "",
  })
  const institutionsQuery = useQuery({
    queryKey: ["institutions"],
    queryFn: getInstitutions,
  })
  const membershipsQuery = useQuery({
    queryKey: ["my-institution-memberships"],
    queryFn: getMyInstitutionMemberships,
  })

  const createMutation = useMutation({
    mutationFn: () =>
      createInstitution({
        name: form.name,
        domain: form.domain || undefined,
        institution_type: form.institution_type,
        description: form.description || undefined,
      }),
    onSuccess: () => {
      setForm({
        name: "",
        domain: "",
        institution_type: "university",
        description: "",
      })
      queryClient.invalidateQueries({ queryKey: ["institutions"] })
    },
  })

  const memberships = membershipsQuery.data || []
  const managerInstitutionIds = new Set(
    memberships
      .filter((membership) => membership.role === "admin")
      .map((membership) => membership.institution_id),
  )
  const primaryMemberships = memberships.filter((membership) => membership.is_primary)
  const partnerMemberships = memberships.filter((membership) => !membership.is_primary)

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Institutions</h1>
        <p className="text-muted-foreground">
          Manage verified partner organizations and onboard faculty, students, and research teams.
        </p>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <CardHeader>
            <CardTitle>Partner Institutions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {institutionsQuery.isLoading ? (
              <p className="text-sm text-muted-foreground">Loading institutions…</p>
            ) : institutionsQuery.isError ? (
              <p className="text-sm text-red-600">Failed to load institutions</p>
            ) : (institutionsQuery.data || []).length === 0 ? (
              <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-muted-foreground/25 py-12 text-center">
                <Building2 className="mb-3 h-8 w-8 text-muted-foreground/40" />
                <p className="text-sm font-medium text-muted-foreground">No institutions available</p>
                <p className="text-xs text-muted-foreground/60">Institutions will appear here once they are created</p>
              </div>
            ) : (
              (institutionsQuery.data || []).map((institution) => (
                <div key={institution.id} className="space-y-4 rounded-2xl border p-5">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <h2 className="text-lg font-semibold">{institution.name}</h2>
                        {institution.is_verified ? (
                          <span className="inline-flex items-center gap-1 text-sm text-emerald-600">
                            <CheckCircle2 className="h-4 w-4" />
                            Verified
                          </span>
                        ) : null}
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {institution.institution_type.replace(/_/g, " ")} • {institution.member_count} members
                      </p>
                      {institution.description ? (
                        <p className="mt-2 text-sm text-muted-foreground">{institution.description}</p>
                      ) : null}
                    </div>
                    <div className="rounded-full bg-primary/10 p-3 text-primary">
                      <Building2 className="h-5 w-5" />
                    </div>
                  </div>

                  {(user?.is_superuser || managerInstitutionIds.has(institution.id)) &&
                  institution.onboarding_enabled ? (
                    <InstitutionManager institution={institution} />
                  ) : null}
                </div>
              ))
            )}
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Your Memberships</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {memberships.length === 0 ? (
                <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-muted-foreground/25 py-8 text-center">
                  <p className="text-sm font-medium text-muted-foreground">Not affiliated with any institutions</p>
                  <p className="text-xs text-muted-foreground/60">Your memberships will appear here once added</p>
                </div>
              ) : null}
              {primaryMemberships.length > 0 ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <span className="rounded-full bg-primary/10 px-2 py-1 text-xs font-semibold text-primary">
                      Primary membership
                    </span>
                  </div>
                  {primaryMemberships.map((membership) => (
                    <div key={membership.id} className="rounded-xl border p-4">
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
                  {partnerMemberships.map((membership) => (
                    <div key={membership.id} className="rounded-xl border p-4">
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
                  ))}
                </div>
              ) : null}
            </CardContent>
          </Card>

          {user?.is_superuser ? (
            <Card>
              <CardHeader>
                <CardTitle>Create Institution</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="institution-name">Institution name</Label>
                  <Input
                    id="institution-name"
                    value={form.name}
                    onChange={(event) =>
                      setForm((current) => ({ ...current, name: event.target.value }))
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="institution-domain">Domain</Label>
                  <Input
                    id="institution-domain"
                    placeholder="example.edu"
                    value={form.domain}
                    onChange={(event) =>
                      setForm((current) => ({ ...current, domain: event.target.value }))
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="institution-type">Institution type</Label>
                  <Input
                    id="institution-type"
                    value={form.institution_type}
                    onChange={(event) =>
                      setForm((current) => ({
                        ...current,
                        institution_type: event.target.value as Institution["institution_type"],
                      }))
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="institution-description">Description</Label>
                  <Textarea
                    id="institution-description"
                    value={form.description}
                    onChange={(event) =>
                      setForm((current) => ({
                        ...current,
                        description: event.target.value,
                      }))
                    }
                  />
                </div>
                <Button
                  onClick={() => createMutation.mutate()}
                  disabled={createMutation.isPending || !form.name}
                >
                  Create institution
                </Button>
              </CardContent>
            </Card>
          ) : null}
        </div>
      </div>
    </div>
  )
}
