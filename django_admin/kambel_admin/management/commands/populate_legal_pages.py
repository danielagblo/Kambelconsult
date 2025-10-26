"""
Management command to populate Privacy Policy and Terms & Conditions
"""
from django.core.management.base import BaseCommand
from kambel_admin.models import PrivacyPolicy, TermsConditions


class Command(BaseCommand):
    help = 'Populate Privacy Policy and Terms & Conditions with default content'

    def handle(self, *args, **options):
        # Privacy Policy
        privacy_policy, created = PrivacyPolicy.objects.get_or_create(
            defaults={
                'title': 'Privacy Policy',
                'subtitle': 'Your privacy is important to us. This policy explains how we collect, use, and protect your information.',
                'content': '''<h3>1. Information We Collect</h3>
<p>We collect information you provide directly to us, such as when you:</p>
<ul>
    <li>Register for our masterclasses or services</li>
    <li>Subscribe to our newsletter</li>
    <li>Contact us through our website</li>
    <li>Purchase our publications or services</li>
</ul>

<h3>2. How We Use Your Information</h3>
<p>We use the information we collect to:</p>
<ul>
    <li>Provide, maintain, and improve our services</li>
    <li>Process transactions and send related information</li>
    <li>Send technical notices, updates, and support messages</li>
    <li>Respond to your comments and questions</li>
    <li>Communicate with you about products, services, and events</li>
</ul>

<h3>3. Information Sharing</h3>
<p>We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except as described in this policy.</p>

<h3>4. Data Security</h3>
<p>We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.</p>

<h3>5. Cookies and Tracking</h3>
<p>We use cookies and similar tracking technologies to enhance your experience on our website. You can control cookie settings through your browser preferences.</p>

<h3>6. Your Rights</h3>
<p>You have the right to:</p>
<ul>
    <li>Access your personal information</li>
    <li>Correct inaccurate information</li>
    <li>Request deletion of your information</li>
    <li>Opt-out of marketing communications</li>
</ul>

<h3>7. Contact Us</h3>
<p>If you have any questions about this Privacy Policy, please contact us through our contact form or email us directly.</p>''',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Privacy Policy.'))
        else:
            self.stdout.write(self.style.WARNING('Privacy Policy already exists.'))

        # Terms & Conditions
        terms_conditions, created = TermsConditions.objects.get_or_create(
            defaults={
                'title': 'Terms & Conditions',
                'subtitle': 'Please read these terms and conditions carefully before using our services.',
                'content': '''<h3>1. Acceptance of Terms</h3>
<p>By accessing and using this website, you accept and agree to be bound by the terms and provision of this agreement.</p>

<h3>2. Use License</h3>
<p>Permission is granted to temporarily download one copy of the materials on Kambel Consult's website for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:</p>
<ul>
    <li>Modify or copy the materials</li>
    <li>Use the materials for any commercial purpose or for any public display</li>
    <li>Attempt to reverse engineer any software contained on the website</li>
    <li>Remove any copyright or other proprietary notations from the materials</li>
</ul>

<h3>3. Services</h3>
<p>Our services include but are not limited to:</p>
<ul>
    <li>Educational publications and course materials</li>
    <li>Consultancy services in education, career, personal development, and business</li>
    <li>Masterclass sessions and training programs</li>
    <li>Online resources and content</li>
</ul>

<h3>4. Payment Terms</h3>
<p>Payment for services must be made in full before delivery. We accept various payment methods as specified during checkout. All prices are subject to change without notice.</p>

<h3>5. Refund Policy</h3>
<p>Refunds are available within 30 days of purchase for digital products and services. Physical products must be returned in original condition. Refund requests must be submitted in writing to our customer service team.</p>

<h3>6. Intellectual Property</h3>
<p>All content, materials, and intellectual property on this website are owned by Kambel Consult and are protected by copyright and other intellectual property laws.</p>

<h3>7. User Conduct</h3>
<p>You agree not to:</p>
<ul>
    <li>Use the website for any unlawful purpose</li>
    <li>Transmit any harmful or malicious code</li>
    <li>Interfere with the proper functioning of the website</li>
    <li>Attempt to gain unauthorized access to any part of the website</li>
</ul>

<h3>8. Limitation of Liability</h3>
<p>In no event shall Kambel Consult or its suppliers be liable for any damages arising out of the use or inability to use the materials on this website, even if Kambel Consult or an authorized representative has been notified orally or in writing of the possibility of such damage.</p>

<h3>9. Privacy</h3>
<p>Your privacy is important to us. Please review our Privacy Policy, which also governs your use of the website, to understand our practices.</p>

<h3>10. Modifications</h3>
<p>Kambel Consult may revise these terms of service at any time without notice. By using this website, you are agreeing to be bound by the then current version of these terms of service.</p>

<h3>11. Contact Information</h3>
<p>If you have any questions about these Terms & Conditions, please contact us through our contact form or email us directly.</p>''',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Terms & Conditions.'))
        else:
            self.stdout.write(self.style.WARNING('Terms & Conditions already exists.'))

        self.stdout.write(self.style.SUCCESS('Legal pages populated successfully.'))

