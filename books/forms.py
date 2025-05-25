# books/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn_number']
        labels = {
            'title': 'Book Title',
            'author': 'Author Name',
            'published_date': 'Year Published',
            'isbn_number': 'ISBN (optional)'
        }
        widgets = {
            'published_date': forms.DateInput(attrs={'placeholder': 'e.g., 2023'}),
            'isbn_number': forms.TextInput(attrs={'placeholder': 'e.g., 978-0321765723'})
        }