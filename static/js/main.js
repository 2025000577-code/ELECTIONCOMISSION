// Main JavaScript file for Online Voting System - Enhanced Mobile Support

// Global variables
let isLoading = false;
let isMobile = window.innerWidth <= 768;
let isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    initializeMobileFeatures();
});

// Handle window resize for responsive behavior
window.addEventListener('resize', debounce(function() {
    isMobile = window.innerWidth <= 768;
    handleResponsiveChanges();
}, 250));

function initializeApp() {
    // Add loading states to forms
    addLoadingStates();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Initialize animations
    initializeAnimations();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
    
    // Initialize mobile-specific features
    if (isMobile || isTouch) {
        initializeMobileFeatures();
    }
}

// Mobile-specific initialization
function initializeMobileFeatures() {
    // Add touch-friendly interactions
    addTouchSupport();
    
    // Optimize forms for mobile
    optimizeFormsForMobile();
    
    // Add mobile navigation enhancements
    enhanceMobileNavigation();
    
    // Add pull-to-refresh (if supported)
    addPullToRefresh();
    
    // Optimize images for mobile
    optimizeImagesForMobile();
    
    // Add mobile-specific event listeners
    addMobileEventListeners();
}

// Add touch support for interactive elements
function addTouchSupport() {
    const touchElements = document.querySelectorAll('.candidate-card, .feature-card, .stat-card, .btn');
    
    touchElements.forEach(element => {
        // Add touch feedback
        element.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        }, { passive: true });
        
        element.addEventListener('touchend', function() {
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        }, { passive: true });
        
        // Prevent double-tap zoom on buttons
        if (element.classList.contains('btn')) {
            element.addEventListener('touchend', function(e) {
                e.preventDefault();
                this.click();
            });
        }
    });
}

// Optimize forms for mobile devices
function optimizeFormsForMobile() {
    const inputs = document.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        // Prevent zoom on iOS when focusing inputs
        if (input.type === 'email' || input.type === 'password' || input.type === 'text') {
            input.style.fontSize = '16px';
        }
        
        // Add mobile-friendly input modes
        if (input.type === 'email') {
            input.setAttribute('inputmode', 'email');
        }
        
        if (input.type === 'tel') {
            input.setAttribute('inputmode', 'tel');
        }
        
        // Add autocomplete attributes
        if (input.name === 'email') {
            input.setAttribute('autocomplete', 'email');
        }
        
        if (input.name === 'password') {
            input.setAttribute('autocomplete', 'current-password');
        }
        
        if (input.name === 'full_name') {
            input.setAttribute('autocomplete', 'name');
        }
    });
}

// Enhance mobile navigation
function enhanceMobileNavigation() {
    const navbar = document.querySelector('.navbar');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (isMobile && navbarCollapse.classList.contains('show')) {
                if (!navbar.contains(e.target)) {
                    navbarToggler.click();
                }
            }
        });
        
        // Close mobile menu when clicking on nav links
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (isMobile && navbarCollapse.classList.contains('show')) {
                    setTimeout(() => {
                        navbarToggler.click();
                    }, 100);
                }
            });
        });
    }
}

// Add pull-to-refresh functionality
function addPullToRefresh() {
    if (!('serviceWorker' in navigator)) return;
    
    let startY = 0;
    let currentY = 0;
    let pullDistance = 0;
    const threshold = 100;
    
    document.addEventListener('touchstart', function(e) {
        startY = e.touches[0].pageY;
    }, { passive: true });
    
    document.addEventListener('touchmove', function(e) {
        currentY = e.touches[0].pageY;
        pullDistance = currentY - startY;
        
        if (pullDistance > 0 && window.scrollY === 0) {
            // Add visual feedback for pull-to-refresh
            document.body.style.transform = `translateY(${Math.min(pullDistance / 3, 50)}px)`;
            document.body.style.opacity = Math.max(0.8, 1 - pullDistance / 300);
        }
    }, { passive: true });
    
    document.addEventListener('touchend', function() {
        if (pullDistance > threshold && window.scrollY === 0) {
            // Trigger refresh
            location.reload();
        }
        
        // Reset visual feedback
        document.body.style.transform = '';
        document.body.style.opacity = '';
        pullDistance = 0;
    }, { passive: true });
}

// Optimize images for mobile
function optimizeImagesForMobile() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        // Add lazy loading
        img.setAttribute('loading', 'lazy');
        
        // Add responsive image attributes
        if (!img.hasAttribute('sizes')) {
            img.setAttribute('sizes', '(max-width: 768px) 100vw, 50vw');
        }
    });
}

// Add mobile-specific event listeners
function addMobileEventListeners() {
    // Handle orientation changes
    window.addEventListener('orientationchange', function() {
        setTimeout(() => {
            handleResponsiveChanges();
            // Fix viewport height on mobile browsers
            document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
        }, 100);
    });
    
    // Handle viewport changes for mobile browsers
    function setViewportHeight() {
        document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
    }
    
    setViewportHeight();
    window.addEventListener('resize', debounce(setViewportHeight, 250));
    
    // Add swipe gestures for cards
    addSwipeGestures();
}

// Add swipe gestures for interactive elements
function addSwipeGestures() {
    const swipeElements = document.querySelectorAll('.candidate-card');
    
    swipeElements.forEach(element => {
        let startX = 0;
        let startY = 0;
        let endX = 0;
        let endY = 0;
        
        element.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }, { passive: true });
        
        element.addEventListener('touchend', function(e) {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            
            // Check if it's a horizontal swipe
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
                if (deltaX > 0) {
                    // Swipe right - could trigger vote action
                    const voteBtn = element.querySelector('.vote-btn');
                    if (voteBtn) {
                        voteBtn.style.background = 'var(--success-gradient)';
                        setTimeout(() => {
                            voteBtn.style.background = '';
                        }, 200);
                    }
                }
            }
        }, { passive: true });
    });
}

// Handle responsive changes
function handleResponsiveChanges() {
    // Update mobile-specific styles
    updateMobileStyles();
    
    // Reinitialize components that need responsive updates
    reinitializeResponsiveComponents();
}

// Update mobile-specific styles
function updateMobileStyles() {
    const body = document.body;
    
    if (isMobile) {
        body.classList.add('mobile-device');
    } else {
        body.classList.remove('mobile-device');
    }
    
    if (isTouch) {
        body.classList.add('touch-device');
    } else {
        body.classList.remove('touch-device');
    }
}

// Reinitialize responsive components
function reinitializeResponsiveComponents() {
    // Reinitialize tooltips for mobile
    if (isMobile) {
        // Disable tooltips on mobile
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => {
            const bsTooltip = bootstrap.Tooltip.getInstance(tooltip);
            if (bsTooltip) {
                bsTooltip.dispose();
            }
        });
    } else {
        // Reinitialize tooltips for desktop
        initializeTooltips();
    }
}

// Add loading states to all forms
function addLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !isLoading) {
                isLoading = true;
                const originalText = submitBtn.innerHTML;
                
                // Mobile-friendly loading text
                const loadingText = isMobile ? 
                    '<i class="fas fa-spinner fa-spin me-1"></i>Loading...' : 
                    '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                
                submitBtn.innerHTML = loadingText;
                submitBtn.disabled = true;
                
                // Add haptic feedback on mobile
                if (isTouch && navigator.vibrate) {
                    navigator.vibrate(50);
                }
                
                // Reset after 5 seconds as fallback
                setTimeout(() => {
                    if (isLoading) {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                        isLoading = false;
                    }
                }, 5000);
            }
        });
    });
}

// Initialize Bootstrap tooltips (desktop only)
function initializeTooltips() {
    if (isMobile) return; // Skip tooltips on mobile
    
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Add smooth scrolling to anchor links
function addSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = isMobile ? 80 : 100; // Account for mobile navbar
                const targetPosition = target.offsetTop - offset;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Initialize scroll animations
function initializeAnimations() {
    // Skip complex animations on mobile for performance
    if (isMobile && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return;
    }
    
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: isMobile ? 0.05 : 0.1,
        rootMargin: isMobile ? '0px 0px -30px 0px' : '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    // Add animation classes to elements
    const animatedElements = document.querySelectorAll('.feature-card, .stat-card, .candidate-card');
    animatedElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(el);
    });
}

// Add keyboard shortcuts (desktop only)
function addKeyboardShortcuts() {
    if (isMobile) return; // Skip keyboard shortcuts on mobile
    
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.activeElement.closest('form');
            if (activeForm) {
                const submitBtn = activeForm.querySelector('button[type="submit"]');
                if (submitBtn && !submitBtn.disabled) {
                    submitBtn.click();
                }
            }
        }
        
        // Escape to close modals/alerts
        if (e.key === 'Escape') {
            // Close any open SweetAlert
            if (Swal.isVisible()) {
                Swal.close();
            }
        }
    });
}

// Enhanced utility functions for mobile

// Show loading spinner with mobile optimization
function showLoading(element, text = 'Loading...') {
    if (element) {
        const loadingText = isMobile ? 
            `<i class="fas fa-spinner fa-spin me-1"></i>${text}` : 
            `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
        
        element.innerHTML = loadingText;
        element.disabled = true;
        
        // Add haptic feedback on mobile
        if (isTouch && navigator.vibrate) {
            navigator.vibrate(50);
        }
    }
}

// Hide loading spinner
function hideLoading(element, originalText) {
    if (element) {
        element.innerHTML = originalText;
        element.disabled = false;
        isLoading = false;
    }
}

// Format numbers with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Validate email format
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validate password strength
function validatePassword(password) {
    const minLength = 6;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    
    return {
        isValid: password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers,
        length: password.length >= minLength,
        upperCase: hasUpperCase,
        lowerCase: hasLowerCase,
        numbers: hasNumbers
    };
}

// Show success message with mobile optimization
function showSuccess(title, message, callback = null) {
    const config = {
        icon: 'success',
        title: title,
        text: message,
        confirmButtonColor: '#198754',
        confirmButtonText: 'OK'
    };
    
    // Mobile-specific optimizations
    if (isMobile) {
        config.width = '90%';
        config.padding = '1rem';
        config.fontSize = '0.9rem';
    }
    
    Swal.fire(config).then((result) => {
        if (callback && result.isConfirmed) {
            callback();
        }
    });
}

// Show error message with mobile optimization
function showError(title, message) {
    const config = {
        icon: 'error',
        title: title,
        text: message,
        confirmButtonColor: '#dc3545',
        confirmButtonText: 'OK'
    };
    
    // Mobile-specific optimizations
    if (isMobile) {
        config.width = '90%';
        config.padding = '1rem';
        config.fontSize = '0.9rem';
    }
    
    Swal.fire(config);
}

// Show confirmation dialog with mobile optimization
function showConfirmation(title, message, confirmText = 'Yes', cancelText = 'No') {
    const config = {
        title: title,
        text: message,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#198754',
        cancelButtonColor: '#6c757d',
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
        reverseButtons: true
    };
    
    // Mobile-specific optimizations
    if (isMobile) {
        config.width = '90%';
        config.padding = '1rem';
        config.fontSize = '0.9rem';
        config.buttonsStyling = true;
    }
    
    return Swal.fire(config);
}

// Copy text to clipboard with mobile support
function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

// Fallback copy method for older browsers
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showToast('Copied to clipboard!', 'success');
    } catch (err) {
        showError('Error', 'Failed to copy to clipboard');
    }
    
    document.body.removeChild(textArea);
}

// Show toast notification
function showToast(message, type = 'info') {
    const config = {
        toast: true,
        position: isMobile ? 'top' : 'top-end',
        icon: type,
        title: message,
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true
    };
    
    if (isMobile) {
        config.width = '90%';
    }
    
    Swal.fire(config);
}

// Generate random ID
function generateId(length = 8) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Enhanced Local Storage helpers with error handling
const Storage = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Error saving to localStorage:', e);
            if (isMobile) {
                showToast('Storage limit reached', 'warning');
            }
            return false;
        }
    },
    
    get: function(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('Error reading from localStorage:', e);
            return defaultValue;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.error('Error removing from localStorage:', e);
            return false;
        }
    },
    
    clear: function() {
        try {
            localStorage.clear();
            return true;
        } catch (e) {
            console.error('Error clearing localStorage:', e);
            return false;
        }
    }
};

// Enhanced API helper functions with mobile optimizations
const API = {
    request: async function(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: isMobile ? 10000 : 5000 // Longer timeout for mobile
        };
        
        const config = { ...defaultOptions, ...options };
        
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), config.timeout);
            
            const response = await fetch(url, {
                ...config,
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            const data = await response.json();
            return { success: response.ok, data, status: response.status };
        } catch (error) {
            console.error('API request failed:', error);
            
            if (error.name === 'AbortError') {
                return { success: false, error: 'Request timeout' };
            }
            
            return { success: false, error: error.message };
        }
    },
    
    get: function(url) {
        return this.request(url, { method: 'GET' });
    },
    
    post: function(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    put: function(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    delete: function(url) {
        return this.request(url, { method: 'DELETE' });
    }
};

// Form validation helpers
const Validator = {
    required: function(value) {
        return value !== null && value !== undefined && value.toString().trim() !== '';
    },
    
    email: function(value) {
        return isValidEmail(value);
    },
    
    minLength: function(value, min) {
        return value && value.length >= min;
    },
    
    maxLength: function(value, max) {
        return value && value.length <= max;
    },
    
    pattern: function(value, pattern) {
        return new RegExp(pattern).test(value);
    }
};

// Device detection utilities
const Device = {
    isMobile: () => isMobile,
    isTouch: () => isTouch,
    isIOS: () => /iPad|iPhone|iPod/.test(navigator.userAgent),
    isAndroid: () => /Android/.test(navigator.userAgent),
    isTablet: () => window.innerWidth >= 768 && window.innerWidth <= 1024,
    getOrientation: () => window.innerHeight > window.innerWidth ? 'portrait' : 'landscape',
    getViewportSize: () => ({
        width: window.innerWidth,
        height: window.innerHeight
    })
};

// Export functions for use in other scripts
window.VotingSystem = {
    showLoading,
    hideLoading,
    showSuccess,
    showError,
    showConfirmation,
    showToast,
    copyToClipboard,
    formatNumber,
    isValidEmail,
    validatePassword,
    Storage,
    API,
    Validator,
    Device,
    debounce,
    throttle,
    generateId,
    isMobile: () => isMobile,
    isTouch: () => isTouch
};