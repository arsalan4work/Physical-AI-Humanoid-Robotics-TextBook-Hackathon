# Tasks: Physical AI & Humanoid Robotics Textbook Creation

**Input**: Design documents from `/specs/001-ai-robotics-textbook/`
**Prerequisites**: plan.md (required), spec.md (required), Constitution(Required)

**Tests**: The feature specification does not explicitly request test tasks. Therefore, no dedicated test tasks will be generated. Functional verification will be through manual review and Docusaurus build validation.

## Path Conventions

- All content will reside under the `docs/` directory at the repository root.
- Chapters will now follow a `module-XX-name/chapter-XX-name.md` structure.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus structure.

- [x] T001 Create `docs/` directory at repository root
- [x] T002 Create `docs/_category_.json` for sidebar configuration
- [x] T003 Create `docs/intro.md` as the main introduction page
- [x] T004 Create `docs/chapters/` directory for module chapters
- [x] T005 Create `docs/assets/` directory for shared assets
- [x] T006 Create `docs/assets/diagrams/` directory for diagrams
- [x] T007 Create `docs/assets/code-samples/` directory for code samples
- [x] T008 Create `docs/modules/` directory for weekly breakdowns and assessments (This task remains as is, as `docs/modules/` is for breakdowns and assessments, not chapters)

---

## Phase 2: Foundational (No explicit Foundational tasks beyond Setup)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Learn ROS 2 Fundamentals (Priority: P1) 🎯 MVP

**Goal**: Students can understand the basics of ROS 2, explain core concepts, run basic commands, and implement simple publishers and subscribers.

**Independent Test**: Student successfully completes the ROS 2 fundamentals chapter, runs provided code, and passes embedded exercises.

### Implementation for User Story 1

- [x] T009 [US1] Create `docs/module-01-ros2-fundamentals/` directory
- [x] T010 [US1] Create `docs/module-01-ros2-fundamentals/category.json`
- [x] T011 [US1] Generate Beginner explanation `docs/module-01-ros2-fundamentals/chapter-01-intro.md`
- [x] T012 [US1] Generate Intermediate breakdown of core concepts `docs/module-01-ros2-fundamentals/chapter-02-basic-concepts.md`
- [x] T013 [US1] Generate Expert depth with functional code samples `docs/module-01-ros2-fundamentals/chapter-03-code-examples.md`
- [x] T014 [US1] Create ROS 2 Python publisher code sample in `docs/assets/code-samples/ros2/publisher.py`
- [x] T015 [US1] Create ROS 2 Python subscriber code sample in `docs/assets/code-samples/ros2/subscriber.py`
- [x] T016 [US1] Add exercises and assessments to `docs/modules/Module 01 ROS2-Fundamentals/chapter-01-intro.md` and `docs/modules/Module 01 ROS2-Fundamentals/chapter-02-basic-concepts.md`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Explore Digital Twin Concepts (Priority: P1)

**Goal**: Students can set up and run robot simulations in Gazebo and visualize them in Unity.

**Independent Test**: Student successfully sets up a digital twin, runs a simulation with examples, and observes robot behavior in Gazebo and Unity.

### Implementation for User Story 2

- [x] T017 [US2] Create `docs/module-02-digital-twin/` directory
- [x] T018 [US2] Create `docs/module-02-digital-twin/category.json`
- [x] T019 [US2] Generate Beginner explanation `docs/module-02-digital-twin/chapter-01-intro.md`
- [x] T020 [US2] Generate Intermediate/Expert Gazebo simulation content `docs/module-02-digital-twin/chapter-02-gazebo-simulation.md`
- [x] T021 [US2] Generate Intermediate/Expert Unity visualization content `docs/module-02-digital-twin/chapter-03-unity-visualization.md`
- [x] T022 [US2] Create Gazebo robot model (URDF/SDF) in `docs/assets/code-samples/gazebo/simple_robot.urdf`
- [x] T023 [US2] Create optional Unity C# example in `docs/assets/code-samples/unity/robot_viz.cs`
- [x] T024 [US2] Add exercises and assessments to `docs/modules/Module 02 Digital-Twin/chapter-01-intro.md` and `docs/modules/Module 02 Digital-Twin/chapter-02-gazebo-simulation.md`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Implement Vision-Language-Action Robotics (Priority: P2)

**Goal**: Advanced students can integrate AI with robotics using VLA concepts and develop VLA pipelines.

**Independent Test**: Advanced student implements a VLA pipeline for a defined task using chapter guidance and adapts provided code examples.

### Implementation for User Story 3

- [x] T025 [US3] Create `docs/module-03-vla-robotics/` directory
- [x] T026 [US3] Create `docs/module-03-vla-robotics/category.json`
- [x] T027 [US3] Generate Beginner explanation `docs/module-03-vla-robotics/chapter-01-intro.md`
- [x] T028 [US3] Generate Intermediate breakdown of VLA systems `docs/module-03-vla-robotics/chapter-02-architecture.md`
- [x] T029 [US3] Generate Expert depth with functional code samples `docs/module-03-vla-robotics/chapter-03-pipelines-examples.md`
- [x] T030 [US3] Create Isaac Sim scripts for VLA in `docs/assets/code-samples/isaac-sim/vla_agent.py`
- [x] T031 [US3] Add exercises and assessments to `docs/module-03-vla-robotics/chapter-01-intro.md` and `docs/module-03-vla-robotics/chapter-02-architecture.md`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Understand Humanoid Kinematics (Priority: P2)

**Goal**: Students can grasp the principles of humanoid robot movement, including forward and inverse kinematics.

**Independent Test**: Student works through the chapter, solves problems, and explains forward and inverse kinematics concepts.

### Implementation for User Story 4 (Structure Only - No Content Generation)

- [x] T032 [US4] Create `docs/module-04-humanoid-kinematics/` directory
- [x] T033 [US4] Create `docs/module-04-humanoid-kinematics/category.json`
- [x] T034 [US4] Generate `docs/module-04-humanoid-kinematics/chapter-01-intro.md`
- [x] T035 [US4] Generate `docs/module-04-humanoid-kinematics/chapter-02-forward-inverse.md`
- [x] T038 [US4] Generate `docs/module-04-humanoid-kinematics/chapter-03-gait-balance.md`
- [x] T039 [US4] Generate `docs/module-04-humanoid-kinematics/chapter-04-manipulation-control.md`
- [x] T040 [US4] Generate `docs/module-04-humanoid-kinematics/chapter-05-advanced-applications.md`
- [x] T036 [US4] Create URDF model in `docs/assets/code-samples/urdf/humanoid_arm.urdf`
- [x] T037 [US4] Add exercises and assessments to `docs/modules/Module 04 Humanoid-Kinematics/chapter-01-intro.md` and `docs/modules/Module 04 Humanoid-Kinematics/chapter-02-forward-inverse.md`

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories or the overall textbook quality.

- [ ] T038 Review all chapters for consistency in tone, formatting, and depth
- [ ] T039 Ensure all diagrams are present and correctly formatted (Mermaid/ASCII) in `docs/assets/diagrams/`
- [ ] T040 Verify all code samples are functional and correctly referenced from `docs/assets/code-samples/`
- [ ] T041 Add global navigation and table of contents configuration to `docusaurus.config.js`
- [ ] T042 Final review of all exercises and assessment questions in `docs/modules/`
- [ ] T043 Validate Docusaurus build process locally

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: No specific foundational tasks beyond Setup.
- **User Stories (Phase 3-6)**: All depend on Setup phase completion.
  - User stories can then proceed in parallel (if staffed) or sequentially in priority order (P1 → P2 → P3).
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories. Can start after Setup.
- **User Story 2 (P1)**: No dependencies on other stories. Can start after Setup. (Can run in parallel with US1)
- **User Story 3 (P2)**: No dependencies on other stories. Can start after Setup.
- **User Story 4 (P2)**: No dependencies on other stories. Can start after Setup.

### Within Each User Story

- Content generation (intro, basic-concepts, code-examples) before adding exercises.
- Code samples should be created before being referenced in chapters.

### Parallel Opportunities

- All Setup tasks (T001-T008) can run in parallel.
- User Stories 1 and 2 (P1) can be worked on in parallel.
- User Stories 3 and 4 (P2) can be worked on in parallel.
- Within each user story, tasks involving creating directories, markdown files, and code samples can often be parallelized (e.g., T011, T012, T013 can be initiated concurrently).

---

## Parallel Example: User Story 1

```bash
# Example of parallel tasks for initial content creation in US1:
Task: "Generate Beginner explanation docs/module-01-ros2-fundamentals/chapter-01-intro.md"
Task: "Generate Intermediate breakdown of core concepts docs/module-01-ros2-fundamentals/chapter-02-basic-concepts.md"
Task: "Generate Expert depth with functional code samples docs/module-01-ros2-fundamentals/chapter-03-code-examples.md"

# Example of parallel tasks for code sample creation:
Task: "Create ROS 2 Python publisher code sample in docs/assets/code-samples/ros2/publisher.py"
Task: "Create ROS 2 Python subscriber code sample in docs/assets/code-samples/ros2/subscriber.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 3: User Story 1
3. **STOP and VALIDATE**: Review `docs/module-01-ros2-fundamentals/` content and verify code samples.
4. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup → Foundation ready
2. Add User Story 1 → Review content → Deploy/Demo (MVP!)
3. Add User Story 2 → Review content → Deploy/Demo
4. Add User Story 3 → Review content → Deploy/Demo
5. Add User Story 4 → Review content → Deploy/Demo
6. Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup together.
2. Once Setup is done:
   - Developer A: User Story 1 (ROS 2 Fundamentals)
   - Developer B: User Story 2 (Digital Twin Concepts)
   - Developer C: User Story 3 (VLA Robotics)
   - Developer D: User Story 4 (Humanoid Kinematics)
3. Stories complete and integrate independently.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to specific user story for traceability.
- Each user story should be independently completable and testable.
- Commit after each task or logical group.
- Stop at any checkpoint to validate story independently.
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.
