# books/views.py
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Book
from .forms import BookForm

# List all books
class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html' # Path to your template
    context_object_name = 'books' # The name of the list object used in the template context

# Display details of a single book
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html' # Path to your template
    context_object_name = 'book' # The name of the single object used in the template context

# Create a new book
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm # Use the form we just created
    template_name = 'books/book_form.html' # This template will be used for both create and update
    success_url = reverse_lazy('book_list') # Redirect here after successful creation
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    def form_valid(self, form):
        return super().form_valid(form)


# Update an existing book
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list') # Redirect here after successful update

# Delete a book
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html' # Confirmation page for deletion
    success_url = reverse_lazy('book_list') # Redirect here after successful deletion