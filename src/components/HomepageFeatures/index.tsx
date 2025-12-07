import type {ReactNode} from 'react';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  description: ReactNode;
  icon: string;
  iconType: 'svg' | 'png';
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Robotic Nervous System (ROS 2)',
    description: 'Build the robot brain using ROS 2 — topics, services, actions, URDF, TF, Nav2, real-time control.',
    icon: 'robot-brain',
    iconType: 'svg',
  },
  {
    title: 'Digital Twin & Simulation',
    description: 'Create accurate digital twins using Gazebo, Unity, Isaac Sim.',
    icon: 'hologram',
    iconType: 'png',
  },
  {
    title: 'AI Planning, Perception & Control',
    description: 'Use NVIDIA Isaac, Isaac ROS, SLAM, perception models, VLA workflows.',
    icon: 'ai-chip',
    iconType: 'png',
  },
  {
    title: 'Humanoid Locomotion & Manipulation',
    description: 'Learn kinematics, gait, balance, control loops, manipulation.',
    icon: 'humanoid',
    iconType: 'svg',
  },
];

function Feature({title, description, icon, iconType}: FeatureItem) {
  // Create simple SVG icons for the features
  const renderIcon = () => {
    switch(icon) {
      case 'robot-brain':
        return (
          <svg
            className={styles.featureIcon}
            viewBox="0 0 100 100"
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* Robot brain/neuron icon */}
            <circle cx="50" cy="50" r="35" fill="none" stroke="#7a3cff" strokeWidth="3" className={styles.neonStroke} />
            <circle cx="35" cy="40" r="8" fill="#7a3cff" className={styles.neonGlow} />
            <circle cx="65" cy="40" r="8" fill="#7a3cff" className={styles.neonGlow} />
            <circle cx="50" cy="65" r="8" fill="#7a3cff" className={styles.neonGlow} />
            <path d="M35 40 L50 50 L65 40" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <path d="M50 65 L50 50" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
          </svg>
        );
      case 'hologram':
        return (
          <svg
            className={styles.featureIcon}
            viewBox="0 0 100 100"
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* Hologram/3D mesh icon */}
            <path d="M20 70 L50 20 L80 70 Z" fill="none" stroke="#7a3cff" strokeWidth="3" className={styles.neonStroke} />
            <path d="M20 70 L50 50 L80 70" fill="none" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <path d="M50 20 L50 50" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
          </svg>
        );
      case 'ai-chip':
        return (
          <svg
            className={styles.featureIcon}
            viewBox="0 0 100 100"
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* AI chip/GPU icon */}
            <rect x="20" y="20" width="60" height="60" rx="5" fill="none" stroke="#7a3cff" strokeWidth="3" className={styles.neonStroke} />
            <rect x="30" y="30" width="40" height="40" rx="2" fill="none" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <line x1="25" y1="25" x2="35" y2="25" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <line x1="25" y1="35" x2="35" y2="35" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <line x1="65" y1="25" x2="75" y2="25" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <line x1="65" y1="35" x2="75" y2="35" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <line x1="25" y1="65" x2="35" y2="65" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <line x1="25" y1="75" x2="35" y2="75" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <line x1="65" y1="65" x2="75" y2="65" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <line x1="65" y1="75" x2="75" y2="75" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
          </svg>
        );
      case 'humanoid':
        return (
          <svg
            className={styles.featureIcon}
            viewBox="0 0 100 100"
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* Humanoid silhouette icon */}
            <circle cx="50" cy="30" r="12" fill="none" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <line x1="50" y1="42" x2="50" y2="70" stroke="#7a3cff" strokeWidth="3" className={styles.neonStroke} />
            <line x1="35" y1="55" x2="65" y2="55" stroke="#7a3cff" strokeWidth="3" className={styles.neonStroke} />
            <line x1="35" y1="70" x2="25" y2="85" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
            <line x1="65" y1="70" x2="75" y2="85" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
          </svg>
        );
      default:
        return (
          <svg
            className={styles.featureIcon}
            viewBox="0 0 100 100"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="50" cy="50" r="30" fill="none" stroke="#7a3cff" strokeWidth="3" className={styles.neonStroke} />
          </svg>
        );
    }
  };

  return (
    <div className={styles.featureCard}>
      <div className={styles.featureIconContainer}>
        {renderIcon()}
      </div>
      <h3 className={styles.featureTitle}>{title}</h3>
      <p className={styles.featureDescription}>{description}</p>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.featuresSection}>
      <div className={styles.container}>
        <div className={styles.featuresGrid}>
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
