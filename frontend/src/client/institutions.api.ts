const getApiBase = () => import.meta.env.VITE_API_URL || ""

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token")
  return {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "",
  }
}

const parseResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    let detail = "Request failed"
    try {
      const body = await response.json()
      detail = body?.detail || detail
    } catch {
      // Ignore non-JSON failures.
    }
    throw new Error(detail)
  }

  return (await response.json()) as T
}

export type Institution = {
  id: string
  name: string
  slug: string
  domain: string | null
  institution_type: "university" | "college" | "research_institute"
  description: string | null
  is_verified: boolean
  is_active: boolean
  onboarding_enabled: boolean
  member_count: number
}

export type InstitutionMembership = {
  id: string
  institution_id: string
  institution_name: string
  institution_slug: string
  role: "admin" | "faculty" | "student" | "researcher" | "staff"
  department: string | null
  title: string | null
  is_primary: boolean
  is_verified: boolean
  user_id: string
  user_email: string
  user_full_name: string | null
}

export type CreateInstitutionPayload = {
  name: string
  domain?: string
  institution_type: Institution["institution_type"]
  description?: string
  is_verified?: boolean
  onboarding_enabled?: boolean
}

export type BulkOnboardMemberPayload = {
  email: string
  password: string
  full_name?: string
  account_type: "student" | "researcher"
  role: InstitutionMembership["role"]
  department?: string
  title?: string
  is_primary?: boolean
  is_verified?: boolean
}

export type BulkOnboardResult = {
  created_users: number
  updated_memberships: number
  memberships: InstitutionMembership[]
}

export const getInstitutions = async (): Promise<Institution[]> => {
  const response = await fetch(`${getApiBase()}/api/v1/institutions`, {
    method: "GET",
    headers: getAuthHeaders(),
  })
  return parseResponse<Institution[]>(response)
}

export const getMyInstitutionMemberships = async (): Promise<
  InstitutionMembership[]
> => {
  const response = await fetch(`${getApiBase()}/api/v1/institutions/me/memberships`, {
    method: "GET",
    headers: getAuthHeaders(),
  })
  return parseResponse<InstitutionMembership[]>(response)
}

export const getInstitutionMembers = async (
  institutionId: string,
): Promise<InstitutionMembership[]> => {
  const response = await fetch(
    `${getApiBase()}/api/v1/institutions/${institutionId}/members`,
    {
      method: "GET",
      headers: getAuthHeaders(),
    },
  )
  return parseResponse<InstitutionMembership[]>(response)
}

export const createInstitution = async (
  payload: CreateInstitutionPayload,
): Promise<Institution> => {
  const response = await fetch(`${getApiBase()}/api/v1/institutions`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  })
  return parseResponse<Institution>(response)
}

export const bulkOnboardInstitutionMembers = async (
  institutionId: string,
  members: BulkOnboardMemberPayload[],
): Promise<BulkOnboardResult> => {
  const response = await fetch(
    `${getApiBase()}/api/v1/institutions/${institutionId}/bulk-onboard`,
    {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ members }),
    },
  )
  return parseResponse<BulkOnboardResult>(response)
}
