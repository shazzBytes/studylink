export type DemoNotification = {
  id: string
  type: "like" | "comment" | "follow" | "mention" | "publication"
  user: {
    name: string
    avatarUrl: string
  }
  content: string
  timestamp: string
  read: boolean
  link?: string
}

export const demoNotifications: DemoNotification[] = [
  {
    id: "1",
    type: "like",
    user: {
      name: "Dr. Sarah Johnson",
      avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah",
    },
    content: 'liked your paper "Deep Learning for Computer Vision"',
    timestamp: "2 hours ago",
    read: false,
    link: "/papers/deep-learning-computer-vision",
  },
  {
    id: "2",
    type: "follow",
    user: {
      name: "Dr. Michael Chen",
      avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Michael",
    },
    content: "started following you",
    timestamp: "5 hours ago",
    read: false,
    link: "/researchers",
  },
  {
    id: "3",
    type: "comment",
    user: {
      name: "Dr. Emily Watson",
      avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Emily",
    },
    content: 'commented on your paper: "Great insights on neural architecture!"',
    timestamp: "1 day ago",
    read: true,
    link: "/papers/neural-architecture-search-efficient-models",
  },
  {
    id: "4",
    type: "publication",
    user: {
      name: "Dr. Alice Brown",
      avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Alice",
    },
    content: 'published a new paper "Transformer Models in NLP"',
    timestamp: "2 days ago",
    read: true,
    link: "/papers/transformer-models-nlp",
  },
  {
    id: "5",
    type: "mention",
    user: {
      name: "Dr. John Smith",
      avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=John",
    },
    content: "mentioned you in a project discussion",
    timestamp: "3 days ago",
    read: true,
    link: "/projects",
  },
]
