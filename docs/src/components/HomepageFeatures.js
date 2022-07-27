import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: '60% less effort',
    Svg: require('../../static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Developing AI models with Jaseci is way faster. Its requires 60% less effort when building with Jaseci.
      </>
    ),
  },
  {
    title: 'Programming Language',
    Svg: require('../../static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Jaseci uses the <a>Jac</a> Programming language which is used for interacting with the Jaseci Engine, giving developers control over Jaseci when building AI powered Apps.
      </>
    ),
  },
  {
    title: 'Three Creations',
    Svg: require('../../static/img/undraw_docusaurus_react.svg').default,
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
