// Modern Header JavaScript
document.addEventListener('DOMContentLoaded', function() {
  const navbar = document.getElementById('mainNav');
  const mobileMenuToggle = document.getElementById('mobileMenuToggle');
  const navbarNav = document.getElementById('navbarNav');
  const scrollProgress = document.getElementById('scrollProgress');
  
  // Scroll effect for navbar
  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    // Add scrolled class
    if (currentScroll > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    
    // Update scroll progress
    const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (currentScroll / windowHeight) * 100;
    scrollProgress.style.width = scrolled + '%';
    
    lastScroll = currentScroll;
  });
  
  // Mobile menu toggle
  if (mobileMenuToggle && navbarNav) {
    mobileMenuToggle.addEventListener('click', () => {
      navbarNav.classList.toggle('active');
      mobileMenuToggle.classList.toggle('active');
      
      // Animate bars
      const bars = mobileMenuToggle.querySelectorAll('.menu-bar');
      if (navbarNav.classList.contains('active')) {
        bars[0].style.transform = 'rotate(45deg) translateY(8px)';
        bars[1].style.opacity = '0';
        bars[2].style.transform = 'rotate(-45deg) translateY(-8px)';
      } else {
        bars[0].style.transform = 'none';
        bars[1].style.opacity = '1';
        bars[2].style.transform = 'none';
      }
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!navbar.contains(e.target) && navbarNav.classList.contains('active')) {
        navbarNav.classList.remove('active');
        mobileMenuToggle.classList.remove('active');
        
        const bars = mobileMenuToggle.querySelectorAll('.menu-bar');
        bars[0].style.transform = 'none';
        bars[1].style.opacity = '1';
        bars[2].style.transform = 'none';
      }
    });
  }
  
  // Active link highlighting
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
  
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && href.length > 1) {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          const headerOffset = 72;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
          
          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
          
          // Close mobile menu if open
          if (navbarNav.classList.contains('active')) {
            navbarNav.classList.remove('active');
            mobileMenuToggle.classList.remove('active');
          }
        }
      }
    });
  });
});
