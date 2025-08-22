from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
import pytest
from django.urls import reverse
from tool.models import Tool

def test_homeview_context(client, tool, category):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
    assert tool in response.context["latest_tools"]
    assert category in response.context["categories"]

def test_homeview_html(client, tool):
    url = reverse("home")
    response = client.get(url)
    content = response.content.decode()
    assert tool.name in content
    assert "Choose necessary tool" in content

def test_toolsview_filters_by_city(client, multiple_tools):
    url = reverse("tools") + "?city=Warsaw"
    response = client.get(url)
    tools = response.context["tools"]
    assert response.status_code == 200
    assert multiple_tools[0] in tools
    assert multiple_tools[1] not in tools
    content = response.content.decode()
    assert "Pump" in content
    assert "Tire levers" not in content

def test_toolsview_filters_by_district(client, multiple_tools):
    url = reverse("tools") + "?district=Ochota"
    response = client.get(url)
    tools = response.context["tools"]
    assert response.status_code == 200
    assert multiple_tools[0] in tools
    assert multiple_tools[1] not in tools
    content = response.content.decode()
    assert "Pump" in content
    assert "Tire levers" not in content

def test_toolsview_post_search(client, multiple_tools):
    response = client.post(reverse("tools"), {"searched": "levers"})
    assert response.status_code == 200
    content = response.content.decode()
    assert "Tire levers" in content
    assert "Pump" not in content
    tools = response.context["tools"]
    assert multiple_tools[1] in tools
    assert multiple_tools[0] not in tools

def test_sorting_newest_oldest(client, multiple_tools):
    url_newest = reverse("tools") + "?sort=newest"
    response_newest = client.get(url_newest)
    content_newest = response_newest.content.decode()

    assert content_newest.index(multiple_tools[1].name) < content_newest.index(multiple_tools[0].name)

    url_oldest = reverse("tools") + "?sort=oldest"
    response_oldest = client.get(url_oldest)
    content_oldest = response_oldest.content.decode()

    assert content_oldest.index(multiple_tools[0].name) < content_oldest.index(multiple_tools[1].name)

def test_toolview_context(client, tool):
    response = client.get(reverse("tool", args=[tool.id]))
    assert response.status_code == 200
    assert response.context["tool"] == tool
    assert tool.owner.profile == response.context["user_profile"]

def test_toolview_html(client, tool):
    response = client.get(reverse("tool", args=[tool.id]))
    content = response.content.decode()
    assert tool.name in content
    assert tool.description in content

def test_categoryview_filters(client, multiple_tools, category):
    response = client.get(reverse("category", args=[category.name]) + "?district=Ochota")
    tools = response.context["tools"]
    assert multiple_tools[0] in tools
    assert multiple_tools[1] not in tools

def test_categoryview_invalid_category(client):
    response = client.get(reverse("category", args=["Invalid"]))
    assert response.status_code == 302

@pytest.mark.django_db
def test_add_tool_get_authenticated(client_logged):
    url = reverse("add-tool")
    response = client_logged.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert "New tool" in content

@pytest.mark.django_db
def test_add_tool_redirect_if_not_authenticated(client):
    url = reverse("add-tool")
    response = client.get(url)
    assert response.status_code == 302
    assert reverse("login") in response.url

@pytest.mark.django_db
def test_add_tool_post_authenticated(client_logged, user, category, all_tools_category, valid_image):
    url = reverse("add-tool")
    data = {
        "name": "Pump",
        "description": "Good pump",
        "category": [str(category.id), str(all_tools_category.id)],
        "image": valid_image,
    }
    response = client_logged.post(url, data, follow=True)
    assert response.status_code == 200
    assert Tool.objects.filter(name="Pump", owner=user).exists()
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "Your tool has been added" in messages

@pytest.mark.django_db
def test_user_tools_authenticated(client_logged, tool, valid_image, category):
    other_user = User.objects.create_user(username="other", password="12345")
    other_tool = Tool.objects.create(name="Pump", owner=other_user, image=valid_image)
    other_tool.category.add(category)

    url = reverse("my-tools")
    response = client_logged.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert tool.name in content
    assert other_tool.name not in content
    assert tool in response.context["tools"]
    assert other_tool not in response.context["tools"]

@pytest.mark.django_db
def test_user_tools_unauthenticated(client, tool):
    url = reverse("my-tools")
    response = client.get(url)
    assert response.status_code == 302
    assert reverse("login") in response.url
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "You are not logged in" in messages

@pytest.mark.django_db
def test_tool_update_get_authenticated(client_logged, tool):
    url = reverse("tool-update", args=[tool.id])
    response = client_logged.get(url)
    assert response.status_code == 200
    assert "Update tool" in response.content.decode()
    assert response.context["form"].instance == tool

@pytest.mark.django_db
def test_tool_update_post_authenticated(client_logged, tool, all_tools_category):
    url = reverse("tool-update", args=[tool.id])
    new_data = {
        "name": "Updated Tool",
        "description": "Updated description",
        "category": [str(all_tools_category.id)],
    }
    response = client_logged.post(url, new_data, follow=True)
    assert response.status_code == 200
    tool.refresh_from_db()
    assert tool.name == "Updated Tool"
    assert tool.description == "Updated description"
    categories = list(tool.category.all())
    assert len(categories) == 1
    assert categories[0].name == "All Tools"

@pytest.mark.django_db
def test_tool_update_post_foreign_tool(client, user, tool, valid_image, all_tools_category):

    foreign_user = User.objects.create_user(username="otheruser", password="pass123")
    client.login(username="otheruser", password="pass123")

    url = reverse("tool-update", args=[tool.id])
    new_data = {
        "name": "Hacked Tool",
        "description": "Trying to update foreign tool",
        "category": [str(all_tools_category.id)],
        "image": valid_image,
    }

    response = client.post(url, new_data)
    assert response.status_code == 404

    tool.refresh_from_db()
    assert tool.name == "Test Tool"
    assert tool.description == "Test description"

@pytest.mark.django_db
def test_tool_delete_authenticated(client_logged, tool):
    url = reverse("tool-delete", args=[tool.id])
    response = client_logged.post(url, follow=True)
    assert response.status_code == 200
    assert not Tool.objects.filter(id=tool.id).exists()


@pytest.mark.django_db
def test_tool_delete_unauthenticated(client, tool):
    url = reverse("tool-delete", args=[tool.id])
    response = client.post(url)
    assert response.status_code == 302
    assert reverse("login") in response.url
    assert Tool.objects.filter(id=tool.id).exists()