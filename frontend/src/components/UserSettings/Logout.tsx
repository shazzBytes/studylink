import { LogOut } from "lucide-react"

import { Button } from "@/components/ui/button"
import useAuth from "@/hooks/useAuth"

const Logout = () => {
  const { logout } = useAuth()

  return (
    <div className="max-w-md mt-4 rounded-lg border p-4">
      <h3 className="font-semibold">Log Out</h3>
      <p className="mt-1 text-sm text-muted-foreground">
        Sign out of your current session on this device.
      </p>
      <Button className="mt-4 gap-2" variant="outline" onClick={logout}>
        <LogOut className="h-4 w-4" />
        Log Out
      </Button>
    </div>
  )
}

export default Logout
