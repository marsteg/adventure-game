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
    ChangePicture, LogText, UnlockDoor, AllowDestroy, GiveItem, TakeItem,
    DestroyItem, ActionChangeDialog, PlaySound
)
from npc import NPC
from dialogbox import DialogBox, get_sound_duration
from answerbox import AnswerBox
from answer import Answer
from save import SaveState, LoadState
from player import Player
from queueing import QueuedInteraction
from menu import MainMenu
from ui import (
    Colors, dialog_renderer, answer_renderer, inventory_renderer,
    tooltip_renderer, transition, draw_rounded_rect
)


class GameState:
    """Manages game state: menu, playing, paused, intro."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    INTRO = "intro"


class IntroSequence:
    """Displays the game's story intro with typewriter effect."""

    def __init__(self):
        self.slides = [
            {
                "title": "Grimwood Academy",
                "text": [
                    "Welcome to Grimwood Academy for the Magically Gifted...",
                    "...and their emotionally unavailable parents.",
                    "Where werewolf kids learn next to zombie toddlers. Health & Safety gave up years ago."
                ]
            },
            {
                "title": "You Are Morticia",
                "text": [
                    "You are Morticia - yes, THAT Morticia. Daughter of Death himself.",
                    "Dad wanted you to follow the family business. You wanted a gap year.",
                    "Compromise: Magic school. At least the cafeteria serves souls on Tuesdays."
                ]
            },
            {
                "title": "Something Is Wrong",
                "text": [
                    "But something dark lurks beneath the school's cheerful facade...",
                    "(Besides the literal dungeon. That's just the gym.)",
                    "Students whisper about the Order of the Crimson Moon. Teachers change the subject.",
                    "The Dean smiles too much. Nobody smiles that much without hiding something."
                ]
            },
            {
                "title": "Your Mission",
                "text": [
                    "Uncover the school's dark secret before it's too late.",
                    "Make friends. Make enemies. Make questionable life choices.",
                    "And maybe, just maybe, earn the right to leave this place...",
                    "",
                    "...for a trip to Wonderland. (Dad owes you big time.)"
                ]
            }
        ]
        self.current_slide = 0
        self.char_index = 0
        self.line_index = 0
        self.timer = 0
        self.char_delay = 35  # ms between characters
        self.line_delay = 800  # ms between lines
        self.waiting_for_line = False
        self.done = False
        self.font_title = None
        self.font_text = None
        self.skip_requested = False

    def _ensure_fonts(self):
        if self.font_title is None:
            self.font_title = pygame.font.Font(None, 52)
            self.font_text = pygame.font.Font(None, 32)

    def update(self, dt):
        if self.done:
            return

        self.timer += dt

        if self.waiting_for_line:
            if self.timer >= self.line_delay:
                self.timer = 0
                self.waiting_for_line = False
                self.line_index += 1
                self.char_index = 0

                slide = self.slides[self.current_slide]
                if self.line_index >= len(slide["text"]):
                    # Slide complete, wait for click
                    pass
        else:
            if self.timer >= self.char_delay:
                self.timer = 0
                slide = self.slides[self.current_slide]
                if self.line_index < len(slide["text"]):
                    current_line = slide["text"][self.line_index]
                    if self.char_index < len(current_line):
                        self.char_index += 1
                    else:
                        self.waiting_for_line = True

    def next_slide(self):
        """Move to next slide or mark as done."""
        self.current_slide += 1
        self.line_index = 0
        self.char_index = 0
        self.timer = 0
        self.waiting_for_line = False

        if self.current_slide >= len(self.slides):
            self.done = True

    def skip_to_end(self):
        """Skip current slide's text animation."""
        slide = self.slides[self.current_slide]
        self.line_index = len(slide["text"]) - 1
        self.char_index = len(slide["text"][self.line_index])

    def draw(self, surface):
        self._ensure_fonts()

        # Dark background
        surface.fill((8, 8, 12))

        if self.current_slide >= len(self.slides):
            return

        slide = self.slides[self.current_slide]

        # Title with accent color
        title_surf = self.font_title.render(slide["title"], True, (210, 175, 110))
        title_x = (SCREEN_WIDTH - title_surf.get_width()) // 2
        surface.blit(title_surf, (title_x, 120))

        # Decorative line under title
        line_width = min(title_surf.get_width() + 100, SCREEN_WIDTH - 200)
        pygame.draw.line(surface, (60, 55, 50), (SCREEN_WIDTH // 2 - line_width // 2, 180),
                         (SCREEN_WIDTH // 2 + line_width // 2, 180), 1)

        # Text lines
        y = 240
        for i, line in enumerate(slide["text"]):
            if i < self.line_index:
                # Fully displayed line
                text_surf = self.font_text.render(line, True, (200, 195, 190))
            elif i == self.line_index:
                # Currently typing line
                displayed = line[:self.char_index]
                text_surf = self.font_text.render(displayed, True, (235, 230, 225))
            else:
                # Not yet displayed
                continue

            text_x = (SCREEN_WIDTH - text_surf.get_width()) // 2
            surface.blit(text_surf, (text_x, y))
            y += 45

        # "Click to continue" prompt (only when slide text is complete)
        if self.line_index >= len(slide["text"]) - 1 and self.char_index >= len(slide["text"][-1]):
            prompt = "Click to continue..." if self.current_slide < len(self.slides) - 1 else "Click to begin your adventure..."
            prompt_surf = self.font_text.render(prompt, True, (120, 115, 110))
            prompt_x = (SCREEN_WIDTH - prompt_surf.get_width()) // 2
            surface.blit(prompt_surf, (prompt_x, SCREEN_HEIGHT - 100))

        # Skip hint
        skip_surf = pygame.font.Font(None, 22).render("Press SPACE to skip", True, (80, 75, 70))
        surface.blit(skip_surf, (SCREEN_WIDTH - skip_surf.get_width() - 20, SCREEN_HEIGHT - 30))


def main():
    pygame.init()
    pygame.display.set_caption('Adventure Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting Adventure Game!")

    clock = pygame.time.Clock()
    dt = 0

    # Game state
    game_state = GameState.MENU
    menu = MainMenu()
    intro = IntroSequence()

    # These will be initialized when game starts
    inventory = None
    answerbox = None
    player = None
    active_room = None
    rooms = {}

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

        Door.containers = (updatable, clickables)
        Item.containers = (updatable, items_group)
        Action.containers = (updatable, clickables)
        Inventory.containers = (updatable)
        Room.containers = (updatable)

        inventory = Inventory()
        answerbox = AnswerBox()

        daisy = Player(100, 100, 50, 75, "assets/player/daisy_waiting.png", "player")
        player = pygame.sprite.Group(daisy)

        # Rooms - The Academy and its secrets
        title = Room(player, "assets/rooms/TitleScreen.png", "title", "assets/sounds/background/Talkline7.wav")
        room1 = Room(player, "assets/rooms/RektorOffice.png", "DeansOffice", "assets/sounds/background/Albatros.wav")
        room2 = Room(player, "assets/rooms/LivingRoom.png", "MainHall", "assets/sounds/background/PrettyOrgan.wav")
        beach_bar = Room(player, "assets/rooms/BeachBar.png", "Courtyard", "assets/sounds/background/dancing_street.wav")
        library = Room(player, "assets/rooms/Library.png", "ForbiddenLibrary", "assets/sounds/background/PrettyOrgan.wav")
        secret_chamber = Room(player, "assets/rooms/SecretChamber.png", "SecretChamber", "assets/sounds/background/Talkline7.wav")
        storage = Room(player, "assets/rooms/LivingRoom.png", "StorageRoom", "assets/sounds/background/Albatros.wav")

        # Items - properly sized for easier clicking (minimum 45x45)
        missile = Item(100, 100, 50, 50, "assets/items/missile.png", "missile")
        missile2 = Item(at_percentage_width(70), at_percentage_height(75), 50, 50, "assets/items/missile2.png", "missile2", True)
        comb = Item(at_percentage_width(85), at_percentage_height(65), 50, 50, "assets/items/comb.png", "comb", True)
        herb = Item(300, 300, 50, 50, "assets/items/muckmuck_share.png", "herb", True)
        hay = Item(at_percentage_width(75), at_percentage_height(50), 60, 60, "assets/items/hay.png", "hay", True)
        book_of_truth = Item(at_percentage_width(20), at_percentage_height(70), 45, 45, "assets/items/bookoftruth.png", "BookofTruth", True)
        paper = Item(at_percentage_width(85), at_percentage_height(30), 35, 45, "assets/items/paper.png", "paper", True)

        # New items for library quest - well spaced positions
        ancient_scroll = Item(at_percentage_width(55), at_percentage_height(72), 45, 55, "assets/items/ancient_scroll.png", "AncientScroll", True)
        crystal_key = Item(200, 200, 50, 50, "assets/items/crystal_key.png", "CrystalKey", True)
        magic_amulet = Item(at_percentage_width(85), at_percentage_height(55), 50, 55, "assets/items/magic_amulet.png", "MagicAmulet", True)

        # Item descriptions - with sarcastic Morticia flavor
        missile.add_description("A gray key. Wolfgang traded it for something red. Werewolves are weird.", "assets/sounds/items/missile_locked.wav")
        missile2.add_description("Something red and shiny. Wolfgang would probably sell his soul for this. Actually, he might.", "assets/sounds/items/missile2_locked.wav")
        comb.add_description("A fancy comb. Lupin needs this for his 'fur crisis'. Werewolf problems.", "assets/sounds/items/comb_locked.wav")
        herb.add_description("A green herb from Raccoon City. Totally legal. Probably. Don't ask questions.", "assets/sounds/items/herb_locked.wav")
        hay.add_description("A haystack. Combine it with the herb for... science. Magical science.", "assets/sounds/items/hay_locked.wav")
        book_of_truth.add_description("The Book of Uncomfortable Facts. Chapter 1: Your childhood was a lie.", "assets/sounds/items/bookoftruth_locked.wav")
        paper.add_description("Magical paper made from combined items. Contains a clue about the Dean's schedule.", "assets/sounds/items/paper_locked.wav")

        # New item descriptions
        ancient_scroll.add_description("An ancient scroll the librarian wants. Knowledge is currency here. Capitalism even in academia.", "assets/sounds/items/paper_locked.wav")
        crystal_key.add_description("A Crystal Key that definitely opens something mysterious. Very Zelda-esque.", "assets/sounds/items/missile_locked.wav")
        magic_amulet.add_description("A pulsing amulet of doom. Or maybe it's just a fancy nightlight. Either way, pretty.", "assets/sounds/items/missile2_locked.wav")

        # Final item - the dark artifact (centered in secret chamber)
        dark_artifact = Item(at_percentage_width(50), at_percentage_height(50), 60, 70, "assets/items/dark_artifact.png", "DarkArtifact", False)
        dark_artifact.add_description("THE DARK ARTIFACT! Proof of the Dean's corruption! Netflix documentary incoming!", "assets/sounds/items/missile_locked.wav")

        # Additional items for expanded story
        old_key = Item(at_percentage_width(20), at_percentage_height(65), 45, 45, "assets/items/missile.png", "OldKey", True)
        old_key.add_description("A dusty old key. The janitor says it opens a shortcut. Janitors know everything.", "assets/sounds/items/missile_locked.wav")

        mysterious_note = Item(at_percentage_width(80), at_percentage_height(60), 40, 50, "assets/items/paper.png", "MysteriousNote", True)
        mysterious_note.add_description("A cryptic note: 'The Order watches.' Very dramatic. Very villain energy.", "assets/sounds/items/paper_locked.wav")

        # Actions - better positioned with larger hitboxes
        button1 = Action(at_percentage_width(50), at_percentage_height(30), 60, 60, "assets/actions/button.png", "button1", False, None)
        button2 = Action(at_percentage_width(40), at_percentage_height(35), 60, 60, "assets/actions/button2.png", "button2", True, missile)
        green_plant = Action(at_percentage_width(35), at_percentage_height(60), 60, 90, "assets/actions/greenplant.png", "GreenPlant", False, None)

        # Action descriptions - sarcastic style
        button1.add_description("A switch. Lupin said it opens the door. If he's wrong, I'm taking his comb back.", "The switch works! Lupin was actually useful. Mark the calendar.", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button1_locked.wav")
        button2.add_description("A mysterious button. Either opens something or launches a nuke. Only one way to find out.", "It makes a satisfying click. No nuke. Disappointing, honestly.", "assets/sounds/actions/button2_locked.wav", "assets/sounds/actions/button2_unlocked.wav")
        green_plant.add_description("A suspicious green plant. Muckmuck says to combine it with hay. I don't ask questions anymore.", "The plant looks slightly less suspicious now. Still wouldn't eat it.", "assets/sounds/items/greenplant_locked.wav", "assets/sounds/items/greenplant_locked.wav")

        # NPCs - larger hitboxes for easier clicking
        wolfboy = NPC(at_percentage_width(65), at_percentage_height(55), 150, 160, "assets/npcs/werewolfboy.png", "wolfboy", True, missile2, YELLOW, "assets/dialogs/wolfboy.yaml")
        wolfboy2 = NPC(at_percentage_width(35), at_percentage_height(55), 150, 160, "assets/npcs/werewolfboy.png", "wolfboy2", True, comb, WHITE, "assets/dialogs/wolfboy2.yaml")
        muckmuck = NPC(at_percentage_width(55), at_percentage_height(50), 100, 110, "assets/npcs/muckmuck_cool.png", "muckmuck", True, herb, GREEN, "assets/dialogs/muckmuck.yaml")

        # The mysterious Librarian - positioned on the left side of library
        librarian = NPC(at_percentage_width(25), at_percentage_height(50), 120, 160, "assets/npcs/librarian.png", "librarian", True, ancient_scroll, PURPLE, "assets/dialogs/librarian.yaml")

        # The nervous Janitor - knows secrets about the Order (in storage room)
        janitor = NPC(at_percentage_width(65), at_percentage_height(55), 100, 140, "assets/npcs/werewolfboy.png", "janitor", True, mysterious_note, WHITE, "assets/dialogs/janitor.yaml")

        # Doors - well positioned for each room
        room1_door1 = Door(at_percentage_width(5), at_percentage_height(45), 100, 200, "assets/doors/door1.png", "Room1Door1", beach_bar, True, missile)
        room1_door2 = Door(at_percentage_width(88), at_percentage_height(45), 100, 200, "assets/doors/door1.png", "Room1Door2", room2, True, button1)
        room2_door2 = Door(at_percentage_width(85), at_percentage_height(45), 100, 200, "assets/doors/door1.png", "Room2Door2", room1, False, None)
        title_door = Door(at_percentage_width(45), at_percentage_height(40), 120, 220, "assets/doors/door1.png", "Titledoor", room1, False, None)
        beach_bar_exit = Door(at_percentage_width(2), at_percentage_height(55), 100, 200, "assets/doors/door1.png", "BeachBarExit", title, False, None)

        # Library entrance door (in room2/living room) - on LEFT side
        room2_to_library = Door(at_percentage_width(5), at_percentage_height(45), 100, 180, "assets/doors/door1.png", "LibraryEntrance", library, False, None)

        # Library doors - exit on RIGHT, secret door in CENTER-RIGHT
        library_exit = Door(at_percentage_width(88), at_percentage_height(50), 100, 180, "assets/doors/door1.png", "LibraryExit", room2, False, None)
        secret_door = Door(at_percentage_width(60), at_percentage_height(45), 120, 180, "assets/doors/door1.png", "SecretDoor", secret_chamber, True, crystal_key)

        # Secret chamber - exit on left
        chamber_exit = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "ChamberExit", library, False, None)

        # Storage room door (from Dean's Office)
        storage_door = Door(at_percentage_width(50), at_percentage_height(70), 90, 150, "assets/doors/door1.png", "StorageDoor", storage, False, None)
        storage_exit = Door(at_percentage_width(50), at_percentage_height(45), 90, 150, "assets/doors/door1.png", "StorageExit", room1, False, None)

        # Door descriptions - Morticia's sarcastic commentary
        title_door.add_description("", "Grimwood Academy awaits. Dad said this would be 'character building'. Ugh.", "assets/sounds/doors/titledoor_unlocked.wav", "assets/sounds/doors/titledoor_unlocked.wav")
        room2_door2.add_description("", "Back to the Dean's Office. Where all the suspicion happens.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")
        room1_door1.add_description("Locked. I need a key. This is like every video game ever.", "The door to the Courtyard! Finally, some fresh air. And a bar, apparently.", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")
        room1_door2.add_description("Locked by some switch mechanism. Very Resident Evil. I love it.", "The switch worked! To the Main Hall!", "assets/sounds/doors/room1door2_locked.wav", "assets/sounds/doors/room1door2_unlocked.wav")
        beach_bar_exit.add_description("", "Back to the title screen. For when I need a break from this chaos.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        # New door descriptions
        room2_to_library.add_description("", "The FORBIDDEN Library. Very dramatic name. I approve.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")
        library_exit.add_description("", "Exit to Main Hall. In case books get too real.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")
        storage_door.add_description("", "The storage room. Where secrets and old mops go to die.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")
        storage_exit.add_description("", "Back to the Dean's boring office.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        # Secret door descriptions
        secret_door.add_description("A HIDDEN DOOR behind a bookshelf?! How cliche. How villainous. How... expected.", "It opens! Classic villain lair incoming. I bet there's torches.", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")
        chamber_exit.add_description("", "Back to the library. Less creepy, more books.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        # Action functions
        button1.add_function(ChangePicture, button1, "assets/actions/button2.png", "assets/actions/button.png", None)
        button1.add_function(LogText, "Text Logged")
        button1.add_function(UnlockDoor, button1, room1_door2)

        button2.add_function(ChangePicture, button2, "assets/actions/button.png", "assets/actions/button2.png", None)
        button2.add_function(LogText, "Useless Button pressed")
        button2.add_function(PlaySound, "assets/sounds/actions/grunz.wav")

        green_plant.add_function(GiveItem, herb, inventory)
        green_plant.add_function(LogText, "You took the herb from the plant")

        # NPC action functions
        wolfboy.add_function(GiveItem, missile, inventory)
        wolfboy.add_function(AllowDestroy, missile2)
        wolfboy.add_function(DestroyItem, missile2, inventory)
        wolfboy.add_function(ActionChangeDialog, wolfboy, "bye2")

        wolfboy2.add_function(ActionChangeDialog, wolfboy2, "bye")
        wolfboy2.add_function(AllowDestroy, comb)
        wolfboy2.add_function(TakeItem, comb, inventory)
        wolfboy2.add_function(UnlockDoor, button1, room1_door2)

        muckmuck.add_function(GiveItem, herb, inventory)
        muckmuck.add_function(LogText, "Muckmuck shared his herb with you")

        # Librarian functions - gives crystal key when unlocked
        librarian.add_function(GiveItem, crystal_key, inventory)
        librarian.add_function(AllowDestroy, ancient_scroll)
        librarian.add_function(DestroyItem, ancient_scroll, inventory)
        librarian.add_function(ActionChangeDialog, librarian, "success")
        librarian.add_function(LogText, "The librarian gave you the Crystal Key!")

        # Janitor functions - reveals secrets when given mysterious note
        janitor.add_function(GiveItem, paper, inventory)
        janitor.add_function(AllowDestroy, mysterious_note)
        janitor.add_function(DestroyItem, mysterious_note, inventory)
        janitor.add_function(ActionChangeDialog, janitor, "careful")
        janitor.add_function(LogText, "The janitor revealed important information about the Order!")

        # Item combinations
        hay.add_combination(herb)
        hay.add_combifunction(AllowDestroy, hay)
        hay.add_combifunction(AllowDestroy, herb)
        hay.add_combifunction(DestroyItem, hay, inventory)
        hay.add_combifunction(DestroyItem, herb, inventory)
        hay.add_combifunction(GiveItem, paper, inventory)

        # Assign objects to rooms
        title.doors[title_door.name] = title_door
        room2.doors[room2_door2.name] = room2_door2
        room1.doors[room1_door1.name] = room1_door1
        room1.doors[room1_door2.name] = room1_door2
        room1.npcs[wolfboy2.name] = wolfboy2
        room1.actions[button1.name] = button1
        room1.items[missile2.name] = missile2
        room1.items[comb.name] = comb
        room2.npcs[wolfboy.name] = wolfboy
        room2.actions[button2.name] = button2
        beach_bar.doors[beach_bar_exit.name] = beach_bar_exit
        beach_bar.npcs[muckmuck.name] = muckmuck
        beach_bar.items[hay.name] = hay
        beach_bar.actions[green_plant.name] = green_plant

        # Library room setup
        library.npcs[librarian.name] = librarian
        library.doors[library_exit.name] = library_exit
        library.doors[secret_door.name] = secret_door  # Secret door to chamber!
        library.items[magic_amulet.name] = magic_amulet

        # Secret chamber setup - the final room!
        secret_chamber.doors[chamber_exit.name] = chamber_exit
        secret_chamber.items[dark_artifact.name] = dark_artifact

        # Add door to library from room2, and ancient scroll to room1
        room2.doors[room2_to_library.name] = room2_to_library
        room1.items[ancient_scroll.name] = ancient_scroll

        # Storage room setup
        room1.doors[storage_door.name] = storage_door
        storage.doors[storage_exit.name] = storage_exit
        storage.items[old_key.name] = old_key
        storage.npcs[janitor.name] = janitor

        # Add some items to library for atmosphere
        library.items[book_of_truth.name] = book_of_truth
        library.items[mysterious_note.name] = mysterious_note

        rooms = Room.rooms
        active_room = title

        # Start music
        pygame.mixer.music.load(active_room.music)
        pygame.mixer.music.set_volume(BACKGROUND_VOLUME)
        pygame.mixer.music.play(-1, 0.0)

        return updatable, active_room

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
                action.unlock(item, inventory)
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
                # Start intro sequence first
                intro = IntroSequence()
                game_state = GameState.INTRO
            elif action == "quit":
                run = False

        elif game_state == GameState.INTRO:
            # Intro sequence handling
            intro.update(dt)
            intro.draw(screen)

            # Check for skip or continue
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                intro.done = True

            if clicked:
                slide = intro.slides[intro.current_slide] if intro.current_slide < len(intro.slides) else None
                if slide:
                    # Check if current slide is fully displayed
                    if intro.line_index >= len(slide["text"]) - 1 and intro.char_index >= len(slide["text"][-1]):
                        intro.next_slide()
                    else:
                        intro.skip_to_end()

            if intro.done:
                updatable, active_room = init_game()
                game_state = GameState.PLAYING
                transition.start_fade(fade_in=True)

        elif game_state == GameState.PLAYING:
            # Update transition
            transition.update()

            # Dialog box cleanup
            for dialbox in DialogBox.dialogboxes[:]:
                if dialbox.room != active_room:
                    # Changed room - close dialog
                    speaker = dialbox.state
                    if speaker is not None and hasattr(speaker, 'dialogline'):
                        speaker.dialogline = 0
                    dialbox.state = None
                    active_talker = None
                    dialbox.kill()
                elif time.time() - dialbox.timer > active_timer:
                    # Timer expired - but DON'T close if answers are available!
                    if answerbox.state is not None:
                        # Answers are showing - keep dialog open, just reset timer
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
                    dialbox.state = None
                    active_talker = None
                    dialbox.kill()

            # Update all objects
            for updatable_object in updatable:
                updatable_object.update(dt)

            # Draw room
            active_room.draw(screen, inventory, answerbox)

            # Draw styled inventory or answer box
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
                SaveState(active_room, inventory, "save.yaml")
            if keys[pygame.K_l]:
                loaded_room, new_inventory = LoadState("save.yaml")
                if loaded_room and new_inventory:
                    inventory.items = {}
                    inventory.items = new_inventory.items
                    active_room = loaded_room
            if keys[pygame.K_ESCAPE]:
                game_state = GameState.MENU

            # Mouse event handling
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
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
