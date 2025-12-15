import axios from 'axios';

// API configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initializeMobileMenu();
  initializeSignupForm();
  initializeSmoothScroll();
});

// Mobile menu toggle
function initializeMobileMenu() {
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  
  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
      // TODO: Implement mobile menu toggle
      console.log('Mobile menu clicked');
    });
  }
}

// Smooth scroll for anchor links
function initializeSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

// Signup form handling
function initializeSignupForm() {
  const form = document.getElementById('signup-form');
  const submitBtn = document.getElementById('submit-btn');
  const submitText = document.getElementById('submit-text');
  const formMessage = document.getElementById('form-message');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Disable submit button
    submitBtn.disabled = true;
    submitText.innerHTML = '<span class="spinner inline-block"></span>';

    // Get form data
    const formData = {
      name: document.getElementById('name').value.trim(),
      email: document.getElementById('email').value.trim(),
      phone: document.getElementById('phone').value.trim() || null,
      business_type: document.getElementById('business_type').value,
      message: document.getElementById('message').value.trim() || null,
      source: 'landing_page',
      created_at: new Date().toISOString()
    };

    try {
      // Send data to backend API
      const response = await axios.post(`${API_BASE_URL}/leads`, formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.status === 201 || response.status === 200) {
        // Success
        showMessage('success', 'Thank you! We\'ll be in touch soon.');
        form.reset();
        
        // Track conversion (optional - for analytics)
        if (window.gtag) {
          window.gtag('event', 'conversion', {
            'event_category': 'signup',
            'event_label': 'landing_page_signup'
          });
        }
      }
    } catch (error) {
      console.error('Signup error:', error);
      
      let errorMessage = 'Something went wrong. Please try again.';
      
      if (error.response) {
        // Server responded with error
        if (error.response.status === 409) {
          errorMessage = 'This email is already registered.';
        } else if (error.response.data && error.response.data.message) {
          errorMessage = error.response.data.message;
        }
      } else if (error.request) {
        // No response from server
        errorMessage = 'Unable to connect to server. Please check your connection.';
      }
      
      showMessage('error', errorMessage);
    } finally {
      // Re-enable submit button
      submitBtn.disabled = false;
      submitText.textContent = 'Get Started Free';
    }
  });

  // Show message helper
  function showMessage(type, message) {
    formMessage.className = `p-4 rounded-xl text-sm ${
      type === 'success' 
        ? 'bg-green-500/10 border border-green-500/20 text-green-400' 
        : 'bg-red-500/10 border border-red-500/20 text-red-400'
    }`;
    formMessage.textContent = message;
    formMessage.classList.remove('hidden');

    // Hide message after 5 seconds
    setTimeout(() => {
      formMessage.classList.add('hidden');
    }, 5000);
  }
}

// Form validation helpers
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function validatePhone(phone) {
  if (!phone) return true; // Phone is optional
  const re = /^[\d\s\-\+\(\)]+$/;
  return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}
