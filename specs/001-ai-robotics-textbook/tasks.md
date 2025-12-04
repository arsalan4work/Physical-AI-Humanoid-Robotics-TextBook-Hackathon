# Tasks: Physical AI & Humanoid Robotics Textbook Creation

**Input**: Design documents from `/specs/001-ai-robotics-textbook/`
**Prerequisites**: plan.md (required), spec.md (required), Constitution(Required)

**Tests**: The feature specification does not explicitly request test tasks. Therefore, no dedicated test tasks will be generated. Functional verification will be through manual review and Docusaurus build validation.

## Path Conventions

- All content will reside under the `docs/` directory at the repository root.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus structure.

- [ ] T001 Create `docs/` directory at repository root
- [ ] T002 Create `docs/_category_.json` for sidebar configuration
- [ ] T003 Create `docs/intro.md` as the main introduction page
- [ ] T004 Create `docs/chapters/` directory for module chapters
- [ ] T005 Create `docs/assets/` directory for shared assets
- [ ] T006 Create `docs/assets/diagrams/` directory for diagrams
- [ ] T007 Create `docs/assets/code-samples/` directory for code samples
- [ ] T008 Create `docs/modules/` directory for weekly breakdowns and assessments

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

- [ ] T009 [US1] Create `docs/chapters/ros2-fundamentals/` directory
- [ ] T010 [US1] Create `docs/chapters/ros2-fundamentals/_category_.json`
- [ ] T011 [US1] Generate Beginner explanation `docs/chapters/ros2-fundamentals/intro.md`
- [ ] T012 [US1] Generate Intermediate breakdown of core concepts `docs/chapters/ros2-fundamentals/basic-concepts.md`
- [ ] T013 [US1] Generate Expert depth with functional code samples `docs/chapters/ros2-fundamentals/code-examples.md`
- [ ] T014 [US1] Create ROS 2 Python publisher code sample in `docs/assets/code-samples/ros2/publisher.py`
- [ ] T015 [US1] Create ROS 2 Python subscriber code sample in `docs/assets/code-samples/ros2/subscriber.py`
- [ ] T016 [US1] Add exercises and assessments to `docs/chapters/ros2-fundamentals/intro.md` and `docs/chapters/ros2-fundamentals/basic-concepts.md`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Explore Digital Twin Concepts (Priority: P1)

**Goal**: Students can set up and run robot simulations in Gazebo and visualize them in Unity.

**Independent Test**: Student successfully sets up a digital twin, runs a simulation with examples, and observes robot behavior in Gazebo and Unity.

### Implementation for User Story 2

- [ ] T017 [US2] Create `docs/chapters/digital-twin/` directory
- [ ] T018 [US2] Create `docs/chapters/digital-twin/_category_.json`
- [ ] T019 [US2] Generate Beginner explanation `docs/chapters/digital-twin/intro.md`
- [ ] T020 [US2] Generate Intermediate/Expert Gazebo simulation content `docs/chapters/digital-twin/gazebo-simulation.md`
- [ ] T021 [US2] Generate Intermediate/Expert Unity visualization content `docs/chapters/digital-twin/unity-visualization.md`
- [ ] T022 [US2] Create Gazebo robot model (URDF/SDF) in `docs/assets/code-samples/gazebo/simple_robot.urdf`
- [ ] T023 [US2] Create optional Unity C# example in `docs/assets/code-samples/unity/robot_viz.cs`
- [ ] T024 [US2] Add exercises and assessments to `docs/chapters/digital-twin/intro.md` and `docs/chapters/digital-twin/gazebo-simulation.md`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Implement Vision-Language-Action Robotics (Priority: P2)

**Goal**: Advanced students can integrate AI with robotics using VLA concepts and develop VLA pipelines.

**Independent Test**: Advanced student implements a VLA pipeline for a defined task using chapter guidance and adapts provided code examples.

### Implementation for User Story 3

- [ ] T025 [US3] Create `docs/chapters/vla-robotics/` directory
- [ ] T026 [US3] Create `docs/chapters/vla-robotics/_category_.json`
- [ ] T027 [US3] Generate Beginner explanation `docs/chapters/vla-robotics/intro.md`
- [ ] T028 [US3] Generate Intermediate breakdown of VLA systems `docs/chapters/vla-robotics/architecture.md`
- [ ] T029 [US3] Generate Expert depth with functional code samples `docs/chapters/vla-robotics/pipelines-examples.md`
- [ ] T030 [US3] Create Isaac Sim scripts for VLA in `docs/assets/code-samples/isaac-sim/vla_agent.py`
- [ ] T031 [US3] Add exercises and assessments to `docs/chapters/vla-robotics/intro.md` and `docs/chapters/vla-robotics/architecture.md`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Understand Humanoid Kinematics (Priority: P2)

**Goal**: Students can grasp the principles of humanoid robot movement, including forward and inverse kinematics.

**Independent Test**: Student works through the chapter, solves problems, and explains forward and inverse kinematics concepts.

### Implementation for User Story 4

- [ ] T032 [US4] Create `docs/chapters/humanoid-kinematics/` directory
- [ ] T033 [US4] Create `docs/chapters/humanoid-kinematics/_category_.json`
- [ ] T034 [US4] Generate Beginner explanation `docs/chapters/humanoid-kinematics/intro.md`
- [ ] T035 [US4] Generate Intermediate/Expert kinematics content `docs/chapters/humanoid-kinematics/forward-inverse.md`
- [ ] T036 [US4] Create URDF/SDF fragments for humanoid robots in `docs/assets/code-samples/urdf/humanoid_arm.urdf`
- [ ] T037 [US4] Add exercises and assessments to `docs/chapters/humanoid-kinematics/intro.md` and `docs/chapters/humanoid-kinematics/forward-inverse.md`

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
Task: "Generate Beginner explanation docs/chapters/ros2-fundamentals/intro.md"
Task: "Generate Intermediate breakdown of core concepts docs/chapters/ros2-fundamentals/basic-concepts.md"
Task: "Generate Expert depth with functional code samples docs/chapters/ros2-fundamentals/code-examples.md"

# Example of parallel tasks for code sample creation:
Task: "Create ROS 2 Python publisher code sample in docs/assets/code-samples/ros2/publisher.py"
Task: "Create ROS 2 Python subscriber code sample in docs/assets/code-samples/ros2/subscriber.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 3: User Story 1
3. **STOP and VALIDATE**: Review `docs/chapters/ros2-fundamentals/` content and verify code samples.
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
