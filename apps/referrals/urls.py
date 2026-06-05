from django.urls import path
from . import views

app_name = 'referrals'

urlpatterns = [
    path('signup/', views.affiliate_signup, name='affiliate_signup'),
    path('login/', views.affiliate_login, name='affiliate_login'),
    path('dashboard/', views.affiliate_dashboard, name='affiliate_dashboard'),
]
