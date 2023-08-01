// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Jaseci Documentation',
  tagline: 'Re-think AI Product Development',
  favicon: 'img/favicon.ico',

  // Production URL
  url: 'https://www.jaseci.org/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  organizationName: 'Jaseci-Labs', // GitHub org/user name.
  projectName: 'jaseci', // Repo name.

  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'warn',

  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/Jaseci-Labs/jaseci',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/favicon.jpg',
      navbar: {
        title: 'Jaseci',
        logo: {
          alt: 'Jaseci Logo',
          src: 'img/favicon.png',
        },
        items: [

          {
            type: 'docSidebar',
            sidebarId: 'docsSidebar',
            position: 'left',
            label: 'Docs',
          },
          {
            type: 'docSidebar',
            sidebarId: 'tutorialsSidebar',
            position: 'left',
            label: 'Tutorials',
          },
          { to: 'https://api.jaseci.org/docs/', label: 'API', position: 'left' },
          {
            href: 'https://github.com/Jaseci-Labs/jaseci',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/jaseci',
              }
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Jaseci Labs.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: false,
      },

      algolia: {

        // The application ID provided by Algolia
        appId: 'HUG2QGQRE1',

        // Public API key: it is safe to commit it
        apiKey: '735d15bf10dc6d2ebb51f24e06e4635e',

        indexName: 'jaseci_jaseci_docs',

        // Optional: see doc section below
        contextualSearch: true,

        // Optional: path for search page that enabled by default (`false` to disable it)
        searchPagePath: 'search',

      }
    }),
    plugins: [require.resolve('docusaurus-lunr-search')]
};

module.exports = config;
