import pygame
import time

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT, FPS, INTERACTION_DISTANCE,
    BACKGROUND_VOLUME, WHITE, YELLOW, GREEN, PURPLE, at_percentage_width, at_percentage_height
)
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
from save import SaveState, LoadState
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


def main():
    pygame.init()
    pygame.display.set_caption('Adventure Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting Adventure Game!")

    clock = pygame.time.Clock()
    dt = 0
    from game import get_metadata
    title, player_start_percent = get_metadata()
    pygame.display.set_caption(title)

    # Game state
    game_state = GameState.MENU
    menu = MainMenu(title)
    #intro = TextCutscene("assets/textcutscenes/intro.yaml")

    # Initialize GameStateManager
    state_manager = GameStateManager.get_instance()

    # These will be initialized when game starts
    inventory = None
    answerbox = None
    #player = None
    active_room = None
    rooms = {}
    daisy = Player(at_percentage_width(20), at_percentage_height(80), 50, 75, "assets/player/daisy_waiting.png", "player")
    player = pygame.sprite.Group(daisy)

    def init_game():
        """Initialize or reset the game."""
        nonlocal inventory, answerbox, player, active_room, rooms

        # Reset class-level containers
        Room.rooms = {}
        Item.items = {}
        NPC.NPCs = {}
        DialogBox.dialogboxes = []

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
        daisy.pos = pygame.Vector2(at_percentage_width(player_start_percent[0]), at_percentage_height(player_start_percent[1]))
        daisy.pos = pygame.Vector2(at_percentage_width(player_start_percent[0]), at_percentage_height(player_start_percent[1]))

        # Start music
        pygame.mixer.music.load(active_room.music)
        pygame.mixer.music.set_volume(BACKGROUND_VOLUME)
        pygame.mixer.music.play(-1, 0.0)

        return updatable, active_room, intro

    updatable = pygame.sprite.Group()
    pending_interaction = None
    interaction_target = None
    active_box = None
    active_click = None
    active_talker = None
    active_timer = 0

    def queue_interaction(obj_or_qi):
        nonlocal pending_interaction, interaction_target, player
        pending_interaction = obj_or_qi
        target_obj = obj_or_qi.target if isinstance(obj_or_qi, QueuedInteraction) else obj_or_qi
        interaction_target = pygame.Vector2(target_obj.rect.centerx, target_obj.rect.centery)
        assert player is not None
        for char in player.sprites():
            char.set_target(interaction_target)
        name = getattr(target_obj, "name", repr(target_obj))
        print(f"Queued interaction with {name}")

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
                daisy.pos = pygame.Vector2(obj.player_target_position)
                daisy.clear_target()
                transition.start_fade(fade_in=True)
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
            sound = obj.dialog[obj.active_dialog]["sound"]
            if isinstance(sound, list):
                sound = obj.dialog[obj.active_dialog]["sound"][obj.dialogline]
            duration = get_sound_duration(sound)
            active_timer = duration
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

    def queue_unlock_door(door, item):
        def _do():
            if door.locked:
                door.unlock(item)
            item.kill(inventory, Room.rooms)
        queue_interaction(QueuedInteraction(door, _do, description=f"Unlock {door.name} with {item.name}"))

    def queue_unlock_action(action, item):
        def _do():
            if action.locked:
                action.unlock(item)
            item.kill(inventory, Room.rooms)
        queue_interaction(QueuedInteraction(action, _do, description=f"Use {item.name} on {action.name}"))

    def queue_unlock_npc(npc, item):
        def _do():
            if npc.locked:
                npc.unlock(item, inventory)
            item.kill(inventory, Room.rooms)
        queue_interaction(QueuedInteraction(npc, _do, description=f"Give {item.name} to {npc.name}"))

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
            action = menu.update(mouse_pos, clicked)
            menu.draw(screen)

            if action == "start_game":
                # Initialize game content first
                updatable, active_room, intro = init_game()

                # Start intro sequence first
                # For intro, we don't push a previous state since we go to PLAYING afterwards
                cutscene = intro
                game_state = GameState.CUTSCENE
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
                elif time.time() - dialbox.timer > active_timer:
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
                    if isinstance(speaker, NPC):
                        line = speaker.dialog[speaker.active_dialog]["line"]
                        if isinstance(line, list):
                            speaker.dialogline += 1
                            if speaker.dialogline >= len(line):
                                speaker.dialogline = 0
                            elif speaker.dialogline < len(line):
                                speaker.talk(active_room, inventory, answerbox)
                                continue  # Don't kill dialog, continue with next line
                    # Stop voice when dialog ends naturally
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
            if keys[pygame.K_s]:
                SaveState(active_room, inventory, player, "save.yaml")
            if keys[pygame.K_l]:
                loaded_room, new_inventory, player_pos = LoadState("save.yaml")
                if loaded_room and new_inventory:
                    inventory.items = {}
                    inventory.items = new_inventory.items
                    active_room = loaded_room
                    player.sprites()[0].rect.left = player_pos.get("left", 100)
                    player.sprites()[0].rect.top = player_pos.get("top", 100)
                    
            if keys[pygame.K_ESCAPE]:
                # Reset state manager when returning to menu
                state_manager.reset()
                game_state = GameState.MENU

            # Mouse event handling
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Check if we should skip current voice line
                        dialog_active = len(DialogBox.dialogboxes) > 0
                        if dialog_active and VoiceManager.is_voice_playing():
                            # Skip current voice and advance dialog
                            VoiceManager.stop_current_voice()
                            # Force timer expiration to advance to next dialog/line
                            for dialbox in DialogBox.dialogboxes:
                                if dialbox.room == active_room:
                                    dialbox.timer = time.time() - active_timer - 1
                            continue  # Skip normal click processing when skipping voice

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
                            if answerbox.state is not None and isinstance(active_click, Answer):
                                if active_click.rect.collidepoint(event.pos):
                                    active_talker = active_click.npc
                                    active_click.action()

                            elif isinstance(active_click, Door):
                                if active_click.rect.collidepoint(event.pos):
                                    queue_interaction(active_click)

                            elif isinstance(active_click, Action):
                                if active_click.rect.collidepoint(event.pos):
                                    queue_interaction(active_click)

                            elif isinstance(active_click, NPC):
                                if active_click.rect.collidepoint(event.pos):
                                    queue_interaction(active_click)

                            elif isinstance(active_click, Item) and active_click in active_room.items.values():
                                if active_click.rect.collidepoint(event.pos):
                                    queue_interaction(active_click)

                        # Move player to clicked position (if not in inventory area AND no dialog active)
                        # Don't move if: dialog box is showing, answer box is active, or we clicked something
                        dialog_active = len(DialogBox.dialogboxes) > 0 or answerbox.state is not None
                        if not dialog_active and active_click is None:
                            mouse = pygame.mouse.get_pos()
                            if mouse[1] < SCREEN_HEIGHT - INVENTORY_HEIGHT:
                                for char in player.sprites():
                                    char.set_target(mouse)

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
                player.update(dt)
                try_execute_pending()

            # Draw transition overlay
            transition.render(screen)

        dt = clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
