# books/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Book
from datetime import date
# --- Model Tests ---
class BookModelTest(TestCase):
    def test_book_creation(self):
        # Create a book instance
        book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            published_date=date(2023, 1, 1),  # Use the correct field
            isbn_number='9781234567890',
            genre='Fiction',
            summary='A test summary for the book.'
        )
        # Assert that the book was created and its attributes are correct
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.published_date, date(2023, 1, 1))  # Check if the date is correct
        self.assertEqual(book.isbn_number, '9781234567890')
        self.assertEqual(book.genre, 'Fiction')
        self.assertEqual(book.summary, 'A test summary for the book.')
        self.assertTrue(isinstance(book, Book))  # Check if it's an instance of Book model

    def test_book_str_method(self):
        book = Book.objects.create(
            title='Another Test Book',
            author='Jane Doe',
            published_date='2023-01-01',  # Required field
            isbn_number='9781234567891',
            genre='Non-Fiction',
            summary='Another test summary.'
        )
        self.assertEqual(str(book), 'Another Test Book')

# --- View Tests ---
class BookListViewTest(TestCase):
    def setUp(self):
        # Create some sample books for testing the list view
        Book.objects.create(
            title='Book A',
            author='Author X',
            published_date='2023-01-01',  # Required field
            isbn_number='9781234567892',
            genre='Fiction',
            summary='Summary for Book A.'
        )
        Book.objects.create(
            title='Book B',
            author='Author Y',
            published_date='2023-01-02',  # Required field
            isbn_number='9781234567893',
            genre='Non-Fiction',
            summary='Summary for Book B.'
        )

    def test_book_list_view_status_code(self):
        # Use reverse to get the URL for the book list view
        response = self.client.get(reverse('book_list'))
        # Assert that the page loads successfully (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)

    def test_book_list_view_uses_correct_template(self):
        response = self.client.get(reverse('book_list'))
        # Assert that the correct template is used to render the page
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_view_context(self):
        response = self.client.get(reverse('book_list'))
        # Assert that the context contains the 'books' object and it has the correct count
        self.assertIn('books', response.context)
        self.assertEqual(len(response.context['books']), 2)
        # You can also check specific book titles are in the response content
        self.assertContains(response, 'Book A')
        self.assertContains(response, 'Book B')

    def test_book_list_view_no_books(self):
        # Delete all existing books to test the empty state
        Book.objects.all().delete()
        response = self.client.get(reverse('book_list'))
        self.assertContains(response, 'No books in your collection yet.')
        self.assertEqual(len(response.context['books']), 0)