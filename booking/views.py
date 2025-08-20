from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Booking, Tool
from booking.forms import BookingForm

class OwnerBookingsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            bookings = Booking.objects.filter(tool__owner=request.user).select_related('tool', 'borrower')
            bookings.filter(is_seen_by_owner=False).update(is_seen_by_owner=True)
            return render(request, 'owner_bookings.html', {
                'bookings': bookings,
                'title': 'Booking requests',
                'subtitle': 'Approve or decline requests',
            })
        else:
            messages.error(request, 'You are not logged in')
            return redirect('login')
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, tool__owner=request.user)
        tool = Tool.objects.get(id=booking.tool_id)
        action = request.POST.get('action')
        if action == 'approve':
            booking.status = 'approved'
            tool.is_available = False
            messages.success(request, f'Request for {booking.tool.name} approved!')
        elif action == 'decline':
            booking.status = 'declined'
            tool.is_available = True
            messages.warning(request, f'Request for {booking.tool.name} declined.')
        booking.is_seen_by_borrower = False
        booking.save()
        tool.save()
        return redirect('owner_bookings')

class BorrowerBookingsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            bookings = Booking.objects.filter(borrower=request.user).select_related('tool', 'tool__owner')
            bookings.filter(is_seen_by_borrower=False).update(is_seen_by_borrower=True)
            return render(request, 'borrower_bookings.html', {
                'bookings': bookings,
                'title': 'My bookings',
                'subtitle': 'Status of your requests',
            })
        else:
            messages.error(request, 'You are not logged in')
            return redirect('login')

class BookToolView(View):
    def get(self, request, tool_id):
        if request.user.is_authenticated:
            tool = get_object_or_404(Tool, id=tool_id)
            form = BookingForm()
            return render(request, 'form_page.html', {
                'form': form,
                'title': f'Book {tool.name}',
                'subtitle': 'Select dates and leave a comment',
                'button_text': 'Send request',
            })
        else:
            messages.error(request, 'You are not logged in')
            return redirect('login')
    def post(self, request, tool_id):
        tool = get_object_or_404(Tool, id=tool_id)
        form = BookingForm(request.POST)
        if tool.owner == request.user:
            messages.error(request, "You cannot book your own tool.")
            return redirect('tool', pk=tool.id)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tool = tool
            booking.borrower = request.user
            booking.status = 'pending'
            booking.save()
            messages.success(request, 'Booking request sent!')
            return redirect('tool', pk=tool.id)
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'form_page.html', {
                'form': form,
                'title': f'Book {tool.name}',
                'subtitle': 'Select dates and leave a comment',
                'button_text': 'Send request',
            })