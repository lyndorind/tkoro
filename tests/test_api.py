from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Service is running"
    }


def test_info():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Git Lab 2 REST Service",
        "version": "1.0.0",
    }


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Git Lab 2 REST Service",
    }


def test_hello():
    response = client.get("/hello/Tamara")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, Tamara!"
    }


def test_hello_unicode():
    response = client.get("/hello/%D0%A2%D0%B0%D0%BC%D0%B0%D1%80%D0%B0")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, Тамара!"
    }
