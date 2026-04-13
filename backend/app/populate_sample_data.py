"""
Script to populate the database with sample data for testing and development.
Run with: python -m app.populate_sample_data
"""
import logging

from sqlmodel import Session

from app import crud
from app.core.db import engine
from app.crud.collaborator import add_researcher_collaborator
from app.crud.institution import create_institution, upsert_institution_membership
from app.crud.publication import create_publication
from app.crud.publication_analytics import track_publication_event
from app.crud.publication_member import add_publication_member
from app.crud.researcher import create_researcher
from app.models import UserCreate
from app.models.institution import InstitutionRole
from app.models.publication import PublicationRole
from app.models.publication_analytics import PublicationEngagementType
from app.schemas.institution import InstitutionCreate
from app.schemas.publications import CreatePublication, PublicationAnalyticsEventCreate
from app.schemas.researcher import CreateResearcherInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_sample_users(session: Session) -> dict:
    """Create sample user accounts"""
    logger.info("Creating sample user accounts...")

    users = {}

    # Regular users
    sample_users = [
        {"email": "john.doe@example.com", "password": "password123", "is_superuser": False, "full_name": "John Doe"},
        {"email": "jane.smith@example.com", "password": "password123", "is_superuser": False, "full_name": "Jane Smith"},
        {"email": "bob.johnson@example.com", "password": "password123", "is_superuser": False, "full_name": "Bob Johnson"},
        {"email": "alice.williams@example.com", "password": "password123", "is_superuser": False, "full_name": "Alice Williams"},
        {"email": "charlie.brown@example.com", "password": "password123", "is_superuser": False, "full_name": "Charlie Brown"},
    ]

    for user_data in sample_users:
        existing_user = crud.get_user_by_email(session=session, email=user_data["email"])
        if not existing_user:
            user_in = UserCreate(
                email=user_data["email"],
                password=user_data["password"],
                is_superuser=user_data["is_superuser"],
                full_name=user_data.get("full_name")
            )
            user = crud.create_user(session=session, user_create=user_in)
            users[user_data["email"]] = user
            logger.info(f"Created user: {user_data['email']}")
        else:
            users[user_data["email"]] = existing_user
            logger.info(f"User already exists: {user_data['email']}")

    return users


def create_sample_institutions(session: Session) -> list:
    """Create sample institutions"""
    logger.info("Creating sample institutions...")

    institutions_data = [
        {
            "name": "Massachusetts Institute of Technology",
            "domain": "mit.edu",
            "institution_type": "university",
            "description": "Leading research university focused on technology, engineering, and AI.",
            "is_verified": True,
            "onboarding_enabled": True,
        },
        {
            "name": "Stanford University",
            "domain": "stanford.edu",
            "institution_type": "university",
            "description": "Top-tier university known for computer science and innovation.",
            "is_verified": True,
            "onboarding_enabled": True,
        },
        {
            "name": "Carnegie Mellon University",
            "domain": "cmu.edu",
            "institution_type": "university",
            "description": "Research university specializing in robotics, AI, and human-centered computing.",
            "is_verified": True,
            "onboarding_enabled": True,
        },
        {
            "name": "Oxford University",
            "domain": "ox.ac.uk",
            "institution_type": "university",
            "description": "Historic university with strong research programs across science and engineering.",
            "is_verified": True,
            "onboarding_enabled": True,
        },
        {
            "name": "Imperial College London",
            "domain": "imperial.ac.uk",
            "institution_type": "university",
            "description": "Leading institution for science, engineering, medicine, and business.",
            "is_verified": True,
            "onboarding_enabled": True,
        },
    ]

    institutions = []
    for institution_data in institutions_data:
        institution_in = InstitutionCreate(**institution_data)
        institution = create_institution(session=session, institution_in=institution_in)
        institutions.append(institution)
        logger.info(f"Created institution: {institution.name}")

    return institutions


def create_institution_memberships(session: Session, institutions: list, users: dict):
    """Add sample users to institutions"""
    logger.info("Creating sample institution memberships...")

    user_list = list(users.values())
    sample_memberships = [
        (0, "john.doe@example.com", InstitutionRole.STUDENT, "Computer Science", "Undergraduate", True, True),
        (1, "jane.smith@example.com", InstitutionRole.RESEARCHER, "Data Science", "Postdoctoral Researcher", True, True),
        (2, "bob.johnson@example.com", InstitutionRole.FACULTY, "Robotics", "Assistant Professor", True, True),
        (3, "alice.williams@example.com", InstitutionRole.RESEARCHER, "Quantum Computing", "Research Scientist", True, True),
        (4, "charlie.brown@example.com", InstitutionRole.STUDENT, "Bioinformatics", "Graduate Student", True, True),
        # Partner institution memberships (secondary affiliations)
        (1, "john.doe@example.com", InstitutionRole.RESEARCHER, "Applied AI", "Visiting Researcher", False, True),
        (2, "jane.smith@example.com", InstitutionRole.RESEARCHER, "Human-Computer Interaction", "Visiting Scholar", False, True),
        (3, "bob.johnson@example.com", InstitutionRole.RESEARCHER, "Robotics", "Visiting Researcher", False, True),
        (0, "alice.williams@example.com", InstitutionRole.RESEARCHER, "Computer Vision", "Visiting Researcher", False, True),
    ]

    created_by_id = user_list[0].id if user_list else None
    for institution_idx, email, role, department, title, is_primary, is_verified in sample_memberships:
        if institution_idx >= len(institutions):
            continue
        user = users.get(email)
        if not user:
            logger.warning(f"Skipping membership for missing user: {email}")
            continue
        try:
            upsert_institution_membership(
                session=session,
                institution_id=institutions[institution_idx].id,
                user_id=user.id,
                role=role,
                department=department,
                title=title,
                is_primary=is_primary,
                is_verified=is_verified,
                created_by_id=created_by_id,
            )
            logger.info(f"Created membership for {email} at {institutions[institution_idx].name}")
        except Exception as e:
            logger.warning(f"Could not create institution membership for {email}: {e}")


def populate_sample_institution_data(session: Session) -> None:
    """Create sample institutions and memberships for development environments."""
    users = create_sample_users(session)
    session.commit()

    institutions = create_sample_institutions(session)
    session.commit()

    create_institution_memberships(session, institutions, users)
    session.commit()


def create_sample_researchers(session: Session, users: dict) -> list:
    """Create sample researchers"""
    logger.info("Creating sample researchers...")

    researchers_data = [
        {
            "full_name": "Dr. Sarah Mitchell",
            "email": "sarah.mitchell@mit.edu",
            "qualification": "Ph.D. in Computer Science",
            "institute": "Massachusetts Institute of Technology",
            "bio": "Expert in machine learning and artificial intelligence with 15 years of research experience."
        },
        {
            "full_name": "Prof. James Anderson",
            "email": "j.anderson@stanford.edu",
            "qualification": "Ph.D. in Data Science",
            "institute": "Stanford University",
            "bio": "Specializes in deep learning and neural networks. Published over 50 papers in top-tier conferences."
        },
        {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "qualification": "M.S. in Data Science",
            "institute": "Massachusetts Institute of Technology",
            "department": "Computer Science",
            "bio": "Sample researcher profile for seeded user John Doe."
        },
        {
            "full_name": "Jane Smith",
            "email": "jane.smith@example.com",
            "qualification": "M.S. in Computational Biology",
            "institute": "Stanford University",
            "department": "Data Science",
            "bio": "Sample researcher profile for seeded user Jane Smith."
        },
        {
            "full_name": "Dr. Maria Garcia",
            "email": "maria.garcia@berkeley.edu",
            "qualification": "Ph.D. in Artificial Intelligence",
            "institute": "University of California, Berkeley",
            "bio": "Research focuses on natural language processing and computer vision."
        },
        {
            "full_name": "Dr. David Chen",
            "email": "david.chen@caltech.edu",
            "qualification": "Ph.D. in Machine Learning",
            "institute": "California Institute of Technology",
            "bio": "Working on reinforcement learning and robotics applications."
        },
        {
            "full_name": "Prof. Emily Rodriguez",
            "email": "e.rodriguez@cmu.edu",
            "qualification": "Ph.D. in Computer Vision",
            "institute": "Carnegie Mellon University",
            "bio": "Pioneer in autonomous systems and computer vision research."
        },
        {
            "full_name": "Dr. Michael Thompson",
            "email": "m.thompson@oxford.ac.uk",
            "qualification": "Ph.D. in Quantum Computing",
            "institute": "University of Oxford",
            "bio": "Leading research in quantum algorithms and quantum machine learning."
        },
        {
            "full_name": "Dr. Lisa Wang",
            "email": "lisa.wang@harvard.edu",
            "qualification": "Ph.D. in Bioinformatics",
            "institute": "Harvard University",
            "bio": "Applying machine learning to biological data analysis and drug discovery."
        },
        {
            "full_name": "Prof. Robert Kumar",
            "email": "r.kumar@imperial.ac.uk",
            "qualification": "Ph.D. in Data Mining",
            "institute": "Imperial College London",
            "bio": "Expert in big data analytics and distributed computing systems."
        }
    ]

    researchers = []
    for data in researchers_data:
        researcher_in = CreateResearcherInfo(**data)
        researcher = create_researcher(session=session, researcher_in=researcher_in)
        user = users.get(data["email"])
        if user:
            researcher.user_id = user.id
            researcher.affiliation_verified = True
            session.add(researcher)
            session.commit()
            session.refresh(researcher)
            logger.info(f"Linked researcher profile {data['email']} to user account")

        researchers.append(researcher)
        logger.info(f"Created researcher: {data['full_name']}")

    return researchers


def create_sample_publications(session: Session, researchers: list) -> list:
    """Create sample publications for researchers"""
    logger.info("Creating sample publications...")

    publications_data = [
        # Dr. Sarah Mitchell's publications
        {
            "researcher_idx": 0,
            "pubs": [
                {
                    "title": "Deep Learning Architectures for Medical Image Analysis",
                    "publisher": "Nature Machine Intelligence",
                    "year": 2023,
                    "description": "A comprehensive study on applying deep learning to medical imaging",
                    "domains": ["Machine Learning", "Healthcare", "Computer Vision"]
                },
                {
                    "title": "Transfer Learning in Neural Networks: A Survey",
                    "publisher": "IEEE Transactions on Neural Networks",
                    "year": 2022,
                    "description": "Survey of transfer learning techniques in modern neural networks",
                    "domains": ["Machine Learning", "Deep Learning"]
                },
                {
                    "title": "Ethical AI: Challenges and Solutions",
                    "publisher": "Journal of AI Ethics",
                    "year": 2024,
                    "description": "Discussion on ethical considerations in AI development",
                    "domains": ["AI Ethics", "Machine Learning"]
                }
            ]
        },
        # Prof. James Anderson's publications
        {
            "researcher_idx": 1,
            "pubs": [
                {
                    "title": "Attention Mechanisms in Transformer Networks",
                    "publisher": "NeurIPS 2023",
                    "year": 2023,
                    "description": "Novel attention mechanisms for improved transformer performance",
                    "domains": ["Deep Learning", "NLP", "Transformers"]
                },
                {
                    "title": "Scaling Laws for Large Language Models",
                    "publisher": "ICML 2022",
                    "year": 2022,
                    "description": "Empirical study on scaling behavior of language models",
                    "domains": ["NLP", "Deep Learning", "Language Models"]
                }
            ]
        },
        # Dr. Maria Garcia's publications
        {
            "researcher_idx": 2,
            "pubs": [
                {
                    "title": "Multimodal Learning for Image and Text Understanding",
                    "publisher": "CVPR 2024",
                    "year": 2024,
                    "description": "Unified framework for joint image and text processing",
                    "domains": ["Computer Vision", "NLP", "Multimodal Learning"]
                },
                {
                    "title": "Few-Shot Learning in Computer Vision",
                    "publisher": "ICCV 2023",
                    "year": 2023,
                    "description": "Novel approaches to learning from limited labeled data",
                    "domains": ["Computer Vision", "Few-Shot Learning"]
                },
                {
                    "title": "Object Detection in Autonomous Vehicles",
                    "publisher": "IEEE Robotics and Automation",
                    "year": 2022,
                    "description": "Real-time object detection for self-driving cars",
                    "domains": ["Computer Vision", "Autonomous Systems", "Robotics"]
                }
            ]
        },
        # Dr. David Chen's publications
        {
            "researcher_idx": 3,
            "pubs": [
                {
                    "title": "Deep Reinforcement Learning for Robotic Manipulation",
                    "publisher": "Science Robotics",
                    "year": 2024,
                    "description": "RL algorithms for complex robotic tasks",
                    "domains": ["Reinforcement Learning", "Robotics"]
                },
                {
                    "title": "Multi-Agent Systems in Game Theory",
                    "publisher": "AAAI 2023",
                    "year": 2023,
                    "description": "Game-theoretic approaches to multi-agent learning",
                    "domains": ["Reinforcement Learning", "Multi-Agent Systems", "Game Theory"]
                }
            ]
        },
        # Prof. Emily Rodriguez's publications
        {
            "researcher_idx": 4,
            "pubs": [
                {
                    "title": "3D Scene Understanding with Point Clouds",
                    "publisher": "ECCV 2024",
                    "year": 2024,
                    "description": "Advanced methods for processing 3D point cloud data",
                    "domains": ["Computer Vision", "3D Vision", "Point Clouds"]
                },
                {
                    "title": "Visual SLAM for Autonomous Navigation",
                    "publisher": "Robotics: Science and Systems",
                    "year": 2023,
                    "description": "Simultaneous localization and mapping using visual sensors",
                    "domains": ["Computer Vision", "Robotics", "SLAM"]
                }
            ]
        },
        # Dr. Michael Thompson's publications
        {
            "researcher_idx": 5,
            "pubs": [
                {
                    "title": "Quantum Algorithms for Machine Learning",
                    "publisher": "Physical Review X",
                    "year": 2024,
                    "description": "Quantum computing approaches to ML problems",
                    "domains": ["Quantum Computing", "Machine Learning"]
                },
                {
                    "title": "Variational Quantum Eigensolver Applications",
                    "publisher": "Nature Quantum Information",
                    "year": 2023,
                    "description": "Practical applications of VQE in chemistry and materials science",
                    "domains": ["Quantum Computing", "Quantum Algorithms"]
                }
            ]
        },
        # Dr. Lisa Wang's publications
        {
            "researcher_idx": 6,
            "pubs": [
                {
                    "title": "Deep Learning for Protein Structure Prediction",
                    "publisher": "Nature Methods",
                    "year": 2024,
                    "description": "AlphaFold-inspired approaches to protein folding",
                    "domains": ["Bioinformatics", "Deep Learning", "Protein Structure"]
                },
                {
                    "title": "Drug Discovery with Graph Neural Networks",
                    "publisher": "Journal of Chemical Information",
                    "year": 2023,
                    "description": "GNN-based methods for molecular property prediction",
                    "domains": ["Bioinformatics", "Drug Discovery", "Graph Neural Networks"]
                }
            ]
        },
        # Prof. Robert Kumar's publications
        {
            "researcher_idx": 7,
            "pubs": [
                {
                    "title": "Distributed Machine Learning at Scale",
                    "publisher": "ACM SIGMOD 2024",
                    "year": 2024,
                    "description": "Efficient algorithms for distributed ML training",
                    "domains": ["Distributed Systems", "Machine Learning", "Big Data"]
                },
                {
                    "title": "Real-Time Stream Processing with Apache Flink",
                    "publisher": "IEEE Big Data",
                    "year": 2023,
                    "description": "Stream processing frameworks for big data analytics",
                    "domains": ["Big Data", "Stream Processing", "Distributed Systems"]
                }
            ]
        }
    ]

    all_publications = []
    for pub_group in publications_data:
        researcher = researchers[pub_group["researcher_idx"]]
        for pub_data in pub_group["pubs"]:
            pub_in = CreatePublication(**pub_data)
            publication = create_publication(
                session=session,
                publication_in=pub_in,
                researcher_id=researcher.id
            )
            all_publications.append(publication)
            logger.info(f"Created publication: {pub_data['title']}")

    return all_publications


def create_sample_publication_analytics(session: Session, publications: list, users: dict):
    """Add publication engagement events for analytics"""
    logger.info("Creating sample publication analytics events...")

    analytics_data = [
        {
            "pub_idx": 0,
            "events": [
                (PublicationEngagementType.VIEW, 120),
                (PublicationEngagementType.DOWNLOAD, 35),
                (PublicationEngagementType.CITATION, 7),
            ],
        },
        {
            "pub_idx": 2,
            "events": [
                (PublicationEngagementType.VIEW, 90),
                (PublicationEngagementType.SAVE, 12),
                (PublicationEngagementType.SHARE, 5),
            ],
        },
        {
            "pub_idx": 4,
            "events": [
                (PublicationEngagementType.VIEW, 150),
                (PublicationEngagementType.DOWNLOAD, 55),
                (PublicationEngagementType.CITATION, 10),
            ],
        },
        {
            "pub_idx": 6,
            "events": [
                (PublicationEngagementType.VIEW, 68),
                (PublicationEngagementType.SAVE, 8),
            ],
        },
    ]

    user_list = list(users.values())
    for analytics in analytics_data:
        pub_idx = analytics["pub_idx"]
        if pub_idx >= len(publications):
            continue
        publication = publications[pub_idx]
        for event_index, (event_type, value) in enumerate(analytics["events"]):
            actor_user = user_list[event_index % len(user_list)] if user_list else None
            try:
                track_publication_event(
                    session=session,
                    publication=publication,
                    event_in=PublicationAnalyticsEventCreate(
                        event_type=event_type,
                        value=value,
                    ),
                    actor_user_id=actor_user.id if actor_user else None,
                )
                logger.info(
                    f"Tracked analytics event for publication {publication.title}: {event_type} x {value}"
                )
            except Exception as e:
                logger.warning(f"Could not track analytics event for publication {publication.title}: {e}")


def create_collaborations(session: Session, researchers: list, users: dict):
    """Create collaborations between researchers"""
    logger.info("Creating researcher collaborations...")

    # Get first user for tracking who added collaborations
    first_user = list(users.values())[0]

    # Define collaboration pairs
    collaborations = [
        (0, 1),  # Sarah & James - both work on ML
        (0, 2),  # Sarah & Maria - both work on vision
        (1, 2),  # James & Maria - NLP and vision overlap
        (2, 4),  # Maria & Emily - both work on computer vision
        (3, 4),  # David & Emily - both work on robotics
        (5, 6),  # Michael & Lisa - quantum computing and bio
        (6, 7),  # Lisa & Robert - data science overlap
        (0, 6),  # Sarah & Lisa - ML applications in bio
    ]

    for idx1, idx2 in collaborations:
        try:
            add_researcher_collaborator(
                session=session,
                researcher_id=researchers[idx1].id,
                collaborator_id=researchers[idx2].id,
                added_by=first_user.id
            )
            logger.info(f"Added collaboration: {researchers[idx1].full_name} <-> {researchers[idx2].full_name}")
        except Exception as e:
            logger.warning(f"Could not add collaboration: {e}")


def add_publication_members(session: Session, publications: list, users: dict):
    """Add users as members to publications"""
    logger.info("Adding users to publications...")

    user_list = list(users.values())

    # Add different users to different publications with various roles
    memberships = [
        (0, 0, PublicationRole.editor),   # John as editor on first pub
        (0, 1, PublicationRole.viewer),   # Jane as viewer on first pub
        (1, 0, PublicationRole.owner),    # John as owner on second pub
        (2, 2, PublicationRole.editor),   # Bob as editor on third pub
        (3, 1, PublicationRole.viewer),   # Alice as viewer on second pub
        (4, 3, PublicationRole.editor),   # Charlie as editor on fourth pub
        (5, 0, PublicationRole.viewer),   # Add more variety
    ]

    for pub_idx, user_idx, role in memberships:
        if pub_idx < len(publications) and user_idx < len(user_list):
            try:
                add_publication_member(
                    session=session,
                    publication_id=publications[pub_idx].id,
                    user_id=user_list[user_idx].id,
                    role=role,
                    added_by=user_list[0].id  # First user adds everyone
                )
                logger.info(f"Added {user_list[user_idx].email} as {role} to publication {pub_idx}")
            except Exception as e:
                logger.warning(f"Could not add publication member: {e}")


def populate_database():
    """Main function to populate the database with sample data"""
    logger.info("Starting database population...")

    with Session(engine) as session:
        # Create users
        users = create_sample_users(session)
        session.commit()

        # Create researchers and attach seeded researchers to matching user accounts
        researchers = create_sample_researchers(session, users)
        session.commit()

        # Create institutions and memberships
        institutions = create_sample_institutions(session)
        session.commit()
        create_institution_memberships(session, institutions, users)
        session.commit()

        # Create publications
        publications = create_sample_publications(session, researchers)
        session.commit()

        # Create publication analytics events
        create_sample_publication_analytics(session, publications, users)
        session.commit()

        # Create collaborations
        create_collaborations(session, researchers, users)
        session.commit()

        # Add publication members
        add_publication_members(session, publications, users)
        session.commit()

    logger.info("Database population completed successfully!")
    logger.info(f"Created {len(users)} users")
    logger.info(f"Created {len(researchers)} researchers")
    logger.info(f"Created {len(publications)} publications")


def main():
    """Entry point for the script"""
    try:
        populate_database()
    except Exception as e:
        logger.error(f"Error populating database: {e}")
        raise


if __name__ == "__main__":
    main()
