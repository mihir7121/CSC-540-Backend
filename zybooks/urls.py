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
    path('chapters/all/', views.read_chapter, name='create_chapter'),
    path('chapters/<int:chapter_id>/', views.chapter, name='chapter'),

    path('sections/', views.create_section, name='create_section'),
    path('sections/all/', views.read_section, name='create_section'),
    path('sections/<str:section_id>/', views.section, name='section'),

    path('contents/', views.create_content, name='create_content'),
    path('contents/all/', views.read_content, name='create_content'),
    path('contents/<int:content_id>/', views.content, name='content'),
    path('contents/<int:content_id>/text/', views.content_text, name='content_text'),
    path('contents/<int:content_id>/image/', views.content_image, name='content_image'),
    
    path('activities/', views.create_activity, name='create_activity'),
    path('activities/all/', views.read_activity, name='create_activity'),
    path('activities/<int:activity_id>/', views.activity, name='activity'),

    path('questions/', views.create_question, name='create_question'),
    path('questions/all/', views.read_questions, name='create_question'),
    path('questions/<int:question_id>/', views.question, name='question'),

    path('courses/', views.read_courses, name='get-all-courses'),      
    path('courses/<int:course_id>/', views.get_course_by_id, name='get-course-by-id'),  
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete-course'),  
    path('courses/create/', views.create_course, name='create-course'),
    path('courses/<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'), #course enrollment
    path('courses/<int:course_id>/worklist/', views.course_worklist, name='course_worklist'), #view worklist
    path('courses/<int:course_id>/students/', views.course_students, name='course_students'), #view enrolled students      
    path('courses/<int:course_id>/update-enrollment/', views.update_enrollment_status, name='update_enrollment_status'), #update enrollment
    
    path('createta/',views.create_ta,name='create-ta'), # create TA
    path('changepassword/',views.change_password,name="change-password"),
    path('students/all/',views.all_students,name="all-students")
]