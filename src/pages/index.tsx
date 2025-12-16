import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css'; // Make sure this exists

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();

  // Table of Contents data
  const chapters = [
    {
      icon: '🧠',
      title: 'Chapter 1',
      subtitle: 'Introduction to Physical AI',
      description: 'Learn the fundamentals of AI systems that interact with the physical world.',
      link: '/docs/chapter-1-introduction-to-physical-ai',
    },
    {
      icon: '🤖',
      title: 'Chapter 2',
      subtitle: 'Basics of Humanoid Robotics',
      description: 'Explore mechanical design, actuators, sensors, and control systems.',
      link: '/docs/chapter-2-basics-of-humanoid-robotics',
    },
    {
      icon: '⚙️',
      title: 'Chapter 3',
      subtitle: 'ROS 2 Fundamentals',
      description: 'Master the industry-standard framework for robot software development.',
      link: '/docs/chapter-3-ros-2-fundamentals',
    },
    {
      icon: '🌐',
      title: 'Chapter 4',
      subtitle: 'Digital Twin Simulation',
      description: 'Use Gazebo and Isaac Sim to test robots in virtual environments.',
      link: '/docs/chapter-4-digital-twin-simulation',
    },
    {
      icon: '👁️',
      title: 'Chapter 5',
      subtitle: 'Vision-Language-Action Systems',
      description: 'Build AI models that understand vision, language, and generate actions.',
      link: '/docs/chapter-5-vision-language-action-systems',
    },
    {
      icon: '🎓',
      title: 'Chapter 6',
      subtitle: 'Capstone Project',
      description: 'Integrate all concepts to build a complete AI-robot pipeline.',
      link: '/docs/chapter-6-capstone-ai-robot-pipeline',
    },
  ];

  return (
    <Layout description="Learn to build intelligent physical systems with ROS 2, simulation, and AI models">
      
      {/* Hero Section */}
      <header className={clsx('hero hero--primary', styles.heroBanner)}>
        <div className="container">
          <Heading as="h1" className="hero__title">
            {siteConfig.title}
          </Heading>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link className="button button--secondary button--lg" to="/docs/chapter-1-introduction-to-physical-ai">
              Start Learning →
            </Link>
          </div>
        </div>
      </header>

      {/* Table of Contents */}
      <main>
        <section className={styles.features}>
          <div className="container">
            <h2 style={{textAlign: 'center', marginBottom: '2rem'}}>Table of Contents</h2>
            <div className="row">
              {chapters.map((chapter) => (
                <div key={chapter.title} className="col col--4">
                  <div className="card margin-bottom--lg">
                    <div className="card__header" style={{textAlign: 'center', paddingTop: '1.5rem'}}>
                      <div style={{fontSize: '3rem', marginBottom: '0.5rem'}}>{chapter.icon}</div>
                      <h3>{chapter.title}</h3>
                      <p><strong>{chapter.subtitle}</strong></p>
                    </div>
                    <div className="card__body" style={{padding: '1rem 1.5rem', textAlign: 'center', color: '#444'}}>
                      {chapter.description}
                    </div>
                    <div className="card__footer" style={{padding: '1rem 1.5rem', textAlign: 'center'}}>
                      <Link to={chapter.link} style={{color: '#2e78f0', fontWeight: 'bold', textDecoration: 'none'}}>
                        Read Chapter →
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
