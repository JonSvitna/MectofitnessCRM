"""AI Chatbot API with OpenAI Integration."""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import openai
import os
from datetime import datetime

bp = Blueprint('ai_chatbot', __name__, url_prefix='/api/chatbot')

# Initialize OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

SYSTEM_PROMPT = """You are a helpful AI fitness assistant for MectoFitness CRM, a personal training management platform. 

Your role is to help personal trainers with:
- Creating effective workout programs
- Exercise recommendations and form tips
- Nutrition guidance
- Client management best practices
- Training methodologies and techniques
- Answering questions about the MectoFitness platform features

Keep responses concise, practical, and actionable. Use fitness industry terminology appropriately.
Be encouraging and professional. When discussing exercises, mention proper form and safety.

Available MectoFitness features:
- Client Management: Track client info, goals, and progress
- Session Scheduling: Book and manage training sessions
- Program Builder: Create custom workout programs
- Exercise Library: Browse 750+ exercises with instructions
- Progress Tracking: Monitor client measurements and achievements
- Calendar Integration: Sync with Google Calendar and Outlook

If asked about features not listed above, let the user know it may be coming in future updates."""


@bp.route('/', methods=['POST'])
@login_required
def chatbot():
    """Handle chatbot messages with OpenAI."""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        message_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'success': False, 'error': 'No message provided'}), 400
        
        if not openai.api_key:
            # Fallback response if OpenAI key not configured
            return jsonify({
                'success': True,
                'response': get_fallback_response(user_message)
            })
        
        # Build conversation history
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add recent message history for context
        for msg in message_history[-6:]:  # Last 3 exchanges
            role = "user" if msg['sender'] == 'user' else "assistant"
            messages.append({"role": role, "content": msg['text']})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",  # or "gpt-3.5-turbo" for faster/cheaper
            messages=messages,
            max_tokens=500,
            temperature=0.7,
            user=str(current_user.id)
        )
        
        ai_response = response.choices[0].message.content
        
        # Log the interaction (optional)
        log_chatbot_interaction(current_user.id, user_message, ai_response)
        
        return jsonify({
            'success': True,
            'response': ai_response
        })
        
    except Exception as e:
        print(f"Chatbot error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to process message',
            'response': get_fallback_response(user_message)
        }), 500


def get_fallback_response(message):
    """Provide basic responses when OpenAI is unavailable."""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['workout', 'program', 'exercise']):
        return "To create a workout program, go to Programs → Add Program. You can browse our exercise library with 750+ exercises by clicking Exercise Library in the navigation menu."
    
    elif any(word in message_lower for word in ['client', 'add client']):
        return "To add a new client, navigate to Clients → Add New Client. You can track their progress, assign programs, and schedule sessions from their profile page."
    
    elif any(word in message_lower for word in ['session', 'schedule', 'booking']):
        return "To schedule a training session, go to Sessions → Add Session. You can view all your sessions in calendar view and manage them easily."
    
    elif any(word in message_lower for word in ['help', 'how do', 'feature']):
        return "MectoFitness CRM offers: Client Management, Session Scheduling, Program Builder, Exercise Library (750+ exercises), Progress Tracking, and Calendar Integration. What would you like to know more about?"
    
    else:
        return "I'm here to help! I can assist with workout programming, exercise selection, client management, and using MectoFitness features. What would you like to know?"


def log_chatbot_interaction(user_id, user_message, ai_response):
    """Log chatbot interactions for analytics and improvement."""
    try:
        # You can implement database logging here if needed
        # For now, just print to console
        timestamp = datetime.utcnow().isoformat()
        print(f"[Chatbot] {timestamp} - User {user_id}: {user_message[:50]}...")
    except Exception as e:
        print(f"Error logging chatbot interaction: {e}")


@bp.route('/suggestions', methods=['GET'])
@login_required
def get_suggestions():
    """Get contextual suggestions based on user's current page."""
    page = request.args.get('page', 'dashboard')
    
    suggestions = {
        'dashboard': [
            "What should I focus on this week?",
            "Give me tips for client retention",
            "How can I improve my training business?"
        ],
        'clients': [
            "Best practices for onboarding new clients",
            "How to track client progress effectively",
            "Client communication tips"
        ],
        'programs': [
            "Create a beginner strength program",
            "Design a fat loss workout",
            "What's a good program split?"
        ],
        'sessions': [
            "How to structure a 1-hour session",
            "Tips for group training sessions",
            "Session planning best practices"
        ]
    }
    
    return jsonify({
        'success': True,
        'suggestions': suggestions.get(page, suggestions['dashboard'])
    })
