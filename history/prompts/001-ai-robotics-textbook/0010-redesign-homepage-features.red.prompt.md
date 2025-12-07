---
id: 0010
stage: red
title: redesign-homepage-features
date: 2025-12-07
model: claude-sonnet-4-5-20250929
feature: 001-ai-robotics-textbook
branch: 003-redesign-homepage-features
user: claude
command: /sp.implement
labels: [ui, features, design, theme]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/components/HomepageFeatures/index.tsx
  - src/components/HomepageFeatures/styles.module.css
tests: []
---

# Redesign Homepage Feature Section

## PROMPT_TEXT

```
Redesign Homepage Feature Section

**Instructions:**

1. **Remove Docusaurus Defaults**
   - Delete default cards and branding.

2. **Create 4-Card Robotics Grid**
   - **Modules:**
     1. Robotic Nervous System (ROS 2) – neuron/robot brain SVG – "Build the robot brain using ROS 2 — topics, services, actions, URDF, TF, Nav2, real-time control."
     2. Digital Twin & Simulation – hologram/3D mesh PNG – "Create accurate digital twins using Gazebo, Unity, Isaac Sim."
     3. AI Planning, Perception & Control – AI-chip/GPU PNG – "Use NVIDIA Isaac, Isaac ROS, SLAM, perception models, VLA workflows."
     4. Humanoid Locomotion & Manipulation – humanoid silhouette SVG – "Learn kinematics, gait, balance, control loops, manipulation."
   - **Design:** Dark-future (#0b0b0f), glass cards, neon purple borders, slight scale + glow on hover, Orbitron/Space Grotesk fonts.
   - **Layout:** 2×2 desktop, 1-column mobile.
   - **Images:** Open-source only.

3. **Files:** `src/components/HomepageFeatures/*
```

## RESPONSE_TEXT

Successfully redesigned the homepage feature section with a 4-card robotics grid as requested:

- Replaced default Docusaurus features with 4 robotics-themed cards
- Created custom SVG icons for each module: robot brain/neuron, hologram/3D mesh, AI chip/GPU, and humanoid silhouette
- Implemented dark-future design with #0b0b0f background
- Created glassmorphism cards with neon purple borders (rgba(122, 60, 255, 0.5))
- Added hover effects with scale and glow animations
- Used Orbitron font for titles and Space Grotesk for descriptions
- Implemented 2×2 grid layout for desktop and 1-column for mobile
- Added CSS animations for neon glow effects on the SVG icons
- Created proper hover states with increased border opacity and glow effect
- Maintained responsive design with appropriate padding and font sizes

The implementation follows all requirements including the dark-future aesthetic, glass card design, and proper module descriptions.

## OUTCOME

The homepage feature section has been successfully redesigned with the requested 4-card robotics grid, featuring the dark-future theme with glass cards, neon borders, and hover animations as specified.