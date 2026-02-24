# Enforce Script Quick Reference

> DayZ uses **Enforce Script** - a C-like language. NOT C#, NOT C++, NOT Lua.

## Primitive Types
| Type | Size | Example |
|------|------|---------|
| `int` | 32-bit signed | `int x = 42;` |
| `float` | 32-bit IEEE | `float f = 3.14;` |
| `bool` | true/false | `bool b = true;` |
| `string` | UTF-8 | `string s = "hello";` |
| `vector` | 3x float (x,y,z) | `vector v = "1 2 3";` or `Vector(1,2,3)` |
| `typename` | Type reference | `typename t = int;` |
| `Class` | Base of all classes | Root type |

## Collections
```c
// Dynamic array
array<string> names = new array<string>;
names.Insert("item");
names.Count();      // size
names.Get(0);       // access
names.Remove(0);    // remove by index
names.Clear();      // empty

// Static array
int fixed[10];      // fixed-size, stack-allocated

// Set (unique values)
set<string> unique = new set<string>;
unique.Insert("a"); // returns false if duplicate

// Map
map<string, int> lookup = new map<string, int>;
lookup.Insert("key", 42);
lookup.Get("key");  // returns 42
lookup.Contains("key"); // true/false
```

## Type Aliases (Common)
| Alias | Actual Type |
|-------|-------------|
| `TStringArray` | `array<string>` |
| `TFloatArray` | `array<float>` |
| `TIntArray` | `array<int>` |
| `TVectorArray` | `array<vector>` |
| `TStringStringMap` | `map<string, string>` |
| `TIntStringMap` | `map<int, string>` |

## Constants & Globals
```c
const float FLT_MAX = 3.402823e+38;
const float FLT_MIN = 1.175494e-38;
float ftime;        // frame delta time (seconds)
```

## Operators
| Category | Operators |
|----------|-----------|
| Arithmetic | `+  -  *  /  %` |
| Comparison | `==  !=  <  >  <=  >=` |
| Logical | `&&  \|\|  !` |
| Bitwise | `&  \|  ^  ~  <<  >>` |
| Assignment | `=  +=  -=  *=  /=  &=  \|=` |

**WARNING:** Bitwise ops have LOWER precedence than comparisons!
```c
// WRONG: compares b == b first, then ANDs
if (flags & FLAG == FLAG)

// RIGHT: parenthesize bitwise
if ((flags & FLAG) == FLAG)
```

## Control Flow
```c
// If/else
if (condition) { } else if (other) { } else { }

// Switch
switch (value)
{
    case 1: /* ... */ break;
    case 2: /* ... */ break;
    default: break;
}

// For loop
for (int i = 0; i < count; i++) { }

// While loop
while (condition) { }

// Foreach
foreach (string item : myArray) { }
// WARNING: Never foreach on a getter return directly!
// WRONG:  foreach (auto x : GetSomething())
// RIGHT:  auto list = GetSomething(); foreach (auto x : list)
```

## Classes & Inheritance
```c
class MyClass extends ParentClass
{
    // Access modifiers: private, protected, public (default)
    private int m_Value;
    protected string m_Name;
    float m_PublicFloat;  // public by default

    // Constructor
    void MyClass()
    {
        m_Value = 0;
    }

    // Destructor
    void ~MyClass()
    {
        // cleanup
    }

    // Methods
    void SetValue(int val) { m_Value = val; }
    int GetValue() { return m_Value; }

    // Static methods
    static MyClass Create() { return new MyClass(); }
}
```

## Modded Classes (DayZ Injection Pattern)
```c
modded class PlayerBase
{
    private int m_CustomData;

    override void Init()
    {
        super.Init();  // ALWAYS call super!
        m_CustomData = 0;
    }

    override void SetActions(out TInputActionMap InputActionMap)
    {
        super.SetActions(InputActionMap);
        AddAction(MyAction, InputActionMap);
    }
}
```

## Templates (Generics)
```c
class Container<Class T>
{
    T m_Item;
    void Set(T item) { m_Item = item; }
    T Get() { return m_Item; }
}
```

## Enums
```c
enum MyEnum
{
    VALUE_A,        // 0
    VALUE_B,        // 1
    VALUE_C = 10,   // 10
    VALUE_D         // 11
}
```

## Casting
```c
// Safe downcast (returns null if invalid)
PlayerBase player = PlayerBase.Cast(entity);
if (player)
{
    // safe to use
}

// Alternative CastTo (out parameter)
PlayerBase player;
if (CastTo(player, entity))
{
    // safe to use
}

// Type checking
if (entity.IsInherited(PlayerBase))
{
    // entity IS a PlayerBase
}

// Get type name
string typeName = entity.ClassName();  // "PlayerBase"
typename type = entity.Type();
```

## String Methods
| Method | Returns | Notes |
|--------|---------|-------|
| `s.Length()` | `int` | String length |
| `s.IndexOf(substr)` | `int` | First occurrence, -1 if not found |
| `s.Substring(start, len)` | `string` | Extract substring |
| `s.Replace(old, new)` | `int` | Replaces in-place, returns count |
| `s.ToLower()` | `int` | Modifies in-place! Returns LENGTH not string |
| `s.ToUpper()` | `int` | Modifies in-place! Returns LENGTH not string |
| `s.Trim()` | `string` | Remove whitespace |
| `s.Split(delim, out arr)` | `void` | Split into array |
| `s.Contains(substr)` | `bool` | Check contains |

**WARNING:** `ToLower()` and `ToUpper()` modify the string in-place AND return the length (int), NOT the modified string!

## Preprocessor
```c
#define MY_CONSTANT 42
#ifdef SERVER
    // server-only code
#endif
#ifndef CLIENT
    // not client
#endif
#include "path/to/file.c"
```

**WARNING:** Empty preprocessor blocks can cause segfaults. Always have content or remove the block entirely.

## Function Parameters
```c
// Normal parameter
void Foo(int x) { }

// Out parameter (modified by callee)
void GetValues(out int x, out int y) { x = 1; y = 2; }

// Default parameter
void Bar(int x, int y = 0, string s = "") { }

// WARNING: ref in params is WRONG - ref is for member variables only!
// WRONG: void Bad(ref int x)
// RIGHT: void Good(out int x)
```

## Key Singletons
```c
GetGame()           // CGame - main game object (use g_Game in 1.28+ for perf)
GetDayZGame()       // DayZGame - DayZ-specific game
GetPlayer()         // Man - local player (client only)
GetRPCManager()     // CF RPCManager (requires Community Framework)
g_Game              // Global game reference (faster than GetGame() in 1.28+)
```
