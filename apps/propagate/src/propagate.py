import shutil
from pathlib import Path

# Root of the leo-tronic-ai repository relative to this file
_REPO_ROOT = Path(__file__).parent.parent.parent.parent

# OpenCode configuration directory
_OPENCODE_CONFIG_DIR = Path.home() / ".config" / "opencode"


def propagate_opencode_agents() -> bool:
    """
    Copies agent files from leo-tronic-ai/docs/agents to
    ~/.config/opencode/agents, injecting general context from general.md
    into each agent-specific context file.
    """
    source_dir = _REPO_ROOT / "docs" / "agents"
    dest_dir = _OPENCODE_CONFIG_DIR / "agents"

    if not source_dir.exists():
        print(f"Error: Source directory does not exist: {source_dir}")
        return False

    # Read the general context that will be injected into all agent files
    general_context_file = source_dir / "general.md"
    if not general_context_file.exists():
        print(f"Error: General context file does not exist: {general_context_file}")
        return False

    try:
        with open(general_context_file, "r") as f:
            general_context = f.read()
    except Exception as e:
        print(f"Error reading general context file: {e}")
        return False

    dest_dir.mkdir(parents=True, exist_ok=True)

    try:
        files_copied = 0
        for file_path in source_dir.iterdir():
            # Skip the general.md file itself and only process other agent files
            if file_path.is_file() and file_path.name != "general.md":
                try:
                    # Read the agent-specific content
                    with open(file_path, "r") as f:
                        agent_content = f.read()

                    # Combine: general context + separator + agent-specific content
                    combined_content = f"{general_context}\n---\n\n{agent_content}"

                    # Write the combined content to the destination
                    dest_file = dest_dir / file_path.name
                    with open(dest_file, "w") as f:
                        f.write(combined_content)

                    print(
                        f"Propagated with injected context: {file_path.name} -> {dest_file}"
                    )
                    files_copied += 1
                except Exception as e:
                    print(f"Error processing {file_path.name}: {e}")
                    return False

        print(
            f"Successfully propagated {files_copied} agent files with injected general context to {dest_dir}"
        )
        return True
    except Exception as e:
        print(f"Error propagating agent files: {e}")
        return False


def propagate_opencode_base_config() -> bool:
    """
    Copies the opencode MCP settings file from
    leo-tronic-ai/config/mcp/opencode.jsonc to
    ~/.config/opencode/opencode.jsonc.
    """
    source_file = _REPO_ROOT / "config" / "mcp" / "opencode.jsonc"
    dest_file = _OPENCODE_CONFIG_DIR / "opencode.jsonc"

    if not source_file.exists():
        print(f"Error: Source file does not exist: {source_file}")
        return False

    _OPENCODE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(source_file, dest_file)
        print(f"Copied: {source_file.name} -> {dest_file}")
        return True
    except Exception as e:
        print(f"Error propagating base config: {e}")
        return False


def propagate_opencode() -> bool:
    """
    Propagates all opencode configuration from the leo-tronic-ai repository
    to ~/.config/opencode/:
      - Agent files (docs/agents -> agents/)
      - Base MCP config (config/mcp/opencode.jsonc -> opencode.jsonc)
    """
    agents_ok = propagate_opencode_agents()
    config_ok = propagate_opencode_base_config()
    return agents_ok and config_ok


if __name__ == "__main__":
    propagate_opencode()
