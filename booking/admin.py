from django.contrib import admin
from booking.models import Book, Booking, Rating

class RateInline(admin.TabularInline):
    model = Rating
    extra = 1

class BookAdmin(admin.ModelAdmin):
    list_display = ("id", 'title', 'author', 'genre', 'current_borrower', 'is_available')
    list_display_links  = ("id", 'title', 'author', 'genre', 'current_borrower')
    search_fields = ('title', 'genre', 'author')
    list_filter = ('title', 'id', 'genre', 'is_available')
    inlines = [RateInline]

class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", 'book', 'borrower', 'start_at', 'end_at')
    list_display_links  = ("id", 'book', 'borrower',)
    search_fields = ('book', 'borrower')
    list_filter = ('book', 'id', 'start_at', 'end_at')
    readonly_fields = ('start_at', 'end_at')

class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", 'book', 'user', 'stars')
    list_display_links  = ("id", 'book', 'user', 'stars')
    search_fields = ('book', 'user')
    list_filter = ('book', 'id', 'user', 'stars')


admin.site.register(Book, BookAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Booking, BookingAdmin)
