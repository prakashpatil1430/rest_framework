from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('students/', views.student_list),
    path('students/<int:pk>/', views.student_details),
    
    path('teachers/', views.teacher_list),
    path('teachers/<int:pk>/', views.teacher_details),
    
    # apiview class
    path('student_view/', views.StudentView.as_view()),
    path('student_view/<int:pk>/', views.StudentView.as_view())
]
