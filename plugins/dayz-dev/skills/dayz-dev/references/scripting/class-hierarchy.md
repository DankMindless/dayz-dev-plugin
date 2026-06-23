# DayZ Class Hierarchy

## Core Entity Chain
```
Class
└── Entity
    └── IEntity
        └── EntityAI
            ├── DayZCreature
            │   ├── DayZAnimal (Animal_BosTaurus, Animal_CanisLupus, etc.)
            │   └── DayZInfected (ZmbM_*, ZmbF_* - all zombie variants)
            ├── Man
            │   └── ManBase
            │       └── PlayerBase
            │           └── DayZPlayer
            │               └── DayZPlayerImplement (SurvivorBase)
            ├── ItemBase (Inventory_Base)
            │   ├── Edible_Base (food, drinks)
            │   ├── Clothing_Base (all wearables)
            │   ├── Container_Base (storage containers)
            │   └── Weapon_Base
            │       ├── Rifle_Base
            │       ├── Pistol_Base
            │       └── Weapon_BaseRifle
            ├── Building / BuildingSuper
            │   └── BuildingWithFireplace
            ├── CarScript (all vehicles)
            │   ├── OffroadHatchback, CivilianSedan, Hatchback_02, etc.
            │   └── ExpansionVehicleBase (Expansion vehicles)
            └── BaseBuildingBase
                └── Fence, Watchtower, etc.
```

## Key IEntity Methods (20+)
```c
vector GetPosition();
void SetPosition(vector pos);
vector GetOrientation();        // yaw, pitch, roll
void SetOrientation(vector ori);
vector GetDirection();          // forward direction
vector GetSpeed();              // velocity
void GetTransform(out vector mat[4]);
void SetTransform(vector mat[4]);
bool IsMan();
bool IsBuilding();
bool IsItemBase();
bool IsTransport();
bool IsAnimal();
bool IsZombie();
```

## Key EntityAI Methods
```c
GameInventory GetInventory();
void SetHealth(string zone, string system, float value);
float GetHealth(string zone, string system);
float GetHealth01(string zone, string system);  // 0-1 range
void ProcessDirectDamage(int damageType, EntityAI source, string component, string ammo, vector modelPos, float damageCoef);
void SetLifetime(float seconds);
float GetLifetimeMax();
bool IsAlive();
bool IsDamageDestroyed();
bool IsRuined();
void AddAction(typename actionType, out TInputActionMap map);
void RemoveAction(typename actionType);
void Delete();
```

## Key PlayerBase Methods
```c
// Identity & State
PlayerIdentity GetIdentity();
string GetIdentity().GetId();       // Steam64 ID
string GetIdentity().GetName();     // Player name
bool IsAlive();
bool IsUnconscious();

// Inventory
EntityAI GetItemInHands();
GameInventory GetInventory();
EntityAI GetInventory().CreateInInventory(string className);
void PredictiveTakeEntityToHands(EntityAI item);

// Position & Movement
vector GetPosition();
void SetPosition(vector pos);
float GetDirection();
bool IsInVehicle();
Transport GetCommand_Vehicle().GetTransport();

// Stats & State
void SetHealth(string zone, string system, float val);
float GetStatWater().Get();
float GetStatEnergy().Get();
float GetStatHeatComfort().Get();
int GetBrokenLegs();

// Context
bool IsControlledPlayer();
bool HasItem(EntityAI item);
```

## Action System Hierarchy
```
ActionBase
├── ActionSingleUseBase (one-time actions)
│   └── ActionSingleUseBase subtypes
├── ActionContinuousBase (hold actions)
│   └── ActionContinuousBase subtypes
├── ActionInteractBase (interact key)
│   └── ActionInteractBase subtypes
└── FirearmActionBase (weapon actions)
    └── FirearmActionBase subtypes
```

### Key Action Methods
```c
class MyAction extends ActionInteractBase
{
    override void CreateConditionComponents()
    {
        m_ConditionItem = new CCINone();
        m_ConditionTarget = new CCTObject(UAMaxDistances.DEFAULT);
    }

    override string GetText() { return "My Action"; }

    override bool ActionCondition(PlayerBase player, ActionTarget target, ItemBase item)
    {
        return true; // when action is available
    }

    override void OnExecuteServer(ActionData action_data)
    {
        // server-side logic
    }

    override void OnExecuteClient(ActionData action_data)
    {
        // client-side logic
    }
}
```

## GameInventory System
```c
// InventoryLocation types
enum InventoryLocationType
{
    GROUND,         // on the ground
    HANDS,          // in player hands
    ATTACHMENT,     // attached to parent
    CARGO,          // in cargo of parent
    PROXYCARGO,     // nearby ground items
    VEHICLE         // in vehicle cargo
}

// Key GameInventory methods
bool CreateInInventory(string type);
bool CanAddEntityInCargo(EntityAI item);
bool CanAddAttachment(EntityAI item);
EntityAI CreateEntityInCargo(string type);
EntityAI CreateAttachment(string type);
bool TakeEntityToCargo(InventoryMode mode, EntityAI item);
bool TakeEntityToInventory(InventoryMode mode, FindInventoryLocationType flags, EntityAI item);
bool FindFreeLocationFor(EntityAI item, FindInventoryLocationType flags, out InventoryLocation loc);
int GetInventoryItemCount();
```

## Key Singletons
```c
// Game
CGame GetGame()             // or g_Game (faster, 1.28+)
DayZGame GetDayZGame()

// Player (client only)
Man GetPlayer()             // local player
PlayerBase.Cast(GetGame().GetPlayer())  // typed local player

// World
World GetGame().GetWorld()

// Mission
MissionBase GetGame().GetMission()

// Weather
Weather GetGame().GetWeather()

// CF (requires Community Framework)
RPCManager GetRPCManager()
```

## Widget/UI System
```c
// Creating UI
Widget root = GetGame().GetWorkspace().CreateWidgets("path/layout.layout");
TextWidget text = TextWidget.Cast(root.FindAnyWidget("TextName"));
text.SetText("Hello");

// Event handling
class MyHandler extends ScriptedWidgetEventHandler
{
    override bool OnClick(Widget w, int x, int y, int button)
    {
        if (w.GetName() == "MyButton")
        {
            // handle click
            return true;
        }
        return false;
    }
}
```

## Effect System
```c
// Sound
SEffectManager.PlaySound("MySoundSet", position);
SEffectManager.PlaySoundOnObject("MySoundSet", object);

// Particles
Particle.PlayInWorld(ParticleList.PARTICLE_ID, position);
Particle.PlayOnObject(ParticleList.PARTICLE_ID, object);
```

## Weather System
```c
Weather weather = GetGame().GetWeather();
weather.GetOvercast().Set(0.8, 300, 600);    // value, time, duration
weather.GetRain().Set(0.5, 60, 120);
weather.GetFog().Set(0.3, 120, 240);
weather.GetWindSpeed().Set(15.0, 60, 120);
weather.GetWindDirection().Set(2.5, 60, 120);
weather.SetStorm(1.0, 0.8, 30);             // density, threshold, timeout
```
