from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/<slug:slug>/', views.payment_checkout, name='payment_checkout'),
    path('initiate/', views.payment_initiate, name='payment_initiate'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
    path('status/<uuid:pk>/', views.payment_status, name='payment_status'),
    path('status/<uuid:pk>/poll/', views.payment_status_poll, name='payment_status_poll'),
]
