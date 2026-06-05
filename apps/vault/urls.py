from django.urls import path
from . import views

app_name = 'vault'

urlpatterns = [
    path('', views.vault_home, name='vault_home'),
    path('upload/', views.document_upload, name='document_upload'),
    path('document/<uuid:pk>/delete/', views.document_delete, name='document_delete'),
]
