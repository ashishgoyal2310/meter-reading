from django.urls import path, re_path

from users import views

urlpatterns = [
    path('', views.users_index, name='users-index'),

    path('login/', views.users_login, name='users-login'),
    path('logout/', views.users_logout, name='users-logout'),

    re_path(r'^forgot-password/$', views.users_forgot_password, name='users-forgot-password'),
    re_path(r'^reset-password/(?P<token>[\w-]+)/$', views.users_reset_password, name='users-reset-password'),

    path(r'list/', views.user_list_view, name='users-list'),
    path(r'new/', views.user_create_view, name='users-new'),
]