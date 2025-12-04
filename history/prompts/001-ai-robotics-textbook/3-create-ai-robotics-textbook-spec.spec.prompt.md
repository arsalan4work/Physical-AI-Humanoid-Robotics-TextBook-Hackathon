id: 3
title: Create AI Robotics Textbook Spec
stage: spec
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-ai-robotics-textbook
branch: 001-ai-robotics-textbook
user: unknown
command: /sp.specify # Prompt: AI/Spec-Driven Book Creation for Physical AI & Humanoid Robotics...
labels: ["specification", "textbook"]
links:
  spec: E:/Codes/hackatons/hackaton-1/physical-ai-and-humanoid-robotics-text-book/specs/001-ai-robotics-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - E:/Codes/hackatons/hackaton-1/physical-ai-and-humanoid-robotics-text-book/specs/001-ai-robotics-textbook/spec.md
  - E:/Codes/hackatons/hackaton-1/physical-ai-and-humanoid-robotics-text-book/specs/001-ai-robotics-textbook/checklists/requirements.md
tests:

---

## Prompt

# Prompt: AI/Spec-Driven Book Creation for Physical AI & Humanoid Robotics

You are an **AI Textbook Architect** tasked with creating a full, production-ready textbook titled:

**“Physical AI & Humanoid Robotics”**

This textbook will be written using **Spec-Kit Plus** and **Claude Code**, and deployed to **Docusaurus on GitHub Pages**. Your work must follow the rules defined in `/sp.constitution`.

---

## GOALS

1. Generate a complete, **technically accurate**, and **AI-native textbook** covering all course modules:
   - ROS 2 (Robotic Nervous System)
   - Digital Twin (Gazebo & Unity)
   - AI-Robot Brain (NVIDIA Isaac)
   - Vision-Language-Action robotics\n   - Humanoid kinematics, locomotion, and manipulation
   - Conversational robotics with LLMs
   - Hardware & lab architecture
   - Weekly breakdown, projects, and assessments

2. Ensure **Docusaurus compatibility**:
   - Markdown files with frontmatter
   - Proper folder structure (`/docs`, `/chapters`, `/modules`, `/assets`)
   - Diagrams using `mermaid` or ASCII
   - Tables, code blocks, and step-by-step instructions

3. Produce **pedagogically optimized content**:
   - Beginner → Intermediate → Expert explanations
   - Concept maps, diagrams, analogies, and real-world examples
   - Exercises and assessment questions per module

4. Include **functional code samples**:
   - ROS 2 Python scripts (rclpy)
   - URDF/SDF robot descriptions
   - Isaac Sim scripts (Python)
   - Optional Unity C# snippets
   - SLAM, navigation, and VLA pipelines

5. Leverage **MCP server + Context7 integration** to maintain global context across all chapters.

---

## INSTRUCTIONS TO CLAUDE CODE

1. Generate chapters **one at a time**, following the Spec-Kit Plus structure.
2. Ensure each chapter:
   - Uses clear Markdown with Docusaurus frontmatter
   - Includes diagrams, tables, and code blocks where needed
   - Follows the 3-layered depth structure (Beginner → Intermediate → Expert)
3. Maintain **consistency across modules**, including naming conventions, file paths, and formatting.
4. Include references to **official documentation** when describing ROS 2, Gazebo, Isaac Sim, or Unity APIs.
5. Output **ready-to-commit Markdown files** for GitHub Pages deployment.

---

## CAPSTONE EXPECTATION

At the end of this process, Claude Code should generate a **fully structured textbook** that is:

- Complete and technically accurate
- Fully Docusaurus-compatible
- Optimized for AI agent interaction and context retention
- Includes all chapters, exercises, diagrams, and code samples

---

## EXTRA NOTES

- Never invent tools, libraries, or hardware; use only real-world resources.
- Optimize for **clarity, step-by-step learning, and AI-native content structure**.
- Maintain full context via MCP server + Context7 to ensure **coherence across all modules**.

## Response snapshot

Created the feature specification for the "Physical AI & Humanoid Robotics" textbook (001-ai-robotics-textbook/spec.md) and a corresponding quality checklist (001-ai-robotics-textbook/checklists/requirements.md). The specification has passed all quality checks and is ready for the next phase.

## Outcome

- ✅ Impact: Feature specification created and validated.
- 🧪 Tests: Spec quality checklist passed.
- 📁 Files: `spec.md`, `requirements.md` created/updated.
- 🔁 Next prompts: Ready for `/sp.clarify` or `/sp.plan`.
- 🧠 Reflection: Successfully created a comprehensive and validated feature specification based on user input, ensuring alignment with project goals and Docusaurus compatibility. All requirements are clear, measurable, and technology-agnostic. No clarifications were needed as the prompt was sufficiently detailed.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
