---
id: "0008"
title: "Restructure tasks.md to Module Hierarchy"
stage: "plan"
date: "2025-12-06"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "001-ai-robotics-textbook"
branch: "001-ai-robotics-textbook"
user: "user"
command: "/sp.plan Module-Based Structure ..."
labels: ["restructure", "tasks", "docusaurus", "plan"]
links:
  spec: "specs/001-ai-robotics-textbook/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - specs/001-ai-robotics-textbook/tasks.md
tests_yaml:
  - null
---
## Prompt
```text
Module-Based Structure

Restructure the entire textbook into a clean **Module → Chapter** hierarchy.
**Do NOT implement or generate any Phase 6 content until explicitly instructed.**

## New Required Folder Structure
All content must follow:

docs/
module-01-ros2-fundamentals/
chapter-01-intro.md
chapter-02-basic-concepts.md
chapter-03-code-examples.md
category.json

module-02-digital-twin/
chapter-01-intro.md
chapter-02-gazebo-simulation.md
chapter-03-unity-visualization.md
category.json

module-03-vla-robotics/
chapter-01-intro.md
chapter-02-architecture.md
chapter-03-pipelines-examples.md
category.json

module-04-humanoid-kinematics/
chapter-01-intro.md
chapter-02-forward-inverse.md
category.json

assets/
diagrams/
code-samples/

## Instructions
- Convert ALL existing tasks into this module-based Docusaurus structure.
- Update all paths, links, and references.
- Ignore and **do NOT generate Phase 6** (Humanoid Kinematics) until i told.
- Only create the folders and structure for Phase 6 (no content).
-
```

## Response
```
The `tasks.md` file has been successfully updated with the new module-based structure and paths. Completed tasks for Phases 1 and 5 have been marked, and placeholder tasks for Phase 6 have been added to reflect the structure-only requirement.
```