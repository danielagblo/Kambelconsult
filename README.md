# Kambel Consult Website

A fully functional website for Kambel Consult featuring publications, consultancy services, blog, masterclasses, and KICT (Kampbell Institute of Career Institute).

## Features

### Frontend
- **Responsive Design**: Built with Bootstrap 5 for mobile-first responsive design
- **Modern UI**: Clean, professional interface with smooth animations
- **Interactive Elements**: Dynamic content loading, form validation, and user interactions
- **Sections**:
  - Publications (Course Books, Guidance Books, Inspirational Books, Literature)
  - Consultancy Services (Education, Career, Personal Development, Business)
  - Blog with dynamic content
  - Masterclass series
  - KICT (Kampbell Institute of Career Institute)
  - Online Training (Under Development)
  - Safe Purchase functionality
  - Contact forms

### Backend
- **Flask API**: RESTful API endpoints for all functionality
- **Data Management**: JSON-based data storage with file persistence
- **Contact System**: Contact form handling with email notifications
- **Newsletter**: Subscription management
- **Purchase System**: E-commerce functionality for books and courses
- **Enrollment**: Course enrollment system

## Technology Stack

### Frontend
- HTML5
- CSS3 (Custom styles with Bootstrap 5)
- JavaScript (ES6+)
- Bootstrap 5.3.0
- Font Awesome 6.4.0

### Backend
- Python 3.8+
- Flask 2.3.3
- Flask-CORS 4.0.0

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd kambelconsult
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the website**
   Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
kambelconsult/
├── app.py                 # Flask backend application
├── index.html            # Main HTML file
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── static/
│   ├── css/
│   │   └── style.css    # Custom CSS styles
│   └── js/
│       └── script.js    # JavaScript functionality
└── data/                # Data storage directory (created automatically)
    ├── contact_messages.json
    └── newsletter_subscriptions.json
```

## API Endpoints

### Blog
- `GET /api/blog` - Get all blog posts
- `GET /api/blog/<id>` - Get specific blog post

### Publications
- `GET /api/publications` - Get all publications
- `GET /api/publications/<category>` - Get publications by category

### Masterclasses
- `GET /api/masterclasses` - Get all masterclasses
- `GET /api/masterclasses/<id>` - Get specific masterclass

### KICT
- `GET /api/kict/courses` - Get KICT courses

### Contact & Forms
- `POST /api/contact` - Submit contact form
- `POST /api/newsletter` - Subscribe to newsletter
- `POST /api/purchase` - Process purchase
- `POST /api/enroll` - Enroll in course

## Features in Detail

### Publications Section
- **Course Books**: Academic and professional course materials
- **Guidance Books**: Expert guidance and mentorship resources
- **Inspirational Books**: Motivational and personal growth content
- **Literature**: Literary works and thought-provoking content

### Consultancy Services
- **Education**: Educational consulting and learning enhancement
- **Career**: Career guidance and professional development
- **Personal Development**: Personal growth and self-improvement
- **Business**: Business consulting and growth strategies

### Blog System
- Dynamic blog post loading
- Category-based filtering
- Author information and publication dates
- Responsive card-based layout

### Masterclass Series
- Expert-led training sessions
- Interactive learning experiences
- Certificate programs
- Networking opportunities

### KICT (Kampbell Institute of Career Institute)
- Professional development programs
- Career transition workshops
- Industry-specific training
- Success tracking and metrics

## Customization

### Adding New Blog Posts
Edit the `BLOG_POSTS` list in `app.py` to add new blog posts.

### Adding New Publications
Update the `PUBLICATIONS` dictionary in `app.py` with new books and resources.

### Styling Changes
Modify `static/css/style.css` to customize the appearance and layout.

### Adding New Features
- Add new API endpoints in `app.py`
- Update the frontend in `index.html` and `static/js/script.js`
- Add new CSS styles as needed

## Production Deployment

### Environment Variables
Set up the following environment variables for production:
- `FLASK_ENV=production`
- `MAIL_USERNAME` - Email username for contact form
- `MAIL_PASSWORD` - Email password for contact form
- `SECRET_KEY` - Flask secret key

### Database Integration
For production, consider replacing JSON file storage with a proper database:
- PostgreSQL
- MySQL
- SQLite
- MongoDB

### Payment Integration
Integrate with payment gateways:
- Stripe
- PayPal
- Square
- Razorpay

### Email Service
Set up proper email service:
- SendGrid
- Mailgun
- AWS SES
- SMTP with proper authentication

## Security Considerations

- Implement proper input validation
- Add CSRF protection
- Use HTTPS in production
- Implement rate limiting
- Add authentication for admin functions
- Sanitize user inputs

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact:
- Email: info@kambelconsult.com
- Phone: +1 (555) 123-4567

## Changelog

### Version 1.0.0
- Initial release
- Complete frontend and backend implementation
- All core features implemented
- Responsive design
- API endpoints for all functionality
