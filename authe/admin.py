from django.contrib import admin
from authe.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", 'username', 'role')
    list_display_links  = ("id", 'username', 'role')
    search_fields = ('username',)
    list_filter = ('username', 'id')

admin.site.register(User, UserAdmin)