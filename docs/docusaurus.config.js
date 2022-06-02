// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');


module.exports = {
  title: 'Jaseci Official Documentation',
  tagline: 'Powering The Next Generation Of AI Products',
  url: 'https://your-docusaurus-test-site.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',
  favicon: 'img/favicon.png',
  organizationName: 'Jaseci Labs', // Usually your GitHub org/user name.
  projectName: 'jaseci-docs', // Usually your repo name.

  themeConfig:
   
    {
      navbar: {
        title: '',
        logo: {
          alt: 'Jaseci Logo',
          src: 'img/jaseci_logo.png',
        },
        items: [
          {
            to: 'docs/getting-started/getting-to-know-jaseci',
            position: 'left',
            label: 'Introduction',
            activeBasePath:'docs/getting-started'
          },
          {to:'docs/Developing_with_JAC/Overview',activeBasePath:'docs/Developing_with_JAC',label:'Development',position :'left'},
          {to:'docs/Tools_and_Features/Overview',activeBasePath:'docs/Tools_and_Features',label:'Tools and Features',position :'left'},
          {to:'docs/scaling-jaseci-development/intro',activeBasePath:'docs/scaling-jaseci-development',label:'Deployment',position :'left'},
          {to:'docs/Samples_and_Tutorials/Overview',activeBasePath:'docs/Samples_and_Tutorials',label:'Samples',position :'left'},
          {to:'docs/Resources/Architectural_Overview',activeBasePath:'docs/Resources',label:'Resources',position :'left'},


           //{to: '/blog', label: 'Blog', position: 'left'},
           //{to: '/gettingStarted', label: 'Getting Started', position: 'left'},
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
            title: 'Tutorial',
            items: [
              {
                label: 'Docs',
                to: '/docs/getting-started/getting-to-know-jaseci',
              },
            ],
          },
          {
            title: 'Forum',
            items: [
              {
                label: 'Github Discussions',
                href: 'https://github.com/Jaseci-Labs/jaseci/discussions',
              },

            ],
          },
          {
            title: 'Open source',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Jaseci-Labs/jaseci',
              },
            ],
          },
          {
            title: 'Official website',
            items: [
              {
                label: 'Jaseci.org',
                href: 'https://www.jaseci.org/',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Jaseci Labs, Inc. Built with Docusaurus.`,
      },
      prism: {
        theme: require('prism-react-renderer/themes/dracula'),
        darkTheme: darkCodeTheme,
        additionalLanguages: ['jac', 'python']
      },
    },
    presets: [
      [
        
        '@docusaurus/preset-classic',
      
        {
          docs: {
            path: 'docs',
            routeBasePath: 'docs',
            sidebarPath: require.resolve('./sidebars.js'),
            // Please change this to your repo.
            editUrl: 'https://github.com/facebook/docusaurus/edit/main/website/',
          },
         
          
          theme: {
            customCss: require.resolve('./src/css/custom.css'),
          },
        },
      ]
    ],
    
};

