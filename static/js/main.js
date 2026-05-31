// TutorIA – kliensoldali logika

// Ország választáskor megjeleníti / elrejti az autonóm közösség mezőt.
// Csak Spanyolország (ES) esetén látszik a régió választó.
function initCountryRegionToggle() {
    const country = document.getElementById('country');
    const regionField = document.getElementById('region-field');
    const region = document.getElementById('region');
    if (!country || !regionField) return;

    function update() {
        const isSpain = country.value === 'ES';
        regionField.style.display = isSpain ? '' : 'none';
        if (region) {
            region.required = isSpain;
            if (!isSpain) region.value = '';
        }
    }

    country.addEventListener('change', update);
    update();
}

// Flash üzenetek automatikus elhalványítása néhány másodperc után.
document.addEventListener('DOMContentLoaded', function () {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(function (el) {
        setTimeout(function () {
            el.style.transition = 'opacity 0.6s ease';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 600);
        }, 5000);
    });
});
