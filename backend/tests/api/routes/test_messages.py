import uuid

from fastapi.testclient import TestClient

from app.core.config import settings


def create_chat(client: TestClient, token_headers: dict[str, str]) -> dict:
    payload = {
        "title": "Chat for messages",
        "participants": [],
    }
    response = client.post(
        f"{settings.API_V1_STR}/chats/",
        headers=token_headers,
        json=payload,
    )
    assert response.status_code == 201
    return response.json()


def create_message(
    client: TestClient,
    token_headers: dict[str, str],
    chat_id: str,
    content: str = "hello",
) -> dict:
    payload = {
        "content": content,
        "attachments": ["https://example.com/file.pdf"],
    }
    response = client.post(
        f"{settings.API_V1_STR}/chats/{chat_id}/messages/",
        headers=token_headers,
        json=payload,
    )
    assert response.status_code == 201
    return response.json()


def test_create_message(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    chat = create_chat(client, normal_user_token_headers)

    payload = {
        "content": "first message",
        "attachments": ["https://example.com/doc.txt"],
    }
    response = client.post(
        f"{settings.API_V1_STR}/chats/{chat['id']}/messages/",
        headers=normal_user_token_headers,
        json=payload,
    )

    assert response.status_code == 201
    content = response.json()
    assert content["chat_id"] == chat["id"]
    assert content["content"] == payload["content"]
    assert content["attachments"] == payload["attachments"]


def test_read_message(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    chat = create_chat(client, normal_user_token_headers)
    message = create_message(client, normal_user_token_headers, chat_id=chat["id"])

    response = client.get(
        f"{settings.API_V1_STR}/chats/{chat['id']}/messages/{message['id']}",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == message["id"]
    assert content["chat_id"] == chat["id"]


def test_read_messages(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    chat = create_chat(client, normal_user_token_headers)
    create_message(client, normal_user_token_headers, chat_id=chat["id"], content="a")
    create_message(client, normal_user_token_headers, chat_id=chat["id"], content="b")

    response = client.get(
        f"{settings.API_V1_STR}/chats/{chat['id']}/messages/",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["count"] >= 2
    assert len(content["data"]) >= 2


def test_update_message(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    chat = create_chat(client, normal_user_token_headers)
    message = create_message(client, normal_user_token_headers, chat_id=chat["id"])

    payload = {
        "content": "updated content",
        "attachments": ["https://example.com/new.png"],
    }
    response = client.patch(
        f"{settings.API_V1_STR}/chats/{chat['id']}/messages/{message['id']}",
        headers=normal_user_token_headers,
        json=payload,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["content"] == payload["content"]
    assert content["attachments"] == payload["attachments"]


def test_delete_message(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    chat = create_chat(client, normal_user_token_headers)
    message = create_message(client, normal_user_token_headers, chat_id=chat["id"])

    response = client.delete(
        f"{settings.API_V1_STR}/chats/{chat['id']}/messages/{message['id']}",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Message deleted successfully"

    get_response = client.get(
        f"{settings.API_V1_STR}/chats/{chat['id']}/messages/{message['id']}",
        headers=normal_user_token_headers,
    )
    assert get_response.status_code == 404


def test_create_message_chat_not_found(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    payload = {
        "content": "msg",
        "attachments": [],
    }
    response = client.post(
        f"{settings.API_V1_STR}/chats/{uuid.uuid4()}/messages/",
        headers=normal_user_token_headers,
        json=payload,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


def test_read_message_not_enough_permissions(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    superuser_token_headers: dict[str, str],
) -> None:
    chat = create_chat(client, normal_user_token_headers)
    message = create_message(client, normal_user_token_headers, chat_id=chat["id"])

    response = client.get(
        f"{settings.API_V1_STR}/chats/{chat['id']}/messages/{message['id']}",
        headers=superuser_token_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"
