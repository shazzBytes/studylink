import { createFileRoute } from "@tanstack/react-router"
import { PaperCard } from "@/components/Common/PaperCard"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { TrendingUp, Clock, Star } from "lucide-react"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  // Mock research papers data - replace with actual API call
  const papers = [
    {
      id: "1",
      title: "Deep Learning for Computer Vision",
      author: "Dr. Alice Brown",
      publishedDate: "January 5, 2026",
      summary: "An extensive study on the advancements in deep learning techniques applied to computer vision tasks such as image recognition, object detection, and segmentation.",
      coverImageUrl: "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
      impressions: 12543,
      isVerified: true,
    },
    {
      id: "2",
      title: "Neural Architecture Search for Efficient Models",
      author: "Dr. Alice Brown",
      publishedDate: "December 20, 2025",
      summary: "This paper presents a novel approach to neural architecture search that significantly reduces computational costs while maintaining high accuracy across various benchmarks.",
      coverImageUrl: "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
      impressions: 8921,
      isVerified: true,
    },
    {
      id: "3",
      title: "Transformer Models in Natural Language Processing",
      author: "Dr. John Smith",
      publishedDate: "December 15, 2025",
      summary: "A comprehensive analysis of transformer architectures and their applications in modern NLP tasks, including machine translation and text generation.",
      coverImageUrl: "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
      impressions: 15678,
      isVerified: true,
    },
    {
      id: "4",
      title: "Reinforcement Learning in Robotics",
      author: "Dr. Sarah Johnson",
      publishedDate: "December 10, 2025",
      summary: "Exploring the application of deep reinforcement learning algorithms in robotic control systems and autonomous navigation.",
      coverImageUrl: "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
      impressions: 6543,
      isVerified: false,
    },
    {
      id: "5",
      title: "Ethical Considerations in AI Development",
      author: "Dr. Michael Chen",
      publishedDate: "December 8, 2025",
      summary: "A critical examination of ethical frameworks and responsible AI practices in the development and deployment of artificial intelligence systems.",
      coverImageUrl: "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
      impressions: 9876,
      isVerified: true,
    },
    {
      id: "6",
      title: "Quantum Computing and Machine Learning",
      author: "Dr. Emily Watson",
      publishedDate: "December 5, 2025",
      summary: "Investigating the intersection of quantum computing and machine learning, exploring quantum algorithms for accelerating ML tasks.",
      coverImageUrl: "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
      impressions: 11234,
      isVerified: true,
    },
  ]

  return (
    <div className="container mx-auto max-w-3xl space-y-6 p-6">
      {/* Header Section */}
      <div className="space-y-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Research Paper Feed</h1>
          <p className="text-muted-foreground">
            Discover the latest research papers from leading researchers worldwide
          </p>
        </div>

        {/* Tabs for filtering */}
        <Tabs defaultValue="trending" className="w-full">
          <TabsList className="grid w-full max-w-md grid-cols-3">
            <TabsTrigger value="trending" className="gap-2">
              <TrendingUp className="h-4 w-4" />
              Trending
            </TabsTrigger>
            <TabsTrigger value="recent" className="gap-2">
              <Clock className="h-4 w-4" />
              Recent
            </TabsTrigger>
            <TabsTrigger value="following" className="gap-2">
              <Star className="h-4 w-4" />
              Following
            </TabsTrigger>
          </TabsList>

          {/* Trending Papers */}
          <TabsContent value="trending" className="space-y-4 mt-6">
            {papers
              .sort((a, b) => b.impressions - a.impressions)
              .map((paper) => (
                <PaperCard
                  key={paper.id}
                  title={paper.title}
                  author={paper.author}
                  publishedDate={paper.publishedDate}
                  summary={paper.summary}
                  coverImageUrl={paper.coverImageUrl}
                  impressions={paper.impressions}
                  isVerified={paper.isVerified}
                />
              ))}
          </TabsContent>

          {/* Recent Papers */}
          <TabsContent value="recent" className="space-y-4 mt-6">
            {papers.map((paper) => (
              <PaperCard
                key={paper.id}
                title={paper.title}
                author={paper.author}
                publishedDate={paper.publishedDate}
                summary={paper.summary}
                coverImageUrl={paper.coverImageUrl}
                impressions={paper.impressions}
                isVerified={paper.isVerified}
              />
            ))}
          </TabsContent>

          {/* Following Papers */}
          <TabsContent value="following" className="space-y-4 mt-6">
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Star className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No papers yet</h3>
              <p className="text-muted-foreground mb-4 max-w-sm">
                Follow researchers to see their latest papers here
              </p>
              <Button>Discover Researchers</Button>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
