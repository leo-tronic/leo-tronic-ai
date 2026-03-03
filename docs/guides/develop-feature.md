# Feature Development Guide

This guide describes how agents and engineers should navigate the feature development lifecycle, from requirements through implementation and review.

The canonical feature doc template lives at [`docs/templates/feature.md`](../templates/feature.md). Copy it to `docs/features/[YYYY-MM-feature-name].md` when starting a new feature.

---

## End-to-End Workflow

### 1. Create a Requirements Document

Copy [`docs/templates/feature.md`](../templates/feature.md) to:

```
docs/features/[YYYY-MM-feature-name].md
```

Fill in at minimum: **Goal**, **Scope**, **Functional Requirements**, **Behavioral Requirements**, **Technical Constraints**, and **Open Questions / Areas to Research**. The remaining sections are populated progressively during planning and implementation.

---

### 2. Request a Plan

**Command:** "Plan the feature in `docs/features/[your-feature].md`"

**What happens:**
- Agent researches the codebase autonomously
- Returns a 3–6 step plan with file links
- Lists considerations and decisions needed
- Populates **Affected Files/Dirs** and **Architecture Overview** (High Level)

---

### 3. Iterate on the Plan

Provide feedback before implementation begins:
- "Focus more on X"
- "What about alternative Y?"
- "Add details for step 3"

Agent re-researches and refines. Unresolved **Open Questions** must be addressed here before moving forward.

---

### 4. Approve the Plan

Once satisfied, explicitly approve the plan or note which parts are ready for implementation. At this point the agent should populate **Architecture Overview (Low Level)** and **Acceptance Criteria** if not already done.

---

### 5. Switch to Implementation

Exit planning mode and switch to regular or implementation mode.

**Request implementation:** "Implement the plan from [conversation/feature doc]"

During implementation the agent should:
- Keep **Affected Files/Dirs** statuses up to date
- Populate **Key Discoveries & Pitfalls** as surprises arise
- Move resolved **Open Questions** out of that section (or strike them through)
- Populate **Outstanding Items** with anything that surfaces mid-implementation

---

### 6. Select a Model

**Premium reasoning models (Sonnet, advanced Pro variants):**
- Complex multi-file changes
- Architectural decisions
- Infrastructure as Code
- Debugging subtle issues
- Requires understanding context across many files

**Mid-tier models (Pro, base variants):**
- Standard feature implementation
- Moderate complexity changes
- Most general development work

**Fast/lightweight models (Haiku, Fast, Mini variants):**
- Simple single-file edits
- Repetitive refactoring
- Straightforward bug fixes
- Documentation updates
- Quick iterations

**Code-specialized models (Codex variants):**
- Pure code generation tasks
- Less context-heavy implementations
- Algorithm implementations

---

### 7. Review Code Changes

**Accepting:**
- Review diffs carefully
- Test in non-production first
- Accept changes when satisfied

**Rejecting:**
- Provide specific feedback
- Request modifications
- Agent will iterate

---

### 8. Close Out the Feature

Once all **Acceptance Criteria** are met:
1. Resolve or document remaining **Outstanding Items**
2. Ensure **Next Steps** are captured or ticketed
3. Move the feature doc to `docs/features/implemented/`

---

## Pro Tips

- **Be specific** in requirements docs — vague goals produce vague plans
- **Iterate plans before implementing** — changes are cheap in planning, expensive mid-implementation
- **One feature at a time** for clarity
- **Link to existing files** in requirements for faster agent research
- **Start with premium models** for planning, then use faster models for execution if changes are straightforward
- **Keep the feature doc alive** — update it as the source of truth throughout the lifecycle, not just at the start
