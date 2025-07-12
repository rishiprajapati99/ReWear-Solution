from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'phone', 'location', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'location')}),
    ) # type: ignore
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'location')}),
    )

admin.site.register(User, CustomUserAdmin)
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'size', 'owner', 'created_at']
    search_fields = ['name', 'category', 'size', 'owner__email']
from .models import SwapRequest

@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    list_display = ['item_from', 'item_to', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['item_from__name', 'item_to__name']
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender', 'swap_request', 'message', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['sender__email', 'message']
from .models import PracticeLog

@admin.register(PracticeLog)
class PracticeLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'items_uploaded', 'swaps_made', 'last_active']
    search_fields = ['user__email']
