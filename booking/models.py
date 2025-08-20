from django.contrib.auth.models import User
from django.db import models
from tool.models import Tool

class BookingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    DECLINED = 'declined', 'Declined'

class Booking(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_made')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_seen_by_owner = models.BooleanField(default=False)
    is_seen_by_borrower = models.BooleanField(default=True)
    comment = models.TextField(blank=True, default='')

    def __str__(self):
        return f'{self.borrower.username} - {self.tool.name} ({self.status})'
