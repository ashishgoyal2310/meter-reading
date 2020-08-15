from django.urls import path

from users import views

urlpatterns = [
    path('', views.users_index, name='users-index'),
    path(r'new/', views.user_create_view, name='users-new'),
]