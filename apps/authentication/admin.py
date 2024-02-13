from django.contrib import admin
from .models import User, Profile, About, FriendRequest,Friendship


# class CustomProfileAdmin(admin.TabularInline):
#     model = Profile


# class CustomUserAdmin(admin.ModelAdmin):
#     inlines = [
#         CustomProfileAdmin,
#     ]

# admin.site.register(User, CustomUserAdmin)

admin.site.register(Profile)
admin.site.register(User)
admin.site.register(About)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
