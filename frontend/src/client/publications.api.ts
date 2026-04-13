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

export type Publication = {
  id: string
  researcher_id: string
  title: string
  publisher: string
  year: number | null
  description: string | null
  citation_count: number
  download_count: number
  view_count: number
  save_count: number
  share_count: number
  last_engagement_at: string | null
  domains: string[]
}

export type AnalyticsTimelinePoint = {
  date: string
  value: number
}

export type PublicationAnalyticsSummary = {
  publication_id: string
  citation_count: number
  download_count: number
  view_count: number
  save_count: number
  share_count: number
  last_engagement_at: string | null
  engagement_last_7_days: AnalyticsTimelinePoint[]
}

export type ResearcherAnalyticsPublication = {
  publication_id: string
  title: string
  year: number | null
  citation_count: number
  download_count: number
  view_count: number
  save_count: number
  share_count: number
}

export type ResearcherAnalyticsSummary = {
  researcher_id: string
  publication_count: number
  total_citations: number
  total_downloads: number
  total_views: number
  total_saves: number
  total_shares: number
  engagement_last_30_days: AnalyticsTimelinePoint[]
  publications: ResearcherAnalyticsPublication[]
}

export const getPublication = async (publicationId: string): Promise<Publication> => {
  const response = await fetch(`${getApiBase()}/api/v1/publications/${publicationId}`, {
    method: "GET",
    headers: getAuthHeaders(),
  })
  return parseResponse<Publication>(response)
}

export const getPublicationAnalytics = async (
  publicationId: string,
): Promise<PublicationAnalyticsSummary> => {
  const response = await fetch(
    `${getApiBase()}/api/v1/publications/${publicationId}/analytics`,
    {
      method: "GET",
      headers: getAuthHeaders(),
    },
  )
  return parseResponse<PublicationAnalyticsSummary>(response)
}

export const trackPublicationEvent = async (
  publicationId: string,
  eventType: "view" | "download" | "save" | "share" | "citation",
  value = 1,
): Promise<Publication> => {
  const response = await fetch(
    `${getApiBase()}/api/v1/publications/${publicationId}/analytics/events`,
    {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ event_type: eventType, value }),
    },
  )
  return parseResponse<Publication>(response)
}

export const updatePublicationAnalytics = async (
  publicationId: string,
  payload: Partial<
    Pick<
      Publication,
      "citation_count" | "download_count" | "view_count" | "save_count" | "share_count"
    >
  >,
): Promise<Publication> => {
  const response = await fetch(
    `${getApiBase()}/api/v1/publications/${publicationId}/analytics`,
    {
      method: "PATCH",
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    },
  )
  return parseResponse<Publication>(response)
}

export const getMyResearcherAnalytics = async (): Promise<ResearcherAnalyticsSummary> => {
  const response = await fetch(`${getApiBase()}/api/v1/researchers/me/analytics`, {
    method: "GET",
    headers: getAuthHeaders(),
  })
  return parseResponse<ResearcherAnalyticsSummary>(response)
}
