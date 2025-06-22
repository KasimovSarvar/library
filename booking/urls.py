from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from booking.views import (book_list_view, book_detail_view,
                           create_book_view, update_book_view,
                           delete_book_view, booking_view,
                           return_book_view, profile_view, rate_book_view)

urlpatterns = [
    path('book_list/', book_list_view, name='book_list'),
    path('book_detail/<int:pk>/', book_detail_view, name='book_detail'),
    path('create_book/', create_book_view, name='create_book'),
    path('update_book/<int:pk>/', update_book_view, name='update_book'),
    path('delete_book/<int:pk>/', delete_book_view, name='delete_book'),
    path('booking/', booking_view, name='booking'),
    path('return_book/<int:pk>/', return_book_view, name='return_book'),
    path('rate_book/<int:pk>/', rate_book_view, name='rate_book'),
    path('profile/', profile_view, name='profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)