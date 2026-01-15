import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuCheckboxItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Search, X, Filter, Calendar, Building2, FileText } from "lucide-react"
import { useState } from "react"

export interface SearchFilters {
  publishers?: string[]
  categories?: string[]
  dateRange?: string
  verified?: boolean
}

interface SearchBarProps {
  placeholder?: string
  onSearch?: (query: string, filters: SearchFilters) => void
  className?: string
  showKeyboardHint?: boolean
  showFilters?: boolean
  availablePublishers?: string[]
  availableCategories?: string[]
}

export function SearchBar({
  placeholder = "Search...",
  onSearch,
  className = "",
  showKeyboardHint = true,
  showFilters = true,
  availablePublishers = ["IEEE", "ACM", "Springer", "Nature", "Science", "arXiv"],
  availableCategories = ["Deep Learning", "Computer Vision", "NLP", "Robotics", "AI Ethics"],
}: SearchBarProps) {
  const [searchQuery, setSearchQuery] = useState("")
  const [filters, setFilters] = useState<SearchFilters>({
    publishers: [],
    categories: [],
    dateRange: "",
    verified: false,
  })

  const handleSearchChange = (value: string) => {
    setSearchQuery(value)
    onSearch?.(value, filters)
  }

  const clearSearch = () => {
    setSearchQuery("")
    onSearch?.("", filters)
  }

  const togglePublisher = (publisher: string) => {
    const newPublishers = filters.publishers?.includes(publisher)
      ? filters.publishers.filter((p) => p !== publisher)
      : [...(filters.publishers || []), publisher]
    
    const newFilters = { ...filters, publishers: newPublishers }
    setFilters(newFilters)
    onSearch?.(searchQuery, newFilters)
  }

  const toggleCategory = (category: string) => {
    const newCategories = filters.categories?.includes(category)
      ? filters.categories.filter((c) => c !== category)
      : [...(filters.categories || []), category]
    
    const newFilters = { ...filters, categories: newCategories }
    setFilters(newFilters)
    onSearch?.(searchQuery, newFilters)
  }

  const setDateRange = (range: string) => {
    const newFilters = { ...filters, dateRange: range }
    setFilters(newFilters)
    onSearch?.(searchQuery, newFilters)
  }

  const toggleVerified = () => {
    const newFilters = { ...filters, verified: !filters.verified }
    setFilters(newFilters)
    onSearch?.(searchQuery, newFilters)
  }

  const clearAllFilters = () => {
    const emptyFilters: SearchFilters = {
      publishers: [],
      categories: [],
      dateRange: "",
      verified: false,
    }
    setFilters(emptyFilters)
    setSearchQuery("")
    onSearch?.("", emptyFilters)
  }

  const activeFilterCount = 
    (filters.publishers?.length || 0) + 
    (filters.categories?.length || 0) + 
    (filters.dateRange ? 1 : 0) + 
    (filters.verified ? 1 : 0)

  const hasActiveFilters = activeFilterCount > 0 || searchQuery !== ""

  return (
    <div className={`w-full space-y-3 ${className}`}>
      <div className="flex gap-2">
        {/* Search Input */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
          <Input
            type="search"
            placeholder={placeholder}
            className="pl-11 pr-10 h-12 bg-muted/50 border-2 focus:bg-background transition-colors"
            value={searchQuery}
            onChange={(e) => handleSearchChange(e.target.value)}
          />
          {searchQuery && (
            <button
              onClick={clearSearch}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
              aria-label="Clear search"
            >
              <X className="h-4 w-4" />
            </button>
          )}
          {showKeyboardHint && !searchQuery && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 hidden md:block">
              <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
                <span className="text-xs">⌘</span>K
              </kbd>
            </div>
          )}
        </div>

        {/* Single Filter Button */}
        {showFilters && (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="lg" className="h-12 gap-2">
                <Filter className="h-5 w-5" />
                Filters
                {activeFilterCount > 0 && (
                  <Badge variant="secondary" className="ml-1 px-2 py-0.5 text-xs">
                    {activeFilterCount}
                  </Badge>
                )}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-72">
              {/* Publishers Section */}
              <DropdownMenuLabel className="flex items-center gap-2">
                <Building2 className="h-4 w-4" />
                Publishers
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              {availablePublishers.map((publisher) => (
                <DropdownMenuCheckboxItem
                  key={publisher}
                  checked={filters.publishers?.includes(publisher)}
                  onCheckedChange={() => togglePublisher(publisher)}
                >
                  {publisher}
                </DropdownMenuCheckboxItem>
              ))}

              <DropdownMenuSeparator />

              {/* Categories Section */}
              <DropdownMenuLabel className="flex items-center gap-2">
                <FileText className="h-4 w-4" />
                Categories
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              {availableCategories.map((category) => (
                <DropdownMenuCheckboxItem
                  key={category}
                  checked={filters.categories?.includes(category)}
                  onCheckedChange={() => toggleCategory(category)}
                >
                  {category}
                </DropdownMenuCheckboxItem>
              ))}

              <DropdownMenuSeparator />

              {/* Date Range Section */}
              <DropdownMenuLabel className="flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                Date Range
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuCheckboxItem
                checked={filters.dateRange === "last7days"}
                onCheckedChange={() => setDateRange(filters.dateRange === "last7days" ? "" : "last7days")}
              >
                Last 7 days
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={filters.dateRange === "last30days"}
                onCheckedChange={() => setDateRange(filters.dateRange === "last30days" ? "" : "last30days")}
              >
                Last 30 days
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={filters.dateRange === "last6months"}
                onCheckedChange={() => setDateRange(filters.dateRange === "last6months" ? "" : "last6months")}
              >
                Last 6 months
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={filters.dateRange === "lastyear"}
                onCheckedChange={() => setDateRange(filters.dateRange === "lastyear" ? "" : "lastyear")}
              >
                Last year
              </DropdownMenuCheckboxItem>

              <DropdownMenuSeparator />

              {/* Additional Filters */}
              <DropdownMenuLabel>Other Options</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuCheckboxItem
                checked={filters.verified}
                onCheckedChange={toggleVerified}
              >
                Verified only
              </DropdownMenuCheckboxItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )}
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm text-muted-foreground">Active filters:</span>
          
          {filters.publishers?.map((publisher) => (
            <Badge key={publisher} variant="secondary" className="gap-1">
              {publisher}
              <button
                onClick={() => togglePublisher(publisher)}
                className="ml-1 hover:text-foreground"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          ))}
          
          {filters.categories?.map((category) => (
            <Badge key={category} variant="secondary" className="gap-1">
              {category}
              <button
                onClick={() => toggleCategory(category)}
                className="ml-1 hover:text-foreground"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          ))}
          
          {filters.dateRange && (
            <Badge variant="secondary" className="gap-1">
              {filters.dateRange === "last7days" && "Last 7 days"}
              {filters.dateRange === "last30days" && "Last 30 days"}
              {filters.dateRange === "last6months" && "Last 6 months"}
              {filters.dateRange === "lastyear" && "Last year"}
              <button
                onClick={() => setDateRange("")}
                className="ml-1 hover:text-foreground"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          )}
          
          {filters.verified && (
            <Badge variant="secondary" className="gap-1">
              Verified only
              <button
                onClick={toggleVerified}
                className="ml-1 hover:text-foreground"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          )}
          
          <Button
            variant="ghost"
            size="sm"
            onClick={clearAllFilters}
            className="h-6 text-xs"
          >
            Clear all
          </Button>
        </div>
      )}
    </div>
  )
}
