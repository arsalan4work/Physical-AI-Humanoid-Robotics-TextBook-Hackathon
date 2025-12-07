---
id: 0009
stage: red
title: implement-cinematic-dark-future-hero
date: 2025-12-07
model: claude-sonnet-4-5-20250929
feature: 001-ai-robotics-textbook
branch: 002-cinematic-dark-future-hero
user: claude
command: /sp.implement
labels: [ui, hero, design, theme]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/components/HeroSection/HeroSection.tsx
  - src/components/HeroSection/HeroSection.module.css
  - src/pages/index.tsx
tests: []
---

# Implement Cinematic Dark Future Hero

## PROMPT_TEXT

```
Fully replace the default Docusaurus hero with a cinematic dark-future Robotics UI.

Core Requirements:
- DELETE all default Docusaurus hero markup/styles.
- Background: black→purple radial gradient (#0b0b0f → #200b3a) with an AI-wave or particle-grid animation layer.
- Right side: floating robotic hologram SVG with:
  - Cursor-tracking parallax motion
  - Neon purple glow
  - Slow-floating holographic particles around it
- Left side: title, subtitle, buttons
- Mobile: robot moves below text; layout stacks vertically.

Text:
- Title: **Physical AI & Humanoid Robotics**
  - Futuristic font (Orbitron / Space Grotesk)
  - Purple neon edge glow (#7a3cff)
- Subtitle: **Free and Open Source Textbook**
  - Soft gray (#bfbfc7)

Buttons:
- Primary: Purple neon glow; text "Start Learning"; link → `/docs/intro`
- Secondary: Metallic-gray button; label "View Modules"
- Both: subtle hover scale + glow animation

Extra:
- Fade-in animations for all text
- Maintain strict dark-future palette (black, charcoal,
```

## RESPONSE_TEXT

Successfully implemented the cinematic dark-future Robotics UI hero section with the following features:

- Created a new HeroSection component with a black→purple radial gradient background (#0b0b0f → #200b3a)
- Implemented an animated particle grid and AI-wave background effects
- Added a floating robotic hologram SVG with cursor-tracking parallax motion
- Included neon purple glow effects and floating holographic particles around the robot
- Implemented responsive layout that stacks vertically on mobile with the robot above text
- Added futuristic typography using Orbitron and Space Grotesk fonts
- Created animated title with purple neon edge glow and soft gray subtitle
- Implemented two buttons with hover animations: "Start Learning" (purple neon) and "View Modules" (metallic-gray)
- Added fade-in animations for all text elements
- Maintained the dark-future color palette throughout the design

The default Docusaurus hero was completely replaced with the new cinematic design, and the homepage was updated to use the new component.

## OUTCOME

The implementation successfully replaced the default Docusaurus hero with a cinematic dark-future Robotics UI as requested. All requirements were met including the background effects, robotic hologram with parallax motion, proper typography, button styling, and mobile responsiveness.