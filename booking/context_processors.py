from itertools import count

from .models import Booking

def notifications(request):
    if not request.user.is_authenticated:
        return {}
    owner_unread = Booking.objects.filter(tool__owner=request.user, is_seen_by_owner=False).count()
    borrower_unread = Booking.objects.filter(borrower=request.user, is_seen_by_borrower=False).count()
    return {
        'owner_unread': owner_unread,
        'borrower_unread': borrower_unread,
        'total_unread': owner_unread + borrower_unread,
    }