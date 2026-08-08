from django.urls import path
from . import views

urlpatterns = [

    # College Home Page
    path('', views.index, name='index'),

    # Student Feedback Form
    path('feedback/', views.home, name='home'),

    # Admin Login
    path('admin-login/', views.admin_login, name='admin_login'),

    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Mark Feedback as Addressed
    path(
        'mark-addressed/<int:feedback_id>/',
        views.mark_addressed,
        name='mark_addressed'
    ),

    # Delete Feedback
    path(
        'delete-feedback/<int:feedback_id>/',
        views.delete_feedback,
        name='delete_feedback'
    ),

    # Admin Logout
    path('admin-logout/', views.admin_logout, name='admin_logout'),

]