from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=50, default='Poland')
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    address = models.CharField(max_length=50, default='', blank=True)
    zipcode = models.CharField(max_length=12, default='', blank=True)
    phone = PhoneNumberField(blank=True, region='PL')
    profile_picture = models.ImageField(upload_to='uploads/profile/', blank=True, null=True)

    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()
post_save.connect(create_user_profile, sender=User)