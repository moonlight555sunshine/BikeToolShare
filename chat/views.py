from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views import View
from django.db.models import Max, OuterRef, Subquery, Q

from booking.models import Booking
from chat.models import Message


@login_required
def booking_chat_room(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user == booking.borrower or request.user == booking.tool.owner:
        latest_messages = booking.chat_messages.select_related('user').order_by('-sent_on')
        latest_messages = reversed(latest_messages)
        return render(request,'chat/room.html', {'booking': booking, 'latest_messages' : latest_messages })
    else:
        return HttpResponseForbidden()

class ChatListView(View):
    def get(self, request):
        if request.user.is_authenticated:
            last_message = (
                Message.objects
                .filter(booking=OuterRef('pk'))
                .order_by('-sent_on')
            )
            my_tools_chats = (Booking.objects
                        .filter(
                            tool__owner=request.user,
                            chat_messages__isnull=False,
                        )
                        .annotate(
                            last_message_at=Max('chat_messages__sent_on'),
                            last_message_text=Subquery(
                                last_message.values('content')[:1]
                            ),
                            last_message_user=Subquery(
                                last_message.values('user__username')[:1]
                            ),
                        )
                        .select_related('tool')
                        .order_by('-last_message_at'))
            rented_tools_chats = (Booking.objects
                        .filter(
                            borrower=request.user,
                            chat_messages__isnull=False,
                        )
                        .annotate(
                            last_message_at=Max('chat_messages__sent_on'),
                            last_message_text=Subquery(
                                last_message.values('content')[:1]
                            ),
                            last_message_user=Subquery(
                                last_message.values('user__username')[:1]
                            ),
                        )
                        .select_related('tool')
                        .order_by('-last_message_at'))
            return render(request, 'chat/chat_list.html', {
                'my_tools_chats': my_tools_chats,
                'rented_tools_chats': rented_tools_chats,
                'title': 'Сhats',
                'subtitle': 'Your conversations',
            })
        else:
            messages.error(request, 'You are not logged in')
            return redirect('login')