/**
 * AI Chatbot Integration with OpenAI
 * MectoFitness CRM
 */

class AIChatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.init();
    }

    init() {
        this.createChatbotUI();
        this.attachEventListeners();
        this.loadWelcomeMessage();
    }

    createChatbotUI() {
        // Create chatbot button
        const button = document.createElement('button');
        button.className = 'ai-chatbot-button';
        button.innerHTML = '🤖';
        button.setAttribute('aria-label', 'Open AI Assistant');
        button.onclick = () => this.toggleChat();
        
        // Create chatbot window
        const window = document.createElement('div');
        window.className = 'ai-chatbot-window';
        window.id = 'ai-chatbot-window';
        window.innerHTML = `
            <div class="chatbot-header">
                <h3>🤖 AI Fitness Assistant</h3>
                <button class="chatbot-close" onclick="window.chatbot.toggleChat()">×</button>
            </div>
            <div class="chatbot-messages" id="chatbot-messages">
                <!-- Messages will be inserted here -->
            </div>
            <div class="chatbot-input-area">
                <input 
                    type="text" 
                    class="chatbot-input" 
                    id="chatbot-input" 
                    placeholder="Ask me anything about fitness..."
                    autocomplete="off"
                />
                <button class="chatbot-send" id="chatbot-send">
                    <span>➤</span>
                </button>
            </div>
        `;
        
        document.body.appendChild(button);
        document.body.appendChild(window);
    }

    attachEventListeners() {
        const input = document.getElementById('chatbot-input');
        const sendBtn = document.getElementById('chatbot-send');
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && input.value.trim()) {
                this.sendMessage(input.value.trim());
                input.value = '';
            }
        });
        
        sendBtn.addEventListener('click', () => {
            if (input.value.trim()) {
                this.sendMessage(input.value.trim());
                input.value = '';
            }
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const window = document.getElementById('ai-chatbot-window');
        window.classList.toggle('active');
        
        if (this.isOpen) {
            document.getElementById('chatbot-input').focus();
        }
    }

    loadWelcomeMessage() {
        const welcomeMsg = "👋 Hi! I'm your AI Fitness Assistant. I can help you with:\n\n" +
            "• Creating workout programs\n" +
            "• Exercise recommendations\n" +
            "• Nutrition advice\n" +
            "• Client management tips\n" +
            "• Training best practices\n\n" +
            "How can I assist you today?";
        
        this.addMessage(welcomeMsg, 'ai');
    }

    async sendMessage(text) {
        // Add user message to chat
        this.addMessage(text, 'user');
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send to backend API
            const response = await fetch('/api/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: text,
                    history: this.messages.slice(-10) // Send last 10 messages for context
                })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator();
            
            if (data.success) {
                this.addMessage(data.response, 'ai');
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'ai');
            }
        } catch (error) {
            console.error('Chatbot error:', error);
            this.removeTypingIndicator();
            this.addMessage('Sorry, I\'m having trouble connecting. Please check your internet connection.', 'ai');
        }
    }

    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}`;
        
        const avatar = document.createElement('div');
        avatar.className = `message-avatar ${sender}`;
        avatar.innerHTML = sender === 'ai' ? '🤖' : '👤';
        
        const content = document.createElement('div');
        content.className = `message-content ${sender}`;
        content.textContent = text;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Store message
        this.messages.push({ text, sender, timestamp: new Date() });
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatbot-messages');
        const indicator = document.createElement('div');
        indicator.className = 'chat-message ai typing-indicator';
        indicator.id = 'typing-indicator';
        indicator.innerHTML = `
            <div class="message-avatar ai">🤖</div>
            <div class="message-content ai">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        `;
        messagesContainer.appendChild(indicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
}

// Quick action suggestions
const quickActions = [
    {
        icon: '💪',
        text: 'Create workout',
        action: () => window.location.href = '/programs/add'
    },
    {
        icon: '👥',
        text: 'Add client',
        action: () => window.location.href = '/clients/add'
    },
    {
        icon: '📅',
        text: 'Schedule session',
        action: () => window.location.href = '/sessions/add'
    },
    {
        icon: '📚',
        text: 'Browse exercises',
        action: () => window.location.href = '/exercise-library'
    }
];

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new AIChatbot();
});

// Gamification Functions
function updateXPBar(current, total) {
    const percentage = (current / total) * 100;
    const xpBar = document.querySelector('.xp-bar-fill');
    const xpText = document.querySelector('.xp-bar-text');
    
    if (xpBar) {
        xpBar.style.width = percentage + '%';
    }
    if (xpText) {
        xpText.textContent = `${current} / ${total} XP`;
    }
}

function showAchievementPopup(achievement) {
    const popup = document.createElement('div');
    popup.className = 'achievement-popup';
    popup.innerHTML = `
        <div class="achievement-popup-content">
            <div class="achievement-icon">🏆</div>
            <div class="achievement-details">
                <h3>Achievement Unlocked!</h3>
                <p>${achievement.name}</p>
                <small>+${achievement.xp} XP</small>
            </div>
        </div>
    `;
    
    document.body.appendChild(popup);
    
    setTimeout(() => {
        popup.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        popup.classList.remove('show');
        setTimeout(() => popup.remove(), 300);
    }, 4000);
}

// Streak tracking
function updateStreakDisplay(days) {
    const streakElement = document.querySelector('.streak-counter');
    if (streakElement) {
        streakElement.innerHTML = `
            <span class="streak-flame">🔥</span>
            <span>${days} Day Streak!</span>
        `;
    }
}

// Progress animations
function animateCountUp(element, target, duration = 1000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = Math.round(target);
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, 16);
}

// Initialize dashboard animations
document.addEventListener('DOMContentLoaded', () => {
    // Animate stat values on dashboard
    document.querySelectorAll('.stat-value-large').forEach(stat => {
        const target = parseInt(stat.textContent);
        if (!isNaN(target)) {
            stat.textContent = '0';
            animateCountUp(stat, target, 1500);
        }
    });
});
