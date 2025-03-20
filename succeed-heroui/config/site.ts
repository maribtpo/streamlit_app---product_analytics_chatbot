export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "Succeed",
  description: "AI agent that automatically detects when users are struggling with your product and guides them to success through natural voice conversations.",
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
    }
  ],
  navMenuItems: [
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
    {
      label: "Login",
      href: "/login",
    }
  ],
  links: {
    github: "https://github.com/maribtpo/succeed",
    twitter: "https://twitter.com/succeed",
    docs: "https://docs.succeed.ai",
    discord: "https://discord.gg/succeed",
    sponsor: "https://github.com/sponsors/succeed",
    login: "/login",
    signup: "/signup"
  },
};
