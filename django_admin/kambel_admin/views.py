"""
API views for Kambel Consult frontend integration
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views import View
import json
from .models import (
    Category, Book, ConsultancyService, ServiceFeature,
    BlogPost, ContactMessage, NewsletterSubscription, SiteConfig, HeroConfig, AboutConfig,
    ProfessionalJourneyItem, EducationQualification, Achievement, SpeakingEngagement,
    Masterclass, SocialMediaLink, PrivacyPolicy, TermsConditions, GalleryItem, MasterclassRegistration
)


class PublicationsAPIView(View):
    """API endpoint for publications"""
    
    def get(self, request):
        books = Book.objects.filter(is_active=True)
        publications = []
        
        for book in books:
            cover_image_url = None
            if book.cover_image:
                # Build absolute URL for media files
                cover_image_url = request.build_absolute_uri(book.cover_image.url)
            
            publication = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'description': book.description,
                'pages': book.pages,
                'price': float(book.price),
                'cover_image_url': cover_image_url,
                'purchase_link': book.purchase_link,
                'category': book.category.name if book.category else None
            }
            publications.append(publication)
        
        return JsonResponse(publications, safe=False)


class CategoriesAPIView(View):
    """API endpoint for categories"""
    
    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        categories_data = []
        
        for category in categories:
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description
            })
        
        return JsonResponse(categories_data, safe=False)


class ConsultancyAPIView(View):
    """API endpoint for consultancy services"""
    
    def get(self, request):
        services = ConsultancyService.objects.filter(is_active=True).order_by('order')
        consultancy_data = []
        
        for service in services:
            cover_image_url = None
            if service.cover_image:
                # Build absolute URL for media files
                cover_image_url = request.build_absolute_uri(service.cover_image.url)
            
            service_data = {
                'id': service.id,
                'name': service.name,
                'service_type': service.service_type,
                'description': service.description,
                'cover_image_url': cover_image_url,
                'icon': service.icon,
                'features': []
            }
            
            for feature in service.features.filter(is_active=True).order_by('order'):
                service_data['features'].append({
                    'id': feature.id,
                    'title': feature.title,
                    'description': feature.description,
                    'icon': feature.icon
                })
            
            consultancy_data.append(service_data)
        
        return JsonResponse(consultancy_data, safe=False)


class BlogAPIView(View):
    """API endpoint for blog posts"""
    
    def get(self, request):
        posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
        blog_data = []
        
        for post in posts:
            cover_image_url = None
            if post.cover_image:
                # Build absolute URL for media files
                cover_image_url = request.build_absolute_uri(post.cover_image.url)
            
            blog_data.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'excerpt': post.excerpt,
                'author': post.author,
                'date': post.created_at.strftime('%B %d, %Y'),
                'cover_image_url': cover_image_url
            })
        
        return JsonResponse(blog_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class ContactAPIView(View):
    """API endpoint for contact form"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            contact = ContactMessage(
                name=data.get('name', ''),
                email=data.get('email', ''),
                subject=data.get('subject', ''),
                message=data.get('message', '')
            )
            contact.save()
            
            return JsonResponse({'message': 'Contact message submitted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class NewsletterAPIView(View):
    """API endpoint for newsletter subscription"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)
            
            # Check if email already exists
            existing = NewsletterSubscription.objects.filter(email=email).first()
            if existing:
                if existing.is_active:
                    return JsonResponse({'message': 'Email is already subscribed'})
                else:
                    existing.is_active = True
                    existing.save()
                    return JsonResponse({'message': 'Email resubscribed successfully'})
            
            subscription = NewsletterSubscription(email=email)
            subscription.save()
            
            return JsonResponse({'message': 'Successfully subscribed to newsletter'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class SiteConfigAPIView(View):
    """API endpoint for site configuration"""
    
    def get(self, request):
        config = SiteConfig.objects.first()
        if not config:
            # Return default configuration
            return JsonResponse({
                'site_name': 'Kambel Consult',
                'tagline': 'Professional Consulting and Training Services',
                'contact_email': 'info@kambelconsult.com',
                'contact_phone': '+1 (555) 123-4567',
                'address': '123 Business Street, City, State 12345',
                'logo_url': None,
                'favicon_url': None
            })
        
        logo_url = None
        if config.logo:
            logo_url = request.build_absolute_uri(config.logo.url)
        
        favicon_url = None
        if config.favicon:
            favicon_url = request.build_absolute_uri(config.favicon.url)
        
        return JsonResponse({
            'site_name': config.site_name,
            'tagline': config.tagline,
            'contact_email': config.contact_email,
            'contact_phone': config.contact_phone,
            'address': config.address,
            'logo_url': logo_url,
            'favicon_url': favicon_url
        })


class ContactInfoAPIView(View):
    """API endpoint for contact information"""
    
    def get(self, request):
        config = SiteConfig.objects.first()
        if not config:
            return JsonResponse([
                {'type': 'email', 'value': 'info@kambelconsult.com', 'icon': 'fas fa-envelope'},
                {'type': 'phone', 'value': '+1 (555) 123-4567', 'icon': 'fas fa-phone'},
                {'type': 'address', 'value': '123 Business Street, City, State 12345', 'icon': 'fas fa-map-marker-alt'},
                {'type': 'location', 'value': 'City, State 12345', 'icon': 'fas fa-map-pin'}
            ], safe=False)
        
        contact_info = []
        if config.contact_email:
            contact_info.append({'type': 'email', 'value': config.contact_email, 'icon': 'fas fa-envelope'})
        if config.contact_phone:
            contact_info.append({'type': 'phone', 'value': config.contact_phone, 'icon': 'fas fa-phone'})
        if config.address:
            contact_info.append({'type': 'address', 'value': config.address, 'icon': 'fas fa-map-marker-alt'})
        if config.location:
            contact_info.append({'type': 'location', 'value': config.location, 'icon': 'fas fa-map-pin'})
        
        return JsonResponse(contact_info, safe=False)


class SocialMediaAPIView(View):
    """API endpoint for social media links"""
    
    def get(self, request):
        # Get active social media links from database
        links = SocialMediaLink.objects.filter(is_active=True).order_by('order')
        
        social_data = []
        for link in links:
            social_data.append({
                'platform': link.platform,
                'url': link.url,
                'icon_class': link.get_icon_class(),
                'order': link.order
            })
        
        # If no links in database, return empty array (frontend will handle gracefully)
        return JsonResponse(social_data, safe=False)


class HeroConfigAPIView(View):
    """API endpoint for hero configuration"""
    
    def get(self, request):
        # Get active hero configuration
        hero_config = HeroConfig.objects.filter(is_active=True).first()
        
        if not hero_config:
            # Return default values if no config exists
            return JsonResponse({
                'hero_title': 'Welcome to Kambel Consult',
                'hero_subtitle': 'Your trusted partner in career development and business excellence',
                'profile_name': 'Moses Agbesi Katamani',
                'profile_title': 'Chief Executive Officer',
                'profile_picture_url': None,
                'years_experience': '15+',
                'years_label': 'Years Experience',
                'years_description': 'Professional Development',
                'clients_count': '5000+',
                'clients_label': 'Clients',
                'clients_description': 'Successfully Helped',
                'publications_count': '50+',
                'publications_label': 'Publications',
                'publications_description': 'Authored Works'
            })
        
        # Build absolute URL for profile picture
        profile_picture_url = None
        if hero_config.profile_picture:
            profile_picture_url = request.build_absolute_uri(hero_config.profile_picture.url)
        
        return JsonResponse({
            'hero_title': hero_config.hero_title,
            'hero_subtitle': hero_config.hero_subtitle,
            'profile_name': hero_config.profile_name,
            'profile_title': hero_config.profile_title,
            'profile_picture_url': profile_picture_url,
            'years_experience': hero_config.years_experience,
            'years_label': hero_config.years_label,
            'years_description': hero_config.years_description,
            'clients_count': hero_config.clients_count,
            'clients_label': hero_config.clients_label,
            'clients_description': hero_config.clients_description,
            'publications_count': hero_config.publications_count,
            'publications_label': hero_config.publications_label,
            'publications_description': hero_config.publications_description
        })


class AboutConfigAPIView(View):
    """API endpoint for about page configuration"""
    
    def get(self, request):
        # Get active about configuration
        about_config = AboutConfig.objects.filter(is_active=True).first()
        
        if not about_config:
            # Return default values if no config exists
            return JsonResponse({
                'hero_years': '15+',
                'hero_clients': '500+',
                'hero_publications': '50+',
                'hero_speaking': '100+',
                'profile_name': 'Moses Agbesi Katamani',
                'profile_title': 'Founder & CEO, Kambel Consult',
                'profile_picture_url': None,
                'bio_summary': 'A visionary leader and expert consultant with over 15 years of experience in education, career development, and business advisory services.',
                'tags': ['Education Expert', 'Career Coach', 'Business Advisor', 'Author', 'Speaker'],
                'philosophy_quote': 'Education is the foundation of all progress. Through knowledge, guidance, and strategic thinking, we can unlock the potential within every individual and organization.',
                'cta_title': 'Ready to Work Together?',
                'cta_description': "Let's discuss how I can help you achieve your goals and unlock your potential.",
                'journey': [],
                'education': [],
                'achievements': [],
                'speaking': []
            })
        
        # Build absolute URL for profile picture
        profile_picture_url = None
        if about_config.profile_picture:
            profile_picture_url = request.build_absolute_uri(about_config.profile_picture.url)
        
        # Parse tags
        tags = [tag.strip() for tag in about_config.tags.split(',') if tag.strip()]
        
        # Get journey items
        journey_items = about_config.journey_items.filter(is_active=True).order_by('order')
        journey = []
        for item in journey_items:
            journey.append({
                'title': item.title,
                'organization': item.organization,
                'period': item.period,
                'description': item.description,
                'icon': item.icon
            })
        
        # Get education items
        education_items = about_config.education_items.filter(is_active=True).order_by('order')
        education = []
        for item in education_items:
            education.append({
                'qualification': item.qualification,
                'institution': item.institution,
                'year': item.year,
                'icon': item.icon
            })
        
        # Get achievements
        achievements_items = about_config.achievements.filter(is_active=True).order_by('order')
        achievements = []
        for item in achievements_items:
            achievements.append({
                'title': item.title,
                'description': item.description,
                'year': item.year,
                'icon': item.icon
            })
        
        # Get speaking engagements
        speaking_items = about_config.speaking_engagements.filter(is_active=True).order_by('order')
        speaking = []
        for item in speaking_items:
            speaking.append({
                'title': item.title,
                'event': item.event,
                'date': item.date,
                'location': item.location
            })
        
        return JsonResponse({
            'hero_years': about_config.hero_years,
            'hero_clients': about_config.hero_clients,
            'hero_publications': about_config.hero_publications,
            'hero_speaking': about_config.hero_speaking,
            'profile_name': about_config.profile_name,
            'profile_title': about_config.profile_title,
            'profile_picture_url': profile_picture_url,
            'bio_summary': about_config.bio_summary,
            'tags': tags,
            'philosophy_quote': about_config.philosophy_quote,
            'cta_title': about_config.cta_title,
            'cta_description': about_config.cta_description,
            'journey': journey,
            'education': education,
            'achievements': achievements,
            'speaking': speaking
        })


class MasterclassesAPIView(View):
    """API endpoint for masterclasses"""
    
    def get(self, request):
        # Get upcoming masterclasses from database
        upcoming_masterclasses = Masterclass.objects.filter(is_upcoming=True, is_active=True).order_by('date')
        
        # Get previous (completed) masterclasses
        previous_masterclasses = Masterclass.objects.filter(is_upcoming=False, is_active=True).order_by('-date')
        
        def format_masterclass(mc):
            """Helper function to format masterclass data"""
            cover_image_url = None
            if mc.cover_image:
                # Build absolute URL for media files
                cover_image_url = request.build_absolute_uri(mc.cover_image.url)
            elif mc.video_url:
                # Generate YouTube thumbnail automatically if no cover image
                if 'youtube.com' in mc.video_url or 'youtu.be' in mc.video_url:
                    # Extract video ID
                    if 'youtu.be' in mc.video_url:
                        video_id = mc.video_url.split('/')[-1].split('?')[0]
                    else:
                        video_id = mc.video_url.split('v=')[-1].split('&')[0]
                    if video_id:
                        cover_image_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
            
            return {
                'id': mc.id,
                'title': mc.title,
                'description': mc.description,
                'date': mc.date.strftime('%Y-%m-%d'),
                'instructor': mc.instructor,
                'duration': mc.duration,
                'price': float(mc.price) if mc.price else 0.00,
                'total_seats': mc.total_seats,
                'seats_available': mc.seats_available,
                'cover_image_url': cover_image_url,
                'video_url': mc.video_url
            }
        
        upcoming = [format_masterclass(mc) for mc in upcoming_masterclasses]
        previous = [format_masterclass(mc) for mc in previous_masterclasses]
        
        return JsonResponse({
            'upcoming': upcoming,
            'previous': previous
        })


class KICTCoursesAPIView(View):
    """API endpoint for KICT courses"""
    
    def get(self, request):
        # Return empty array - no courses to display
        return JsonResponse([], safe=False)


class PrivacyPolicyAPIView(View):
    """API endpoint for privacy policy"""
    
    def get(self, request):
        policy = PrivacyPolicy.objects.filter(is_active=True).first()
        if not policy:
            return JsonResponse({
                'title': 'Privacy Policy',
                'subtitle': 'Your privacy is important to us. This policy explains how we collect, use, and protect your information.',
                'content': '<p>Privacy policy content will be available soon.</p>',
                'last_updated': None
            })
        
        return JsonResponse({
            'title': policy.title,
            'subtitle': policy.subtitle,
            'content': policy.content,
            'last_updated': policy.last_updated.strftime('%Y-%m-%d') if policy.last_updated else None
        })


class TermsConditionsAPIView(View):
    """API endpoint for terms & conditions"""
    
    def get(self, request):
        terms = TermsConditions.objects.filter(is_active=True).first()
        if not terms:
            return JsonResponse({
                'title': 'Terms & Conditions',
                'subtitle': 'Please read these terms and conditions carefully before using our services.',
                'content': '<p>Terms and conditions content will be available soon.</p>',
                'last_updated': None
            })
        
        return JsonResponse({
            'title': terms.title,
            'subtitle': terms.subtitle,
            'content': terms.content,
            'last_updated': terms.last_updated.strftime('%Y-%m-%d') if terms.last_updated else None
        })


class GalleryAPIView(View):
    """API endpoint for gallery items"""
    
    def get(self, request):
        featured_only = request.GET.get('featured', '').lower() == 'true'
        
        gallery_items = GalleryItem.objects.filter(is_active=True)
        if featured_only:
            gallery_items = gallery_items.filter(is_featured=True)
        
        items = []
        for item in gallery_items:
            media_url = None
            thumbnail_url = None
            
            if item.media_type == 'image' and item.image:
                media_url = request.build_absolute_uri(item.image.url)
                thumbnail_url = request.build_absolute_uri(item.image.url)
            elif item.media_type == 'video':
                if item.video_url:
                    media_url = item.video_url
                elif item.video_file:
                    media_url = request.build_absolute_uri(item.video_file.url)
                
                if item.thumbnail:
                    thumbnail_url = request.build_absolute_uri(item.thumbnail.url)
                elif item.video_url:
                    # Generate YouTube thumbnail automatically
                    if 'youtube.com' in item.video_url or 'youtu.be' in item.video_url:
                        # Extract video ID
                        if 'youtu.be' in item.video_url:
                            video_id = item.video_url.split('/')[-1].split('?')[0]
                        else:
                            video_id = item.video_url.split('v=')[-1].split('&')[0]
                        if video_id:
                            thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
            
            items.append({
                'id': item.id,
                'title': item.title,
                'caption': item.caption,
                'description': item.description,
                'media_type': item.media_type,
                'media_url': media_url,
                'thumbnail_url': thumbnail_url,
                'is_featured': item.is_featured,
                'order': item.order,
                'created_at': item.created_at.strftime('%Y-%m-%d') if item.created_at else None
            })
        
        return JsonResponse(items, safe=False)


class MasterclassRegistrationAPIView(View):
    """API endpoint for masterclass registration"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Get masterclass if ID provided
            masterclass = None
            masterclass_title = data.get('masterclass_title', '')
            
            if data.get('masterclass_id'):
                try:
                    masterclass = Masterclass.objects.get(id=data.get('masterclass_id'), is_active=True)
                    masterclass_title = masterclass.title
                except Masterclass.DoesNotExist:
                    pass
            
            # Create registration
            registration = MasterclassRegistration.objects.create(
                masterclass=masterclass,
                masterclass_title=masterclass_title,
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                email=data.get('email', ''),
                phone=data.get('phone', ''),
                company=data.get('company', ''),
                experience_years=data.get('experience_years', ''),
                motivation=data.get('motivation', ''),
                subscribe_newsletter=data.get('subscribe_newsletter', False),
                status='pending'
            )
            
            # Update seats available if masterclass is linked
            if masterclass and masterclass.seats_available > 0:
                masterclass.seats_available -= 1
                masterclass.save()
            
            # Subscribe to newsletter if requested
            if data.get('subscribe_newsletter'):
                NewsletterSubscription.objects.get_or_create(
                    email=data.get('email'),
                    defaults={'subscribed_at': timezone.now()}
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Registration submitted successfully! We\'ll contact you soon with further details.',
                'registration_id': registration.id
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error submitting registration: {str(e)}'
            }, status=400)


class SEOContentAPIView(View):
    """API endpoint for SEO content"""
    
    def get(self, request, page):
        # Return default SEO content
        return JsonResponse({
            'page': page,
            'title': f'Kambel Consult - {page.title()}',
            'meta_description': 'Professional consulting and training services',
            'meta_keywords': 'consulting, training, career development, business strategy',
            'og_title': f'Kambel Consult - {page.title()}',
            'og_description': 'Professional consulting and training services',
            'og_image_url': None
        })
