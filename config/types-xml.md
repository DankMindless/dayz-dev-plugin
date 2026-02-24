# Central Economy - types.xml & Spawn System

## types.xml Reference

```xml
<type name="ItemClassName">
    <nominal>10</nominal>          <!-- Target count on map -->
    <lifetime>14400</lifetime>     <!-- Seconds before cleanup (0 = infinite) -->
    <restock>1800</restock>        <!-- Seconds between restock checks -->
    <min>5</min>                   <!-- Minimum count before restock -->
    <quantmin>-1</quantmin>        <!-- Min quantity (-1 = default) -->
    <quantmax>-1</quantmax>        <!-- Max quantity (-1 = default) -->
    <cost>100</cost>               <!-- Priority cost (higher = rarer) -->
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
    <category name="tools"/>       <!-- Spawn category -->
    <usage name="Town"/>           <!-- Where it spawns (Town, Village, Military, etc.) -->
    <usage name="Village"/>
    <value name="Tier1"/>          <!-- Tier restriction (Tier1-4) -->
    <value name="Tier2"/>
    <tag name="shelves"/>          <!-- Spawn position tags -->
</type>
```

## Key Parameters

| Parameter | Description | Range |
|-----------|-------------|-------|
| `nominal` | Target count on map | 0-9999 |
| `lifetime` | Seconds before despawn | 0 = never |
| `restock` | Seconds between restocks | 0 = instant |
| `min` | Minimum before restock triggers | 0-nominal |
| `quantmin` | Min quantity % | -1 (default), 0-100 |
| `quantmax` | Max quantity % | -1 (default), 0-100 |
| `cost` | Spawn priority (higher = rarer) | 0-999 |

## Flags

| Flag | Description |
|------|-------------|
| `count_in_cargo` | Count items inside containers |
| `count_in_hoarder` | Count items in player storage |
| `count_in_map` | Count items on ground/buildings |
| `count_in_player` | Count items in player inventory |
| `crafted` | Is a crafted item |
| `deloot` | Dynamic event loot (helicrash etc.) |

## Usage Tags (Where Items Spawn)

| Tag | Description |
|-----|-------------|
| `Town` | Town buildings |
| `Village` | Village buildings |
| `Military` | Military buildings |
| `Farm` | Farm buildings |
| `Industrial` | Industrial buildings |
| `Coast` | Coastal areas |
| `Hunting` | Hunting areas |
| `Medical` | Medical facilities |
| `Police` | Police stations |
| `School` | Schools |
| `Firefighter` | Fire stations |
| `Prison` | Prison areas |
| `Office` | Office buildings |
| `ContaminatedArea` | Contaminated zones |
| `Lunapark` | Amusement areas |

## Value Tags (Tier Restrictions)

| Tag | Description |
|-----|-------------|
| `Tier1` | Coastal/starting areas |
| `Tier2` | Inland areas |
| `Tier3` | Northwest/military areas |
| `Tier4` | High-value areas |

## cfgspawnabletypes.xml (1.28 Enhanced)

### Basic Spawn Configuration
```xml
<type name="AKM">
    <attachments chance="0.3">
        <item name="AK_WoodBttstck" chance="0.8"/>
        <item name="AK_PlasticBttstck" chance="0.2"/>
    </attachments>
    <cargo chance="0.5">
        <item name="Mag_AKM_30Rnd" chance="1.0"/>
    </cargo>
</type>
```

### NEW in 1.28 - Enhanced Spawn Features

```xml
<!-- Nested item cargo and attachments -->
<type name="AKM">
    <attachments chance="0.5">
        <item name="AK_Suppressor" chance="0.1"/>
        <item name="PSO1Optic" chance="0.2"/>
    </attachments>
    <cargo chance="0.7">
        <!-- Item with quantity range (NEW in 1.28) -->
        <item name="Mag_AKM_30Rnd" chance="1.0" quantmin="20" quantmax="80"/>
    </cargo>
</type>

<!-- Nested damage values (NEW in 1.28) -->
<type name="Weapon_Example">
    <cargo chance="1.0">
        <item name="Mag_Example" chance="1.0" damagemin="0.1" damagemax="0.5"/>
    </cargo>
</type>

<!-- Nested presets (NEW in 1.28) -->
<type name="SurvivorM_Hassan">
    <cargo equip="true">
        <item name="RandomPresetName" chance="1.0"/>
    </cargo>
</type>

<!-- Weapons with chambered bullets (NEW in 1.28) -->
<type name="AKM">
    <cargo chance="0.5">
        <item name="Ammo_762x39" chance="1.0"/>  <!-- Chambers automatically -->
    </cargo>
</type>
```

### randompresets.xml
```xml
<!-- Can now be appended via cfgeconomycore.xml (NEW in 1.28) -->
<randompresets>
    <cargo name="MyPreset">
        <item name="BandageDressing" chance="1.0"/>
        <item name="Morphine" chance="0.5"/>
        <item name="Codeine" chance="0.3"/>
    </cargo>
</randompresets>
```

## events.xml (Dynamic Events)

```xml
<event name="StaticHeliCrash">
    <nominal>3</nominal>
    <min>1</min>
    <max>3</max>
    <lifetime>1500</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="3" min="1" type="Wreck_Mi8"/>
    </children>
</event>
```

### NEW in 1.28 - Dynamic Events on Sakhal
- Helicopter crashes
- Military patrol boat wrecks (coastal)
- Fishing boat wrecks (coastal)
- Ambulance wrecks (roads)
- Geysers in hot springs

## cfgeconomycore.xml

Controls which files the CE system loads:
```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types"/>
        <file name="spawnabletypes.xml" type="spawnabletypes"/>
        <file name="events.xml" type="events"/>
        <file name="globals.xml" type="globals"/>
        <!-- Append custom presets (NEW in 1.28) -->
        <file name="myrandompresets.xml" type="randompresets"/>
    </ce>
</economycore>
```

## Common Patterns

### Rare Military Item
```xml
<type name="MyRareWeapon">
    <nominal>3</nominal>
    <lifetime>14400</lifetime>
    <restock>3600</restock>
    <min>1</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>100</cost>
    <flags count_in_cargo="0" count_in_hoarder="1" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
    <category name="weapons"/>
    <usage name="Military"/>
    <value name="Tier3"/>
    <value name="Tier4"/>
</type>
```

### Common Civilian Item
```xml
<type name="MyCommonItem">
    <nominal>50</nominal>
    <lifetime>7200</lifetime>
    <restock>900</restock>
    <min>25</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>20</cost>
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
    <category name="tools"/>
    <usage name="Town"/>
    <usage name="Village"/>
    <value name="Tier1"/>
    <value name="Tier2"/>
    <value name="Tier3"/>
</type>
```
