import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import useBaseUrl from '@docusaurus/useBaseUrl';



const FeatureList = [
  {
    title: 'Introduction to Jaseci',
    imgUrl: 'img/tutorial/landingpage/introduction_to_jaseci.png',
    href: 'docs/introduction',
    description: (
      <>
        Developing AI models with Jaseci is way faster. Its requires 60% less effort when building with Jaseci. Get started  <a href="/docs/introduction">Here</a>
      </>
    ),
  },
  {
    title: 'Developing with Jaseci',
    imgUrl: 'img/tutorial/landingpage/developing_with_jaseci.png',
    href: '/docs/development',

    description: (
      <>
        Jaseci uses the <a>JAC</a> Programming language which is used for interacting with the Jaseci Engine, giving developers control over Jaseci when building AI powered Apps. Get started  <a href="/docs/Developing_with_JAC/Overview">Here</a>
      </>
    ),
  },
  {
    title: 'Tools and Features',
    imgUrl: 'img/tutorial/landingpage/tools_and_features.png',
    href: '/docs/Tools_and_Features/Overview',

    description: (
      <>
        Jaseci comes with powerful tools to speed up and empower your development. Jaseci Kit , Jaseci Studio, VS code plugins are all avaliable for you !
      </>
    ),
  }
];

function Feature({ imgUrl, href, title, description }) {

  const imageUrl = useBaseUrl(imgUrl);
  return (
    <div className={clsx('col col--4', styles.feature)}>
      {imageUrl && (
        <div className="text--center">
          <a href={href} ><img className={styles.featureSvg} src={imageUrl} alt={title} /></a>
        </div>
      )}
      <h3>{title}</h3>
      <p>{description}</p>
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
