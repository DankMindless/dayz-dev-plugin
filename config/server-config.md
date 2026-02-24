# DayZ Server Configuration

## Configuration Files Overview

| File | Location | Purpose |
|------|----------|---------|
| `serverDZ.cfg` | Server root | Main server settings |
| `cfgGameplay.json` | Mission folder | Gameplay behavior |
| `types.xml` | `db/` folder | Item spawning |
| `events.xml` | `db/` folder | Dynamic events |
| `cfgspawnabletypes.xml` | `db/` folder | Item spawn attachments |
| `cfgeconomycore.xml` | `db/` folder | Economy file loading |
| `globals.xml` | `db/` folder | Global CE variables |
| `cfgenvironment.xml` | `db/` folder | Environment zones |
| `cfgweather.xml` | `db/` folder | Weather configuration |
| `cfgplayerspawnpoints.xml` | `db/` folder | Player spawn locations |

## serverDZ.cfg Key Parameters

```
hostname = "My DayZ Server";
password = "";                        // Server password
passwordAdmin = "adminpassword";      // Admin password
maxPlayers = 60;
verifySignatures = 2;                 // 0=off, 1=warn, 2=kick
forceSameBuild = 1;                   // Require same game version
disableVoN = 0;                       // Voice over network
vonCodecQuality = 20;                 // VoN quality (0-30)
disable3rdPerson = 0;                 // 0=allow, 1=first person only
disableCrosshair = 0;                 // 0=show, 1=hide
serverTime = "2020/4/1/08/00";       // Initial date/time
serverTimeAcceleration = 4;           // Time multiplier
serverNightTimeAcceleration = 8;      // Night speed multiplier
serverTimePersistent = 0;             // Save server time
guaranteedUpdates = 1;                // Guaranteed network updates
loginQueueConcurrentPlayers = 5;      // Concurrent login slots
loginQueueMaxPlayers = 500;           // Max login queue
instanceId = 1;                       // Server instance ID
lootHistory = 1;                      // Track loot history
storeHouseStateDisabled = false;      // Save building states
storageAutoFix = 1;                   // Auto-fix corrupt storage
respawnTime = 5;                      // Respawn timer (seconds)

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus"; // or "dayzOffline.enoch" for Livonia, "dayzOffline.sakhal" for Sakhal
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
            "staminaKgToStaminaPercentPenalty": 1.75,
            "staminaMinCap": 5,
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
        "canCraftAnywhere": false
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

```xml
<variables>
    <var name="AnimalMaxCount" type="0" value="200"/>
    <var name="CleanupAvoidance" type="0" value="100"/>
    <var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>
    <var name="CleanupLifetimeDeadInfected" type="0" value="330"/>
    <var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>
    <var name="CleanupLifetimeDefault" type="0" value="45"/>
    <var name="CleanupLifetimeLimit" type="0" value="1200"/>
    <var name="CleanupLifetimeRuined" type="0" value="330"/>
    <var name="FlagRefreshFrequency" type="0" value="432000"/>
    <var name="FlagRefreshMaxDuration" type="0" value="3456000"/>
    <var name="IdleModeCountdown" type="0" value="60"/>
    <var name="IdleModeStartup" type="0" value="1"/>
    <var name="InitialSpawn" type="0" value="1200"/>
    <var name="RespawnAttempt" type="0" value="24"/>
    <var name="RespawnLimit" type="0" value="120"/>
    <var name="RespawnTypes" type="0" value="12"/>
    <var name="RestartSpawn" type="0" value="0"/>
    <var name="SpawnInitial" type="0" value="1200"/>
    <var name="TimeHopping" type="0" value="60"/>
    <var name="TimeLogin" type="0" value="15"/>
    <var name="TimeLogout" type="0" value="15"/>
    <var name="TimePenalty" type="0" value="20"/>
    <var name="ZombieMaxCount" type="0" value="1000"/>
    <var name="ZoneSpawnDist" type="0" value="300"/>
    <var name="WorldWetTempUpdate" type="0" value="1"/>
</variables>
```

## File Locations

```
ServerRoot/
├── serverDZ.cfg
├── battleye/
│   └── beserver_x64.cfg
├── mpmissions/
│   └── dayzOffline.chernarusplus/     # or .enoch / .sakhal
│       ├── cfgGameplay.json
│       ├── cfgenvironment.xml
│       ├── cfgweather.xml
│       ├── cfgplayerspawnpoints.xml
│       ├── init.c                     # Mission init script
│       ├── db/
│       │   ├── types.xml
│       │   ├── events.xml
│       │   ├── globals.xml
│       │   ├── cfgspawnabletypes.xml
│       │   ├── cfgeconomycore.xml
│       │   └── randompresets.xml
│       └── storage_1/                 # Persistence data
│           └── data/
└── profiles/
    ├── DayZ*.ADM                      # Admin log
    ├── DayZ*.RPT                      # Script log
    └── DayZ*.log                      # Server log
```

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
