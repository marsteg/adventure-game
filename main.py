import pygame
import time

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT, FPS, INTERACTION_DISTANCE,
    BACKGROUND_VOLUME, WHITE, YELLOW, GREEN, PURPLE, at_percentage_width, at_percentage_height,
    DIALOG_SKIP_COOLDOWN, DOUBLE_CLICK_THRESHOLD
)
from debug_grid import debug_grid
from item import Item
from inventory import Inventory
from room import Room
from door import Door
from action import Action
from actionfuncs import (
    ChangePicture, ChangeRoomPicture, LogText, UnlockDoor, AllowDestroy, GiveItem, TakeItem,
    DestroyItem, ActionChangeDialog, PlaySound
)
from npc import NPC
from dialogbox import DialogBox, VoiceManager, get_sound_duration
from answerbox import AnswerBox
from answer import Answer
from save import SaveState, LoadState, SaveStateToSlot, LoadStateFromSlot, MigrateOldSave, GetMostRecentSlot, DeleteSlot
from saveloadmenu import SaveLoadMenu, ConfirmDialog
from debug import debug_inventory_state, toggle_debug
from player import Player
from queueing import QueuedInteraction
from menu import MainMenu
from textcutscene import TextCutscene
from gamestate_manager import GameStateManager
from ui import (
    Colors, dialog_renderer, answer_renderer, inventory_renderer,
    tooltip_renderer, transition, draw_rounded_rect
)


class GameState:
    """Manages game state: menu, playing, paused, intro."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    CUTSCENE = "intro"
    SAVE_MENU = "save_menu"
    LOAD_MENU = "load_menu"


def main():
    pygame.init()
    pygame.display.set_caption('Adventure Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting Adventure Game!")

    clock = pygame.time.Clock()
    dt = 0
    from game import get_metadata, get_player_config
    title, player_start_percent = get_metadata()
    player_sprite, player_name = get_player_config()
    pygame.display.set_caption(title)

    # Game state
    game_state = GameState.MENU
    menu = MainMenu(title, in_game=False)  # Startup menu
    #intro = TextCutscene("assets/textcutscenes/intro.yaml")

    # Initialize GameStateManager
    state_manager = GameStateManager.get_instance()

    # These will be initialized when game starts
    inventory = None
    answerbox = None
    #player = None
    active_room = None
    rooms = {}
    player_char = Player(at_percentage_width(20), at_percentage_height(80), 50, 75, player_sprite, player_name)
    player = pygame.sprite.Group(player_char)

    # Playtime tracking
    playtime_seconds = 0
    session_start_time = None

    # Save/Load menus
    save_menu = None
    load_menu = None
    confirm_dialog = None
    pending_menu_action = None
    gameplay_screenshot = None  # Store screenshot before menu opens

    # Auto-save tracking
    last_room_for_autosave = None

    # Check for old save file and migrate
    MigrateOldSave()

    def init_game():
        """Initialize or reset the game."""
        nonlocal inventory, answerbox, player, active_room, rooms, playtime_seconds, session_start_time, last_room_for_autosave

        # Reset class-level containers
        Room.rooms = {}
        Item.items = {}
        NPC.NPCs = {}
        DialogBox.dialogboxes = []

        # Reset playtime tracking
        playtime_seconds = 0
        session_start_time = time.time()
        last_room_for_autosave = None

        updatable = pygame.sprite.Group()
        items_group = pygame.sprite.Group()
        clickables = pygame.sprite.Group()


        inventory = Inventory()
        answerbox = AnswerBox()

        # ============================================================
        # REPLACE WITH your own game content creation function, which should return the rooms and starting room
        # ============================================================
        from game import create_game_content
        rooms, active_room, intro = create_game_content(player, inventory)

        # Set player starting position in Tourist Shop
        from constants import at_percentage_width, at_percentage_height
        start_pos = pygame.Vector2(at_percentage_width(player_start_percent[0]), at_percentage_height(player_start_percent[1]))
        # Validate starting position - ensure feet will be walkable
        walkable_start = active_room.find_nearest_walkable_spawn(start_pos)
        player_char.pos = pygame.Vector2(walkable_start)

        # Start music
        pygame.mixer.music.load(active_room.music)
        pygame.mixer.music.set_volume(BACKGROUND_VOLUME)
        pygame.mixer.music.play(-1, 0.0)

        return updatable, active_room, intro

    def capture_thumbnail(scale=0.15):
        """Capture current game screen as a thumbnail.

        Args:
            scale: Scale factor for thumbnail (default 0.15 = 15% of original size)

        Returns:
            pygame.Surface: Scaled thumbnail surface
        """
        # Capture current screen
        thumbnail = screen.copy()
        # Scale down for thumbnail
        thumb_width = int(SCREEN_WIDTH * scale)
        thumb_height = int(SCREEN_HEIGHT * scale)
        thumbnail = pygame.transform.smoothscale(thumbnail, (thumb_width, thumb_height))
        return thumbnail

    def update_playtime():
        """Update the playtime counter based on elapsed time."""
        nonlocal playtime_seconds, session_start_time
        if session_start_time:
            elapsed = time.time() - session_start_time
            playtime_seconds += int(elapsed)
            session_start_time = time.time()

    def perform_save(slot_number, thumbnail_override=None):
        """Perform save to specified slot with thumbnail and playtime.

        Args:
            slot_number: Slot number to save to
            thumbnail_override: Optional pre-captured thumbnail surface
        """
        nonlocal playtime_seconds, title
        update_playtime()
        # Use provided thumbnail or capture current screen
        thumbnail = thumbnail_override if thumbnail_override else capture_thumbnail()
        success = SaveStateToSlot(title, active_room, inventory, player, slot_number, playtime_seconds, thumbnail)
        if success:
            print(f"Game saved to slot {slot_number} (Playtime: {playtime_seconds}s)")
        return success

    def perform_load(slot_number):
        """Load game from specified slot and update playtime."""
        nonlocal inventory, active_room, playtime_seconds, session_start_time, last_room_for_autosave, title

        loaded_room, new_inventory, player_pos, loaded_playtime = LoadStateFromSlot(slot_number, title)

        if loaded_room and new_inventory:
            # Clear current inventory state
            inventory.clear_all_slots()
            inventory.items.clear()

            # Copy items from loaded inventory
            for item_name, item_obj in new_inventory.items.items():
                if hasattr(item_obj, 'stashed'):
                    item_obj.stashed = True
                inventory.items[item_name] = item_obj
                pos = inventory.get_available_slots(item_obj)
                if pos:
                    item_obj.rect.topleft = pos
                    item_obj.position = pygame.Vector2(pos)

            # Safe room transition with music handling
            if loaded_room != active_room:
                pygame.mixer.music.stop()
                active_room = loaded_room
                last_room_for_autosave = active_room  # Update auto-save tracking
                pygame.mixer.music.load(active_room.music)
                pygame.mixer.music.set_volume(BACKGROUND_VOLUME)
                pygame.mixer.music.play(-1, 0.0)

            # Safe player positioning - validate loaded position with feet check
            player_x = max(0, min(player_pos.get("left", 100), SCREEN_WIDTH - 50))
            player_y = max(0, min(player_pos.get("top", 100), SCREEN_HEIGHT - INVENTORY_HEIGHT - 50))
            loaded_pos = pygame.Vector2(player_x, player_y)
            walkable_pos = active_room.find_nearest_walkable_spawn(loaded_pos)
            player.sprites()[0].rect.left = int(walkable_pos.x)
            player.sprites()[0].rect.top = int(walkable_pos.y)
            player.sprites()[0].pos = walkable_pos

            # Restore playtime and restart session timer
            playtime_seconds = loaded_playtime
            session_start_time = time.time()

            print(f"Game loaded from slot {slot_number} successfully! (Playtime: {playtime_seconds}s)")
            return True
        else:
            print(f"Failed to load from slot {slot_number}")
            return False

    def check_and_perform_autosave():
        """Auto-save to slot 0 when changing rooms."""
        nonlocal last_room_for_autosave
        if active_room != last_room_for_autosave:
            print(f"Room changed to {active_room.name} - Auto-saving...")
            perform_save(0)  # Slot 0 is auto-save
            last_room_for_autosave = active_room

    updatable = pygame.sprite.Group()
    pending_interaction = None
    interaction_target = None
    active_box = None
    active_click = None
    active_talker = None
    active_timer = 0
    last_click_time = 0
    last_click_target = None

    def queue_interaction(obj_or_qi, fast_walk=False):
        nonlocal pending_interaction, interaction_target, player, active_room
        pending_interaction = obj_or_qi
        target_obj = obj_or_qi.target if isinstance(obj_or_qi, QueuedInteraction) else obj_or_qi
        interaction_target = pygame.Vector2(target_obj.rect.centerx, target_obj.rect.centery)

        # Find nearest walkable point to the interaction target
        walkable_target = active_room.find_nearest_walkable(interaction_target)
        interaction_target = pygame.Vector2(walkable_target)

        assert player is not None
        for char in player.sprites():
            if fast_walk:
                char.enable_fast_walk()
            char.set_target(interaction_target)
        name = getattr(target_obj, "name", repr(target_obj))
        print(f"Queued {'FAST ' if fast_walk else ''}interaction with {name}")

        pchar = next(iter(player.sprites()))
        if (pchar.pos - interaction_target).length() <= INTERACTION_DISTANCE:
            try_execute_pending(force=True)

    def execute_base_interaction(obj):
        nonlocal active_room, active_timer, active_talker
        if isinstance(obj, Door):
            if obj.locked:
                print(f"Door locked: {obj.name}")
                obj.describe(active_room)
            else:
                print(f"Entering door: {obj.name}")
                # Fade transition
                transition.start_fade(fade_in=False)
                active_room = obj.target_room
                active_room.play()
                # Validate player spawn position - ensure feet will be walkable
                target_pos = pygame.Vector2(obj.player_target_position)
                walkable_spawn = active_room.find_nearest_walkable_spawn(target_pos)
                player_char.pos = pygame.Vector2(walkable_spawn)
                player_char.clear_target()
                transition.start_fade(fade_in=True)
                # Auto-save on room transition
                check_and_perform_autosave()
        elif isinstance(obj, Action):
            if obj.locked:
                print(f"Action locked: {obj.name}")
                obj.describe(active_room)
            else:
                print(f"Trigger action: {obj.name}")
                obj.action()
        elif isinstance(obj, NPC):
            print(f"Talk to NPC: {obj.name}")
            obj.talk(active_room, inventory, answerbox)

            # DialogBox now manages its own timing, no need to set active_timer
            active_talker = obj
        elif isinstance(obj, Item):
            print(f"Pickup item: {obj.name}")
            obj.stash(inventory, active_room)
            obj.action()

    def try_execute_pending(force=False):
        nonlocal pending_interaction
        if not pending_interaction:
            return
        target_obj = pending_interaction.target if isinstance(pending_interaction, QueuedInteraction) else pending_interaction
        pchar = next(iter(player.sprites()))
        dist = (pchar.pos - interaction_target).length()
        if force or dist <= INTERACTION_DISTANCE:
            for char in player.sprites():
                char.clear_target()
            qi = pending_interaction
            pending_interaction = None
            if isinstance(qi, QueuedInteraction):
                print(f"Executing queued action: {qi.description or qi.action_callable.__name__}")
                qi.action_callable(*qi.args)
            else:
                execute_base_interaction(qi)

    def queue_unlock_door(door, item, fast_walk=False):
        def _do():
            if door.locked:
                door.unlock(item)
            item.kill(inventory, Room.rooms)
        queue_interaction(QueuedInteraction(door, _do, description=f"Unlock {door.name} with {item.name}"), fast_walk=fast_walk)

    def queue_unlock_action(action, item, fast_walk=False):
        def _do():
            if action.locked:
                action.unlock(item)
            item.kill(inventory, Room.rooms)
        queue_interaction(QueuedInteraction(action, _do, description=f"Use {item.name} on {action.name}"), fast_walk=fast_walk)

    def queue_unlock_npc(npc, item, fast_walk=False):
        def _do():
            if npc.locked:
                npc.unlock(item, inventory)
            item.kill(inventory, Room.rooms)
        queue_interaction(QueuedInteraction(npc, _do, description=f"Give {item.name} to {npc.name}"), fast_walk=fast_walk)

    def draw_styled_inventory(surface, inventory_obj, hover_pos, dragged_item=None):
        """Draw the styled inventory."""
        inv_rect = (0, SCREEN_HEIGHT - INVENTORY_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT)
        inventory_renderer.render(surface, inventory_obj.items, inv_rect, hover_pos, dragged_item)

    def draw_styled_answerbox(surface, answerbox_obj, hover_pos):
        """Draw the styled answer box."""
        if answerbox_obj.state is None:
            return []

        answers_list = list(answerbox_obj.answers.values())
        ans_rect = (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - INVENTORY_HEIGHT, 500, INVENTORY_HEIGHT)
        return answer_renderer.render_answers(surface, answers_list, ans_rect, hover_pos)

    def draw_styled_hover(surface, text, pos):
        """Draw a styled hover tooltip."""
        if text:
            tooltip_renderer.render(surface, text, pos)

    # Dialog skip tracking
    last_dialog_skip_time = 0

    # Main game loop
    run = True
    while run:
        mouse_pos = pygame.mouse.get_pos()
        clicked = False
        events = pygame.event.get()  # Get events once, use everywhere

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        if game_state == GameState.MENU:
            # Menu handling
            action = menu.update(mouse_pos, clicked, events)
            menu.draw(screen)

            if action == "start_game":
                # Initialize game content first
                updatable, active_room, intro = init_game()

                # Start intro sequence first
                cutscene = intro
                game_state = GameState.CUTSCENE
            elif action == "load_game":
                # Open load menu from main menu
                game_state = GameState.LOAD_MENU
                load_menu = SaveLoadMenu(mode="load")
            elif action == "save_game":
                # Open save menu from in-game menu
                gameplay_screenshot = capture_thumbnail()  # Capture before menu
                game_state = GameState.SAVE_MENU
                save_menu = SaveLoadMenu(mode="save")
            elif action == "resume":
                # Resume gameplay from in-game menu
                game_state = GameState.PLAYING
                session_start_time = time.time()  # Restart timer
                menu = MainMenu(title, in_game=False)  # Reset menu for next time
            elif isinstance(action, tuple) and action[0] == "continue":
                # Continue from most recent save
                slot_num = action[1]
                print(f"Continuing from slot {slot_num}...")
                # Initialize game first
                updatable, active_room, intro = init_game()
                # Then load the save
                if perform_load(slot_num):
                    game_state = GameState.PLAYING
                    session_start_time = time.time()
                else:
                    # If load fails, just start new game
                    cutscene = intro
                    game_state = GameState.CUTSCENE
            elif action == "quit_to_menu":
                # Return to startup menu (reset game)
                update_playtime()
                state_manager.reset()
                game_state = GameState.MENU
                session_start_time = None
                menu = MainMenu(title, in_game=False)  # Startup menu
            elif action == "quit":
                run = False

        elif game_state == GameState.CUTSCENE:
            # Intro sequence handling
            cutscene.update(dt)
            cutscene.draw(screen)

            # Check for skip or continue
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                cutscene.done = True

            if clicked:
                slide = cutscene.slides[cutscene.current_slide] if cutscene.current_slide < len(cutscene.slides) else None
                if slide:
                    # Check if current slide is fully displayed
                    if cutscene.line_index >= len(slide["text"]) - 1 and cutscene.char_index >= len(slide["text"][-1]):
                        cutscene.next_slide()
                    else:
                        cutscene.skip_to_end()

            if cutscene.done:
                # Return to previous state (PLAYING for dynamic cutscenes, or PLAYING for intro)
                previous_state = state_manager.pop_state()
                game_state = previous_state if previous_state is not None else GameState.PLAYING
                transition.start_fade(fade_in=True)
                # Start session timer when entering gameplay
                if game_state == GameState.PLAYING and session_start_time is None:
                    session_start_time = time.time()

        elif game_state == GameState.SAVE_MENU:
            # Save menu handling
            if confirm_dialog:
                # Handle confirmation dialog
                result = confirm_dialog.update(mouse_pos, events)
                confirm_dialog.draw(screen)

                if result == "confirm":
                    # Execute the pending action
                    if pending_menu_action and pending_menu_action[0] == "overwrite":
                        slot_num = pending_menu_action[1]
                        if perform_save(slot_num, gameplay_screenshot):
                            save_menu.refresh_slots()
                            # Show success message
                            if slot_num == 0:
                                save_menu.show_success("Auto-save overwritten!")
                            else:
                                save_menu.show_success(f"Slot {slot_num} overwritten!")
                    confirm_dialog = None
                    pending_menu_action = None
                elif result == "cancel":
                    confirm_dialog = None
                    pending_menu_action = None
            else:
                # Normal save menu
                if save_menu is None:
                    save_menu = SaveLoadMenu(mode="save")

                action = save_menu.update(mouse_pos, events, dt)
                save_menu.draw(screen)

                if action == "cancel":
                    game_state = GameState.PLAYING
                    save_menu = None
                    gameplay_screenshot = None  # Clear screenshot
                    session_start_time = time.time()  # Restart session timer
                elif action and action[0] == "save":
                    slot_num = action[1]
                    if perform_save(slot_num, gameplay_screenshot):
                        save_menu.refresh_slots()
                        # Show success message and keep menu open
                        if slot_num == 0:
                            save_menu.show_success("Auto-save updated!")
                        else:
                            save_menu.show_success(f"Game saved to Slot {slot_num}!")
                elif action and action[0] == "confirm_overwrite":
                    pending_menu_action = ("overwrite", action[1])
                    confirm_dialog = ConfirmDialog("overwrite", action[1])
                elif action and action[0] == "confirm_delete":
                    pending_menu_action = ("delete", action[1])
                    confirm_dialog = ConfirmDialog("delete", action[1])

            # Also handle delete confirmations
            if confirm_dialog and pending_menu_action and pending_menu_action[0] == "delete":
                result = confirm_dialog.update(mouse_pos, events)
                if result == "confirm":
                    slot_num = pending_menu_action[1]
                    if DeleteSlot(slot_num):
                        save_menu.refresh_slots()
                        # Show success message
                        save_menu.show_success(f"Slot {slot_num} deleted!")
                    confirm_dialog = None
                    pending_menu_action = None
                elif result == "cancel":
                    confirm_dialog = None
                    pending_menu_action = None

        elif game_state == GameState.LOAD_MENU:
            # Load menu handling
            if confirm_dialog:
                # Handle confirmation dialog for delete
                result = confirm_dialog.update(mouse_pos, events)
                confirm_dialog.draw(screen)

                if result == "confirm":
                    if pending_menu_action and pending_menu_action[0] == "delete":
                        slot_num = pending_menu_action[1]
                        if DeleteSlot(slot_num):
                            load_menu.refresh_slots()
                            # Show success message
                            load_menu.show_success(f"Slot {slot_num} deleted!")
                    confirm_dialog = None
                    pending_menu_action = None
                elif result == "cancel":
                    confirm_dialog = None
                    pending_menu_action = None
            else:
                # Normal load menu
                if load_menu is None:
                    load_menu = SaveLoadMenu(mode="load")

                action = load_menu.update(mouse_pos, events, dt)
                load_menu.draw(screen)

                if action == "cancel":
                    # Return to menu or playing depending on context
                    if active_room is None:
                        game_state = GameState.MENU
                    else:
                        game_state = GameState.PLAYING
                        session_start_time = time.time()
                    load_menu = None
                elif action and action[0] == "load":
                    slot_num = action[1]
                    if perform_load(slot_num):
                        # Initialize game if loading from menu
                        if active_room:
                            game_state = GameState.PLAYING
                            session_start_time = time.time()
                        load_menu = None
                elif action and action[0] == "confirm_delete":
                    pending_menu_action = ("delete", action[1])
                    confirm_dialog = ConfirmDialog("delete", action[1])

        elif game_state == GameState.PLAYING:
            # Check for pending cutscenes first
            pending_cutscene = state_manager.get_pending_cutscene()
            if pending_cutscene is not None:
                # Save current state and transition to cutscene
                state_manager.push_state(GameState.PLAYING)
                cutscene = pending_cutscene
                game_state = GameState.CUTSCENE
                continue  # Skip normal PLAYING logic and handle cutscene

            # Update transition
            transition.update()

            # Dialog box cleanup
            for dialbox in DialogBox.dialogboxes[:]:
                if dialbox.room != active_room:
                    # Changed room - close dialog and stop voice
                    VoiceManager.stop_current_voice()
                    speaker = dialbox.state
                    if speaker is not None and hasattr(speaker, 'dialogline'):
                        speaker.dialogline = 0
                    dialbox.state = None
                    active_talker = None
                    dialbox.kill()
                elif time.time() - dialbox.timer > dialbox.dialog_duration:
                    # Timer expired - but DON'T close if answers are available or voice is still playing!
                    if answerbox.state is not None:
                        # Answers are showing - keep dialog open, just reset timer
                        dialbox.timer = time.time()
                        continue

                    # Keep dialog open if voice is still playing
                    if VoiceManager.is_voice_playing():
                        dialbox.timer = time.time()
                        continue

                    speaker = dialbox.state
                    if isinstance(speaker, NPC) and hasattr(speaker, 'dialog') and hasattr(speaker, 'active_dialog'):
                        try:
                            line = speaker.dialog[speaker.active_dialog]["line"]
                            if isinstance(line, list):
                                speaker.dialogline += 1
                                if speaker.dialogline >= len(line):
                                    # Array completed - end dialog
                                    speaker.dialogline = 0
                                    VoiceManager.stop_current_voice()
                                    dialbox.state = None
                                    active_talker = None
                                    dialbox.kill()
                                elif speaker.dialogline < len(line):
                                    # Continue with next line in array
                                    speaker.talk(active_room, inventory, answerbox)
                                    continue  # Don't kill dialog, continue with next line
                            else:
                                # Single line completed
                                VoiceManager.stop_current_voice()
                                dialbox.state = None
                                active_talker = None
                                dialbox.kill()
                        except (KeyError, AttributeError):
                            # If we can't access dialog structure, just close the dialog
                            VoiceManager.stop_current_voice()
                            dialbox.state = None
                            active_talker = None
                            dialbox.kill()
                    else:
                        # Non-NPC dialog (Action, Item, Player, "describe") completed
                        VoiceManager.stop_current_voice()
                        dialbox.state = None
                        active_talker = None
                        dialbox.kill()

            # Update all objects
            for updatable_object in updatable:
                updatable_object.update(dt)

            # Draw room
            assert active_room is not None
            active_room.draw(screen, inventory, answerbox)

            # Draw styled inventory or answer box
            assert answerbox is not None
            if answerbox.state is not None:
                answer_rects = draw_styled_answerbox(screen, answerbox, mouse_pos)
                # Update answer rects to match rendered positions
                answers_list = list(answerbox.answers.values())
                for i, answer in enumerate(answers_list):
                    if i < len(answer_rects):
                        answer.rect = answer_rects[i]
            else:
                draw_styled_inventory(screen, inventory, mouse_pos, active_box)

            # Draw dragged item at mouse position
            if active_box is not None and hasattr(active_box, 'image'):
                drag_size = 50
                scaled = pygame.transform.scale(active_box.image, (drag_size, drag_size))
                screen.blit(scaled, (mouse_pos[0] - drag_size // 2, mouse_pos[1] - drag_size // 2))

            # Draw hover tooltip
            hover_text = ""
            assert inventory is not None
            for box in list(active_room.items.values()) + list(inventory.items.values()) + list(active_room.doors.values()) + list(active_room.actions.values()) + list(active_room.npcs.values()):
                if box.rect.collidepoint(mouse_pos):
                    hover_text = box.name
                    break

            if hover_text:
                draw_styled_hover(screen, hover_text, mouse_pos)

            # Key handling
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                for drawable_room in Room.rooms.values():
                    if drawable_room == active_room:
                        drawable_room.shine(screen)

            # W key to toggle walkable area visualization
            if keys[pygame.K_w]:
                import constants
                constants.SHOW_WALKABLE_AREA = not constants.SHOW_WALKABLE_AREA
                status = "ON" if constants.SHOW_WALKABLE_AREA else "OFF"
                print(f"Walkable area visualization: {status}")
                pygame.time.wait(200)  # Debounce

            # Draw walkable area overlay if enabled
            import constants
            if constants.SHOW_WALKABLE_AREA:
                active_room.draw_walkable_overlay(screen)

            # G key to toggle debug grid
            if keys[pygame.K_g]:
                grid_status = debug_grid.toggle()
                status = "ON" if grid_status else "OFF"
                print(f"Debug grid: {status}")
                pygame.time.wait(200)  # Debounce

            # Draw debug grid if enabled
            if debug_grid.enabled:
                # Get player position
                player_position = None
                if player and len(player.sprites()) > 0:
                    pchar = next(iter(player.sprites()))
                    # Use the center-bottom of player sprite (their "feet")
                    player_position = (pchar.pos.x + pchar.rect.width // 2, pchar.pos.y + pchar.rect.height)
                debug_grid.draw(screen, pygame.mouse.get_pos(), player_position)

            # New save/load menu system (S and L keys)
            if keys[pygame.K_s]:
                update_playtime()  # Update playtime before entering save menu
                gameplay_screenshot = capture_thumbnail()  # Capture BEFORE menu opens
                game_state = GameState.SAVE_MENU
                save_menu = SaveLoadMenu(mode="save")
                print("Opening save menu...")

            if keys[pygame.K_l]:
                game_state = GameState.LOAD_MENU
                load_menu = SaveLoadMenu(mode="load")
                print("Opening load menu...")

            # Debug toggle (press D for debug info)
            if keys[pygame.K_d]:
                debug_inventory_state(inventory, "Manual Debug Check")
                print("Press T to toggle debug logging on/off")

            if keys[pygame.K_t]:
                debug_enabled = toggle_debug()
                print(f"Debug logging {'ON' if debug_enabled else 'OFF'}")

            if keys[pygame.K_ESCAPE]:
                # Open in-game menu (pause game)
                update_playtime()
                game_state = GameState.MENU
                menu = MainMenu(title, in_game=True)  # In-game menu
                session_start_time = None  # Pause timer

            # Mouse event handling
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Check if we should skip current dialog line
                        dialog_active = len(DialogBox.dialogboxes) > 0
                        current_time = time.time()

                        # Skip on ANY click during dialog, unless answers are showing or in cooldown
                        if dialog_active and answerbox.state is None:
                            # Check cooldown to prevent accidental double-clicks
                            if current_time - last_dialog_skip_time < DIALOG_SKIP_COOLDOWN:
                                continue  # Still in cooldown, ignore this click

                            # Stop any playing voice
                            VoiceManager.stop_current_voice()

                            # Check if we're on the last line of the dialog
                            for dialbox in DialogBox.dialogboxes:
                                if dialbox.room == active_room:
                                    speaker = dialbox.state
                                    is_last_line = False

                                    # Determine if this is the last line
                                    # Only NPCs have multi-line dialogs with the dialog/active_dialog structure
                                    if isinstance(speaker, NPC) and hasattr(speaker, 'dialog') and hasattr(speaker, 'active_dialog'):
                                        try:
                                            line = speaker.dialog[speaker.active_dialog]["line"]
                                            if isinstance(line, list):
                                                # Multi-line dialog: check if we're on the last line
                                                is_last_line = (speaker.dialogline >= len(line) - 1)
                                            else:
                                                # Single line dialog: always last line
                                                is_last_line = True
                                        except (KeyError, AttributeError):
                                            # If we can't access dialog structure, treat as last line
                                            is_last_line = True
                                    else:
                                        # Non-NPC dialog (Action, Item, Player, "describe"): always last line
                                        is_last_line = True

                                    if is_last_line:
                                        # Last line: close dialog immediately
                                        if isinstance(speaker, NPC) and hasattr(speaker, 'dialogline'):
                                            speaker.dialogline = 0
                                        dialbox.state = None
                                        active_talker = None
                                        dialbox.kill()
                                    else:
                                        # Not last line: force timer expiration to advance
                                        dialbox.timer = time.time() - active_timer - 1

                                    # Update last skip time to start cooldown
                                    last_dialog_skip_time = current_time

                            continue  # Skip normal click processing when skipping dialog

                    if event.button in (1, 3):
                        active_click = None  # Reset click tracking

                        # Priority order: Answers > Inventory > NPCs > Actions > Items > Doors
                        # Check answers first if dialog is active
                        if answerbox.state is not None:
                            for answer in answerbox.answers.values():
                                if answer.rect.collidepoint(event.pos):
                                    active_click = answer
                                    break

                        # Check inventory items (for dragging)
                        if active_click is None:
                            for box in list(inventory.items.values()):
                                if box.rect.collidepoint(event.pos):
                                    active_box = box
                                    active_click = box
                                    break

                        # Check room NPCs
                        if active_click is None:
                            for npc in active_room.npcs.values():
                                if npc.rect.collidepoint(event.pos):
                                    active_click = npc
                                    break

                        # Check room actions
                        if active_click is None:
                            for action in active_room.actions.values():
                                if action.rect.collidepoint(event.pos):
                                    active_click = action
                                    break

                        # Check room items
                        if active_click is None:
                            for box in list(active_room.items.values()):
                                if box.rect.collidepoint(event.pos):
                                    active_click = box
                                    break

                        # Check doors (lowest priority, often in background)
                        if active_click is None and answerbox.state is None:
                            for door in active_room.doors.values():
                                if door.rect.collidepoint(event.pos):
                                    active_click = door
                                    break

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # Handle dragged item drop
                        if active_box is not None:
                            drop_pos = event.pos
                            dropped = False

                            # Check if dropped on a door
                            for door in active_room.doors.values():
                                if door.rect.collidepoint(drop_pos):
                                    queue_unlock_door(door, active_box)
                                    dropped = True
                                    break

                            # Check if dropped on an action
                            if not dropped:
                                for action in active_room.actions.values():
                                    if action.rect.collidepoint(drop_pos):
                                        queue_unlock_action(action, active_box)
                                        dropped = True
                                        break

                            # Check if dropped on an NPC
                            if not dropped:
                                for npc in active_room.npcs.values():
                                    if npc.rect.collidepoint(drop_pos):
                                        queue_unlock_npc(npc, active_box)
                                        dropped = True
                                        break

                            # Check if dropped on another inventory item (combine)
                            if not dropped:
                                for item in list(inventory.items.values()):
                                    if item != active_box and item.rect.collidepoint(drop_pos):
                                        active_box.combine(item)
                                        dropped = True
                                        break

                            # Return to inventory if not used
                            if not dropped:
                                active_box.stash(inventory, active_room)

                            active_box = None

                        # Use active_click to execute action (ensures click start and end match)
                        if active_click is not None:
                            # Detect double-click
                            current_time = time.time()
                            is_double_click = False

                            if (active_click == last_click_target and
                                current_time - last_click_time < DOUBLE_CLICK_THRESHOLD):
                                is_double_click = True

                            # Update click tracking
                            last_click_time = current_time
                            last_click_target = active_click

                            if answerbox.state is not None and isinstance(active_click, Answer):
                                if active_click.rect.collidepoint(event.pos):
                                    active_talker = active_click.npc
                                    active_click.action()

                            elif isinstance(active_click, Door):
                                if active_click.rect.collidepoint(event.pos):
                                    queue_interaction(active_click, fast_walk=is_double_click)

                            elif isinstance(active_click, Action):
                                if active_click.rect.collidepoint(event.pos):
                                    queue_interaction(active_click, fast_walk=is_double_click)

                            elif isinstance(active_click, NPC):
                                if active_click.rect.collidepoint(event.pos):
                                    queue_interaction(active_click, fast_walk=is_double_click)

                            elif isinstance(active_click, Item) and active_click in active_room.items.values():
                                if active_click.rect.collidepoint(event.pos):
                                    queue_interaction(active_click, fast_walk=is_double_click)

                        # Move player to clicked position (if not in inventory area AND no dialog active)
                        # Don't move if: dialog box is showing, answer box is active, or we clicked something
                        dialog_active = len(DialogBox.dialogboxes) > 0 or answerbox.state is not None
                        if not dialog_active and active_click is None:
                            mouse = pygame.mouse.get_pos()
                            if mouse[1] < SCREEN_HEIGHT - INVENTORY_HEIGHT:
                                # Check if clicked position is walkable, if not find nearest walkable point
                                walkable_pos = active_room.find_nearest_walkable(mouse)
                                for char in player.sprites():
                                    char.disable_fast_walk()  # Reset to normal speed for ground clicks
                                    char.set_target(walkable_pos)
                                pending_interaction = None  # Cancel any queued interaction

                        active_click = None

                    if event.button == 3:
                        # Right-click to describe objects
                        if active_click is not None:
                            if isinstance(active_click, Door):
                                if active_click.rect.collidepoint(event.pos):
                                    active_talker = active_click
                                    active_click.describe(active_room)
                                    active_timer = 3

                            elif isinstance(active_click, Action):
                                if active_click.rect.collidepoint(event.pos):
                                    active_talker = active_click
                                    active_click.describe(active_room)
                                    active_timer = 3

                            elif isinstance(active_click, NPC):
                                if active_click.rect.collidepoint(event.pos):
                                    active_talker = active_click
                                    active_click.describe(active_room)
                                    if active_click.locked:
                                        sound = active_click.dialog["description"]["locked"]["sound"]
                                        active_timer = get_sound_duration(sound)
                                    else:
                                        sound = active_click.dialog["description"]["unlocked"]["sound"]
                                        active_timer = get_sound_duration(sound)

                            elif isinstance(active_click, Item):
                                if active_click.rect.collidepoint(event.pos):
                                    active_talker = active_click
                                    active_timer = 3
                                    active_click.describe(active_room)

                            active_click = None
                        active_box = None

                if event.type == pygame.MOUSEMOTION:
                    if active_box is not None:
                        active_box.move_ip(event.rel)

            # Only update player movement if no dialog is active
            dialog_active = len(DialogBox.dialogboxes) > 0 or answerbox.state is not None
            if not dialog_active:
                # Pass active_room to player update for walkable area validation
                for char in player.sprites():
                    char.update(dt, active_room)
                try_execute_pending()

            # Draw transition overlay
            transition.render(screen)

            # Draw debug grid on top of everything (if enabled)
            if debug_grid.enabled:
                # Get player position
                player_position = None
                if player and len(player.sprites()) > 0:
                    pchar = next(iter(player.sprites()))
                    # Use the center-bottom of player sprite (their "feet")
                    player_position = (pchar.pos.x + pchar.rect.width // 2, pchar.pos.y + pchar.rect.height)
                debug_grid.draw(screen, pygame.mouse.get_pos(), player_position)

        dt = clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
