export function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-border/60 flex flex-col gap-1 border-t px-6 py-4 text-center sm:text-left">
      <p className="text-sm font-medium">StudyLink</p>
      <p className="text-muted-foreground text-xs">
        Built for researchers, teams, and academic collaboration. {currentYear}
      </p>
    </footer>
  )
}
