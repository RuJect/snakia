# 🐍 Snakia Framework

**Snakia** is a modern Python framework for creating applications with Entity-Component-System (ECS) architecture, event system, and reactive programming. Built with performance (maybe) and modularity in mind, Snakia provides a clean API for developing complex applications ranging from games to terminal user interfaces.

## 📋 Table of Contents

- [🎯 Roadmap & TODO](#-roadmap--todo)
- [🚀 Installation](#-installation)
- [🚀 Quick Start](#-quick-start)
- [🏗️ Architecture](#️-architecture)
- [⚙️ Core](#️-core)
- [🎯 ECS System](#-ecs-system)
- [📡 Event System (ES)](#-event-system-es)
- [🔌 Plugin System](#-plugin-system)
- [🎨 TUI System](#-tui-system)
- [⚡ Reactive Programming (RX)](#-reactive-programming-rx)
- [🛠️ Utilities](#️-utilities)
- [🎭 Decorators](#-decorators)
- [🏷️ Properties](#-properties)
- [🌐 Platform Abstraction](#-platform-abstraction)
- [📦 Examples](#-examples)
- [🤝 Contributing](#-contributing)
- [🆘 Support](#-support)
- [📄 License](#-license)

### ✨ Key Features

- 🏗️ **ECS Architecture** - Flexible entity-component-system for scalable game/app logic
- 📡 **Event System** - Asynchronous event handling with filters and priorities
- 🔌 **Plugin System** - Modular plugin architecture for extensibility
- 🎨 **TUI Framework** - Rich terminal user interface with reactive widgets
- ⚡ **Reactive Programming** - Observable data streams and reactive bindings
- 🛠️ **Rich Utilities** - Decorators, properties, platform abstraction, and more
- 🎯 **Type Safety** - Full type hints and Pydantic integration

> ⚠️ **Experimental Framework**  
> This framework is currently in **beta/experimental stage**. Not all features are fully implemented, there might be bugs, and the API is subject to change. Use at your own risk! 🚧

## 🚀 Installation

### Prerequisites

- **Python** >= 3.12
- **pip** or **uv** (recommended) package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/RuJect/Snakia.git
cd Snakia

# Install with pip
pip install -e .

# Or with uv (recommended)
uv sync
```

## 🎯 Roadmap & TODO

Here's what we're working on to make Snakia even better:

- [ ] Plugin Isolation: restrict plugin access to only events and components statically defined in manifest
- [ ] Async & Multithreading: implement proper async/await support and multithreading capabilities  
- [ ] Platform Support: expand platform abstraction to support more operating systems
- [ ] Random Implementations: add various random generations implementations
- [ ] TUI Widgets: create more ready-to-use TUI widgets and components
- [ ] Code Documentation: add comprehensive docstrings and inline comments
- [ ] Documentation: create detailed API documentation and tutorials

## 🚀 Quick Start

```python
from snakia.core.engine import Engine
from snakia.core.loader import Meta, Plugin, PluginProcessor
from snakia.core.ecs import Component
from snakia.types import Version

# Creating a component
class HealthComponent(Component):
    value: int = 100
    max_value: int = 100

# Creating a processor
class HealthProcessor(PluginProcessor):
    def process(self, system):
        for entity, (health,) in system.get_components(HealthComponent):
            if health.value <= 0:
                print(f"Entity {entity} died!")

# Creating a plugin
class HealthPlugin(Plugin, meta=Meta(
    name="health",
    version=Version.from_args(1, 0, 0),
    processors=(HealthProcessor,)
)):
    def on_load(self): pass
    def on_unload(self): pass

# Starting the engine
engine = Engine()
engine.loader.register(HealthPlugin)
engine.loader.load_all()
engine.start()
```

## 🏗️ Architecture

Snakia is built on a modular architecture with clear separation of concerns:

```plaintext
Snakia/
├── 🧠 core/           # Framework core
│   ├── engine.py      # Main engine
│   ├── ecs/           # Entity-Component-System
│   ├── es/            # Event System
│   ├── loader/        # Plugin loading system
│   ├── rx/            # Reactive programming
│   └── tui/           # Terminal User Interface
├── 🎭 decorators/     # Decorators
├── 🏷️ property/       # Property system
├── 🌐 platform/      # Platform abstraction
├── 🛠️ utils/         # Utilities
├── 🎲 random/        # Random number generation
├── 📝 field/         # Typed fields
└── 🔧 types/         # Special types
```

## ⚙️ Core

### Engine

The central component of the framework that coordinates all systems:

```python
from snakia.core.engine import Engine

engine = Engine()
# Systems:
# - engine.system    - ECS system
# - engine.dispatcher - Event system  
# - engine.loader    - Plugin loader

engine.start()  # Start all systems
engine.stop()   # Stop all systems
engine.update() # Update systems
```

## 🎯 ECS System

Entity-Component-System architecture for creating flexible and performant applications.

### Component

Base class for all components:

```python
from snakia.core.ecs import Component
from pydantic import Field

class PositionComponent(Component):
    x: float = Field(default=0.0)
    y: float = Field(default=0.0)

class VelocityComponent(Component):
    vx: float = Field(default=0.0)
    vy: float = Field(default=0.0)
```

### Processor

Processors handle components in the system:

```python
from snakia.core.ecs import Processor, System

class MovementProcessor(Processor):
    def process(self, system: System) -> None:
        # Get all entities with Position and Velocity
        for entity, (pos, vel) in system.get_components(
            PositionComponent, VelocityComponent
        ):
            pos.x += vel.vx
            pos.y += vel.vy
```

### System

Entity and component management:

```python
# Creating an entity with components
entity = system.create_entity(
    PositionComponent(x=10, y=20),
    VelocityComponent(vx=1, vy=0)
)

# Adding a component to an existing entity
system.add_component(entity, HealthComponent(value=100))

# Getting entity components
pos, vel = system.get_components_of_entity(
    entity, PositionComponent, VelocityComponent
)

# Checking for components
if system.has_components(entity, PositionComponent, VelocityComponent):
    print("Entity has position and velocity")

# Removing a component
system.remove_component(entity, VelocityComponent)

# Deleting an entity
system.delete_entity(entity)
```

## 📡 Event System (ES)

Asynchronous event system with filter and priority support.

### Event

Base class for events:

```python
from snakia.core.es import Event
from pydantic import Field

class PlayerDiedEvent(Event):
    player_id: int = Field()
    cause: str = Field(default="unknown")
    ttl: int = Field(default=10)  # Event lifetime
```

### Handler

Event handlers:

```python
from snakia.core.es import Handler, Action

def on_player_died(event: PlayerDiedEvent) -> Action | None:
    print(f"Player {event.player_id} died from {event.cause}")
    return Action.move(1)  # Move to next handler
```

### Filter

Event filters:

```python
from snakia.core.es import Filter

def only_important_deaths(event: PlayerDiedEvent) -> bool:
    return event.cause in ["boss", "pvp"]

# Using a filter
@dispatcher.on(PlayerDiedEvent, filter=only_important_deaths)
def handle_important_death(event: PlayerDiedEvent):
    print("Important death occurred!")
```

### Dispatcher

Central event dispatcher:

```python
from snakia.core.es import Dispatcher, Subscriber

dispatcher = Dispatcher()

# Subscribing to an event
dispatcher.subscribe(PlayerDiedEvent, Subscriber(
    handler=on_player_died,
    filter=only_important_deaths,
    priority=10
))

# Decorator for subscription
@dispatcher.on(PlayerDiedEvent, priority=5)
def handle_death(event: PlayerDiedEvent):
    print("Death handled!")

# Publishing an event
dispatcher.publish(PlayerDiedEvent(player_id=123, cause="boss"))
```

## 🔌 Plugin System

Modular system for loading and managing plugins.

### Plugin

Base class for plugins:

```python
from snakia.core.loader import Meta, Plugin, PluginProcessor
from snakia.types import Version

class MyProcessor(PluginProcessor):
    def process(self, system):
        # Processor logic
        pass

class MyPlugin(Plugin, meta=Meta(
    name="my_plugin",
    author="developer",
    version=Version.from_args(1, 0, 0),
    processors=(MyProcessor,),
    subscribers=()
)):
    def on_load(self):
        print("Plugin loaded!")
    
    def on_unload(self):
        print("Plugin unloaded!")
```

### Meta

Plugin metadata:

```python
from snakia.core.loader import Meta
from snakia.core.es import Subscriber

meta = Meta(
    name="plugin_name",
    author="author_name", 
    version=Version.from_args(1, 0, 0),
    processors=(Processor1, Processor2),
    subscribers=(
        (EventType, Subscriber(handler, filter, priority)),
    )
)
```

### Loader

Plugin loader:

```python
from snakia.core.loader import Loader

loader = Loader(engine)

# Registering a plugin
loader.register(MyPlugin)

# Loading all plugins
loader.load_all()

# Unloading all plugins
loader.unload_all()
```

## 🎨 TUI System

System for creating text-based user interfaces.

### Widget

Base class for widgets:

```python
from snakia.core.tui import Widget, Canvas, CanvasChar
from snakia.core.rx import Bindable

class MyWidget(Widget):
    def __init__(self):
        super().__init__()
        self.text = self.state("Hello World")
        self.color = self.state(CanvasChar(fg_color="red"))
    
    def on_render(self) -> Canvas:
        canvas = Canvas(20, 5)
        canvas.draw_text(0, 0, self.text.value, self.color.value)
        return canvas
```

### Canvas

Drawing canvas:

```python
from snakia.core.tui import Canvas, CanvasChar

canvas = Canvas(80, 24)

# Drawing text
canvas.draw_text(10, 5, "Hello", CanvasChar(fg_color="blue"))

# Drawing rectangle
canvas.draw_rect(0, 0, 20, 10, CanvasChar("█", fg_color="green"))

# Filling area
canvas.draw_filled_rect(5, 5, 10, 5, CanvasChar(" ", bg_color="red"))

# Lines
canvas.draw_line_h(0, 0, 20, CanvasChar("-"))
canvas.draw_line_v(0, 0, 10, CanvasChar("|"))
```

### CanvasChar

Character with attributes:

```python
from snakia.core.tui import CanvasChar

char = CanvasChar(
    char="A",
    fg_color="red",      # Text color
    bg_color="blue",     # Background color
    bold=True,           # Bold
    italic=False,        # Italic
    underline=True       # Underline
)
```

### Renderer

Screen rendering:

```python
from snakia.core.tui import RenderContext
from snakia.core.tui.render import ANSIRenderer
import sys

class StdoutTarget:
    def write(self, text: str): sys.stdout.write(text)
    def flush(self): sys.stdout.flush()

renderer = ANSIRenderer(StdoutTarget())

with RenderContext(renderer) as ctx:
    ctx.render(widget.render())
```

### Ready-made Widgets

```python
from snakia.core.tui.widgets import (
    TextWidget, BoxWidget, 
    HorizontalSplitWidget, VerticalSplitWidget
)

# Text widget
text = TextWidget("Hello", CanvasChar(fg_color="red", bold=True))

# Box widget
box = BoxWidget(10, 5, CanvasChar("█", fg_color="yellow"))

# Splitters
h_split = HorizontalSplitWidget([text1, text2], "|")
v_split = VerticalSplitWidget([h_split, box], "-")
```

## ⚡ Reactive Programming (RX)

Reactive programming system for creating responsive interfaces.

### Bindable

Reactive variables:

```python
from snakia.core.rx import Bindable, ValueChanged

# Creating a reactive variable
counter = Bindable(0)

# Subscribing to changes
def on_change(event: ValueChanged[int]):
    print(f"Counter changed from {event.old_value} to {event.new_value}")

counter.subscribe(on_change)

# Changing value
counter.set(5)  # Will call on_change
counter(10)     # Alternative syntax
```

### AsyncBindable

Asynchronous reactive variables:

```python
from snakia.core.rx import AsyncBindable

async_counter = AsyncBindable(0)

async def async_handler(event: ValueChanged[int]):
    print(f"Async counter: {event.new_value}")

await async_counter.subscribe(async_handler, run_now=True)
await async_counter.set(42)
```

### Operators

```python
from snakia.core.rx import map, filter, combine, merge

# Transformation
doubled = map(counter, lambda x: x * 2)

# Filtering
even_only = filter(counter, lambda x: x % 2 == 0)

# Combining
combined = combine(counter, doubled, lambda a, b: a + b)

# Merging streams
merged = merge(counter, async_counter)
```

## 🛠️ Utilities

### to_async

Converting synchronous functions to asynchronous:

```python
from snakia.utils import to_async

def sync_function(x):
    return x * 2

async_function = to_async(sync_function)
result = await async_function(5)
```

### nolock

Performance optimization:

```python
from snakia.utils import nolock

def busy_loop():
    while running:
        # Work
        nolock()  # Release GIL
```

### inherit

Simplified inheritance:

```python
from snakia.utils import inherit

class Base:
    def method(self): pass

class Derived(inherit(Base)):
    def method(self):
        super().method()
        # Additional logic
```

### this

Reference to current object:

```python
from snakia.utils import this

def func():
    return this()  # Returns `<function func at ...>`
```

### throw

Throwing exceptions:

```python
from snakia.utils import throw

def validate(value):
    if value < 0:
        throw(ValueError("Value must be positive"))
```

### frame

Working with frames:

```python
from snakia.utils import frame

def process_frame():
    current_frame = frame()
    # Process frame
```

## 🎭 Decorators

### inject_replace

Method replacement:

```python
from snakia.decorators import inject_replace

class Original:
    def method(self): return "original"

@inject_replace(Original, "method")
def new_method(self): return "replaced"
```

### inject_before / inject_after

Hooks before and after execution:

```python
from snakia.decorators import inject_before, inject_after

@inject_before(MyClass, "method")
def before_hook(self): print("Before method")

@inject_after(MyClass, "method") 
def after_hook(self): print("After method")
```

### singleton

Singleton pattern:

```python
from snakia.decorators import singleton

@singleton
class Database:
    def __init__(self):
        self.connection = "connected"
```

### pass_exceptions

Exception handling:

```python
from snakia.decorators import pass_exceptions

@pass_exceptions(ValueError, TypeError)
def risky_function():
    # Code that might throw exceptions
    pass
```

## 🏷️ Properties

### readonly

Read-only property:

```python
from snakia.property import readonly


class Currency:
    @readonly
    def rate(self) -> int:
        return 100


currency = Currency()
currency.rate = 200
print(currency.rate)  # Output: 100
```

### initonly

Initialization-only property:

```python
from snakia.property import initonly


class Person:
    name = initonly[str]("name")


bob = Person()
bob.name = "Bob"
print(bob.name)  # Output: "Bob"
bob.name = "not bob"
print(bob.name)  # Output: "Bob"
```

### 🏛️ classproperty

Class property:

```python
from snakia.property import classproperty

class MyClass:
    @classproperty
    def class_value(cls):
        return "class_value"
```

## 🌐 Platform Abstraction

### 🖥️ PlatformOS

Operating system abstraction:

```python
from snakia.platform import PlatformOS, OS

# Detecting current OS
current_os = OS.current()

if current_os == PlatformOS.LINUX:
    print("Running on Linux")
elif current_os == PlatformOS.ANDROID:
    print("Running on Android")
```

### 🏗️ PlatformLayer

Platform layers:

```python
from snakia.platform import LinuxLayer, AndroidLayer

# Linux layer
linux_layer = LinuxLayer()

# Android layer  
android_layer = AndroidLayer()
```

## 📦 Examples

### Health System

```python
from snakia.core.engine import Engine
from snakia.core.ecs import Component
from snakia.core.es import Event
from snakia.core.loader import Meta, Plugin, PluginProcessor
from snakia.types import Version
from pydantic import Field

class HealthComponent(Component):
    max_value: int = Field(default=100, ge=0)
    value: int = Field(default=100, ge=0)

class DamageComponent(Component):
    damage: int = Field(ge=0)
    ticks: int = Field(default=1, ge=0)

class DeathEvent(Event):
    entity: int = Field()

class HealthProcessor(PluginProcessor):
    def process(self, system):
        # Processing damage
        for entity, (damage, health) in system.get_components(
            DamageComponent, HealthComponent
        ):
            health.value -= damage.damage
            damage.ticks -= 1
            
            if damage.ticks <= 0:
                system.remove_component(entity, DamageComponent)
            
            if health.value <= 0:
                system.remove_component(entity, HealthComponent)
                self.plugin.dispatcher.publish(DeathEvent(entity=entity))

class HealthPlugin(Plugin, meta=Meta(
    name="health",
    version=Version.from_args(1, 0, 0),
    processors=(HealthProcessor,)
)):
    def on_load(self): pass
    def on_unload(self): pass

# Usage
engine = Engine()
engine.loader.register(HealthPlugin)
engine.loader.load_all()

# Creating a player
player = engine.system.create_entity(
    HealthComponent(value=100, max_value=100)
)

# Dealing damage
engine.system.add_component(player, DamageComponent(damage=25, ticks=1))

engine.start()
```

### TUI Application

```python
from snakia.core.tui import CanvasChar, RenderContext
from snakia.core.tui.render import ANSIRenderer
from snakia.core.tui.widgets import TextWidget, BoxWidget, VerticalSplitWidget
import sys

class StdoutTarget:
    def write(self, text: str): sys.stdout.write(text)
    def flush(self): sys.stdout.flush()

def main():
    # Creating widgets
    title = TextWidget("Snakia TUI", CanvasChar(fg_color="cyan", bold=True))
    content = TextWidget("Welcome to Snakia!", CanvasChar(fg_color="white"))
    box = BoxWidget(20, 5, CanvasChar("█", fg_color="green"))
    
    # Layout
    layout = VerticalSplitWidget([title, content, box], "-")
    
    # Rendering
    renderer = ANSIRenderer(StdoutTarget())
    
    with RenderContext(renderer) as ctx:
        ctx.render(layout.render())

if __name__ == "__main__":
    main()
```

## 🤝 Contributing

We welcome contributions to Snakia development! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Add** tests if applicable
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Development Guidelines

- Add type hints to all new code
- Write clear commit messages
- Update documentation for new features
- Test your changes thoroughly

## 🆘 Support

Need help? We're here to assist you!

- 🐛 **Bug Reports** - [GitHub Issues](https://github.com/RuJect/Snakia/issues)
- 💬 **Community Chat** - [RuJect Community Telegram](https://t.me/RuJect_Community)
- 📧 **Direct Contact** - mailto:rus07tam.uwu@gmail.com

## 📄 License

This project is distributed under the CC0 1.0 Universal. See the `LICENSE` file for details.
