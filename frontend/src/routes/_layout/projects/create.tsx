import { createFileRoute, useNavigate, Link } from "@tanstack/react-router"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { z } from "zod"
import {
  createProject,
  type CreateProjectPayload,
  type Project,
} from "@/client/projects.api"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { ArrowLeft } from "lucide-react"
import useCustomToast from "@/hooks/useCustomToast"

export const Route = createFileRoute("/_layout/projects/create")({
  component: CreateProjectPage,
})

const projectSchema = z.object({
  title: z.string().min(1, "Title is required").max(100, "Title is too long"),
  description: z.string().max(500, "Description is too long").optional().or(z.literal("")),
  domain: z
    .string()
    .min(1, "Domain is required")
    .max(50, "Domain is too long")
    .regex(/^[a-z0-9-]+$/, "Domain must be lowercase letters, numbers, and hyphens only"),
  is_public: z.boolean(),
})

type ProjectFormData = z.infer<typeof projectSchema>

function CreateProjectPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const form = useForm<ProjectFormData>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      title: "",
      description: "",
      domain: "",
      is_public: false,
    },
  })

  const createMutation = useMutation({
    mutationFn: (data: CreateProjectPayload) => createProject(data),
    onSuccess: (data: Project) => {
      queryClient.invalidateQueries({ queryKey: ["projects"] })
      showSuccessToast("Project created successfully")
      navigate({ to: "/projects/$id", params: { id: data.id } })
    },
    onError: (error) => {
      showErrorToast(
        error instanceof Error ? error.message : "Failed to create project"
      )
    },
  })

  const onSubmit = (data: ProjectFormData) => {
    createMutation.mutate(data)
  }

  return (
    <div className="container mx-auto max-w-2xl space-y-6 p-6">
      <div>
        <Link to="/projects">
          <Button variant="ghost" size="sm" className="gap-2 mb-4">
            <ArrowLeft className="h-4 w-4" />
            Back to Projects
          </Button>
        </Link>
        <h1 className="text-3xl font-bold tracking-tight">Create New Project</h1>
        <p className="text-muted-foreground">
          Start a new research project and invite collaborators
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Project Details</CardTitle>
          <CardDescription>
            Fill in the information about your research project
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="title"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Project Title</FormLabel>
                    <FormControl>
                      <Input placeholder="AI for Healthcare" {...field} />
                    </FormControl>
                    <FormDescription>
                      A clear, descriptive name for your project
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="domain"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Domain</FormLabel>
                    <FormControl>
                      <div className="flex items-center gap-2">
                        <span className="text-muted-foreground">/</span>
                        <Input
                          placeholder="healthcare-ai"
                          {...field}
                          onChange={(e) => {
                            field.onChange(e.target.value.toLowerCase())
                          }}
                        />
                      </div>
                    </FormControl>
                    <FormDescription>
                      Unique URL-friendly identifier (lowercase, hyphens allowed)
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Research on AI diagnostics..."
                        className="resize-none"
                        rows={4}
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Describe what your research project is about
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="is_public"
                render={({ field }) => (
                  <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
                    <div className="space-y-0.5">
                      <FormLabel className="text-base">Public Project</FormLabel>
                      <FormDescription>
                        Allow anyone to view this project
                      </FormDescription>
                    </div>
                    <FormControl>
                      <Switch
                        checked={field.value}
                        onCheckedChange={field.onChange}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />

              <div className="flex gap-2 justify-end">
                <Link to="/projects">
                  <Button type="button" variant="outline">
                    Cancel
                  </Button>
                </Link>
                <Button type="submit" disabled={createMutation.isPending}>
                  {createMutation.isPending ? "Creating..." : "Create Project"}
                </Button>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  )
}
