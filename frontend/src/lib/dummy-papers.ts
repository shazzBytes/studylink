export type DummyPaper = {
  id: string
  title: string
  author: string
  authors: Array<{
    name: string
    affiliation: string
  }>
  publishedDate: string
  summary: string
  coverImageUrl: string
  impressions?: number
  isVerified?: boolean
  abstract: string
  keywords: string[]
  journal: string
  volume: string
  issue: string
  pages: string
  doi: string
  citationCount: number
  readTime: string
  sections: Array<{
    heading: string
    content: string
  }>
}

export const dummyPapers: DummyPaper[] = [
  {
    id: "deep-learning-computer-vision",
    title: "Deep Learning for Computer Vision",
    author: "Dr. Alice Brown",
    authors: [
      {
        name: "Dr. Alice Brown",
        affiliation: "Institute for Applied Intelligence, Department of Vision Systems",
      },
      {
        name: "Dr. Maya Patel",
        affiliation: "Clinical Machine Perception Lab, Horizon Medical University",
      },
    ],
    publishedDate: "January 5, 2026",
    summary:
      "An extensive study on the advancements in deep learning techniques applied to computer vision tasks such as image recognition, object detection, and segmentation.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 12543,
    isVerified: true,
    abstract:
      "This paper surveys modern deep learning methods for computer vision and evaluates how convolutional and transformer-based architectures perform across classification, detection, and segmentation tasks in real-world conditions. We synthesize benchmark evidence, deployment constraints, and clinical-adjacent application lessons to outline a practical perspective on the current state of visual intelligence systems.",
    keywords: ["Computer Vision", "Deep Learning", "Transformers", "Image Recognition"],
    journal: "Journal of Vision Systems",
    volume: "Vol. 18",
    issue: "Issue 1",
    pages: "pp. 41-67",
    doi: "10.2147/jvs.2026.04167",
    citationCount: 214,
    readTime: "18 min read",
    sections: [
      {
        heading: "Introduction",
        content:
          "Computer vision research has transitioned from manually engineered feature pipelines toward data-driven representation learning. This shift has materially changed not only benchmark performance, but also how teams design annotation strategies, reason about transfer learning, and evaluate robustness under domain shift. In this paper we revisit that progression and emphasize why performance on static datasets is no longer sufficient as a standalone measure of practical utility.",
      },
      {
        heading: "Methodology",
        content:
          "We compare convolutional, hybrid, and transformer-based architectures across representative tasks including image classification, object detection, and semantic segmentation. Beyond top-line accuracy, we analyze calibration, latency, parameter efficiency, and annotation sensitivity. Our review uses a comparative synthesis framework designed to make architectural tradeoffs interpretable to applied teams, particularly those operating under moderate compute constraints.",
      },
      {
        heading: "Results",
        content:
          "Transformer-heavy models demonstrated superior representational flexibility, especially on large-scale heterogeneous datasets, while convolutional baselines maintained advantages in smaller and cost-constrained environments. Hybrid approaches consistently offered the most balanced deployment profile, combining competitive accuracy with tractable fine-tuning and reduced operational complexity.",
      },
      {
        heading: "Discussion",
        content:
          "The most important practical finding is that architecture choice should be driven by deployment context rather than benchmark leadership alone. In regulated or high-stakes settings, interpretability, calibration, and failure analysis remain as important as raw task performance. Future research should therefore connect architecture innovation more directly to lifecycle validation and monitoring practices.",
      },
    ],
  },
  {
    id: "neural-architecture-search-efficient-models",
    title: "Neural Architecture Search for Efficient Models",
    author: "Dr. Alice Brown",
    authors: [
      {
        name: "Dr. Alice Brown",
        affiliation: "Institute for Applied Intelligence, Department of Vision Systems",
      },
      {
        name: "Dr. Liam Chen",
        affiliation: "Center for Scalable ML Infrastructure",
      },
    ],
    publishedDate: "December 20, 2025",
    summary:
      "This paper presents a novel approach to neural architecture search that significantly reduces computational costs while maintaining high accuracy across various benchmarks.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 8921,
    isVerified: true,
    abstract:
      "We introduce a resource-aware neural architecture search framework that reduces search cost through progressive pruning and performance prediction, enabling practical model discovery for smaller labs. The resulting workflow preserves competitive downstream performance while materially lowering experimentation overhead.",
    keywords: ["NAS", "Efficiency", "Model Search", "Optimization"],
    journal: "Machine Learning Review",
    volume: "Vol. 29",
    issue: "Issue 4",
    pages: "pp. 212-236",
    doi: "10.5103/mlr.2025.21236",
    citationCount: 143,
    readTime: "16 min read",
    sections: [
      {
        heading: "Problem Statement",
        content:
          "Neural architecture search has historically demanded large compute budgets, effectively limiting adoption to well-resourced industrial labs. This paper addresses that imbalance by reframing architecture search as a constrained optimization problem in which wall-clock time and hardware budget are first-class objectives rather than secondary considerations.",
      },
      {
        heading: "Proposed Framework",
        content:
          "The framework combines lightweight performance prediction with progressive candidate pruning. Rather than exhaustively evaluating each architecture, we estimate utility early and eliminate weak branches before they consume meaningful resources. This substantially compresses the search process while preserving a useful frontier of high-quality candidate models.",
      },
      {
        heading: "Empirical Analysis",
        content:
          "Across image and sequence benchmarks, the proposed method reduced search cost by a substantial margin while maintaining competitive final performance. The strongest gains were observed in teams with strict hardware ceilings, suggesting that the framework is especially valuable for academic, non-profit, and domain-specific applied research settings.",
      },
      {
        heading: "Implications",
        content:
          "The broader implication is organizational rather than merely algorithmic: architecture search becomes more democratized when it is designed around realistic compute constraints. This creates room for more diverse model exploration, especially in fields where domain adaptation matters more than leaderboard maximization.",
      },
    ],
  },
  {
    id: "transformer-models-nlp",
    title: "Transformer Models in Natural Language Processing",
    author: "Dr. John Smith",
    authors: [
      {
        name: "Dr. John Smith",
        affiliation: "Center for Language Systems",
      },
      {
        name: "Dr. Sofia Garcia",
        affiliation: "Multilingual Reasoning Lab, Iberia Research Institute",
      },
    ],
    publishedDate: "December 15, 2025",
    summary:
      "A comprehensive analysis of transformer architectures and their applications in modern NLP tasks, including machine translation and text generation.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 15678,
    isVerified: true,
    abstract:
      "This paper reviews transformer model design, scaling trends, and deployment tradeoffs across major natural language processing tasks including translation, summarization, and dialogue generation. We focus particularly on where scaling continues to help and where architectural novelty has become secondary to data quality, retrieval, and alignment strategy.",
    keywords: ["NLP", "Transformers", "Language Models", "Text Generation"],
    journal: "Transactions on NLP Systems",
    volume: "Vol. 11",
    issue: "Issue 6",
    pages: "pp. 501-534",
    doi: "10.9001/tnlps.2025.501534",
    citationCount: 389,
    readTime: "21 min read",
    sections: [
      {
        heading: "Background",
        content:
          "Transformer architectures replaced recurrence with attention-centric sequence modeling and quickly became the dominant paradigm across NLP. Their success derives not only from architectural parallelism, but also from the way self-attention supports reusable representations across diverse downstream tasks.",
      },
      {
        heading: "Applications",
        content:
          "We review machine translation, summarization, retrieval augmentation, dialogue systems, and multilingual adaptation. The evidence suggests that transformer families remain highly flexible, but the strongest practical systems now depend on data curation, retrieval quality, and post-training alignment as much as on architectural scale itself.",
      },
      {
        heading: "Deployment Tradeoffs",
        content:
          "Large language systems impose substantial serving, monitoring, and governance burdens. We therefore examine compression, distillation, and retrieval-based decomposition strategies that preserve task value while reducing cost and operational uncertainty.",
      },
      {
        heading: "Future Work",
        content:
          "The next generation of NLP systems should prioritize reliability and controllability. Progress will likely come from better hybrid retrieval stacks, more interpretable adaptation methods, and evaluation practices that reflect real communication tasks rather than isolated benchmark artifacts.",
      },
    ],
  },
  {
    id: "reinforcement-learning-robotics",
    title: "Reinforcement Learning in Robotics",
    author: "Dr. Sarah Johnson",
    authors: [
      {
        name: "Dr. Sarah Johnson",
        affiliation: "Autonomous Systems Lab",
      },
      {
        name: "Dr. Emily Watson",
        affiliation: "Center for Adaptive Control and Robotics",
      },
    ],
    publishedDate: "December 10, 2025",
    summary:
      "Exploring the application of deep reinforcement learning algorithms in robotic control systems and autonomous navigation.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 6543,
    isVerified: false,
    abstract:
      "We evaluate reinforcement learning methods for robotic control, focusing on sim-to-real transfer and policy stability in navigation and manipulation tasks. The analysis emphasizes operational safety, sample efficiency, and the kinds of engineering support required to make learned control viable outside simulation.",
    keywords: ["Robotics", "Reinforcement Learning", "Control", "Navigation"],
    journal: "Robotics and Learning Quarterly",
    volume: "Vol. 7",
    issue: "Issue 4",
    pages: "pp. 118-146",
    doi: "10.3314/rlq.2025.118146",
    citationCount: 97,
    readTime: "17 min read",
    sections: [
      {
        heading: "Sim-to-Real Gap",
        content:
          "Robotic control policies frequently perform well in simulation yet degrade when exposed to real-world noise, latency, and imperfect sensing. We review domain randomization, adaptation strategies, and reward regularization techniques that help narrow this gap without introducing unsafe exploration behavior.",
      },
      {
        heading: "Control Policies",
        content:
          "Model-free and model-based approaches are evaluated under realistic compute and data constraints. While model-free policies can achieve strong final performance, they remain demanding in sample complexity. Model-based methods offer more structured reasoning but introduce additional system-identification burdens that are not trivial in practice.",
      },
      {
        heading: "Operational Safety",
        content:
          "Safety remains a central concern in embodied learning. We highlight the need for constrained action spaces, fallback controllers, and offline validation before any policy is permitted to act in a partially open environment.",
      },
      {
        heading: "Conclusion",
        content:
          "Reinforcement learning in robotics is most successful when treated as part of a wider systems pipeline rather than a self-contained modeling solution. Reliable performance still depends on simulation quality, hardware-aware constraints, and disciplined evaluation beyond benchmark rewards.",
      },
    ],
  },
  {
    id: "ethical-considerations-ai-development",
    title: "Ethical Considerations in AI Development",
    author: "Dr. Michael Chen",
    authors: [
      {
        name: "Dr. Michael Chen",
        affiliation: "Ethics and Compute Institute",
      },
      {
        name: "Dr. Maya Patel",
        affiliation: "Policy and Systems Governance Program",
      },
    ],
    publishedDate: "December 8, 2025",
    summary:
      "A critical examination of ethical frameworks and responsible AI practices in the development and deployment of artificial intelligence systems.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 9876,
    isVerified: true,
    abstract:
      "This paper synthesizes current responsible-AI frameworks and proposes a practical governance model that teams can adopt during development, evaluation, and deployment. The emphasis is on operationalizing ethics through repeatable review structures, not simply articulating high-level principles.",
    keywords: ["Ethics", "Responsible AI", "Governance", "Safety"],
    journal: "Responsible Systems Review",
    volume: "Vol. 5",
    issue: "Issue 2",
    pages: "pp. 9-31",
    doi: "10.4102/rsr.2025.00931",
    citationCount: 176,
    readTime: "15 min read",
    sections: [
      {
        heading: "Core Principles",
        content:
          "Fairness, transparency, accountability, and human oversight remain foundational, but many organizations struggle to translate these principles into concrete operating procedures. We argue that ethical maturity depends on ownership, escalation paths, and measurable review criteria.",
      },
      {
        heading: "Operational Governance",
        content:
          "We propose lightweight governance rituals that can be embedded into ordinary product and research workflows. These include pre-deployment risk reviews, evidence logging, post-launch monitoring, and designated decision owners who are accountable for documented tradeoffs.",
      },
      {
        heading: "Case Analysis",
        content:
          "Examining deployment scenarios across public-sector and commercial environments, we show that governance failures typically arise from weak process integration rather than a lack of policy vocabulary. Teams often know what the right questions are, but lack structure for acting on the answers.",
      },
      {
        heading: "Implications",
        content:
          "Responsible AI becomes durable when integrated into tooling, review cadence, and launch criteria. This suggests that the future of ethical AI practice is infrastructural: it must be supported by systems design, not left as a purely advisory function.",
      },
    ],
  },
  {
    id: "quantum-computing-machine-learning",
    title: "Quantum Computing and Machine Learning",
    author: "Dr. Emily Watson",
    authors: [
      {
        name: "Dr. Emily Watson",
        affiliation: "Center for Adaptive Control and Robotics",
      },
      {
        name: "Dr. John Smith",
        affiliation: "Center for Language Systems",
      },
    ],
    publishedDate: "December 5, 2025",
    summary:
      "Investigating the intersection of quantum computing and machine learning, exploring quantum algorithms for accelerating ML tasks.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 11234,
    isVerified: true,
    abstract:
      "We explore where quantum techniques may realistically support machine learning workflows and distinguish near-term promise from speculative long-term expectations. The paper focuses on hybrid methods, hardware constraints, and the mismatch between theoretical speedups and deployable systems.",
    keywords: ["Quantum Computing", "Machine Learning", "Algorithms", "Acceleration"],
    journal: "Computational Frontiers in AI",
    volume: "Vol. 13",
    issue: "Issue 12",
    pages: "pp. 740-768",
    doi: "10.7788/cfai.2025.740768",
    citationCount: 122,
    readTime: "19 min read",
    sections: [
      {
        heading: "Scope",
        content:
          "The intersection of quantum computing and machine learning remains promising but uneven. We examine candidate problem classes where quantum advantage may plausibly emerge, while also distinguishing exploratory results from practical evidence that can inform real system design today.",
      },
      {
        heading: "Algorithmic Outlook",
        content:
          "Quantum kernels, variational circuits, and hybrid workflows are reviewed with close attention to hardware fragility and reproducibility limits. We find that hybrid pipelines currently offer the most credible path forward, particularly where classical methods can absorb instability from quantum components.",
      },
      {
        heading: "Experimental Constraints",
        content:
          "Noise, qubit limits, and measurement overhead remain major barriers. As a result, performance claims should be interpreted in the context of tightly scoped workloads rather than assumed to generalize across broader machine learning pipelines.",
      },
      {
        heading: "Practical Takeaway",
        content:
          "Near-term value is likely to come from targeted experimentation in optimization-heavy or scientific-computing contexts rather than from immediate broad disruption of mainstream machine learning practice.",
      },
    ],
  },
]

export const getDummyPaperById = (id: string) =>
  dummyPapers.find((paper) => paper.id === id)

export const getDummyPaperIdByTitle = (title: string) =>
  dummyPapers.find((paper) => paper.title === title)?.id
