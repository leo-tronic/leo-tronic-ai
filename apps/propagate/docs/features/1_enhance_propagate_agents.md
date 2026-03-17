# Feature 1: Enhance propagate agents

## Goal
Enhance propagate agents for opencode by injecting general context into agent-specific context files. Since opencode does not have a "system" context (only agent-specific contexts), general guidelines must be defined centrally in `general.md` and injected into each agent's context file.

**Key Deliverables:**
- Modified `propagate_opencode_agents()` method to read and inject general context
- General context prepended to all agent files with visual separator
- Elimination of duplicate content across agent files

---

## Implementation Summary

### Changes Made
Modified `apps/propagate/src/propagate.py` - `propagate_opencode_agents()` method:

1. **Read General Context**: Loads content from `docs/agents/general.md`
2. **Iterate Agent Files**: Processes all agent files except `general.md` (build.md, debug.md, plan.md, software_design.md)
3. **Inject Context**: For each agent file:
   - Prepends the general context from `general.md`
   - Adds `---` separator for clarity
   - Appends the agent-specific content
   - Writes combined content to `~/.config/opencode/agents/`
4. **Skip General.md**: The `general.md` file itself is not copied, serving only as a source for injection

### Key Design Decisions
- **Prepend Pattern**: General context comes first to establish baseline guidelines before agent-specific instructions
- **Separator**: `---` provides visual separation between general and agent-specific sections
- **No Duplication**: Each agent file now contains the general context without manual duplication

### Testing & Verification
- ✅ Local test execution successful: All 4 agent files propagated correctly
- ✅ Content verification: Correct injection pattern with separator confirmed
- ✅ General.md skipping: Verified that `general.md` is not copied to output directory

### Result
Agent context files now automatically include general guidelines from a single source of truth, ensuring consistency across all agents while reducing maintenance burden.

---

## Commit Information
- **Commit Hash**: 15f5228
- **Message**: "feat: enhance propagate_opencode_agents to inject general context into agent files"

