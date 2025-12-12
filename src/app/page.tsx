import { Navbar } from '@/components/sections/Navbar';
import { Hero } from '@/components/sections/Hero';
import { SocialProof } from '@/components/sections/SocialProof';
import { Features } from '@/components/sections/Features';
import { Difference } from '@/components/sections/Difference';
import { Pricing } from '@/components/sections/Pricing';
import { FAQ } from '@/components/sections/FAQ';
import { CTA } from '@/components/sections/CTA';
import { Footer } from '@/components/sections/Footer';

export default function HomePage() {
  return (
    <main className="relative min-h-screen bg-black">
      <Navbar />
      <Hero />
      <SocialProof />
      <Features />
      <Difference />
      <Pricing />
      <FAQ />
      <CTA />
      <Footer />
    </main>
  );
}
