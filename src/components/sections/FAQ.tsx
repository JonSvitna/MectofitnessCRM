'use client';

import { Card } from '@/components/ui/Card';
import { motion } from 'framer-motion';
import { Plus, Minus } from 'lucide-react';
import { useState } from 'react';

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const faqs = [
    {
      question: 'What makes Mectofitness different from other coaching platforms?',
      answer: 'Mectofitness is built specifically for fitness coaches with an accountability-first approach. Unlike generic project management tools, our platform is designed to keep clients engaged with automated check-ins, intuitive workout tracking, and seamless communication. We focus on what actually works for online coaching.',
    },
    {
      question: 'Do I need any technical skills to use Mectofitness?',
      answer: 'Not at all! Mectofitness is designed to be intuitive and easy to use. You can onboard your first client and start delivering programs within minutes. Our clean interface and guided setup make it simple for any trainer to get started.',
    },
    {
      question: 'Can my clients access their programs on mobile?',
      answer: 'Yes! Your clients get access to a mobile-optimized experience where they can view workouts, log their progress, message you, and complete check-ins. The platform works seamlessly on any device - phone, tablet, or computer.',
    },
    {
      question: 'What kind of support do you offer?',
      answer: 'All plans include email support with responses within 24 hours. Professional and Enterprise plans get priority support. Enterprise customers also receive a dedicated account manager and phone support.',
    },
    {
      question: 'Can I try Mectofitness before committing?',
      answer: 'Absolutely! We offer a 14-day free trial with full access to all features. No credit card required to start. You can explore the platform, onboard clients, and see if it\'s the right fit for your coaching business.',
    },
    {
      question: 'How does billing work?',
      answer: 'We bill monthly or annually (save 20% with annual billing). You can upgrade, downgrade, or cancel at any time. If you exceed your plan\'s client limit, we\'ll notify you and help you upgrade seamlessly.',
    },
    {
      question: 'Is my client data secure?',
      answer: 'Yes. We take security seriously. All data is encrypted in transit and at rest. We\'re GDPR compliant and follow industry best practices for data protection. We never sell or share your data with third parties.',
    },
    {
      question: 'Can I customize the platform with my branding?',
      answer: 'Professional and Enterprise plans include custom branding options. You can add your logo, colors, and custom domain. Enterprise plans also offer white-label mobile apps.',
    },
  ];

  return (
    <section id="faq" className="relative py-20 sm:py-32 bg-white/[0.01]">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-4">
            Frequently asked{' '}
            <span className="bg-gradient-to-r from-orange-500 to-orange-600 bg-clip-text text-transparent">
              questions
            </span>
          </h2>
          <p className="text-lg text-gray-400">
            Everything you need to know about the platform.
          </p>
        </motion.div>

        {/* FAQ items */}
        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.05 }}
            >
              <Card className="cursor-pointer" hover>
                <button
                  onClick={() => setOpenIndex(openIndex === index ? null : index)}
                  className="w-full text-left"
                >
                  <div className="flex items-start justify-between gap-4">
                    <h3 className="text-lg font-semibold text-white pr-8">
                      {faq.question}
                    </h3>
                    <div className="flex-shrink-0 w-6 h-6 bg-orange-500/10 rounded-full flex items-center justify-center">
                      {openIndex === index ? (
                        <Minus size={16} className="text-orange-500" />
                      ) : (
                        <Plus size={16} className="text-orange-500" />
                      )}
                    </div>
                  </div>
                  
                  {openIndex === index && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.3 }}
                      className="mt-4 text-gray-400 leading-relaxed"
                    >
                      {faq.answer}
                    </motion.div>
                  )}
                </button>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
