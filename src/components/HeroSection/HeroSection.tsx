import React, { useState, useEffect, useRef } from 'react';
import styles from './HeroSection.module.css';

const HeroSection = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const robotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  useEffect(() => {
    if (robotRef.current) {
      const rect = robotRef.current.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      const deltaX = (mousePosition.x - centerX) / 50;
      const deltaY = (mousePosition.y - centerY) / 50;

      robotRef.current.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
    }
  }, [mousePosition]);

  return (
    <section className={styles.heroSection}>
      <div className={styles.background}>
        <div className={styles.radialGradient}></div>
        <div className={styles.particleGrid}>
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className={styles.particle}
              style={{
                top: `${Math.random() * 100}%`,
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
              }}
            ></div>
          ))}
        </div>
        <div className={styles.aiWave}></div>
      </div>

      <div className={styles.contentContainer}>
        <div className={styles.textContent}>
          <h1 className={styles.title}>
            Physical AI & Humanoid Robotics
          </h1>
          <p className={styles.subtitle}>
            Free and Open Source Textbook
          </p>
          <div className={styles.buttonGroup}>
            <a href="/docs/intro" className={styles.primaryButton}>
              Start Learning
            </a>
            <a href="/docs/intro" className={styles.secondaryButton}>
              View Modules
            </a>
          </div>
        </div>

        <div className={styles.robotContainer} ref={robotRef}>
          <div className={styles.robotHologram}>
            <svg
              className={styles.robotSvg}
              viewBox="0 0 200 200"
              xmlns="http://www.w3.org/2000/svg"
            >
              {/* Robot body */}
              <rect x="80" y="70" width="40" height="60" rx="5" fill="none" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />

              {/* Robot head */}
              <circle cx="100" cy="50" r="15" fill="none" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />

              {/* Robot arms */}
              <line x1="70" y1="80" x2="80" y2="80" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
              <line x1="130" y1="80" x2="140" y2="80" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />

              {/* Robot legs */}
              <line x1="90" y1="130" x2="90" y2="150" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />
              <line x1="110" y1="130" x2="110" y2="150" stroke="#7a3cff" strokeWidth="2" className={styles.neonStroke} />

              {/* Robot eye */}
              <circle cx="100" cy="48" r="3" fill="#7a3cff" className={styles.neonGlow} />
            </svg>
          </div>

          {/* Holographic particles around robot */}
          {[...Array(8)].map((_, i) => (
            <div
              key={i}
              className={styles.holographicParticle}
              style={{
                top: `${20 + Math.random() * 60}%`,
                left: `${20 + Math.random() * 60}%`,
                animationDelay: `${i * 0.5}s`,
              }}
            ></div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HeroSection;