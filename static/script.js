const API_BASE_URL = '';  // Keep empty when frontend & backend are same server

// State management
let chatHistory = [];

// ==================== PAGE NAVIGATION ====================
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    initializeGuidanceForm();
    initializeChat();
    initializeLawyers();
    initializeScrollAnimations();
});

function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.page');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            const targetPage = link.getAttribute('data-page');
            
            // Update active nav link
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Update active page
            pages.forEach(p => p.classList.remove('active'));
            document.getElementById(`${targetPage}-page`).classList.add('active');
            
            // Hide chat on non-home pages
            const chatToggle = document.getElementById('chat-toggle');
            const chatWindow = document.getElementById('chat-window');
            if (targetPage === 'home') {
                chatToggle.style.display = 'flex';
            } else {
                chatToggle.style.display = 'none';
                chatWindow.classList.remove('active');
            }
            
            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
}

// ==================== LEGAL GUIDANCE FORM ====================
function initializeGuidanceForm() {
    const form = document.getElementById('guidance-form');
    const input = document.getElementById('problem-input');
    const submitBtn = form.querySelector('.btn-primary');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const problem = input.value.trim();
        if (!problem) return;
        
        // Show loading state
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        submitBtn.disabled = true;
        
        try {
            const response = await fetch(`${API_BASE_URL}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ problem })
            });
            
            if (!response.ok) {
                throw new Error('Failed to get response from server');
            }
            
            const data = await response.json();
            displayResponse(data);
            checkEmergency(data);
            
            // Smooth scroll to response
            setTimeout(() => {
                document.getElementById('response-section').scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }, 100);
            
        } catch (error) {
            console.error('Error:', error);

            // Show backend error inside response section instead of popup
            document.getElementById('response-heard').innerHTML =
                "<p>We are currently unable to process your request.</p>";

            document.getElementById('response-law').innerHTML =
                "<p>Please check if the backend server is running.</p>";

            document.getElementById('response-steps').innerHTML =
                "<p>Try refreshing the page or restarting the server.</p>";

            document.getElementById('response-helplines').innerHTML =
                "<p>Emergency: 112<br>Women Helpline: 181</p>";

            document.getElementById('response-disclaimer').innerHTML =
                "<p>This is general information, not legal advice.</p>";

            document.getElementById('response-section').style.display = 'block';

        } finally {
            // Reset button state
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
            submitBtn.disabled = false;
        }
    });
}

function displayResponse(data) {
    const responseSection = document.getElementById('response-section');
    
    // Populate response sections
    // Show related laws instead of "You Are Heard"
    if (data.related_laws && data.related_laws.length > 0) {

        const lawsHtml = data.related_laws.map(law => `
            <li style="margin-bottom:15px;">
                <strong>${law.law_id} – ${law.law_name}</strong><br>
                <b>Act:</b> ${law.act}<br>
                <b>Category:</b> ${law.category}<br>
                <b>Emergency:</b> ${law.emergency ? "Yes" : "No"}<br>
                <b>Description:</b> ${law.description}
            </li>
        `).join("");

        document.getElementById('response-heard').innerHTML =
            `<ul>${lawsHtml}</ul>`;

    } else {
        document.getElementById('response-heard').innerHTML =
            "<p>No related laws found.</p>";
    }

    document.getElementById('response-law').innerHTML = formatText(data.what_the_law_says || 'Legal information is being prepared.');
    document.getElementById('response-steps').innerHTML = formatText(data.your_next_steps || 'Please consult with a legal professional.');
    document.getElementById('response-helplines').innerHTML = formatText(data.helplines || 'Emergency: 112<br>Women Helpline: 181');
    document.getElementById('response-disclaimer').innerHTML = formatText(data.disclaimer || 'This is general information, not legal advice.');
    
    // Show response section with animation
    responseSection.style.display = 'block';

    const responseCard = responseSection.querySelector('.response-card');
    if (responseCard) {
        responseCard.classList.remove('fade-in');
        void responseCard.offsetWidth;
        responseCard.classList.add('fade-in');
    }
}

function formatText(text) {
    if (!text) return '';
    
    // Convert newlines to <br> and handle basic formatting
    return text
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^(.+)$/, '<p>$1</p>');
}

function checkEmergency(data) {
    // Check for emergency keywords in response
    const emergencyKeywords = ['immediate danger', 'violence', 'emergency', 'urgent', 'call 112', 'safety'];
    const allText = JSON.stringify(data).toLowerCase();
    
    const hasEmergency = emergencyKeywords.some(keyword => allText.includes(keyword));
    
    const banner = document.getElementById('emergency-banner');
    if (hasEmergency) {
        banner.style.display = 'block';
    } else {
        banner.style.display = 'none';
    }
}

// ==================== CHAT FUNCTIONALITY ====================
function initializeChat() {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatClose = document.getElementById('chat-close');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.querySelector('.typing-indicator');
    
    // Toggle chat window
    chatToggle.addEventListener('click', () => {
        chatWindow.classList.add('active');
        chatInput.focus();
    });
    
    // Close chat window
    chatClose.addEventListener('click', () => {
        chatWindow.classList.remove('active');
    });
    
    // Handle chat form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addChatMessage(message, 'user');
        chatInput.value = '';
        
        // Show typing indicator
        typingIndicator.style.display = 'inline-flex';
        scrollChatToBottom();
        
        try {
            const response = await fetch('/chat', {

                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) {
                throw new Error('Failed to get chat response');
            }
            
            const data = await response.json();
            
            // Hide typing indicator
            typingIndicator.style.display = 'none';
            
            // Add bot response to chat
            addChatMessage(data.response || 'I apologize, but I couldn\'t process that. Could you rephrase?', 'bot');
            
        } catch (error) {
            console.error('Chat error:', error);
            typingIndicator.style.display = 'none';
            addChatMessage('I\'m having trouble connecting right now. Please try again in a moment.', 'bot');
        }
    });
}

function addChatMessage(content, type) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    scrollChatToBottom();
}

function scrollChatToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ==================== LAWYERS PAGE ====================
function initializeLawyers() {
    const lawyersData = [
        {
            name: 'Adv. Priya Sharma',
            specialization: 'Domestic Violence & Family Law',
            experience: 12,
            city: 'Mumbai',
            phone: '+91 98765 43210',
            email: 'priya.sharma@legalaid.in'
        },
        {
            name: 'Adv. Meera Reddy',
            specialization: 'Workplace Harassment & Employment',
            experience: 8,
            city: 'Bangalore',
            phone: '+91 98765 43211',
            email: 'meera.reddy@legalaid.in'
        },
        {
            name: 'Adv. Anjali Desai',
            specialization: 'Women\'s Rights & Civil Matters',
            experience: 15,
            city: 'Delhi',
            phone: '+91 98765 43212',
            email: 'anjali.desai@legalaid.in'
        },
        {
            name: 'Adv. Kavita Patel',
            specialization: 'Divorce & Matrimonial Law',
            experience: 10,
            city: 'Ahmedabad',
            phone: '+91 98765 43213',
            email: 'kavita.patel@legalaid.in'
        },
        {
            name: 'Adv. Lakshmi Iyer',
            specialization: 'Sexual Harassment & Criminal Law',
            experience: 14,
            city: 'Chennai',
            phone: '+91 98765 43214',
            email: 'lakshmi.iyer@legalaid.in'
        },
        {
            name: 'Adv. Sunita Kapoor',
            specialization: 'Property Rights & Inheritance',
            experience: 11,
            city: 'Pune',
            phone: '+91 98765 43215',
            email: 'sunita.kapoor@legalaid.in'
        }
    ];
    
    const lawyersGrid = document.getElementById('lawyers-grid');
    
    lawyersData.forEach((lawyer, index) => {
        const card = createLawyerCard(lawyer, index);
        lawyersGrid.appendChild(card);
    });
}

function createLawyerCard(lawyer, index) {
    const card = document.createElement('div');
    card.className = 'lawyer-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    card.innerHTML = `
        <div class="lawyer-icon">⚖ </div>
        <h3 class="lawyer-name">${lawyer.name}</h3>
        <div class="lawyer-specialization">${lawyer.specialization}</div>
        <div class="lawyer-details">
            <div class="lawyer-detail">
                <span class="lawyer-detail-icon">📍</span>
                <span>${lawyer.city}</span>
            </div>
            <div class="lawyer-detail">
                <span class="lawyer-detail-icon">⏱️</span>
                <span>${lawyer.experience} years experience</span>
            </div>
            <div class="lawyer-detail">
                <span class="lawyer-detail-icon">📞</span>
                <span>${lawyer.phone}</span>
            </div>
            ${lawyer.email ? `
                <div class="lawyer-detail">
                    <span class="lawyer-detail-icon">✉️</span>
                    <span>${lawyer.email}</span>
                </div>
            ` : ''}
        </div>
        <button class="lawyer-contact-btn" onclick="contactLawyer('${lawyer.name}', '${lawyer.email}')">
            Contact
        </button>
    `;
    
    return card;
}

function contactLawyer(name, email) {
    // Option 1: Open email client
    window.location.href = `mailto:${email}?subject=Legal Consultation Request`;
    
    // Option 2: You could also show a modal with contact info
    // alert(`Contact ${name} at ${email}`);
}

// ==================== UTILITY FUNCTIONS ====================

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
    };

    const observer = new IntersectionObserver((entries, currentObserver) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                currentObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.scroll-section, .lawyer-card');
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// Error handling for API calls
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    // Optionally show user-friendly error message
});

