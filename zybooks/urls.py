from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('signup/', views.signup, name="logout"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('add_section/', views.add_section, name="addSection"),
    
    path('textbooks/', views.create_textbook, name='create_textbook'),
    path('textbooks/all/', views.read_textbooks, name='read_textbooks'),
    path('textbooks/<int:textbook_id>/', views.textbook, name='textbook'),

    path('chapters/', views.create_chapter, name='create_chapter'),
    path('chapters/all', views.read_chapter, name='create_chapter'),
    path('chapters/<int:chapter_id>/', views.chapter, name='chapter'),
]
