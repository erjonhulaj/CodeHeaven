// Grabs DOM elements once so we don't re-query them on every interaction
const codeInput = document.getElementById('codeInput');
const modeButtons = document.querySelectorAll('.mode-btn');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const resultsList = document.getElementById('resultsList');
const errorMsg = document.getElementById('errorMsg');

let currentMode = 'local';

modeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        modeButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentMode = btn.dataset.mode;
    });
});

const API_URL = 'http://127.0.0.1:8000/api/explain';

analyzeBtn.addEventListener('click', async () => {
    const code = codeInput.value.trim();

    if (!code) {
        showError('Please paste some code first.');
        return;
    }

    hideError();
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing...';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code: code,
                language: 'python',
                mode: currentMode
            })
        });

        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }

        const data = await response.json();
        renderResults(data);
    } catch (err) {
        showError(`Something went wrong: ${err.message}`);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = 'Analyze';
    }
});

// Renders either local-mode findings (array of issues) or AI-mode text explanation
function renderResults(data) {
    resultsList.innerHTML = '';
    resultsSection.classList.remove('hidden');

    if (data.mode === 'ai') {
        const block = document.createElement('pre');
        block.className = 'ai-output';
        block.textContent = data.explanation;
        resultsList.appendChild(block);
        return;
    }

    const issues = data.explanation.issues;

    if (!issues || issues.length === 0) {
        resultsList.innerHTML = '<p class="no-issues">No issues found. Clean code.</p>';
        return;
    }

    issues.forEach(issue => {
        const card = document.createElement('div');
        card.className = `finding finding-${issue.severity}`;

        card.innerHTML = `
            <div class="finding-header">
                <span class="severity-badge">${issue.severity}</span>
                <span class="rule-name">${issue.rule}</span>
                ${issue.line ? `<span class="line-tag">Line ${issue.line}</span>` : ''}
            </div>
            <p class="finding-message">${issue.message}</p>
        `;

        resultsList.appendChild(card);
    });
}

function showError(message) {
    errorMsg.textContent = message;
    errorMsg.classList.remove('hidden');
}

function hideError() {
    errorMsg.classList.add('hidden');
}