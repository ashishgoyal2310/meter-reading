from django.urls import path

from users import views

urlpatterns = [
    path('', views.users_index, name='users-index'),

    path('login/', views.users_login, name='users-login'),
    path('logout/', views.users_logout, name='users-logout'),

    path('forgot-password/', views.users_forgot_password, name='users-forgot-password'),

    path(r'list/', views.user_list_view, name='users-list'),
    path(r'new/', views.user_create_view, name='users-new'),
]