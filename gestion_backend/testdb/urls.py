from django.urls import path
from .views import register, login, logout, MemberListCreateView, MemberDetailView, EmpruntListCreateView, EmpruntDetailView
from .views import BookListCreateView, BookDetailView
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    
    # Endpoints pour les membres
    path('membres/', MemberListCreateView.as_view(), name='member-list-create'),
    path('membres/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),

    # Endpoints pour les emprunts
    path('emprunts/', EmpruntListCreateView.as_view(), name='emprunt-list-create'),
    path('emprunts/<int:pk>/', EmpruntDetailView.as_view(), name='emprunt-detail'),
    
    # Endpoint pour rendre un emprunt
        
    # Endpoint pour rafraîchir le token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('books/', BookListCreateView.as_view(), name='book-list-create'),  
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
