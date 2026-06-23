# DayZ Expansion Framework

> **Steam Workshop:** Multiple modules (Core, Scripts, Market, Quests, AI, etc.)
> **GitHub:** https://github.com/salutesh/DayZ-Expansion-Scripts
> **Wiki:** https://github.com/salutesh/DayZ-Expansion-Scripts/wiki
> **Minimum for 1.28:** Expansion 1.9.28

## Module System

Expansion is split into independent modules:
| Module | Workshop ID | Purpose |
|--------|-------------|---------|
| Core | 2291785308 | Base framework |
| Scripts | 2116151222 | All scripting |
| Market | Included | Trading/economy |
| Quests | Included | Quest system |
| AI | Included | AI patrols/guards |
| Basebuilding | Included | Territory/building |
| Vehicles | Included | Extended vehicles |

## Market System

### Configuration Files
- `ExpansionMarketSettings.json` - Global market settings
- `ExpansionMarketTraders/` - Individual trader configs
- `ExpansionMarketCategories/` - Item category definitions

### Trader Setup
```json
// ExpansionMarketTraders/MyTrader.json
{
    "TraderName": "General Store",
    "TraderIcon": "Deliver",
    "Currencies": ["ExpansionMoneyDollar"],
    "Items": [
        {
            "ClassName": "BandageDressing",
            "MaxPriceThreshold": 50,
            "MinPriceThreshold": 10,
            "SellPricePercent": 50,
            "MaxStockThreshold": 100,
            "MinStockThreshold": 1,
            "QuantityPercent": -1,
            "SpawnAttachments": [],
            "Variants": []
        }
    ]
}
```

### Market API
```c
// Get market module
ExpansionMarketModule marketModule = ExpansionMarketModule.Cast(
    CF_ModuleCoreManager.Get(ExpansionMarketModule));

// Check item price
int buyPrice = marketModule.GetBuyPrice("BandageDressing");
int sellPrice = marketModule.GetSellPrice("BandageDressing");

// Player money (via Expansion banking)
int balance = player.GetMoney();
```

## Quest System

### Quest Types
| Objective Type | Description |
|---------------|-------------|
| `TRAVEL` | Go to location |
| `COLLECT` | Collect items |
| `DELIVERY` | Deliver items to NPC |
| `TARGET` | Kill specific targets |
| `AIPATROL` | Kill AI patrol |
| `AICCAMP` | Clear AI camp |
| `TREASUREHUNT` | Find treasure |
| `ACTION` | Custom scripted action |

### Quest Configuration
```json
// ExpansionQuests/MyQuest.json
{
    "ID": 1001,
    "Title": "Supply Run",
    "Description": "Collect medical supplies",
    "ObjectiveType": "COLLECT",
    "Objectives": [
        {
            "ClassName": "BandageDressing",
            "Amount": 5
        }
    ],
    "Rewards": [
        {
            "ClassName": "ExpansionMoneyDollar",
            "Amount": 100
        }
    ],
    "PreQuest": -1,
    "Repeatable": true,
    "CooldownTime": 3600
}
```

### Quest Implementation (3 Phases)
1. **Define objectives** in JSON config
2. **Create NPC** with quest giver settings
3. **Register quest** in ExpansionQuestSettings.json

## AI System

### AI Patrol Setup
```json
// ExpansionAIPatrols/MyPatrol.json
{
    "Name": "Military Patrol",
    "Faction": "East",
    "LoadoutFile": "MilitaryLoadout",
    "NumberOfAI": 4,
    "Waypoints": [
        {"Position": [3456.7, 0, 8901.2]},
        {"Position": [3500.0, 0, 8950.0]},
        {"Position": [3450.0, 0, 9000.0]}
    ],
    "Behaviour": "PATROL",
    "Speed": "JOG",
    "RespawnTime": 1800,
    "DespawnTime": 300
}
```

### AI Settings
```json
// ExpansionAISettings.json
{
    "Enabled": true,
    "MaxRecruitableAI": 5,       // NEW in 1.9.41
    "LootDropOnDeath": true,
    "AccuracyMin": 0.3,
    "AccuracyMax": 0.7,
    "ThreatRange": 150
}
```

### AI FSM Behaviors
| Behavior | Description |
|----------|-------------|
| `PATROL` | Walk between waypoints |
| `GUARD` | Guard a position |
| `FOLLOW` | Follow a target |
| `IDLE` | Stand in place |

## Basebuilding / Territory

### Territory Setup
```json
// ExpansionTerritorySettings.json
{
    "Enabled": true,
    "TerritorySize": 150,
    "MaxMembersPerTerritory": 10,
    "MaxTerritoriesPerPlayer": 1,
    "EnableCodeLocks": true,
    "EnableFlagMenu": true
}
```

### Building Kits
- Territory Flag Kit (establishes territory)
- Wooden Floor/Wall/Roof Kits
- Metal variants for upgrades
- Code Lock Kit (security)

## Vehicle Extensions

Expansion adds helicopters, boats, bikes, and more with custom physics.

### Key Settings
```json
// ExpansionVehicleSettings.json
{
    "VehicleSyncRate": 10,
    "OverrideClientWeaponFiring": false,    // NEW in 1.9.48
    "RecreateWeaponNetworkRepresentation": false  // NEW in 1.9.48
}
```

## Persistence Pattern (3-Phase)

All Expansion data follows this save/load pattern:

```c
// Phase 1: OnStoreSave (server shutdown/autosave)
override void OnStoreSave(ParamsWriteContext ctx)
{
    super.OnStoreSave(ctx);
    ctx.Write(m_Data);
}

// Phase 2: OnStoreLoad (server startup)
override bool OnStoreLoad(ParamsReadContext ctx, int version)
{
    if (!super.OnStoreLoad(ctx, version)) return false;
    if (!ctx.Read(m_Data)) return false;
    return true;
}

// Phase 3: AfterStoreLoad (post-load initialization)
override void AfterStoreLoad()
{
    super.AfterStoreLoad();
    // Rebuild runtime state from loaded data
}
```

## 1.28 Expansion Notes

- **1.9.28**: Animation graph updated, CTD workarounds for `ProcessDirectDamage` and fog settings
- **1.9.30**: Dynamic physics disabled for items on contact (vanilla bug T192415)
- **1.9.47**: `GetGame()` replaced with `g_Game` across all mods
- **1.9.48**: `SurfaceRoadY(3D)` replaced with `GetSurface` NoWait for performance

### Known Issues
- Vehicle winching doesn't work properly
- Vehicle restore/uncover while standing on it may cause fall-through
