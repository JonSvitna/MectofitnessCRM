import { cn } from '@/lib/cn';
import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}

export function Card({ children, className, hover = false }: CardProps) {
  return (
    <div
      className={cn(
        'bg-white/[0.02] backdrop-blur-sm border border-white/10 rounded-2xl p-8',
        'shadow-lg shadow-black/10',
        hover && 'transition-all duration-300 hover:bg-white/[0.04] hover:border-white/20 hover:-translate-y-1 hover:shadow-xl hover:shadow-black/20',
        className
      )}
    >
      {children}
    </div>
  );
}
