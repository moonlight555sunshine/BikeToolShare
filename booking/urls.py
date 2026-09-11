from django.urls import path
from booking.views import OwnerBookingsView, BorrowerBookingsView, BookToolView, BookCancelView

urlpatterns = [
    path('owner/bookings/', OwnerBookingsView.as_view(), name='owner_bookings'),
    path('owner/bookings/<int:booking_id>/', OwnerBookingsView.as_view(), name='owner_booking_action'),
    path('borrower/bookings/', BorrowerBookingsView.as_view(), name='borrower_bookings'),
    path('book-tool/<int:tool_id>/', BookToolView.as_view(), name='book_tool'),
    path('borrower/bookings/cancel/<int:pk>/', BookCancelView.as_view(), name='booking-cancel'),
]