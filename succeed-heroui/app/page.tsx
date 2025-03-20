import { Link } from "@heroui/link";
import { Snippet } from "@heroui/snippet";
import { Code } from "@heroui/code";
import { button as buttonStyles } from "@heroui/theme";

import { siteConfig } from "@/config/site";
import { title, subtitle } from "@/components/primitives";
import { GithubIcon } from "@/components/icons";

export default function Home() {
  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <div className="inline-block max-w-xl text-center justify-center">
        <span className={title()}>AI-Powered&nbsp;</span>
        <span className={title({ color: "violet" })}>Product Analytics&nbsp;</span>
        <br />
        <span className={title()}>
          that helps you understand your users better.
        </span>
        <div className={subtitle({ class: "mt-4" })}>
          Detect stuck users, analyze behavior patterns, and provide proactive support through intelligent voice interactions.
        </div>
      </div>

      <div className="flex gap-3">
        <Link
          isExternal
          className={buttonStyles({
            color: "primary",
            radius: "full",
            variant: "shadow",
          })}
          href={siteConfig.links.docs}
        >
          Try Demo
        </Link>
        <Link
          isExternal
          className={buttonStyles({ variant: "bordered", radius: "full" })}
          href={siteConfig.links.github}
        >
          <GithubIcon size={20} />
          GitHub
        </Link>
      </div>

      <div className="mt-8">
        <Snippet hideCopyButton hideSymbol variant="bordered">
          <span>
            Powered by <Code color="primary">Mixpanel</Code> and <Code color="primary">OpenAI</Code>
          </span>
        </Snippet>
      </div>
    </section>
  );
}
