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
                "name": "Josh Adkins",
                "title": "Data Engineer & Tech Specialist",
                "description": "I design and build scalable data pipelines, create intuitive user experiences, and develop innovative solutions for Healthcare and Fintech industries.",
                "about": "I'm a passionate Data Engineer with specialized expertise in UI/UX design, Healthcare technology, and Fintech solutions. I architect robust data pipelines that power mission-critical applications while ensuring exceptional user experiences.",
                "email": "business.joshadkins@gmail.com",
                "phone": "+1 (555) 123-4567",
                "location": "Open to Remote",
                "social_links": {
                    "github": "https://github.com/yourusername",
                    "linkedin": "https://linkedin.com/in/yourusername",
                    "twitter": "https://twitter.com/yourusername"
                }
            },
            "work_experience": [
                {
                    "company": "Cedar",
                    "period": "June 2025 - Present",
                    "title": "Solutions Architect",
                    "description": "I serve as a Solutions Architect, partnering with enterprise healthcare clients to integrate their platforms with Cedar Pay, Cedar Pre, and Cedar Cover. My role focuses on designing scalable, secure architectures that simplify the complexity of healthcare billing, streamline revenue cycle operations, and ensure seamless interoperability with EHRs and legacy systems.",
                    "technologies": ["Solutions Architecture", "Healthcare APIs", "EHR Integration", "Revenue Cycle"]
                },
                {
                    "company": "Midwest DataWorks",
                    "period": "Feb 2025 - Present",
                    "title": "Founder",
                    "description": "I serve as founder of Midwest DataWorks, an advisory-focused side venture where we help teams make smarter decisions about data. From modern cloud architecture to healthcare analytics strategy, we guide partners through complex problems with clear thinking and pragmatic design.",
                    "technologies": ["Data Strategy", "Cloud Architecture", "Healthcare Analytics", "Advisory"]
                },
                {
                    "company": "Nordic Consulting Partners",
                    "period": "Feb 2025 - May 2025",
                    "title": "Solutions Architect & Data Engineer",
                    "description": "I worked as a Solutions Architect and Data Engineer focused on building scalable, cloud-native data infrastructure for enterprise healthcare clients. I designed and implemented robust pipelines across Azure and AWS ecosystems—including Databricks, ADF, and Spark—to streamline ingestion, transformation, and delivery across structured and unstructured data domains.",
                    "technologies": ["Azure Databricks", "Apache Spark", "ADF", "Cloud Migration"]
                },
                {
                    "company": "Tegria",
                    "period": "Dec 2023 - Feb 2025",
                    "title": "Data Engineering Consultant",
                    "description": "I served as a Data Engineering Consultant, delivering cloud-native data solutions for healthcare organizations navigating modernization. I designed and built scalable pipelines across Azure Databricks, Synapse, and ADF to support high-volume, high-complexity workloads.",
                    "technologies": ["Azure Synapse", "Data Governance", "Healthcare Modernization", "Data Warehousing"]
                },
                {
                    "company": "Health Catalyst",
                    "period": "Aug 2021 - Dec 2023",
                    "title": "Senior Analytics Engineer → Senior Analytics Director",
                    "description": "At Health Catalyst, I held dual roles as Senior Analytics Engineer and later as Senior Analytics Director, delivering end-to-end data solutions for healthcare clients. As Director, I led a team of consulting analysts through high-stakes analytics initiatives, translating client goals into actionable roadmaps.",
                    "technologies": ["Team Leadership", "Tableau", "SAFe Agile", "HIPAA Compliance"]
                },
                {
                    "company": "Corewell Health",
                    "period": "July 2016 - Aug 2021",
                    "title": "Senior Application Developer",
                    "description": "I advanced through four increasingly technical and strategic roles over five years—culminating as a Senior Application Developer focused on data engineering and application architecture. I led the development of secure, scalable data pipelines, integrating tools like Denodo, Snowflake, Azure, and Epic.",
                    "technologies": ["Snowflake", "Epic Integration", "Mentoring", "Application Architecture"]
                }
            ],
            "stats": {
                "projects": "25+",
                "experience": "8+",
                "clients": "15+"
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

@app.route('/api/experience')
def api_experience():
    """API endpoint for work experience data"""
    portfolio_data = load_portfolio_data()
    return jsonify(portfolio_data.get('work_experience', []))

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000) 