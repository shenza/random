from django.contrib import admin

from .models import Control


@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    pass
