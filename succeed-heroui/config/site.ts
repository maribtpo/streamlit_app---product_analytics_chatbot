export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "Succeed - AI Product Analytics",
  description: "AI-powered product analytics that helps you understand your users better through intelligent voice interactions.",
  navItems: [
    {
      label: "Home",
      href: "/",
    },
    {
      label: "Features",
      href: "/features",
    },
    {
      label: "Pricing",
      href: "/pricing",
    },
    {
      label: "About",
      href: "/about",
    },
  ],
  navMenuItems: [
    {
      label: "Dashboard",
      href: "/dashboard",
    },
    {
      label: "Analytics",
      href: "/analytics",
    },
    {
      label: "Voice Chat",
      href: "/voice-chat",
    },
    {
      label: "Settings",
      href: "/settings",
    },
    {
      label: "Help & Support",
      href: "/help",
    },
    {
      label: "Logout",
      href: "/logout",
    },
  ],
  links: {
    github: "https://github.com/maribtpo/streamlit_app---product_analytics_chatbot",
    twitter: "https://twitter.com/succeed_ai",
    docs: "https://succeed.ai",
    discord: "https://discord.gg/succeed",
    sponsor: "https://patreon.com/succeed",
  },
};
