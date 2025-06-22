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
        read_only_fields = ('book', 'user')
        fields = ('id', 'book', 'user', 'stars', 'comment')

        def validate_stars(self, value):
            if not 1 <= value <= 5:
                raise serializers.ValidationError("Stars must be between 1 and 5")
            return value