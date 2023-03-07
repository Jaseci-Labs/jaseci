import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import useBaseUrl from '@docusaurus/useBaseUrl';



const FeatureList = [
 {
    title: 'Introduction to Jaseci',
    imgUrl: 'img/tutorial/landingpage/introduction_to_jaseci.png',
    href : '/docs/getting-started/getting-to-know-jaseci',
    description: (
      <>
        Developing AI models with Jaseci is way faster. Its requires 60% less effort when building with Jaseci. Get started  <a href="/docs/getting-started/getting-to-know-jaseci">Here</a>
      </>
    ),
  },
  {
    title: 'Developing with Jaseci',
    imgUrl : 'img/tutorial/landingpage/developing_with_jaseci.png',
    href : '/docs/Developing_with_JAC/Overview',

    description: (
      <>
        Jaseci uses the <a>JAC</a> Programming language which is used for interacting with the Jaseci Engine, giving developers control over Jaseci when building AI powered Apps. Get started  <a href="/docs/Developing_with_JAC/Overview">Here</a>
      </>
    ),
  },
  {
    title: 'Tools and Features',
    imgUrl: 'img/tutorial/landingpage/tools_and_features.png',
    href : '/docs/Tools_and_Features/Overview',

    description: (
      <>
        Jaseci comes with powerful tools to speed up and empower your development. Jaseci Kit , Jaseci Studio, VS code plugins are all avaliable for you !
      </>
    ),
  }
];

function Feature({imgUrl,href, title, description}) {

  const imageUrl = useBaseUrl(imgUrl);
  return (
      <div className={clsx('col col--4', styles.feature)}>
          {imageUrl && (
              <div className="text--center">
                  <a href= {href} ><img className={styles.featureSvg} src={imageUrl} alt={title}/></a>
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


  /*
  ,
  {
    title: 'Scaling Jaseci Deployment ',
    imgUrl: 'img/tutorial/landingpage/jaseci_deployment.png',
    href : '/docs/scaling-jaseci-development/intro',

    description: (
      <>
        Jaseci provides out-of-box production-grade containerization and orchestration so you can stand up a production-ready stack in minutes. With novel load balancing and facilitation techniques, your production Jaseci cluster scales intelligently with your application’s demand.
      </>
    ),
  },
  {
    title: 'Samples and Tutorials',
    imgUrl: 'img/tutorial/landingpage/tutorials.png',
    href : '/docs/Samples_and_Tutorials/Overview',

    description: (
      <>
        Don't know where or what to start building ? Well checkout some of starter projects to guide you on your adventures.
      </>
    ),
  },
  {
    title: 'Resources',
    imgUrl: 'img/tutorial/landingpage/resources.png',
    href : '/docs/Resources/Architectural_Overview',

    description: (
      <>
        Powering the next generation of AI products. Jaseci powers apps
        like <a href="https://myca.ai">myca.ai</a>, <a href="http://zeroshotbot.com/">zeroshotbot.com</a> and <a href="http://trueselph.com/">trueselph.com</a>.
        Build your next generation AI product today!
      </>
    ),
  },
  */