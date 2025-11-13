from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),

    # Admin
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Course
    path('course/', views.course, name='course'),
    path('add_course/', views.add_course, name='add_course'),

    # Student
    path('student/', views.student, name='student'),
    path('add_student/', views.add_student, name='add_student'),
    path('show_details/', views.show_details, name='show_details'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),

    # Teacher
    path('teacher/signup/', views.teacher_signup, name='teacher_signup'),
    path('teachers/', views.show_teachers, name='show_teachers'),
    path('edit_teacher/<int:id>/', views.edit_teacher, name='edit_teacher'),
    path('delete_teacher/<int:id>/', views.delete_teacher, name='delete_teacher'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # Authentication
    path('loginfun/', views.loginfun, name='loginfun'),
     path('logout_fun', views.logout_fun, name='logout_fun'),
]
