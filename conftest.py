import pytest
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from tool.models import Tool, Category

@pytest.fixture
def valid_image():
    file = io.BytesIO()
    image = Image.new("RGB", (1, 1), color="white")
    image.save(file, "PNG")
    file.seek(0)
    return SimpleUploadedFile("test.png", file.read(), content_type="image/png")

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpswd", email = "testuser@example.com")

@pytest.fixture
def category(db):
    category = Category.objects.create(name="Wheels")
    return category

@pytest.fixture(autouse=True)
def all_tools_category(db):
    category, _ = Category.objects.get_or_create(name="All Tools")
    return category

@pytest.fixture
def tool(user, category, valid_image):

    tool = Tool.objects.create(
        name="Test Tool",
        description="Test description",
        owner=user,
        is_available=True,
        image=valid_image,
    )
    tool.category.add(category)
    return tool

@pytest.fixture
def multiple_tools(db, category, valid_image):

    user1 = User.objects.create_user(username="user1", password="pass")
    user1.profile.city = "Warsaw"
    user1.profile.district = "Ochota"
    user1.profile.save()
    tool1 = Tool.objects.create(name="Pump", owner=user1, image=valid_image)
    tool1.category.add(category)

    user2 = User.objects.create_user(username="user2", password="pass")
    user2.profile.city = "Krakow"
    user1.profile.district = "Old town"
    user2.profile.save()
    tool2 = Tool.objects.create(name="Tire levers", owner=user2, image=valid_image)
    tool2.category.add(category)


    return [tool1, tool2]

@pytest.fixture
def client_logged(client, user):
    client.login(username="testuser", password="testpswd")
    return client