/**
 * Dental Clinic - Frontend JavaScript
 *
 * Handles all client-side interactions:
 * - Loading screen animation
 * - Navbar scroll behavior
 * - Mobile menu toggle
 * - Scroll reveal animations
 * - Counter animations
 * - Booking modal with form validation
 * - Appointment submission via API (fetch to /api/appointment/)
 * - Back-to-top button
 * - Confetti celebration
 * - Button ripple effects
 */


// ─────────────────────────────────────────────
// LOADER
// ─────────────────────────────────────────────
// Hides the loading spinner after the page finishes loading.
window.addEventListener('load', () => {
    const loader = document.getElementById('loader');
    // Fade out after a brief delay, then remove from DOM
    setTimeout(() => {
        loader.style.opacity = '0';
        setTimeout(() => loader.style.display = 'none', 800);
    }, 500);
});


// ─────────────────────────────────────────────
// NAVBAR SCROLL
// ─────────────────────────────────────────────
// Adds/removes 'scrolled' class on navbar based on scroll position.
// Also controls visibility of the back-to-top button.
function updateNavbarState() {
    const nav = document.getElementById('navbar');
    if (window.scrollY > 100) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }

    // Show/hide back-to-top button based on scroll depth
    const btt = document.getElementById('backToTop');
    if (window.scrollY > 500) {
        btt.classList.add('visible');
    } else {
        btt.classList.remove('visible');
    }
}

window.addEventListener('scroll', updateNavbarState);
window.addEventListener('DOMContentLoaded', updateNavbarState);


// ─────────────────────────────────────────────
// MOBILE MENU
// ─────────────────────────────────────────────
// Toggles the mobile navigation menu and animates the hamburger icon.
const mobileToggle = document.getElementById('mobile-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const mobileLinks = document.querySelectorAll('.mobile-link');

mobileToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
    // Animate hamburger into X when menu is open
    const divs = mobileToggle.querySelectorAll('div');
    divs[0].style.transform = mobileMenu.classList.contains('active') ? 'rotate(45deg) translate(5px, 6px)' : 'none';
    divs[1].style.opacity = mobileMenu.classList.contains('active') ? '0' : '1';
    divs[2].style.transform = mobileMenu.classList.contains('active') ? 'rotate(-45deg) translate(5px, -6px)' : 'none';
});

// Close mobile menu when a link is clicked
mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        const divs = mobileToggle.querySelectorAll('div');
        divs.forEach(d => { d.style.transform = 'none'; d.style.opacity = '1'; });
    });
});


// ─────────────────────────────────────────────
// REVEAL ON SCROLL
// ─────────────────────────────────────────────
// Uses IntersectionObserver to add 'visible' class to elements
// when they enter the viewport, triggering CSS animations.
const observerOptions = { threshold: 0.15 };
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            // If the element contains a counter, start counting animation
            if (entry.target.querySelector('.counter')) {
                startCounters(entry.target);
            }
        }
    });
}, observerOptions);

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
document.querySelectorAll('.stat-item').forEach(el => observer.observe(el));


// ─────────────────────────────────────────────
// COUNTER LOGIC
// ─────────────────────────────────────────────
// Animates number counting from 0 to the target value for stat items.
function startCounters(container) {
    const counters = container.querySelectorAll('.counter');
    counters.forEach(counter => {
        if (counter.classList.contains('counted')) return;
        counter.classList.add('counted');
        const target = +counter.getAttribute('data-target');
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const updateCount = () => {
            current += increment;
            if (current < target) {
                counter.innerText = Math.ceil(current).toLocaleString() + (target > 1000 ? '+' : '+');
                requestAnimationFrame(updateCount);
            } else {
                counter.innerText = target.toLocaleString() + '+';
            }
        };
        updateCount();
    });
}


// ─────────────────────────────────────────────
// BACK TO TOP
// ─────────────────────────────────────────────
// Scrolls the page back to the top when the button is clicked.
document.getElementById('backToTop').addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});


// ─────────────────────────────────────────────
// DATE INPUT RESTRICTION
// ─────────────────────────────────────────────
// Set the minimum date on the appointment date picker to today.
// This prevents users from selecting past dates.
document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('book-date');
    if (dateInput) {
        // Get today's date formatted as YYYY-MM-DD for the input's min attribute
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        dateInput.setAttribute('min', `${year}-${month}-${day}`);
    }
});


// ─────────────────────────────────────────────
// MODAL LOGIC
// ─────────────────────────────────────────────
// Controls the booking modal: open, close, and reset behavior.
const modal = document.getElementById('booking-modal');
const openModalBtns = document.querySelectorAll('.open-modal');
const closeModalBtn = document.querySelector('.close-modal');
const formContent = document.getElementById('modal-form-content');
const successContent = document.getElementById('modal-success-content');
const appForm = document.getElementById('appointmentForm');

// Open modal when any "book" button is clicked
openModalBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
});

// Close modal function: hides modal, resets form, removes validation states
const closeFunc = () => {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
    // Reset modal after close transition completes
    setTimeout(() => {
        formContent.style.display = 'block';
        successContent.style.display = 'none';
        appForm.reset();
        document.querySelectorAll('.error-msg').forEach(e => e.style.display = 'none');
        document.querySelectorAll('.form-control').forEach(i => i.classList.remove('invalid'));
    }, 400);
};

closeModalBtn.addEventListener('click', closeFunc);

// Close modal when clicking outside the modal box
modal.addEventListener('click', (e) => {
    if (e.target === modal) closeFunc();
});


// ─────────────────────────────────────────────
// FORM VALIDATION & API SUBMISSION
// ─────────────────────────────────────────────
// Intercepts the appointment form submission, validates all fields,
// sends data to the Django API endpoint, and handles the response.
appForm.addEventListener('submit', async (e) => {
    // Prevent the default HTML form submission (we handle it via fetch)
    e.preventDefault();
    let isValid = true;

// Define all required form fields with their element IDs and error message IDs
     // Time, date, service and email fields are optional — not included here
     const fields = [
         { id: 'book-name', err: 'err-name' },
         { id: 'book-phone', err: 'err-phone' }
     ];

    const formData = {};

    // Validate each required field: check if empty, show/hide error messages
    fields.forEach(field => {
        const el = document.getElementById(field.id);
        const err = document.getElementById(field.err);
        if (!el.value || el.value.trim() === "") {
            el.classList.add('invalid');
            err.style.display = 'block';
            isValid = false;
        } else {
            el.classList.remove('invalid');
            err.style.display = 'none';
            // Map form field IDs to the API field names expected by Django
            const apiFieldMap = {
                'book-name': 'full_name',
                'book-phone': 'phone',
                'book-date': 'preferred_date',
                'book-service': 'service'
            };
            formData[apiFieldMap[field.id]] = el.value;
        }
    });

    // Only proceed with submission if all validations pass
    if (isValid) {
        // Collect optional fields: time and comment are not required
        formData.preferred_time = document.getElementById('book-time')?.value?.trim() || '';
        formData.message = document.getElementById('book-comment')?.value?.trim() || '';

        // Disable the submit button to prevent duplicate submissions
        const submitBtn = appForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = "Yuborilmoqda...";

        try {
            // Send the form data to the Django API endpoint as JSON
            const response = await fetch('/api/appointment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            // Parse the JSON response from the server
            const result = await response.json();

            if (result.success) {
                // On success: hide form, show success message, trigger confetti
                formContent.style.opacity = '0';
                setTimeout(() => {
                    formContent.style.display = 'none';
                    successContent.style.display = 'block';
                    successContent.style.opacity = '0';
                    setTimeout(() => {
                        successContent.style.opacity = '1';
                        createConfetti();
                    }, 50);
                }, 300);

                // Auto-close the modal after 4 seconds
                setTimeout(closeFunc, 4000);
            } else {
                // On server error: show error message to the user
alert("Xatolik: " + (result.error || "Ariza yuborilmadi. Qaytadan urinib ko'ring."));
                 submitBtn.disabled = false;
                 submitBtn.textContent = "Yuborish ✨";
            }
        } catch (error) {
            // On network error: show error message to the user
            console.error("Error submitting form:", error);
alert("Tarmoq xatoligi. Ulanishni tekshiring va qaytadan urinib ko'ring.");
             submitBtn.disabled = false;
             submitBtn.textContent = "Yuborish ✨";
        }
    }
});


// ─────────────────────────────────────────────
// PARTNERS ANIMATION DURATION
// ─────────────────────────────────────────────
// Calculates and sets the animation duration for the partner logo marquee
// based on the width of the scrollable content.
function setPartnersAnimationDuration() {
    const track = document.querySelector('.partners-scroll');
    if (!track) return;
    const oneLoopWidth = track.scrollWidth / 2;
    if (!oneLoopWidth || !Number.isFinite(oneLoopWidth)) return;
    const pxPerSecond = 80;
    const duration = Math.max(12, oneLoopWidth / pxPerSecond);
    track.style.setProperty('--partners-duration', `${duration}s`);
}


// ─────────────────────────────────────────────
// CONFETTI CELEBRATION
// ─────────────────────────────────────────────
// Creates a burst of colorful confetti particles for the success animation.
function createConfetti() {
    const colors = ['#4A90D9', '#43C6AC', '#F5A623', '#FF6B6B', '#FFFFFF'];
    for (let i = 0; i < 100; i++) {
        const conf = document.createElement('div');
        conf.className = 'confetti';
        conf.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        conf.style.left = '50%';
        conf.style.top = '50%';

        // Random angle and velocity for each confetti particle
        const angle = Math.random() * Math.PI * 2;
        const velocity = 5 + Math.random() * 15;
        const distance = 100 + Math.random() * 300;

        document.body.appendChild(conf);

        const startTime = Date.now();
        const duration = 1500 + Math.random() * 1000;

        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = elapsed / duration;

            if (progress < 1) {
                // Calculate position with easing and gravity effect
                const currentDist = distance * (1 - Math.pow(1 - progress, 2));
                const x = Math.cos(angle) * currentDist;
                const y = Math.sin(angle) * currentDist + (progress * progress * 500);

                conf.style.transform = `translate(${x}px, ${y}px) rotate(${progress * 1000}deg)`;
                conf.style.opacity = 1 - progress;
                requestAnimationFrame(animate);
            } else {
                conf.remove();
            }
        };
        requestAnimationFrame(animate);
    }
}


// ─────────────────────────────────────────────
// RIPPLE EFFECT
// ─────────────────────────────────────────────
// Adds a material-design-like ripple effect to all buttons on click.
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('mousedown', function (e) {
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        this.appendChild(ripple);

        // Position the ripple at the click coordinates
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;

        setTimeout(() => ripple.remove(), 600);
    });
});
