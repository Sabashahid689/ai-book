import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This config runs in Node.js (not in the browser)
const config: Config = {
  title: 'Physical AI & Humanoid Robotics — Essentials',
  tagline: 'A comprehensive guide to building intelligent physical systems',
  favicon: 'img/favicon.ico',

  // Future flags for Docusaurus v4 compatibility
  future: {
    v4: true,
  },

  // GitHub Pages deployment config
  url: 'https://sabashahid689.github.io', // your GitHub Pages URL
  baseUrl: '/website/',                  // repo name
  organizationName: 'Sabashahid689',     // GitHub username
  projectName: 'website',                // repo name

  onBrokenLinks: 'throw', // fail on broken links

  // Internationalization
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
        htmlLang: 'en-US',
      },
      ur: {
        label: 'اردو (Urdu)',
        direction: 'rtl',
        htmlLang: 'ur-PK',
      },
    },
  },

  // Presets
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/Sabashahid689/website/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  // Theme configuration
  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI Textbook',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'textbookSidebar',
          position: 'left',
          label: 'Chapters',
        },
        {
          href: 'https://github.com/Sabashahid689/website',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Textbook',
          items: [
            {
              label: 'Chapter 1: Introduction',
              to: '/docs/chapter-1-introduction-to-physical-ai',
            },
            {
              label: 'Chapter 6: Capstone',
              to: '/docs/chapter-6-capstone-ai-robot-pipeline',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Portfolio',
              href: 'https://saba-portfolio-seven.vercel.app/',
            },
            {
              label: 'Facebook',
              href: 'https://www.facebook.com/',
            },
            {
              label: 'Linkedin',
              href: 'https://www.linkedin.com/in/saba-malik-050325386',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/Sabashahid689/website',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'typescript', 'yaml', 'bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;