# General 

- CONTEXT LOAD VERIFICATION TEST: Cyrus' favorite color is neon
- **Slack Messaging (Feature Toggle)**: Slack status/summary messaging is **disabled by default**. To enable Slack notifications for agent progress and findings, explicitly request it in your chat message (e.g., "enable slack updates" or "send slack notifications"). When enabled, agents will notify via the slack-bot MCP in the channel ID listed below with any questions, findings, or updates.
- When there is any doubt our ambiguity, ask for clarification first. Do not limit the amount of questions asked.
- Before beginning any work, ensure a todo list is constructed and approved first
- DO NOT modify any files without first getting explicit approval
- When working through a planning or research document with multiple sections or acceptance criteria, **do NOT proceed to the next section or AC without explicit approval from the user**. Complete the current section, present findings, and wait for instruction before continuing.
- Do not access new directories outside of the current workspace without approval.
- Always get your MCP tool call chains approved first
- Do not doom loop, aka continue looping infinitely.
- When working on a todo for a long time, ensure you are stopping and presenting roadblocks to the driver of the agent before proceeding any longer
- Always explain reasoning and steps, no matter what
- Do not print code to stdout with line numbers, they are not copy-able
- When coming across major problems, whether it be on the task at hand or observed in an unrelated location, always alert the driver.
- The path to all documents is `~/repos/leo-tronic-ai/docs/`
- The following directories are where various forms of documents are stored in the leo-tronic-ai repo:
  - docs/bugs
  - docs/designs
  - docs/features
  - docs/research
- Docs will be numbered with <doctype>/<number>_<title>.md
  - Thus if I say "feature doc 5", it maps to `~/repos/leo-tronic-ai/docs/<doctype>/<number>_<title>.md`, in this case
  it will be: `~/repos/leo-tronic-ai/docs/features/5_TITLE.md`
- When tasks are independent, run them in parallel if possible. If it is unclear whether they can be 
  executed independently, always ask
- For ANY slack usage outside of simply writing messages to inform the user, use the "slack" MCP instead, 
as slack-bot does not have the right permissions to read/write messages outside of that singular channel listed below

# Metadata
- Slack channel for agent communication: C0ALVT30US1
- My Confluence Space ID is: 712020c5ab58d828254cf7920b8efed46bd147. Use this ID instead of perfoming an MCP search
- My JIRA project is "TRAN" and team is "Front Office API - TRAN"

## Agent Context Sync
- After making ANY changes to agent context files (e.g. files under `~/repos/leo-tronic-ai/docs/agents/`), always run the following command to sync the changes to the corresponding tools:
  ```
  python3 /Users/lscarano/repos/leo-tronic-ai/apps/propagate/src/propagate.py
  ```

## Github MCP tool
- If at any point the Github MCP tool call fails, use the gh CLI instead if possible
