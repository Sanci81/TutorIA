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

// Jelszó megjelenítés / elrejtés (szem ikon).
function initPasswordToggles() {
    document.querySelectorAll('[data-password-toggle]').forEach(function (btn) {
        const inputId = btn.dataset.passwordToggle;
        const input = document.getElementById(inputId);
        if (!input) return;

        const labelShow = btn.getAttribute('aria-label');
        const labelHide = btn.dataset.labelHide;

        btn.addEventListener('click', function () {
            const visible = input.type === 'text';
            input.type = visible ? 'password' : 'text';
            btn.classList.toggle('visible', !visible);
            btn.setAttribute('aria-label', visible ? labelShow : labelHide);
        });
    });
}

// Flash üzenetek automatikus elhalványítása néhány másodperc után.
document.addEventListener('DOMContentLoaded', function () {
    initPasswordToggles();
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(function (el) {
        setTimeout(function () {
            el.style.transition = 'opacity 0.6s ease';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 600);
        }, 5000);
    });
});
