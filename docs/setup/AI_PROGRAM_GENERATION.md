# AI Program Generation Setup

## Overview
MectoFitness CRM now includes AI-powered workout program generation using OpenAI's GPT-4. This feature automatically creates complete, personalized training programs based on client goals, fitness level, and your 722-exercise library.

## Features
- 🤖 **Intelligent Program Design**: GPT-4 creates evidence-based workout plans
- 💪 **Exercise Selection**: Automatically selects from 722 professional exercises
- 📊 **Progressive Overload**: Built-in periodization and progression
- 🎯 **Personalized**: Considers client fitness level, goals, and medical conditions
- ⚡ **Fast Generation**: Complete programs in 10-20 seconds
- 📝 **Detailed Instructions**: Sets, reps, tempo, rest periods, and form cues

## Setup Instructions

### 1. Get Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to **API Keys** section
4. Click **Create new secret key**
5. Copy the key (starts with `sk-...`)

### 2. Configure Environment Variable

#### For Local Development:
Add to your `.env` file:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

#### For Production (Railway, Render, Vercel):
Add environment variable in your hosting platform:
- **Name**: `OPENAI_API_KEY`
- **Value**: Your OpenAI API key

### 3. Verify Configuration

1. Restart your application
2. Create a new training program
3. Click "🤖 Generate AI Program"
4. If configured correctly, program will generate in 10-20 seconds

## Usage

### Generating a Program

1. **Create Program**: Go to Programs → Create Program
2. **Fill Details**: Add client, goal, duration, difficulty level
3. **Generate**: Click "🤖 Generate AI Program" button
4. **Configure**: Select training frequency (2-6 days/week)
5. **Generate**: Click "Generate Program" and wait 10-20 seconds

### What Gets Generated

The AI creates:
- **Complete workout split** (e.g., Push/Pull/Legs, Upper/Lower)
- **Weekly structure** with progressive overload
- **Exercise selection** from your 722-exercise library
- **Sets, reps, rest periods** for each exercise
- **Form cues and safety notes**
- **Progression guidelines**
- **Nutrition and recovery tips**

## Cost Information

### Pricing (as of 2024)
- **GPT-4 Turbo**: ~$0.02-0.05 per program generation
- **GPT-3.5 Turbo**: ~$0.002-0.005 per program generation

### Estimated Monthly Costs
- **Low Usage** (10 programs/month): $0.20-0.50
- **Medium Usage** (50 programs/month): $1.00-2.50
- **High Usage** (200 programs/month): $4.00-10.00

### Changing the Model

To use a different model, edit `app/services/ai_program_generator.py`:

```python
# For GPT-4 Turbo (Recommended - best quality)
self.model = "gpt-4-turbo-preview"

# For GPT-3.5 Turbo (Faster and cheaper)
self.model = "gpt-3.5-turbo"

# For GPT-4 (Most capable, slower)
self.model = "gpt-4"
```

## Example Generated Program

```json
{
  "program_overview": "12-week hypertrophy program with progressive overload",
  "training_split": "Push/Pull/Legs",
  "weeks": [
    {
      "week_number": 1,
      "focus": "Establishing baseline strength and form",
      "workouts": [
        {
          "day": 1,
          "title": "Push Day - Chest, Shoulders, Triceps",
          "exercises": [
            {
              "exercise_name": "Barbell Bench Press",
              "sets": 4,
              "reps": "8-10",
              "rest_seconds": 120,
              "tempo": "2-0-2-0",
              "notes": "Keep shoulder blades retracted, lower to chest"
            }
          ]
        }
      ]
    }
  ]
}
```

## Troubleshooting

### "OpenAI API key not configured"
- Ensure `OPENAI_API_KEY` is set in environment variables
- Restart your application after adding the key
- Check that key starts with `sk-`

### "Rate limit exceeded"
- OpenAI has rate limits on API calls
- Wait a few minutes and try again
- Consider upgrading your OpenAI plan

### "Model not found"
- Ensure you have access to GPT-4 in your OpenAI account
- Some accounts need to add payment method first
- Try switching to `gpt-3.5-turbo` in the code

### Generation Takes Too Long
- Normal generation time is 10-20 seconds
- GPT-4 is slower but higher quality than GPT-3.5
- Check your internet connection

## Best Practices

1. **Complete Program Details**: Fill in client info, goals, and fitness level for best results
2. **Review Generated Programs**: Always review AI output before assigning to clients
3. **Customize as Needed**: Edit generated exercises to fit specific needs
4. **Track Performance**: Monitor how AI programs perform vs manual ones
5. **Provide Feedback**: Note what works well to improve future generations

## Features Coming Soon

- **Program Templates**: Save and reuse successful program structures
- **Client Feedback Integration**: AI learns from client progress
- **Video Demonstrations**: Auto-link exercises to video tutorials
- **Nutrition Integration**: AI-generated meal plans matching workout intensity
- **Recovery Optimization**: Smart deload weeks and periodization

## Support

For issues or questions:
- Check OpenAI status: https://status.openai.com/
- Review OpenAI docs: https://platform.openai.com/docs
- Contact support if key issues persist
