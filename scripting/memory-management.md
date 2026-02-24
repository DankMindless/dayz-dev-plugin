# Memory Management in Enforce Script

## Overview

Enforce Script uses **garbage collection** with optional **reference counting** via the `Managed` base class. Understanding this is critical for avoiding memory leaks and crashes.

## Key Rules

1. **Never use `delete`** - Null the reference instead; `delete` can cause segfaults
2. **Use `ref`/`autoptr` ONLY for member variables** - Never in function parameters, returns, or locals
3. **Inherit from `Managed`** to enable `ref`/`autoptr` reference counting
4. **`autoptr` auto-deletes** when the variable goes out of scope
5. **One strong reference per object** when possible - minimize `ref` references to same object
6. **The GC is very aggressive** - destroys function-scope instances immediately when no `ref` holds them

## Reference Types

### `ref` - Strong Reference (Member Variables Only)
```c
class MyClass
{
    ref MyData m_Data;  // Prevents GC collection while MyClass exists

    void Init()
    {
        m_Data = new MyData();  // m_Data prevents GC of MyData
    }

    // When MyClass is destroyed, ref is released
    // If nothing else references MyData, it gets collected
}
```

### `autoptr` - Auto-Deleting Reference
```c
void MyFunction()
{
    autoptr MyData tempData = new MyData();
    // Use tempData...

    // tempData is automatically deleted when this scope exits
    // Even if an exception occurs
}
```

### Weak Reference (No Keyword)
```c
class MyClass
{
    MyData m_WeakRef;  // Does NOT prevent GC collection

    void SetData(MyData data)
    {
        m_WeakRef = data;  // If data is GC'd elsewhere, this becomes null
    }
}
```

## Common Patterns

### Pattern 1: Owner Holds Strong Ref
```c
class PlayerModule
{
    ref array<ref CustomData> m_PlayerData;  // Strong ref to array AND contents

    void PlayerModule()
    {
        m_PlayerData = new array<ref CustomData>;
    }

    void AddData(string name)
    {
        ref CustomData data = new CustomData(name);
        m_PlayerData.Insert(data);
    }

    void ClearAll()
    {
        m_PlayerData.Clear();  // All CustomData objects are released
    }
}
```

### Pattern 2: Temporary Processing
```c
void ProcessItems()
{
    // autoptr ensures cleanup even if we return early
    autoptr array<EntityAI> items = new array<EntityAI>;

    // Fill array...
    GetGame().GetObjectsAtPosition(pos, radius, items, null);

    foreach (EntityAI item : items)
    {
        if (SomeCondition(item))
            return;  // autoptr still cleans up items array
    }
}
```

### Pattern 3: Managed Base Class
```c
// Your class MUST extend Managed (or a class that extends it) for ref to work
class CustomData : Managed
{
    string m_Name;
    int m_Value;

    void CustomData(string name)
    {
        m_Name = name;
    }
}

// Now ref works:
ref CustomData data = new CustomData("test");
```

## Common Mistakes

### Mistake 1: `ref` in Function Parameters
```c
// WRONG - ref is for member variables only!
void BadFunction(ref MyData data)
{
    // This does NOT work as intended
}

// RIGHT - use out parameter or just pass normally
void GoodFunction(out MyData data)
{
    data = new MyData();
}

void AlsoGood(MyData data)
{
    // data is a weak reference copy
}
```

### Mistake 2: Forgetting Managed Inheritance
```c
// WRONG - ref has no effect without Managed
class BadClass
{
    int m_Value;
}
ref BadClass bad = new BadClass();  // ref does nothing here

// RIGHT - extend Managed
class GoodClass : Managed
{
    int m_Value;
}
ref GoodClass good = new GoodClass();  // ref works correctly
```

### Mistake 3: Circular References
```c
// DANGER - circular refs prevent GC
class Parent : Managed
{
    ref Child m_Child;
}

class Child : Managed
{
    ref Parent m_Parent;  // Circular! Neither will ever be collected
}

// FIX - use weak ref on one side
class Child : Managed
{
    Parent m_Parent;  // Weak ref - doesn't prevent GC of Parent
}
```

### Mistake 4: Using `delete` Keyword
```c
// WRONG - delete can segfault!
MyObject obj = new MyObject();
delete obj;  // Can cause crashes!

// RIGHT - null the reference instead, let GC handle cleanup
MyObject obj = new MyObject();
obj = null;  // Reference released, GC cleans up

// RIGHT - use autoptr for scope-based cleanup
autoptr MyObject obj = new MyObject();
// obj is cleaned up when scope exits
```

### Mistake 5: Not Using `ref` on Member Variables (Premature GC)
```c
// WRONG - GC is aggressive, may collect the object between frames
class MySystem
{
    MyData m_Data;  // Weak ref - GC can destroy MyData at any time!

    void Init()
    {
        m_Data = new MyData();
        // m_Data may be GC'd before next use!
    }
}

// RIGHT - ref prevents premature collection
class MySystem
{
    ref MyData m_Data;  // Strong ref - GC won't collect while MySystem exists

    void Init()
    {
        m_Data = new MyData();
        // m_Data is safe as long as MySystem is alive
    }
}
```

### Mistake 6: Multiple Strong References to Same Object
```c
// AVOID - creates confusing ownership
class SystemA { ref MyData m_Data; }
class SystemB { ref MyData m_Data; }  // Two owners = unclear lifecycle

// BETTER - one strong owner, others use weak references
class SystemA { ref MyData m_Data; }   // Owner
class SystemB { MyData m_DataRef; }    // Observer (weak ref)
```

## Entity Lifecycle

DayZ entities (items, players, vehicles) are managed by the engine, NOT by script GC:

```c
// Creating entities
EntityAI item = GetGame().CreateObjectEx("AKM", position, ECE_PLACE_ON_SURFACE);

// Deleting entities (server only!)
if (GetGame().IsServer())
{
    GetGame().ObjectDelete(item);  // Proper entity deletion
    // OR
    item.Delete();  // Also valid
}

// Do NOT use delete keyword on entities
// delete item;  // WRONG - use ObjectDelete or Delete() method
```

## Persistence & Lifetime

```c
// Set entity lifetime (seconds until cleanup)
item.SetLifetime(3600);          // 1 hour
item.SetLifetimeMax(14400);      // 4 hours max

// Persistence (survives server restart)
// Configured in types.xml: <flags count_in_cargo="0" count_in_hoarder="0" ... />
// Items in player inventory are automatically persistent
// Items on ground follow CE lifetime rules
```

## Credits

Memory management patterns referenced from [TrueDolphin's EnScript Style Guide](https://github.com/TrueDolphin/references/wiki/EnScript-(Enforce-Script)-Style-Guide).
