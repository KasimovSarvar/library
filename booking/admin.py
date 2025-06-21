from django.contrib import admin
from booking.models import Book, Booking


class BookAdmin(admin.ModelAdmin):
    list_display = ("id", 'title', 'author', 'genre', 'current_borrower', 'is_available')
    list_display_links  = ("id", 'title', 'author', 'genre', 'current_borrower')
    search_fields = ('title', 'genre', 'author')
    list_filter = ('title', 'id', 'genre', 'is_available')

class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", 'book', 'borrower', 'start_at', 'end_at')
    list_display_links  = ("id", 'book', 'borrower',)
    search_fields = ('book', 'borrower')
    list_filter = ('book', 'id', 'start_at', 'end_at')
    readonly_fields = ('start_at', 'end_at')

admin.site.register(Book, BookAdmin)
admin.site.register(Booking, BookingAdmin)