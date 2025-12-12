import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Mectofitness - Coaching Software That Runs Like a System | Online Coaching Platform',
  description: 'Mectofitness is the accountability-first fitness coaching platform for personal trainers. Manage clients, deliver training programs, track workouts, and scale your online coaching business with professional personal trainer software.',
  keywords: [
    'online coaching software',
    'personal trainer software',
    'fitness coaching platform',
    'client workout tracking',
    'coach messaging and check-ins',
    'training program delivery',
    'accountability coaching system',
    'fitness coaching app',
    'online training software',
    'personal training management',
  ],
  authors: [{ name: 'Mectofitness' }],
  creator: 'Mectofitness',
  publisher: 'Mectofitness',
  metadataBase: new URL('https://mectofitness.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'Mectofitness - Coaching Software That Runs Like a System',
    description: 'The accountability-first fitness coaching platform built for personal trainers. Deliver world-class online coaching and scale your training business.',
    url: 'https://mectofitness.com',
    siteName: 'Mectofitness',
    locale: 'en_US',
    type: 'website',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Mectofitness - Online Coaching Software',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Mectofitness - Coaching Software That Runs Like a System',
    description: 'The accountability-first fitness coaching platform built for personal trainers.',
    images: ['/twitter-image.png'],
    creator: '@mectofitness',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet" />
        <meta name="theme-color" content="#000000" />
      </head>
      <body className="antialiased font-sans">
        {children}
      </body>
    </html>
  );
}
