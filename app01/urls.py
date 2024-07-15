from django.conf.urls import url, include
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^sendcode/', views.send_code),
    url(r'^register/', views.register, name='register'),
    ]