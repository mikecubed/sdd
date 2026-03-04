#!/bin/bash

set -euo pipefail

run_command() {
    local command_to_run="$*"
    local output
    local exit_code

    output=$(eval "$command_to_run" 2>&1) || exit_code=$?
    exit_code=${exit_code:-0}

    if [ $exit_code -ne 0 ]; then
        echo -e "\033[0;31m[ERROR] Command failed (Exit Code $exit_code): $command_to_run\033[0m" >&2
        echo -e "\033[0;31m$output\033[0m" >&2
        exit $exit_code
    fi
}

echo -e "\n🤖 Installing Copilot CLI..."
run_command "npm install -g @github/copilot@latest"
echo "✅ Done"

echo -e "\n🤖 Installing Claude Code..."
run_command "npm install -g @anthropic-ai/claude-code@latest"
echo "✅ Done"

echo -e "\n🐍 Installing uv..."
run_command "pipx install uv"
echo "✅ Done"

echo -e "\n📦 Installing sdd-cli in development mode..."
run_command "uv pip install --system -e '.[test]'"
echo "✅ Done"

echo -e "\n🧹 Cleaning cache..."
run_command "sudo apt-get autoclean"
run_command "sudo apt-get clean"

echo "✅ Setup complete. Run 'sdd --help' to get started."

