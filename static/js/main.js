// Placeholder for site-wide JS
console.log('MindSight static JS loaded');

// Real-time message analysis
async function analyzeMessage(message) {
    try {
        const response = await fetch('/chat/api/analyze/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                message: message,
                user_id: getCurrentUserId() // Implement this based on your auth
            })
        });
        
        const result = await response.json();
        
        if (result.ml_available) {
            displayMlResults(result);
            handleRiskAssessment(result.risk_assessment);
            showRecommendations(result.recommendations);
        }
        
        return result;
    } catch (error) {
        console.error('ML Analysis failed:', error);
        return null;
    }
}

// Display ML results in your chat UI
function displayMlResults(result) {
    const emotions = result.analysis.emotions;
    const dominantEmotion = result.analysis.dominant_emotion;
    
    // Create emotion indicators in your chat UI
    const emotionHTML = `
        <div class="emotion-indicator">
            <span class="dominant-emotion">${dominantEmotion}</span>
            <div class="emotion-bar">
                ${Object.entries(emotions).map(([emotion, score]) => `
                    <div class="emotion-item" style="width: ${score * 100}%">
                        ${emotion}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    // Append to your chat message or sidebar
    document.getElementById('ml-results').innerHTML = emotionHTML;
}

// Handle risk assessment alerts
function handleRiskAssessment(riskData) {
    if (riskData.risk_category === 'high') {
        showEmergencyAlert(riskData);
    } else if (riskData.risk_category === 'medium') {
        showSupportMessage();
    }
}

// Show recommendations
function showRecommendations(recommendations) {
    if (recommendations && recommendations.length > 0) {
        const recHTML = recommendations.map(rec => `
            <div class="recommendation-card">
                <h4>${rec.icon} ${rec.title}</h4>
                <p>${rec.description}</p>
                <small>${rec.duration} minutes • ${rec.difficulty}</small>
            </div>
        `).join('');
        
        document.getElementById('recommendations-panel').innerHTML = recHTML;
    }
}

// Get CSRF token function
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}