from django.contrib import admin
from .models import UserProfile, Preference, Match

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender')
    search_fields = ('user__username', 'age', 'gender')

class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'smoking', 'pets', 'noise_level', 'sleep_schedule')
    list_filter = ('smoking', 'pets', 'noise_level', 'sleep_schedule')

class MatchAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'score')
    search_fields = ('user1__user__username', 'user2__user__username')
    ordering = ('-score',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Preference, PreferenceAdmin)
admin.site.register(Match, MatchAdmin)
