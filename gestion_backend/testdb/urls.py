from django.urls import path
from .views import register, login, logout, MemberListCreateView, MemberDetailView, LivreListCreateView, LivreDetailView, EmpruntListCreateView, EmpruntDetailView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    
    # Cheikh Gueye : Endpoints pour les membres
    path('membres/', MemberListCreateView.as_view(), name='member-list-create'),
    path('membres/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),

    # Cheikh Gueye : Endpoints pour les livres
    path('livres/', LivreListCreateView.as_view(), name='livre-list-create'),
    path('livres/<int:pk>/', LivreDetailView.as_view(), name='livre-detail'),

    # Cheikh Gueye : Endpoints pour les emprunts
    path('emprunts/', EmpruntListCreateView.as_view(), name='emprunt-list-create'),
    path('emprunts/<int:pk>/', EmpruntDetailView.as_view(), name='emprunt-detail'),
    
    # Cheikh Gueue : Endpoint pour rafraichir le token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]