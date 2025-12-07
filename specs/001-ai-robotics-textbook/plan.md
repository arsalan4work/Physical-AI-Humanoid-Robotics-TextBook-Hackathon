# Implementation Plan: Module-Based Textbook Structure

## 1. Scope and Dependencies

### In Scope:
- Restructure all existing and future textbook content into a `docs/module-XX-name/chapter-XX-name.md` hierarchy.
- Update all internal paths, links, and references within `.md` files, `_category_.json` files (renamed to `category.json`), and `sidebars.ts`.
- Create new directory structures and `category.json` files for all modules (01-04).
- For `module-04-humanoid-kinematics/` (Phase 6), only create the directory and `category.json` file; no content generation for chapter `.md` files.

### Out of Scope:
- Generating content for chapter `.md` files within `module-04-humanoid-kinematics/`.
- Modifying `docusaurus.config.ts` at this stage (will be handled in Phase 7: Polish & Cross-Cutting Concerns).
- Implementing or generating any new content beyond the structural changes.

### External Dependencies:
- Existing `spec.md` for feature requirements.
- Updated `tasks.md` for detailed task breakdown and status.
- Docusaurus framework for path and frontmatter conventions.

## 2. Key Decisions and Rationale

### Decision: Adopt Module-Chapter Hierarchy
- **Options Considered**:
    - Current `docs/chapters/topic/` structure.
    - Flat `docs/topic-chapter.md` structure.
    - Proposed `docs/module-XX-name/chapter-XX-name.md` structure.
- **Trade-offs**:
    - Current structure: Less organized for a multi-module textbook.
    - Flat structure: Difficult to manage large numbers of chapters, less intuitive navigation.
    - Proposed structure: Clearer organization, improved scalability for new modules, better aligns with Docusaurus best practices for large documentation sites, enhances user navigation and content discoverability.
- **Rationale**: The proposed module-chapter structure significantly improves the textbook's organization, scalability, and maintainability, aligning with pedagogical and Docusaurus requirements for a comprehensive resource.

### Decision: Phased Implementation with Structure-Only for Phase 6
- **Rationale**: To adhere to the explicit user instruction to "DO NOT implement or generate any Phase 6 content until explicitly instructed," this approach ensures compliance while preparing the necessary structural foundation for future content generation.

## 3. Interfaces and API Contracts

(Not applicable for this planning phase as it focuses on internal content structure and file organization, not external APIs or data contracts.)

## 4. Non-Functional Requirements (NFRs) and Budgets

### Performance:
- **Goal**: Maintain efficient Docusaurus build times.
- **Strategy**: The restructuring itself should not significantly impact build times. Large content files will be handled by Docusaurus's inherent optimization.

### Reliability:
- **Goal**: Ensure all Docusaurus links and references remain valid after restructuring.
- **Strategy**: Meticulous updates to internal links and `category.json` files will be performed. Docusaurus's build process will serve as a validation step for broken links.

### Security:
- **Goal**: No security implications from file restructuring.
- **Strategy**: The changes are purely structural and content-organization related, with no impact on security.

### Cost:
- **Goal**: Minimal cost impact.
- **Strategy**: The work is primarily organizational, leveraging existing Docusaurus features.

## 5. Data Management and Migration

### Source of Truth:
- The `specs/001-ai-robotics-textbook/tasks.md` file will serve as the source of truth for the new file paths and task statuses.
- Existing `.md` content files will be migrated to their new locations.

### Schema Evolution:
- The Docusaurus file structure is evolving from a `chapters/` subdirectory to a `module-XX-name/chapter-XX-name.md` format within the `docs/` root.
- `_category_.json` files will be updated to `category.json` and moved into their respective module directories.

### Migration and Rollback:
- **Migration**: Content will be moved using `git mv` (conceptually, actual will be file write/delete and new file write) to preserve history where possible, or rewritten with `Write` tool if file moves are complex.
- **Rollback**: Standard Git version control will allow for easy rollback to previous states if issues arise during restructuring.

## 6. Operational Readiness

### Observability:
- **Logs**: Standard CLI output from `Bash` and `Write` tool will provide operational logs.
- **Metrics**: Not applicable for this phase.
- **Traces**: Not applicable for this phase.

### Alerting:
- **Thresholds**: Docusaurus build errors or broken links detected during validation will serve as alerts.
- **On-call owners**: The user (Lead Architect) and Claude Code.

### Runbooks for common tasks:
- This plan acts as a runbook for the restructuring process.

### Deployment and Rollback strategies:
- **Deployment**: The restructured files will be committed and pushed to the GitHub repository, then deployed via GitHub Pages (handled by Docusaurus).
- **Rollback**: Git revert functionality.

### Feature Flags and compatibility:
- Not applicable for this structural change.

## 7. Risk Analysis and Mitigation

### Top 3 Risks:

1.  **Broken Internal Links**: Restructuring a large number of files carries a risk of breaking internal links within Docusaurus.
    -   **Mitigation**: Meticulous updating of all internal `.md` file references and `sidebars.ts`. Docusaurus's `docusaurus build` command will be used to detect and report broken links.
2.  **Incorrect `category.json` Configuration**: Errors in `category.json` files could lead to incorrect sidebar navigation or content display.
    -   **Mitigation**: Careful construction of `category.json` files according to Docusaurus documentation and thorough visual inspection of the generated sidebar after a local build.
3.  **Inadvertent Content Generation for Phase 6**: The instruction to only create structure for Phase 6 could be misinterpreted.
    -   **Mitigation**: Explicit placeholder tasks in `tasks.md` and careful review of generated files to ensure no actual content is written for Phase 6 chapters.

## 8. Evaluation and Validation

### Definition of Done (tests, scans):
- All `.md` files are in their new `docs/module-XX-name/chapter-XX-name.md` locations.
- All `_category_.json` files are renamed to `category.json` and correctly placed.
- `sidebars.ts` is updated to reflect the new module-chapter hierarchy.
- A local Docusaurus build (`npm run build`) completes without errors or broken links.
- The Docusaurus sidebar correctly displays the new module-chapter structure.
- No content has been generated for Phase 6 chapters.

### Output Validation for format/requirements/safety:
- Markdown files adhere to Docusaurus frontmatter requirements.
- File paths and naming conventions match the specified `module-XX-name/chapter-XX-name.md` format.

## 9. Architectural Decision Record (ADR)

📋 Architectural decision detected: Module-Based Textbook Structure Adoption
   Document reasoning and tradeoffs? Run `/sp.adr Module-Based-Textbook-Structure`
