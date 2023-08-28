from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from actions import Action
from assets import color

if TYPE_CHECKING:
    from entity import Actor


class RaiseDeadAction(Action):
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)

    @property
    def target_corpse(self) -> Optional[Actor]:
        """Return the closest corpse to the entity using this action"""
        return self.engine.game_map.get_nearest_corpse(self.entity.x, self.entity.y)
    
    def perform(self) -> None:
        """Finds the nearest corpse to the player (within sight) and raises it as a minion"""
        corpse = self.target_corpse

        if corpse:
            corpse.fighter.turn_to_minion()
        else:
            self.entity.gamemap.engine.message_log.add_message("There are no corpses nearby to raise", color.impossible)

