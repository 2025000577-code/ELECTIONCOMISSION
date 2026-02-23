# 🌍 Environment Setup Guide

## Quick Setup (Automated)

### Option 1: One-Command Setup
```bash
python setup_environment.py
```

This script will:
- ✅ Check Python version compatibility
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Set up environment variables
- ✅ Create necessary directories
- ✅ Run database migrations
- ✅ Create admin user and sample data

### Option 2: Manual Setup

#### 1. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate.bat
# Mac/Linux:
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
```

#### 4. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user and sample data
python manage.py setup_voting --create-admin --create-candidates
```

#### 5. Create Directories
```bash
mkdir -p media/id_proofs logs staticfiles
```

## Environment Files

### Development (.env)
```env
SECRET_KEY=django-insecure-voting-system-dev-key-2024
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*
DB_ENGINE=sqlite
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Production (.env.production)
```env
SECRET_KEY=your-super-secret-production-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=mysql
DB_NAME=voting_system_prod
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
SECURE_SSL_REDIRECT=True
```

## Environment Variables Reference

### Django Core
| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `SECRET_KEY` | Django secret key | Generated | `django-insecure-...` |
| `DEBUG` | Debug mode | `True` | `False` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,...` | `yourdomain.com` |

### Database
| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DB_ENGINE` | Database type | `sqlite` | `mysql` |
| `DB_NAME` | Database name | `voting_system` | `voting_prod` |
| `DB_USER` | Database user | `root` | `voting_user` |
| `DB_PASSWORD` | Database password | `` | `secure_password` |
| `DB_HOST` | Database host | `localhost` | `db.example.com` |
| `DB_PORT` | Database port | `3306` | `3306` |

### Email
| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `EMAIL_BACKEND` | Email backend | `console` | `smtp` |
| `EMAIL_HOST` | SMTP host | `smtp.gmail.com` | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` | `587` |
| `EMAIL_USE_TLS` | Use TLS | `True` | `True` |
| `EMAIL_HOST_USER` | Email username | `` | `admin@example.com` |
| `EMAIL_HOST_PASSWORD` | Email password | `` | `app_password` |

### Security
| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `SESSION_COOKIE_AGE` | Session timeout | `3600` | `1800` |
| `SESSION_COOKIE_SECURE` | HTTPS only cookies | `False` | `True` |
| `SECURE_SSL_REDIRECT` | Force HTTPS | `False` | `True` |
| `SECURE_HSTS_SECONDS` | HSTS max age | `0` | `31536000` |

## Database Configurations

### SQLite (Development)
```env
DB_ENGINE=sqlite
```
- ✅ No additional setup required
- ✅ Perfect for development
- ✅ File-based database
- ❌ Not suitable for production

### MySQL (Production)
```env
DB_ENGINE=mysql
DB_NAME=voting_system
DB_USER=voting_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=3306
```

#### MySQL Setup:
```sql
CREATE DATABASE voting_system;
CREATE USER 'voting_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON voting_system.* TO 'voting_user'@'localhost';
FLUSH PRIVILEGES;
```

## Email Configurations

### Console Backend (Development)
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
- ✅ Prints emails to console
- ✅ No SMTP setup required
- ✅ Perfect for development

### SMTP Backend (Production)
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### Gmail Setup:
1. Enable 2-factor authentication
2. Generate app password
3. Use app password in `EMAIL_HOST_PASSWORD`

## Directory Structure

```
voting-system/
├── .env                    # Environment variables
├── .env.example           # Environment template
├── .env.production        # Production environment
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── setup_environment.py  # Automated setup script
├── manage.py            # Django management
├── db.sqlite3           # SQLite database (dev)
├── media/               # User uploads
│   └── id_proofs/       # ID card images
├── logs/                # Application logs
├── staticfiles/         # Collected static files
├── venv/               # Virtual environment
├── voting_system/      # Django project
├── voting/             # Main app
├── templates/          # HTML templates
└── static/            # Static assets
```

## Security Considerations

### Development
- ✅ Debug mode enabled
- ✅ Console email backend
- ✅ SQLite database
- ✅ HTTP allowed
- ⚠️ Weak secret key (acceptable for dev)

### Production
- ✅ Debug mode disabled
- ✅ SMTP email backend
- ✅ MySQL database
- ✅ HTTPS enforced
- ✅ Strong secret key
- ✅ HSTS enabled
- ✅ Secure cookies

## Deployment Environments

### Local Development
```bash
# Use default .env
python manage.py runserver
```

### Staging
```bash
# Use staging environment
cp .env.staging .env
python manage.py runserver 0.0.0.0:8000
```

### Production
```bash
# Use production environment
cp .env.production .env
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn voting_system.wsgi:application
```

## Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError: No module named 'dotenv'**
```bash
pip install python-dotenv
```

**Issue: Database connection failed**
- Check database credentials in `.env`
- Ensure database server is running
- Verify database exists

**Issue: Static files not loading**
```bash
python manage.py collectstatic
```

**Issue: Permission denied on media folder**
```bash
chmod 755 media/
chmod 755 media/id_proofs/
```

### Environment Validation

Check your environment setup:
```bash
python manage.py check
python manage.py check --deploy  # Production checks
```

## Best Practices

### Security
1. **Never commit `.env` files** to version control
2. **Use strong secret keys** in production
3. **Enable HTTPS** in production
4. **Use environment-specific settings**
5. **Regularly rotate secrets**

### Development
1. **Use virtual environments**
2. **Keep dependencies updated**
3. **Use different databases** for dev/prod
4. **Test with production-like settings**

### Deployment
1. **Use environment variables** for all secrets
2. **Validate environment** before deployment
3. **Use process managers** (systemd, supervisor)
4. **Monitor logs** and performance
5. **Backup databases** regularly

## Quick Commands

```bash
# Setup everything
python setup_environment.py

# Start development server
python manage.py runserver

# Start for Android access
python start_for_android.py

# Create admin user
python manage.py setup_voting --create-admin

# Run tests
python manage.py test

# Check deployment readiness
python manage.py check --deploy
```

---

**Environment Status:** ✅ Fully Configured
**Auto-Setup Available:** ✅ Yes (`setup_environment.py`)
**Production Ready:** ✅ Yes (with proper `.env.production`)