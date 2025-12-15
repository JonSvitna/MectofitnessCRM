'use client';

import { Card } from '@/components/ui/Card';
import { motion } from 'framer-motion';
import { Check, X } from 'lucide-react';

export function Difference() {
  const ourAdvantages = [
    'Built specifically for fitness coaching and personal training',
    'Accountability-first UX that keeps clients engaged',
    'No complex setup - start coaching in minutes',
    'Mobile app that clients actually use',
    'Automated check-ins and progress tracking',
    'All-in-one platform: no need for multiple tools',
  ];

  const theirLimitations = [
    'Generic project management tools repurposed for coaching',
    'Clients forget to check in and fall off track',
    'Hours of setup before you can onboard a client',
    'Clunky mobile experience or no mobile app',
    'Manual follow-ups that drain your time',
    'Juggling spreadsheets, WhatsApp, and payment apps',
  ];

  return (
    <section className="relative py-20 sm:py-32 bg-white/[0.01]">
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
            Why Mectofitness is{' '}
            <span className="bg-gradient-to-r from-orange-500 to-orange-600 bg-clip-text text-transparent">
              different
            </span>
          </h2>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto">
            We&apos;re not just another fitness coaching platform. We&apos;re an accountability coaching system built from the ground up for personal trainers who demand excellence.
          </p>
        </motion.div>

        {/* Comparison grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Mectofitness - Us */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <Card className="h-full border-orange-500/20">
              <div className="flex items-center gap-3 mb-6">
                <div className="px-4 py-1.5 bg-orange-500/10 border border-orange-500/20 rounded-full">
                  <span className="text-sm font-semibold text-orange-500">Mectofitness</span>
                </div>
              </div>
              <div className="space-y-4">
                {ourAdvantages.map((advantage, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-6 h-6 bg-green-500/10 rounded-full flex items-center justify-center mt-0.5">
                      <Check size={16} className="text-green-500" />
                    </div>
                    <p className="text-gray-300 leading-relaxed">{advantage}</p>
                  </div>
                ))}
              </div>
            </Card>
          </motion.div>

          {/* Other platforms - Them */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <Card className="h-full">
              <div className="flex items-center gap-3 mb-6">
                <div className="px-4 py-1.5 bg-white/5 border border-white/10 rounded-full">
                  <span className="text-sm font-semibold text-gray-400">Other Platforms</span>
                </div>
              </div>
              <div className="space-y-4">
                {theirLimitations.map((limitation, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-6 h-6 bg-red-500/10 rounded-full flex items-center justify-center mt-0.5">
                      <X size={16} className="text-red-500" />
                    </div>
                    <p className="text-gray-500 leading-relaxed">{limitation}</p>
                  </div>
                ))}
              </div>
            </Card>
          </motion.div>
        </div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-12 text-center"
        >
          <p className="text-lg text-gray-400">
            Join thousands of coaches who have switched to a system that actually works.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
