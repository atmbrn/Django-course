from django.db import models
from django.utils import timezone


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return str(self)

    def books_count(self):
        return self.books.count()


class Book(models.Model):
    STATUS_AVAILABLE = 'available'
    STATUS_CHECKED_OUT = 'checked_out'
    STATUS_RESERVED = 'reserved'

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_CHECKED_OUT, 'Checked out'),
        (STATUS_RESERVED, 'Reserved'),
    ]

    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['-published_date', 'title']

    def __str__(self):
        return self.title

    def age_days(self):
        if not self.published_date:
            return None
        delta = timezone.now().date() - self.published_date
        return delta.days
