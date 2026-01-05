# Constitution

The Constitution is a set of invariant rules and guidelines that the agent must follow at all times. It takes precedence over all other instructions.

## 1. Git Workflow
- **Branch Strategy**: modifications/experiments MUST be done on a separate branch.
- **Base Branch**: New feature branches (Spec) MUST be created from `main`.
- **Procedure**: `git checkout main` -> `git pull` -> `git checkout -b {number}-{short-description}`.
- **Commit Messages**: Semantic Commit Messages (e.g., `feat:`, `fix:`, `docs:`).

## 2. Operational Modes
The Agent must classify the user's request into one of two modes before proceeding.

### Mode A: Standard SDD (Default)
- **Triggers**: New features, complex refactoring, architectural changes, or when "Direct Mode" becomes too complex.
- **Process**: Must follow the **6-Step SDD Cycle** strictly.
- **Artifacts**: Full `specs/` directory structure required.

### Mode B: Direct Request ("Fast Track")
- **Triggers**: Simple Q&A, minor bug fixes (1-2 files), documentation updates, one-off scripts.
- **Process**:
  1. **Execute**: Implement changes directly.
  2. **Verify**: Run tests to ensure no regressions.
  3. **Escalate**: If changes affect >3 files or require architectural decisions, switch to **Mode A**.
- **Artifacts**: Minimal or no `specs/` generation.

## 3. SDD Workflow (Mode A)
The Agent MUST follow the 6-step cycle for every feature in **Mode A**. Do NOT skip steps.

### Step 1: Specify (`speckit.specify`)
- **Goal**: Define WHAT to build.
- **Output**: `specs/{branch}/spec.md`
- **Content**: Summary, Requirements, User Stories.

### Step 2: Clarify (`speckit.clarify`)
- **Goal**: Clear up ambiguities.
- **Output**: `specs/{branch}/clarify.md` (or `research.md`)
- **Content**: Q&A, Edge cases, Constraints.

### Step 3: Plan (`speckit.plan`)
- **Goal**: Design HOW to build.
- **Output**: `specs/{branch}/plan.md`
- **Content**: Architecture, DB Schema, API Endpoints.

### Step 4: Tasks (`speckit.tasks`)
- **Goal**: Break down into actionable steps.
- **Output**: `specs/{branch}/tasks.md`
- **Content**: Detailed implementation checklist (TDD).

### Step 5: Analyze (`speckit.analyze`)
- **Goal**: Impact analysis.
- **Output**: `specs/{branch}/analysis.md`
- **Content**: Files to modify, Side effects, Migration needs.

### Step 6: Implement (`speckit.implement`)
- **Goal**: Write code & Test.
- **Action**: Execute `tasks.md`. Verify with tests.

## 4. Clean Architecture
- **Dependency Rule**: Source code dependencies can only point inwards.
- **Layers**:
  - `Entities` (Enterprise Business Rules)
  - `Use Cases` (Application Business Rules)
  - `Interface Adapters` (Controllers, Gateways, Presenters)
  - `Frameworks & Drivers` (Web, DB, Devices)
- **Directory Structure**:
  - `app/api`: Presentation Layer
  - `app/services`: Application Layer (Use Cases)
  - `app/domain`: Domain Layer (Models, Interfaces)
  - `app/infrastructure`: Infrastructure Layer
  - `app/core`: Shared Utilities

### 5. Documentation
- **Lean README**: The root `README.md` MUST remain lightweight. It serves as an entry point only.
- **Spec as Docs**: Feature details live in `specs/{number}-{name}/spec.md`. Do NOT duplicate this into the README.
- **Docs Directory**: General guides (Deployment, API Style Guide, etc.) go to `docs/`.

## 6. Agent Behavior
- **Proactive**: If requirements are vague, ask clarifying questions (Step 2).
- **Safe**: Always run tests before finishing a task.
- **No Silent Execution**: NEVER commit code or modify permanent documentation without explaining the plan and getting explicit user approval first.
- **Consultative**: Do NOT blindly follow instructions if they carry risk. Offer professional opinion first.
- **Context**: Always check `.specify/memory` for project context.

### 7. Communication Protocol
- **Explicit Confirmation**: For critical decisions (e.g., Plan approval, High-risk deletions), the Agent MUST ask for an explicit "Accept" or "Cancel" and set `BlockedOnUser=true`.
- **Change Management**: Any deviation from the initial plan MUST be recorded in the `Decision Log` of the corresponding Spec/Plan document.

### 8. Response Handling
- **Accept Aliases**: `Accept`, `Yes`, `Y`, `Ok`, `Okay`, `Good`, `Go`, `G`, `A`, `1`, `Dd`, `Dz`, `ㅇㅇ`, `ㅇㅋ`, `어`, `좋아`, `ㄱㄱ`
  - Action: Proceed immediately.
- **Cancel Aliases**: `Cancel`, `No`, `N`, `Stop`, `Quit`, `Wait`, `X`, `2`, `Ss`, `ㄴㄴ`, `아니`, `취소`, `멈춰`
  - Action: Stop and ask for revised instructions.
- **Other Input**: Interpret as new feedback or a change in requirements.