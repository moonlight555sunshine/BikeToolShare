from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User

admin.site.register(UserProfile)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "email", "first_name", "last_name"]
    inlines = [UserProfileInline]

# # unregister the old way
# admin.site.unregister(User)
#
# # register the new way
# admin.site.register(User, UserAdmin)