import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.models import User
from app.models.chat import Chat
from tests.utils.user import authentication_token_from_email, create_random_user


def create_chat(
    client: TestClient,
    token_headers: dict[str, str],
    participant_id: str | None = None,
    title: str = "Chat title",
    participants: list[str] | None = None,
) -> dict:
    if participants is None:
        if participant_id is None:
            raise ValueError("participant_id or participants must be provided")
        participants = [participant_id]
    payload = {
        "title": title,
        "participants": participants,
    }
    response = client.post(
        f"{settings.API_V1_STR}/chats/",
        headers=token_headers,
        json=payload,
    )
    assert response.status_code == 201
    return response.json()


def test_create_chat(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    normal_user = db.exec(
        select(User).where(User.email == settings.EMAIL_TEST_USER)
    ).first()
    assert normal_user is not None
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None

    payload = {
        "title": None,
        "participants": [str(super_user.id)],
    }
    response = client.post(
        f"{settings.API_V1_STR}/chats/",
        headers=normal_user_token_headers,
        json=payload,
    )

    assert response.status_code == 201
    content = response.json()
    assert content["title"] is None
    assert content["chat_type"] == "dm"
    assert content["user_id"] == str(normal_user.id)
    assert str(normal_user.id) in content["participants"]
    assert str(super_user.id) in content["participants"]
    assert content["last_message"] is None
    assert content["created_at"] is not None


def test_create_chat_deduplicates_participants_and_sets_dm_type(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    normal_user = db.exec(
        select(User).where(User.email == settings.EMAIL_TEST_USER)
    ).first()
    assert normal_user is not None
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None

    response = client.post(
        f"{settings.API_V1_STR}/chats/",
        headers=normal_user_token_headers,
        json={
            "title": "Deduped DM",
            "participants": [str(super_user.id), str(super_user.id), str(normal_user.id)],
        },
    )

    assert response.status_code == 201
    content = response.json()
    assert content["chat_type"] == "dm"
    assert content["participants"] == [str(normal_user.id), str(super_user.id)]


def test_create_chat_rejects_invalid_participant_ids(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None

    response = client.post(
        f"{settings.API_V1_STR}/chats/",
        headers=normal_user_token_headers,
        json={"title": "Invalid", "participants": [str(super_user.id), "not-a-uuid"]},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "One or more selected participants are invalid"


def test_create_chat_rejects_unknown_participant_ids(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/chats/",
        headers=normal_user_token_headers,
        json={"title": "Unknown", "participants": [str(uuid.uuid4())]},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "One or more selected participants are invalid"


def test_read_chat(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Read chat",
    )

    response = client.get(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == created["id"]
    assert content["title"] == "Read chat"

    participant_headers = authentication_token_from_email(
        client=client,
        email=super_user.email,
        db=db,
    )
    participant_response = client.get(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=participant_headers,
    )

    assert participant_response.status_code == 200
    assert participant_response.json()["id"] == created["id"]


def test_read_chat_not_found(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/chats/{uuid.uuid4()}",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


def test_read_chat_not_enough_permissions(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Private chat",
    )
    outsider = create_random_user(db)
    outsider_headers = authentication_token_from_email(
        client=client,
        email=outsider.email,
        db=db,
    )

    response = client.get(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=outsider_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


def test_read_chats(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    first_chat = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="List chat A",
    )
    second_chat = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="List chat B",
    )

    response = client.get(
        f"{settings.API_V1_STR}/chats/",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert "count" in content
    assert len(content["data"]) >= 2

    participant_headers = authentication_token_from_email(
        client=client,
        email=super_user.email,
        db=db,
    )
    participant_response = client.get(
        f"{settings.API_V1_STR}/chats/",
        headers=participant_headers,
    )
    assert participant_response.status_code == 200
    participant_chat_ids = {
        chat["id"] for chat in participant_response.json()["data"]
    }
    assert first_chat["id"] in participant_chat_ids
    assert second_chat["id"] in participant_chat_ids


def test_read_chats_respects_skip_limit_and_count(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None

    created_ids = [
        create_chat(
            client,
            normal_user_token_headers,
            participant_id=str(super_user.id),
            title=f"Paged chat {index}",
        )["id"]
        for index in range(3)
    ]

    response = client.get(
        f"{settings.API_V1_STR}/chats/?skip=1&limit=1",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["count"] >= len(created_ids)
    assert len(content["data"]) == 1
    assert content["data"][0]["id"] in created_ids


def test_update_chat(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
) -> None:
    normal_user = db.exec(
        select(User).where(User.email == settings.EMAIL_TEST_USER)
    ).first()
    assert normal_user is not None

    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None

    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Old title",
    )
    payload = {
        "title": "Updated title",
        "participants": [str(super_user.id)],
        "last_message": "hello",
    }
    response = client.patch(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=normal_user_token_headers,
        json=payload,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["title"] == payload["title"]
    assert content["chat_type"] == "dm"
    assert content["last_message"] == payload["last_message"]
    assert str(normal_user.id) in content["participants"]


def test_update_chat_adds_participant_and_converts_to_group(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    third_user = create_random_user(db)
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Expand chat",
    )

    response = client.patch(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=normal_user_token_headers,
        json={"participants": [str(super_user.id), str(third_user.id)]},
    )

    assert response.status_code == 200
    content = response.json()
    assert content["chat_type"] == "group"
    assert set(content["participants"]) == {
        content["user_id"],
        str(super_user.id),
        str(third_user.id),
    }


def test_update_chat_rejects_invalid_participant_ids(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Strict update",
    )

    response = client.patch(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=normal_user_token_headers,
        json={"participants": [str(super_user.id), "bad-id"]},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "One or more selected participants are invalid"


def test_update_chat_forbidden_to_non_participant(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="No outsider updates",
    )
    outsider = create_random_user(db)
    outsider_headers = authentication_token_from_email(
        client=client,
        email=outsider.email,
        db=db,
    )

    response = client.patch(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=outsider_headers,
        json={"title": "Intrusion"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


def test_update_chat_not_found(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    payload = {
        "title": "Updated title",
    }
    response = client.patch(
        f"{settings.API_V1_STR}/chats/{uuid.uuid4()}",
        headers=normal_user_token_headers,
        json=payload,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


def test_delete_chat(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="To delete",
    )

    response = client.delete(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Chat deleted successfully"

    get_response = client.get(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=normal_user_token_headers,
    )
    assert get_response.status_code == 404


def test_leave_chat_removes_conversation_from_participant_inbox(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Leave me",
    )
    participant_headers = authentication_token_from_email(
        client=client,
        email=super_user.email,
        db=db,
    )

    response = client.post(
        f"{settings.API_V1_STR}/chats/{created['id']}/leave",
        headers=participant_headers,
    )
    assert response.status_code == 200

    inbox_response = client.get(
        f"{settings.API_V1_STR}/chats/",
        headers=participant_headers,
    )
    assert inbox_response.status_code == 200
    assert created["id"] not in {chat["id"] for chat in inbox_response.json()["data"]}


def test_leave_chat_keeps_history_for_remaining_participants(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Stay visible",
    )
    participant_headers = authentication_token_from_email(
        client=client,
        email=super_user.email,
        db=db,
    )

    response = client.post(
        f"{settings.API_V1_STR}/chats/{created['id']}/leave",
        headers=participant_headers,
    )

    assert response.status_code == 200

    owner_inbox_response = client.get(
        f"{settings.API_V1_STR}/chats/",
        headers=normal_user_token_headers,
    )
    assert owner_inbox_response.status_code == 200
    assert created["id"] in {
        chat["id"] for chat in owner_inbox_response.json()["data"]
    }


def test_leave_chat_prevents_second_leave(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Leave once",
    )
    participant_headers = authentication_token_from_email(
        client=client,
        email=super_user.email,
        db=db,
    )

    first_response = client.post(
        f"{settings.API_V1_STR}/chats/{created['id']}/leave",
        headers=participant_headers,
    )
    assert first_response.status_code == 200

    second_response = client.post(
        f"{settings.API_V1_STR}/chats/{created['id']}/leave",
        headers=participant_headers,
    )
    assert second_response.status_code == 404
    assert second_response.json()["detail"] == "Chat not found"


def test_report_chat(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Report this",
    )

    response = client.post(
        f"{settings.API_V1_STR}/chats/{created['id']}/report",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Chat reported successfully"

    db.expire_all()
    db_chat = db.get(Chat, uuid.UUID(created["id"]))
    assert db_chat is not None
    assert db_chat.reported_by == [str(db_chat.user_id)]


def test_report_chat_is_idempotent_for_same_user(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Report once",
    )

    for _ in range(2):
        response = client.post(
            f"{settings.API_V1_STR}/chats/{created['id']}/report",
            headers=normal_user_token_headers,
        )
        assert response.status_code == 200

    db.expire_all()
    db_chat = db.get(Chat, uuid.UUID(created["id"]))
    assert db_chat is not None
    assert db_chat.reported_by == [str(db_chat.user_id)]


def test_read_chat_contacts_excludes_current_user_and_filters_by_query(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    normal_user = db.exec(
        select(User).where(User.email == settings.EMAIL_TEST_USER)
    ).first()
    assert normal_user is not None
    searchable_user = create_random_user(db)
    searchable_user.full_name = "Unique Contact Name"
    db.add(searchable_user)
    db.commit()
    db.refresh(searchable_user)

    response = client.get(
        f"{settings.API_V1_STR}/chats/contacts?q=Unique Contact&limit=10",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    returned_ids = {item["id"] for item in content}
    assert str(searchable_user.id) in returned_ids
    assert str(normal_user.id) not in returned_ids


def test_delete_chat_hides_conversation_from_other_participants(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    super_user = db.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    assert super_user is not None
    created = create_chat(
        client,
        normal_user_token_headers,
        participant_id=str(super_user.id),
        title="Delete for all",
    )
    participant_headers = authentication_token_from_email(
        client=client,
        email=super_user.email,
        db=db,
    )

    response = client.delete(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200

    participant_get_response = client.get(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=participant_headers,
    )
    assert participant_get_response.status_code == 404
    assert participant_get_response.json()["detail"] == "Chat not found"


def test_create_chat_requires_other_participant(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/chats/",
        headers=normal_user_token_headers,
        json={"participants": []},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "A conversation must include at least one other participant"
