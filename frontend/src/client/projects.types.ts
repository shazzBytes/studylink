// Project API Types
export interface Project {
  id: string
  title: string
  description: string | null
  domain: string
  owner_id: string
  is_public: boolean
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  title: string
  description?: string | null
  domain: string
  is_public: boolean
}

export interface ProjectUpdate {
  title?: string
  description?: string | null
  is_public?: boolean
}

export interface ProjectMember {
  user_id: string
  role: string
  added_at: string
}

export interface MessageResponse {
  message: string
}
