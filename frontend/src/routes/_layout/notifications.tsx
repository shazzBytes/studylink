import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Bell, Heart, MessageSquare, UserPlus, FileText, Check } from "lucide-react"
import {
  demoNotifications,
  type DemoNotification,
} from "@/lib/demo-notifications"

export const Route = createFileRoute("/_layout/notifications")({
  component: NotificationsPage,
})

function NotificationsPage() {
  const [notifications, setNotifications] = useState(demoNotifications)

  const unreadNotifications = notifications.filter((n) => !n.read)
  const allNotifications = notifications

  const getIcon = (type: DemoNotification["type"]) => {
    switch (type) {
      case "like":
        return <Heart className="h-5 w-5 text-red-500" />
      case "comment":
        return <MessageSquare className="h-5 w-5 text-blue-500" />
      case "follow":
        return <UserPlus className="h-5 w-5 text-green-500" />
      case "mention":
        return <MessageSquare className="h-5 w-5 text-purple-500" />
      case "publication":
        return <FileText className="h-5 w-5 text-orange-500" />
    }
  }

  const markAllAsRead = () => {
    setNotifications((current) =>
      current.map((notification) => ({ ...notification, read: true }))
    )
  }

  const NotificationCard = ({ notification }: { notification: DemoNotification }) => {
    const card = (
      <Card className={notification.read ? "" : "bg-muted/50 border-primary/20"}>
        <CardContent className="p-4">
          <div className="flex gap-4">
            <div className="relative">
              <Avatar className="h-12 w-12">
                <AvatarImage src={notification.user.avatarUrl} alt={notification.user.name} />
                <AvatarFallback>{notification.user.name.split(" ").map((n) => n[0]).join("")}</AvatarFallback>
              </Avatar>
              <div className="absolute -bottom-1 -right-1 rounded-full bg-background p-1">
                {getIcon(notification.type)}
              </div>
            </div>

            <div className="flex-1 space-y-1">
              <div className="flex items-start justify-between">
                <div>
                  <span className="font-semibold">{notification.user.name}</span>
                  <span className="ml-1 text-sm text-muted-foreground">
                    {notification.content}
                  </span>
                </div>
                {!notification.read && (
                  <Badge variant="default" className="ml-2 h-2 w-2 rounded-full p-0" />
                )}
              </div>
              <p className="text-xs text-muted-foreground">{notification.timestamp}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    )

    if (notification.link) {
      return (
        <a href={notification.link} className="block">
          {card}
        </a>
      )
    }

    return card
  }

  return (
    <div className="container mx-auto max-w-3xl space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Notifications</h1>
          <p className="text-muted-foreground">
            Stay updated with your research community
          </p>
        </div>
        {unreadNotifications.length > 0 && (
          <Button variant="ghost" size="sm" onClick={markAllAsRead} className="gap-2">
            <Check className="h-4 w-4" />
            Mark all as read
          </Button>
        )}
      </div>

      {/* Tabs */}
      <Tabs defaultValue="all" className="w-full">
        <TabsList className="grid w-full max-w-md grid-cols-2">
          <TabsTrigger value="all" className="gap-2">
            <Bell className="h-4 w-4" />
            All
          </TabsTrigger>
          <TabsTrigger value="unread" className="gap-2">
            <Bell className="h-4 w-4" />
            Unread
            {unreadNotifications.length > 0 && (
              <Badge variant="secondary" className="ml-1">
                {unreadNotifications.length}
              </Badge>
            )}
          </TabsTrigger>
        </TabsList>

        {/* All Notifications */}
        <TabsContent value="all" className="space-y-4 mt-6">
          {allNotifications.length > 0 ? (
            allNotifications.map((notification) => (
              <NotificationCard key={notification.id} notification={notification} />
            ))
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                <Bell className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No notifications yet</h3>
                <p className="text-sm text-muted-foreground">
                  When you get notifications, they'll show up here
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Unread Notifications */}
        <TabsContent value="unread" className="space-y-4 mt-6">
          {unreadNotifications.length > 0 ? (
            unreadNotifications.map((notification) => (
              <NotificationCard key={notification.id} notification={notification} />
            ))
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                <Check className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">All caught up!</h3>
                <p className="text-sm text-muted-foreground">
                  You've read all your notifications
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
