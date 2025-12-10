# AI Chatbot Setup Guide

## Overview
MectoFitness CRM now includes an intelligent AI chatbot powered by OpenAI to assist trainers with workout programming, exercise recommendations, nutrition guidance, and platform navigation.

## Features
- 🤖 **Intelligent Assistance**: Powered by GPT-4 for accurate fitness advice
- 💬 **Context-Aware**: Remembers conversation history
- 🎯 **Fitness-Focused**: Trained specifically for personal training scenarios
- 📚 **Platform Knowledge**: Understands MectoFitness features and navigation
- ⚡ **Fallback Responses**: Works even without OpenAI API (basic responses)

## Setup Instructions

### 1. Get Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to **API Keys** section
4. Click **"Create new secret key"**
5. Copy your API key (starts with `sk-...`)
6. **Important**: Store it securely - you won't see it again!

### 2. Add API Key to Railway

#### Option A: Railway Dashboard (Recommended)
1. Go to your Railway project dashboard
2. Click on your **web service** (MectoFitnessCRM)
3. Navigate to the **Variables** tab
4. Click **"+ New Variable"**
5. Add:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: `sk-...` (your actual API key)
6. Railway will automatically redeploy

#### Option B: Local Development
```bash
# Add to your .env file
OPENAI_API_KEY=sk-...your-api-key-here
```

### 3. Configure Model (Optional)

The chatbot uses GPT-4 Turbo by default. To change the model, edit `app/routes/api_chatbot.py`:

```python
# For GPT-4 Turbo (Recommended - more capable)
model="gpt-4-turbo-preview"

# For GPT-3.5 Turbo (Faster and cheaper)
model="gpt-3.5-turbo"

# For GPT-4 (Most capable, slower)
model="gpt-4"
```

### 4. Usage Limits & Cost

#### Pricing (as of Dec 2024)
- **GPT-4 Turbo**: $0.01 per 1K input tokens, $0.03 per 1K output tokens
- **GPT-3.5 Turbo**: $0.0005 per 1K input tokens, $0.0015 per 1K output tokens

#### Cost Estimation
Average chat message costs:
- **GPT-4 Turbo**: ~$0.02 per exchange
- **GPT-3.5 Turbo**: ~$0.002 per exchange

For 100 conversations/day:
- **GPT-4 Turbo**: ~$60/month
- **GPT-3.5 Turbo**: ~$6/month

#### Set Usage Limits
1. Go to [OpenAI Billing](https://platform.openai.com/account/billing/limits)
2. Set **Hard Limit** to prevent overuse (e.g., $50/month)
3. Add email alerts for usage thresholds

### 5. Fallback Mode

If the OpenAI API key is not set or the API is unavailable, the chatbot automatically uses fallback responses that provide:
- Basic navigation help
- Feature explanations
- Direct links to key pages
- Simple Q&A responses

This ensures users always get help, even without OpenAI.

## Chatbot Features

### What It Can Help With

#### Workout Programming
```
"Create a beginner strength training program"
"Give me a HIIT workout for fat loss"
"What's a good 3-day split?"
```

#### Exercise Selection
```
"Best exercises for building chest"
"Alternative to barbell squats?"
"Show me bodyweight leg exercises"
```

#### Nutrition Advice
```
"Protein intake for muscle gain?"
"Meal planning tips for clients"
"Best post-workout nutrition"
```

#### Client Management
```
"How to onboard new clients?"
"Tips for client retention"
"How to track client progress?"
```

#### Platform Navigation
```
"How do I create a program?"
"Where's the exercise library?"
"How to schedule sessions?"
```

### Customization

Edit the system prompt in `app/routes/api_chatbot.py` to customize the chatbot's personality and knowledge:

```python
SYSTEM_PROMPT = """You are a helpful AI fitness assistant...
[Customize this to match your brand voice]
"""
```

## User Interface

### Chatbot Button
- **Location**: Bottom-right corner (floating button)
- **Icon**: 🤖 Robot emoji
- **Animation**: Subtle floating animation
- **Always Visible**: Accessible from any page

### Chat Window
- **Size**: 400x600px (mobile-responsive)
- **Position**: Opens above the button
- **Features**:
  - Message history
  - Typing indicators
  - Smooth animations
  - Auto-scroll to latest message

### Keyboard Shortcuts
- **Enter**: Send message
- **Esc**: Close chat window (coming soon)

## Monitoring & Analytics

### View Logs
```bash
# Check chatbot usage logs
tail -f logs/chatbot.log
```

### Track Usage
OpenAI Dashboard provides:
- API call counts
- Token usage
- Cost tracking
- Rate limit monitoring

## Troubleshooting

### Issue: "Sorry, I encountered an error"
**Solutions:**
1. Check if `OPENAI_API_KEY` is set in Railway
2. Verify API key is valid on OpenAI dashboard
3. Check usage limits aren't exceeded
4. View logs for detailed error messages

### Issue: Slow Responses
**Solutions:**
1. Switch to GPT-3.5 Turbo (faster)
2. Reduce `max_tokens` parameter
3. Check OpenAI API status page

### Issue: Rate Limiting
**Solutions:**
1. Implement request queue
2. Add user-based rate limiting
3. Upgrade OpenAI plan
4. Use fallback mode during peak times

## Best Practices

### 1. Monitor Costs
- Set up billing alerts
- Review usage weekly
- Use GPT-3.5 for testing

### 2. Improve Responses
- Update system prompt based on common questions
- Add specific fitness domain knowledge
- Include your gym's policies/procedures

### 3. User Education
- Show example questions
- Add quick suggestion buttons
- Provide feedback mechanism

### 4. Security
- Never expose API key in frontend code
- Rotate keys periodically
- Monitor for unusual usage patterns

## Advanced Features (Coming Soon)

- [ ] Voice input/output
- [ ] Image analysis (exercise form check)
- [ ] Workout video generation
- [ ] Integration with client profiles
- [ ] Automated program suggestions
- [ ] Multi-language support

## Support

For issues or questions:
- Check OpenAI documentation: https://platform.openai.com/docs
- Review chatbot logs
- Test with fallback mode first
- Contact support if persistent issues

## Updates

**Version 1.0** (Current)
- GPT-4 Turbo integration
- Context-aware conversations
- Fallback response system
- Basic fitness knowledge base

**Planned Enhancements**
- Fine-tuned model for fitness
- Integration with exercise library
- Client-specific recommendations
- Voice assistant mode
