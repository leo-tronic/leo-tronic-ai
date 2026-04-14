import json
import shutil
from pathlib import Path
import re

# Root of the leo-tronic-ai repository relative to this file
_REPO_ROOT = Path(__file__).parent.parent.parent.parent

# OpenCode configuration directory
_OPENCODE_CONFIG_DIR = Path.home() / ".config" / "opencode"

# Claude configuration file
_CLAUDE_CONFIG_FILE = Path.home() / ".claude.json"


def _strip_jsonc_comments(content: str) -> str:
    """
    Remove JSON comments from JSONC content.
    Handles both line comments (//) and block comments (/* */).
    """
    # Remove line comments (// ...)
    content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
    # Remove block comments (/* ... */)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return content


def _load_json_or_jsonc(file_path: Path) -> dict:
    """
    Load JSON or JSONC file, handling comments in JSONC files.
    """
    try:
        with open(file_path, "r") as f:
            content = f.read()

        # Strip comments if needed
        if file_path.suffix == ".jsonc":
            content = _strip_jsonc_comments(content)

        return json.loads(content)
    except Exception as e:
        raise Exception(f"Error parsing {file_path.name}: {e}")


def propagate_claude_mcp() -> bool:
    """
    Reads MCP server definitions from leo-tronic-ai/config/mcp/claude_code.json
    and merges them into ~/.claude.json under the "mcpServers" key.
    Preserves existing servers not managed by the repository.
    """
    mcp_source_dir = _REPO_ROOT / "config" / "mcp"
    claude_code_file = mcp_source_dir / "claude_code.json"

    if not claude_code_file.exists():
        print(f"Error: Source file does not exist: {claude_code_file}")
        return False

    try:
        # Load the source MCP servers from claude_code.json
        source_config = _load_json_or_jsonc(claude_code_file)
        source_servers = source_config.get("mcpServers", {})

        # Load existing ~/.claude.json or create empty structure
        if _CLAUDE_CONFIG_FILE.exists():
            try:
                with open(_CLAUDE_CONFIG_FILE, "r") as f:
                    claude_config = json.load(f)
            except Exception as e:
                print(f"Error reading {_CLAUDE_CONFIG_FILE}: {e}")
                return False
        else:
            claude_config = {}

        # Ensure mcpServers key exists
        if "mcpServers" not in claude_config:
            claude_config["mcpServers"] = {}

        # Track changes for reporting
        added = []
        updated = []

        # Merge servers from source into destination
        for server_name, server_def in source_servers.items():
            if server_name in claude_config["mcpServers"]:
                updated.append(server_name)
            else:
                added.append(server_name)
            claude_config["mcpServers"][server_name] = server_def

        # Write updated config back to ~/.claude.json
        try:
            with open(_CLAUDE_CONFIG_FILE, "w") as f:
                json.dump(claude_config, f, indent=2)
        except Exception as e:
            print(f"Error writing to {_CLAUDE_CONFIG_FILE}: {e}")
            return False

        # Report results
        print(f"Propagated MCP servers to {_CLAUDE_CONFIG_FILE}")
        if added:
            print(f"  Added: {', '.join(added)}")
        if updated:
            print(f"  Updated: {', '.join(updated)}")

        return True

    except Exception as e:
        print(f"Error propagating Claude MCP configuration: {e}")
        return False


def propagate_claude() -> bool:
    """
    Propagates all Claude MCP configuration.
    """
    return propagate_claude_mcp()


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


def propagate_all() -> bool:
    """
    Unified entry point: propagates both OpenCode and Claude configurations.
    """
    opencode_ok = propagate_opencode()
    claude_ok = propagate_claude()
    return opencode_ok and claude_ok


if __name__ == "__main__":
    propagate_all()
