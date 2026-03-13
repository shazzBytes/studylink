import { Button } from "@/components/ui/button"
import useAuth from "@/hooks/useAuth"

export default function Logout() {
  const { logout } = useAuth()

  return (
    <div className="max-w-md">
      <h3 className="py-4 text-lg font-semibold">Logout</h3>
      <p className="mb-4 text-sm text-muted-foreground">
        End your current session on this device.
      </p>
      <Button onClick={logout}>Log out</Button>
    </div>
  )
}
