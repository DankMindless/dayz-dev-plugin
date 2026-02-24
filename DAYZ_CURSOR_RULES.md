# DayZ Enforce Script Development Rules

> For Cursor, Windsurf, and other AI coding assistants.
> Target: DayZ 1.28+ (v1.28.161464)

## Language: Enforce Script

DayZ uses **Enforce Script**, a C-like language. Key differences from C/C#/C++:
- No namespaces, no exceptions (try/catch), no operator overloading
- Single inheritance only, `modded class` for injection
- `ref` keyword for member variables only (NOT function params)
- Garbage collected with optional reference counting via `Managed`
- `autoptr` for scope-based cleanup
- Built-in `vector` type (3x float), `array<T>`, `set<T>`, `map<K,V>`

## Critical Rules

### NEVER DO
- Use C# syntax (`player.GetComponent<>()`, `using`, `namespace`)
- Use C++ syntax (`std::`, `template<>`, `nullptr`)
- Invent class names or methods that don't exist
- Use `ref` in function parameters, returns, or local variables
- Add `: ParentClass` inheritance to `modded class` (already inherits)
- Use `delete` keyword (null the reference instead; `delete` can segfault)
- Trust `GetGame().IsClient()` during init (returns FALSE)
- Skip null checks on `Cast<>`, `GetInventory()`, `GetIdentity()`
- Leave empty `#ifdef`/`#endif` blocks (causes segfaults)
- Write files outside `$saves:` or `$profile:` directories
- Create methods with more than 16 parameters
- Compare against `int.MIN` (`1 < int.MIN` returns TRUE - known bug)

### ALWAYS DO
- Use `!GetGame().IsDedicatedServer()` for client checks during init
- Null-check every `Cast<>` result before use
- Call `super.Method()` in overrides
- Use `SetSynchDirty()` after changing NetSync variables
- Check `GetGame().IsServer()` before gameplay logic
- Parenthesize bitwise operations: `(flags & FLAG) == FLAG`
- Assign getter results to local var before `foreach`
- Use `g_Game` instead of `GetGame()` in performance-critical code

## Mod Structure
```
@MyMod/Addons/MyMod/
├── config.cpp              # CfgPatches, CfgMods, CfgVehicles
├── $PREFIX$                # Addon prefix
├── scripts/
│   ├── config.cpp          # Script module registration
│   ├── 3_Game/             # Available everywhere
│   ├── 4_World/            # Entities, items, actions
│   └── 5_Mission/          # HUD, menus, mission logic
└── data/                   # Models, textures
```

## Script Module Access
- `5_Mission` can access `4_World` and `3_Game`
- `4_World` can access `3_Game`
- `3_Game` cannot access `4_World` or `5_Mission`

## Common Patterns

### Modded Class
```c
modded class PlayerBase
{
    override void SetActions(out TInputActionMap InputActionMap)
    {
        super.SetActions(InputActionMap);
        AddAction(MyAction, InputActionMap);
    }
}
```

### RPC (Vanilla)
```c
ScriptRPC rpc = new ScriptRPC();
rpc.Write(data);
rpc.Send(target, ERPCs.RPC_USER_ACTION_MESSAGE, true, identity);
```

### RPC (CF)
```c
GetRPCManager().AddRPC("MyMod", "MyHandler", this, SingleplayerExecutionType.Both);
GetRPCManager().SendRPC("MyMod", "MyHandler", new Param1<string>("data"), true, identity);
```

### Net Sync
```c
RegisterNetSyncVariableInt("m_Var", 0, 100);
// After changing: SetSynchDirty();
// Client receives: OnVariablesSynchronized()
```

### Null-Safe Item Creation
```c
PlayerBase player = PlayerBase.Cast(GetGame().GetPlayer());
if (player && player.GetInventory())
{
    EntityAI item = player.GetInventory().CreateInInventory("AKM");
    if (item)
    {
        item.SetHealth("", "", 100);
    }
}
```

## Documentation Sources
- Script API (v1.28): https://dayz-scripts.yadz.app/
- Script Diff: https://github.com/BohemiaInteractive/DayZ-Script-Diff
- BI Wiki: https://community.bistudio.com/wiki/DayZ:Enforce_Script_Syntax
- CF Docs: https://github.com/Arkensor/DayZ-CommunityFramework
- Expansion Wiki: https://github.com/salutesh/DayZ-Expansion-Scripts/wiki
- Server Config: https://dzconfig.com/wiki/

## 1.28 Breaking Changes
1. Vehicle brake values must be doubled
2. Contact class: `dMaterial` -> `SurfaceProperties`, removed MaterialIndex/Index
3. `PhysicsGeomDef.MaterialName` now takes .bisurf or #CfgSurfaces
4. 16-parameter method limit enforced
5. `sealed` keyword prevents inheritance
6. Storage wipe recommended for modded servers (horticulture)
