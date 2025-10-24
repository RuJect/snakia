from typing import final

from pydantic import Field

from snakia.core.ecs import Component
from snakia.core.ecs.system import System
from snakia.core.engine import Engine
from snakia.core.es import Event
from snakia.core.loader import Meta, Plugin, PluginProcessor
from snakia.types import Version


class HealthComponent(Component):
    max_value: int = Field(default=100, ge=0)
    value: int = Field(default=100, ge=0)


class DamageComponent(Component):
    damage: int = Field(ge=0)
    ticks: int = Field(default=1, ge=0)


class HealComponent(Component):
    heal: int = Field(ge=0)
    ticks: int = Field(default=1, ge=0)


class DeathEvent(Event):
    entity: int = Field()


class HealthProcessor(PluginProcessor):
    def process(self, system: System) -> None:
        for entity, (heal, health) in system.get_components(
            HealComponent, HealthComponent
        ):
            health.value += heal.heal
            heal.ticks -= 1
            if heal.ticks <= 0:
                system.remove_component(entity, HealComponent)
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


@final
class HealthPlugin(
    Plugin,
    meta=Meta(
        name="health",
        author="snakia",
        version=Version.from_args(1, 0, 0),
        subscribers=(),
        processors=(HealthProcessor,),
    ),
):
    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass


def main() -> None:
    engine = Engine()
    engine.loader.register(HealthPlugin)
    engine.loader.load_all()

    @engine.dispatcher.on(DeathEvent)
    def on_death(event: DeathEvent) -> None:
        print(f"Entity: {event.entity} is death!")

    player = engine.system.create_entity()
    engine.system.add_component(player, HealthComponent())
    engine.system.add_component(player, DamageComponent(damage=10, ticks=10))

    engine.start()


if __name__ == "__main__":
    main()
