import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.models import User


def create_chat(
    client: TestClient, token_headers: dict[str, str], title: str = "Chat title"
) -> dict:
    payload = {
        "title": title,
        "participants": [],
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

    payload = {
        "title": "My first chat",
        "participants": [],
    }
    response = client.post(
        f"{settings.API_V1_STR}/chats/",
        headers=normal_user_token_headers,
        json=payload,
    )

    assert response.status_code == 201
    content = response.json()
    assert content["title"] == payload["title"]
    assert content["user_id"] == str(normal_user.id)
    assert str(normal_user.id) in content["participants"]
    assert content["last_message"] is None
    assert content["created_at"] is not None


def test_read_chat(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    created = create_chat(client, normal_user_token_headers, title="Read chat")

    response = client.get(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == created["id"]
    assert content["title"] == "Read chat"


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
    superuser_token_headers: dict[str, str],
) -> None:
    created = create_chat(client, normal_user_token_headers, title="Private chat")

    response = client.get(
        f"{settings.API_V1_STR}/chats/{created['id']}",
        headers=superuser_token_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


def test_read_chats(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    create_chat(client, normal_user_token_headers, title="List chat A")
    create_chat(client, normal_user_token_headers, title="List chat B")

    response = client.get(
        f"{settings.API_V1_STR}/chats/",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert "count" in content
    assert len(content["data"]) >= 2


def test_update_chat(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
) -> None:
    normal_user = db.exec(
        select(User).where(User.email == settings.EMAIL_TEST_USER)
    ).first()
    assert normal_user is not None

    created = create_chat(client, normal_user_token_headers, title="Old title")
    payload = {
        "title": "Updated title",
        "participants": [str(uuid.uuid4())],
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
    assert content["last_message"] == payload["last_message"]
    assert str(normal_user.id) in content["participants"]


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
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    created = create_chat(client, normal_user_token_headers, title="To delete")

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
