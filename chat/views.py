from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from booking.models import Booking

@login_required
def booking_chat_room(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user == booking.borrower:
        return render(request, 'chat/room.html', {'booking': booking})
    else:
        return HttpResponseForbidden()