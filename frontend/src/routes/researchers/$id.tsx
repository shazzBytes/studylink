import { createFileRoute } from "@tanstack/react-router"
import { ResearcherHeader } from "@/components/Common/ResearcherHeader"
import { ResearcherSummary } from "@/components/Common/ResearcherSummary"
import { ResearcherInterests } from "@/components/Common/ResearcherInterests"
import { ResearcherPublications } from "@/components/Common/ResearcherPublications"
import { ResearcherMentorship } from "@/components/Common/ResearcherMentorship"
import { ResearcherConnect } from "@/components/Common/ResearcherConnect"

export const Route = createFileRoute("/researchers/$id")({
  component: ResearcherProfile,
})

function ResearcherProfile() {
  // Mock data - replace with actual API call using route params
  const researcher = {
    id: "1",
    name: "Dr. Alice Brown",
    role: "Associate Professor",
    affiliation: "Massachusetts Institute of Technology",
    location: "Cambridge, MA",
    avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Alice",
    bio: "Dr. Brown is a leading researcher in deep learning and computer vision with over 15 years of experience. Her work focuses on developing novel architectures for image recognition and object detection.",
    researchInterests: [
      "Deep Learning",
      "Computer Vision",
      "Neural Networks",
      "Image Recognition",
      "Object Detection",
      "Machine Learning"
    ],
    publications: [
      {
        id: "1",
        title: "Deep Learning for Computer Vision",
        author: "Dr. Alice Brown",
        publishedDate: "January 5, 2026",
        summary: "An extensive study on the advancements in deep learning techniques applied to computer vision tasks such as image recognition, object detection, and segmentation.",
        coverImageUrl: "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
        impressions: 12543,
        isVerified: true
      },
      {
        id: "2",
        title: "Neural Architecture Search for Efficient Models",
        author: "Dr. Alice Brown",
        publishedDate: "September 20, 2025",
        summary: "This paper presents a novel approach to neural architecture search that significantly reduces computational costs while maintaining high accuracy across various benchmarks.",
        coverImageUrl: "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
        impressions: 8921,
        isVerified: true
      }
    ],
    mentorship: {
      available: true,
      areas: ["Deep Learning", "Computer Vision", "PhD Supervision"],
      note: "Currently accepting PhD students for Fall 2026. Please reach out via email with your research proposal."
    },
    externalLinks: {
      email: "alice.brown@mit.edu",
      linkedin: "https://linkedin.com/in/alicebrown",
      website: "https://alicebrown.mit.edu"
    },
    stats: {
      publications: 47,
      citations: 3245,
      hIndex: 28
    }
  }

  const handleMentorshipClick = () => {
    const mentorshipSection = document.getElementById('mentorship-section')
    if (mentorshipSection) {
      mentorshipSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  return (
    <div className="container mx-auto space-y-6 px-6 pb-6">
      <ResearcherHeader
        name={researcher.name}
        role={researcher.role}
        affiliation={researcher.affiliation}
        location={researcher.location}
        avatarUrl={researcher.avatarUrl}
        mentorshipAvailable={researcher.mentorship.available}
        onMentorshipClick={handleMentorshipClick}
        stats={researcher.stats}
      />

      <ResearcherSummary bio={researcher.bio} />

      <ResearcherInterests interests={researcher.researchInterests} />

      <ResearcherPublications publications={researcher.publications} />

      <ResearcherMentorship
        available={researcher.mentorship.available}
        areas={researcher.mentorship.areas}
        note={researcher.mentorship.note}
      />

      <ResearcherConnect
        email={researcher.externalLinks.email}
        linkedin={researcher.externalLinks.linkedin}
        website={researcher.externalLinks.website}
      />
    </div>
  )
}
