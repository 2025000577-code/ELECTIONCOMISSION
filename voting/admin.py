from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Candidate, Vote, Election


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model"""
    list_display = ('email', 'full_name', 'username', 'has_voted', 'is_admin', 'is_active', 'date_joined')
    list_filter = ('has_voted', 'is_admin', 'is_active', 'date_joined')
    search_fields = ('email', 'full_name', 'username')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Voting Information', {
            'fields': ('full_name', 'has_voted', 'is_admin')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Personal Information', {
            'fields': ('email', 'full_name', 'is_admin')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing user
            return ('has_voted',)  # Make has_voted readonly when editing
        return ()


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    """Admin interface for Candidate model"""
    list_display = ('name', 'description', 'vote_count_display', 'vote_percentage_display', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('vote_count_display', 'vote_percentage_display', 'created_at')
    
    fieldsets = (
        ('Candidate Information', {
            'fields': ('name', 'description', 'image', 'is_active')
        }),
        ('Statistics', {
            'fields': ('vote_count_display', 'vote_percentage_display', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def vote_count_display(self, obj):
        """Display vote count with styling"""
        count = obj.vote_count
        if count > 0:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', count)
        return count
    vote_count_display.short_description = 'Total Votes'
    
    def vote_percentage_display(self, obj):
        """Display vote percentage with styling"""
        percentage = obj.vote_percentage
        if percentage > 0:
            return format_html('<span style="color: blue; font-weight: bold;">{:.1f}%</span>', percentage)
        return '0%'
    vote_percentage_display.short_description = 'Vote Percentage'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Admin interface for Vote model"""
    list_display = ('candidate', 'voted_at')
    list_filter = ('candidate', 'voted_at')
    search_fields = ('candidate__name',)
    ordering = ('-voted_at',)
    readonly_fields = ('candidate', 'voted_at')
    
    def has_add_permission(self, request):
        """Disable adding votes through admin"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable changing votes through admin"""
        return False


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    """Admin interface for Election model"""
    list_display = ('title', 'start_date', 'end_date', 'is_ongoing_display', 'is_active', 'total_votes_display')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('is_ongoing_display', 'total_votes_display', 'created_at')
    
    fieldsets = (
        ('Election Information', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Statistics', {
            'fields': ('is_ongoing_display', 'total_votes_display', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_ongoing_display(self, obj):
        """Display if election is ongoing with styling"""
        if obj.is_ongoing:
            return format_html('<span style="color: green; font-weight: bold;">✓ Ongoing</span>')
        return format_html('<span style="color: red;">✗ Not Active</span>')
    is_ongoing_display.short_description = 'Status'
    
    def total_votes_display(self, obj):
        """Display total votes with styling"""
        count = obj.total_votes
        if count > 0:
            return format_html('<span style="color: blue; font-weight: bold;">{}</span>', count)
        return count
    total_votes_display.short_description = 'Total Votes'


# Customize admin site
admin.site.site_header = "Online Voting System Administration"
admin.site.site_title = "Voting Admin"
admin.site.index_title = "Welcome to Online Voting System"