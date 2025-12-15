'use client';

import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { motion } from 'framer-motion';
import { Check, Sparkles } from 'lucide-react';

export function Pricing() {
  const tiers = [
    {
      name: 'Starter',
      price: '$29',
      period: '/month',
      description: 'Perfect for new coaches getting started',
      features: [
        'Up to 10 active clients',
        'Unlimited programs & workouts',
        'Basic messaging',
        'Mobile app access',
        'Email support',
      ],
      cta: 'Start Free Trial',
      popular: false,
    },
    {
      name: 'Professional',
      price: '$79',
      period: '/month',
      description: 'For established trainers scaling their business',
      features: [
        'Up to 50 active clients',
        'Unlimited programs & workouts',
        'Advanced messaging & check-ins',
        'Mobile app access',
        'Priority support',
        'Custom branding',
        'Analytics & reporting',
        'Calendar integrations',
      ],
      cta: 'Start Free Trial',
      popular: true,
    },
    {
      name: 'Enterprise',
      price: '$199',
      period: '/month',
      description: 'For coaching businesses and gym teams',
      features: [
        'Unlimited clients',
        'Everything in Professional',
        'Multi-coach accounts',
        'White-label mobile app',
        'Dedicated account manager',
        'API access',
        'Custom integrations',
        'SLA guarantee',
      ],
      cta: 'Contact Sales',
      popular: false,
    },
  ];

  return (
    <section id="pricing" className="relative py-20 sm:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-4">
            Simple, transparent{' '}
            <span className="bg-gradient-to-r from-orange-500 to-orange-600 bg-clip-text text-transparent">
              pricing
            </span>
          </h2>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto">
            Start with a 14-day free trial. No credit card required. Cancel anytime.
          </p>
        </motion.div>

        {/* Pricing cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {tiers.map((tier, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="relative"
            >
              {tier.popular && (
                <div className="absolute -top-4 left-0 right-0 flex justify-center">
                  <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-gradient-to-r from-orange-500 to-orange-600 rounded-full text-sm font-semibold text-white shadow-lg shadow-orange-500/30">
                    <Sparkles size={16} />
                    Most Popular
                  </div>
                </div>
              )}
              <Card 
                className={`h-full ${
                  tier.popular 
                    ? 'border-orange-500/30 bg-gradient-to-br from-white/[0.04] to-white/[0.02]' 
                    : ''
                }`}
              >
                <div className="flex flex-col h-full">
                  {/* Tier header */}
                  <div className="mb-6">
                    <h3 className="text-xl font-semibold text-white mb-2">
                      {tier.name}
                    </h3>
                    <p className="text-sm text-gray-400">{tier.description}</p>
                  </div>

                  {/* Price */}
                  <div className="mb-6">
                    <div className="flex items-baseline gap-1">
                      <span className="text-4xl sm:text-5xl font-bold text-white">
                        {tier.price}
                      </span>
                      <span className="text-gray-400">{tier.period}</span>
                    </div>
                  </div>

                  {/* Features */}
                  <div className="flex-1 mb-6">
                    <ul className="space-y-3">
                      {tier.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="flex items-start gap-3">
                          <div className="flex-shrink-0 w-5 h-5 bg-orange-500/10 rounded-full flex items-center justify-center mt-0.5">
                            <Check size={14} className="text-orange-500" />
                          </div>
                          <span className="text-gray-300 text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* CTA */}
                  <Button 
                    variant={tier.popular ? 'primary' : 'secondary'} 
                    className="w-full"
                    href="/register"
                  >
                    {tier.cta}
                  </Button>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Bottom note */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mt-12 text-center"
        >
          <p className="text-gray-400">
            All plans include our mobile app, unlimited storage, and 99.9% uptime SLA.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
