'use client';

import { Link } from "@heroui/link";
import { Code } from "@heroui/code";
import { button as buttonStyles } from "@heroui/theme";
import { RainbowButton } from "@/components/magicui/rainbow-button";

import { siteConfig } from "@/config/site";
import { title, subtitle } from "@/components/primitives";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  
  return (
    <section className="flex flex-col lg:flex-row items-start justify-between max-w-[1024px] mx-auto px-4 gap-16 pt-32 md:pt-48 pb-16 md:pb-24">
      {/* Left Column - Copy and CTA */}
      <div className="flex-1 max-w-xl">
        <h1 className="text-[64px] leading-[1.1] font-regular tracking-tight mb-8 text-left">
          <span>Never lose a</span>
          <br />
          <span className="text-black font-bold">
            struggling user
          </span>
          <br />
          <span>
            again.
          </span>
        </h1>
        
        <p className="text-gray-600 text-xl mb-12 leading-relaxed">
        AI agent that automatically detects struggling users via Mixpanel and guides them to success through voice conversations.
        </p>

        <div className="flex items-center gap-6 mb-16">
          <RainbowButton onClick={() => router.push(siteConfig.links.docs)}>
            Try Now
          </RainbowButton>
          <span className="text-gray-600">Integrates with Mixpanel</span>
        </div>

        <div>
          <p className="text-gray-600 mb-6">Trusted by product teams worldwide</p>
          <div className="flex gap-8 items-center opacity-75">
            <img src="/logos/company1.svg" alt="Company 1" className="h-8" />
            <img src="/logos/company2.svg" alt="Company 2" className="h-8" />
            <img src="/logos/company3.svg" alt="Company 3" className="h-8" />
          </div>
        </div>
      </div>

      {/* Right Column - Interactive Demo */}
      <div className="flex-1 max-w-xl w-full lg:mt-8">
        <div className="relative w-full min-h-[600px] bg-white rounded-3xl shadow-lg border border-black/10 overflow-hidden p-6">
          <div>
            {/* Analytics Alert */}
            <div className="demo-item absolute top-6 left-6 right-6">
              <div className="flex items-center gap-3 p-3 rounded-xl bg-black/5">
                <span className="px-3 py-0.5 text-sm font-medium bg-red-50 text-red-500 rounded-lg">ALERT</span>
                <span className="text-gray-600">3 users stuck on export feature</span>
              </div>
            </div>

            {/* Usage Pattern */}
            <div className="demo-item absolute top-[100px] left-6 right-6">
              <div className="flex items-center gap-3 p-3 rounded-xl bg-black/5">
                <div className="space-y-2">
                  <div className="h-1.5 w-32 bg-gray-100 rounded-full overflow-hidden">
                    <div className="h-full w-1/3 bg-black rounded-full"></div>
                  </div>
                  <p className="text-sm text-gray-600">Export attempts: 3</p>
                </div>
              </div>
            </div>

            {/* Voice Chat Initiation */}
            <div className="demo-item absolute top-[180px] left-6 right-6">
              <div className="flex items-center gap-3 p-3 rounded-xl bg-black/5">
                <span className="px-3 py-0.5 text-sm font-medium bg-green-50 text-green-500 rounded-lg">ACTIVE</span>
                <span className="text-gray-600">Voice assistance initiated</span>
              </div>
            </div>
          </div>

          {/* Chat Messages */}
          <div className="absolute bottom-6 left-6 right-6 space-y-4">
            <div className="chat-item">
              <div className="bg-black/5 p-4 rounded-xl inline-block ml-auto max-w-[85%] float-right clear-both">
                <p className="text-gray-600">👋 Hi! I noticed you're having trouble with the export feature. Let me help you with that!</p>
              </div>
            </div>
            <div className="chat-item relative">
              <div className="bg-gray-50 p-4 rounded-xl inline-block max-w-[85%] clear-both">
                <p className="text-gray-600">Yes, I can't find where to export as CSV...</p>
              </div>
              {/* Microphone Indicator */}
              <div className="absolute -left-8 top-1/2 -translate-y-1/2 w-6 h-6 rounded-full bg-black/10 flex items-center justify-center mic-pulse">
                <svg className="w-3.5 h-3.5 text-black" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
              </div>
            </div>
            <div className="chat-item">
              <div className="bg-black/5 p-4 rounded-xl inline-block ml-auto max-w-[85%] float-right clear-both">
                <p className="text-gray-600">I'll guide you through it! Click the ••• menu in the top right of your dashboard, then select "Export as CSV" 📊</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
