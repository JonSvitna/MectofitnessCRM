'use client';

import { Card } from '@/components/ui/Card';
import { motion } from 'framer-motion';
import { 
  Dumbbell, 
  MessageSquare, 
  Calendar, 
  BarChart3, 
  Smartphone,
  FileText
} from 'lucide-react';

export function Features() {
  const features = [
    {
      icon: Dumbbell,
      title: 'Training Program Delivery',
      description: 'Build and deliver custom workout programs with our intuitive program builder. Track exercises, sets, reps, and client progress with ease.',
    },
    {
      icon: MessageSquare,
      title: 'Coach Messaging & Check-ins',
      description: 'Stay connected with your clients through built-in messaging. Automated check-in reminders ensure accountability and consistent progress tracking.',
    },
    {
      icon: Calendar,
      title: 'Session Scheduling',
      description: 'Seamlessly schedule training sessions, sync with your calendar, and send automated reminders. Never miss a session again.',
    },
    {
      icon: BarChart3,
      title: 'Client Workout Tracking',
      description: 'Monitor every rep, set, and workout your clients complete. Visualize progress with detailed analytics and performance metrics.',
    },
    {
      icon: Smartphone,
      title: 'Mobile-First Experience',
      description: 'Your clients access their programs on any device. Responsive design ensures a perfect experience on mobile, tablet, or desktop.',
    },
    {
      icon: FileText,
      title: 'Assessment & Forms',
      description: 'Collect client data with customizable intake forms. Track measurements, photos, and assessments all in one place.',
    },
  ];

  return (
    <section id="features" className="relative py-20 sm:py-32">
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
            Everything you need for{' '}
            <span className="bg-gradient-to-r from-orange-500 to-orange-600 bg-clip-text text-transparent">
              online coaching software
            </span>
          </h2>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto">
            Professional personal trainer software built for coaches who want to deliver exceptional results while running their business efficiently.
          </p>
        </motion.div>

        {/* Features grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card hover className="h-full">
                <div className="flex flex-col h-full">
                  <div className="p-3 bg-orange-500/10 rounded-xl w-fit mb-4">
                    <feature.icon size={28} className="text-orange-500" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-400 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
