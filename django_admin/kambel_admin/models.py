"""
Models for Kambel Consult Admin Panel
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """Publication categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Books/Publications"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120, default="Moses Agbesi Katamani")
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    pages = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    cover_image = models.ImageField(upload_to='publications/covers/', blank=True, null=True)
    purchase_link = models.URLField(blank=True, null=True, help_text="Link to external bookstore (Amazon, etc.)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class ConsultancyService(models.Model):
    """Consultancy services"""
    SERVICE_TYPES = [
        ('career', 'Career Development'),
        ('business', 'Business Consulting'),
        ('personal', 'Personal Development'),
        ('education', 'Education & Training'),
    ]
    
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=100, choices=SERVICE_TYPES)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='consultancy/covers/', blank=True, null=True, help_text="Upload a cover image for this consultancy service")
    icon = models.CharField(max_length=100, default='fas fa-briefcase')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class ServiceFeature(models.Model):
    """Features for consultancy services"""
    service = models.ForeignKey(ConsultancyService, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='fas fa-star')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return f"{self.service.name} - {self.title}"


class BlogPost(models.Model):
    """Blog posts"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    author = models.CharField(max_length=100, default="Kambel Team")
    cover_image = models.ImageField(upload_to='blog/covers/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"


class NewsletterSubscription(models.Model):
    """Newsletter subscriptions"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


class SiteConfig(models.Model):
    """Site configuration"""
    site_name = models.CharField(max_length=100, default="Kambel Consult")
    tagline = models.CharField(max_length=200, default="Professional Consulting and Training Services")
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True, help_text="Full street address")
    location = models.CharField(max_length=200, blank=True, help_text="City, State/Country")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
    
    def __str__(self):
        return self.site_name


class HeroConfig(models.Model):
    """Hero section configuration"""
    hero_title = models.CharField(max_length=200, default="Welcome to Kambel Consult")
    hero_subtitle = models.TextField(default="Your trusted partner in career development and business excellence")
    
    # Profile Information
    profile_name = models.CharField(max_length=100, default="Moses Agbesi Katamani")
    profile_title = models.CharField(max_length=100, default="Chief Executive Officer")
    profile_picture = models.ImageField(upload_to='hero/', blank=True, null=True, help_text="CEO Profile Picture")
    
    # Credentials/Stats
    years_experience = models.CharField(max_length=50, default="15+", help_text="e.g., '15+' or '15 Years'")
    years_label = models.CharField(max_length=100, default="Years Experience", help_text="Label for years")
    years_description = models.CharField(max_length=100, default="Professional Development")
    
    clients_count = models.CharField(max_length=50, default="5000+", help_text="e.g., '5000+' or '5000'")
    clients_label = models.CharField(max_length=100, default="Clients", help_text="Label for clients")
    clients_description = models.CharField(max_length=100, default="Successfully Helped")
    
    publications_count = models.CharField(max_length=50, default="50+", help_text="e.g., '50+' or '50'")
    publications_label = models.CharField(max_length=100, default="Publications", help_text="Label for publications")
    publications_description = models.CharField(max_length=100, default="Authored Works")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hero Configuration"
        verbose_name_plural = "Hero Configuration"
    
    def __str__(self):
        return f"Hero Config - {self.hero_title}"


class AboutConfig(models.Model):
    """About page configuration"""
    # Hero Section Stats
    hero_years = models.CharField(max_length=50, default="15+", help_text="Years of experience (e.g., '15+')")
    hero_clients = models.CharField(max_length=50, default="500+", help_text="Clients served (e.g., '500+')")
    hero_publications = models.CharField(max_length=50, default="50+", help_text="Publications count (e.g., '50+')")
    hero_speaking = models.CharField(max_length=50, default="100+", help_text="Speaking engagements (e.g., '100+')")
    
    # Profile Section
    profile_name = models.CharField(max_length=100, default="Moses Agbesi Katamani")
    profile_title = models.CharField(max_length=100, default="Founder & CEO, Kambel Consult")
    profile_picture = models.ImageField(upload_to='about/', blank=True, null=True, help_text="Profile picture for about page")
    bio_summary = models.TextField(default="A visionary leader and expert consultant with over 15 years of experience in education, career development, and business advisory services. Moses is dedicated to empowering individuals and organizations to achieve their full potential through strategic guidance and innovative solutions.")
    
    # Tags/Badges
    tags = models.CharField(max_length=500, default="Education Expert,Career Coach,Business Advisor,Author,Speaker", help_text="Comma-separated tags (e.g., 'Education Expert,Career Coach')")
    
    # Philosophy
    philosophy_quote = models.TextField(default="Education is the foundation of all progress. Through knowledge, guidance, and strategic thinking, we can unlock the potential within every individual and organization.")
    
    # CTA Section
    cta_title = models.CharField(max_length=200, default="Ready to Work Together?")
    cta_description = models.TextField(default="Let's discuss how I can help you achieve your goals and unlock your potential.")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About Page Configuration"
        verbose_name_plural = "About Page Configuration"
    
    def __str__(self):
        return f"About Config - {self.profile_name}"


class ProfessionalJourneyItem(models.Model):
    """Professional journey timeline items"""
    about_config = models.ForeignKey(AboutConfig, on_delete=models.CASCADE, related_name='journey_items')
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    period = models.CharField(max_length=100, help_text="e.g., '2010-2015' or '2020 - Present'")
    description = models.TextField()
    icon = models.CharField(max_length=50, default="briefcase", help_text="Font Awesome icon name (without 'fa-' prefix)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Professional Journey Item"
        verbose_name_plural = "Professional Journey Items"
    
    def __str__(self):
        return f"{self.title} at {self.organization}"


class EducationQualification(models.Model):
    """Education and qualifications"""
    about_config = models.ForeignKey(AboutConfig, on_delete=models.CASCADE, related_name='education_items')
    qualification = models.CharField(max_length=200, help_text="e.g., 'Bachelor of Science in Business Administration'")
    institution = models.CharField(max_length=200)
    year = models.CharField(max_length=50, help_text="e.g., '2010' or '2010-2014'")
    icon = models.CharField(max_length=50, default="graduation-cap", help_text="Font Awesome icon name")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Education & Qualification"
        verbose_name_plural = "Education & Qualifications"
    
    def __str__(self):
        return f"{self.qualification} - {self.institution}"


class Achievement(models.Model):
    """Achievements and recognition"""
    about_config = models.ForeignKey(AboutConfig, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.CharField(max_length=50, help_text="e.g., '2020' or '2020-2021'")
    icon = models.CharField(max_length=50, default="trophy", help_text="Font Awesome icon name")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
    
    def __str__(self):
        return f"{self.title} ({self.year})"


class SpeakingEngagement(models.Model):
    """Speaking engagements"""
    about_config = models.ForeignKey(AboutConfig, on_delete=models.CASCADE, related_name='speaking_engagements')
    title = models.CharField(max_length=200, help_text="Topic or title of the speaking engagement")
    event = models.CharField(max_length=200, help_text="Event or conference name")
    date = models.CharField(max_length=100, help_text="e.g., 'March 2020' or '2020-03-15'")
    location = models.CharField(max_length=200, blank=True, help_text="Location of the event")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Speaking Engagement"
        verbose_name_plural = "Speaking Engagements"
    
    def __str__(self):
        return f"{self.title} - {self.event}"


class PrivacyPolicy(models.Model):
    """Privacy Policy content"""
    title = models.CharField(max_length=200, default="Privacy Policy")
    subtitle = models.CharField(max_length=300, default="Your privacy is important to us. This policy explains how we collect, use, and protect your information.")
    content = models.TextField(help_text="Main content of the privacy policy. Use HTML tags for formatting.")
    last_updated = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Privacy Policy"
        verbose_name_plural = "Privacy Policy"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Only allow one active privacy policy
        if self.is_active:
            qs = PrivacyPolicy.objects.filter(is_active=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(is_active=False)
        super().save(*args, **kwargs)


class TermsConditions(models.Model):
    """Terms & Conditions content"""
    title = models.CharField(max_length=200, default="Terms & Conditions")
    subtitle = models.CharField(max_length=300, default="Please read these terms and conditions carefully before using our services.")
    content = models.TextField(help_text="Main content of the terms and conditions. Use HTML tags for formatting.")
    last_updated = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Terms & Conditions"
        verbose_name_plural = "Terms & Conditions"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Only allow one active terms & conditions
        if self.is_active:
            qs = TermsConditions.objects.filter(is_active=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(is_active=False)
        super().save(*args, **kwargs)


class Masterclass(models.Model):
    """Masterclasses and training workshops"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100, default="Moses Agbesi Katamani")
    date = models.DateField(help_text="Masterclass date")
    duration = models.CharField(max_length=50, help_text="e.g., '1 Day', '2 Days', '3 Hours'")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Registration price (0.00 for free)")
    total_seats = models.PositiveIntegerField(default=30)
    seats_available = models.PositiveIntegerField(default=30)
    cover_image = models.ImageField(upload_to='masterclasses/covers/', blank=True, null=True, help_text="Upload a cover image for this masterclass")
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or video URL")
    is_upcoming = models.BooleanField(default=True, help_text="Mark as upcoming masterclass")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', 'title']
        verbose_name_plural = "Masterclasses"
    
    def __str__(self):
        return self.title


class SocialMediaLink(models.Model):
    """Social media links for footer"""
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
    ]
    
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(help_text="Full URL to your social media profile")
    icon_class = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class (e.g., 'fab fa-facebook')")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'platform']
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"
    
    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"
    
    def get_icon_class(self):
        """Get icon class with fallback"""
        if self.icon_class:
            return self.icon_class
        # Default icons based on platform
        defaults = {
            'facebook': 'fab fa-facebook',
            'twitter': 'fab fa-twitter',
            'linkedin': 'fab fa-linkedin',
            'instagram': 'fab fa-instagram',
            'youtube': 'fab fa-youtube',
            'tiktok': 'fab fa-tiktok',
        }
        return defaults.get(self.platform, 'fas fa-share-alt')


class GalleryItem(models.Model):
    """Gallery items for images and videos"""
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, help_text="Main caption/title for the gallery item")
    caption = models.CharField(max_length=300, blank=True, help_text="Short caption")
    description = models.TextField(blank=True, help_text="Detailed description or additional information")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='gallery/images/', blank=True, null=True, help_text="Upload image for image type")
    video_url = models.URLField(blank=True, help_text="Video URL (YouTube, Vimeo, etc.) for video type")
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True, help_text="Or upload video file")
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True, help_text="Custom thumbnail (optional)")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    is_featured = models.BooleanField(default=False, help_text="Show in featured section")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"
    
    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"
    
    def get_media_url(self):
        """Get the media URL based on type"""
        if self.media_type == 'image':
            return self.image.url if self.image else None
        elif self.media_type == 'video':
            return self.video_url if self.video_url else (self.video_file.url if self.video_file else None)
        return None
    
    def get_thumbnail_url(self):
        """Get thumbnail URL"""
        if self.thumbnail:
            return self.thumbnail.url
        elif self.media_type == 'image' and self.image:
            return self.image.url
        return None


class MasterclassRegistration(models.Model):
    """Masterclass registration records"""
    masterclass = models.ForeignKey(Masterclass, on_delete=models.CASCADE, related_name='registrations', null=True, blank=True, help_text="Link to specific masterclass (optional)")
    masterclass_title = models.CharField(max_length=200, help_text="Masterclass title (if not linked to specific masterclass)")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True, help_text="Company/Organization")
    experience_years = models.CharField(max_length=20, blank=True, help_text="Years of experience")
    motivation = models.TextField(blank=True, help_text="Why interested in this masterclass")
    subscribe_newsletter = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    notes = models.TextField(blank=True, help_text="Admin notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Masterclass Registration"
        verbose_name_plural = "Masterclass Registrations"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.masterclass_title or (self.masterclass.title if self.masterclass else 'N/A')}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
