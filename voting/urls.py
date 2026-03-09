from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('results/', views.results_view, name='results'),
    path('results/live/', views.results_charts_view, name='results_charts'),
    
    # API endpoints
    path('api/live-results/', views.live_results_api, name='live_results_api'),
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # User voting
    path('vote/', views.vote_view, name='vote'),
    path('vote/cast/', views.cast_vote_ajax, name='cast_vote_ajax'),
    path('vote/success/', views.vote_success_view, name='vote_success'),
    
    # Admin authentication (changed from admin/ to voting-admin/)
    path('voting-admin/login/', views.admin_login_view, name='admin_login'),
    
    # Admin dashboard (changed from admin/ to voting-admin/)
    path('voting-admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('voting-admin/users/', views.manage_users_view, name='manage_users'),
    path('voting-admin/verify-users/', views.verify_users_view, name='verify_users'),
    path('voting-admin/verify-user/<int:user_id>/', views.verify_user_action, name='verify_user_action'),
    path('voting-admin/view-id-proof/<int:user_id>/', views.view_id_proof, name='view_id_proof'),
    
    # Candidate management (changed from admin/ to voting-admin/)
    path('voting-admin/candidates/add/', views.add_candidate_view, name='add_candidate'),
    path('voting-admin/candidates/add-ajax/', views.add_candidate_ajax, name='add_candidate_ajax'),
    path('voting-admin/candidates/edit/<int:candidate_id>/', views.edit_candidate_view, name='edit_candidate'),
    path('voting-admin/candidates/edit-ajax/<int:candidate_id>/', views.edit_candidate_ajax, name='edit_candidate_ajax'),
    path('voting-admin/candidates/delete/<int:candidate_id>/', views.delete_candidate_ajax, name='delete_candidate_ajax'),
]