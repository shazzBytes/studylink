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
      // Ignore parse failures for non-JSON error responses.
    }
    throw new Error(detail)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}

export type Project = {
  id: string
  title: string
  description: string | null
  domain: string
  owner_id: string
  is_public: boolean
}

export type ProjectMember = {
  user_id: string
  role: string
  added_at: string
}

export type CreateProjectPayload = {
  title: string
  description?: string
  domain: string
  is_public: boolean
}

export const getProjects = async (): Promise<Project[]> => {
  const response = await fetch(`${getApiBase()}/api/v1/search/projects`, {
    method: "GET",
    headers: getAuthHeaders(),
  })
  return parseResponse<Project[]>(response)
}

export const getProject = async (id: string): Promise<Project> => {
  const projects = await getProjects()
  const project = projects.find((item) => item.id === id)
  if (!project) {
    throw new Error("Project not found")
  }
  return project
}

export const createProject = async (
  payload: CreateProjectPayload,
): Promise<Project> => {
  const response = await fetch(`${getApiBase()}/api/v1/projects`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  })
  return parseResponse<Project>(response)
}

export const deleteProject = async (id: string): Promise<void> => {
  const response = await fetch(`${getApiBase()}/api/v1/projects/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  })
  return parseResponse<void>(response)
}

export const getProjectMembers = async (
  projectId: string,
): Promise<ProjectMember[]> => {
  const response = await fetch(`${getApiBase()}/api/v1/projects/${projectId}/members`, {
    method: "GET",
    headers: getAuthHeaders(),
  })
  return parseResponse<ProjectMember[]>(response)
}
