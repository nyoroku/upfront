from django.urls import path
from . import views

app_name = 'lanes'

urlpatterns = [
    path('', views.lane_dashboard, name='lane_dashboard'),
    path('milestone/<slug:slug>/', views.milestone_detail, name='milestone_detail'),
    path('milestone/<slug:slug>/status/', views.milestone_status, name='milestone_status'),
]
