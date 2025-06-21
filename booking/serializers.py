from rest_framework import serializers
from booking.models import Book, Booking, Rating

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'genre', 'pdf')


class BookingSerializer(serializers.ModelSerializer):
    pdf = serializers.FileField(source='book.pdf', read_only=True)
    class Meta:
        model = Booking
        read_only_fields = ('start_at', 'end_at')
        fields = ('id', 'book', 'pdf', 'start_at', 'end_at')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'book', 'user', 'stars', 'comment')