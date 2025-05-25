# books/urls.py
from django.urls import path
from . import views # Import your views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'), # books/
    path('new/', views.BookCreateView.as_view(), name='book_new'), # books/new/
    path('<int:pk>/', views.BookDetailView.as_view(), name='book_detail'), # books/1/, books/2/ etc.
    path('<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'), # books/1/edit/
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'), # books/1/delete/
]