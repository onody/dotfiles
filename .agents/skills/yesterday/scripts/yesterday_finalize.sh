#!/bin/zsh
set -euo pipefail

repo_root="/Users/onod/src/memo"
skill_root="/Users/onod/.agents/skills/yesterday"
target_date="${1:-$(date -v-1d +%F)}"
commit_message="EOD ${target_date}"

# Codex can invoke this script with a restricted environment, so bootstrap a
# standard PATH and resolve the binaries we need up front.
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:${PATH:-}"

git_bin="$(command -v git || true)"
python_bin="$(command -v python3 || true)"
ssh_bin="$(command -v ssh || true)"

if [[ -z "$git_bin" ]]; then
  echo "git not found in PATH: $PATH" >&2
  exit 1
fi

if [[ -z "$python_bin" ]]; then
  echo "python3 not found in PATH: $PATH" >&2
  exit 1
fi

if [[ -z "$ssh_bin" ]]; then
  echo "ssh not found in PATH: $PATH" >&2
  exit 1
fi

export GIT_SSH_COMMAND="${GIT_SSH_COMMAND:-$ssh_bin}"

cd "$repo_root"

# Normalize only changed markdown so this does not rewrite the whole repo.
changed_files=()
while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  path="${line#?? }"
  [[ "$path" != *.md ]] && continue
  case "$path" in
    raw/*|wiki/*)
      changed_files+=("$path")
      ;;
  esac
done < <("$git_bin" -C "$repo_root" status --short raw/ wiki/)

if (( ${#changed_files[@]} > 0 )); then
  "$python_bin" "$skill_root/scripts/yesterday_normalize_markdown.py" "${changed_files[@]}"
fi

"$git_bin" -C "$repo_root" add raw/ wiki/

if "$git_bin" -C "$repo_root" diff --cached --quiet; then
  echo "No staged changes under raw/ or wiki/. Skipping commit and push."
  exit 0
fi

"$git_bin" -C "$repo_root" commit -m "$commit_message"
"$git_bin" -C "$repo_root" push origin main

echo "Pushed: $commit_message"
