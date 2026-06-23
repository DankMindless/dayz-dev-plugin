# Community Framework (CF)

> **Steam Workshop ID:** 1559212036
> **GitHub:** https://github.com/Arkensor/DayZ-CommunityFramework
> **Minimum for 1.28:** CF 1.5.7

## Overview

Community Framework provides essential modding utilities:
- **RPCManager** - Named cross-mod RPC system
- **Modules** - Event-driven module registration
- **NetworkedVariables** - Easy state synchronization
- **ModStorage** - Per-entity persistent storage
- **TypeConverters** - Type conversion utilities
- **NotificationSystem** - In-game notifications
- **Surface Info** - Surface type queries

## Script Structure
```
JM/CF/
  Scripts/
    config.cpp
    3_Game/
      CommunityFramework/
        CommunityFramework.c        # Core framework
        RPC/
          RPCManager.c              # Cross-mod RPC
        Game/
          DayZGame.c                # Modded DayZGame
        Notification/
          NotificationSystem.c      # Notifications
    4_World/
      CommunityFramework/
        Module/                     # World-level modules
    5_Mission/
      CommunityFramework/
        Module/                     # Mission-level modules
```

## RPCManager

### Registration
```c
// Register in your class constructor or init
GetRPCManager().AddRPC(
    "MyModName",                        // Namespace (your mod name)
    "RPC_FunctionName",                 // RPC name (must match handler method)
    this,                               // Handler object
    SingleplayerExecutionType.Both      // Singleplayer behavior
);
```

### SingleplayerExecutionType
| Value | Behavior |
|-------|----------|
| `Both` | Runs on both client and server in SP |
| `Client` | Client-side only in SP |
| `Server` | Server-side only in SP |

### Sending
```c
// To specific client (from server)
GetRPCManager().SendRPC("MyMod", "RPC_Name",
    new Param1<string>("data"),
    true,                              // Guaranteed delivery
    targetPlayer.GetIdentity());       // Target client

// To server (from client)
GetRPCManager().SendRPC("MyMod", "RPC_Name",
    new Param1<int>(42),
    true,
    null);                             // null = server

// Broadcast to all clients
GetRPCManager().VSendRPC("MyMod", "RPC_Name",
    new Param1<string>("broadcast"),
    true);
```

### Handler Pattern
```c
void RPC_MyHandler(CallType type, ParamsReadContext ctx, PlayerIdentity sender, Object target)
{
    // Read parameters (MUST match what was sent)
    Param2<string, int> data;
    if (!ctx.Read(data)) return;

    string name = data.param1;
    int value = data.param2;

    if (type == CallType.Server)
    {
        // Running on server
        if (!sender) return;  // Validate sender
        // Process server-side
    }
    else if (type == CallType.Client)
    {
        // Running on client
        // Update UI, effects, etc.
    }
}
```

## CF Modules

### Registration
```c
[CF_RegisterModule(MyModule)]
class MyModule : CF_ModuleWorld
{
    // Module is automatically instantiated and registered
}
```

### Key Events
```c
class MyModule : CF_ModuleWorld
{
    override void OnInit()
    {
        super.OnInit();
        // Module initialization - register RPCs, load config
    }

    override void OnUpdate(CF_EventUpdateArgs args)
    {
        // Per-frame update
        float dt = args.DeltaTime;
        // Use dt for timing
    }

    override void OnMissionStart(Class sender, CF_EventArgs args)
    {
        // Mission started
    }

    override void OnMissionFinish(Class sender, CF_EventArgs args)
    {
        // Mission ending - save data
    }

    override void OnMissionLoaded(Class sender, CF_EventArgs args)
    {
        // Mission fully loaded
    }

    override void OnClientReady(Class sender, CF_EventArgs args)
    {
        // Client fully loaded and ready
    }

    override void OnClientDisconnect(Class sender, CF_EventArgs args)
    {
        // Client disconnecting
    }

    override void OnClientNew(Class sender, CF_EventArgs args)
    {
        // New client connected
    }

    override void OnClientRespawn(Class sender, CF_EventArgs args)
    {
        // Client respawning
    }
}
```

## ModStorage (CF 1.5.5+)

Per-entity persistent key-value storage that survives server restarts.

```c
modded class ItemBase
{
    protected int m_CustomValue;
    protected string m_CustomName;

    // Save data
    override void OnStoreSave(ParamsWriteContext ctx)
    {
        super.OnStoreSave(ctx);
        ctx.Write(m_CustomValue);
        ctx.Write(m_CustomName);
    }

    // Load data
    override bool OnStoreLoad(ParamsReadContext ctx, int version)
    {
        if (!super.OnStoreLoad(ctx, version)) return false;

        if (!ctx.Read(m_CustomValue)) return false;
        if (!ctx.Read(m_CustomName)) return false;

        return true;
    }
}
```

**Note (CF 1.5.7+):** ModStorage no longer requires a custom class inheriting from `ModStructure` - simplified API.

## NetworkedVariables

```c
class MyModule : CF_ModuleWorld
{
    CF_NetworkedVariable<int> m_Score;
    CF_NetworkedVariable<string> m_Message;
    CF_NetworkedVariable<bool> m_Active;

    override void OnInit()
    {
        super.OnInit();
        m_Score = new CF_NetworkedVariable<int>(0);
        m_Message = new CF_NetworkedVariable<string>("");
        m_Active = new CF_NetworkedVariable<bool>(false);
    }

    // Set values (automatically synced)
    void UpdateScore(int score)
    {
        m_Score.Set(score);
    }

    // Read values
    int GetScore()
    {
        return m_Score.Get();
    }
}
```

**Warning:** CF NetworkedVariables have a nesting depth limit. Don't nest complex data structures too deeply.

## NotificationSystem

```c
// Send notification to player
NotificationSystem.AddNotification(player, NotificationType.FRIENDLY, "Title", "Message text");

// Notification types
// NotificationType.FRIENDLY   - Green
// NotificationType.NEUTRAL    - White
// NotificationType.HOSTILE    - Red
```

## TypeConverters

```c
// Convert between types
string str = CF_TypeConverters.IntToString(42);
int val = CF_TypeConverters.StringToInt("42");
```

## config.cpp Integration

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = {"DZ_Data", "JM_CF_Scripts"};
    };
};
```

## CF 1.5.7+ Changes (1.28 Compatible)
- ModStorage simplified (no ModStructure needed)
- Fixed file state tracking on entity load
- Millisecond logging timestamps
- Non-ASCII character handling fixes

## CF 1.5.8 Changes (1.29 Experimental)
- `CF_Byte::ToHex` renamed to `CF_ToHex`
- No longer creating new `CF_EventUpdateArgs` each OnUpdate (performance)
- `GetGame()` -> `g_Game` optimization recommended
