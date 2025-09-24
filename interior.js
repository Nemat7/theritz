// Filter functionality for interior page
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');

    if (filterButtons.length > 0 && galleryItems.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                
                galleryItems.forEach(item => {
                    if (filter === 'all' || item.classList.contains(filter)) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }

    // Lightbox
    if (typeof lightbox !== 'undefined') {
        lightbox.option({
            'resizeDuration': 200,
            'wrapAround': true,
            'albumLabel': "Изображение %1 из %2"
        });
    }
});


// Yandex Map for interior page
if (typeof ymaps !== 'undefined') {
    ymaps.ready(function() {
        const mapContainer = document.getElementById('map');
        if (mapContainer && !mapContainer._map) { // Проверяем, не инициализирована ли уже карта
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
            mapContainer._map = map; // Помечаем контейнер как инициализированный
        }
    });
}

