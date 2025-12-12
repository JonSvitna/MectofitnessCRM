# Quick Start Guide for New Integrations

This guide helps you quickly configure and test the newly implemented Zoom and Stripe integrations.

## Prerequisites

✅ Application is installed and running  
✅ You have admin access to the application  
✅ You have accounts on Zoom and Stripe  

## 🎥 Zoom Integration - 5 Minute Setup

### Step 1: Create Zoom App (3 minutes)

1. Visit [https://marketplace.zoom.us/](https://marketplace.zoom.us/)
2. Click **Develop** → **Build App**
3. Choose **Server-to-Server OAuth**
4. Fill in app name: "MectoFitness CRM"
5. Copy these credentials:
   - Account ID
   - Client ID
   - Client Secret
6. Add these scopes:
   - `meeting:write:admin`
   - `meeting:read:admin`
   - `user:read:admin`

### Step 2: Configure Application (1 minute)

Edit your `.env` file:

```bash
ZOOM_CLIENT_ID=your-client-id-here
ZOOM_CLIENT_SECRET=your-client-secret-here
ZOOM_ACCOUNT_ID=your-account-id-here
```

### Step 3: Test Integration (1 minute)

1. Restart the application
2. Log in to MectoFitness CRM
3. Go to **Settings** → **Integrations**
4. Click **Connect** next to Zoom
5. Status should show "Connected" ✅

### Usage

**Create a Zoom Meeting:**
```bash
# Via API
curl -X POST http://localhost:5000/api/v1/zoom/meetings \
  -H "Content-Type: application/json" \
  -d '{"session_id": 123}'
```

**From UI (when implemented):**
1. Go to Sessions
2. Select a session
3. Click "Add Video Conference"
4. Select Zoom
5. Meeting link is automatically created!

---

## 💳 Stripe Integration - 5 Minute Setup

### Step 1: Get Stripe Keys (2 minutes)

1. Visit [https://stripe.com](https://stripe.com) and sign in
2. Go to **Developers** → **API keys**
3. Copy **Test Mode** keys (for development):
   - Publishable key (starts with `pk_test_`)
   - Secret key (starts with `sk_test_`)

### Step 2: Configure Application (1 minute)

Edit your `.env` file:

```bash
STRIPE_SECRET_KEY=sk_test_your-secret-key-here
STRIPE_PUBLISHABLE_KEY=pk_test_your-publishable-key-here
```

### Step 3: Set Up Webhook (2 minutes)

1. In Stripe Dashboard: **Developers** → **Webhooks**
2. Click **Add endpoint**
3. Enter URL: `https://your-domain.com/api/v1/stripe/webhook`
4. Select these events:
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
   - `customer.subscription.created`
   - `customer.subscription.deleted`
5. Copy the **Signing secret** (starts with `whsec_`)
6. Add to `.env`:
   ```bash
   STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret-here
   ```

### Step 4: Test Integration

1. Restart the application
2. Log in to MectoFitness CRM
3. Go to **Settings** → **Integrations**
4. Click **Connect** next to Stripe
5. Status should show "Connected" ✅

### Test Payment

Use test card: **4242 4242 4242 4242**
- Expiry: Any future date
- CVV: Any 3 digits
- Postal: Any 5 digits

**Create Payment:**
```bash
curl -X POST http://localhost:5000/api/v1/stripe/payment-intents \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.00,
    "client_id": 123,
    "description": "Training Session"
  }'
```

---

## 🤖 AI Chatbot

Already configured! Just needs OpenAI API key:

### Setup (2 minutes)

1. Get API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Add to `.env`:
   ```bash
   OPENAI_API_KEY=sk-your-api-key-here
   ```
3. Restart application

### Usage

**Keyboard Shortcuts:**
- `Ctrl+/` (Windows/Linux) or `Cmd+/` (Mac) - Toggle chatbot
- `Escape` - Close chatbot

**Features:**
- Workout program advice
- Exercise recommendations
- Nutrition guidance
- Client management tips
- Platform help

---

## 🧪 Testing Checklist

### Zoom
- [ ] Integration status shows "Connected"
- [ ] Can create meeting for a session
- [ ] Meeting has valid URL and password
- [ ] Can delete a meeting
- [ ] Webhook receives meeting events

### Stripe
- [ ] Integration status shows "Connected"
- [ ] Can create Stripe customer
- [ ] Can create payment intent
- [ ] Test card payment succeeds
- [ ] Webhook receives payment events
- [ ] Payment status updates automatically

### Chatbot
- [ ] Chatbot button appears on left side
- [ ] Opens with Ctrl+/ keyboard shortcut
- [ ] Closes with Escape key
- [ ] Responds to messages
- [ ] Maintains conversation context

---

## 🚨 Troubleshooting

### Zoom Not Connecting
- ✅ Verify credentials in `.env`
- ✅ Check Zoom app is "Activated"
- ✅ Ensure all required scopes are added
- ✅ Check server logs for errors

### Stripe Not Working
- ✅ Using test keys (not live keys)
- ✅ Webhook endpoint is accessible
- ✅ Webhook secret matches `.env`
- ✅ Test with provided test card numbers

### Chatbot Not Responding
- ✅ OpenAI API key is valid
- ✅ Account has API credits
- ✅ Check browser console for errors
- ✅ Verify `/api/chatbot/` endpoint works

---

## 📚 Additional Resources

- **Zoom Setup**: See `ZOOM_SETUP.md` for detailed instructions
- **Stripe Setup**: See `STRIPE_SETUP.md` for security best practices
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY_DEC2024.md`
- **API Documentation**: See `API.md` for endpoint details

---

## 🎯 Next Steps

1. ✅ Configure Zoom (5 min)
2. ✅ Configure Stripe (5 min)
3. ✅ Test basic functionality (10 min)
4. 🔨 Build integration management UI
5. 🧪 End-to-end testing
6. 🚀 Deploy to production

---

## 💡 Tips

**Development:**
- Always use test mode for Stripe
- Test webhooks with Stripe CLI: `stripe listen --forward-to localhost:5000/api/v1/stripe/webhook`
- Check server logs for integration errors

**Production:**
- Switch to Stripe live keys
- Configure production webhook URLs
- Enable SSL/HTTPS
- Monitor integration status dashboard
- Set up error alerting

**Security:**
- Never commit API keys to git
- Rotate keys periodically
- Use different keys for dev/prod
- Monitor for suspicious activity

---

## Need Help?

- 📖 Check detailed setup guides
- 🐛 Review server logs
- 💬 Open an issue on GitHub
- 📧 Contact support

Happy Training! 💪
