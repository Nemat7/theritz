// Correct Swiper initialization with scroll prevention
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Swiper with proper settings
    const heroSwiper = new Swiper('.hero-swiper', {
        direction: 'horizontal',
        loop: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        // Enable smooth sliding
        speed: 600,
        effect: 'fade',
        fadeEffect: {
            crossFade: true
        },
        // Proper touch settings
        touchRatio: 1,
        touchAngle: 45,
        simulateTouch: true,
        shortSwipes: true,
        longSwipes: true,
        followFinger: true,
        // Prevent scroll issues but keep functionality
        resistance: true,
        resistanceRatio: 0.5,
        // Autoplay if needed
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
    });

    // Only prevent horizontal scroll on body, don't break swiper
    document.body.style.overflowX = 'hidden';

    // Ensure swiper elements can still function
    const swiperElements = document.querySelectorAll('.hero-swiper, .swiper-wrapper');
    swiperElements.forEach(el => {
        el.style.overflow = 'visible';
    });
});


// Mobile Menu
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenuClose = document.getElementById('mobile-menu-close');
const mobileMenu = document.getElementById('mobile-menu');

function openMobileMenu() {
    mobileMenu.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeMobileMenu() {
    mobileMenu.classList.remove('active');
    document.body.style.overflow = 'auto';
}

if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', openMobileMenu);
}

if (mobileMenuClose) {
    mobileMenuClose.addEventListener('click', closeMobileMenu);
}

// Close mobile menu when clicking on links
const mobileNavLinks = document.querySelectorAll('.mobile-nav__link');
mobileNavLinks.forEach(link => {
    link.addEventListener('click', closeMobileMenu);
});

// Modal functionality
const modal = document.getElementById('booking-modal');
const closeBtn = document.querySelector('.modal__close');
const form = document.getElementById('booking-form');

function openModal() {
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal() {
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Добавляем обработчики для всех кнопок бронирования
const bookingButtons = [
    'booking-btn',
    'hero-booking-btn',
    'hero-booking-btn2',
    'left-booking-btn',
    'content-booking-btn',
    'floating-booking-btn',
    'interior-booking-btn'
];

bookingButtons.forEach(btnId => {
    const button = document.getElementById(btnId);
    if (button) {
        button.addEventListener('click', openModal);
    }
});

if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
}

if (modal) {
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
}

// Form submission
async function submitBookingForm(formData) {
    try {
        const response = await fetch('http://localhost:8000/api/booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.success) {
            alert('Спасибо за бронирование! Мы свяжемся с вами в ближайшее время.');
            return true;
        } else {
            alert('Ошибка при бронировании. Попробуйте еще раз.');
            return false;
        }
    } catch (error) {
        console.error('Booking error:', error);
        alert('Ошибка соединения. Попробуйте еще раз.');
        return false;
    }
}

if (form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Собираем данные из формы
        const formData = {
            name: document.querySelector('#booking-form input[type="text"]').value,
            phone: document.querySelector('#booking-form input[type="tel"]').value,
            date: document.querySelector('#booking-form input[type="date"]').value,
            time: document.querySelector('#booking-form input[type="time"]').value,
            guests: document.querySelector('#booking-form select').value,
            comments: document.querySelector('#booking-form textarea').value
        };

        // Проверяем обязательные поля
        if (!formData.name || !formData.phone || !formData.date || !formData.time || !formData.guests) {
            alert('Пожалуйста, заполните все обязательные поля');
            return;
        }

        const success = await submitBookingForm(formData);
        if (success) {
            form.reset();
            closeModal();
        }
    });
}

// Yandex Map
if (typeof ymaps !== 'undefined') {
    ymaps.ready(function() {
        const mapContainer = document.getElementById('map');
        if (mapContainer) {
            const map = new ymaps.Map('map', {
                center: [38.571123, 68.792527],
                zoom: 16,
                controls: ['zoomControl']
            });

            const placemark = new ymaps.Placemark([38.571123, 68.792527], {
                hintContent: 'THE RITZ Гастробар',
                balloonContent: 'Душанбе, Таджикистан'
            }, {
                iconLayout: 'default#image',
                iconImageHref: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
                iconImageSize: [40, 40],
                iconImageOffset: [-20, -40]
            });

            map.geoObjects.add(placemark);
            map.behaviors.disable('scrollZoom');
        }
    });
}

// Floating button functionality
const floatingBtn = document.getElementById('floating-booking-btn');
if (floatingBtn) {
    floatingBtn.addEventListener('click', openModal);
}