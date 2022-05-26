import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Introduction to Jaseci',
    Svg: require('../../static/img/tutorial/landingpage/introduction to jaseci.svg').default,
    href: '/docs/getting-started/getting-to-know-jaseci',
    description: (
      <>
        Developing AI models with Jaseci is way faster. Its requires 60% less effort when building with Jaseci. Get started  <a href="/docs/getting-started/getting-to-know-jaseci">Here</a>
      </>
    ),
  },
  {
    title: 'Developing with Jaseci',
    Svg: require('../../static/img/tutorial/landingpage/developing with jaseci.svg').default,
    description: (
      <>
        Jaseci uses the <a>Jac</a> Programming language which is used for interacting with the Jaseci Engine, giving developers control over Jaseci when building AI powered Apps. Get started  <a href="/docs/Developing_with_JAC/Overview">Here</a>
      </>
    ),
  },
  {
    title: 'Tools and Features',
    Svg: require('../../static/img/tutorial/landingpage/tools and features.svg').default,
    description: (
      <>
        Jaseci comes with powerful tools to speed up and empower your development. Jaseci Kit , Jaseci Studio, VS code plugins are all avaliable for you !
      </>
    ),
  },
  {
    title: 'Scaling Jaseci Deployment ',
    Svg: require('../../static/img/tutorial/landingpage/jaseci deployment.svg').default,
    description: (
      <>
        Jaseci provides out-of-box production-grade containerization and orchestration so you can stand up a production-ready stack in minutes. With novel load balancing and facilitation techniques, your production Jaseci cluster scales intelligently with your application’s demand.
      </>
    ),
  },
  {
    title: 'Samples and Tutorials',
    Svg: require('../../static/img/tutorial/landingpage/tutorials.svg').default,
    description: (
      <>
        Don't know where or what to start building ? Well checkout some of starter projects to guide you on your adventures.
      </>
    ),
  },
  {
    title: 'Resources',
    Svg: require('../../static/img/tutorial/landingpage/resources.svg').default,
    description: (
      <>
        Powering the next generation of AI products. Jaseci powers apps
        like <a href="https://myca.ai">myca.ai</a>, <a href="http://zeroshotbot.com/">zeroshotbot.com</a> and <a href="http://trueselph.com/">trueselph.com</a>.
        Build your next generation AI product today!
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
