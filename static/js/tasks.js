// Feladatkártyák – tipp és válasz fokozatos felfedése
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-task-card]').forEach(function (card) {
        var hintBtn = card.querySelector('[data-show-hint]');
        var answerBtn = card.querySelector('[data-show-answer]');
        var hintBox = card.querySelector('.task-hint');
        var answerBox = card.querySelector('.task-answer');

        if (!hintBtn || !answerBtn || !hintBox || !answerBox) return;

        hintBtn.addEventListener('click', function () {
            hintBox.hidden = false;
            hintBtn.hidden = true;
            answerBtn.disabled = false;
            answerBtn.classList.remove('is-disabled');
            hintBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });

        answerBtn.addEventListener('click', function () {
            answerBox.hidden = false;
            answerBtn.hidden = true;
            answerBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });
    });
});
