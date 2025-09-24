from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.home, name="home"), 

    # Assignments
    
    path("assignments/add/", views.assignment_create, name="assignment_create"),
    
    path("assignments/<int:pk>/delete/", views.assignment_delete, name="assignment_delete"),
    path("assignments/<int:pk>/review/", views.mark_reviewed, name="mark_reviewed"),
   
    path("assignments/", views.assignment_list, name="assignment_list"),
    path("assignments/<int:pk>/edit/", views.assignment_update, name="assignment_update"),
    path("assignments/<int:pk>/", views.assignment_detail, name="assignment_detail"),

    path("submissions/<int:submission_id>/grade/", views.grade_submission, name="grade_submission"),
     
    # Dashboards
    path("redirect-dashboard/", views.redirect_dashboard, name="redirect_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("student/dashboard/", views.submit_assignment, name="submit_assignment"),
     
    # Auth
    path("register/", views.register, name="register"),
    path("accounts/logout/", views.user_logout, name="logout"),  # overrides built-in
         
    # Student-specific views    
    
    path("assignments/<int:assignment_id>/submit/", views.submit_assignment, name="submit_assignment"),
    path("results/", views.student_results, name="student_results"),
]


