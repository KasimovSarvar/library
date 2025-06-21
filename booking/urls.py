from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from booking.views import book_list_view, book_detail_view, create_book_view, update_book_view, delete_book_view, booking_view, return_book_view

urlpatterns = [
    path('book_list/', book_list_view),
    path('book_detail/<int:pk>/', book_detail_view),
    path('create_book/', create_book_view),
    path('update_book/<int:pk>/', update_book_view),
    path('delete_book/<int:pk>/', delete_book_view),
    path('booking/', booking_view),
    path('return_book/', return_book_view),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)