import { BadgeCheck, ChartNoAxesColumn, MessagesSquare, ShieldCheck } from "lucide-react"

import { Appearance } from "@/components/Common/Appearance"
import { cn } from "@/lib/utils"
import { Footer } from "./Footer"

interface AuthLayoutProps {
  children: React.ReactNode
  eyebrow?: string
  title?: string
  description?: string
  mode?: "login" | "signup"
}

const authHighlights = [
  {
    icon: ShieldCheck,
    title: "Protected access",
    description: "Secure account flows keep projects, chats, and profiles private.",
  },
  {
    icon: MessagesSquare,
    title: "Team coordination",
    description: "Move from discovery to discussion without leaving the workspace.",
  },
  {
    icon: ChartNoAxesColumn,
    title: "Research momentum",
    description: "Track collaborators, publications, and active project work in one place.",
  },
]

const authStats = [
  { label: "Profiles", value: "Smart" },
  { label: "Projects", value: "Shared" },
  { label: "Chat", value: "Realtime" },
]

export function AuthLayout({
  children,
  eyebrow = "Welcome",
  title = "Access StudyLink",
  description = "Sign in to continue collaborating with your research network.",
  mode = "login",
}: AuthLayoutProps) {
  return (
    <div className="from-background via-background to-primary/8 relative min-h-svh overflow-hidden bg-gradient-to-br">
      <div className="bg-primary/10 absolute inset-x-0 top-0 h-64 blur-3xl" />
      <div className="absolute inset-y-0 left-0 hidden w-1/2 bg-[radial-gradient(circle_at_top_left,rgba(20,184,166,0.16),transparent_42%),radial-gradient(circle_at_bottom_left,rgba(15,23,42,0.12),transparent_38%)] lg:block dark:bg-[radial-gradient(circle_at_top_left,rgba(45,212,191,0.14),transparent_42%),radial-gradient(circle_at_bottom_left,rgba(255,255,255,0.08),transparent_38%)]" />

      <div className="relative grid min-h-svh lg:grid-cols-[1.15fr_0.85fr]">
        <section className="relative hidden px-10 py-10 lg:flex lg:flex-col lg:justify-between xl:px-16">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-primary text-sm font-semibold tracking-[0.28em] uppercase">
                StudyLink
              </p>
              <p className="text-muted-foreground mt-2 max-w-sm text-sm leading-6">
                The collaboration workspace for research teams building ideas
                together.
              </p>
            </div>
            <Appearance />
          </div>

          <div className="max-w-xl space-y-10">
            <div className="space-y-5">
              <div className="text-primary/80 inline-flex items-center gap-2 rounded-full border border-current/15 bg-background/65 px-4 py-1 text-xs font-semibold tracking-[0.24em] uppercase shadow-sm backdrop-blur">
                <BadgeCheck className="size-3.5" />
                Research Network
              </div>
              <div className="space-y-4">
                <h1 className="text-foreground text-4xl font-semibold tracking-tight xl:text-5xl">
                  Collaborate with the right people faster.
                </h1>
                <p className="text-muted-foreground max-w-lg text-base leading-7 xl:text-lg">
                  Build your profile, discover aligned researchers, and keep
                  projects moving from first contact to final output.
                </p>
              </div>
            </div>

            <div className="grid gap-4">
              {authHighlights.map(({ icon: Icon, title, description }) => (
                <div
                  key={title}
                  className="bg-background/72 border-border/60 flex items-start gap-4 rounded-2xl border p-4 shadow-sm backdrop-blur"
                >
                  <div className="bg-primary/12 text-primary flex size-11 shrink-0 items-center justify-center rounded-2xl">
                    <Icon className="size-5" />
                  </div>
                  <div className="space-y-1.5">
                    <p className="text-sm font-semibold">{title}</p>
                    <p className="text-muted-foreground text-sm leading-6">
                      {description}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-3 gap-3">
              {authStats.map((stat) => (
                <div
                  key={stat.label}
                  className="bg-background/72 border-border/60 rounded-2xl border p-4 shadow-sm backdrop-blur"
                >
                  <p className="text-foreground text-xl font-semibold">
                    {stat.value}
                  </p>
                  <p className="text-muted-foreground mt-1 text-xs uppercase tracking-[0.22em]">
                    {stat.label}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <p className="text-muted-foreground text-sm leading-6">
            {mode === "login"
              ? "Pick up where your team left off with projects, messages, and profile updates waiting for you."
              : "Create your account to join conversations, publish your profile, and start collaborating with your next research team."}
          </p>
        </section>

        <section className="flex flex-col p-5 sm:p-7 lg:p-10">
          <div className="flex justify-end lg:hidden">
            <Appearance />
          </div>

          <div className="flex flex-1 items-center justify-center py-8 lg:py-0">
            <div className="w-full max-w-xl">
              <div
                className={cn(
                  "bg-background/86 border-border/60 shadow-primary/5 rounded-[2rem] border p-6 shadow-2xl backdrop-blur sm:p-8",
                  mode === "signup" && "max-w-2xl"
                )}
              >
                <div className="mb-8 space-y-3">
                  <p className="text-primary text-xs font-semibold tracking-[0.24em] uppercase">
                    {eyebrow}
                  </p>
                  <div className="space-y-2">
                    <h2 className="text-3xl font-semibold tracking-tight">
                      {title}
                    </h2>
                    <p className="text-muted-foreground max-w-lg text-sm leading-6">
                      {description}
                    </p>
                  </div>
                </div>

                {children}
              </div>
            </div>
          </div>

          <Footer />
        </section>
      </div>
    </div>
  )
}
