import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from booking.models import Booking


@pytest.mark.django_db
def test_book_tool_get_authenticated(client_logged, tool_owned_by_other):
    url = reverse("book_tool", args=[tool_owned_by_other.id])
    response = client_logged.get(url)
    assert response.status_code == 200
    assert f"Book {tool_owned_by_other.name}" in response.content.decode()

@pytest.mark.django_db
def test_book_tool_post_authenticated(client_logged, user, tool_owned_by_other):
    url = reverse("book_tool", args=[tool_owned_by_other.id])
    data = {"start_date": "2025-01-01", "end_date": "2025-01-02", "comment": "Need tool"}
    response = client_logged.post(url, data, follow=True)

    assert response.status_code == 200
    assert Booking.objects.filter(borrower=user, tool=tool_owned_by_other).exists()
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "Booking request sent!" in messages[0]

@pytest.mark.django_db
def test_book_tool_post_own_tool(client_logged, tool):
    url = reverse("book_tool", args=[tool.id])
    data = {"start_date": "2025-01-01", "end_date": "2025-01-02"}
    response = client_logged.post(url, data, follow=True)

    assert response.status_code == 200
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "You cannot book your own tool." in messages[0]
    assert not Booking.objects.filter(tool=tool).exists()

@pytest.mark.django_db
def test_owner_bookings_get_authenticated(client_logged, booking_for_user_tool):
    url = reverse("owner_bookings")
    response = client_logged.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert "Booking requests" in content
    assert booking_for_user_tool.tool.name in content
    assert booking_for_user_tool in response.context["bookings"]
    booking_for_user_tool.refresh_from_db()
    assert booking_for_user_tool.is_seen_by_owner is True

@pytest.mark.django_db
def test_owner_bookings_post_approve(client_logged, booking_for_user_tool):
    url = reverse("owner_booking_action", args=[booking_for_user_tool.id])
    data = {"action": "approve"}
    response = client_logged.post(url, data, follow=True)
    booking_for_user_tool.refresh_from_db()
    assert booking_for_user_tool.status == "approved"
    assert booking_for_user_tool.tool.is_available is False

    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert f"Request for {booking_for_user_tool.tool.name} approved!" in messages

@pytest.mark.django_db
def test_owner_bookings_post_decline(client_logged, booking_for_user_tool):
    url = reverse("owner_booking_action", args=[booking_for_user_tool.id])
    data = {"action": "decline"}
    response = client_logged.post(url, data, follow=True)

    booking_for_user_tool.refresh_from_db()
    assert booking_for_user_tool.status == "declined"
    assert booking_for_user_tool.tool.is_available is True

    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert f"Request for {booking_for_user_tool.tool.name} declined." in messages

@pytest.mark.django_db
def test_borrower_bookings_get_authenticated(client_logged, booking_request):
    url = reverse("borrower_bookings")
    response = client_logged.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert "My bookings" in content
    assert booking_request.tool.name in content
