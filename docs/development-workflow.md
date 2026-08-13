# Development Workflow & Branch Strategy

HemoVision follows a structured, milestone-driven branching model aligned with project development phases.

---

## 1. Branch Hierarchy

```text
main (Production / Stable Release Branch)
 │
 ├── phase-0-foundation           <-- (ACTIVE PHASE)
 ├── phase-1-dataset
 ├── phase-2-camera
 ├── phase-3-segmentation
 ├── phase-4-quality
 ├── phase-5-hb-model
 ├── phase-6-validation
 ├── phase-7-mobile
 ├── phase-8-on-device
 └── phase-9-backend
```

### Branch Guidelines
* `main`: Protected branch representing audited, stable code. Direct pushes are blocked.
* `phase-N-*`: Dedicated milestone feature branches tracking phase objectives.
* `feature/<feature-name>`: Ephemeral development topic branches created off the current phase branch.

---

## 2. Standard 7-Step Pull Request (PR) Process

Every feature or phase completion must follow these 7 steps:

1. **Branch Creation**: Create a topic branch (e.g., `git checkout -b feature/dataset-schemas phase-0-foundation`).
2. **Implementation**: Build required functionality or documentation according to specification.
3. **Tests**: Add unit tests or validation scripts under `ml/tests/`.
4. **Documentation**: Update corresponding `docs/` specifications or `README.md`.
5. **Local Verification**: Run linting and unit test suite:
   ```bash
   pytest ml/tests/
   ```
6. **Pull Request**: Open a Pull Request targeting the active phase branch or `main`. Attach metric evidence or test verification outputs.
7. **Merge**: Require at least 1 code review approval and passing automated CI checks before merging.
