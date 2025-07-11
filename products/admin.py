# products/admin.py
from django.contrib import admin
from .models import ClothingStyle

@admin.register(ClothingStyle)
class ClothingStyleAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_editable = ['is_active']