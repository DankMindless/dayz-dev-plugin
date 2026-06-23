# Codex plugin

This repository is a public Codex marketplace. Its self-contained plugin lives
at `plugins/dayz-dev`; the original Claude, Gemini, Cursor, and Windsurf files
remain available at the repository root.

## Install

From the current default branch:

```powershell
codex plugin marketplace add DayZGhost/dayz-dev-plugin --ref main
codex plugin add dayz-dev@dayzghost-dayz
```

For a pinned install, use a release tag:

```powershell
codex plugin marketplace add DayZGhost/dayz-dev-plugin --ref v0.1.0
codex plugin add dayz-dev@dayzghost-dayz
```

Start a new Codex thread after installation so the `$dayz-dev` skill appears
in the thread's capability list.

## Configure DayZ source discovery

The plugin uses local source as its primary API contract. A valid
`DAYZ_SOURCE_ROOT` is the directory containing all three of these paths:

- `scripts/1_core`
- `scripts/3_game`
- `scripts/4_world`

The read-only helper resolves the source root in this order:

1. `DAYZ_SOURCE_ROOT`
2. the current workspace and its ancestors
3. the standard Windows `P:\` mapping
4. a path explicitly supplied by the user

Example for the current PowerShell session:

```powershell
$env:DAYZ_SOURCE_ROOT = 'P:\'
```

Persist it for future processes with:

```powershell
[Environment]::SetEnvironmentVariable('DAYZ_SOURCE_ROOT', 'P:\', 'User')
```

No source tree is bundled. If local discovery fails, the skill asks for a path
or uses current authoritative web documentation.

## Upgrade

Refresh the marketplace, reinstall the plugin, and start a new Codex thread:

```powershell
codex plugin marketplace upgrade dayzghost-dayz
codex plugin remove dayz-dev@dayzghost-dayz
codex plugin add dayz-dev@dayzghost-dayz
```

Run `codex plugin marketplace --help` if the installed experimental CLI uses a
different refresh subcommand.

## Troubleshooting

- Confirm the marketplace with `codex plugin marketplace list`.
- Confirm installation and enabled state with `codex plugin list`.
- Run `python plugins/dayz-dev/skills/dayz-dev/scripts/find_dayz_source.py --start .`.
- If discovery fails, set `DAYZ_SOURCE_ROOT` or pass `--root <path>` when testing.
- Reinstall and open a new thread after changing plugin files or versions.

## Privacy and safety

The plugin contains instructions, Markdown references, and a read-only source
discovery helper. It has no MCP server, app, hooks, credentials, telemetry, or
build automation. Codex may read local project and DayZ source files while
answering a request. Web access is used only when local evidence is absent or
freshness matters, subject to the user's Codex network and approval settings.

## License and attribution

The repository and Codex adaptation are GPL-3.0. Codex packaging was
contributed by JustWats; the project and reference material derive
from [DayZGhost/dayz-dev-plugin](https://github.com/DayZGhost/dayz-dev-plugin)
at the revision recorded in `plugins/dayz-dev/NOTICE.txt`, and their authorship
remains with the upstream contributors. Bohemia Interactive source files are
neither copied into nor distributed with this plugin.
