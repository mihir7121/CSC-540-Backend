from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    
    path('textbooks/', views.create_textbook, name='create_textbook'),
    path('textbooks/all/', views.read_textbooks, name='read_textbooks'),
    path('textbooks/<int:textbook_id>/', views.textbook, name='textbook'),

    path('chapters/', views.create_chapter, name='create_chapter'),
    path('chapters/all/', views.read_chapter, name='create_chapter'),
    path('chapters/<str:chapter_name>/', views.chapter, name='chapter'),

    path('sections/', views.create_section, name='create_section'),
    path('sections/all/', views.read_section, name='create_section'),
    path('sections/<str:number>/', views.section, name='section'),

    path('contents/', views.create_content, name='create_content'),
    path('contents/all/', views.read_content, name='create_content'),
    path('contents/<str:content_name>/', views.content, name='content'),
    path('contents/<str:content_name>/text/', views.content_text, name='content_text'),
    path('contents/<str:content_name>/image/', views.content_image, name='content_image'),
    
    path('activities/', views.create_activity, name='create_activity'),
    path('activities/all/', views.read_activity, name='create_activity'),
    path('activities/<str:activity_number>/', views.activity, name='activity'),

    path('questions/', views.create_question, name='create_question'),
    path('questions/all/', views.read_questions, name='create_question'),
    path('questions/<int:question_id>/', views.question, name='question'),

    path('courses/', views.create_course, name='create_course'),      
    path('courses/all/', views.read_courses, name='read_courses'),  
    path('courses/<str:course_id>/', views.course, name='course'),  
    
    path('enroll/', views.enroll_in_course, name='enrollment'), #course enrollment
    path('courses/<str:course_id>/worklist/', views.course_worklist, name='course_worklist'), #view worklist
    path('courses/<str:course_id>/students/', views.course_students, name='course_students'), #view enrolled students      
    path('courses/<str:course_id>/update-enrollment/', views.update_enrollment_status, name='update_enrollment_status'), #update enrollment
    path('notifications/', views.view_notifications, name='view_notifications'), 
    
    path('createfaculty/', views.create_faculty, name='create_faculty'),
    path('createta/',views.create_ta,name='create_ta'), # create TA
    path('changepassword/',views.change_password,name="change_password"),
    path('students/all/',views.all_students,name="all_students"),
    path('students/home/',views.get_course_details,name='student_home'),
    path('students/submit_activity/',views.submit_activity,name="activity-points")
]