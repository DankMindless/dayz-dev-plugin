---
name: dayz-dev
description: 'Develop, review, and explain DayZ mods using verified Enforce Script APIs and configuration formats. Use for DayZ classes or methods, config.cpp, mod structure, networking and RPC, inventory, actions, weapons, vehicles, Central Economy XML, server configuration, vanilla or Community Framework or Expansion integration, and version compatibility.'
---

# DayZ Development

Use the installed DayZ source tree as the primary API contract. Use the bundled references for concepts and patterns, then consult current authoritative sources when the installed files do not answer the question.

## Core workflow

1. Ground the task in the active project.
   - Locate the installed source with `python scripts/find_dayz_source.py --start .`. The helper checks `DAYZ_SOURCE_ROOT`, the workspace and its ancestors, then the standard Windows `P:\` mapping. If those fail, ask for an explicit root and pass it with `--root`.
   - `DAYZ_SOURCE_ROOT` means the directory containing `scripts/1_core`, `scripts/3_game`, and `scripts/4_world`.
   - Treat discovery as read-only. Never modify the installed vanilla source unless the user explicitly places it in edit scope.
   - Inspect the relevant mod directory before proposing edits. Search its `config.cpp`, script modules, and existing conventions.
   - Determine whether the task asks for explanation, diagnosis, review, or an implementation. Only write project files when the request authorizes changes.

2. Detect the framework and script layer.
   - Inspect `requiredAddons[]`, `CfgMods`, imports, and existing symbols.
   - Treat `JM_CF_Scripts` or `GetRPCManager()` as Community Framework evidence.
   - Treat `DayZExpansion_*`, `Expansion*`, or `eAI*` dependencies as Expansion evidence.
   - Identify whether a symbol belongs to `1_Core`, `2_GameLib`, `3_Game`, `4_World`, or `5_Mission`. Respect that dependency direction when adding code.

3. Verify exact APIs locally before using them.
   - Search the discovered `<DAYZ_SOURCE_ROOT>/scripts` with `rg` for declarations, overrides, and representative call sites.
   - Start with an exact, file-limited query such as `rg -n -m 50 'class RestContext|RestContext\\(' <scripts-root>` or `rg -l -m 50 'ExactSymbol' <scripts-root>`. Narrow by script module or filename before broadening.
   - Read bounded source windows around matches. Do not dump entire large files or unbounded search results into context.
   - Prefer exact class definitions and method signatures over summaries. Inspect parameter types, return types, inheritance, access level, and script module.
   - If a class, method, config token, or parameter cannot be verified, do not invent it. State the uncertainty and continue to an authoritative source.

4. Load only the relevant bundled references from the map below.
   - Treat these files as a curated snapshot, not as proof of the installed game version.
   - The 1.28 guide is historical compatibility material. Never let it override newer installed source or current documentation.

5. Browse when local evidence is insufficient or freshness matters.
   - Prefer the official DayZ Script Diff and Bohemia repositories for exact source and configuration data.
   - Use the generated DayZ Scripts API as a navigation and cross-checking aid.
   - Use the official CF and Expansion repositories for their framework APIs.
   - Verify current versions at response time; do not assume the version named in a bundled reference is current.
   - Cite the pages used and distinguish documented facts from inference.

6. Answer or edit with project evidence.
   - Match the existing mod's structure and naming.
   - After edits, inspect the diff and run relevant static checks available in the project.
   - This skill contains no DayZ Tools or PBO build automation. Do not invoke packaging or compilation as part of this workflow.

## Source precedence

Use this order when sources disagree:

1. The active mod's source and configuration for its intended behavior.
2. The discovered local `scripts` tree for installed vanilla APIs and signatures.
3. Official current DayZ, CF, or Expansion source repositories.
4. Generated API documentation and official wikis.
5. Bundled references for established patterns and historical context.
6. Community documentation only when primary sources are silent; label it accordingly.

## Correctness rules

- Write Enforce Script, not C#, C++, Java, or Lua. Avoid unsupported language features and syntax.
- Verify every nontrivial class, method, override signature, enum, and config token before presenting it as valid.
- Null-check potentially absent values before dereferencing them, including cast results, players, identities, inventories, and objects returned during initialization or teardown.
- Keep gameplay authority and validation on the server. Validate RPC payloads and sender identity before mutating state.
- Distinguish dedicated-server, server, client, and single-player execution. Do not assume `IsClient()` is reliable during every initialization phase.
- Do not add an explicit parent class to a `modded class`; it already extends the existing class.
- Preserve the correct script module and call `super` where the local base implementation requires it.
- Do not apply performance advice such as using `g_Game` unless the installed source supports it and the code path benefits.
- Avoid unrelated rewrites when editing an existing mod.

## Reference map

### Scripting

- Read [Enforce Script](references/scripting/enforce-script.md) for language syntax and common patterns.
- Read [Class hierarchy](references/scripting/class-hierarchy.md) for major types and singletons.
- Read [Client and server](references/scripting/client-server.md) for modules and execution context.
- Read [Memory management](references/scripting/memory-management.md) for `ref`, `autoptr`, `Managed`, and lifecycle behavior.

### Systems

- Read [Mod structure](references/systems/mod-structure.md) for folders, script registration, and PBO-oriented layout concepts.
- Read [Networking](references/systems/networking.md) for RPC and synchronized variables.
- Read [Inventory](references/systems/inventory.md) for item creation, movement, and inventory locations.
- Read [Actions](references/systems/actions.md) for custom interaction actions.
- Read [Weapons](references/systems/weapons.md) for weapon configuration and FSM concepts.
- Read [Vehicles](references/systems/vehicles.md) for vehicle configuration, physics, and version-sensitive behavior.

### Frameworks and configuration

- Read [Framework detection](references/frameworks/framework-detection.md) before choosing vanilla, CF, or Expansion patterns.
- Read [Community Framework](references/frameworks/community-framework.md) for CF modules, RPC, and storage patterns.
- Read [Expansion](references/frameworks/expansion.md) for Expansion systems and integration points.
- Read [config.cpp](references/config/config-cpp.md) for addon and entity configuration patterns.
- Read [Central Economy XML](references/config/types-xml.md) for loot and spawn configuration.
- Read [Server configuration](references/config/server-config.md) for `serverDZ.cfg` and gameplay settings.
- Read [DayZ 1.28 compatibility](references/compatibility/version-128.md) only for 1.28 behavior or migration history.

## Authoritative online sources

- Installed vanilla source: resolve with `python scripts/find_dayz_source.py --start .`
- DayZ Script Diff: `https://github.com/BohemiaInteractive/DayZ-Script-Diff`
- DayZ Scripts API: `https://dayz-scripts.yadz.app/`
- Enforce Script syntax: `https://community.bistudio.com/wiki/DayZ:Enforce_Script_Syntax`
- Central Economy: `https://github.com/BohemiaInteractive/DayZ-Central-Economy`
- Community Framework: `https://github.com/Arkensor/DayZ-CommunityFramework`
- DayZ Expansion Scripts: `https://github.com/salutesh/DayZ-Expansion-Scripts`

## Completion checks

Before finalizing DayZ code or configuration:

- Confirm the referenced API exists in the intended source/version.
- Confirm the override signature and script module.
- Confirm nullable values and server/client boundaries are handled.
- Confirm framework dependencies match `config.cpp`.
- Separate verified facts from suggestions, and mention any verification gap plainly.
