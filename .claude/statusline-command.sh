#!/usr/bin/env bash
# Claude Code status line
# Layout: <dir>  <branch>  <model>  <context>
input=$(cat)

dir=$(echo "$input" | jq -r '.workspace.current_dir // .cwd')
model=$(echo "$input" | jq -r '.model.display_name // .model.id // "Claude"')
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
five_h=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
seven_d=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

# Shorten dir: replace $HOME with ~
home_dir="$HOME"
display_dir="${dir/#$home_dir/~}"

# Git branch (skip optional locks)
git_branch=""
if git -C "$dir" rev-parse --git-dir > /dev/null 2>&1; then
  git_branch=$(git -C "$dir" --no-optional-locks symbolic-ref --short HEAD 2>/dev/null \
    || git -C "$dir" --no-optional-locks rev-parse --short HEAD 2>/dev/null)
fi

# Context percentage with color
# green < 30%, yellow 30–85%, red > 85%
ctx_part=""
if [ -n "$used_pct" ]; then
  used_int=${used_pct%.*}
  if [ "$used_int" -ge 85 ]; then
    ctx_color="\033[0;31m"   # red
  elif [ "$used_int" -ge 30 ]; then
    ctx_color="\033[0;33m"   # yellow
  else
    ctx_color="\033[0;32m"   # green
  fi
  ctx_part="${ctx_color}${used_int}%\033[0m"
fi

# Separator (dim)
sep="\033[2m \033[0m"

# Parts
dir_part="\033[1;36m${display_dir}\033[0m"

branch_part=""
if [ -n "$git_branch" ]; then
  # Check for uncommitted changes (staged or unstaged)
  git_dirty=""
  if ! git -C "$dir" --no-optional-locks diff --quiet HEAD 2>/dev/null || \
     [ -n "$(git -C "$dir" --no-optional-locks ls-files --others --exclude-standard 2>/dev/null | head -1)" ]; then
    git_dirty=" \033[0;33m●\033[0m"
  fi
  branch_part="\033[0;35m${git_branch}\033[0m${git_dirty}"
fi

model_part="\033[2m${model}\033[0m"

# Rate limits — only show when yellow (≥50%) or red (≥80%)
rate_part=""
if [ -n "$five_h" ]; then
  five_int=${five_h%.*}
  if [ "$five_int" -ge 80 ]; then
    rate_part="\033[0;31m5h:${five_int}%\033[0m"
  elif [ "$five_int" -ge 50 ]; then
    rate_part="\033[0;33m5h:${five_int}%\033[0m"
  fi
fi
if [ -n "$seven_d" ]; then
  seven_int=${seven_d%.*}
  if [ "$seven_int" -ge 80 ]; then
    seven_part="\033[0;31m7d:${seven_int}%\033[0m"
  elif [ "$seven_int" -ge 50 ]; then
    seven_part="\033[0;33m7d:${seven_int}%\033[0m"
  fi
  if [ -n "$seven_part" ]; then
    if [ -n "$rate_part" ]; then
      rate_part="${rate_part} ${seven_part}"
    else
      rate_part="${seven_part}"
    fi
  fi
fi

# Assemble — skip empty parts
output="${dir_part}"
[ -n "$branch_part" ] && output="${output}${sep}${branch_part}"
output="${output}${sep}${model_part}"
[ -n "$ctx_part" ]    && output="${output}${sep}${ctx_part}"
[ -n "$rate_part" ]   && output="${output}${sep}${rate_part}"

echo -ne "${output}"
