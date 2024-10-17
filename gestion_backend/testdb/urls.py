from django.urls import path
from .views import register, login, logout
from .views import BookListCreateView, BookDetailView
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),  
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )