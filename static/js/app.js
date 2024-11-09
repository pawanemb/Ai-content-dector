// static/js/app.js
class AIDetectorApp {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
    }

    initializeElements() {
        // Input elements
        this.textInput = document.getElementById('textInput');
        this.charCount = document.getElementById('charCount');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        
        // Results elements
        this.resultsSection = document.getElementById('resultsSection');
        this.overallScore = document.getElementById('overallScore');
        this.scoreBar = document.getElementById('scoreBar');
        this.categoryScores = document.getElementById('categoryScores');
        this.analysisText = document.getElementById('analysisText');
    }

    attachEventListeners() {
        // Text input handler
        this.textInput.addEventListener('input', () => {
            const length = this.textInput.value.length;
            this.charCount.textContent = `${length} characters`;
            this.analyzeBtn.disabled = length < 50;
        });

        // Analyze button handler
        this.analyzeBtn.addEventListener('click', () => this.analyzeText());
    }

    async analyzeText() {
        try {
            this.setLoading(true);
            
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: this.textInput.value,
                    min_length: 50
                }),
            });

            if (!response.ok) {
                throw new Error(await response.text());
            }

            const result = await response.json();
            this.displayResults(result);
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.setLoading(false);
        }
    }

    displayResults(result) {
        // Show results section
        this.resultsSection.classList.remove('hidden');
        this.resultsSection.classList.add('fade-in');

        // Update overall score
        const overallScore = result.scores.overall;
        this.overallScore.textContent = `${(overallScore * 100).toFixed(1)}%`;
        
        // Update score bar
        this.scoreBar.style.width = `${overallScore * 100}%`;
        this.scoreBar.className = `score-bar-fill h-2.5 rounded-full ${this.getScoreColorClass(overallScore)}`;

        // Update category scores
        this.displayCategoryScores(result.scores);

        // Update analysis text
        this.analysisText.textContent = result.summary;
    }

    displayCategoryScores(scores) {
        this.categoryScores.innerHTML = '';
        
        Object.entries(scores).forEach(([category, score]) => {
            if (category === 'overall') return;

            const card = document.createElement('div');
            card.className = 'bg-gray-50 p-4 rounded-lg';
            card.innerHTML = `
                <h4 class="font-medium mb-2">${this.formatCategoryName(category)}</h4>
                <div class="text-lg font-bold mb-2">${(score * 100).toFixed(1)}%</div>
                <div class="w-full bg-gray-200 rounded-full h-1.5">
                    <div class="h-1.5 rounded-full ${this.getScoreColorClass(score)}" 
                         style="width: ${score * 100}%"></div>
                </div>
            `;
            this.categoryScores.appendChild(card);
        });
    }

    formatCategoryName(category) {
        return category.charAt(0).toUpperCase() + category.slice(1);
    }

    getScoreColorClass(score) {
        if (score < 0.4) return 'bg-green-500';
        if (score < 0.7) return 'bg-yellow-500';
        return 'bg-red-500';
    }

    setLoading(isLoading) {
        this.analyzeBtn.disabled = isLoading;
        this.analyzeBtn.innerHTML = isLoading ? 
            '<svg class="animate-spin h-5 w-5 mx-auto" viewBox="0 0 24 24">' +
            '<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>' +
            '<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>' :
            'Analyze Text';
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 fade-in';
        errorDiv.innerHTML = `
            <strong class="font-bold">Error!</strong>
            <span class="block sm:inline"> ${message}</span>
        `;
        
        this.resultsSection.parentNode.insertBefore(errorDiv, this.resultsSection);
        
        // Remove error after 5 seconds
        setTimeout(() => errorDiv.remove(), 5000);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AIDetectorApp();
});
