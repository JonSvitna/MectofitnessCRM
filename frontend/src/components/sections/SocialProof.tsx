'use client';

import { motion } from 'framer-motion';
import { Award, Shield, Zap, TrendingUp, Heart, Star } from 'lucide-react';

export function SocialProof() {
  const proofItems = [
    { icon: Star, text: '4.9/5 rating from 2,500+ reviews' },
    { icon: Shield, text: 'GDPR & HIPAA compliant' },
    { icon: Zap, text: 'Lightning-fast performance' },
    { icon: TrendingUp, text: '10,000+ active coaches' },
    { icon: Heart, text: '98% client satisfaction' },
    { icon: Award, text: 'Best coaching software 2024' },
  ];

  return (
    <section className="relative py-12 sm:py-16 border-y border-white/10 bg-white/[0.01]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8"
        >
          {proofItems.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="flex flex-col items-center text-center space-y-2"
            >
              <div className="p-3 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl">
                <item.icon size={24} className="text-orange-500" />
              </div>
              <p className="text-xs sm:text-sm text-gray-400 leading-tight">
                {item.text}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
