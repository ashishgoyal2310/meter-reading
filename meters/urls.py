from django.urls import path

from meters import views

urlpatterns = [
    path('register/', views.register, name='register'),
]