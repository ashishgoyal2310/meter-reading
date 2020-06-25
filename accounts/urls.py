from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send_json/', views.send_json, name='send_json'),
    path('login_request/',views.login_request, name='login_request'),
    path('register/',views.register, name='register'),
    path('myprofile/',views.myprofile, name='myprofile'),
]