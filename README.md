# 🗳️ Django Online Voting System

A secure, modern web-based voting system built with Django, MySQL, Bootstrap, and SweetAlert. This application provides a complete digital voting experience similar to India's electronic voting systems.

## ✨ Features

### 🔐 Security & Authentication
- **Secure User Registration & Login** with Django's built-in authentication
- **Admin Authentication** with separate admin panel
- **Session Management** with Django sessions
- **Vote Integrity** - One vote per user policy
- **Anonymous Voting** - No vote-user linkage stored
- **CSRF Protection** built into Django

### 🎨 Modern UI/UX
- **Responsive Design** with Bootstrap 5
- **Beautiful Gradient Themes** and animations
- **SweetAlert Integration** for elegant notifications
- **Mobile-Friendly** interface
- **Accessibility Compliant** design
- **Crispy Forms** for beautiful form rendering

### 📊 Admin Features
- **Django Admin Panel** with custom interfaces
- **Real-time Dashboard** with voting statistics
- **Candidate Management** - Add/Delete candidates with images
- **User Management** with pagination
- **Live Results** with percentage calculations
- **Secure Admin Panel** with role-based access

### 🗳️ Voting Features
- **Intuitive Voting Interface** with candidate cards
- **Vote Confirmation** with SweetAlert dialogs
- **Real-time Vote Counting**
- **Vote Success Confirmation**
- **Duplicate Vote Prevention**
- **Public Results Page**

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Django 4.2** - Web framework
- **MySQL** - Database with mysqlclient
- **Django Authentication** - User management
- **Django Admin** - Administrative interface
- **Crispy Forms** - Form rendering

### Frontend
- **HTML5** - Structure
- **CSS3** - Custom styling with gradients
- **Bootstrap 5** - Responsive UI framework
- **JavaScript** - Client-side interactions
- **SweetAlert2** - Beautiful alerts and confirmations
- **Font Awesome** - Icons

## 📋 Requirements

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd django-online-voting-system
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Database
Edit `voting_system/settings.py` and update the database configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'voting_system',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. Set Up Database and Initial Data
```bash
python run_django.py
```

This will:
- Run database migrations
- Create an admin user (admin/admin123)
- Add sample candidates
- Create a sample election
- Start the development server

### 5. Manual Setup (Alternative)
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user and sample data
python manage.py setup_voting --create-admin --create-candidates --create-election

# Collect static files
python manage.py collectstatic

# Run server
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 👥 Default Credentials

### Admin Login
- **Username:** `admin`
- **Password:** `admin123`
- **Django Admin:** `http://localhost:8000/admin/`
- **Voting Admin:** `http://localhost:8000/admin/login/`

### Sample Candidates
The setup creates sample candidates:
- Rajesh Kumar (Indian National Congress)
- Priya Sharma (Bharatiya Janata Party)
- Amit Singh (Aam Aadmi Party)
- Sunita Devi (Independent Candidate)

## 📱 Usage Guide

### For Voters
1. **Register** - Create an account at `/register/`
2. **Login** - Sign in with your credentials at `/login/`
3. **Vote** - Select your preferred candidate and confirm at `/vote/`
4. **Success** - View confirmation of your vote at `/vote/success/`
5. **Results** - Check live results at `/results/`

### For Administrators
1. **Admin Login** - Use admin credentials at `/admin/login/`
2. **Django Admin** - Full admin interface at `/admin/`
3. **Dashboard** - View statistics at `/admin/dashboard/`
4. **Manage Candidates** - Add/remove candidates
5. **Manage Users** - View and manage registered users
6. **Monitor Results** - View real-time voting results

## 🗄️ Database Models

### User Model (Custom)
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    has_voted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
```

### Candidate Model
```python
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='candidates/', blank=True)
    is_active = models.BooleanField(default=True)
```

### Vote Model
```python
class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)
    # No user reference for anonymity
```

### Election Model
```python
class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
```

## 🔒 Security Features

- **Django Authentication** with secure password hashing
- **Session Management** with configurable timeouts
- **CSRF Protection** on all forms
- **SQL Injection Prevention** with Django ORM
- **XSS Protection** with Django templates
- **Anonymous Voting** - votes not linked to users
- **One Vote Policy** - users cannot vote multiple times
- **Admin Role Separation** - distinct admin users

## 🎨 UI Features

- **Gradient Backgrounds** for modern appearance
- **Hover Effects** on interactive elements
- **Smooth Animations** and transitions
- **Responsive Design** for all screen sizes
- **Loading States** for better user feedback
- **Toast Notifications** for non-intrusive alerts
- **Crispy Forms** for beautiful form rendering

## 🔧 Management Commands

### Create Admin User
```bash
python manage.py create_admin
```

### Setup Complete System
```bash
python manage.py setup_voting --create-admin --create-candidates --create-election
```

### Django Admin Commands
```bash
python manage.py createsuperuser  # Create Django superuser
python manage.py shell           # Django shell
python manage.py dbshell         # Database shell
```

## 🔧 Customization

### Adding New Features
1. Create new views in `voting/views.py`
2. Add URL patterns in `voting/urls.py`
3. Create templates in `templates/voting/`
4. Add models in `voting/models.py`
5. Create and run migrations

### Changing Styles
Edit `static/css/style.css` for custom styling:
```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}
```

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
python manage.py flush
python manage.py migrate
python manage.py setup_voting --create-admin --create-candidates
```

### Static Files Issues
```bash
python manage.py collectstatic --clear
```

### Permission Issues
```bash
# Create new admin user
python manage.py create_admin
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support and questions:
- Check Django documentation
- Review the troubleshooting section
- Create an issue on GitHub

## 🎯 Future Enhancements

- [ ] Email verification for registration
- [ ] Two-factor authentication
- [ ] Multiple election support
- [ ] Advanced analytics dashboard
- [ ] REST API for mobile apps
- [ ] Real-time notifications
- [ ] Audit trail and logging
- [ ] Export results to PDF/Excel
- [ ] Multi-language support

---

**Built with ❤️ using Django for democratic participation**