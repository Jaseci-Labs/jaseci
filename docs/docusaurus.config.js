// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Jaseci Offical Documentation',
  tagline: 'Powering The Next Generation Of AI Products',
  url: 'https://docs.jaseci.org/',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.png',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Jaseci Labs', // Usually your GitHub org/user name.
  projectName: 'jaseci', // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
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
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
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
      navbar: {
        title: '',
        logo: {
          alt: 'Jaseci Logo',
          src: 'img/jaseci_logo.png',
        },
        items: [
          {to: 'docs/getting-started/getting-to-know-jaseci', activeBasePath:'docs/getting-started',label: 'Introduction', position: 'left'},
          {to:'docs/Developing_with_JAC/Overview',activeBasePath:'docs/Developing_with_JAC',label:'Development',position :'left'},
          {to:'docs/Tools_and_Features/Overview',activeBasePath:'docs/Tools_and_Features',label:'Tools and Features',position :'left'},
          //{to:'docs/scaling-jaseci-development/intro',activeBasePath:'docs/scaling-jaseci-development',label:'Deployment',position :'left'},
          //{to:'docs/Samples_and_Tutorials/Overview',activeBasePath:'docs/Samples_and_Tutorials',label:'Samples',position :'left'},
          //{to:'docs/Resources/Architectural_Overview',activeBasePath:'docs/Resources',label:'Resources',position :'left'},
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
            title: 'Docs',
            items: [
              {
                label: 'Tutorial',
                to: 'docs/getting-started/getting-to-know-jaseci',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: '/',
              },
              {
                label: 'Discord',
                href: '/',
              },
              {
                label: 'Twitter',
                href: '/',
              },
            ],
          },
          {
            title: 'More',
            items: [
              
              {
                label: 'GitHub',
                href: 'https://github.com/Jaseci-Labs/jaseci',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Jaseci Labs, Inc. Built with Docusaurus.`,
      },
      prism: {
        theme: require('prism-react-renderer/themes/dracula'),
        darkTheme: darkCodeTheme,
        
      },
    }),
};

module.exports = config;
