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
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.overallScore = document.getElementById('overallScore');
        this.scoreBar = document.getElementById('scoreBar');
        this.featureScores = document.getElementById('featureScores');
        this.detailedAnalysis = document.getElementById('detailedAnalysis');
        this.visualizationChart = document.getElementById('visualizationChart');
    }

    attachEventListeners() {
        // Update character count and button state
        this.textInput.addEventListener('input', () => {
            const length = this.textInput.value.length;
            this.charCount.textContent = `${length} characters`;
            this.analyzeBtn.disabled = length < 50;
        });

        // Handle analysis button click
        this.analyzeBtn.addEventListener('click', () => this.analyzeText());
    }

    async analyzeText() {
        try {
            this.showLoading(true);
            
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
            this.showLoading(false);
        }
    }

    displayResults(result) {
        // Show results section
        this.resultsSection.classList.remove('hidden');
        
        // Update overall score
        const overallScore = result.scores.overall;
        this.overallScore.textContent = `${(overallScore * 100).toFixed(1)}%`;
        this.scoreBar.style.width = `${overallScore * 100}%`;
        this.scoreBar.className = this.getScoreColorClass(overallScore);

        // Update feature scores
        this.updateFeatureScores(result.scores);
        
        // Update detailed analysis
        this.detailedAnalysis.innerHTML = result.summary.replace(/\n/g, '<br>');
        
        // Create visualization
        this.createVisualization(result.scores);
    }

    updateFeatureScores(scores) {
        this.featureScores.innerHTML = '';
        
        Object.entries(scores).forEach(([feature, score]) => {
            if (feature === 'overall') return;
            
            const card = document.createElement('div');
            card.className = 'feature-card';
            card.innerHTML = `
                <h4>${feature.charAt(0).toUpperCase() + feature.slice(1)}</h4>
                <div class="feature-score">${(score * 100).toFixed(1)}%</div>
                <div class="score-bar">
                    <div class="score-bar-fill ${this.getScoreColorClass(score)}" 
                         style="width: ${score * 100}%"></div>
                </div>
            `;
            this.featureScores.appendChild(card);
        });
    }

    createVisualization(scores) {
        const data = [{
            type: 'bar',
            x: Object.keys(scores).filter(k => k !== 'overall'),
            y: Object.values(scores).filter((_, i) => Object.keys(scores)[i] !== 'overall').map(v => v * 100),
            marker: {
                color: Object.values(scores)
                    .filter((_, i) => Object.keys(scores)[i] !== 'overall')
                    .map(score => this.getScoreColor(score))
            }
        }];

        const layout = {
            title: 'Feature Score Distribution',
            yaxis: {
                title: 'Score (%)',
                range: [0, 100]
            },
            margin: { t: 40, r: 20, b: 40, l: 40 }
        };

        Plotly.newPlot(this.visualizationChart, data, layout);
    }

    getScoreColorClass(score) {
        if (score < 0.4) return 'score-low';
        if (score < 0.7) return 'score-medium';
        return 'score-high';
    }

    getScoreColor(score) {
        if (score < 0.4) return 'rgb(34, 197, 94)';
        if (score < 0.7) return 'rgb(234, 179, 8)';
        return 'rgb(239, 68, 68)';
    }

    showLoading(show) {
        this.loadingIndicator.classList.toggle('hidden', !show);
        this.analyzeBtn.disabled = show;
    }

    showError(message) {
        alert(`Analysis failed: ${message}`);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AIDetectorApp();
});