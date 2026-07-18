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

const API_URL = '/api/explain';

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

function renderResults(data) {
    resultsList.innerHTML = '';
    resultsSection.classList.remove('hidden');

    const aiDisclaimer = document.getElementById('aiDisclaimer');

    if (data.mode === 'ai') {
        renderAiResponse(data.explanation);
        aiDisclaimer.classList.remove('hidden');
        return;
    }

    aiDisclaimer.classList.add('hidden');

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

function renderAiResponse(text) {
    const suggestionsIndex = text.indexOf('Suggestions:');

    let explanation = text;
    let suggestions = '';

    if (suggestionsIndex !== -1) {
        explanation = text.slice(0, suggestionsIndex).trim();
        suggestions = text.slice(suggestionsIndex + 'Suggestions:'.length).trim();
    }

    explanation = explanation.replace('Explanation:', '').trim();

    const explanationBlock = document.createElement('div');
    explanationBlock.className = 'ai-block';
    explanationBlock.innerHTML = `
        <h3 class="ai-block-title">Explanation</h3>
        <p class="ai-block-text">${explanation}</p>
    `;
    resultsList.appendChild(explanationBlock);

    if (suggestions) {
        const suggestionLines = suggestions
            .split('\n')
            .map(line => line.replace(/^[-•]\s*/, '').trim())
            .filter(line => line.length > 0);

        const suggestionsBlock = document.createElement('div');
        suggestionsBlock.className = 'ai-block';
        suggestionsBlock.innerHTML = `
            <h3 class="ai-block-title">Suggestions</h3>
            <ul class="ai-suggestions-list">
                ${suggestionLines.map(line => `<li>${line}</li>`).join('')}
            </ul>
        `;
        resultsList.appendChild(suggestionsBlock);
    }
}

function showError(message) {
    errorMsg.textContent = message;
    errorMsg.classList.remove('hidden');
}

function hideError() {
    errorMsg.classList.add('hidden');
}
