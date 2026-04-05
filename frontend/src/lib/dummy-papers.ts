export type DummyPaper = {
  id: string
  title: string
  author: string
  publishedDate: string
  summary: string
  coverImageUrl: string
  impressions?: number
  isVerified?: boolean
  abstract: string
  keywords: string[]
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
    publishedDate: "January 5, 2026",
    summary:
      "An extensive study on the advancements in deep learning techniques applied to computer vision tasks such as image recognition, object detection, and segmentation.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 12543,
    isVerified: true,
    abstract:
      "This paper surveys modern deep learning methods for computer vision and evaluates how convolutional and transformer-based architectures perform across classification, detection, and segmentation tasks in real-world conditions.",
    keywords: ["Computer Vision", "Deep Learning", "Transformers", "Image Recognition"],
    sections: [
      {
        heading: "Introduction",
        content:
          "Computer vision has shifted from hand-crafted feature pipelines to end-to-end learned systems. This paper outlines that transition and explains why modern visual models are now able to generalize across large and noisy datasets.",
      },
      {
        heading: "Methodology",
        content:
          "We compare convolutional baselines with hybrid and transformer-based models using common benchmark tasks. Performance is reviewed not only by accuracy, but also by inference cost, robustness, and sample efficiency.",
      },
      {
        heading: "Results",
        content:
          "Transformer-based architectures showed strong gains in representation learning, while convolutional approaches remained competitive in efficiency-sensitive settings. Hybrid systems often offered the best practical balance.",
      },
    ],
  },
  {
    id: "neural-architecture-search-efficient-models",
    title: "Neural Architecture Search for Efficient Models",
    author: "Dr. Alice Brown",
    publishedDate: "December 20, 2025",
    summary:
      "This paper presents a novel approach to neural architecture search that significantly reduces computational costs while maintaining high accuracy across various benchmarks.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 8921,
    isVerified: true,
    abstract:
      "We introduce a resource-aware neural architecture search framework that reduces search cost through progressive pruning and performance prediction, enabling practical model discovery for smaller labs.",
    keywords: ["NAS", "Efficiency", "Model Search", "Optimization"],
    sections: [
      {
        heading: "Problem Statement",
        content:
          "Many architecture-search techniques require prohibitive compute budgets. This work focuses on reducing that barrier while preserving competitive downstream performance.",
      },
      {
        heading: "Proposed Framework",
        content:
          "Candidate architectures are ranked using a lightweight proxy model. Poor-performing branches are pruned early, which shortens the search cycle and lowers overall infrastructure cost.",
      },
      {
        heading: "Discussion",
        content:
          "The approach is especially useful in academic or applied settings where rapid experimentation matters more than finding a globally optimal architecture at any cost.",
      },
    ],
  },
  {
    id: "transformer-models-nlp",
    title: "Transformer Models in Natural Language Processing",
    author: "Dr. John Smith",
    publishedDate: "December 15, 2025",
    summary:
      "A comprehensive analysis of transformer architectures and their applications in modern NLP tasks, including machine translation and text generation.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 15678,
    isVerified: true,
    abstract:
      "This paper reviews transformer model design, scaling trends, and deployment tradeoffs across major natural language processing tasks including translation, summarization, and dialogue generation.",
    keywords: ["NLP", "Transformers", "Language Models", "Text Generation"],
    sections: [
      {
        heading: "Background",
        content:
          "Transformer architectures replaced recurrent models by making attention the central mechanism for sequence modeling. Their flexibility has since enabled broad transfer learning in NLP.",
      },
      {
        heading: "Applications",
        content:
          "We review machine translation, summarization, retrieval augmentation, and conversation systems, highlighting where transformers excel and where domain adaptation remains challenging.",
      },
      {
        heading: "Future Work",
        content:
          "The next stage of transformer research should emphasize efficiency, interpretability, and safer adaptation in domain-specific environments.",
      },
    ],
  },
  {
    id: "reinforcement-learning-robotics",
    title: "Reinforcement Learning in Robotics",
    author: "Dr. Sarah Johnson",
    publishedDate: "December 10, 2025",
    summary:
      "Exploring the application of deep reinforcement learning algorithms in robotic control systems and autonomous navigation.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 6543,
    isVerified: false,
    abstract:
      "We evaluate reinforcement learning methods for robotic control, focusing on sim-to-real transfer and policy stability in navigation and manipulation tasks.",
    keywords: ["Robotics", "Reinforcement Learning", "Control", "Navigation"],
    sections: [
      {
        heading: "Sim-to-Real Gap",
        content:
          "Robotic systems frequently perform well in simulation but degrade in real deployment. This section examines domain randomization and adaptation methods that narrow that gap.",
      },
      {
        heading: "Control Policies",
        content:
          "We compare model-free and model-based policies under constrained hardware conditions, especially where sample efficiency and safety are major concerns.",
      },
      {
        heading: "Conclusion",
        content:
          "Reliable real-world robotic learning still depends on disciplined environment design, safety constraints, and careful evaluation beyond benchmark scores.",
      },
    ],
  },
  {
    id: "ethical-considerations-ai-development",
    title: "Ethical Considerations in AI Development",
    author: "Dr. Michael Chen",
    publishedDate: "December 8, 2025",
    summary:
      "A critical examination of ethical frameworks and responsible AI practices in the development and deployment of artificial intelligence systems.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 9876,
    isVerified: true,
    abstract:
      "This paper synthesizes current responsible-AI frameworks and proposes a practical governance model that teams can adopt during development, evaluation, and deployment.",
    keywords: ["Ethics", "Responsible AI", "Governance", "Safety"],
    sections: [
      {
        heading: "Core Principles",
        content:
          "Fairness, transparency, accountability, and human oversight remain central principles, but implementation often fails without concrete ownership and measurable checkpoints.",
      },
      {
        heading: "Operational Governance",
        content:
          "We propose lightweight governance rituals that product teams can embed into regular workflows instead of treating ethics review as a one-time compliance exercise.",
      },
      {
        heading: "Implications",
        content:
          "Responsible AI practice becomes more durable when it is integrated into tooling, review cycles, and launch criteria rather than layered on at the end.",
      },
    ],
  },
  {
    id: "quantum-computing-machine-learning",
    title: "Quantum Computing and Machine Learning",
    author: "Dr. Emily Watson",
    publishedDate: "December 5, 2025",
    summary:
      "Investigating the intersection of quantum computing and machine learning, exploring quantum algorithms for accelerating ML tasks.",
    coverImageUrl:
      "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: 11234,
    isVerified: true,
    abstract:
      "We explore where quantum techniques may realistically support machine learning workflows and distinguish near-term promise from speculative long-term expectations.",
    keywords: ["Quantum Computing", "Machine Learning", "Algorithms", "Acceleration"],
    sections: [
      {
        heading: "Scope",
        content:
          "The intersection of quantum computing and ML is promising but uneven. We examine candidate tasks where quantum advantage might plausibly emerge.",
      },
      {
        heading: "Algorithmic Outlook",
        content:
          "Quantum kernels, variational circuits, and hybrid workflows are reviewed with attention to hardware limitations and reproducibility concerns.",
      },
      {
        heading: "Practical Takeaway",
        content:
          "The field remains exploratory, but hybrid experimentation may yield useful insight for specialized optimization and scientific computing workloads.",
      },
    ],
  },
]

export const getDummyPaperById = (id: string) =>
  dummyPapers.find((paper) => paper.id === id)
