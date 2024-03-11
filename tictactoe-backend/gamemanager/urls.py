from django.urls import path
from . import views

urlpatterns = [
    path('register_for_game/<str:username>/', views.RegisterForGame.as_view(), name='register_for_game')
]