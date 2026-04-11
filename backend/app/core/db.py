from datetime import datetime, timedelta, timezone

from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models.chat import Chat, ChatType
from app.models.message import Message
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.publication import Publication
from app.models.researcher import ResearcherInfo
from app.models.users import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

DEMO_PASSWORD = "DemoPass123!"

DEMO_USERS = [
    {
        "email": "maya.patel@studylink.demo",
        "full_name": "Dr. Maya Patel",
        "is_superuser": False,
    },
    {
        "email": "liam.chen@studylink.demo",
        "full_name": "Dr. Liam Chen",
        "is_superuser": False,
    },
    {
        "email": "sofia.garcia@studylink.demo",
        "full_name": "Dr. Sofia Garcia",
        "is_superuser": False,
    },
]

DEMO_RESEARCHERS = [
    {
        "email": "alice.brown@research.demo",
        "full_name": "Dr. Alice Brown",
        "qualification": "Professor of Computer Vision",
        "institute": "Institute for Applied Intelligence",
        "bio": "Alice studies practical vision systems for healthcare imaging, model efficiency, and trustworthy deployment.",
    },
    {
        "email": "john.smith@research.demo",
        "full_name": "Dr. John Smith",
        "qualification": "NLP Research Lead",
        "institute": "Center for Language Systems",
        "bio": "John works on foundation models, multilingual transfer, and research tooling for academic teams.",
    },
    {
        "email": "sarah.johnson@research.demo",
        "full_name": "Dr. Sarah Johnson",
        "qualification": "Robotics Scientist",
        "institute": "Autonomous Systems Lab",
        "bio": "Sarah focuses on reinforcement learning for robotics, safe control, and sim-to-real evaluation.",
    },
    {
        "email": "michael.chen@research.demo",
        "full_name": "Dr. Michael Chen",
        "qualification": "Responsible AI Fellow",
        "institute": "Ethics and Compute Institute",
        "bio": "Michael explores governance patterns for AI teams and measurable ways to operationalize responsible AI.",
    },
]

DEMO_PUBLICATIONS = [
    {
        "researcher_email": "alice.brown@research.demo",
        "title": "Deep Learning for Computer Vision",
        "publisher": "Journal of Vision Systems",
        "year": 2026,
        "description": "A survey of modern deep learning approaches for image understanding, detection, and segmentation in real-world deployments.",
        "domains": ["Computer Vision", "Deep Learning", "Healthcare AI"],
    },
    {
        "researcher_email": "alice.brown@research.demo",
        "title": "Neural Architecture Search for Efficient Models",
        "publisher": "Machine Learning Review",
        "year": 2025,
        "description": "A resource-aware neural architecture search workflow designed for smaller research teams with limited compute.",
        "domains": ["Model Optimization", "Deep Learning", "Efficiency"],
    },
    {
        "researcher_email": "john.smith@research.demo",
        "title": "Transformer Models in Natural Language Processing",
        "publisher": "Transactions on NLP Systems",
        "year": 2025,
        "description": "A broad review of transformer architectures and how they shape translation, summarization, retrieval, and generation tasks.",
        "domains": ["NLP", "Transformers", "Language Models"],
    },
    {
        "researcher_email": "sarah.johnson@research.demo",
        "title": "Reinforcement Learning in Robotics",
        "publisher": "Robotics and Learning Quarterly",
        "year": 2025,
        "description": "An applied view of reinforcement learning in navigation and manipulation, with emphasis on real deployment constraints.",
        "domains": ["Robotics", "Reinforcement Learning", "Control Systems"],
    },
    {
        "researcher_email": "michael.chen@research.demo",
        "title": "Ethical Considerations in AI Development",
        "publisher": "Responsible Systems Review",
        "year": 2025,
        "description": "A practical governance framework for responsible AI review within product and research organizations.",
        "domains": ["Responsible AI", "Governance", "AI Ethics"],
    },
]

DEMO_PROJECTS = [
    {
        "title": "Studylink Demo Command Center",
        "description": "A shared workspace for rehearsing the product walkthrough, collecting talking points, and tracking demo-ready stories.",
        "domain": "studylink-demo-command-center",
        "owner_email": settings.FIRST_SUPERUSER,
        "is_public": True,
        "members": [
            ("maya.patel@studylink.demo", "editor"),
            ("liam.chen@studylink.demo", "editor"),
        ],
    },
    {
        "title": "Clinical Vision Bench",
        "description": "Benchmarking imaging models for diagnosis support with an emphasis on speed, calibration, and clinician review flows.",
        "domain": "clinical-vision-bench",
        "owner_email": "maya.patel@studylink.demo",
        "is_public": True,
        "members": [
            ("liam.chen@studylink.demo", "editor"),
            ("sofia.garcia@studylink.demo", "viewer"),
        ],
    },
    {
        "title": "Policy Aligned AI Toolkit",
        "description": "Building reusable templates for AI review checklists, launch criteria, and evidence capture across research teams.",
        "domain": "policy-aligned-ai-toolkit",
        "owner_email": "liam.chen@studylink.demo",
        "is_public": False,
        "members": [
            ("maya.patel@studylink.demo", "editor"),
            ("sofia.garcia@studylink.demo", "editor"),
        ],
    },
]

DEMO_CHATS = [
    {
        "title": "Admin Demo Prep",
        "participants": [
            settings.FIRST_SUPERUSER,
            "maya.patel@studylink.demo",
            "liam.chen@studylink.demo",
        ],
        "messages": [
            (
                "maya.patel@studylink.demo",
                "I seeded realistic researcher and publication data so Search has something to explore.",
            ),
            (
                "liam.chen@studylink.demo",
                "Projects are live too. The public one is perfect for the walkthrough.",
            ),
            (
                settings.FIRST_SUPERUSER,
                "Great. I’ll use this chat thread as the collaboration demo after projects.",
            ),
        ],
    },
    {
        "title": None,
        "participants": [
            "maya.patel@studylink.demo",
            "liam.chen@studylink.demo",
        ],
        "messages": [
            (
                "maya.patel@studylink.demo",
                "Hey Liam, can you sanity-check the project narrative before the demo?",
            ),
            (
                "liam.chen@studylink.demo",
                "Yep, I tightened the wording around outcomes and added a more believable milestone timeline.",
            ),
            (
                "maya.patel@studylink.demo",
                "Perfect. I’ll use that thread when I walk through Projects and Messages.",
            ),
        ],
    },
    {
        "title": "Demo Launch Team",
        "participants": [
            "maya.patel@studylink.demo",
            "liam.chen@studylink.demo",
            "sofia.garcia@studylink.demo",
        ],
        "messages": [
            (
                "sofia.garcia@studylink.demo",
                "I seeded researcher profiles and publications so Search feels populated now.",
            ),
            (
                "liam.chen@studylink.demo",
                "Nice. I’m going to demo private vs public projects right after that.",
            ),
            (
                "maya.patel@studylink.demo",
                "Great, and I’ll end with this group chat to show collaboration activity.",
            ),
        ],
    },
]


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_user(
    session: Session,
    *,
    email: str,
    password: str,
    full_name: str | None,
    is_superuser: bool,
) -> User:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        user = crud.create_user(
            session=session,
            user_create=UserCreate(
                email=email,
                password=password,
                full_name=full_name,
                is_superuser=is_superuser,
            ),
        )
        return user

    needs_commit = False
    if user.full_name != full_name:
        user.full_name = full_name
        needs_commit = True
    if user.is_superuser != is_superuser:
        user.is_superuser = is_superuser
        needs_commit = True
    if not verify_password(password, user.hashed_password):
        user.hashed_password = get_password_hash(password)
        needs_commit = True
    if not user.is_active:
        user.is_active = True
        needs_commit = True

    if needs_commit:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def _ensure_researcher(session: Session, researcher_data: dict[str, str]) -> ResearcherInfo:
    researcher = session.exec(
        select(ResearcherInfo).where(ResearcherInfo.email == researcher_data["email"])
    ).first()
    if not researcher:
        researcher = ResearcherInfo(**researcher_data)
        session.add(researcher)
        session.commit()
        session.refresh(researcher)
        return researcher

    needs_commit = False
    for field in ("full_name", "qualification", "institute", "bio"):
        value = researcher_data[field]
        if getattr(researcher, field) != value:
            setattr(researcher, field, value)
            needs_commit = True
    if needs_commit:
        session.add(researcher)
        session.commit()
        session.refresh(researcher)
    return researcher


def _ensure_publication(
    session: Session,
    *,
    publication_data: dict[str, object],
    researcher_id: object,
) -> Publication:
    publication = session.exec(
        select(Publication).where(Publication.title == publication_data["title"])
    ).first()
    if not publication:
        publication = Publication(
            researcher_id=researcher_id,
            title=str(publication_data["title"]),
            publisher=str(publication_data["publisher"]),
            year=publication_data["year"],
            description=publication_data["description"],
            domains=publication_data["domains"],
        )
        session.add(publication)
        session.commit()
        session.refresh(publication)
        return publication

    publication.researcher_id = researcher_id
    publication.publisher = str(publication_data["publisher"])
    publication.year = publication_data["year"]
    publication.description = publication_data["description"]
    publication.domains = publication_data["domains"]
    session.add(publication)
    session.commit()
    session.refresh(publication)
    return publication


def _ensure_project(
    session: Session,
    *,
    project_data: dict[str, object],
    owner_id: object,
) -> Project:
    project = session.exec(
        select(Project).where(Project.domain == project_data["domain"])
    ).first()
    if not project:
        project = Project(
            title=str(project_data["title"]),
            description=project_data["description"],
            domain=str(project_data["domain"]),
            owner_id=owner_id,
            is_public=bool(project_data["is_public"]),
            is_deleted=False,
        )
        session.add(project)
        session.commit()
        session.refresh(project)
        return project

    project.title = str(project_data["title"])
    project.description = project_data["description"]
    project.owner_id = owner_id
    project.is_public = bool(project_data["is_public"])
    project.is_deleted = False
    project.deleted_at = None
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def _ensure_project_member(
    session: Session, *, project_id: object, user_id: object, role: str
) -> None:
    member = session.exec(
        select(ProjectMember)
        .where(ProjectMember.project_id == project_id)
        .where(ProjectMember.user_id == user_id)
    ).first()
    if not member:
        session.add(ProjectMember(project_id=project_id, user_id=user_id, role=role))
        session.commit()
        return

    if member.role != role:
        member.role = role
        session.add(member)
        session.commit()


def _ensure_chat(
    session: Session,
    *,
    title: str | None,
    participant_ids: list[str],
    owner_id: object,
) -> Chat:
    chats = session.exec(select(Chat).where(Chat.is_deleted == False)).all()  # noqa: E712
    participant_set = set(participant_ids)
    chat = next(
        (
            existing_chat
            for existing_chat in chats
            if set(existing_chat.participants) == participant_set
            and existing_chat.title == title
        ),
        None,
    )
    if chat:
        return chat

    created_at = _now() - timedelta(hours=6)
    member_states = {
        participant_id: [{"start": created_at.isoformat(), "end": None}]
        for participant_id in participant_ids
    }
    chat = Chat(
        user_id=owner_id,
        chat_type=ChatType.dm if len(participant_ids) == 2 else ChatType.group,
        title=title,
        participants=participant_ids,
        member_states=member_states,
        reported_by=[],
        created_at=created_at,
        updated_at=created_at,
        is_deleted=False,
    )
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat


def _ensure_chat_messages(
    session: Session,
    *,
    chat: Chat,
    email_to_user: dict[str, User],
    messages: list[tuple[str, str]],
) -> None:
    existing_messages = session.exec(
        select(Message).where(Message.chat_id == chat.id).where(Message.is_deleted == False)  # noqa: E712
    ).all()
    if existing_messages:
        return

    started_at = chat.created_at or _now()
    for index, (sender_email, content) in enumerate(messages):
        created_at = started_at + timedelta(minutes=(index + 1) * 7)
        session.add(
            Message(
                chat_id=chat.id,
                sender_id=email_to_user[sender_email].id,
                content=content,
                attachments=[],
                created_at=created_at,
                updated_at=created_at,
                is_deleted=False,
            )
        )
        chat.last_message = content
        chat.updated_at = created_at

    session.add(chat)
    session.commit()


def init_db(session: Session) -> None:
    admin_user = _ensure_user(
        session,
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        full_name="Studylink Admin",
        is_superuser=True,
    )

    demo_users = {
        settings.FIRST_SUPERUSER: admin_user,
    }
    for user_data in DEMO_USERS:
        demo_user = _ensure_user(
            session,
            email=user_data["email"],
            password=DEMO_PASSWORD,
            full_name=user_data["full_name"],
            is_superuser=bool(user_data["is_superuser"]),
        )
        demo_users[demo_user.email] = demo_user

    researchers_by_email = {}
    for researcher_data in DEMO_RESEARCHERS:
        researcher = _ensure_researcher(session, researcher_data=researcher_data)
        researchers_by_email[researcher.email] = researcher

    for publication_data in DEMO_PUBLICATIONS:
        researcher = researchers_by_email[str(publication_data["researcher_email"])]
        _ensure_publication(
            session,
            publication_data=publication_data,
            researcher_id=researcher.id,
        )

    for project_data in DEMO_PROJECTS:
        owner = demo_users[str(project_data["owner_email"])]
        project = _ensure_project(
            session,
            project_data=project_data,
            owner_id=owner.id,
        )
        for member_email, role in project_data["members"]:
            _ensure_project_member(
                session,
                project_id=project.id,
                user_id=demo_users[member_email].id,
                role=role,
            )

    for chat_data in DEMO_CHATS:
        participant_ids = [
            str(demo_users[email].id) for email in chat_data["participants"]
        ]
        owner = demo_users[chat_data["participants"][0]]
        chat = _ensure_chat(
            session,
            title=chat_data["title"],
            participant_ids=participant_ids,
            owner_id=owner.id,
        )
        _ensure_chat_messages(
            session,
            chat=chat,
            email_to_user=demo_users,
            messages=chat_data["messages"],
        )
