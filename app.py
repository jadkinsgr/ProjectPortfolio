from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_mail import Mail, Message
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Load portfolio data
def load_portfolio_data():
    """Load portfolio data from JSON files"""
    try:
        with open('data/portfolio.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default data if file doesn't exist
        return {
            "personal_info": {
                "name": "Your Name",
                "title": "Full Stack Developer & UI/UX Designer",
                "description": "I create beautiful, functional, and user-centered digital experiences that solve real-world problems.",
                "about": "I'm a passionate developer with over X years of experience in creating digital solutions that bridge the gap between design and technology. I enjoy turning complex problems into simple, beautiful, and intuitive designs.",
                "email": "your.email@example.com",
                "phone": "+1 (555) 123-4567",
                "location": "Your City, Country",
                "social_links": {
                    "github": "https://github.com/yourusername",
                    "linkedin": "https://linkedin.com/in/yourusername",
                    "twitter": "https://twitter.com/yourusername"
                }
            },
            "stats": {
                "projects": "50+",
                "experience": "3+",
                "clients": "20+"
            },
            "projects": [
                {
                    "title": "E-Commerce Platform",
                    "description": "A full-stack e-commerce solution built with React and Node.js, featuring user authentication, payment processing, and inventory management.",
                    "technologies": ["React", "Node.js", "MongoDB", "Stripe"],
                    "demo_url": "#",
                    "github_url": "#",
                    "image": "fas fa-code"
                },
                {
                    "title": "Task Management App",
                    "description": "A responsive task management application with drag-and-drop functionality, real-time updates, and team collaboration features.",
                    "technologies": ["Vue.js", "Firebase", "CSS3", "PWA"],
                    "demo_url": "#",
                    "github_url": "#",
                    "image": "fas fa-mobile-alt"
                },
                {
                    "title": "Analytics Dashboard",
                    "description": "An interactive data visualization dashboard for business analytics with real-time charts, filtering, and export capabilities.",
                    "technologies": ["D3.js", "Python", "Flask", "PostgreSQL"],
                    "demo_url": "#",
                    "github_url": "#",
                    "image": "fas fa-chart-line"
                }
            ],
            "skills": {
                "Frontend": [
                    {"name": "HTML5", "icon": "fab fa-html5"},
                    {"name": "CSS3", "icon": "fab fa-css3-alt"},
                    {"name": "JavaScript", "icon": "fab fa-js-square"},
                    {"name": "React", "icon": "fab fa-react"},
                    {"name": "Vue.js", "icon": "fab fa-vuejs"}
                ],
                "Backend": [
                    {"name": "Python", "icon": "fab fa-python"},
                    {"name": "Node.js", "icon": "fab fa-node-js"},
                    {"name": "Flask", "icon": "fas fa-server"},
                    {"name": "Django", "icon": "fas fa-database"}
                ],
                "Tools": [
                    {"name": "Git", "icon": "fab fa-git-alt"},
                    {"name": "Docker", "icon": "fab fa-docker"},
                    {"name": "AWS", "icon": "fab fa-aws"},
                    {"name": "PostgreSQL", "icon": "fas fa-database"}
                ]
            },
            "blog_posts": [
                {
                    "title": "Building Modern Web Applications",
                    "excerpt": "Learn how to create scalable and maintainable web applications using modern frameworks and best practices.",
                    "date": "2024-01-15",
                    "category": "Web Development",
                    "url": "#"
                },
                {
                    "title": "The Future of Frontend Development",
                    "excerpt": "Exploring upcoming trends and technologies that will shape the future of frontend development.",
                    "date": "2024-01-10",
                    "category": "Technology",
                    "url": "#"
                }
            ]
        }

@app.route('/')
def index():
    """Main portfolio page"""
    portfolio_data = load_portfolio_data()
    return render_template('index.html', **portfolio_data)

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Validate form data
        if not all([name, email, subject, message]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Send email if mail is configured
        if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
            msg = Message(
                subject=f"Portfolio Contact: {subject}",
                recipients=[app.config['MAIL_DEFAULT_SENDER']],
                reply_to=email
            )
            msg.body = f"""
            New message from your portfolio contact form:
            
            Name: {name}
            Email: {email}
            Subject: {subject}
            
            Message:
            {message}
            """
            
            mail.send(msg)
            return jsonify({'success': True, 'message': 'Message sent successfully!'})
        else:
            # Log to console if email not configured
            print(f"Contact form submission from {name} ({email}): {message}")
            return jsonify({'success': True, 'message': 'Message received! (Email not configured in development)'})
    
    except Exception as e:
        print(f"Error sending contact form: {e}")
        return jsonify({'success': False, 'message': 'There was an error sending your message. Please try again.'}), 500

@app.route('/api/projects')
def api_projects():
    """API endpoint for projects data"""
    portfolio_data = load_portfolio_data()
    return jsonify(portfolio_data.get('projects', []))

@app.route('/api/blog')
def api_blog():
    """API endpoint for blog posts data"""
    portfolio_data = load_portfolio_data()
    return jsonify(portfolio_data.get('blog_posts', []))

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000) 