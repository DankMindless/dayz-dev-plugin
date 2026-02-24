# DayZ Development Plugin

A comprehensive plugin for DayZ mod development with Enforce Script. Provides dynamic documentation fetching, framework support for vanilla, Community Framework, and DayZ Expansion.

**Supports:** Claude Code, Cursor, Windsurf, and other AI coding assistants.
**Target Version:** DayZ 1.28+ (v1.28.161464)

## Features

- **Dynamic Documentation Fetching** - Fetches up-to-date script API, config references, and mod docs via WebFetch
- **Multi-Framework Support** - Vanilla, Community Framework (CF), DayZ Expansion with auto-detection
- **Enforce Script Correctness** - Never outputs C#/C++ syntax, always uses proper Enforce Script
- **No-Hallucination Policy** - Verifies all classes, methods, and config tokens against documentation
- **1.28 Compatibility** - Full reference for breaking changes, migration guide, and new features
- **Best Practices** - Null safety, server/client context, memory management, performance patterns

## Installation

### Claude Code (NPM)

```bash
npm install -g claude-dayz-dev
```

### Claude Code (Git)

```bash
git clone https://github.com/chaos/dayz-dev-plugin.git ~/.claude/skills/dayz-dev
```

### Cursor / Windsurf

1. Download `DAYZ_CURSOR_RULES.md` from this repo
2. Copy to your DayZ mod project root as `.cursorrules`

```bash
curl -o .cursorrules https://raw.githubusercontent.com/chaos/dayz-dev-plugin/main/DAYZ_CURSOR_RULES.md
```

### Manual

1. Download/clone this repository
2. Copy to `~/.claude/skills/dayz-dev/`
3. Restart your AI assistant

## Usage

### Automatic (Skill)

The skill activates automatically when you ask DayZ-related questions:

- "How do I create a custom item in DayZ?"
- "What's the config.cpp format for a new weapon?"
- "How does the CF RPCManager work?"
- "Show me the Expansion market trader config"
- "What broke in 1.28?"

### Command

Use the `/dayz-dev` command for direct queries:

```
/dayz-dev How to create a modded class for PlayerBase?
/dayz-dev What are the NetSync variable types?
/dayz-dev Expansion quest system setup
/dayz-dev 1.28 vehicle breaking changes
```

## Documentation Sources

| Source | URL | Coverage |
|--------|-----|----------|
| DayZ Scripts API | https://dayz-scripts.yadz.app/ | Script API v1.28, classes, methods |
| DayZ Script Diff | https://github.com/BohemiaInteractive/DayZ-Script-Diff | Official source code changes |
| BI Community Wiki | https://community.bistudio.com/wiki/DayZ:Enforce_Script_Syntax | Language reference |
| DayZ Explorer | https://dayzexplorer.zeroy.com/ | Enforce essentials, Math, FileIO |
| Community Framework | https://github.com/Arkensor/DayZ-CommunityFramework | CF source + docs |
| Expansion Wiki | https://github.com/salutesh/DayZ-Expansion-Scripts/wiki | 119+ wiki pages |
| DZconfig Wiki | https://dzconfig.com/wiki/ | Server configuration |
| Central Economy | https://github.com/BohemiaInteractive/DayZ-Central-Economy | types.xml, events.xml |

## Skill Files

| Directory | Contents |
|-----------|----------|
| `SKILL.md` | Main orchestrator with decision tree and verification rules |
| `scripting/` | Enforce Script language, class hierarchy, client-server, memory management |
| `systems/` | Mod structure, networking, inventory, actions, weapons, vehicles |
| `frameworks/` | Framework detection, Community Framework, Expansion |
| `config/` | config.cpp, types.xml, server configuration |
| `compatibility/` | Version 1.28 breaking changes and migration guide |
| `commands/` | `/dayz-dev` slash command template |

## What's Covered

### Enforce Script
- Complete language reference (types, operators, control flow, classes)
- Modded class injection patterns
- Memory management (ref, autoptr, Managed)
- Templates, enums, casting, preprocessor

### DayZ Systems
- Mod folder structure and PBO packaging
- RPC systems (vanilla ScriptRPC + CF RPCManager)
- Net sync variables and CF NetworkedVariables
- Inventory system (locations, creation, movement)
- Action system (interact, continuous, single-use, firearm)
- Weapon system (FSM, configs, scripting)
- Vehicle system (configs, physics, 1.28 changes)

### Frameworks
- Vanilla, CF, and Expansion auto-detection
- CF Modules, RPCManager, ModStorage
- Expansion Market, Quests, AI, Basebuilding, Vehicles

### Configuration
- config.cpp (CfgPatches, CfgMods, CfgVehicles, CfgWeapons)
- types.xml and Central Economy
- Server configuration (serverDZ.cfg, cfgGameplay.json)
- 1.28 enhanced spawnabletypes.xml

### 1.28 Compatibility
- 12 breaking changes documented with before/after code
- Migration checklist
- New features (sealed, Obsolete, new Entity methods)
- Framework version requirements

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - Feel free to use and modify.

## Credits

- Bohemia Interactive - DayZ, Enforce Script, official documentation
- Arkensor - Community Framework
- salutesh - DayZ Expansion Scripts
- DayZ modding community - DayZ Explorer, DayZ Scripts, community wikis
- FiveM Dev Plugin (melihbozkurt10) - Architectural inspiration
