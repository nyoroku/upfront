from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:slug>/module/<int:pk>/complete/', views.module_complete, name='module_complete'),
    path('<slug:slug>/quiz/<int:pk>/', views.quiz_start, name='quiz_start'),
    path('<slug:slug>/quiz/<int:pk>/submit/', views.quiz_submit, name='quiz_submit'),
]
