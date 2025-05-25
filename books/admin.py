from django.contrib import admin
from .models import Book

@admin.register(Book) # This decorator is a concise way to register your model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'isbn_number')
    search_fields = ('title', 'author', 'isbn_number')
    list_filter = ('published_date',)