// Custom JavaScript for Kambel Consult

document.addEventListener('DOMContentLoaded', function() {
    // Hide loading screen
    setTimeout(() => {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 500);
        }
    }, 1500);

    // Update current year
    updateCurrentYear();

    // Initialize all functionality
    initSmoothScrolling();
    initNavbarScroll();
    
    // Initialize newsletter form
    initNewsletterForm();
    initContactForm();
    initBlogPosts();
    initAnimations();
    initTooltips();
    loadSiteConfig();
    loadHeroConfig();
});

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Navbar scroll effect
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', function() {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
        
        // Hide navbar on scroll down, show on scroll up
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollY = currentScrollY;
    });
}

// Contact form handling
function initContactForm() {
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate form
            if (!validateForm(this)) {
                return;
            }
            
            // Get form data
            const data = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                subject: document.getElementById('subject').value,
                message: document.getElementById('message').value
            };
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading"></span> Sending...';
            submitBtn.disabled = true;
            
            // Send to API
            fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.message) {
                    // Reset form
                    this.reset();
                    
                    // Show success message
                    showAlert('Message sent successfully! We\'ll get back to you soon.', 'success');
                } else {
                    showAlert('Error sending message. Please try again.', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error sending message. Please try again.', 'danger');
            })
            .finally(() => {
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        });
    }
}

// Blog posts functionality
function initBlogPosts() {
    const blogContainer = document.getElementById('blog-posts');
    
    if (blogContainer) {
        // Load blog posts from API
        fetch('/api/blog')
            .then(response => response.json())
            .then(posts => {
                // Render blog posts
                blogContainer.innerHTML = posts.map(post => `
                    <div class="col-md-6 col-lg-4">
                        <div class="card blog-card h-100">
                            <div class="card-body">
                                <div class="text-center mb-3">
                                    ${post.cover_image_url ? 
                                        `<img src="${post.cover_image_url}" alt="${post.title} cover" class="img-fluid rounded shadow-sm" style="height: 180px; width: 100%; object-fit: cover;" loading="lazy"/>` : 
                                        `<i class="${post.icon} fa-3x text-primary"></i>`
                                    }
                                </div>
                                <div class="blog-meta mb-2">
                                    <span class="badge bg-primary me-2">${post.category}</span>
                                    <small class="text-muted">${formatDate(post.date)}</small>
                                </div>
                                <h5 class="card-title">${post.title}</h5>
                                <p class="card-text">${post.excerpt}</p>
                                <div class="d-flex justify-content-between align-items-center">
                                    <small class="text-muted">By ${post.author}</small>
                                    <a href="#" class="btn btn-outline-primary btn-sm" onclick="viewBlogPost(${post.id})">Read More</a>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');
            })
            .catch(error => {
                console.error('Error loading blog posts:', error);
                blogContainer.innerHTML = '<div class="col-12"><div class="alert alert-warning">Unable to load blog posts. Please try again later.</div></div>';
            });
    }
}

// Initialize animations
function initAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    // Add animation classes to elements
    const elementsToAnimate = document.querySelectorAll('.card, .section-header, .hero-content h1, .hero-content p, .hero-content .btn-group-enhanced');
    elementsToAnimate.forEach((el, index) => {
        if (!el.classList.contains('fade-in')) {
            el.classList.add('fade-in');
        }
        el.style.animationDelay = `${index * 0.1}s`;
        observer.observe(el);
    });
    
    // Add staggered animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const cards = document.querySelectorAll('.card');
            
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

// Newsletter subscription
function subscribeNewsletter(email) {
    // Simulate API call
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log('Newsletter subscription:', email);
            resolve({ success: true });
        }, 1000);
    });
}

// Book purchase functionality
function purchaseBook(bookId, bookTitle, price) {
    // Open prefilled email to sales
    const subject = encodeURIComponent(`Purchase Inquiry: ${bookTitle}`);
    const body = encodeURIComponent(
        `Hello Kambel Consult Sales Team,%0D%0A%0D%0A` +
        `I would like to purchase the following publication:%0D%0A` +
        `- Title: ${bookTitle}%0D%0A` +
        (price !== undefined ? `- Price: $${price}%0D%0A` : '') +
        `- Book ID: ${bookId}%0D%0A%0D%0A` +
        `Please let me know the next steps for payment and delivery.%0D%0A%0D%0A` +
        `Best regards,%0D%0A`
    );
    window.location.href = `mailto:sales@kambelconsult.com?subject=${subject}&body=${body}`;
}

// Course enrollment
function enrollCourse(courseId, courseTitle) {
    // Simulate enrollment process
    showAlert(`Successfully enrolled in "${courseTitle}"!`, 'success');
    
    // In a real application, this would:
    // 1. Process enrollment
    // 2. Send confirmation email
    // 3. Redirect to course dashboard
}

// Contact form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    // Email validation
    const emailField = form.querySelector('input[type="email"]');
    if (emailField && emailField.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value)) {
            emailField.classList.add('is-invalid');
            isValid = false;
        }
    }
    
    return isValid;
}

// Add to cart functionality
function addToCart(itemId, itemName, price) {
    // Get existing cart from localStorage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Check if item already exists
    const existingItem = cart.find(item => item.id === itemId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: itemId,
            name: itemName,
            price: price,
            quantity: 1
        });
    }
    
    // Save to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Update cart counter
    updateCartCounter();
    
    showAlert(`${itemName} added to cart!`, 'success');
}

// Update cart counter
function updateCartCounter() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    const cartCounter = document.getElementById('cart-counter');
    if (cartCounter) {
        cartCounter.textContent = totalItems;
        cartCounter.style.display = totalItems > 0 ? 'inline' : 'none';
    }
}

// Initialize cart counter on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartCounter();
});

// Mobile menu toggle
function toggleMobileMenu() {
    const navbarCollapse = document.getElementById('navbarNav');
    const navbarToggler = document.querySelector('.navbar-toggler');
    
    if (navbarCollapse.classList.contains('show')) {
        navbarCollapse.classList.remove('show');
        navbarToggler.setAttribute('aria-expanded', 'false');
    }
}

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', toggleMobileMenu);
});

// Back to top button
function initBackToTop() {
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-primary position-fixed';
    backToTopBtn.style.cssText = 'bottom: 20px; right: 20px; z-index: 999; border-radius: 50%; width: 50px; height: 50px; display: none;';
    backToTopBtn.setAttribute('aria-label', 'Back to top');
    
    document.body.appendChild(backToTopBtn);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    // Scroll to top when clicked
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Initialize back to top button
initBackToTop();

// View blog post function
function viewBlogPost(postId) {
    fetch(`/api/blog/${postId}`)
        .then(response => response.json())
        .then(post => {
            // Create modal for blog post
            const modal = createBlogPostModal(post);
            document.body.appendChild(modal);
            
            // Show modal
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
            
            // Remove modal when hidden
            modal.addEventListener('hidden.bs.modal', function() {
                document.body.removeChild(modal);
            });
        })
        .catch(error => {
            console.error('Error loading blog post:', error);
            showAlert('Error loading blog post. Please try again.', 'danger');
        });
}

// Create blog post modal
function createBlogPostModal(post) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${post.title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="blog-cover mb-3">
                        ${post.cover_image_url ? 
                            `<img src="${post.cover_image_url}" alt="${post.title} cover" class="img-fluid rounded shadow-sm" style="width: 100%; max-height: 300px; object-fit: cover;"/>` : 
                            `<div class="text-center"><i class="${post.icon} fa-4x text-primary"></i></div>`
                        }
                    </div>
                    <div class="blog-meta mb-3">
                        <span class="badge bg-primary me-2">${post.category}</span>
                        <small class="text-muted">By ${post.author} • ${formatDate(post.date)}</small>
                    </div>
                    <div class="blog-content">
                        ${post.content}
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" onclick="shareBlogPost(${post.id})">Share</button>
                </div>
            </div>
        </div>
    `;
    return modal;
}

// Share blog post
function shareBlogPost(postId) {
    if (navigator.share) {
        navigator.share({
            title: 'Kambel Consult Blog',
            text: 'Check out this blog post from Kambel Consult',
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href).then(() => {
            showAlert('Link copied to clipboard!', 'success');
        });
    }
}

// Load publications dynamically
function loadPublications() {
    fetch('/api/publications')
        .then(response => response.json())
        .then(publications => {
            // Update publication cards with real data
            updatePublicationCards(publications);
        })
        .catch(error => {
            console.error('Error loading publications:', error);
        });
}

// Update publication cards
function updatePublicationCards(publications) {
    // This function can be used to dynamically update publication cards
    // when the user clicks on specific categories
    console.log('Publications loaded:', publications);
}

// Load masterclasses
let allMasterclasses = [];

function loadMasterclasses() {
    fetch('/api/masterclasses')
        .then(response => response.json())
        .then(data => {
            // Store all masterclasses globally for registration
            allMasterclasses = [...(data.upcoming || []), ...(data.previous || [])];
            
            // Update upcoming masterclasses section
            if (data.upcoming) {
                updateMasterclassSection(data.upcoming, 'upcoming');
            }
            // Update previous masterclasses section
            if (data.previous) {
                updatePreviousMasterclassesSection(data.previous);
            }
        })
        .catch(error => {
            console.error('Error loading masterclasses:', error);
        });
}

// Update masterclass section
function updateMasterclassSection(masterclasses, type = 'upcoming') {
    // Find the masterclass cards container
    // Look for section with "Upcoming Masterclasses" heading
    const heading = Array.from(document.querySelectorAll('h2, h3')).find(
        h => h.textContent.includes('Upcoming Masterclasses')
    );
    
    let masterclassContainer = null;
    
    if (heading) {
        // Find the row container after the heading section
        const section = heading.closest('section');
        if (section) {
            masterclassContainer = section.querySelector('.row.g-4');
        }
    }
    
    // Fallback: try to find any row with g-4 class that contains masterclass cards
    if (!masterclassContainer) {
        const rows = document.querySelectorAll('.row.g-4');
        for (let row of rows) {
            // Check if this row contains masterclass-related content
            if (row.querySelector('.card .btn.btn-primary')) {
                masterclassContainer = row;
                break;
            }
        }
    }
    
    if (!masterclassContainer) {
        console.log('Masterclass container not found');
        return;
    }
    
    if (masterclasses.length === 0) {
        console.log('No masterclasses to display');
        return;
    }
    
    // Clear existing cards and create new ones from API data
    masterclassContainer.innerHTML = '';
    
    masterclasses.forEach(mc => {
        // Format date
        const date = new Date(mc.date);
        const formattedDate = date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        
        // Create masterclass card
        const card = document.createElement('div');
        card.className = 'col-md-6 col-lg-4';
        
        let cardContent = '<div class="card h-100 border-0 shadow-sm hover-lift">';
        
        // Add cover image if available
        if (mc.cover_image_url) {
            cardContent += `<img src="${mc.cover_image_url}" alt="${mc.title}" class="card-img-top" style="height: 200px; object-fit: cover;">`;
        } else {
            // Add icon if no cover image
            cardContent += '<div class="card-body text-center p-4"><div class="mb-3"><i class="fas fa-chalkboard-teacher fa-3x text-primary"></i></div></div>';
        }
        
        // Add card body with content
        cardContent += `
            <div class="card-body text-center p-4">
                <h5 class="card-title mb-2">${mc.title || 'Masterclass'}</h5>
                <p class="card-text text-muted mb-3">${mc.description || 'Master the art of professional development'}</p>
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="badge bg-primary rounded-pill">${mc.instructor || 'Expert'}</span>
                    <span class="text-muted small">${mc.duration || 'TBD'}</span>
                </div>
                <div class="mb-2">
                    <small class="text-muted">${formattedDate}</small>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                    <span class="text-muted small">${mc.seats_available || 0} seats available</span>
                    <button class="btn btn-primary" onclick="registerMasterclassById(${mc.id}, '${mc.title.replace(/'/g, "\\'")}')">
                        <i class="fas fa-calendar-plus me-1"></i>Register
                    </button>
                </div>
            </div>
        </div>`;
        
        card.innerHTML = cardContent;
        
        masterclassContainer.appendChild(card);
    });
    
    console.log('Masterclasses rendered:', masterclasses.length);
}

// Update previous masterclasses section
function updatePreviousMasterclassesSection(masterclasses) {
    // Find the "Previous Masterclasses" heading
    const previousHeading = Array.from(document.querySelectorAll('h2, h3')).find(
        h => h.textContent.includes('Previous Masterclasses')
    );
    
    if (!previousHeading) {
        console.log('Previous masterclasses section not found');
        return;
    }
    
    // Find the row container right after the heading row
    // The structure is: <div class="row mt-5"> (heading row) -> <div class="row g-4"> (cards row)
    let previousContainer = null;
    
    // Method 1: Find the parent container and look for the next .row.g-4
    const headingRow = previousHeading.closest('.row');
    if (headingRow && headingRow.nextElementSibling) {
        const nextRow = headingRow.nextElementSibling;
        if (nextRow.classList.contains('g-4')) {
            previousContainer = nextRow;
        }
    }
    
    // Method 2: Find the section and get all .row.g-4, use the second one
    if (!previousContainer) {
        const section = previousHeading.closest('section');
        if (section) {
            const rows = section.querySelectorAll('.row.g-4');
            // Use the last row.g-4 (which should be the previous masterclasses section)
            previousContainer = rows.length > 1 ? rows[rows.length - 1] : null;
        }
    }
    
    // Method 3: Find the row.g-4 that comes after the "Previous Masterclasses" heading in DOM order
    if (!previousContainer) {
        const allRows = document.querySelectorAll('.row.g-4');
        let foundHeading = false;
        for (let row of allRows) {
            // Check if we've passed the previous heading
            const rect = previousHeading.getBoundingClientRect();
            const rowRect = row.getBoundingClientRect();
            if (rowRect.top > rect.top && !foundHeading) {
                previousContainer = row;
                break;
            }
        }
    }
    
    if (!previousContainer) {
        console.log('Previous masterclasses container not found');
        return;
    }
    
    renderPreviousMasterclasses(previousContainer, masterclasses);
}

function renderPreviousMasterclasses(container, masterclasses) {
    if (masterclasses.length === 0) {
        console.log('No previous masterclasses to display');
        return;
    }
    
    // Clear existing cards
    container.innerHTML = '';
    
    masterclasses.forEach(mc => {
        // Format date
        const date = new Date(mc.date);
        const formattedDate = date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        
        // Create previous masterclass card
        const card = document.createElement('div');
        card.className = 'col-md-6 col-lg-4';
        
        let cardContent = '<div class="card h-100 border-0 shadow-sm hover-lift"><div class="card-body p-0">';
        
        // Add video thumbnail with play button if video URL exists
        if (mc.video_url || mc.cover_image_url) {
            cardContent += '<div class="video-thumbnail position-relative">';
            
            // Determine image URL
            let imageUrl = mc.cover_image_url;
            
            // If no cover image but video URL exists, try to generate YouTube thumbnail
            if (!imageUrl && mc.video_url) {
                if (mc.video_url.includes('youtube.com') || mc.video_url.includes('youtu.be')) {
                    const videoId = mc.video_url.includes('youtu.be') ? 
                        mc.video_url.split('/').pop().split('?')[0] :
                        mc.video_url.split('v=')[1]?.split('&')[0];
                    if (videoId) {
                        imageUrl = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
                    }
                }
            }
            
            // Fallback to placeholder if still no image
            if (!imageUrl) {
                imageUrl = 'https://via.placeholder.com/400x200?text=Masterclass';
            }
            
            cardContent += `<img src="${imageUrl}" alt="${mc.title}" class="card-img-top" style="height: 200px; object-fit: cover;" onerror="this.src='https://via.placeholder.com/400x200?text=Masterclass'">`;
            
            // Add play button if video URL exists
            if (mc.video_url) {
                cardContent += '<div class="play-button position-absolute top-50 start-50 translate-middle"><i class="fas fa-play-circle fa-3x text-white" style="text-shadow: 0 2px 8px rgba(0,0,0,0.5);"></i></div>';
            }
            
            cardContent += '</div>';
        }
        
        // Add card body content
        cardContent += `
            <div class="p-4">
                <h5 class="card-title mb-2">${mc.title || 'Masterclass'}</h5>
                <p class="card-text text-muted mb-3">${mc.description || 'Professional development masterclass'}</p>
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="badge bg-primary rounded-pill">${mc.instructor || 'Expert'}</span>
                    <span class="text-muted small">${mc.duration || 'TBD'}</span>
                </div>
                <div class="mb-2">
                    <small class="text-muted">${formattedDate}</small>
                </div>
                <div class="d-flex gap-2">
                    ${mc.video_url ? 
                        `<button onclick="playMasterclassVideo('${mc.video_url}', '${mc.title.replace(/'/g, "\\'")}')" class="btn btn-primary btn-sm flex-fill">
                            <i class="fas fa-play me-1"></i>Watch Video
                        </button>` :
                        '<span class="text-muted small">No video available</span>'
                    }
                </div>
            </div>
        </div></div>`;
        
        card.innerHTML = cardContent;
        container.appendChild(card);
    });
    
    console.log('Previous masterclasses rendered:', masterclasses.length);
}

// Initialize newsletter form
function initNewsletterForm() {
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('newsletter-email').value;
            subscribeNewsletter(email);
        });
    }
}

// Play masterclass video in modal
function playMasterclassVideo(videoUrl, title) {
    const modalTitle = document.getElementById('videoModalTitle');
    const modalContent = document.getElementById('videoModalContent');
    
    if (modalTitle) modalTitle.textContent = title || 'Masterclass Video';
    
    let embedCode = '';
    
    if (videoUrl.includes('youtube.com') || videoUrl.includes('youtu.be')) {
        let videoId = '';
        if (videoUrl.includes('youtu.be')) {
            // Short URL format: https://youtu.be/VIDEO_ID
            videoId = videoUrl.split('youtu.be/')[1]?.split('?')[0] || videoUrl.split('youtu.be/')[1];
        } else if (videoUrl.includes('youtube.com')) {
            // Long URL format: https://www.youtube.com/watch?v=VIDEO_ID
            const urlParams = new URLSearchParams(videoUrl.split('?')[1] || '');
            videoId = urlParams.get('v') || videoUrl.split('v=')[1]?.split('&')[0];
        }
        
        if (videoId) {
            embedCode = `<iframe src="https://www.youtube.com/embed/${videoId}?autoplay=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
        } else {
            embedCode = '<p class="text-danger p-3">Could not extract video ID from URL</p>';
        }
    } else if (videoUrl.includes('vimeo.com')) {
        const videoId = videoUrl.split('/').pop().split('?')[0];
        embedCode = `<iframe src="https://player.vimeo.com/video/${videoId}?autoplay=1" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>`;
    } else {
        // Direct video file
        embedCode = `<video controls autoplay style="width: 100%; height: 100%;"><source src="${videoUrl}" type="video/mp4">Your browser does not support the video tag.</video>`;
    }
    
    if (modalContent) {
        modalContent.innerHTML = embedCode;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('videoModal'));
    modal.show();
    
    // Clean up when modal is closed
    const videoModal = document.getElementById('videoModal');
    if (videoModal) {
        videoModal.addEventListener('hidden.bs.modal', function () {
            if (modalContent) {
                modalContent.innerHTML = '<!-- Video will be loaded here -->';
            }
        }, { once: true });
    }
}

// Newsletter subscription
function subscribeNewsletter(email) {
    if (!email) {
        showAlert('Please enter a valid email address.', 'warning');
        return;
    }
    
    fetch('/api/newsletter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(result => {
        if (result.message) {
            showAlert('Successfully subscribed to newsletter!', 'success');
            // Clear the form
            document.getElementById('newsletter-email').value = '';
        } else if (result.error) {
            showAlert(result.error, 'danger');
        } else {
            showAlert('Error subscribing to newsletter. Please try again.', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error subscribing to newsletter. Please try again.', 'danger');
    });
}

// Update current year in footer
function updateCurrentYear() {
    const currentYearElement = document.getElementById('current-year');
    if (currentYearElement) {
        const currentYear = new Date().getFullYear();
        currentYearElement.textContent = currentYear;
    }
}

// Load site configuration and update page content
async function loadSiteConfig() {
    try {
        const response = await fetch('/api/site/config');
        if (response.ok) {
            const config = await response.json();
            updatePageContent(config);
        } else {
            console.error('Failed to load site configuration');
        }
    } catch (error) {
        console.error('Error loading site configuration:', error);
    }
}

// Load hero configuration
function loadHeroConfig() {
    fetch('/api/site/hero')
        .then(response => response.ok ? response.json() : null)
        .then(data => {
            if (!data) return;
            
            // Update hero title and subtitle
    const heroTitle = document.getElementById('hero-title');
    const heroSubtitle = document.getElementById('hero-subtitle');
            if (heroTitle) heroTitle.textContent = data.hero_title || 'Welcome to Kambel Consult';
            if (heroSubtitle) heroSubtitle.textContent = data.hero_subtitle || 'Your trusted partner in career development and business excellence';
    
    // Update profile section
    const profileName = document.getElementById('profile-name');
    const profileTitle = document.getElementById('profile-title');
    const profileImage = document.querySelector('.profile-photo');
    
            if (profileName) profileName.textContent = data.profile_name || 'Moses Agbesi Katamani';
            if (profileTitle) profileTitle.textContent = data.profile_title || 'Chief Executive Officer';
            if (profileImage && data.profile_picture_url) {
                profileImage.src = data.profile_picture_url;
                profileImage.alt = `${data.profile_name} - ${data.profile_title}`;
            }
            
            // Update credentials/stats
            updateHeroCredentials(data);
            
            console.log('Hero configuration loaded');
        })
        .catch(error => {
            console.error('Error loading hero configuration:', error);
        });
}

// Update hero credentials/stats
function updateHeroCredentials(data) {
    // Find credential containers
    const credentialContainers = document.querySelectorAll('.col-md-4');
    
    credentialContainers.forEach((container, index) => {
        const boldText = container.querySelector('.fw-bold.small.text-dark');
        const smallText = container.querySelector('.small[style*="color: #4a5568"]');
        
        if (boldText && smallText) {
            // Update based on icon class
            const icon = container.querySelector('.fas, .far');
            if (icon) {
                const iconClass = icon.className;
                
                if (iconClass.includes('fa-award')) {
                    // Years experience
                    boldText.textContent = `${data.years_experience} ${data.years_label}`;
                    smallText.textContent = data.years_description;
                } else if (iconClass.includes('fa-users')) {
                    // Clients
                    boldText.textContent = `${data.clients_count} ${data.clients_label}`;
                    smallText.textContent = data.clients_description;
                } else if (iconClass.includes('fa-book')) {
                    // Publications
                    boldText.textContent = `${data.publications_count} ${data.publications_label}`;
                    smallText.textContent = data.publications_description;
                }
            }
        }
    });
}

// Update page content with site configuration
function updatePageContent(config) {
    // Update site name in navigation
    const siteName = document.querySelector('.navbar-brand');
    if (siteName) {
        siteName.innerHTML = `<img src="static/css/klogo.jpeg" alt="${config.site_name}" class="site-logo me-2">${config.site_name}`;
    }
    
    // Update page title
    document.title = `${config.site_name} - ${config.site_tagline}`;
    
    // Update footer
    const footerText = document.querySelector('footer p');
    if (footerText) footerText.textContent = config.footer_text || '© 2024 Kambel Consult. All rights reserved.';
    
    console.log('Site configuration loaded and applied');
}

// Initialize all dynamic content
document.addEventListener('DOMContentLoaded', function() {
    // Load dynamic content
    loadPublications();
    loadMasterclasses();
    loadSiteConfig();
    loadHeroConfig();
    hydratePageContentBySlug();
    
    // Load additional dynamic content
    loadContactInfo();
    loadSocialMediaLinks();
    loadKICTCourses();
    loadSEOContent();
    
    // Handle hash navigation to contact form
    if (window.location.hash === '#contact') {
        setTimeout(() => {
            const contactSection = document.getElementById('contact');
            if (contactSection) {
                contactSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }, 500); // Wait for page to fully load
    }
});

// Hydrate static pages (education.html, career.html, etc.) from Django by slug
function hydratePageContentBySlug() {
    const path = window.location.pathname;
    const slug = path.replace(/^\/+|\.html$/g, '').split('/').pop();
    const editableSlugs = [
        'education', 'career', 'personal-development', 'business',
        'course-books', 'guidance-books', 'inspirational-books', 'literature'
    ];
    if (!slug || slug === 'index' || editableSlugs.indexOf(slug) === -1) return;

    fetch(`/api/site/page/${slug}`)
        .then(r => r.ok ? r.json() : null)
        .then(data => {
            if (!data) return;
            const heroH1 = document.querySelector('.section-header h2, .page-hero h1, h1');
            const heroLead = document.querySelector('.section-header .lead, .page-hero .lead, .lead');
            if (heroH1 && data.hero_title) heroH1.textContent = data.hero_title;
            if (heroLead && data.hero_subtitle) heroLead.textContent = data.hero_subtitle;
            const bodyContainer = document.querySelector('.page-body, .content, main');
            if (bodyContainer && data.body_html) bodyContainer.innerHTML = data.body_html;
            const heroImg = document.querySelector('.page-hero img, .hero-image img');
            if (heroImg && data.hero_image_url) heroImg.src = data.hero_image_url;
        })
        .catch(() => {});
}

// Load contact information
function loadContactInfo() {
    fetch('/api/site/contact-info')
        .then(response => response.ok ? response.json() : null)
        .then(data => {
            if (!data || !Array.isArray(data)) return;
            
            // Process contact info array from API
            const contactData = {};
            data.forEach(item => {
                if (item.type === 'email') {
                    contactData.email = item.value;
                } else if (item.type === 'phone') {
                    contactData.phone = item.value;
                } else if (item.type === 'address') {
                    contactData.address = item.value;
                } else if (item.type === 'location') {
                    contactData.location = item.value;
                }
            });
            
            // Update contact email
            const emailElements = document.querySelectorAll('[data-contact="email"]');
            emailElements.forEach(el => el.textContent = contactData.email || 'Not provided');
            
            // Update contact phone
            const phoneElements = document.querySelectorAll('[data-contact="phone"]');
            phoneElements.forEach(el => el.textContent = contactData.phone || 'Not provided');
            
            // Update contact address
            const addressElements = document.querySelectorAll('[data-contact="address"]');
            addressElements.forEach(el => el.textContent = contactData.address || 'Not provided');
            
            // Update contact location
            const locationElements = document.querySelectorAll('[data-contact="location"]');
            locationElements.forEach(el => el.textContent = contactData.location || 'Not provided');
            
            console.log('Contact information loaded');
        })
        .catch(() => {});
}

// Load social media links
function loadSocialMediaLinks() {
    fetch('/api/site/social-media')
        .then(response => response.ok ? response.json() : null)
        .then(data => {
            if (!data || !Array.isArray(data)) return;
            
            const socialContainer = document.querySelector('#social-links');
            if (!socialContainer) return;
            
            // Sort by order
            data.sort((a, b) => a.order - b.order);
            
            // Clear existing content
            socialContainer.innerHTML = '';
            
            // Add social media links
            data.forEach(link => {
                const linkElement = document.createElement('a');
                linkElement.href = link.url;
                linkElement.className = 'text-white me-3 d-inline-flex align-items-center';
                linkElement.style.textDecoration = 'none';
                linkElement.target = '_blank';
                linkElement.rel = 'noopener noreferrer';
                
                // Capitalize platform name for title attribute
                const platformName = link.platform.charAt(0).toUpperCase() + link.platform.slice(1);
                linkElement.title = platformName;
                
                // Create icon only (no text)
                linkElement.innerHTML = `
                    <i class="${resolveSocialIconClass(link.icon_class, link.platform)} fa-lg"></i>
                `;
                socialContainer.appendChild(linkElement);
            });
            
            console.log('Social media links loaded');
        })
        .catch(() => {});
}

// Resolve icon class with safe fallbacks per platform
function resolveSocialIconClass(iconClass, platform) {
    if (iconClass && typeof iconClass === 'string' && iconClass.trim().length > 0) {
        return iconClass;
    }
    const normalized = (platform || '').toLowerCase();
    const defaults = {
        facebook: 'fab fa-facebook',
        twitter: 'fab fa-twitter',
        x: 'fab fa-x-twitter', // alternate key if backend uses 'x'
        linkedin: 'fab fa-linkedin',
        instagram: 'fab fa-instagram',
        youtube: 'fab fa-youtube',
        tiktok: 'fab fa-tiktok'
    };
    return defaults[normalized] || 'fas fa-share-alt';
}

// Load KICT courses
function loadKICTCourses() {
    fetch('/api/kict/courses')
        .then(response => response.ok ? response.json() : null)
        .then(data => {
            if (!data || !Array.isArray(data)) return;
            
            const coursesContainer = document.querySelector('#kict-courses');
            if (!coursesContainer) return;
            
            // Clear existing content
            coursesContainer.innerHTML = '';
            
            // Add courses
            data.forEach(course => {
                const courseElement = document.createElement('div');
                courseElement.className = 'col-md-6 mb-4';
                courseElement.innerHTML = `
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">${course.title}</h5>
                            <p class="card-text">${course.description}</p>
                            <ul class="list-unstyled">
                                <li><strong>Duration:</strong> ${course.duration}</li>
                                <li><strong>Instructor:</strong> ${course.instructor}</li>
                                <li><strong>Start Date:</strong> ${course.start_date}</li>
                                <li><strong>Price:</strong> $${course.price}</li>
                            </ul>
                        </div>
                    </div>
                `;
                coursesContainer.appendChild(courseElement);
            });
            
            console.log('KICT courses loaded');
        })
        .catch(() => {});
}

// Load SEO content
function loadSEOContent() {
    const currentPage = window.location.pathname.replace(/^\/+|\.html$/g, '').split('/').pop() || 'home';
    
    fetch(`/api/site/seo/${currentPage}`)
        .then(response => response.ok ? response.json() : null)
        .then(data => {
            if (!data) return;
            
            // Update page title
            if (data.title) {
                document.title = data.title;
            }
            
            // Update meta description
            let metaDesc = document.querySelector('meta[name="description"]');
            if (!metaDesc) {
                metaDesc = document.createElement('meta');
                metaDesc.name = 'description';
                document.head.appendChild(metaDesc);
            }
            metaDesc.content = data.description;
            
            // Update meta keywords
            let metaKeywords = document.querySelector('meta[name="keywords"]');
            if (!metaKeywords) {
                metaKeywords = document.createElement('meta');
                metaKeywords.name = 'keywords';
                document.head.appendChild(metaKeywords);
            }
            metaKeywords.content = data.keywords;
            
            // Update Open Graph tags
            let ogTitle = document.querySelector('meta[property="og:title"]');
            if (!ogTitle) {
                ogTitle = document.createElement('meta');
                ogTitle.setAttribute('property', 'og:title');
                document.head.appendChild(ogTitle);
            }
            ogTitle.content = data.og_title || data.title;
            
            let ogDesc = document.querySelector('meta[property="og:description"]');
            if (!ogDesc) {
                ogDesc = document.createElement('meta');
                ogDesc.setAttribute('property', 'og:description');
                document.head.appendChild(ogDesc);
            }
            ogDesc.content = data.og_description || data.description;
            
            if (data.og_image_url) {
                let ogImage = document.querySelector('meta[property="og:image"]');
                if (!ogImage) {
                    ogImage = document.createElement('meta');
                    ogImage.setAttribute('property', 'og:image');
                    document.head.appendChild(ogImage);
                }
                ogImage.content = data.og_image_url;
            }
            
            console.log('SEO content loaded');
        })
        .catch(() => {});
}
