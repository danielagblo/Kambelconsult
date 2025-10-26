from flask import Flask, render_template, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import json
import os
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'

# Django Admin API Configuration
DJANGO_API_BASE = 'http://localhost:8000/api'

# Helper function to fetch data from Django Admin API
def fetch_from_django_api(endpoint):
    """Fetch data from Django Admin API with fallback to empty list"""
    try:
        response = requests.get(f"{DJANGO_API_BASE}/{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Django API error for {endpoint}: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Django API for {endpoint}: {e}")
        return None

def get_blog_posts():
    """Get blog posts from Django Admin API"""
    posts = fetch_from_django_api('blog/')
    # Transform Django data to match frontend expectations
    return [
        {
            "id": post.get('id', 0),
            "title": post.get('title', ''),
            "content": post.get('content', ''),
            "excerpt": post.get('excerpt', ''),
            "author": post.get('author', 'Kambel Team'),
            "date": post.get('date', ''),
            "category": post.get('category', ''),
            "icon": post.get('icon', 'fas fa-book'),
            "cover_image_url": post.get('cover_image_url'),
            "tags": [post.get('category', '').lower()]
        }
        for post in posts
    ]

def get_publications():
    """Get publications from Django Admin API"""
    books = fetch_from_django_api('publications/')
    # Group books by category
    publications = {
        "course_books": [],
        "guidance_books": [],
        "inspirational_books": [],
        "literature": []
    }
    
    for book in books:
        book_data = {
            "id": book.get('id', 0),
            "title": book.get('title', ''),
            "author": book.get('author', 'Moses Agbesi Katamani'),
            "price": float(book.get('price', 0)),
            "description": book.get('description', ''),
            "category": book.get('category', '') if isinstance(book.get('category'), str) else (book.get('category', {}).get('name', '') if book.get('category') else ''),
            "pages": book.get('pages', 0),
            "isbn": f"978-{book.get('id', 0):010d}",
            "cover_image_url": book.get('cover_image_url'),
            "purchase_link": book.get('purchase_link', '')
        }
        
        category_name = book_data['category'].lower()
        # Map categories based on common keywords
        if 'course' in category_name or 'business' in category_name or 'management' in category_name or 'education' in category_name:
            publications["course_books"].append(book_data)
        elif 'guidance' in category_name or 'career' in category_name:
            publications["guidance_books"].append(book_data)
        elif 'inspirational' in category_name or 'personal' in category_name or 'motivation' in category_name:
            publications["inspirational_books"].append(book_data)
        else:
            publications["literature"].append(book_data)
    
    return publications

def get_masterclasses():
    """Get masterclasses from Django Admin API"""
    data = fetch_from_django_api('masterclasses/')
    if not data:
        return {"upcoming": [], "previous": []}
    
    def transform_masterclass(mc):
        """Transform Django masterclass data to match frontend expectations"""
        return {
            "id": mc.get('id', 0),
            "title": mc.get('title', ''),
            "instructor": mc.get('instructor', 'Moses Agbesi Katamani'),
            "date": mc.get('date', ''),
            "time": "10:00 AM - 4:00 PM",  # Default time (can be added to model later)
            "price": 299.99,  # Default price (can be added to model later)
            "description": mc.get('description', ''),
            "seats_available": mc.get('seats_available', 0),
            "total_seats": mc.get('total_seats', 30),
            "duration": mc.get('duration', ''),
            "cover_image_url": mc.get('cover_image_url'),
            "video_url": mc.get('video_url')
        }
    
    upcoming = [transform_masterclass(mc) for mc in data.get('upcoming', [])]
    previous = [transform_masterclass(mc) for mc in data.get('previous', [])]
    
    return {
        "upcoming": upcoming,
        "previous": previous
    }

def get_site_config():
    """Get site configuration from Django Admin API"""
    config = fetch_from_django_api('site/config/')
    if not config:
        # Return default configuration
        return {
            "hero_title": "Welcome to Kambel Consult",
            "hero_subtitle": "Your trusted partner in career development and business excellence",
            "profile_name": "Moses Agbesi Katamani",
            "profile_title": "Founder & Lead Consultant",
            "profile_description": "Experienced consultant with over 15 years in career development and business strategy",
            "profile_picture_url": None,
            "services_title": "Our Services",
            "services_subtitle": "Comprehensive solutions for your professional growth",
            "about_title": "About Kambel Consult",
            "about_content": "We are dedicated to empowering individuals and organizations through expert consulting and training services",
            "contact_title": "Get In Touch",
            "contact_subtitle": "Ready to take your career or business to the next level?",
            "footer_text": "© 2024 Kambel Consult. All rights reserved.",
            "site_name": "Kambel Consult",
            "site_tagline": "Empowering Success Through Expert Guidance"
        }
    return config

def get_kict_courses():
    """Get KICT courses from Django Admin API"""
    courses = fetch_from_django_api('kict/courses/')
    return [
        {
            "id": course.get('id', 0),
            "title": course.get('title', ''),
            "duration": course.get('duration', ''),
            "price": float(course.get('price', 0)),
            "description": course.get('description', ''),
            "instructor": course.get('instructor', ''),
            "start_date": course.get('start_date', '')
        }
        for course in courses
    ]

def get_contact_info():
    """Get contact information from Django Admin API"""
    contact_data = fetch_from_django_api('site/contact-info/')
    if contact_data:
        return contact_data
    # Fallback to default values
    return {
        "email": "info@kambelconsult.com",
        "phone": "+1 (555) 123-4567",
        "address": "123 Business Street",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "United States"
    }

def get_social_media_links():
    """Get social media links from Django Admin API"""
    links = fetch_from_django_api('site/social-media/')
    return [
        {
            "platform": link.get('platform', ''),
            "url": link.get('url', ''),
            "icon_class": link.get('icon_class', ''),
            "order": link.get('order', 0)
        }
        for link in links
    ]

def get_seo_content(page):
    """Get SEO content for a specific page from Django Admin API"""
    seo_data = fetch_from_django_api(f'site/seo/{page}/')
    if seo_data:
        return seo_data
    # Fallback to default values
    return {
        "page": page,
        "title": f"Kambel Consult - {page.title()}",
        "description": "Professional consulting and training services",
        "keywords": "consulting, training, career development, business strategy",
        "og_title": f"Kambel Consult - {page.title()}",
        "og_description": "Professional consulting and training services",
        "og_image_url": None
    }

# Routes
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Support direct navigation to index.html
@app.route('/index.html')
def index_html():
    return send_from_directory('.', 'index.html')

@app.route('/publications.html')
def publications():
    return send_from_directory('.', 'publications.html')


# Redirect old publication pages to new unified page
@app.route('/course-books.html')
def course_books():
    return redirect('/publications.html')

@app.route('/guidance-books.html')
def guidance_books():
    return redirect('/publications.html')

@app.route('/inspirational-books.html')
def inspirational_books():
    return redirect('/publications.html')

@app.route('/literature.html')
def literature():
    return redirect('/publications.html')

# Consultancy pages - Consolidated into single consultancy page

@app.route('/consultancy-unified.html')
def consultancy_unified():
    return send_from_directory('.', 'consultancy-unified.html')

# Redirect old consultancy.html to unified page
@app.route('/consultancy.html')
def consultancy_redirect():
    return redirect('/consultancy-unified.html')

# Redirect old consultancy pages to new unified page
@app.route('/education.html')
def education():
    return redirect('/consultancy-unified.html')

@app.route('/career.html')
def career():
    return redirect('/consultancy-unified.html')

@app.route('/personal-development.html')
def personal_development():
    return redirect('/consultancy-unified.html')

@app.route('/business.html')
def business():
    return redirect('/consultancy-unified.html')

# About page
@app.route('/about.html')
def about():
    return send_from_directory('.', 'about.html')

# Gallery page
@app.route('/gallery.html')
def gallery():
    return send_from_directory('.', 'gallery.html')


# Masterclass page
@app.route('/masterclass.html')
def masterclass():
    return send_from_directory('.', 'masterclass.html')

# Legal pages
@app.route('/privacy-policy.html')
def privacy_policy():
    return send_from_directory('.', 'privacy-policy.html')

@app.route('/terms-conditions.html')
def terms_conditions():
    return send_from_directory('.', 'terms-conditions.html')

@app.route('/api/blog')
def api_get_blog_posts():
    """Get all blog posts from Django API"""
    posts = get_blog_posts()
    return jsonify(posts)

@app.route('/api/blog/<int:post_id>')
def get_blog_post(post_id):
    """Get a specific blog post"""
    posts = get_blog_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return jsonify(post)
    return jsonify({'error': 'Post not found'}), 404

@app.route('/api/publications')
def api_get_publications():
    """Get all publications from Django API"""
    publications = get_publications()
    return jsonify(publications)

@app.route('/api/publications/<category>')
def get_publications_by_category(category):
    """Get publications by category"""
    publications = get_publications()
    if category in publications:
        return jsonify(publications[category])
    return jsonify({'error': 'Category not found'}), 404

@app.route('/api/categories')
def api_get_categories():
    """Get all categories from Django API"""
    categories = fetch_from_django_api('categories/')
    return jsonify(categories)

@app.route('/api/consultancy')
def api_get_consultancy():
    """Get all consultancy services from Django API"""
    consultancy = fetch_from_django_api('consultancy/')
    return jsonify(consultancy)

@app.route('/api/masterclasses')
def api_get_masterclasses():
    """Get all masterclasses from Django API"""
    masterclasses = get_masterclasses()
    return jsonify(masterclasses)

@app.route('/api/masterclasses/<int:masterclass_id>')
def get_masterclass(masterclass_id):
    """Get a specific masterclass"""
    masterclasses = get_masterclasses()
    masterclass = next((m for m in masterclasses if m['id'] == masterclass_id), None)
    if masterclass:
        return jsonify(masterclass)
    return jsonify({'error': 'Masterclass not found'}), 404

@app.route('/api/kict/courses')
def api_get_kict_courses():
    """Get KICT courses"""
    return jsonify(get_kict_courses())

@app.route('/api/site/contact-info')
def api_get_contact_info():
    return jsonify(get_contact_info())

@app.route('/api/site/social-media')
def api_get_social_media():
    return jsonify(get_social_media_links())

@app.route('/api/site/seo/<page>')
def api_get_seo_content(page):
    return jsonify(get_seo_content(page))

@app.route('/api/site/config')
def api_get_site_config():
    """Get site configuration from Django API"""
    config = get_site_config()
    return jsonify(config)

@app.route('/api/site/hero')
def api_get_hero_config():
    """Get hero configuration from Django API"""
    hero_config = fetch_from_django_api('site/hero/')
    if not hero_config:
        # Return default values
        return jsonify({
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
    return jsonify(hero_config)

@app.route('/api/site/privacy-policy')
def api_get_privacy_policy():
    """Get privacy policy from Django API"""
    try:
        response = requests.get(f"{DJANGO_API_BASE}/site/privacy-policy/", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        # Return default values if not found
        return jsonify({
            'title': 'Privacy Policy',
            'subtitle': 'Your privacy is important to us. This policy explains how we collect, use, and protect your information.',
            'content': '<p>Privacy policy content will be available soon.</p>',
            'last_updated': None
        })
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch privacy policy: {e}")
        return jsonify({
            'title': 'Privacy Policy',
            'subtitle': 'Your privacy is important to us. This policy explains how we collect, use, and protect your information.',
            'content': '<p>Privacy policy content will be available soon.</p>',
            'last_updated': None
        })

@app.route('/api/site/terms-conditions')
def api_get_terms_conditions():
    """Get terms & conditions from Django API"""
    try:
        response = requests.get(f"{DJANGO_API_BASE}/site/terms-conditions/", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        # Return default values if not found
        return jsonify({
            'title': 'Terms & Conditions',
            'subtitle': 'Please read these terms and conditions carefully before using our services.',
            'content': '<p>Terms and conditions content will be available soon.</p>',
            'last_updated': None
        })
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch terms & conditions: {e}")
        return jsonify({
            'title': 'Terms & Conditions',
            'subtitle': 'Please read these terms and conditions carefully before using our services.',
            'content': '<p>Terms and conditions content will be available soon.</p>',
            'last_updated': None
        })

@app.route('/api/gallery')
def api_get_gallery():
    """Get gallery items from Django API"""
    try:
        featured = request.args.get('featured', 'false')
        response = requests.get(f"{DJANGO_API_BASE}/gallery/?featured={featured}", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        return jsonify([])
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch gallery: {e}")
        return jsonify([])

@app.route('/api/masterclass/register', methods=['POST'])
def api_register_masterclass():
    """Register for masterclass via Django API"""
    try:
        data = request.get_json()
        response = requests.post(f"{DJANGO_API_BASE}/masterclass/register/", json=data, timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        return jsonify({'success': False, 'message': 'Registration failed. Please try again.'}), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Failed to register masterclass: {e}")
        return jsonify({'success': False, 'message': 'Unable to submit registration. Please try again later.'}), 500

@app.route('/api/site/about')
def api_get_about_config():
    """Get about page configuration from Django API"""
    try:
        response = requests.get(f"{DJANGO_API_BASE}/site/about/", timeout=5)
        if response.status_code == 200:
            about_config = response.json()
            return jsonify(about_config)
        else:
            print(f"Django API error for about: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Django API for about: {e}")
    
    # Return default values if API fails
    return jsonify({
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

@app.route('/api/site/page/<slug>')
def api_get_page_content(slug):
    """Get page content from Django API"""
    try:
        response = requests.get(f"{DJANGO_API_BASE}/site/page/{slug}/", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Page not found'}), 404
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page content for {slug}: {e}")
        return jsonify({'error': 'Failed to fetch page content'}), 500

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Forward to Django admin API
        response = requests.post('http://localhost:8000/api/contact/', json=data, timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to submit contact form'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/newsletter', methods=['POST'])
def newsletter():
    """Handle newsletter subscription"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Forward to Django admin API
        response = requests.post('http://localhost:8000/api/newsletter/', json=data, timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to subscribe to newsletter'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/purchase', methods=['POST'])
def purchase():
    """Handle purchase requests"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['item_id', 'item_type', 'customer_info']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Process purchase (in production, integrate with payment gateway)
        process_purchase(data)
        
        return jsonify({'message': 'Purchase processed successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enroll', methods=['POST'])
def enroll():
    """Handle course enrollment"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['course_id', 'student_info']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Process enrollment (in production, save to database)
        process_enrollment(data)
        
        return jsonify({'message': 'Successfully enrolled in course'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Helper functions
def send_contact_email(data):
    """Send contact form email"""
    # In production, implement actual email sending
    print(f"Contact form submission: {data}")
    pass

def save_contact_message(data):
    """Save contact message to Django database"""
    try:
        contact_data = {
            'name': data['name'],
            'email': data['email'],
            'subject': data['subject'],
            'message': data['message']
        }
        
        response = requests.post(
            f"{DJANGO_API_BASE}/site/contact/",
            json=contact_data,
            timeout=5
        )
        
        if response.status_code in [200, 201]:
            print(f"Contact message saved to Django: {data['email']}")
        else:
            print(f"Failed to save contact message to Django: {response.status_code}")
            # Fallback to file storage
            save_to_file_fallback(data)
            
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Django API for contact message: {e}")
        # Fallback to file storage
        save_to_file_fallback(data)

def save_to_file_fallback(data):
    """Fallback method to save contact message to file"""
    message = {
        'timestamp': datetime.now().isoformat(),
        'name': data['name'],
        'email': data['email'],
        'subject': data['subject'],
        'message': data['message']
    }
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Append to messages file
    with open('data/contact_messages.json', 'a') as f:
        f.write(json.dumps(message) + '\n')

def save_newsletter_subscription(email):
    """Save newsletter subscription to Django database"""
    try:
        subscription_data = {
            'email': email
        }
        
        response = requests.post(
            f"{DJANGO_API_BASE}/site/newsletter/",
            json=subscription_data,
            timeout=5
        )
        
        if response.status_code == 201:
            print(f"Newsletter subscription saved to Django: {email}")
        else:
            print(f"Failed to save newsletter subscription to Django: {response.status_code}")
            # Fallback to file storage
            save_newsletter_to_file_fallback(email)
            
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Django API for newsletter subscription: {e}")
        # Fallback to file storage
        save_newsletter_to_file_fallback(email)

def save_newsletter_to_file_fallback(email):
    """Fallback method to save newsletter subscription to file"""
    subscription = {
        'email': email,
        'timestamp': datetime.now().isoformat()
    }
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Append to subscriptions file
    with open('data/newsletter_subscriptions.json', 'a') as f:
        f.write(json.dumps(subscription) + '\n')

def process_purchase(data):
    """Process purchase request"""
    # In production, integrate with payment gateway
    print(f"Purchase processed: {data}")
    pass

def process_enrollment(data):
    """Process course enrollment"""
    # In production, save to database
    print(f"Enrollment processed: {data}")
    pass

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5001)
