document.addEventListener('DOMContentLoaded', () => {
  // Mobile Menu Toggle
  const menuToggle = document.getElementById('menu-toggle');
  const mainNav = document.getElementById('main-nav');
  
  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', () => {
      menuToggle.classList.toggle('active');
      mainNav.classList.toggle('active');
    });
  }

  // Intersection Observer for Scroll Animations
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.15
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target); // Reveal only once
      }
    });
  }, observerOptions);

  const revealElements = document.querySelectorAll('.reveal');
  revealElements.forEach(el => observer.observe(el));

  // Mouse Effects
  document.addEventListener('mousemove', (e) => {
    // Spotlight effect globally via CSS vars
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    document.body.style.setProperty('--mouse-x', x);
    document.body.style.setProperty('--mouse-y', y);
    
    // Blob parallax
    const blob1 = document.querySelector('.blob-1');
    const blob2 = document.querySelector('.blob-2');
    if(blob1) blob1.style.transform = `translate(${(x - 0.5) * 100}px, ${(y - 0.5) * 100}px)`;
    if(blob2) blob2.style.transform = `translate(${(x - 0.5) * -80}px, ${(y - 0.5) * -80}px)`;
  });
});
