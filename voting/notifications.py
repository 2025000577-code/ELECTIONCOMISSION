"""
Notification System for Voting Application
Handles in-app notifications for users and admins
"""

from django.db import models
from django.utils import timezone
from .models import User


class Notification(models.Model):
    """Model for storing notifications"""
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


def create_notification(user, title, message, notification_type='info', link=None):
    """Helper function to create notifications"""
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        link=link
    )


def notify_user_verified(user, admin):
    """Notify user when their account is verified"""
    return create_notification(
        user=user,
        title="Account Verified! 🎉",
        message=f"Your account has been verified by {admin.full_name}. You can now cast your vote!",
        notification_type='success',
        link='/vote/'
    )


def notify_admin_new_registration(admin, new_user):
    """Notify admin when new user registers"""
    return create_notification(
        user=admin,
        title="New User Registration",
        message=f"{new_user.full_name} ({new_user.email}) has registered and needs verification.",
        notification_type='info',
        link='/voting-admin/verify-users/'
    )


def notify_vote_cast(user):
    """Notify user after successful vote"""
    return create_notification(
        user=user,
        title="Vote Recorded Successfully! ✓",
        message="Your vote has been securely recorded. Thank you for participating!",
        notification_type='success',
        link='/results/live/'
    )


def notify_election_started(user):
    """Notify user when election starts"""
    return create_notification(
        user=user,
        title="Election Started!",
        message="The election is now open. Cast your vote now!",
        notification_type='info',
        link='/vote/'
    )


def notify_election_ending_soon(user, hours_left):
    """Notify user when election is ending soon"""
    return create_notification(
        user=user,
        title="Election Ending Soon! ⏰",
        message=f"Only {hours_left} hours left to vote. Don't miss your chance!",
        notification_type='warning',
        link='/vote/'
    )
