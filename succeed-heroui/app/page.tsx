import { Link } from "@heroui/link";
import { Code } from "@heroui/code";
import { button as buttonStyles } from "@heroui/theme";

import { siteConfig } from "@/config/site";
import { title, subtitle } from "@/components/primitives";

export default function Home() {
  return (
    <section className="flex flex-col lg:flex-row items-start justify-between max-w-[1024px] mx-auto px-4 gap-16 pt-32 md:pt-48 pb-16 md:pb-24">
      {/* Left Column - Copy and CTA */}
      <div className="flex-1 max-w-xl">
        <h1 className="text-[64px] leading-[1.1] font-regular tracking-tight mb-8 text-left">
          <span>Never lose a</span>
          <br />
          <span className="text-[#85f3b7] font-bold">
            stuck user
          </span>
          <br />
          <span>
            again.
          </span>
        </h1>
        
        <p className="text-gray-600 text-xl mb-12 leading-relaxed">
          AI agent that automatically detects when users are struggling with your product and guides them to success through natural voice conversations.
        </p>

        <div className="flex items-center gap-6 mb-16">
          <Link
            className={buttonStyles({ 
              size: "lg",
              radius: "full",
              className: "bg-black text-white hover:bg-black/90 px-8"
            })}
            href={siteConfig.links.docs}
          >
            Try Now
          </Link>
          <span className="text-gray-600">Integrates with Mixpanel 
            <br></br>or any analytics tool</span>
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

      {/* Right Column - Preview Card */}
      <div className="flex-1 max-w-xl w-full lg:mt-8">
        <div className="w-full bg-white rounded-2xl shadow-lg border border-[#85f3b7]/20">
          <div className="p-8">
            <h3 className="text-xl font-semibold mb-6">Active Monitoring</h3>
            
            <div className="space-y-4">
              <div className="flex items-center gap-3 p-4 rounded-xl bg-[#85f3b7]/10">
                <span className="px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-600">ALERT</span>
                <span>User stuck on feature X</span>
              </div>
              
              <div className="flex items-center gap-3 p-4 rounded-xl bg-[#85f3b7]/10">
                <span className="px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-600">ACTIVE</span>
                <span>Voice assistance initiated</span>
              </div>

              <button className="flex items-center gap-2 p-4 rounded-xl border-2 border-dashed border-gray-200 w-full text-gray-500 hover:bg-[#85f3b7]/5 transition-colors">
                <span>+</span> Configure alerts
              </button>
            </div>

            <div className="mt-8">
              <div className="bg-[#85f3b7]/10 p-4 rounded-xl inline-block ml-auto max-w-[80%] float-right">
                👋 Hi! I noticed you're having trouble with the export feature. Let me help you with that!
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
