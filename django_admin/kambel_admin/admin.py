"""
Admin configuration for Kambel Consult
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Book, ConsultancyService, ServiceFeature,
    BlogPost, ContactMessage, NewsletterSubscription, SiteConfig, HeroConfig, AboutConfig,
    ProfessionalJourneyItem, EducationQualification, Achievement, SpeakingEngagement,
    Masterclass, SocialMediaLink, PrivacyPolicy, TermsConditions, GalleryItem, MasterclassRegistration
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ['title', 'description', 'icon', 'is_active', 'order']


@admin.register(ConsultancyService)
class ConsultancyServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'has_cover_image', 'is_active', 'order', 'created_at']
    list_filter = ['service_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']
    inlines = [ServiceFeatureInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'service_type', 'description')
        }),
        ('Media', {
            'fields': ('cover_image', 'icon'),
            'description': 'Upload a cover image to display on the website'
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def has_cover_image(self, obj):
        return bool(obj.cover_image)
    has_cover_image.boolean = True
    has_cover_image.short_description = 'Has Cover Image'


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'service', 'is_active', 'order', 'created_at']
    list_filter = ['service', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'author', 'description']
    list_editable = ['is_active']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'description', 'category')
        }),
        ('Details', {
            'fields': ('pages', 'price', 'purchase_link')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'author', 'content']
    list_editable = ['is_published']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'excerpt', 'author')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('Status', {
            'fields': ('is_published',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'tagline', 'contact_email', 'contact_phone', 'updated_at']
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'tagline')
        }),
        ('Media', {
            'fields': ('logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'address', 'location')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one site configuration
        return not SiteConfig.objects.exists()


@admin.register(HeroConfig)
class HeroConfigAdmin(admin.ModelAdmin):
    list_display = ['hero_title', 'profile_name', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['hero_title', 'hero_subtitle', 'profile_name']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Hero Content', {
            'fields': ('hero_title', 'hero_subtitle')
        }),
        ('Profile Information', {
            'fields': ('profile_name', 'profile_title', 'profile_picture')
        }),
        ('Credentials/Stats', {
            'fields': (
                ('years_experience', 'years_label', 'years_description'),
                ('clients_count', 'clients_label', 'clients_description'),
                ('publications_count', 'publications_label', 'publications_description')
            ),
            'description': 'Configure the three credential cards displayed in the hero section'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one hero configuration
        return not HeroConfig.objects.exists()


# Inline admin classes for AboutConfig
class ProfessionalJourneyItemInline(admin.TabularInline):
    model = ProfessionalJourneyItem
    extra = 1
    fields = ['title', 'organization', 'period', 'description', 'icon', 'order', 'is_active']
    ordering = ['order']


class EducationQualificationInline(admin.TabularInline):
    model = EducationQualification
    extra = 1
    fields = ['qualification', 'institution', 'year', 'icon', 'order', 'is_active']
    ordering = ['order']


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1
    fields = ['title', 'description', 'year', 'icon', 'order', 'is_active']
    ordering = ['order']


class SpeakingEngagementInline(admin.TabularInline):
    model = SpeakingEngagement
    extra = 1
    fields = ['title', 'event', 'date', 'location', 'order', 'is_active']
    ordering = ['order']


@admin.register(AboutConfig)
class AboutConfigAdmin(admin.ModelAdmin):
    list_display = ['profile_name', 'profile_title', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['profile_name', 'profile_title', 'bio_summary']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Hero Section Stats', {
            'fields': (
                ('hero_years', 'hero_clients'),
                ('hero_publications', 'hero_speaking')
            ),
            'description': 'Statistics displayed in the hero section of the about page'
        }),
        ('Profile Information', {
            'fields': ('profile_name', 'profile_title', 'profile_picture', 'bio_summary')
        }),
        ('Tags/Badges', {
            'fields': ('tags',),
            'description': 'Comma-separated tags to display as badges (e.g., "Education Expert,Career Coach")'
        }),
        ('Philosophy', {
            'fields': ('philosophy_quote',)
        }),
        ('Call to Action', {
            'fields': ('cta_title', 'cta_description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    inlines = [
        ProfessionalJourneyItemInline,
        EducationQualificationInline,
        AchievementInline,
        SpeakingEngagementInline
    ]
    
    def has_add_permission(self, request):
        # Only allow one about configuration - but allow editing if it exists
        if AboutConfig.objects.exists():
            return False
        return True


@admin.register(Masterclass)
class MasterclassAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'date', 'duration', 'price', 'seats_available', 'is_upcoming', 'is_active', 'created_at']
    list_filter = ['is_upcoming', 'is_active', 'date', 'created_at']
    search_fields = ['title', 'description', 'instructor']
    list_editable = ['is_upcoming', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'instructor')
        }),
        ('Schedule & Pricing', {
            'fields': ('date', 'duration', 'price', 'total_seats', 'seats_available'),
            'description': 'Set price to 0.00 for free masterclasses'
        }),
        ('Media', {
            'fields': ('cover_image', 'video_url'),
            'description': 'Upload a cover image and optionally add a video URL'
        }),
        ('Status', {
            'fields': ('is_upcoming', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-date', 'title')


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active', 'order', 'created_at']
    list_filter = ['platform', 'is_active', 'created_at']
    search_fields = ['platform', 'url']
    list_editable = ['is_active', 'order']
    fieldsets = (
        ('Social Media Information', {
            'fields': ('platform', 'url'),
            'description': 'The platform logo will be automatically set based on your selection'
        }),
        ('Advanced', {
            'fields': ('icon_class',),
            'classes': ('collapse',),
            'description': 'Icon class is auto-filled. Only modify if you need a custom icon.'
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    # Default icon classes for each platform
    ICON_CLASSES = {
        'facebook': 'fab fa-facebook',
        'twitter': 'fab fa-twitter',
        'linkedin': 'fab fa-linkedin',
        'instagram': 'fab fa-instagram',
        'youtube': 'fab fa-youtube',
        'tiktok': 'fab fa-tiktok',
    }
    
    class Media:
        js = ('admin/js/social_media_auto_icon.js',)
    
    def save_model(self, request, obj, form, change):
        # Auto-fill icon_class if not provided or if platform changed
        if not obj.icon_class or (change and 'platform' in form.changed_data):
            obj.icon_class = self.ICON_CLASSES.get(obj.platform, 'fas fa-share-alt')
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order', 'platform')


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'last_updated', 'updated_at']
    readonly_fields = ['last_updated', 'created_at', 'updated_at']
    fieldsets = (
        ('Header Information', {
            'fields': ('title', 'subtitle')
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Use HTML tags for formatting. Examples: <h3>Heading</h3>, <p>Paragraph</p>, <ul><li>Item</li></ul>'
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('last_updated', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one privacy policy - but allow editing if it exists
        if PrivacyPolicy.objects.exists():
            return False
        return True


@admin.register(TermsConditions)
class TermsConditionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'last_updated', 'updated_at']
    readonly_fields = ['last_updated', 'created_at', 'updated_at']
    fieldsets = (
        ('Header Information', {
            'fields': ('title', 'subtitle')
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Use HTML tags for formatting. Examples: <h3>Heading</h3>, <p>Paragraph</p>, <ul><li>Item</li></ul>'
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('last_updated', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one terms & conditions - but allow editing if it exists
        if TermsConditions.objects.exists():
            return False
        return True


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'is_featured', 'is_active', 'order', 'created_at']
    list_filter = ['media_type', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'caption', 'description']
    ordering = ['order', '-created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'caption', 'description')
        }),
        ('Media', {
            'fields': ('media_type', 'image', 'video_url', 'video_file', 'thumbnail'),
            'description': 'For images: upload an image. For videos: provide a URL (YouTube/Vimeo) or upload a video file.'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        return readonly


@admin.register(MasterclassRegistration)
class MasterclassRegistrationAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_masterclass_title', 'email', 'phone', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'subscribe_newsletter']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'masterclass_title', 'company']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Masterclass Information', {
            'fields': ('masterclass', 'masterclass_title')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company')
        }),
        ('Registration Details', {
            'fields': ('experience_years', 'motivation', 'subscribe_newsletter')
        }),
        ('Admin', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Name'
    
    def get_masterclass_title(self, obj):
        return obj.masterclass_title or (obj.masterclass.title if obj.masterclass else 'N/A')
    get_masterclass_title.short_description = 'Masterclass'


# Customize admin site
admin.site.site_header = "Kambel Consult Administration"
admin.site.site_title = "Kambel Consult Admin"
admin.site.index_title = "Welcome to Kambel Consult Administration"
