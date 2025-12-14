from django.contrib import admin
from .models import Poll, Option

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('option_text', 'poll')
