# Codex Skills Setup

This folder records how to reproduce the Codex skill setup without changing
or duplicating the Claude source tree.

## Sources and active locations

- Versioned source of truth: `.claude/skills/` in this repository.
- Codex personal skills: `%USERPROFILE%\.agents\skills\`.
- Codex-native skills and built-in integrations: `%CODEX_HOME%\skills\` (normally
  `%USERPROFILE%\.codex\skills\`). Keep these separate from imported skills.
- Codex custom agents: `%CODEX_HOME%\agents\`. Plugin-derived agent prompts are
  local adaptations and are not copied into this repository.

Do not commit a second tree of generated skill copies. On a new machine, clone
this private repository, then use Codex's `migrate-to-codex` skill on the
checked-in `.claude/skills` source. Use its `--plan`, `--dry-run`, and
`--validate-target` steps; select skills only, use its documented global-scope
target, and review the report before accepting the result.
Do not migrate Claude credentials, settings, hooks, MCP configuration, or
plugins as part of a skills-only setup.

## Routing contract

The top-level `skill-map` routes by repository and task. Load `velth-preflight`
or `veos-preflight` first in those repositories, then follow that preflight's
task table and hard-dependency pairs. Skill `description` metadata is the
supported automatic activation signal; `when_to_use` is source-specific
metadata where present. There is no supported `trigger:` field and no
automatic transitive loading, so mandatory pairs are stated explicitly in the
map/preflight rather than copied into every unrelated skill.

## Current source snapshot

The source checkout was verified at `fix/missing-hotfixes`, commit
`5e7d9ac7bd7f57c6c8a3d5e6f4ca102d787eb4a1` on 2026-09-26. Fetch and verify the
remote before refreshing; do not assume this recorded commit remains latest.

Claude plugin-synced skills and cached marketplace agent prompts are not
redistributed here. Install or adapt them only through their supported local
plugin workflows and terms. Codex-native equivalents should be preferred when
available.
