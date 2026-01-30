from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils import timezone

from .models import Author, Book


class BookInline(admin.TabularInline):
    model = Book
    fields = ('title', 'published_date', 'status')
    extra = 0
    max_num = 5
    show_change_link = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'books_count', 'last_book_date', 'created_at')
    search_fields = ('first_name', 'last_name', 'bio')
    inlines = [BookInline]
    list_per_page = 20

    def full_name(self, obj):
        return obj.full_name()

    full_name.short_description = 'Name'

    def books_count(self, obj):
        return obj.books_count()

    books_count.short_description = 'Books'

    def last_book_date(self, obj):
        last = obj.books.order_by('-published_date').first()
        if last and last.published_date:
            return last.published_date
        return '-'

    last_book_date.short_description = 'Last published'


@admin.action(description='Mark selected books as available')
def make_available(modeladmin, request, queryset):
    updated = queryset.update(status=Book.STATUS_AVAILABLE)
    modeladmin.message_user(request, f"{updated} book(s) marked as available.", messages.SUCCESS)


@admin.action(description='Mark selected books as checked out')
def make_checked_out(modeladmin, request, queryset):
    updated = queryset.update(status=Book.STATUS_CHECKED_OUT)
    modeladmin.message_user(request, f"{updated} book(s) marked as checked out.", messages.SUCCESS)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_date', 'age_days_display')
    list_filter = ('status', 'published_date', 'author')
    search_fields = ('title', 'isbn')
    readonly_fields = ('created_at',)
    actions = [make_available, make_checked_out]
    list_per_page = 25

    fieldsets = (
        ('Main', {
            'fields': ('title', 'author', 'published_date')
        }),
        ('Metadata', {
            'fields': ('isbn', 'pages')
        }),
        ('Status & Info', {
            'fields': ('status', 'created_at')
        }),
    )

    def age_days_display(self, obj):
        days = obj.age_days()
        if days is None:
            return '-'
        if days < 30:
            return format_html('<span style="color:green">{} days</span>', days)
        return f"{days} days"

    age_days_display.short_description = 'Age (days)'
