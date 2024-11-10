from django.contrib import admin
from django.contrib.auth import get_user_model

from user.models import UserProfile

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_verified', 'is_staff')


admin.site.register(User, UserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_type')


admin.site.register(UserProfile, UserProfileAdmin)
