'use client';

import { Button } from '@/components/ui/Button';
import { motion } from 'framer-motion';
import { ArrowRight, CheckCircle2, BarChart3, Calendar, MessageSquare, Users } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
      {/* Grid background */}
      <div className="absolute inset-0 grid-background" />
      
      {/* Blue glow */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl glow-blue" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-32">
        <div className="text-center space-y-8">
          {/* Proof chips */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="flex flex-wrap justify-center gap-4 mb-8"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/5 backdrop-blur-sm border border-white/10 rounded-full text-sm text-gray-300">
              <CheckCircle2 size={16} className="text-green-400" />
              <span>Trusted by 10,000+ coaches</span>
            </div>
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/5 backdrop-blur-sm border border-white/10 rounded-full text-sm text-gray-300">
              <CheckCircle2 size={16} className="text-green-400" />
              <span>Free 14-day trial</span>
            </div>
          </motion.div>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight"
          >
            <span className="text-white">Coaching software</span>
            <br />
            <span className="bg-gradient-to-r from-orange-500 via-orange-600 to-orange-500 bg-clip-text text-transparent">
              that runs like a system
            </span>
          </motion.h1>

          {/* Subheadline */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="max-w-3xl mx-auto text-lg sm:text-xl text-gray-400 leading-relaxed"
          >
            Mectofitness is the accountability-first fitness coaching platform that helps personal trainers deliver world-class online coaching, manage clients effortlessly, and scale their training business with professional workout tracking and program delivery.
          </motion.p>

          {/* CTAs */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <Button variant="primary" size="lg" className="group" href="/register">
              Start Free Trial
              <ArrowRight size={20} className="ml-2 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button variant="secondary" size="lg" href="#features">
              View Features
            </Button>
          </motion.div>

          {/* Mini Dashboard Preview */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.5 }}
            className="mt-16 max-w-5xl mx-auto"
          >
            <div className="relative">
              {/* Glow effect behind preview */}
              <div className="absolute inset-0 bg-gradient-to-t from-orange-500/20 to-blue-500/20 blur-3xl transform -translate-y-12" />
              
              {/* Dashboard preview card */}
              <div className="relative bg-gradient-to-br from-white/[0.03] to-white/[0.01] backdrop-blur-sm border border-white/20 rounded-2xl p-6 sm:p-8 shadow-2xl">
                {/* Browser chrome */}
                <div className="flex items-center gap-2 mb-6 pb-4 border-b border-white/10">
                  <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500/50" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
                    <div className="w-3 h-3 rounded-full bg-green-500/50" />
                  </div>
                  <div className="flex-1 text-center text-sm text-gray-500">
                    app.mectofitness.com
                  </div>
                </div>

                {/* Mini dashboard UI */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4 hover:bg-white/10 transition-colors">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="p-2 bg-orange-500/10 rounded-lg">
                        <Users size={20} className="text-orange-500" />
                      </div>
                      <div className="text-2xl font-bold text-white">124</div>
                    </div>
                    <div className="text-sm text-gray-400">Active Clients</div>
                  </div>

                  <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4 hover:bg-white/10 transition-colors">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="p-2 bg-blue-500/10 rounded-lg">
                        <Calendar size={20} className="text-blue-500" />
                      </div>
                      <div className="text-2xl font-bold text-white">48</div>
                    </div>
                    <div className="text-sm text-gray-400">Sessions Today</div>
                  </div>

                  <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4 hover:bg-white/10 transition-colors">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="p-2 bg-purple-500/10 rounded-lg">
                        <MessageSquare size={20} className="text-purple-500" />
                      </div>
                      <div className="text-2xl font-bold text-white">12</div>
                    </div>
                    <div className="text-sm text-gray-400">New Messages</div>
                  </div>

                  <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4 hover:bg-white/10 transition-colors">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="p-2 bg-green-500/10 rounded-lg">
                        <BarChart3 size={20} className="text-green-500" />
                      </div>
                      <div className="text-2xl font-bold text-white">94%</div>
                    </div>
                    <div className="text-sm text-gray-400">Check-in Rate</div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
