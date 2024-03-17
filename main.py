#!/usr/bin/env python3
import traceback

import tcod

import assets.color as color
import exceptions
from input_handlers import BaseEventHandler, EventHandler
import setup_game


def save_game(handler: BaseEventHandler, filename: str) -> None:
    """If the current event handler was an active Engine then save it."""
    if isinstance(handler, EventHandler):
        handler.engine.save_as(filename)


def main() -> None:
    screen_width = 120
    screen_height = 75

    tileset = tcod.tileset.load_tilesheet(
        "assets/tilesets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    handler: BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Death n Taxes",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error)
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise


if __name__ == "__main__":
    main()
