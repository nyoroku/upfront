from django.urls import path
from . import views

app_name = 'seo'

urlpatterns = [
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('faqs/', views.faq_list, name='faq_list'),
    path('destinations/', views.local_page_list, name='local_page_list'),
    path('destinations/<str:destination>/', views.local_page_list_by_destination, name='local_page_list_by_destination'),
    path('destinations/page/<slug:slug>/', views.local_page_detail, name='local_page_detail'),
]
