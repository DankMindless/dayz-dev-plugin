# DayZ Server Configuration

## Configuration Files Overview

| File | Location | Purpose |
|------|----------|---------|
| `serverDZ.cfg` | Server root | Main server settings (name, ports, passwords, time) |
| `economy.xml` | Mission folder | Master CE entry point, entity persistence flags |
| `cfgGameplay.json` | Mission folder | Gameplay behavior (stamina, building, UI) |
| `cfgenvironment.xml` | Mission folder | Animal territories, zombie spawn zones |
| `cfgweather.xml` | Mission folder | Weather patterns (rain, fog, wind, storms) |
| `cfgplayerspawnpoints.xml` | Mission folder | Player spawn locations and safety distances |
| `cfgEffectArea.json` | Mission folder | Contaminated zones and effect areas |
| `types.xml` | `db/` folder | Item spawning (nominal, lifetime, flags) |
| `events.xml` | `db/` folder | Dynamic events (helicrashes, wrecks) |
| `globals.xml` | `db/` folder | Global CE variables (cleanup, counts) |
| `cfgspawnabletypes.xml` | `db/` folder | Item spawn attachments and cargo |
| `cfgeconomycore.xml` | `db/` folder | CE logging, dynamic event settings |
| `cfgrandompresets.xml` | `db/` folder | Grouped item spawn presets |
| `cfglimitsdefinition.xml` | `db/` folder | Category/usage/value tag definitions |
| `cfgIgnoreList.xml` | `db/` folder | Items exempt from CE cleanup |
| `cfgeventspawns.xml` | `db/` folder | Event spawn coordinates |
| `messages.xml` | `db/` folder | Server messages and MOTD |

## serverDZ.cfg Key Parameters

```
// === Basic Settings ===
hostname = "My DayZ Server";
password = "";                        // Server password (empty = public)
passwordAdmin = "adminpassword";      // Admin/RCON password
maxPlayers = 60;                      // Max concurrent players (40-60 standard, 80-100 high-end)
respawnTime = 5;                      // Seconds before respawn available after death

// === Network Ports ===
port = 2302;                          // Main game port
steamQueryPort = 2303;                // Steam server browser query port
steamPort = 2304;                     // Steam authentication/VAC port

// === Security ===
BattlEye = 1;                         // 0=off, 1=on (strongly recommended)
verifySignatures = 2;                 // 0=off, 1=relaxed, 2=full (recommended)
forceSameBuild = 1;                   // Require same game version

// === Gameplay ===
disableVoN = 0;                       // 0=enabled, 1=disabled
vonCodecQuality = 20;                 // VoN quality (0-30)
disable3rdPerson = 0;                 // 0=allow 3PP, 1=first person only
disableCrosshair = 0;                 // 0=show, 1=hide

// === Time ===
serverTime = "2020/4/1/08/00";       // Initial time: "YYYY/MM/DD/HH/MM" or "SystemTime"
serverTimeAcceleration = 1;           // Daytime speed multiplier (1=realtime, default: 1)
serverNightTimeAcceleration = 4;      // Night speed multiplier (default: 4)
serverTimePersistent = 0;             // 1=save/restore time across restarts

// === Queue & Login ===
guaranteedUpdates = 1;                // Guaranteed network updates
loginQueueConcurrentPlayers = 5;      // Concurrent login slots
loginQueueMaxPlayers = 500;           // Max login queue

// === Persistence & Economy ===
instanceId = 1;                       // Server instance ID
lootHistory = 1;                      // Track loot history
storeHouseStateDisabled = false;      // Save building states
storageAutoFix = 1;                   // Auto-fix corrupt storage

// === Mission ===
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
        // "dayzOffline.enoch" for Livonia
        // "dayzOffline.sakhal" for Sakhal
    };
};
```

## cfgGameplay.json

```json
{
    "version": 124,
    "GeneralData": {
        "disableBaseDamage": false,
        "disableContainerDamage": false,
        "disableRespawnDialog": false,
        "disableRespawnInUnconsciousness": false
    },
    "PlayerData": {
        "disablePersonalLight": false,
        "StaminaData": {
            "staminaMax": 100,
            "staminaMinCap": 5,
            "staminaWeightLimitThreshold": 6000,
            "staminaKgToStaminaPercentPenalty": 1.75,
            "sprintStaminaModifierErc": 1,
            "sprintStaminaModifierCro": 1
        },
        "ShockHandlingData": {
            "shockRefillSpeedConscious": 5,
            "shockRefillSpeedUnconscious": 1,
            "allowRefillSpeedModifier": true
        }
    },
    "WorldData": {
        "lightingConfig": 0,
        "objectSpawnersArr": [],
        "environmentMinTemps": [-3, -2, 0, 4, 9, 14, 18, 17, 12, 7, 4, 0],
        "environmentMaxTemps": [3, 5, 7, 14, 19, 24, 26, 25, 21, 16, 10, 5],
        "wetnessWeightModifiers": [1, 1, 1.5, 2]
    },
    "BaseBuildingData": {
        "canBuildAnywhere": false,
        "canCraftAnywhere": false,
        "HologramData": {
            "disableIsCollidingBBoxCheck": false,
            "disableIsCollidingPlayerCheck": false,
            "disableHeightPlacementCheck": false,
            "disableIsInTerrainCheck": false,
            "disableIsUnderwaterCheck": false,
            "disableIsCollidingAngleCheck": false
        }
    },
    "UIData": {
        "use3DMap": false,
        "HitIndicationData": {
            "hitDirectionOverrideEnabled": false,
            "hitDirectionBehaviour": 1,
            "hitDirectionStyle": 0,
            "hitDirectionIndicatorColorStr": "0xffff0000",
            "hitDirectionMaxDuration": 2,
            "hitDirectionBreakPointRelative": 0.2,
            "hitDirectionScatter": 10,
            "hitIndicationPostProcessEnabled": true
        }
    },
    "MapData": {
        "ignoreMapOwnership": false,
        "ignoreNavItemsOwnership": false,
        "displayPlayerPosition": false,
        "displayNavInfo": true
    }
}
```

## globals.xml (CE Global Variables)

Variable types: `type="0"` = integer, `type="1"` = float.

```xml
<variables>
    <!-- Entity Limits -->
    <var name="AnimalMaxCount" type="0" value="200"/>
    <var name="ZombieMaxCount" type="0" value="1000"/>
    <var name="ZoneSpawnDist" type="0" value="300"/>

    <!-- Cleanup Timers (seconds) -->
    <var name="CleanupAvoidance" type="0" value="100"/>     <!-- Meters: skip cleanup near players -->
    <var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>
    <var name="CleanupLifetimeDeadInfected" type="0" value="330"/>
    <var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>
    <var name="CleanupLifetimeDefault" type="0" value="45"/>
    <var name="CleanupLifetimeLimit" type="0" value="1200"/>
    <var name="CleanupLifetimeRuined" type="0" value="330"/>

    <!-- Loot Spawning -->
    <var name="LootDamageMin" type="1" value="0.0"/>        <!-- Min damage on spawned loot -->
    <var name="LootDamageMax" type="1" value="0.82"/>       <!-- Max damage on spawned loot -->
    <var name="LootSpawnAvoidance" type="0" value="100"/>   <!-- Meters: don't spawn loot near players -->
    <var name="LootProxyPlacement" type="0" value="1"/>     <!-- 1=enable proxy placement system -->

    <!-- Base Building -->
    <var name="FlagRefreshFrequency" type="0" value="432000"/>    <!-- 5 days -->
    <var name="FlagRefreshMaxDuration" type="0" value="3456000"/> <!-- 40 days -->

    <!-- Spawn/Respawn -->
    <var name="SpawnInitial" type="0" value="1200"/>
    <var name="RespawnAttempt" type="0" value="24"/>
    <var name="RespawnLimit" type="0" value="120"/>
    <var name="RespawnTypes" type="0" value="12"/>
    <var name="RestartSpawn" type="0" value="0"/>

    <!-- Login/Logout Timers (seconds) -->
    <var name="TimeLogin" type="0" value="15"/>
    <var name="TimeLogout" type="0" value="15"/>
    <var name="TimeHopping" type="0" value="60"/>      <!-- Server hop cooldown -->
    <var name="TimePenalty" type="0" value="20"/>

    <!-- Server Modes -->
    <var name="IdleModeStartup" type="0" value="1"/>   <!-- 1=start in idle mode -->
    <var name="IdleModeCountdown" type="0" value="60"/>

    <!-- Environment -->
    <var name="FoodDecay" type="0" value="1"/>          <!-- 1=enable food decay -->
    <var name="WorldWetTempUpdate" type="0" value="1"/> <!-- 1=enable wetness/temp updates -->
</variables>
```

**Performance note:** High `ZombieMaxCount` is the primary cause of server lag. Scale entity limits to hardware capacity. Setting `TimeLogin`/`TimeLogout` below 15 seconds enables combat logging exploitation.

## File Locations

```
ServerRoot/
├── serverDZ.cfg
├── battleye/
│   └── beserver_x64.cfg
├── mpmissions/
│   └── dayzOffline.chernarusplus/     # or .enoch / .sakhal
│       ├── cfgGameplay.json
│       ├── cfgEffectArea.json         # Contaminated zones
│       ├── cfgenvironment.xml         # Animal/zombie territories
│       ├── cfgweather.xml
│       ├── cfgplayerspawnpoints.xml
│       ├── economy.xml                # Master CE entry point
│       ├── init.c                     # Mission init script
│       ├── env/                       # Territory definition files
│       │   ├── cattle_territories.xml
│       │   ├── wolf_territories.xml
│       │   ├── bear_territories.xml
│       │   └── zombie_territories.xml
│       ├── db/
│       │   ├── types.xml
│       │   ├── events.xml
│       │   ├── globals.xml
│       │   ├── cfgspawnabletypes.xml
│       │   ├── cfgeconomycore.xml
│       │   ├── cfgrandompresets.xml
│       │   ├── cfglimitsdefinition.xml
│       │   ├── cfgIgnoreList.xml
│       │   ├── cfgeventspawns.xml
│       │   └── messages.xml
│       └── storage_1/                 # Persistence data
│           └── data/
└── profiles/
    ├── DayZ*.ADM                      # Admin log
    ├── DayZ*.RPT                      # Script log
    └── DayZ*.log                      # Server log
```

## economy.xml (Master CE Entry Point)

Controls entity initialization, persistence, and which config files the CE loads:
```xml
<economy>
    <ce folder="db">
        <file name="types.xml" type="types"/>
        <file name="spawnabletypes.xml" type="spawnabletypes"/>
        <file name="globals.xml" type="globals"/>
        <file name="events.xml" type="events"/>
        <file name="messages.xml" type="messages"/>
    </ce>
    <!-- Entity persistence flags: init, load, respawn, save -->
    <classes>
        <class name="dynamic" init="1" load="1" respawn="1" save="1"/>  <!-- Loot -->
        <class name="vehicles" init="1" load="1" respawn="1" save="1"/>
        <class name="building" init="1" load="1" respawn="0" save="1"/> <!-- Player structures -->
        <class name="player" init="1" load="1" respawn="1" save="1"/>
        <class name="animals" init="1" load="0" respawn="1" save="0"/>
        <class name="zombies" init="1" load="0" respawn="1" save="0"/>
        <class name="custom" init="0" load="0" respawn="0" save="0"/>  <!-- Modded content -->
    </classes>
</economy>
```

**Critical:** Player and vehicle entities must keep `save=1` or progress is lost on restart.

## cfgIgnoreList.xml (Cleanup Exemptions)

Items listed here persist indefinitely, surviving their normal lifetime expiration:
```xml
<ignore>
    <item name="Fence"/>
    <item name="Watchtower"/>
    <item name="WoodenCrate"/>
    <item name="SeaChest"/>
    <item name="BarrelHoles_ColorBase"/>
</ignore>
```

**Note:** Items can still be destroyed by damage or players - they simply won't be auto-cleaned by the CE.

## cfgEffectArea.json (Contaminated Zones)

```json
{
    "staticEffectArea": [
        {
            "type": "ContaminatedArea_Static",
            "position": [7500, 0, 7500],
            "radius": 200,
            "duration": -1,
            "outerRingToggle": 1,
            "outerRingDist": 50
        }
    ],
    "dynamicEffectArea": [
        {
            "type": "ContaminatedArea_Dynamic",
            "spawnChance": 0.5,
            "respawnTime": 3600
        }
    ]
}
```

## messages.xml (Server Messages)

```xml
<messages>
    <message type="welcome" delay="5">
        Welcome to our DayZ server! Check our Discord.
    </message>
    <message type="periodic" interval="1800">
        Server restarts every 4 hours.
    </message>
</messages>
```

Message types: `welcome` (shown once on connect), `periodic` (broadcast at interval), `event` (triggered by game events).

## Admin Commands

Execute via in-game chat (requires admin login):
```
#login adminpassword     - Login as admin
#logout                  - Logout from admin
#mission filename        - Load mission
#missions                - List missions
#restart                 - Restart server
#shutdown                - Shut down server
#kick playername         - Kick player
#ban playername          - Ban player
```

## Dynamic Fetching Sources
- **serverDZ.cfg reference**: https://dzconfig.com/wiki/serverdz
- **cfgGameplay.json reference**: https://dzconfig.com/wiki/cfggameplay
- **Gameplay Settings wiki**: https://community.bistudio.com/wiki/DayZ:Gameplay_Settings
- **Server Configuration wiki**: https://community.bistudio.com/wiki/DayZ:Server_Configuration
