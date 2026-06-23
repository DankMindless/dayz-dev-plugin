# DayZ 1.28 Compatibility Guide

> **Released:** June 3, 2025 (PC Stable 1.28.159992)
> **Script Version:** v1.28.161464

## CRITICAL Breaking Changes

### 1. Vehicle Brake Values Must Be Doubled
**Impact:** All vehicle mods

The engine now applies brake force once instead of twice internally. You must **double** all brake-related config values.

```cpp
// BEFORE (1.27)
maxBrakeTorque = 2000;
maxHandbrakeTorque = 1600;
brakeForce = 2000;

// AFTER (1.28) - Double all values
maxBrakeTorque = 4000;
maxHandbrakeTorque = 3200;
brakeForce = 4000;
```

### 2. Contact Class API Overhaul
**Impact:** Any mod using physics contacts (EOnContact, collision handling)

| Removed | Added |
|---------|-------|
| `Contact.MaterialIndex1` | `Contact.ShapeIndex1` |
| `Contact.MaterialIndex2` | `Contact.ShapeIndex2` |
| `Contact.Index1` | `Contact.VelocityBefore1` |
| `Contact.Index2` | `Contact.VelocityBefore2` |
| | `Contact.VelocityAfter1` |
| | `Contact.VelocityAfter2` |

`Contact.Material1` and `Contact.Material2` changed from type `dMaterial` to `SurfaceProperties`.

```c
// BEFORE (1.27)
override void EOnContact(IEntity other, Contact extra)
{
    dMaterial mat = extra.Material1;
    int idx = extra.MaterialIndex1;
}

// AFTER (1.28)
override void EOnContact(IEntity other, Contact extra)
{
    SurfaceProperties surf = extra.Material1;
    int shapeIdx = extra.ShapeIndex1;
    vector velBefore = extra.VelocityBefore1;
    vector velAfter = extra.VelocityAfter1;
}
```

### 3. PhysicsGeomDef.MaterialName Format Change
**Impact:** Mods defining custom physics geometry

```c
// BEFORE (1.27)
geomDef.MaterialName = "concrete";

// AFTER (1.28) - Use .bisurf path or CfgSurfaces reference
geomDef.MaterialName = "DZ/data/data/penetration.bisurf";
// Or
geomDef.MaterialName = "#cp_concrete1";
```

### 4. Script Method 16-Parameter Limit
**Impact:** Mods with methods exceeding 16 parameters

The compiler now throws an error. Previously this caused silent buffer overflows and random crashes.

```c
// WILL NOT COMPILE in 1.28
void TooManyParams(int a, int b, int c, int d, int e, int f, int g, int h,
                   int i, int j, int k, int l, int m, int n, int o, int p,
                   int q)  // 17th param = COMPILE ERROR
{
}

// FIX: Use a params object
class MyParams
{
    int a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q;
}

void FixedParams(MyParams params) { }
```

### 5. useNewNetworking Default
**Impact:** Vehicle mods with custom physics

New config parameter defaults to `1`. Mods modifying vehicle physics outside `SimulationModule` may need:

```cpp
class SimulationModule
{
    useNewNetworking = 0;  // Disable for custom physics
};
```

## Important Changes (Should Address)

### 6. CGame.OnPostUpdate Timing
**Impact:** UI mods using GetScreenPos

`CGame.OnPostUpdate` now fires **after** camera update. `CGame.GetScreenPos` now returns correct positions. Remove any workarounds for the old behavior.

### 7. SoundObject.SetParent Signature
**Impact:** Sound mods

Now accepts a pivot index for animated component attachment:
```c
// NEW: Optional pivot index parameter
soundObj.SetParent(entity, pivotIndex);
```

### 8. sealed Keyword
**Impact:** Mods inheriting from vanilla classes

If a vanilla class is now marked `sealed`, you cannot inherit from it. Check for compile errors after updating.

### 9. Obsolete Attribute
**Impact:** Mods using deprecated functions

Functions/classes marked `[Obsolete]` may generate warnings. Plan migration to alternatives.

### 10. Horticulture Storage
**Impact:** Modded servers

Changes to plant systems may corrupt saved horticulture data. **Storage wipe recommended for modded servers** (delete `storage_1` folder).

### 11. Vanilla CTD Workarounds
**Impact:** All mods

Two vanilla bugs that can crash mods:
- `ProcessDirectDamage` with static damage source (T192088) - avoid static `EntityAI` as source
- Setting fog in custom intro scenes (T192270) - don't call fog functions in intro

## New Features

### New Script Keywords
- **`sealed`** - Prevent inheritance/override
- **`Obsolete`** - Mark deprecated code

```c
sealed class FinalClass { }      // Cannot be inherited
// class Bad : FinalClass { }    // COMPILE ERROR

class MyClass
{
    [Obsolete]
    void OldMethod() { }         // Generates deprecation warning
    void NewMethod() { }
}
```

### New Script Functions
```c
// Animation source queries
int count = entity.GetNumUserAnimationSourceNames();
string name = entity.GetUserAnimationSourceName(0);

// Base position without animation
vector basePos = object.GetSelectionBasePositionLS("selection_name");
```

### New Vehicle Config Parameters
```cpp
wheelHubFriction = 0.1;     // Axle drag without wheels (NEW)
useNewNetworking = 1;         // Reforger-based vehicle networking (NEW, default: 1)
```

### Enhanced spawnabletypes.xml
- `quantmin`/`quantmax` attributes (0-100%)
- Nested item cargo and attachments
- Nested damage min/max
- Nested presets via `equip="true"`
- Weapons spawn with chambered bullets
- `randompresets.xml` appendable via `cfgeconomycore.xml`

### Workbench Enhancements
- Alt+Up/Down for line movement
- Split view for dual file editing
- Ctrl+Shift+T to reopen closed tabs
- Debugger watch search bar
- Breakpoint management improvements
- Context menu: "Overrides"/"Base Classes"/"Derived Classes"

## Performance Recommendations

```c
// Use g_Game instead of GetGame() in hot paths
// BEFORE
void OnUpdate(float dt)
{
    if (GetGame().IsServer())  // Function call overhead each frame
    {
        GetGame().GetWorld().GetPlayerList(players);
    }
}

// AFTER (1.28+ recommended)
void OnUpdate(float dt)
{
    if (g_Game.IsServer())     // Direct variable access
    {
        g_Game.GetWorld().GetPlayerList(players);
    }
}
```

## Framework Compatibility

| Framework | Minimum Version | Key Changes |
|-----------|----------------|-------------|
| Community Framework | 1.5.7 | ModStorage simplified, 1.28 compat |
| Expansion Core | 1.9.28 | Animation graph updated, CTD workarounds |
| Expansion Scripts | 1.9.28+ | ProcessDirectDamage workaround, fog fix |

## Migration Checklist

```
[ ] Update vehicle brake torque values (double all)
[ ] Update Contact class usage (new API)
[ ] Update PhysicsGeomDef.MaterialName format
[ ] Check for methods with 16+ params (refactor)
[ ] Test with useNewNetworking = 1
[ ] Check for sealed class compile errors
[ ] Check for Obsolete warnings
[ ] Update CF to 1.5.7+
[ ] Update Expansion to 1.9.28+
[ ] Replace GetGame() with g_Game in hot paths
[ ] Test ProcessDirectDamage usage (avoid static source)
[ ] Recommend storage wipe for modded servers
```
