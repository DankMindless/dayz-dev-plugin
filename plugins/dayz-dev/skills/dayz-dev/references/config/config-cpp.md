# config.cpp Reference

## Structure Overview

```cpp
class CfgPatches { /* What this mod adds */ };
class CfgMods { /* Mod metadata and script registration */ };
class CfgVehicles { /* Items, vehicles, buildings, entities */ };
class CfgWeapons { /* Weapons and optics */ };
class CfgMagazines { /* Magazines and ammo containers */ };
class CfgAmmo { /* Ammunition/projectile properties */ };
class CfgNonAIVehicles { /* Non-interactive objects */ };
class CfgSurfaces { /* Surface/material properties */ };
```

## CfgPatches (Required)

```cpp
class CfgPatches
{
    class MyMod
    {
        units[] = {"MyItem1", "MyItem2"};     // Classnames added
        weapons[] = {"MyWeapon1"};            // Weapon classnames added
        requiredVersion = 0.1;
        requiredAddons[] = {"DZ_Data"};        // Dependencies
    };
};
```

## CfgMods (Required for Script Registration)

```cpp
class CfgMods
{
    class MyMod
    {
        dir = "MyMod";
        picture = "";
        action = "";
        hideName = 1;
        hidePicture = 1;
        name = "MyMod";
        credits = "";
        author = "AuthorName";
        authorID = "";
        version = "1.0";
        extra = 0;
        type = "mod";
        dependencies[] = {"Game", "World", "Mission"};

        class defs
        {
            class gameScriptModule
            {
                value = "";
                files[] = {"MyMod/scripts/3_Game"};
            };
            class worldScriptModule
            {
                value = "";
                files[] = {"MyMod/scripts/4_World"};
            };
            class missionScriptModule
            {
                value = "";
                files[] = {"MyMod/scripts/5_Mission"};
            };
        };
    };
};
```

## CfgVehicles - Common Item

```cpp
class CfgVehicles
{
    class Inventory_Base;  // External class reference

    class MyItem : Inventory_Base
    {
        scope = 2;                           // 0=private, 1=protected, 2=public
        displayName = "My Item";
        descriptionShort = "Description";
        model = "\MyMod\data\myitem.p3d";
        weight = 500;                        // grams
        itemSize[] = {2, 3};                 // inventory slots (W x H)
        rotationFlags = 17;                  // inventory rotation
        absorbency = 0;                      // water absorption 0-1
        inventorySlot[] = {};                // attachment slots this fits in
        lootCategory = "Crafted";
        lootTag[] = {"Civilian"};
        isMeleeWeapon = 0;
        canBeSplit = 0;
        varQuantityInit = 0;
        varQuantityMin = 0;
        varQuantityMax = 0;
        quantityBar = 0;

        class DamageSystem
        {
            class GlobalHealth
            {
                class Health
                {
                    hitpoints = 100;
                    healthLevels[] =
                    {
                        {1.0, {}},           // Pristine
                        {0.7, {}},           // Worn
                        {0.5, {}},           // Damaged
                        {0.3, {}},           // Badly Damaged
                        {0.0, {}}            // Ruined
                    };
                };
            };
        };
    };
};
```

## CfgVehicles - Clothing

```cpp
class Clothing_Base;

class MyShirt : Clothing_Base
{
    scope = 2;
    displayName = "My Shirt";
    descriptionShort = "A custom shirt";
    model = "\MyMod\data\myshirt_g.p3d";
    weight = 350;
    itemSize[] = {3, 3};
    inventorySlot[] = {"Body"};              // Where it's worn

    // Cargo
    itemsCargoSize[] = {6, 3};               // Internal cargo space

    // Hidden selections for retexturing
    hiddenSelections[] = {"camoGround", "camoMale", "camoFemale"};
    hiddenSelectionsTextures[] = {
        "\MyMod\data\myshirt_co.paa",
        "\MyMod\data\myshirt_co.paa",
        "\MyMod\data\myshirt_co.paa"
    };
    hiddenSelectionsMaterials[] = {
        "\MyMod\data\myshirt.rvmat",
        "\MyMod\data\myshirt.rvmat",
        "\MyMod\data\myshirt.rvmat"
    };

    // Insulation
    heatIsolation = 0.6;

    // Armor (optional)
    class ClothingTypes
    {
        // Armor values for different zones
    };

    class DamageSystem
    {
        class GlobalHealth
        {
            class Health
            {
                hitpoints = 200;
                healthLevels[] =
                {
                    {1.0, {"\MyMod\data\myshirt.rvmat"}},
                    {0.7, {"\MyMod\data\myshirt_damage.rvmat"}},
                    {0.5, {"\MyMod\data\myshirt_damage.rvmat"}},
                    {0.3, {"\MyMod\data\myshirt_destruct.rvmat"}},
                    {0.0, {"\MyMod\data\myshirt_destruct.rvmat"}}
                };
            };
        };
    };
};
```

## CfgVehicles - Container

```cpp
class Container_Base;

class MyContainer : Container_Base
{
    scope = 2;
    displayName = "My Container";
    model = "\MyMod\data\container.p3d";
    weight = 2000;
    itemSize[] = {4, 4};
    itemsCargoSize[] = {10, 10};             // Internal cargo
    canBeDigged = 0;
    heavyItem = 1;

    // Attachment slots
    class Cargo
    {
        itemsCargoSize[] = {10, 10};
        allowOwnedCargoManipulation = 1;
    };
};
```

## Scope Values

| Value | Name | Meaning |
|-------|------|---------|
| 0 | Private | Cannot be spawned, hidden |
| 1 | Protected | Can be spawned but hidden from lists |
| 2 | Public | Fully spawnable and visible |

## Key Config Tokens

| Token | Type | Description |
|-------|------|-------------|
| `scope` | int | Visibility (0/1/2) |
| `displayName` | string | In-game name |
| `descriptionShort` | string | Tooltip description |
| `model` | string | P3D model path |
| `weight` | int | Weight in grams |
| `itemSize[]` | int[2] | Inventory size (W x H) |
| `inventorySlot[]` | string[] | Slots this fits in |
| `itemsCargoSize[]` | int[2] | Internal cargo (W x H) |
| `rotationFlags` | int | Inventory rotation |
| `absorbency` | float | Water absorption (0-1) |
| `heatIsolation` | float | Heat insulation |
| `lootCategory` | string | Loot spawning category |
| `lootTag[]` | string[] | Loot spawn tags |
| `hiddenSelections[]` | string[] | Retexture targets |
| `hiddenSelectionsTextures[]` | string[] | Texture paths |
| `hiddenSelectionsMaterials[]` | string[] | Material paths |
| `canBeSplit` | int | Can be split (0/1) |
| `varQuantityInit` | float | Initial quantity |
| `varQuantityMin` | float | Min quantity |
| `varQuantityMax` | float | Max quantity |

## External Class References

When inheriting from vanilla classes, declare them first:
```cpp
class CfgVehicles
{
    class Inventory_Base;      // Generic inventory item
    class Clothing_Base;       // Wearable clothing
    class Container_Base;      // Storage container
    class Edible_Base;         // Food/drink
    class Weapon_Base;         // Weapons
    class CarScript;           // Vehicles
    class HouseNoDestruct;     // Buildings

    class MyItem : Inventory_Base { /* ... */ };
};
```
