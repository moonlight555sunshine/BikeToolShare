import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from accounts.models import UserProfile

@pytest.mark.django_db
def test_register_get(client):
    url = reverse("register")
    response = client.get(url)
    assert response.status_code == 200
    assert "Register" in response.content.decode()

@pytest.mark.django_db
def test_register_post_valid(client):
    url = reverse("register")
    data = {
        "username": "newuser",
        "password1": "StrongPassword123!",
        "password2": "StrongPassword123!",
        "email": "newuser@example.com",
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert User.objects.filter(username="newuser").exists()
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "Account created" in messages[0]

@pytest.mark.django_db
def test_register_post_invalid(client):
    url = reverse("register")
    data = {
        "username": "baduser",
        "password1": "123",
        "password2": "456",
        "email": "baduser@example.com",
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert not User.objects.filter(username="baduser").exists()
    assert "Please correct the error below." in response.content.decode()


@pytest.mark.django_db
def test_login_get(client):
    url = reverse("login")
    response = client.get(url)
    assert response.status_code == 200
    assert "Login" in response.content.decode()

@pytest.mark.django_db
def test_login_post_valid(client, user):
    url = reverse("login")
    data = {"username": user.username, "password": "testpswd"}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "You are now logged in" in messages[0]

@pytest.mark.django_db
def test_logout_view(client_logged):
    url = reverse("logout")
    response = client_logged.get(url, follow=True)
    assert response.status_code == 200
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "logged out" in messages[0]

@pytest.mark.django_db
def test_update_info_post_authenticated(client_logged, user, valid_image):
    url = reverse("update_info")
    data = {
        "city": "Warsaw",
        "district": "Ochota",
        "profile_picture": valid_image,
    }
    response = client_logged.post(url, data, follow=True)

    assert response.status_code == 200
    user.profile.refresh_from_db()
    assert user.profile.city == "Warsaw"

@pytest.mark.django_db
def test_update_info_redirect_if_unauthenticated(client):
    url = reverse("update_info")
    response = client.get(url)

    assert response.status_code == 302
    assert reverse("login") in response.url

@pytest.mark.django_db
def test_account_view_authenticated(client_logged, user):
    url = reverse("account")
    response = client_logged.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "Your account" in content
    assert user.username in content
    assert user.email in content
    assert user.profile.city in content
    assert user.profile.district in content

@pytest.mark.django_db
def test_account_view_redirect_if_unauthenticated(client):
    url = reverse("account")
    response = client.get(url)

    assert response.status_code == 302
    assert reverse("login") in response.url

