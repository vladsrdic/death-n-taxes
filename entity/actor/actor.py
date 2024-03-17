from __future__ import annotations

from typing import Optional, Tuple, Type, TYPE_CHECKING

from entity import Entity
from entity.render_order import RenderOrder
from entity.actor.components.ai import HostileEnemy, PlayerMinion

if TYPE_CHECKING:
    from entity.actor.components.ai import BaseAI
    from entity.actor.components.equipment import Equipment
    from entity.actor.components.fighter import Fighter
    from entity.actor.components.inventory import Inventory
    from entity.actor.components.level import Level


class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        original_name: str = None,
        ai_cls: Type[BaseAI],
        equipment: Equipment,
        fighter: Fighter,
        inventory: Inventory,
        level: Level,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            original_name=original_name or name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.equipment: Equipment = equipment
        self.equipment.parent = self

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

        self.level = level
        self.level.parent = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
    
    @property
    def is_hostile(self) -> bool:
        """Returns true as long as this actor has a hostile AI"""
        return isinstance(self.ai, HostileEnemy)

    @property
    def is_minion(self) -> bool:
        """Returns true as long as this actor has a player minion AI"""
        return isinstance(self.ai, PlayerMinion)