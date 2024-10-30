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

    path('sections/', views.create_section, name='create_section'),
    path('sections/all', views.read_section, name='create_section'),
    path('sections/<str:section_id>/', views.section, name='section'),

    path('contents/', views.create_content, name='create_content'),
    path('contents/all', views.read_content, name='create_content'),
    path('contents/<int:content_id>/', views.content, name='content'),
]
