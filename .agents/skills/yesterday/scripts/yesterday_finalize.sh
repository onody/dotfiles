#!/bin/zsh
set -euo pipefail

repo_root="/Users/onod/src/memo"
skill_root="/Users/onod/.agents/skills/eod"
today="$(date +%F)"
commit_message="EOD ${today}"

cd "$repo_root"

# Normalize only changed markdown so EOD does not rewrite the whole repo.
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
done < <(git -C "$repo_root" status --short raw/ wiki/)

if (( ${#changed_files[@]} > 0 )); then
  python3 "$skill_root/scripts/eod_normalize_markdown.py" "${changed_files[@]}"
fi

git -C "$repo_root" add raw/ wiki/

if git -C "$repo_root" diff --cached --quiet; then
  echo "No staged changes under raw/ or wiki/. Skipping commit and push."
  exit 0
fi

git -C "$repo_root" commit -m "$commit_message"
git -C "$repo_root" push origin main

echo "Pushed: $commit_message"
