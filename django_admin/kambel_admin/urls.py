"""
URL configuration for Kambel Consult Admin Panel.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.conf import settings
import os
from . import views

def serve_html(request, page_name):
    """Serve HTML pages"""
    template_path = os.path.join(settings.BASE_DIR.parent.parent, f'{page_name}.html')
    
    if os.path.exists(template_path):
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HttpResponse(content, content_type='text/html')
        except Exception as e:
            return HttpResponse(f"Error loading page: {str(e)}", status=500)
    else:
        return HttpResponse(f"Page '{page_name}' not found", status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints for frontend integration
    path('api/publications/', views.PublicationsAPIView.as_view(), name='publications_api'),
    path('api/categories/', views.CategoriesAPIView.as_view(), name='categories_api'),
    path('api/consultancy/', views.ConsultancyAPIView.as_view(), name='consultancy_api'),
    path('api/blog/', views.BlogAPIView.as_view(), name='blog_api'),
    path('api/contact/', views.ContactAPIView.as_view(), name='contact_api'),
    path('api/newsletter/', views.NewsletterAPIView.as_view(), name='newsletter_api'),
    path('api/site/config/', views.SiteConfigAPIView.as_view(), name='site_config_api'),
    path('api/site/hero/', views.HeroConfigAPIView.as_view(), name='hero_config_api'),
    path('api/site/about/', views.AboutConfigAPIView.as_view(), name='about_config_api'),
    path('api/site/contact-info/', views.ContactInfoAPIView.as_view(), name='contact_info_api'),
    path('api/site/social-media/', views.SocialMediaAPIView.as_view(), name='social_media_api'),
    path('api/masterclasses/', views.MasterclassesAPIView.as_view(), name='masterclasses_api'),
    path('api/kict/courses/', views.KICTCoursesAPIView.as_view(), name='kict_courses_api'),
    path('api/site/seo/<str:page>/', views.SEOContentAPIView.as_view(), name='seo_content_api'),
    path('api/site/privacy-policy/', views.PrivacyPolicyAPIView.as_view(), name='privacy_policy_api'),
    path('api/site/terms-conditions/', views.TermsConditionsAPIView.as_view(), name='terms_conditions_api'),
    path('api/gallery/', views.GalleryAPIView.as_view(), name='gallery_api'),
    path('api/masterclass/register/', views.MasterclassRegistrationAPIView.as_view(), name='masterclass_register_api'),
    
    # Frontend pages
    path('', lambda request: serve_html(request, 'index'), name='home'),
    path('masterclass.html', lambda request: serve_html(request, 'masterclass')),
    path('masterclass', lambda request: serve_html(request, 'masterclass')),
    path('publications.html', lambda request: serve_html(request, 'publications')),
    path('publications', lambda request: serve_html(request, 'publications')),
    path('consultancy.html', lambda request: serve_html(request, 'consultancy-unified')),
    path('consultancy', lambda request: serve_html(request, 'consultancy-unified')),
    path('gallery.html', lambda request: serve_html(request, 'gallery')),
    path('gallery', lambda request: serve_html(request, 'gallery')),
    path('about.html', lambda request: serve_html(request, 'about')),
    path('about', lambda request: serve_html(request, 'about')),
    path('privacy-policy.html', lambda request: serve_html(request, 'privacy-policy')),
    path('privacy-policy', lambda request: serve_html(request, 'privacy-policy')),
    path('terms-conditions.html', lambda request: serve_html(request, 'terms-conditions')),
    path('terms-conditions', lambda request: serve_html(request, 'terms-conditions')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
