# Agent Usage Guide

## End-to-End Workflow

### 1. Create Requirements Document

**Location:** `docs/features/[YYYY-MM-feature-name].md`

# Feature: [Name]

## Goal
What you're trying to achieve

## Functional Requirements
- Specific requirement 1
- Specific requirement 2

## Behavioral Requirements
- Specific requirement 1
- Specific requirement 2

## Technical Constraints
- Must/cannot do X

## Affected Areas
- Link to relevant components

## Testing & Validation
- Test X comonent against Y requirement

## Open Questions / Areas to Research
- Open question 1
- Area to research 1

## Additional Resources
- web: <url>
- Document: <relative_or_absolute_path_to_doc>
- Code: <relative_or_absolute_path_to_code_file>
- Directory: <relative_or_absolute_path_to_dir>

### 2. Request a Plan

**Command:** "Plan the feature in `docs/features/active/[your-feature].md`"

**What happens:**
- Agent researches codebase autonomously
- Returns 3-6 step plan with file links
- Lists considerations/decisions needed

### 3. Iterate on Plan

**Provide feedback:**
- "Focus more on X"
- "What about alternative Y?"
- "Add details for step 3"

Agent re-researches and refines until you're satisfied.

### 4. Approve Plan

Once happy with the plan, explicitly approve it or note what's ready for implementation.

### 5. Switch to Implementation

**Exit Plan mode** - Switch to regular or implementation mode

**Request implementation:** "Implement the plan from [conversation/feature doc]"

### 6. Select Model

**Premium reasoning models (Sonnet, advanced Pro variants):**
- Complex multi-file changes
- Architectural decisions
- Infrastructure as Code
- Requires understanding context across many files
- Debugging subtle issues

**Mid-tier models (Pro, base variants):**
- Standard feature implementation
- Moderate complexity changes
- Good balance of speed and capability
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

### 7. Review Code Changes

**Accepting:**
- Review diffs carefully
- Test in non-production first
- Accept changes when satisfied

**Rejecting:**
- Provide specific feedback
- Request modifications
- Agent will iterate

## Pro Tips

- **Be specific** in requirements docs
- **Iterate plans** before implementing
- **One feature at a time** for clarity
- **Move implemented specs** to `docs/features/implemented/`
- **Link to existing files** in requirements for faster agent research
- **Start with premium models** for planning, then use faster models for execution if changes are straightforward
