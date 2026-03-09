from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.core.paginator import Paginator
from django.utils import timezone
import json
import logging

from .models import User, Candidate, Vote, Election
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AdminLoginForm, CandidateForm, VoteForm

# Security logger
security_logger = logging.getLogger('voting.security')

def get_client_ip(request):
    """Get client IP address for security logging"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    """Home page view"""
    context = {
        'total_users': User.objects.count(),
        'total_votes': Vote.objects.count(),
        'total_candidates': Candidate.objects.filter(is_active=True).count(),
    }
    return render(request, 'voting/home.html', context)


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('vote' if not request.user.is_admin else 'admin_dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Your account is pending verification. You will be notified once approved.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'voting/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('vote' if not request.user.is_admin else 'admin_dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.full_name}!')
                return redirect('vote' if not user.is_admin else 'admin_dashboard')
        messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'voting/login.html', {'form': form})


def admin_login_view(request):
    """Admin login view - same as user login but for admins with enhanced security"""
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                
                # Log successful admin login
                security_logger.info(f"Admin user {user.email} successfully logged in from IP {get_client_ip(request)}")
                
                messages.success(request, f'Welcome, Admin {user.full_name}!')
                return redirect('admin_dashboard')
            else:
                # Log failed admin login attempt
                security_logger.warning(f"Failed admin login attempt for email '{username}' from IP {get_client_ip(request)}")
                messages.error(request, 'Invalid admin credentials or not an admin user.')
        else:
            # Log invalid form submission
            security_logger.warning(f"Invalid admin login form submission from IP {get_client_ip(request)}")
            messages.error(request, 'Invalid email or password.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'voting/admin_login.html', {'form': form})


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def vote_view(request):
    """Voting page view with enhanced security"""
    if request.user.is_admin:
        security_logger.warning(f"Admin user {request.user.email} attempted to access voting page from IP {get_client_ip(request)}")
        return redirect('admin_dashboard')
    
    # Check if user is verified
    if not request.user.is_verified:
        messages.warning(request, 'Your account is pending verification. Please wait for admin approval.')
        return render(request, 'voting/verification_pending.html')
    
    if request.user.has_voted:
        security_logger.info(f"User {request.user.email} attempted to vote again from IP {get_client_ip(request)}")
        return redirect('vote_success')
    
    candidates = Candidate.objects.filter(is_active=True).order_by('name')
    
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        
        # Enhanced security validation
        if not candidate_id or not candidate_id.isdigit():
            security_logger.warning(f"Invalid candidate ID '{candidate_id}' submitted by user {request.user.email} from IP {get_client_ip(request)}")
            messages.error(request, 'Invalid candidate selection!')
            return render(request, 'voting/vote.html', {'candidates': candidates})
        
        try:
            candidate = get_object_or_404(Candidate, id=candidate_id, is_active=True)
            
            # Triple-check user hasn't voted (security measure)
            if request.user.has_voted:
                security_logger.warning(f"User {request.user.email} attempted double voting from IP {get_client_ip(request)}")
                messages.error(request, 'You have already voted!')
                return redirect('vote_success')
            
            # Verify user is still verified
            if not request.user.is_verified:
                security_logger.warning(f"Unverified user {request.user.email} attempted to vote from IP {get_client_ip(request)}")
                messages.error(request, 'Your account verification status has changed. Please contact admin.')
                return redirect('home')
            
            # Atomic transaction for vote integrity
            with transaction.atomic():
                # Create vote record
                Vote.objects.create(candidate=candidate)
                
                # Update user voting status
                request.user.has_voted = True
                request.user.save()
                
                # Create success notification
                from .models import Notification
                Notification.objects.create(
                    user=request.user,
                    title="Vote Recorded Successfully! ✓",
                    message=f"Your vote has been securely recorded. Thank you for participating in the election!",
                    notification_type='success',
                    link='/results/live/'
                )
                
                # Log successful vote (without revealing candidate for anonymity)
                security_logger.info(f"User {request.user.email} successfully voted from IP {get_client_ip(request)}")
            
            messages.success(request, f'Your vote for {candidate.name} has been recorded!')
            return redirect('vote_success')
            
        except Exception as e:
            security_logger.error(f"Vote submission error for user {request.user.email} from IP {get_client_ip(request)}: {str(e)}")
            messages.error(request, 'An error occurred while casting your vote. Please try again.')
    
    return render(request, 'voting/vote.html', {'candidates': candidates})


@require_http_methods(["POST"])
@login_required
def cast_vote_ajax(request):
    """AJAX endpoint for casting votes"""
    if request.user.is_admin:
        return JsonResponse({'success': False, 'message': 'Admins cannot vote!'})
    
    if request.user.has_voted:
        return JsonResponse({'success': False, 'message': 'You have already voted!'})
    
    try:
        data = json.loads(request.body)
        candidate_id = data.get('candidate_id')
        
        if not candidate_id:
            return JsonResponse({'success': False, 'message': 'No candidate selected!'})
        
        candidate = get_object_or_404(Candidate, id=candidate_id, is_active=True)
        
        # Create vote and update user atomically
        with transaction.atomic():
            Vote.objects.create(candidate=candidate)
            request.user.has_voted = True
            request.user.save()
        
        return JsonResponse({
            'success': True, 
            'message': f'Your vote for {candidate.name} has been recorded successfully!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred while casting your vote.'})


@login_required
def vote_success_view(request):
    """Vote success page"""
    if not request.user.has_voted:
        return redirect('vote')
    
    return render(request, 'voting/vote_success.html')


def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and user.is_admin


@user_passes_test(is_admin)
def admin_dashboard_view(request):
    """Admin dashboard view"""
    from django.db.models import Count
    
    # Get statistics
    total_users = User.objects.count()
    total_votes = Vote.objects.count()
    total_candidates = Candidate.objects.count()
    
    # Get candidates with vote counts using proper annotation (avoid conflict with property)
    candidates = Candidate.objects.all().annotate(
        total_votes=Count('votes')
    ).order_by('-total_votes', 'name')
    
    # Add vote counts and percentages
    candidates_data = []
    for candidate in candidates:
        vote_count = candidate.total_votes  # Use the annotated field
        vote_percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        candidates_data.append({
            'candidate': candidate,
            'vote_count': vote_count,
            'vote_percentage': vote_percentage
        })
    
    # Already sorted by vote count descending from the query
    
    context = {
        'total_users': total_users,
        'total_votes': total_votes,
        'total_candidates': total_candidates,
        'candidates_data': candidates_data,
    }
    
    return render(request, 'voting/admin_dashboard.html', context)


@user_passes_test(is_admin)
def add_candidate_view(request):
    """Add candidate view"""
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, f'Candidate {candidate.name} added successfully!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CandidateForm()
    
    return render(request, 'voting/add_candidate.html', {'form': form})


@require_http_methods(["POST"])
@user_passes_test(is_admin)
def add_candidate_ajax(request):
    """AJAX endpoint for adding candidates with audit logging"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        
        if not name or not description:
            security_logger.warning(f"Admin {request.user.email} attempted to add candidate with missing data from IP {get_client_ip(request)}")
            return JsonResponse({'success': False, 'message': 'Name and description are required!'})
        
        candidate = Candidate.objects.create(name=name, description=description)
        
        # Log candidate addition
        security_logger.info(f"Admin {request.user.email} added candidate '{candidate.name}' from IP {get_client_ip(request)}")
        
        return JsonResponse({
            'success': True,
            'message': f'Candidate {candidate.name} added successfully!',
            'candidate': {
                'id': candidate.id,
                'name': candidate.name,
                'description': candidate.description,
                'vote_count': 0,
                'vote_percentage': 0
            }
        })
        
    except json.JSONDecodeError:
        security_logger.warning(f"Admin {request.user.email} sent invalid JSON data from IP {get_client_ip(request)}")
        return JsonResponse({'success': False, 'message': 'Invalid request data!'})
    except Exception as e:
        security_logger.error(f"Error adding candidate by admin {request.user.email} from IP {get_client_ip(request)}: {str(e)}")
        return JsonResponse({'success': False, 'message': 'An error occurred while adding the candidate.'})


@require_http_methods(["DELETE"])
@user_passes_test(is_admin)
def delete_candidate_ajax(request, candidate_id):
    """AJAX endpoint for deleting candidates with audit logging"""
    try:
        candidate = get_object_or_404(Candidate, id=candidate_id)
        candidate_name = candidate.name
        vote_count = candidate.votes.count()
        
        # Delete candidate and associated votes
        with transaction.atomic():
            Vote.objects.filter(candidate=candidate).delete()
            candidate.delete()
        
        # Log candidate deletion
        security_logger.warning(f"Admin {request.user.email} deleted candidate '{candidate_name}' with {vote_count} votes from IP {get_client_ip(request)}")
        
        return JsonResponse({
            'success': True,
            'message': f'Candidate {candidate_name} deleted successfully!'
        })
        
    except Exception as e:
        security_logger.error(f"Error deleting candidate by admin {request.user.email} from IP {get_client_ip(request)}: {str(e)}")
        return JsonResponse({'success': False, 'message': 'An error occurred while deleting the candidate.'})


@user_passes_test(is_admin)
def manage_users_view(request):
    """Manage users view"""
    users = User.objects.all().order_by('-date_joined')
    
    # Calculate statistics
    total_users = users.count()
    voted_users_count = users.filter(has_voted=True).count()
    
    # Pagination
    paginator = Paginator(users, 20)  # Show 20 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_users': total_users,
        'voted_users_count': voted_users_count,
    }
    
    return render(request, 'voting/manage_users.html', context)


def results_view(request):
    """Public results view (if enabled)"""
    from django.db.models import Count
    
    # Get candidates with vote counts using proper annotation (avoid conflict with property)
    candidates = Candidate.objects.filter(is_active=True).annotate(
        total_votes=Count('votes')
    ).order_by('-total_votes', 'name')
    
    total_votes = Vote.objects.count()
    
    candidates_data = []
    for candidate in candidates:
        vote_count = candidate.total_votes  # Use the annotated field
        vote_percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        candidates_data.append({
            'candidate': candidate,
            'vote_count': vote_count,
            'vote_percentage': vote_percentage
        })
    
    context = {
        'candidates_data': candidates_data,
        'total_votes': total_votes
    }
    
    return render(request, 'voting/results.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin)
def verify_users_view(request):
    """Admin view to verify user identities"""
    unverified_users = User.objects.filter(is_verified=False, is_admin=False).order_by('-created_at')
    verified_users = User.objects.filter(is_verified=True, is_admin=False).order_by('-verified_at')[:10]
    
    context = {
        'unverified_users': unverified_users,
        'verified_users': verified_users,
        'unverified_count': unverified_users.count(),
    }
    return render(request, 'voting/verify_users.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin)
def verify_user_action(request, user_id):
    """Admin action to verify or reject a user"""
    from .models import Notification
    
    if request.method != 'POST':
        return redirect('verify_users')
    
    user = get_object_or_404(User, id=user_id, is_admin=False)
    action = request.POST.get('action')
    
    if action == 'verify':
        user.is_verified = True
        user.verified_at = timezone.now()
        user.verified_by = request.user
        user.save()
        
        # Create notification for user
        Notification.objects.create(
            user=user,
            title="Account Verified! 🎉",
            message=f"Your account has been verified by {request.user.full_name}. You can now cast your vote!",
            notification_type='success',
            link='/vote/'
        )
        
        security_logger.info(f"Admin {request.user.email} verified user {user.email} from IP {get_client_ip(request)}")
        messages.success(request, f'User {user.full_name} has been verified successfully!')
        
    elif action == 'reject':
        security_logger.info(f"Admin {request.user.email} rejected user {user.email} from IP {get_client_ip(request)}")
        messages.warning(request, f'User {user.full_name} has been rejected and deleted.')
        user.delete()
    
    return redirect('verify_users')


@login_required
@user_passes_test(lambda u: u.is_admin)
def view_id_proof(request, user_id):
    """Admin view to see user's ID proof"""
    user = get_object_or_404(User, id=user_id)
    return render(request, 'voting/view_id_proof.html', {'user_to_verify': user})


@login_required
@user_passes_test(lambda u: u.is_admin)
def edit_candidate_view(request, candidate_id):
    """Admin view to edit a candidate"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            security_logger.info(f"Admin {request.user.email} edited candidate '{candidate.name}' from IP {get_client_ip(request)}")
            messages.success(request, f'Candidate {candidate.name} updated successfully!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CandidateForm(instance=candidate)
    
    return render(request, 'voting/edit_candidate.html', {'form': form, 'candidate': candidate})


@require_http_methods(["POST"])
@login_required
@user_passes_test(lambda u: u.is_admin)
def edit_candidate_ajax(request, candidate_id):
    """AJAX endpoint for editing candidates"""
    try:
        candidate = get_object_or_404(Candidate, id=candidate_id)
        data = json.loads(request.body)
        
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        is_active = data.get('is_active', True)
        
        if not name or not description:
            return JsonResponse({'success': False, 'message': 'Name and description are required!'})
        
        old_name = candidate.name
        candidate.name = name
        candidate.description = description
        candidate.is_active = is_active
        candidate.save()
        
        security_logger.info(f"Admin {request.user.email} edited candidate '{old_name}' to '{name}' from IP {get_client_ip(request)}")
        
        return JsonResponse({
            'success': True,
            'message': f'Candidate updated successfully!',
            'candidate': {
                'id': candidate.id,
                'name': candidate.name,
                'description': candidate.description,
                'is_active': candidate.is_active
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data!'})
    except Exception as e:
        security_logger.error(f"Error editing candidate by admin {request.user.email} from IP {get_client_ip(request)}: {str(e)}")
        return JsonResponse({'success': False, 'message': 'An error occurred while updating the candidate.'})


@require_http_methods(["GET"])
def live_results_api(request):
    """API endpoint for live results data"""
    from django.db.models import Count
    
    candidates = Candidate.objects.filter(is_active=True).annotate(
        vote_count=Count('votes')
    ).order_by('-vote_count')
    
    candidates_data = [{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'votes': c.vote_count
    } for c in candidates]
    
    total_votes = Vote.objects.count()
    total_users = User.objects.filter(is_admin=False).count()
    
    return JsonResponse({
        'candidates': candidates_data,
        'total_votes': total_votes,
        'total_users': total_users,
        'timestamp': timezone.now().isoformat()
    })


def results_charts_view(request):
    """Live results with charts"""
    from django.db.models import Count
    
    candidates = Candidate.objects.filter(is_active=True).annotate(
        vote_count=Count('votes')
    ).order_by('-vote_count')
    
    total_votes = Vote.objects.count()
    total_users = User.objects.filter(is_admin=False).count()
    total_candidates = candidates.count()
    
    leading_candidate = None
    if candidates.exists() and total_votes > 0:
        leading = candidates.first()
        leading_candidate = {
            'name': leading.name,
            'votes': leading.vote_count
        }
    
    context = {
        'total_votes': total_votes,
        'total_users': total_users,
        'total_candidates': total_candidates,
        'leading_candidate': leading_candidate,
    }
    
    return render(request, 'voting/results_charts.html', context)


@login_required
@require_http_methods(["GET"])
def notifications_api(request):
    """API endpoint for user notifications"""
    from .models import Notification
    
    notifications = Notification.objects.filter(user=request.user)[:20]
    unread_count = notifications.filter(is_read=False).count()
    
    notifications_data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'notification_type': n.notification_type,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat(),
        'link': n.link
    } for n in notifications]
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': unread_count
    })


@login_required
@require_http_methods(["POST"])
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    from .models import Notification
    
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)


@login_required
@require_http_methods(["POST"])
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    from .models import Notification
    
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})
