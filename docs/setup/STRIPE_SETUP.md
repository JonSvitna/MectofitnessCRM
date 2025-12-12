# Stripe Payment Integration Setup Guide

This guide will help you set up Stripe payment processing with MectoFitness CRM.

## Prerequisites

- A Stripe account (sign up at [stripe.com](https://stripe.com))
- Admin access to your MectoFitness CRM instance
- SSL certificate for your domain (required for payment processing)

## Step 1: Create a Stripe Account

1. Go to [https://stripe.com](https://stripe.com) and sign up
2. Complete your account verification
3. Provide business details and banking information

## Step 2: Get Your API Keys

1. Log in to your Stripe Dashboard
2. Click "Developers" in the left sidebar
3. Go to "API keys"
4. You'll see two types of keys:
   - **Publishable key** (starts with `pk_`) - Used in client-side code
   - **Secret key** (starts with `sk_`) - Used in server-side code

### Test Mode vs. Live Mode

Stripe provides separate keys for test and live environments:
- **Test keys** (for development): Use these during development and testing
- **Live keys** (for production): Use these only when you're ready to process real payments

⚠️ **Important**: Never use live keys in development!

## Step 3: Configure Environment Variables

Add the following variables to your `.env` file:

```bash
# Stripe Integration
# For development, use test keys (they start with sk_test_ and pk_test_)
STRIPE_SECRET_KEY=sk_test_your-secret-key-here
STRIPE_PUBLISHABLE_KEY=pk_test_your-publishable-key-here

# For production, use live keys (they start with sk_live_ and pk_live_)
# STRIPE_SECRET_KEY=sk_live_your-secret-key-here
# STRIPE_PUBLISHABLE_KEY=pk_live_your-publishable-key-here
```

## Step 4: Set Up Webhook Endpoint

Webhooks allow Stripe to notify your application about payment events.

1. In the Stripe Dashboard, go to "Developers" → "Webhooks"
2. Click "Add endpoint"
3. Enter your webhook URL:
   ```
   https://your-domain.com/api/v1/stripe/webhook
   ```
4. Select events to listen to:
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`

5. Copy the "Signing secret" and add it to your `.env`:
   ```bash
   STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret-here
   ```

## Step 5: Connect in MectoFitness CRM

1. Log in to your MectoFitness CRM account
2. Navigate to **Settings** → **Integrations**
3. Find "Stripe" in the list of available integrations
4. Click "Connect"
5. Verify that the connection status shows as "Connected"

## Using Stripe Integration

### One-Time Payments

1. Go to **Payments** in the navigation menu
2. Click "Create Payment"
3. Select the client
4. Enter the amount and description
5. Click "Create Payment Intent"
6. Share the payment link with your client
7. Client completes payment using their credit card
8. Payment status updates automatically via webhook

### Recurring Subscriptions

1. First, create a product in Stripe Dashboard:
   - Go to "Products" → "Add product"
   - Set name (e.g., "Monthly Training Package")
   - Set price and billing interval
   - Note the Price ID (starts with `price_`)

2. In MectoFitness CRM:
   - Go to client's profile
   - Click "Add Subscription"
   - Enter the Stripe Price ID
   - System creates subscription automatically
   - Client receives payment notification

### Supported Payment Methods

Stripe supports various payment methods:
- **Credit/Debit Cards**: Visa, Mastercard, American Express, Discover
- **Digital Wallets**: Apple Pay, Google Pay
- **Bank Transfers**: ACH (US), SEPA (Europe)
- **Buy Now, Pay Later**: Klarna, Afterpay

## Payment Flow

1. **Create Customer**: First-time clients get a Stripe customer ID
2. **Create Payment Intent**: Generate a secure payment intent
3. **Client Pays**: Client enters card details on secure Stripe form
4. **Webhook Notification**: Stripe notifies your app of payment status
5. **Update Database**: Payment record updates to "completed"
6. **Receipt**: Client receives automatic email receipt from Stripe

## Security Best Practices

### Never Log or Store Card Details
- **Never** log card numbers, CVV, or full card data
- Let Stripe handle all sensitive card information
- Use Stripe's secure payment forms

### Protect Your Secret Key
- Never commit secret keys to version control
- Use environment variables only
- Rotate keys if accidentally exposed
- Different keys for test/live environments

### Verify Webhooks
- Always verify webhook signatures
- The application automatically validates all webhooks
- Invalid webhooks are rejected automatically

### SSL/HTTPS Required
- Stripe requires HTTPS for all production endpoints
- Obtain an SSL certificate for your domain
- Test mode works with HTTP for development

## Testing

### Test Card Numbers

Use these cards in test mode:

| Card Number | Description |
|------------|-------------|
| 4242 4242 4242 4242 | Successful payment |
| 4000 0000 0000 0002 | Card declined |
| 4000 0000 0000 9995 | Insufficient funds |
| 4000 0025 0000 3155 | 3D Secure authentication required |

- Use any future expiration date
- Use any 3-digit CVV
- Use any billing postal code

### Testing Webhooks Locally

1. Install Stripe CLI:
   ```bash
   # macOS
   brew install stripe/stripe-cli/stripe
   
   # Other platforms: https://stripe.com/docs/stripe-cli
   ```

2. Forward webhooks to local server:
   ```bash
   stripe listen --forward-to localhost:5000/api/v1/stripe/webhook
   ```

3. Trigger test events:
   ```bash
   stripe trigger payment_intent.succeeded
   ```

## Going Live

Before accepting real payments:

1. **Complete Stripe Account Setup**
   - Verify your business information
   - Add bank account for payouts
   - Set up tax settings

2. **Switch to Live Keys**
   - Replace test keys with live keys in `.env`
   - Update webhook endpoint to production URL
   - Test with a small real transaction

3. **Configure Payout Schedule**
   - Set how often you receive payouts
   - Default is usually 2-7 business days

4. **Enable Statement Descriptors**
   - Set how charges appear on customer statements
   - Use your business name for clarity

## Fees and Pricing

Stripe charges per successful transaction:
- **2.9% + $0.30** for card payments (US)
- **0.8%** for ACH transfers
- Fees vary by country and payment method

Check [Stripe's pricing page](https://stripe.com/pricing) for your region.

## Troubleshooting

### Connection Failed
- Verify API keys are correct
- Check keys match the environment (test vs. live)
- Ensure keys have proper permissions

### Payments Not Processing
- Verify SSL certificate is valid
- Check Stripe Dashboard logs for errors
- Ensure webhook endpoint is accessible

### Webhook Not Receiving Events
- Verify webhook URL is correct and publicly accessible
- Check webhook signing secret matches `.env`
- Review Stripe Dashboard webhook logs
- Test with Stripe CLI

## Advanced Features

### Refunds
```python
# Process a refund via Stripe Dashboard or API
# Refunds are credited back to customer's card
```

### Disputes/Chargebacks
- Monitor Stripe Dashboard for disputes
- Respond promptly with evidence
- Keep training session records as proof of service

### Revenue Reports
- Use Stripe Dashboard for detailed reports
- Export transaction data to CSV
- Integrate with accounting software (QuickBooks, Xero)

## Support

### Stripe Resources
- [Stripe Documentation](https://stripe.com/docs)
- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Support](https://support.stripe.com/)

### MectoFitness CRM Support
- Open an issue in the GitHub repository
- Email: support@mectofitness.com

## Compliance

- **PCI Compliance**: Stripe handles PCI compliance
- **GDPR**: Review Stripe's data handling for EU clients
- **Receipts**: Stripe automatically sends receipts
- **Tax**: Configure tax collection in Stripe Dashboard

## Next Steps

1. Test payment flow with test cards
2. Create sample products/subscriptions
3. Process a small live transaction
4. Monitor transactions in Stripe Dashboard
5. Set up automatic payout to your bank account
