from django.db import models
from authe.models import User
from abstraction.base_models import BaseModel

class Book(BaseModel):
    GENRES = [
        ("fiction", "Fiction"),
        ("science", "Science"),
        ("historical", "Historical"),
        ("biography", "Biography"),
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=20, choices=GENRES)
    pdf = models.FileField(upload_to="books/pdfs/")
    is_available = models.BooleanField(default=True)
    current_borrower = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='borrowed_books')

    def __str__(self):
        return self.title

class Booking(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.borrower} -> {self.book.title}"

class Rating(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.stars}⭐️ - {self.book.title} by {self.user}"
