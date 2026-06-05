"""
Root URL configuration for Worklane project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from apps.seo import views as app_views
from apps.referrals.views import referral_redirect

admin.site.site_header = "Upfront Administration"
admin.site.site_title = "Upfront Admin Portal"
admin.site.index_title = "Welcome to the Upfront Management Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', include('apps.lanes.urls', namespace='lanes')),
    path('courses/', include('apps.courses.urls', namespace='courses')),
    path('vault/', include('apps.vault.urls', namespace='vault')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('partners/', include('apps.partners.urls', namespace='partners')),
    path('tinymce/', include('tinymce.urls')),
    path('affiliates/', include('apps.referrals.urls', namespace='referrals')),
    path('ref/<str:code>/', referral_redirect, name='referral_redirect'),
    path('', include('apps.seo.urls', namespace='seo')),
    path('', app_views.home_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
