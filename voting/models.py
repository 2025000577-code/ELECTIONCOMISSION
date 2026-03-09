from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    has_voted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Identity Verification Fields
    id_card_number = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text="National ID or Voter ID number")
    id_card_proof = models.FileField(upload_to='id_proofs/', null=True, blank=True, help_text="Upload ID card image")
    is_verified = models.BooleanField(default=False, help_text="Admin verification status")
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_users')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']
    
    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='voting_users',
        related_query_name='voting_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='voting_users',
        related_query_name='voting_user',
    )
    
    class Meta:
        db_table = 'voting_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    def save(self, *args, **kwargs):
        # Set staff status for admin users
        if self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)


class Candidate(models.Model):
    """Model for election candidates"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, help_text="Party or description")
    # Removed image field to avoid Pillow dependency issues
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'voting_candidates'
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.description}"


class Vote(models.Model):
    """Model for storing votes"""
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)
    # Note: We don't store user reference to maintain anonymity
    
    class Meta:
        db_table = 'voting_votes'
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        ordering = ['-voted_at']
    
    def __str__(self):
        return f"Vote for {self.candidate.name} at {self.voted_at}"


class Election(models.Model):
    """Model for managing elections"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'voting_elections'
        verbose_name = 'Election'
        verbose_name_plural = 'Elections'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('End date must be after start date.')
    
    @property
    def is_ongoing(self):
        """Check if election is currently ongoing"""
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active
    
    @property
    def total_votes(self):
        """Get total votes in this election"""
        return Vote.objects.count()  # Simplified for single election system



class Notification(models.Model):
    """Model for in-app notifications"""
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'voting_notifications'
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
