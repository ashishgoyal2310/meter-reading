from django.urls import path

from meters import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('all_meters/', views.all_meters, name='all_meters'),
    path('info/<int:pid>/', views.info, name='info'),
]