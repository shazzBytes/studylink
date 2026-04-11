import { zodResolver } from "@hookform/resolvers/zod"
import {
  createFileRoute,
  Link as RouterLink,
  redirect,
} from "@tanstack/react-router"
import { ArrowRight, CheckCircle2 } from "lucide-react"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { AuthLayout } from "@/components/Common/AuthLayout"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { LoadingButton } from "@/components/ui/loading-button"
import { PasswordInput } from "@/components/ui/password-input"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import useAuth, { isLoggedIn } from "@/hooks/useAuth"

const formSchema = z
  .object({
    email: z.email(),
    full_name: z.string().min(1, { message: "Full Name is required" }),
    account_type: z.enum(["student", "researcher"]),
    password: z
      .string()
      .min(1, { message: "Password is required" })
      .min(8, { message: "Password must be at least 8 characters" }),
    confirm_password: z
      .string()
      .min(1, { message: "Password confirmation is required" }),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "The passwords don't match",
    path: ["confirm_password"],
  })

type FormData = z.infer<typeof formSchema>

export const Route = createFileRoute("/signup")({
  component: SignUp,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({
        to: "/",
      })
    }
  },
})

function SignUp() {
  const { signUpMutation } = useAuth()
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      email: "",
      full_name: "",
      account_type: "student",
      password: "",
      confirm_password: "",
    },
  })

  const onSubmit = (data: FormData) => {
    if (signUpMutation.isPending) return

    // exclude confirm_password from submission data
    const { confirm_password: _confirm_password, ...submitData } = data
    signUpMutation.mutate(submitData)
  }

  return (
    <AuthLayout
      eyebrow="New Account"
      title="Create your StudyLink profile"
      description="Join the platform to connect with researchers, manage projects, and participate in team discussions."
      mode="signup"
    >
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex flex-col gap-6"
        >
          <div className="grid gap-3 rounded-2xl border border-emerald-500/15 bg-emerald-500/6 px-4 py-4 text-sm">
            <div className="flex items-center gap-2 font-medium text-emerald-700 dark:text-emerald-300">
              <CheckCircle2 className="size-4" />
              What you unlock
            </div>
            <div className="text-muted-foreground grid gap-2 leading-6 sm:grid-cols-2">
              <p>Build a visible researcher profile for discovery.</p>
              <p>Coordinate projects and chat with collaborators in realtime.</p>
            </div>
          </div>

          <div className="grid gap-5 sm:grid-cols-2">
            <FormField
              control={form.control}
              name="account_type"
              render={({ field }) => (
                <FormItem className="sm:col-span-2">
                  <FormLabel>I am joining as</FormLabel>
                  <FormControl>
                    <RadioGroup
                      onValueChange={field.onChange}
                      value={field.value}
                      className="grid gap-3 sm:grid-cols-2"
                    >
                      <Label
                        htmlFor="account-type-student"
                        className="border-border hover:border-primary/40 has-[button[data-state=checked]]:border-primary has-[button[data-state=checked]]:bg-primary/6 flex items-start gap-3 rounded-2xl border p-4 transition-colors"
                      >
                        <RadioGroupItem
                          value="student"
                          id="account-type-student"
                          className="mt-1"
                        />
                        <div className="space-y-1">
                          <p className="font-semibold">Student</p>
                          <p className="text-muted-foreground text-sm leading-6">
                            Explore researchers, join projects, and grow your
                            academic network.
                          </p>
                        </div>
                      </Label>

                      <Label
                        htmlFor="account-type-researcher"
                        className="border-border hover:border-primary/40 has-[button[data-state=checked]]:border-primary has-[button[data-state=checked]]:bg-primary/6 flex items-start gap-3 rounded-2xl border p-4 transition-colors"
                      >
                        <RadioGroupItem
                          value="researcher"
                          id="account-type-researcher"
                          className="mt-1"
                        />
                        <div className="space-y-1">
                          <p className="font-semibold">Researcher</p>
                          <p className="text-muted-foreground text-sm leading-6">
                            Build a research-focused presence for collaboration
                            and discovery.
                          </p>
                        </div>
                      </Label>
                    </RadioGroup>
                  </FormControl>
                  <FormDescription>
                    Choose the kind of account you want to create.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="full_name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Full Name</FormLabel>
                  <FormControl>
                    <Input
                      data-testid="full-name-input"
                      placeholder="Alex Johnson"
                      type="text"
                      className="h-11 rounded-xl"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input
                      data-testid="email-input"
                      placeholder="user@example.com"
                      type="email"
                      className="h-11 rounded-xl"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <PasswordInput
                      data-testid="password-input"
                      placeholder="Password"
                      className="h-11 rounded-xl"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="confirm_password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirm Password</FormLabel>
                  <FormControl>
                    <PasswordInput
                      data-testid="confirm-password-input"
                      placeholder="Confirm Password"
                      className="h-11 rounded-xl"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <LoadingButton
              type="submit"
              className="h-11 w-full rounded-xl text-sm font-semibold sm:col-span-2"
              loading={signUpMutation.isPending}
            >
              Sign Up
              {!signUpMutation.isPending && <ArrowRight className="size-4" />}
            </LoadingButton>
          </div>

          <div className="text-muted-foreground text-center text-sm">
            Already have an account?{" "}
            <RouterLink
              to="/login"
              className="text-foreground font-medium underline underline-offset-4"
            >
              Log in
            </RouterLink>
          </div>
        </form>
      </Form>
    </AuthLayout>
  )
}

export default SignUp
