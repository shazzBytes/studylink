import { OpenAPI } from './core/OpenAPI'
import type {
  Project,
  ProjectCreate,
  ProjectUpdate,
  ProjectMember,
  MessageResponse,
} from './projects.types'

const BASE_URL = '/api/v1/projects'

/**
 * Create a new research project
 */
export async function createProject(data: ProjectCreate): Promise<Project> {
  const response = await fetch(`${OpenAPI.BASE}${BASE_URL}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${OpenAPI.TOKEN}`,
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error(`Failed to create project: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Get all projects (owned + member + public)
 */
export async function getProjects(): Promise<Project[]> {
  const response = await fetch(`${OpenAPI.BASE}${BASE_URL}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${OpenAPI.TOKEN}`,
    },
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch projects: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Get a project by ID
 */
export async function getProject(projectId: string): Promise<Project> {
  const response = await fetch(`${OpenAPI.BASE}${BASE_URL}/${projectId}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${OpenAPI.TOKEN}`,
    },
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch project: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Update a project (owner only)
 */
export async function updateProject(
  projectId: string,
  data: ProjectUpdate
): Promise<Project> {
  const response = await fetch(`${OpenAPI.BASE}${BASE_URL}/${projectId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${OpenAPI.TOKEN}`,
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error(`Failed to update project: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Delete a project (soft delete, owner only)
 */
export async function deleteProject(projectId: string): Promise<MessageResponse> {
  const response = await fetch(`${OpenAPI.BASE}${BASE_URL}/${projectId}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${OpenAPI.TOKEN}`,
    },
  })

  if (!response.ok) {
    throw new Error(`Failed to delete project: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Get project members
 */
export async function getProjectMembers(projectId: string): Promise<ProjectMember[]> {
  const response = await fetch(`${OpenAPI.BASE}${BASE_URL}/${projectId}/members`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${OpenAPI.TOKEN}`,
    },
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch project members: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Add a member to project (owner only)
 */
export async function addProjectMember(
  projectId: string,
  userId: string
): Promise<MessageResponse> {
  const response = await fetch(
    `${OpenAPI.BASE}${BASE_URL}/${projectId}/members?user_id=${userId}`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${OpenAPI.TOKEN}`,
      },
    }
  )

  if (!response.ok) {
    throw new Error(`Failed to add member: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Remove a member from project (owner only)
 */
export async function removeProjectMember(
  projectId: string,
  userId: string
): Promise<MessageResponse> {
  const response = await fetch(`${OpenAPI.BASE}${BASE_URL}/${projectId}/members/${userId}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${OpenAPI.TOKEN}`,
    },
  })

  if (!response.ok) {
    throw new Error(`Failed to remove member: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Get project by domain (public)
 */
export async function getProjectByDomain(domain: string): Promise<Project> {
  const response = await fetch(`${OpenAPI.BASE}${BASE_URL}/by_domain/${domain}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${OpenAPI.TOKEN}`,
    },
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch project by domain: ${response.statusText}`)
  }

  return response.json()
}
