// Gyakorló feladatok – válasz beküldés, hang (<=7), tipp, fokozatos válaszfelfedés
document.addEventListener('DOMContentLoaded', function () {
    var cfg = window.TASKS_PAGE || {};
    var checkUrl = cfg.checkUrl;
    var speakUrl = cfg.speakUrl;
    var transcribeUrl = cfg.transcribeUrl;
    var voiceYoung = !!cfg.voiceYoung;
    var encouragement = document.getElementById('tasks-encouragement');
    var anyAttempt = false;

    var voiceSupported =
        typeof navigator !== 'undefined' &&
        !!navigator.mediaDevices &&
        typeof MediaRecorder !== 'undefined';

    var currentAudio = null;
    var globalVoiceBusy = false;

    function showEncouragement() {
        if (anyAttempt || !encouragement) return;
        anyAttempt = true;
        encouragement.hidden = false;
    }

    function setGlobalVoiceBusy(on) {
        globalVoiceBusy = on;
        document.querySelectorAll('[data-read-aloud], [data-speak-answer], [data-speak-answer-optional]').forEach(function (btn) {
            btn.disabled = on;
        });
    }

    function speakText(text, done) {
        if (!text || !speakUrl) {
            if (done) done();
            return;
        }
        setGlobalVoiceBusy(true);
        fetch(speakUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        })
            .then(function (r) {
                if (!r.ok) throw new Error('tts');
                return r.blob();
            })
            .then(function (blob) {
                if (currentAudio) {
                    currentAudio.pause();
                    if (currentAudio.src) URL.revokeObjectURL(currentAudio.src);
                }
                var url = URL.createObjectURL(blob);
                currentAudio = new Audio(url);
                currentAudio.onended = function () {
                    URL.revokeObjectURL(url);
                    currentAudio = null;
                    setGlobalVoiceBusy(false);
                    if (done) done();
                };
                currentAudio.onerror = function () {
                    setGlobalVoiceBusy(false);
                    if (done) done();
                };
                return currentAudio.play();
            })
            .catch(function () {
                setGlobalVoiceBusy(false);
                if (done) done();
            });
    }

    function getCardText(card, attr) {
        return (card.getAttribute(attr) || '').trim();
    }

    function bindHoldToRecord(btn, card, onTranscribed) {
        if (!btn) return;
        if (!voiceSupported) {
            btn.disabled = true;
            return;
        }

        var mediaRecorder = null;
        var mediaStream = null;
        var audioChunks = [];
        var recording = false;

        function setStatus(msg, show) {
            var status = card.querySelector('[data-voice-status]');
            if (!status) return;
            if (show && msg) {
                status.textContent = msg;
                status.hidden = false;
            } else {
                status.hidden = true;
            }
        }

        function uploadAndTranscribe(blob) {
            if (!blob || blob.size < 200) {
                setStatus('', false);
                alert('Túl rövid felvétel – próbáld újra!');
                return;
            }
            setStatus(cfg.msgProcessing || 'Egy pillanat…', true);
            var fd = new FormData();
            fd.append('file', blob, 'answer.webm');
            fetch(transcribeUrl, { method: 'POST', body: fd })
                .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
                .then(function (res) {
                    setStatus('', false);
                    if (!res.ok || !res.data.text) {
                        alert('Nem értettem – próbáld újra!');
                        return;
                    }
                    onTranscribed(res.data.text.trim());
                })
                .catch(function () {
                    setStatus('', false);
                    alert('Hálózati hiba – próbáld újra!');
                });
        }

        function stopRecording() {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
            }
            btn.classList.remove('recording');
            recording = false;
        }

        function startRecording() {
            if (recording || globalVoiceBusy) return;
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(function (stream) {
                    mediaStream = stream;
                    audioChunks = [];
                    var mime = 'audio/webm';
                    if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
                        mime = 'audio/webm;codecs=opus';
                    } else if (!MediaRecorder.isTypeSupported('audio/webm')) {
                        mime = '';
                    }
                    mediaRecorder = new MediaRecorder(stream, mime ? { mimeType: mime } : undefined);
                    mediaRecorder.ondataavailable = function (e) {
                        if (e.data && e.data.size > 0) audioChunks.push(e.data);
                    };
                    mediaRecorder.onstop = function () {
                        if (mediaStream) {
                            mediaStream.getTracks().forEach(function (t) { t.stop(); });
                            mediaStream = null;
                        }
                        var type = (mediaRecorder && mediaRecorder.mimeType) || 'audio/webm';
                        uploadAndTranscribe(new Blob(audioChunks, { type: type }));
                    };
                    mediaRecorder.start();
                    recording = true;
                    btn.classList.add('recording');
                    setStatus(cfg.msgListening || 'Figyelek… 👂', true);
                })
                .catch(function () {
                    alert('Kérjük engedélyezd a mikrofon használatát!');
                });
        }

        btn.addEventListener('mousedown', function (e) {
            e.preventDefault();
            startRecording();
        });
        btn.addEventListener('touchstart', function (e) {
            e.preventDefault();
            startRecording();
        }, { passive: false });
        btn.addEventListener('mouseup', stopRecording);
        btn.addEventListener('mouseleave', stopRecording);
        btn.addEventListener('touchend', function (e) {
            e.preventDefault();
            stopRecording();
        });
        btn.addEventListener('touchcancel', stopRecording);
    }

    document.querySelectorAll('[data-read-aloud]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var card = btn.closest('[data-task-card]');
            if (!card || globalVoiceBusy) return;
            var text = getCardText(card, 'data-question-text');
            if (card.querySelector('.task-title')) {
                text = (card.querySelector('.task-title').textContent + '. ' + text).trim();
            }
            speakText(text);
        });
    });

    document.querySelectorAll('[data-task-card]').forEach(function (card) {
        var hintBtn = card.querySelector('[data-show-hint]');
        var answerBtn = card.querySelector('[data-show-answer]');
        var hintBox = card.querySelector('.task-hint');
        var answerBox = card.querySelector('.task-answer');
        var input = card.querySelector('[data-task-input]');
        var checkBtn = card.querySelector('[data-check-answer]');
        var feedbackBox = card.querySelector('[data-feedback-box]');
        var feedbackText = card.querySelector('[data-feedback-text]');
        var speakAnswerBtn = card.querySelector('[data-speak-answer]');
        var speakOptionalBtn = card.querySelector('[data-speak-answer-optional]');
        var taskIndex = parseInt(card.getAttribute('data-task-index'), 10);
        var wrongAttempts = 0;
        var hintUsed = false;

        function revealAnswerButton() {
            if (answerBtn) answerBtn.hidden = false;
        }

        if (hintBtn && hintBox) {
            hintBtn.addEventListener('click', function () {
                hintBox.hidden = false;
                hintBtn.hidden = true;
                hintUsed = true;
                revealAnswerButton();
                var hintText = getCardText(card, 'data-hint-text') ||
                    (hintBox.querySelector('p') && hintBox.querySelector('p').textContent) || '';
                if (voiceYoung && hintText) {
                    speakText(hintText);
                }
                hintBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            });
        }

        if (answerBtn && answerBox) {
            answerBtn.addEventListener('click', function () {
                answerBox.hidden = false;
                answerBtn.hidden = true;
                var ansText = getCardText(card, 'data-answer-text') ||
                    (answerBox.querySelector('p') && answerBox.querySelector('p').textContent) || '';
                if (voiceYoung && ansText) {
                    speakText(ansText);
                }
                answerBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            });
        }

        function setChecking(on) {
            if (checkBtn) {
                checkBtn.disabled = on;
                checkBtn.setAttribute('aria-busy', on ? 'true' : 'false');
            }
            if (input) input.disabled = on;
            if (speakAnswerBtn) speakAnswerBtn.disabled = on;
        }

        function showFeedback(text, isCorrect) {
            if (!feedbackBox || !feedbackText) return;
            feedbackText.textContent = text;
            feedbackBox.hidden = false;
            feedbackBox.classList.toggle('task-feedback-correct', !!isCorrect);
            feedbackBox.classList.toggle('task-feedback-wrong', !isCorrect);
            if (voiceYoung && text) {
                speakText(text);
            }
            feedbackBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        function submitCheck(answerOverride) {
            if (!checkUrl) return;
            var answer = (answerOverride || (input && input.value) || '').trim();
            if (!answer) {
                if (input && input.type !== 'hidden') input.focus();
                return;
            }
            if (input) input.value = answer;

            showEncouragement();
            setChecking(true);

            fetch(checkUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    task_index: taskIndex,
                    answer: answer
                })
            })
                .then(function (r) {
                    return r.json().then(function (d) {
                        return { ok: r.ok, data: d };
                    });
                })
                .then(function (res) {
                    setChecking(false);
                    if (!res.ok) {
                        showFeedback('Sajnos most nem tudom ellenőrizni. Próbáld újra! 🙂', false);
                        return;
                    }
                    var correct = !!res.data.correct;
                    showFeedback(res.data.feedback || '', correct);
                    if (!correct) {
                        wrongAttempts += 1;
                        if (wrongAttempts >= 2) {
                            revealAnswerButton();
                        }
                    }
                })
                .catch(function () {
                    setChecking(false);
                    showFeedback('Hálózati hiba – próbáld újra!', false);
                });
        }

        if (checkBtn) {
            checkBtn.addEventListener('click', function () { submitCheck(); });
        }
        if (input && input.type !== 'hidden') {
            input.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    submitCheck();
                }
            });
        }

        if (speakAnswerBtn) {
            bindHoldToRecord(speakAnswerBtn, card, function (text) {
                submitCheck(text);
            });
        }

        if (speakOptionalBtn) {
            bindHoldToRecord(speakOptionalBtn, card, function (text) {
                if (input) {
                    input.value = text;
                    input.focus();
                }
            });
        }
    });
});
