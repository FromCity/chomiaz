import pytest
import json
from django.test import Client
from celery import Celery
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chomiaz.settings")
django.setup()
from .models import Message
from .data_test import payload, payload_order_status, payload_operator_request, payload_unknown
from .data_test import payload_history1, payload_history2, data_history
from .models import MessageType


@pytest.fixture(scope="module")
def celery_app():
    """
    Configures a test-specific Celery app for pytest.
    """
    app = Celery("test_chomiaz")
    app.conf.update(
        broker_url="redis://127.0.0.1:6379",
        result_backend="redis://127.0.0.1:6379",
        task_always_eager=True,
        task_eager_propagates=True,
    )
    return app

@pytest.mark.django_db
def test_create(celery_app):
    client = Client()
    response = client.post("/api/webhooks/messages/", json.dumps(payload),
                                content_type="application/json")
    queryset = Message.objects.get(external_message_id=payload['external_message_id'])

    data = {"external_message_id":queryset.external_message_id,
            "user_id": queryset.user_id, "text":queryset.text,
            "created_at": queryset.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')}
    assert data == payload
    queryset.delete()

@pytest.mark.django_db
def test_repeat_2_webhook(celery_app):
    client = Client()
    response1 = client.post("/api/webhooks/messages/", json.dumps(payload),
                                content_type="application/json")
    response2 = client.post("/api/webhooks/messages/", json.dumps(payload),
                                content_type="application/json")
    queryset = Message.objects.filter(external_message_id=payload['external_message_id'])
    assert queryset.count() == 1
    Message.objects.get(external_message_id=payload['external_message_id']).delete()

@pytest.mark.django_db
def test_invalid_webhook(celery_app):
    client = Client()
    response = client.get("/api3/messages/1")
    assert response.status_code == 404

@pytest.mark.django_db
def test_order_type(celery_app):
    client = Client()
    response = client.post("/api/webhooks/messages/", json.dumps(payload_order_status),
                                content_type="application/json")
    queryset = Message.objects.get(external_message_id=payload_order_status['external_message_id'])
    assert queryset.message_type == MessageType.ORDER_STATUS
    queryset.delete()


@pytest.mark.django_db
def test_operator_type(celery_app):
    client = Client()
    response = client.post("/api/webhooks/messages/", json.dumps(payload_operator_request),
                                content_type="application/json")
    queryset = Message.objects.get(external_message_id=payload_operator_request['external_message_id'])
    assert queryset.message_type == MessageType.OPERATOR_REQUEST
    queryset.delete()

@pytest.mark.django_db
def test_unknown_type(celery_app):
    client = Client()
    response = client.post("/api/webhooks/messages/", json.dumps(payload_unknown),
                                content_type="application/json")
    queryset = Message.objects.get(external_message_id=payload_unknown['external_message_id'])
    assert queryset.message_type == MessageType.UNKNOWN
    queryset.delete()


@pytest.mark.django_db
def test_history_message(celery_app):
    client = Client()
    response = client.post("/api/webhooks/messages/", json.dumps(payload_history1),
                                content_type="application/json")
    response = client.post("/api/webhooks/messages/", json.dumps(payload_history2),
                                content_type="application/json")
    response = client.get(f"/api/users/{payload_history1['user_id']}/messages",
                          content_type="application/json")
    content = eval(response.content.decode("utf-8"))

    #res = {x.split(":")[0]: str(x.split(":")[1]) for x in content.split(", ")}
    #content =res
    data = [{"external_message_id":content[0]['external_message_id'],
            "user_id": content[0]['user_id'], "text":content[0]['text'],
            "created_at": content[0]['created_at']},

            {"external_message_id":content[1]['external_message_id'],
            "user_id": content[1]['user_id'], "text":content[1]['text'],
            "created_at": content[1]['created_at']}]

    assert data == data_history
    queryset = Message.objects.filter(user_id=payload_history1['user_id'])
    queryset.delete()


@pytest.mark.django_db
def test_message_detail(celery_app):
    client = Client()
    response = client.post("/api/webhooks/messages/", json.dumps(payload),
                                content_type="application/json")
    id = eval(response.content.decode("utf-8"))['id']

    response = client.get(f"/api/messages/{id}",
                                content_type="application/json")
    content = eval(response.content.decode("utf-8"))
    data = {"external_message_id":content['external_message_id'],
            "user_id": content['user_id'], "text":content['text'],
            "created_at": content['created_at']}
    assert data == payload
    queryset = Message.objects.get(id=id)
    queryset.delete()
