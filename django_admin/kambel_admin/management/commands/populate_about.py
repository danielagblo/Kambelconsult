"""
Management command to populate default about page data
"""
from django.core.management.base import BaseCommand
from kambel_admin.models import (
    AboutConfig, ProfessionalJourneyItem, EducationQualification,
    Achievement, SpeakingEngagement
)


class Command(BaseCommand):
    help = 'Populate default about page configuration'

    def handle(self, *args, **options):
        # Get or create AboutConfig
        about_config, created = AboutConfig.objects.get_or_create(
            defaults={
                'hero_years': "15+",
                'hero_clients': "5000+",
                'hero_publications': "50+",
                'hero_speaking': "100+",
                'profile_name': "Moses Agbesi Katamani",
                'profile_title': "Founder & CEO, Kambel Consult",
                'bio_summary': "A visionary leader and expert consultant with over 15 years of experience in education, career development, and business advisory services. Moses is dedicated to empowering individuals and organizations to achieve their full potential through strategic guidance and innovative solutions.",
                'tags': "Education Expert,Career Coach,Business Advisor,Author,Speaker,Leadership Consultant",
                'philosophy_quote': "Education is the foundation of all progress. Through knowledge, guidance, and strategic thinking, we can unlock the potential within every individual and organization.",
                'cta_title': "Ready to Work Together?",
                'cta_description': "Let's discuss how I can help you achieve your goals and unlock your potential. Whether you're seeking career guidance, business advice, or personal development, I'm here to support your journey.",
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created new AboutConfig'))
        else:
            self.stdout.write(self.style.WARNING('AboutConfig already exists. Adding/updating related items.'))
        
        # Delete existing related items if they exist (to avoid duplicates)
        ProfessionalJourneyItem.objects.filter(about_config=about_config).delete()
        EducationQualification.objects.filter(about_config=about_config).delete()
        Achievement.objects.filter(about_config=about_config).delete()
        SpeakingEngagement.objects.filter(about_config=about_config).delete()

        # Create Professional Journey Items
        journey_items = [
            {
                'title': 'Founder & CEO',
                'organization': 'Kambel Consult',
                'period': '2010 - Present',
                'description': 'Leading a comprehensive consultancy firm specializing in education, career development, and business advisory services. Empowering thousands of individuals and organizations to achieve their goals.',
                'icon': 'briefcase',
                'order': 1
            },
            {
                'title': 'Senior Career Consultant',
                'organization': 'Career Development Institute',
                'period': '2008 - 2010',
                'description': 'Provided strategic career guidance to professionals across various industries, helping them navigate career transitions and achieve professional growth.',
                'icon': 'users',
                'order': 2
            },
            {
                'title': 'Business Strategy Advisor',
                'organization': 'Various Organizations',
                'period': '2005 - 2008',
                'description': 'Consulted with businesses on strategic planning, organizational development, and talent management, contributing to significant growth in client organizations.',
                'icon': 'chart-line',
                'order': 3
            },
            {
                'title': 'Education Specialist',
                'organization': 'Educational Institutions',
                'period': '2000 - 2005',
                'description': 'Developed and implemented educational programs, trained educators, and created curriculum materials that improved learning outcomes for thousands of students.',
                'icon': 'graduation-cap',
                'order': 4
            }
        ]

        for item_data in journey_items:
            ProfessionalJourneyItem.objects.create(
                about_config=about_config,
                **item_data
            )

        # Create Education & Qualifications
        education_items = [
            {
                'qualification': 'Master of Business Administration (MBA)',
                'institution': 'University of Business Excellence',
                'year': '2005',
                'icon': 'university',
                'order': 1
            },
            {
                'qualification': 'Bachelor of Education',
                'institution': 'Educational Leadership Institute',
                'year': '2000',
                'icon': 'graduation-cap',
                'order': 2
            },
            {
                'qualification': 'Certified Career Development Facilitator',
                'institution': 'Career Development Association',
                'year': '2008',
                'icon': 'certificate',
                'order': 3
            },
            {
                'qualification': 'Professional Certified Coach (PCC)',
                'institution': 'International Coach Federation',
                'year': '2010',
                'icon': 'medal',
                'order': 4
            }
        ]

        for item_data in education_items:
            EducationQualification.objects.create(
                about_config=about_config,
                **item_data
            )

        # Create Achievements & Recognition
        achievements = [
            {
                'title': 'Outstanding Contribution to Education',
                'description': 'Recognized for exceptional service in advancing educational opportunities and career development initiatives.',
                'year': '2020',
                'icon': 'trophy',
                'order': 1
            },
            {
                'title': 'Best-selling Author',
                'description': 'Published multiple bestselling books on career development and personal growth, reaching thousands of readers worldwide.',
                'year': '2018',
                'icon': 'book',
                'order': 2
            },
            {
                'title': 'Leadership Excellence Award',
                'description': 'Awarded for outstanding leadership in organizational development and strategic consulting.',
                'year': '2015',
                'icon': 'award',
                'order': 3
            },
            {
                'title': 'Community Impact Recognition',
                'description': 'Recognized for significant contributions to community development through mentorship and educational programs.',
                'year': '2012',
                'icon': 'hands-helping',
                'order': 4
            }
        ]

        for item_data in achievements:
            Achievement.objects.create(
                about_config=about_config,
                **item_data
            )

        # Create Speaking Engagements
        speaking_items = [
            {
                'title': 'The Future of Career Development',
                'event': 'International Career Summit',
                'date': '2023',
                'location': 'London, UK',
                'order': 1
            },
            {
                'title': 'Strategic Leadership in Modern Business',
                'event': 'Business Leadership Conference',
                'date': '2022',
                'location': 'New York, USA',
                'order': 2
            },
            {
                'title': 'Education Transformation',
                'event': 'Global Education Forum',
                'date': '2021',
                'location': 'Singapore',
                'order': 3
            },
            {
                'title': 'Personal Development Masterclass',
                'event': 'Personal Growth Summit',
                'date': '2020',
                'location': 'Lagos, Nigeria',
                'order': 4
            }
        ]

        for item_data in speaking_items:
            SpeakingEngagement.objects.create(
                about_config=about_config,
                **item_data
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated about page configuration with default data!'))
        self.stdout.write(self.style.SUCCESS(f'Created AboutConfig: {about_config.profile_name}'))
        self.stdout.write(self.style.SUCCESS(f'Added {len(journey_items)} professional journey items'))
        self.stdout.write(self.style.SUCCESS(f'Added {len(education_items)} education qualifications'))
        self.stdout.write(self.style.SUCCESS(f'Added {len(achievements)} achievements'))
        self.stdout.write(self.style.SUCCESS(f'Added {len(speaking_items)} speaking engagements'))

