from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div
from crispy_forms.bootstrap import Field
from .models import User, Candidate


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )
    id_card_number = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your National ID or Voter ID number'
        }),
        help_text='Enter your government-issued ID number'
    )
    id_card_proof = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*,.pdf'
        }),
        help_text='Upload a clear photo of your ID card (front side) or PDF'
    )
    
    class Meta:
        model = User
        fields = ('email', 'full_name', 'username', 'id_card_number', 'id_card_proof', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': '', 'enctype': 'multipart/form-data'}
        
        # Customize field widgets
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
        
        self.helper.layout = Layout(
            HTML('<div class="mb-3">'),
            Field('full_name', css_class='form-control-lg'),
            HTML('</div>'),
            HTML('<div class="mb-3">'),
            Field('email', css_class='form-control-lg'),
            HTML('</div>'),
            HTML('<div class="mb-3">'),
            Field('username', css_class='form-control-lg'),
            HTML('</div>'),
            HTML('<div class="mb-3">'),
            Field('id_card_number', css_class='form-control-lg'),
            HTML('</div>'),
            HTML('<div class="mb-3">'),
            HTML('<label class="form-label">ID Card Proof</label>'),
            Field('id_card_proof', css_class='form-control'),
            HTML('<small class="text-muted">Upload a clear photo of your government-issued ID card</small>'),
            HTML('</div>'),
            HTML('<div class="mb-3">'),
            Field('password1', css_class='form-control-lg'),
            HTML('</div>'),
            HTML('<div class="mb-4">'),
            Field('password2', css_class='form-control-lg'),
            HTML('</div>'),
            HTML('<div class="alert alert-info">'),
            HTML('<i class="fas fa-info-circle"></i> Your account will be verified by admin before you can vote.'),
            HTML('</div>'),
            Submit('submit', 'Register', css_class='btn btn-primary btn-lg w-100')
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.id_card_number = self.cleaned_data['id_card_number']
        user.id_card_proof = self.cleaned_data['id_card_proof']
        user.is_verified = False  # Requires admin verification
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form"""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your password'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        
        self.helper.layout = Layout(
            HTML('<div class="mb-3">'),
            Field('username', css_class='form-control-lg'),
            HTML('</div>'),
            HTML('<div class="mb-4">'),
            Field('password', css_class='form-control-lg'),
            HTML('</div>'),
            Submit('submit', 'Login', css_class='btn btn-primary btn-lg w-100')
        )


class AdminLoginForm(AuthenticationForm):
    """Admin login form - same as user login but for admins"""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter admin email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter admin password'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        
        self.helper.layout = Layout(
            HTML('<div class="mb-3">'),
            Field('username', css_class='form-control-lg'),
            HTML('</div>'),
            HTML('<div class="mb-4">'),
            Field('password', css_class='form-control-lg'),
            HTML('</div>'),
            Submit('submit', 'Admin Login', css_class='btn btn-warning btn-lg w-100')
        )
    
    def confirm_login_allowed(self, user):
        """Only allow admin users to login through this form"""
        super().confirm_login_allowed(user)
        if not user.is_admin:
            raise forms.ValidationError('Only admin users can login here.')


class CandidateForm(forms.ModelForm):
    """Form for adding/editing candidates"""
    class Meta:
        model = Candidate
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter candidate name'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter party or description'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('description', css_class='col-md-6'),
            ),
            Row(
                Column(
                    Div(
                        HTML('<div class="form-check">'),
                        Field('is_active'),
                        HTML('<label class="form-check-label" for="id_is_active">Active Candidate</label>'),
                        HTML('</div>'),
                        css_class='mt-4'
                    ),
                    css_class='col-md-6'
                ),
            ),
            Submit('submit', 'Save Candidate', css_class='btn btn-success mt-3')
        )


class VoteForm(forms.Form):
    """Form for casting votes"""
    candidate = forms.ModelChoiceField(
        queryset=Candidate.objects.filter(is_active=True),
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        empty_label=None
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'vote-form'
        
        # Customize the candidate field to show as cards
        self.fields['candidate'].widget = forms.HiddenInput()
        
        self.helper.layout = Layout(
            Field('candidate'),
            HTML('<div id="candidate-cards" class="row g-3 g-md-4"></div>'),
            HTML('<div class="text-center mt-4">'),
            Submit('submit', 'Cast Vote', css_class='btn btn-success btn-lg', css_id='vote-submit-btn', style='display: none;'),
            HTML('</div>')
        )