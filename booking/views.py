from django.utils import timezone
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from .serializers import BookSerializer, BookingSerializer, RatingSerializer
from booking.models import Booking, Book, Rating
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin


search_param = openapi.Parameter(
    name='search',
    in_=openapi.IN_QUERY,
    description='Search books by title or author (case-insensitive)',
    type=openapi.TYPE_STRING,
)

@swagger_auto_schema(
    method='get',
    manual_parameters=[search_param],
    responses={200: BookSerializer(many=True)},
    tags=["Book"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_list_view(request):
    search = request.GET.get('search')
    if search:
        books = Book.objects.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search) |
            Q(genre__icontains=search)
        )
    else:
        books = Book.objects.all()

    serializer = BookSerializer(books, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    responses={200: BookSerializer, 404: "Book not found"},
    tags=["Book"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_detail_view(request, pk):
    book = Book.objects.filter(id=pk).first()
    if not book:
        return Response({"error": f"Book - '{book.title}' not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(book, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    request_body=BookSerializer,
    responses={201: BookSerializer, 400: "Invalid credentials"},
    tags=["Book"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
@parser_classes([MultiPartParser, FormParser])
def create_book_view(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(current_borrower=None)
        return Response({"message": f"Book created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    request_body=BookSerializer,
    responses={200: BookSerializer, 404: "Book not found"},
    tags=["Book"]
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdmin])
@parser_classes([MultiPartParser, FormParser])
def update_book_view(request, pk):
    book = Book.objects.filter(id=pk).first()
    if not book:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(book, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": f"Book - '{book.title}' updated", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='delete',
    responses={204: "Book deleted", 404: "Book not found"},
    tags=["Book"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def delete_book_view(request, pk):
    book = Book.objects.filter(id=pk).first()
    if not book:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    book.delete()
    return Response({"message": f"Book - '{book.title}' deleted"}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_summary="Rate a book",
    request_body=RatingSerializer,
    responses={
        201: openapi.Response(description="Rating submitted successfully"),
        400: openapi.Response(description="Validation error"),
        403: openapi.Response(description="Return book before rating"),
        404: openapi.Response(description="Book not found")
    },
    tags=["Rating"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_book_view(request, pk):
    book = Book.objects.filter(id=pk).first()
    if not book:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    if not Booking.objects.filter(book=book, borrower=request.user).exists():
        return Response({"error": "Not your book"}, status=status.HTTP_403_FORBIDDEN)

    if not Booking.objects.filter(book=book, borrower=request.user, end_at__isnull=False).exists():
        return Response({"error": "Return book before rating"}, status=status.HTTP_403_FORBIDDEN)

    if Rating.objects.filter(book=book, user=request.user).exists():
        return Response({"error": "You already rated this book"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RatingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, book=book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_summary="Book a book",
    request_body=BookingSerializer,
    responses={
        201: openapi.Response(description="Book booked successfully. Includes book title and PDF URL."),
        400: openapi.Response(description="Book already borrowed or validation error"),
        409: openapi.Response(description="You already borrowed this book"),
    },
    tags=["Booking"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def booking_view(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.validated_data['book']

        if book.current_borrower == request.user:
            return Response({"message": "You already borrowed this book"}, status=status.HTTP_409_CONFLICT)
        if not book.is_available:
            return Response({'error': f"Book is already borrowed by {book.current_borrower.username}"}, status=status.HTTP_400_BAD_REQUEST)

        book.current_borrower = request.user
        book.is_available = False
        book.save()

        serializer.save(borrower=request.user)

        pdf_url = request.build_absolute_uri(book.pdf.url) if book.pdf else None

        return Response({
            "message": f"Book - '{book.title}' booked successfully",
            "book": {
                "title": book.title,
                "pdf_url": pdf_url,
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    responses={
        200: openapi.Response("Book returned successfully"),
        404: "Book not found or not borrowed by user"
    },
    tags=["Booking"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book_view(request, pk):
    active_booking = (
        Booking.objects.select_related('book')
        .filter(book_id=pk, borrower=request.user, end_at__isnull=True)
        .first()
    )
    if not active_booking:
        return Response(
            {"error": "You didn't borrow this book"}, status=status.HTTP_404_NOT_FOUND
        )

    active_booking.end_at = timezone.now()
    active_booking.save()

    book = active_booking.book
    book.is_available = True
    book.current_borrower = None
    book.save()

    return Response(
        {"message": f"Book - '{book.title}' returned"},
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(
    method='get',
    responses={200: "User reading/finished books stats"},
    tags=["Profile"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    read_books = Booking.objects.filter(borrower=user, end_at__isnull=True).select_related('book')
    finish_books = Booking.objects.filter(borrower=user, end_at__isnull=False).select_related('book')

    reading_books = [b.book for b in read_books]
    finished_books = [b.book for b in finish_books]

    return Response({
        "username": user.username,
        "reading_books_count": len(reading_books),
        "finished_books_count": len(finished_books),
        "reading_books": BookSerializer(reading_books, many=True, context={"request": request}).data,
        "finished_books": BookSerializer(finished_books, many=True, context={"request": request}).data,
    }, status=status.HTTP_200_OK)

