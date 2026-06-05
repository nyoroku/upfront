from django.urls import path
from . import views

app_name = 'partners'

urlpatterns = [
    path('', views.partner_dashboard, name='partner_dashboard'),
    path('verify/<uuid:doc_pk>/', views.verify_document, name='verify_document'),
]
