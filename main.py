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

        # ============================================================
        # ROOMS - The Academy and its many secrets
        # ============================================================
        title = Room(player, "assets/rooms/TitleScreen.png", "title", "assets/sounds/background/Talkline7.wav")
        room1 = Room(player, "assets/rooms/RektorOffice.png", "DeansOffice", "assets/sounds/background/Albatros.wav")
        room2 = Room(player, "assets/rooms/LivingRoom.png", "MainHall", "assets/sounds/background/PrettyOrgan.wav")
        beach_bar = Room(player, "assets/rooms/BeachBar.png", "Courtyard", "assets/sounds/background/dancing_street.wav")
        library = Room(player, "assets/rooms/Library.png", "ForbiddenLibrary", "assets/sounds/background/PrettyOrgan.wav")
        secret_chamber = Room(player, "assets/rooms/SecretChamber.png", "SecretChamber", "assets/sounds/background/Talkline7.wav")
        storage = Room(player, "assets/rooms/LivingRoom.png", "StorageRoom", "assets/sounds/background/Albatros.wav")

        # NEW ROOMS - The Expanded Academy
        dormitory = Room(player, "assets/rooms/LivingRoom.png", "Dormitory", "assets/sounds/background/PrettyOrgan.wav")
        cafeteria = Room(player, "assets/rooms/BeachBar.png", "Cafeteria", "assets/sounds/background/dancing_street.wav")
        dungeon_gym = Room(player, "assets/rooms/SecretChamber.png", "DungeonGym", "assets/sounds/background/Talkline7.wav")
        clock_tower = Room(player, "assets/rooms/RektorOffice.png", "ClockTower", "assets/sounds/background/Albatros.wav")
        rooftop = Room(player, "assets/rooms/TitleScreen.png", "Rooftop", "assets/sounds/background/Talkline7.wav")
        basement = Room(player, "assets/rooms/SecretChamber.png", "Basement", "assets/sounds/background/Albatros.wav")
        greenhouse = Room(player, "assets/rooms/BeachBar.png", "Greenhouse", "assets/sounds/background/dancing_street.wav")
        teachers_lounge = Room(player, "assets/rooms/LivingRoom.png", "TeachersLounge", "assets/sounds/background/PrettyOrgan.wav")
        trophy_room = Room(player, "assets/rooms/RektorOffice.png", "TrophyRoom", "assets/sounds/background/Albatros.wav")
        final_confrontation = Room(player, "assets/rooms/SecretChamber.png", "FinalConfrontation", "assets/sounds/background/Talkline7.wav")

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

        # ============================================================
        # NEW ITEMS - Expanded Story
        # ============================================================

        # Dormitory Items
        ghost_glasses = Item(at_percentage_width(70), at_percentage_height(40), 50, 45, "assets/items/comb.png", "GhostGlasses", True)
        ghost_glasses.add_description("Spectral spectacles. Let you see invisible things. Or make you look pretentious. Both useful.", "assets/sounds/items/missile_locked.wav")

        student_diary = Item(at_percentage_width(25), at_percentage_height(75), 45, 55, "assets/items/paper.png", "StudentDiary", True)
        student_diary.add_description("Someone's diary. 'Day 47: Still no WiFi. Send help.' The real horror of magic school.", "assets/sounds/items/paper_locked.wav")

        broken_wand = Item(at_percentage_width(60), at_percentage_height(65), 45, 50, "assets/items/missile2.png", "BrokenWand", True)
        broken_wand.add_description("A snapped wand. Someone had a bad day. Or a very dramatic breakup.", "assets/sounds/items/missile2_locked.wav")

        # Cafeteria Items
        mystery_meat = Item(at_percentage_width(30), at_percentage_height(55), 55, 50, "assets/items/muckmuck_share.png", "MysteryMeat", True)
        mystery_meat.add_description("The cafeteria special. Don't ask what it is. Seriously. My lawyer advised me not to.", "assets/sounds/items/herb_locked.wav")

        cafeteria_pass = Item(at_percentage_width(75), at_percentage_height(45), 45, 55, "assets/items/paper.png", "CafeteriaPass", True)
        cafeteria_pass.add_description("VIP access to the kitchen. The chef will talk to anyone with this. Bribery works.", "assets/sounds/items/paper_locked.wav")

        enchanted_fork = Item(at_percentage_width(50), at_percentage_height(70), 40, 50, "assets/items/missile2.png", "EnchantedFork", True)
        enchanted_fork.add_description("A fork that always points to the nearest dessert. Finally, useful magic.", "assets/sounds/items/missile_locked.wav")

        # Dungeon Gym Items
        rusty_chain = Item(at_percentage_width(80), at_percentage_height(50), 55, 60, "assets/items/hay.png", "RustyChain", True)
        rusty_chain.add_description("Old chains from the 'exercise equipment'. Very medieval. Very concerning.", "assets/sounds/items/hay_locked.wav")

        gym_locker_key = Item(at_percentage_width(20), at_percentage_height(40), 45, 45, "assets/items/missile.png", "GymLockerKey", True)
        gym_locker_key.add_description("Opens the forbidden locker. Whatever's in there has been there since 1347.", "assets/sounds/items/missile_locked.wav")

        # Clock Tower Items
        clock_gear = Item(at_percentage_width(65), at_percentage_height(35), 60, 60, "assets/items/hay.png", "ClockGear", True)
        clock_gear.add_description("A gear from the clock mechanism. Time is money, and this is... metal.", "assets/sounds/items/hay_locked.wav")

        tower_key = Item(at_percentage_width(35), at_percentage_height(70), 50, 50, "assets/items/missile.png", "TowerKey", True)
        tower_key.add_description("Opens the top of the clock tower. Where all dramatic confrontations happen.", "assets/sounds/items/missile_locked.wav")

        time_crystal = Item(at_percentage_width(50), at_percentage_height(25), 55, 60, "assets/items/crystal_key.png", "TimeCrystal", True)
        time_crystal.add_description("A crystal that glows with temporal energy. Or it's just really shiny. Science is hard.", "assets/sounds/items/missile_locked.wav")

        # Greenhouse Items
        moonflower = Item(at_percentage_width(25), at_percentage_height(50), 50, 60, "assets/items/muckmuck_share.png", "Moonflower", True)
        moonflower.add_description("A flower that only blooms at midnight. Very goth. I approve.", "assets/sounds/items/herb_locked.wav")

        venus_flytrap_tooth = Item(at_percentage_width(70), at_percentage_height(65), 45, 50, "assets/items/missile2.png", "VenusFlytrapTooth", True)
        venus_flytrap_tooth.add_description("From a giant carnivorous plant. It tried to eat me. We're enemies now.", "assets/sounds/items/missile2_locked.wav")

        rare_seed = Item(at_percentage_width(85), at_percentage_height(40), 40, 45, "assets/items/hay.png", "RareSeed", True)
        rare_seed.add_description("A mysterious seed. Plant it and something grows. That's how seeds work. Allegedly.", "assets/sounds/items/hay_locked.wav")

        # Basement Items
        ancient_tome = Item(at_percentage_width(30), at_percentage_height(60), 50, 60, "assets/items/bookoftruth.png", "AncientTome", True)
        ancient_tome.add_description("A book bound in suspicious leather. The Order's secret history. Very expose-worthy.", "assets/sounds/items/bookoftruth_locked.wav")

        ritual_candle = Item(at_percentage_width(75), at_percentage_height(45), 40, 55, "assets/items/missile2.png", "RitualCandle", True)
        ritual_candle.add_description("Never goes out. Either magic or really good wax. Either way, useful for dramatic lighting.", "assets/sounds/items/missile2_locked.wav")

        basement_map = Item(at_percentage_width(50), at_percentage_height(75), 50, 55, "assets/items/paper.png", "BasementMap", True)
        basement_map.add_description("Shows secret passages. X marks the spot. Several spots, actually. Bad cartography.", "assets/sounds/items/paper_locked.wav")

        # Teachers Lounge Items
        faculty_badge = Item(at_percentage_width(40), at_percentage_height(50), 45, 50, "assets/items/missile.png", "FacultyBadge", True)
        faculty_badge.add_description("Makes you look official. Opens doors meant for adults. Basically a golden ticket.", "assets/sounds/items/missile_locked.wav")

        coffee_of_awakening = Item(at_percentage_width(80), at_percentage_height(60), 45, 55, "assets/items/muckmuck_share.png", "CoffeeOfAwakening", True)
        coffee_of_awakening.add_description("Magical coffee. One sip and you see the truth. Also, crippling caffeine addiction.", "assets/sounds/items/herb_locked.wav")

        detention_records = Item(at_percentage_width(20), at_percentage_height(35), 50, 60, "assets/items/paper.png", "DetentionRecords", True)
        detention_records.add_description("Every student the Dean has 'dealt with'. Some names are crossed out. Ominous.", "assets/sounds/items/paper_locked.wav")

        # Trophy Room Items
        cursed_trophy = Item(at_percentage_width(55), at_percentage_height(40), 55, 65, "assets/items/magic_amulet.png", "CursedTrophy", True)
        cursed_trophy.add_description("First place in the 1666 Dark Arts Championship. The winner 'retired' mysteriously.", "assets/sounds/items/missile2_locked.wav")

        founders_portrait = Item(at_percentage_width(30), at_percentage_height(65), 60, 70, "assets/items/bookoftruth.png", "FoundersPortrait", True)
        founders_portrait.add_description("The school founder. His eyes follow you. Literally. Very unsettling.", "assets/sounds/items/bookoftruth_locked.wav")

        # Rooftop Items
        gargoyle_eye = Item(at_percentage_width(70), at_percentage_height(35), 50, 50, "assets/items/crystal_key.png", "GargoyleEye", True)
        gargoyle_eye.add_description("Fell off a gargoyle. Or was given to me. Gargoyles are cryptic.", "assets/sounds/items/missile_locked.wav")

        weather_vane = Item(at_percentage_width(25), at_percentage_height(55), 55, 65, "assets/items/hay.png", "WeatherVane", True)
        weather_vane.add_description("Always points to danger. Currently spinning like crazy. That's... probably fine.", "assets/sounds/items/hay_locked.wav")

        # Final Items for the ending
        deans_journal = Item(at_percentage_width(50), at_percentage_height(50), 55, 65, "assets/items/bookoftruth.png", "DeansJournal", True)
        deans_journal.add_description("His plans! His schemes! His... surprisingly good handwriting. Evil, but organized.", "assets/sounds/items/bookoftruth_locked.wav")

        soul_contract = Item(at_percentage_width(30), at_percentage_height(45), 50, 55, "assets/items/paper.png", "SoulContract", True)
        soul_contract.add_description("The contract he used to trap students. Fine print is EVIL. Always read the fine print.", "assets/sounds/items/paper_locked.wav")

        proof_of_corruption = Item(at_percentage_width(70), at_percentage_height(55), 60, 70, "assets/items/magic_amulet.png", "ProofOfCorruption", True)
        proof_of_corruption.add_description("Everything needed to expose the Dean. Netflix documentary incoming. For real this time.", "assets/sounds/items/missile2_locked.wav")

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

        # ============================================================
        # NEW NPCs - Expanded Cast
        # ============================================================

        # Ghost Professor - haunts the Teachers Lounge, knows about the Order's history
        ghost_professor = NPC(at_percentage_width(40), at_percentage_height(45), 120, 150, "assets/npcs/librarian.png", "ghost_professor", True, faculty_badge, PURPLE, "assets/dialogs/ghost_professor.yaml")

        # Cafeteria Chef - a troll who serves questionable food, has info about secret meetings
        chef_gronk = NPC(at_percentage_width(50), at_percentage_height(55), 130, 160, "assets/npcs/muckmuck_cool.png", "chef_gronk", True, cafeteria_pass, GREEN, "assets/dialogs/chef_gronk.yaml")

        # Vampire Classmate - in the Dormitory, knows about students who "transferred"
        vampire_victoria = NPC(at_percentage_width(70), at_percentage_height(50), 110, 150, "assets/npcs/librarian.png", "vampire_victoria", True, student_diary, PURPLE, "assets/dialogs/vampire_victoria.yaml")

        # Ghost Student - in the Basement, was a victim of the Order
        ghost_timmy = NPC(at_percentage_width(35), at_percentage_height(60), 100, 130, "assets/npcs/werewolfboy.png", "ghost_timmy", True, ghost_glasses, WHITE, "assets/dialogs/ghost_timmy.yaml")

        # Greenhouse Keeper - a sentient plant, knows about the Moonflower ritual
        planty = NPC(at_percentage_width(60), at_percentage_height(45), 140, 170, "assets/npcs/muckmuck_cool.png", "planty", True, rare_seed, GREEN, "assets/dialogs/planty.yaml")

        # Clock Tower Guardian - an ancient golem, guards the Time Crystal
        tick_tock = NPC(at_percentage_width(50), at_percentage_height(40), 150, 180, "assets/npcs/werewolfboy.png", "tick_tock", True, clock_gear, YELLOW, "assets/dialogs/tick_tock.yaml")

        # Gym Coach - a minotaur, has the key to the forbidden locker
        coach_bull = NPC(at_percentage_width(65), at_percentage_height(50), 140, 170, "assets/npcs/muckmuck_cool.png", "coach_bull", True, rusty_chain, YELLOW, "assets/dialogs/coach_bull.yaml")

        # Trophy Room Curator - a talking portrait, knows the school's dark history
        sir_portrait = NPC(at_percentage_width(45), at_percentage_height(35), 100, 140, "assets/npcs/librarian.png", "sir_portrait", True, cursed_trophy, PURPLE, "assets/dialogs/sir_portrait.yaml")

        # The Dean - final boss, appears in the confrontation room
        dean_malvora = NPC(at_percentage_width(50), at_percentage_height(40), 140, 180, "assets/npcs/librarian.png", "dean_malvora", True, proof_of_corruption, PURPLE, "assets/dialogs/dean_malvora.yaml")

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

        # ============================================================
        # NEW DOORS - Connecting the expanded Academy
        # ============================================================

        # From Main Hall to new areas
        hall_to_dormitory = Door(at_percentage_width(50), at_percentage_height(25), 100, 160, "assets/doors/door1.png", "DormitoryDoor", dormitory, False, None)
        hall_to_dormitory.add_description("", "To the Dormitory. Where students sleep and secrets lurk.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        hall_to_cafeteria = Door(at_percentage_width(30), at_percentage_height(70), 100, 160, "assets/doors/door1.png", "CafeteriaDoor", cafeteria, False, None)
        hall_to_cafeteria.add_description("", "The Cafeteria. Abandon dietary expectations, all ye who enter.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        # Dormitory connections
        dorm_to_hall = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "DormToHall", room2, False, None)
        dorm_to_hall.add_description("", "Back to the Main Hall. Adulting awaits.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        dorm_to_rooftop = Door(at_percentage_width(88), at_percentage_height(30), 90, 140, "assets/doors/door1.png", "RooftopDoor", rooftop, True, tower_key)
        dorm_to_rooftop.add_description("Locked. I need a key. Probably leads somewhere dramatic.", "To the Rooftop! Where all dramatic things happen.", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")

        # Cafeteria connections
        cafe_to_hall = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "CafeToHall", room2, False, None)
        cafe_to_hall.add_description("", "Back to the Main Hall. Escaping the mystery meat.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        cafe_to_greenhouse = Door(at_percentage_width(88), at_percentage_height(45), 100, 160, "assets/doors/door1.png", "GreenhouseDoor", greenhouse, False, None)
        cafe_to_greenhouse.add_description("", "The Greenhouse. Where 'organic' gets scary.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        # Greenhouse connections
        green_to_cafe = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "GreenToCafe", cafeteria, False, None)
        green_to_cafe.add_description("", "Back to the Cafeteria. Where plants become food.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        # Courtyard connections to new areas
        court_to_gym = Door(at_percentage_width(88), at_percentage_height(45), 100, 160, "assets/doors/door1.png", "GymDoor", dungeon_gym, False, None)
        court_to_gym.add_description("", "The Dungeon Gym. PE stands for Pain Experience.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        court_to_tower = Door(at_percentage_width(50), at_percentage_height(20), 90, 180, "assets/doors/door1.png", "ClockTowerDoor", clock_tower, True, gym_locker_key)
        court_to_tower.add_description("Strange lock. Need a special key.", "The Clock Tower! Time to discover some truths. Get it? Time? I'll stop.", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")

        # Gym connections
        gym_to_court = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "GymToCourt", beach_bar, False, None)
        gym_to_court.add_description("", "Back to the Courtyard. Away from the gains.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        gym_to_basement = Door(at_percentage_width(50), at_percentage_height(75), 100, 140, "assets/doors/door1.png", "BasementDoor", basement, True, ancient_tome)
        gym_to_basement.add_description("Sealed with ancient magic. Need something powerful.", "The Basement. Definitely not creepy at all.", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")

        # Clock Tower connections
        tower_to_court = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "TowerToCourt", beach_bar, False, None)
        tower_to_court.add_description("", "Back to the Courtyard. My ears are ringing.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        # Rooftop connections
        roof_to_dorm = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "RoofToDorm", dormitory, False, None)
        roof_to_dorm.add_description("", "Back to the Dormitory. Away from the vertigo.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        # Basement connections
        base_to_gym = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "BaseToGym", dungeon_gym, False, None)
        base_to_gym.add_description("", "Back up to the Gym. Escaping the darkness.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        base_to_teachers = Door(at_percentage_width(88), at_percentage_height(45), 100, 160, "assets/doors/door1.png", "TeachersDoor", teachers_lounge, True, faculty_badge)
        base_to_teachers.add_description("Faculty Only. Need proper credentials.", "The Teachers Lounge! Where adults hide from students.", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")

        # Teachers Lounge connections
        teach_to_base = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "TeachToBase", basement, False, None)
        teach_to_base.add_description("", "Back to the creepy Basement.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        teach_to_trophy = Door(at_percentage_width(88), at_percentage_height(45), 100, 160, "assets/doors/door1.png", "TrophyDoor", trophy_room, False, None)
        teach_to_trophy.add_description("", "The Trophy Room. Past glory and past horrors.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        # Trophy Room connections
        trophy_to_teach = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "TrophyToTeach", teachers_lounge, False, None)
        trophy_to_teach.add_description("", "Back to the Teachers Lounge.", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        trophy_to_final = Door(at_percentage_width(50), at_percentage_height(25), 120, 180, "assets/doors/door1.png", "FinalDoor", final_confrontation, True, deans_journal)
        trophy_to_final.add_description("The Dean's secret entrance. Need undeniable proof.", "This is it. The final confrontation awaits.", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")

        # Final room exit (back to trophy room after confrontation)
        final_to_trophy = Door(at_percentage_width(5), at_percentage_height(50), 100, 160, "assets/doors/door1.png", "FinalToTrophy", trophy_room, False, None)
        final_to_trophy.add_description("", "Retreat! Strategic retreat!", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

        # Action functions
        button1.add_function(ChangePicture, button1, "assets/actions/button2.png", "assets/actions/button.png", None)
        button1.add_function(LogText, "Text Logged")
        button1.add_function(UnlockDoor, button1, room1_door2)

        button2.add_function(ChangePicture, button2, "assets/actions/button.png", "assets/actions/button2.png", None)
        button2.add_function(LogText, "Useless Button pressed")
        button2.add_function(PlaySound, "assets/sounds/actions/grunz.wav")

        green_plant.add_function(GiveItem, herb, inventory)
        green_plant.add_function(LogText, "You took the herb from the plant")

        # ============================================================
        # NEW ACTIONS - Interactive objects in new rooms
        # ============================================================

        # Dormitory - Broken mirror that reveals secrets
        broken_mirror = Action(at_percentage_width(80), at_percentage_height(35), 70, 90, "assets/actions/button.png", "BrokenMirror", True, ghost_glasses)
        broken_mirror.add_description("A cracked mirror. Shows nothing... or does it? Need special eyes.", "With the ghost glasses, I can see messages in the mirror! 'The Dean lies.'", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button1_locked.wav")
        broken_mirror.add_function(GiveItem, student_diary, inventory)
        broken_mirror.add_function(LogText, "The mirror revealed a hidden diary!")

        # Cafeteria - Suspicious pot that needs stirring
        mystery_pot = Action(at_percentage_width(40), at_percentage_height(55), 80, 80, "assets/actions/greenplant.png", "MysteryPot", True, enchanted_fork)
        mystery_pot.add_description("A bubbling pot. Smells like regret and... cinnamon?", "Stirring reveals a hidden compartment! Classic chef trick.", "assets/sounds/actions/button2_locked.wav", "assets/sounds/actions/button2_unlocked.wav")
        mystery_pot.add_function(GiveItem, cafeteria_pass, inventory)
        mystery_pot.add_function(LogText, "Found the VIP pass in the pot!")

        # Gym - Forbidden locker
        forbidden_locker = Action(at_percentage_width(75), at_percentage_height(40), 70, 100, "assets/actions/button2.png", "ForbiddenLocker", True, gym_locker_key)
        forbidden_locker.add_description("A locker covered in warning signs. Very inviting.", "Inside: old records! Students who 'graduated early'. Suspicious.", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button1_locked.wav")
        forbidden_locker.add_function(GiveItem, ancient_tome, inventory)
        forbidden_locker.add_function(LogText, "The locker contained forbidden knowledge!")

        # Clock Tower - Clock mechanism
        clock_mechanism = Action(at_percentage_width(50), at_percentage_height(55), 100, 100, "assets/actions/button.png", "ClockMechanism", True, clock_gear)
        clock_mechanism.add_description("The heart of the clock. Missing a gear.", "The clock works! It reveals a hidden compartment with a crystal!", "assets/sounds/actions/button2_locked.wav", "assets/sounds/actions/button2_unlocked.wav")
        clock_mechanism.add_function(GiveItem, time_crystal, inventory)
        clock_mechanism.add_function(LogText, "The Time Crystal was hidden in the clock!")

        # Greenhouse - Moonflower planter
        moonflower_pot = Action(at_percentage_width(35), at_percentage_height(60), 70, 80, "assets/actions/greenplant.png", "MoonflowerPot", True, rare_seed)
        moonflower_pot.add_description("An empty pot with lunar symbols. Needs a special seed.", "The Moonflower blooms! Its petals form a map to the Dean's study!", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button1_locked.wav")
        moonflower_pot.add_function(GiveItem, moonflower, inventory)
        moonflower_pot.add_function(LogText, "The Moonflower revealed secrets!")

        # Basement - Ritual circle
        ritual_circle = Action(at_percentage_width(50), at_percentage_height(70), 120, 80, "assets/actions/button.png", "RitualCircle", True, ritual_candle)
        ritual_circle.add_description("A dormant ritual circle. Needs to be activated.", "The circle glows! Shows visions of the Order's rituals. Creepy but informative.", "assets/sounds/actions/button2_locked.wav", "assets/sounds/actions/button2_unlocked.wav")
        ritual_circle.add_function(GiveItem, basement_map, inventory)
        ritual_circle.add_function(LogText, "The ritual circle revealed a map!")

        # Teachers Lounge - Coffee machine
        coffee_machine = Action(at_percentage_width(70), at_percentage_height(40), 60, 80, "assets/actions/button2.png", "CoffeeMachine", False, None)
        coffee_machine.add_description("Faculty coffee. Probably cursed. Definitely strong.", "The coffee reveals the truth! Also, I'm very awake now.", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button1_locked.wav")
        coffee_machine.add_function(GiveItem, coffee_of_awakening, inventory)
        coffee_machine.add_function(LogText, "Got magical coffee!")

        # Trophy Room - Suspicious painting
        suspicious_painting = Action(at_percentage_width(70), at_percentage_height(50), 80, 100, "assets/actions/button.png", "SuspiciousPainting", True, founders_portrait)
        suspicious_painting.add_description("The founder's eyes follow you. Literally. It's a magic painting.", "Swapping portraits reveals a safe! Very Scooby-Doo.", "assets/sounds/actions/button2_locked.wav", "assets/sounds/actions/button2_unlocked.wav")
        suspicious_painting.add_function(GiveItem, deans_journal, inventory)
        suspicious_painting.add_function(LogText, "Found the Dean's Journal!")

        # Rooftop - Gargoyle statue
        gargoyle_statue = Action(at_percentage_width(80), at_percentage_height(30), 80, 100, "assets/actions/button.png", "GargoyleStatue", True, gargoyle_eye)
        gargoyle_statue.add_description("A gargoyle missing an eye. Looks sad. Relateable.", "The gargoyle comes alive briefly, points to the Dean's window. Dramatic.", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button1_locked.wav")
        gargoyle_statue.add_function(GiveItem, tower_key, inventory)
        gargoyle_statue.add_function(LogText, "The gargoyle gave you a key!")

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

        # ============================================================
        # NEW NPC FUNCTIONS
        # ============================================================

        # Ghost Professor - gives faculty badge for accessing restricted areas
        ghost_professor.add_function(GiveItem, detention_records, inventory)
        ghost_professor.add_function(AllowDestroy, faculty_badge)
        ghost_professor.add_function(DestroyItem, faculty_badge, inventory)
        ghost_professor.add_function(ActionChangeDialog, ghost_professor, "helped")
        ghost_professor.add_function(LogText, "The Ghost Professor shared detention records!")

        # Chef Gronk - gives mystery meat and info
        chef_gronk.add_function(GiveItem, mystery_meat, inventory)
        chef_gronk.add_function(AllowDestroy, cafeteria_pass)
        chef_gronk.add_function(DestroyItem, cafeteria_pass, inventory)
        chef_gronk.add_function(ActionChangeDialog, chef_gronk, "fed")
        chef_gronk.add_function(LogText, "Chef Gronk shared some... food!")

        # Vampire Victoria - reveals student disappearance info
        vampire_victoria.add_function(GiveItem, broken_wand, inventory)
        vampire_victoria.add_function(AllowDestroy, student_diary)
        vampire_victoria.add_function(DestroyItem, student_diary, inventory)
        vampire_victoria.add_function(ActionChangeDialog, vampire_victoria, "trusting")
        vampire_victoria.add_function(LogText, "Victoria revealed secrets about missing students!")

        # Ghost Timmy - victim of the Order, has crucial testimony
        ghost_timmy.add_function(GiveItem, ritual_candle, inventory)
        ghost_timmy.add_function(AllowDestroy, ghost_glasses)
        ghost_timmy.add_function(DestroyItem, ghost_glasses, inventory)
        ghost_timmy.add_function(ActionChangeDialog, ghost_timmy, "visible")
        ghost_timmy.add_function(LogText, "Timmy's story is crucial evidence!")

        # Planty - greenhouse keeper, knows ritual ingredients
        planty.add_function(GiveItem, venus_flytrap_tooth, inventory)
        planty.add_function(AllowDestroy, rare_seed)
        planty.add_function(DestroyItem, rare_seed, inventory)
        planty.add_function(ActionChangeDialog, planty, "bloomed")
        planty.add_function(LogText, "Planty shared botanical secrets!")

        # Tick Tock - clock tower golem, guards time crystal
        tick_tock.add_function(GiveItem, clock_gear, inventory)
        tick_tock.add_function(AllowDestroy, clock_gear)
        tick_tock.add_function(ActionChangeDialog, tick_tock, "ticking")
        tick_tock.add_function(LogText, "Tick Tock accepted the gear!")

        # Coach Bull - minotaur gym teacher
        coach_bull.add_function(GiveItem, gym_locker_key, inventory)
        coach_bull.add_function(AllowDestroy, rusty_chain)
        coach_bull.add_function(DestroyItem, rusty_chain, inventory)
        coach_bull.add_function(ActionChangeDialog, coach_bull, "impressed")
        coach_bull.add_function(LogText, "Coach Bull was impressed by your strength!")

        # Sir Portrait - knows the school's dark history
        sir_portrait.add_function(GiveItem, founders_portrait, inventory)
        sir_portrait.add_function(AllowDestroy, cursed_trophy)
        sir_portrait.add_function(DestroyItem, cursed_trophy, inventory)
        sir_portrait.add_function(ActionChangeDialog, sir_portrait, "confessed")
        sir_portrait.add_function(LogText, "Sir Portrait revealed the founder's sins!")

        # Dean Malvora - final confrontation
        dean_malvora.add_function(GiveItem, soul_contract, inventory)
        dean_malvora.add_function(AllowDestroy, proof_of_corruption)
        dean_malvora.add_function(DestroyItem, proof_of_corruption, inventory)
        dean_malvora.add_function(ActionChangeDialog, dean_malvora, "defeated")
        dean_malvora.add_function(LogText, "THE DEAN HAS BEEN EXPOSED!")

        # Item combinations
        hay.add_combination(herb)
        hay.add_combifunction(AllowDestroy, hay)
        hay.add_combifunction(AllowDestroy, herb)
        hay.add_combifunction(DestroyItem, hay, inventory)
        hay.add_combifunction(DestroyItem, herb, inventory)
        hay.add_combifunction(GiveItem, paper, inventory)

        # ============================================================
        # NEW ITEM COMBINATIONS
        # ============================================================

        # Broken Wand + Time Crystal = Restored Wand (unlocks magic)
        broken_wand.add_combination(time_crystal)
        broken_wand.add_combifunction(AllowDestroy, broken_wand)
        broken_wand.add_combifunction(AllowDestroy, time_crystal)
        broken_wand.add_combifunction(DestroyItem, broken_wand, inventory)
        broken_wand.add_combifunction(DestroyItem, time_crystal, inventory)
        broken_wand.add_combifunction(GiveItem, proof_of_corruption, inventory)

        # Ancient Tome + Detention Records = Complete Evidence
        ancient_tome.add_combination(detention_records)
        ancient_tome.add_combifunction(AllowDestroy, ancient_tome)
        ancient_tome.add_combifunction(AllowDestroy, detention_records)
        ancient_tome.add_combifunction(DestroyItem, ancient_tome, inventory)
        ancient_tome.add_combifunction(DestroyItem, detention_records, inventory)
        ancient_tome.add_combifunction(GiveItem, deans_journal, inventory)

        # Moonflower + Ritual Candle = Illuminated Path
        moonflower.add_combination(ritual_candle)
        moonflower.add_combifunction(AllowDestroy, moonflower)
        moonflower.add_combifunction(AllowDestroy, ritual_candle)
        moonflower.add_combifunction(DestroyItem, moonflower, inventory)
        moonflower.add_combifunction(DestroyItem, ritual_candle, inventory)
        moonflower.add_combifunction(GiveItem, faculty_badge, inventory)

        # Mystery Meat + Coffee of Awakening = Truth Serum (for the Dean)
        mystery_meat.add_combination(coffee_of_awakening)
        mystery_meat.add_combifunction(AllowDestroy, mystery_meat)
        mystery_meat.add_combifunction(AllowDestroy, coffee_of_awakening)
        mystery_meat.add_combifunction(DestroyItem, mystery_meat, inventory)
        mystery_meat.add_combifunction(DestroyItem, coffee_of_awakening, inventory)
        mystery_meat.add_combifunction(GiveItem, soul_contract, inventory)

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

        # ============================================================
        # ASSIGN NEW OBJECTS TO NEW ROOMS
        # ============================================================

        # Main Hall - add doors to new areas
        room2.doors[hall_to_dormitory.name] = hall_to_dormitory
        room2.doors[hall_to_cafeteria.name] = hall_to_cafeteria

        # Dormitory setup
        dormitory.doors[dorm_to_hall.name] = dorm_to_hall
        dormitory.doors[dorm_to_rooftop.name] = dorm_to_rooftop
        dormitory.npcs[vampire_victoria.name] = vampire_victoria
        dormitory.items[ghost_glasses.name] = ghost_glasses
        dormitory.actions[broken_mirror.name] = broken_mirror

        # Cafeteria setup
        cafeteria.doors[cafe_to_hall.name] = cafe_to_hall
        cafeteria.doors[cafe_to_greenhouse.name] = cafe_to_greenhouse
        cafeteria.npcs[chef_gronk.name] = chef_gronk
        cafeteria.items[enchanted_fork.name] = enchanted_fork
        cafeteria.actions[mystery_pot.name] = mystery_pot

        # Greenhouse setup
        greenhouse.doors[green_to_cafe.name] = green_to_cafe
        greenhouse.npcs[planty.name] = planty
        greenhouse.items[rare_seed.name] = rare_seed
        greenhouse.items[venus_flytrap_tooth.name] = venus_flytrap_tooth
        greenhouse.actions[moonflower_pot.name] = moonflower_pot

        # Courtyard - add new doors
        beach_bar.doors[court_to_gym.name] = court_to_gym
        beach_bar.doors[court_to_tower.name] = court_to_tower

        # Dungeon Gym setup
        dungeon_gym.doors[gym_to_court.name] = gym_to_court
        dungeon_gym.doors[gym_to_basement.name] = gym_to_basement
        dungeon_gym.npcs[coach_bull.name] = coach_bull
        dungeon_gym.items[rusty_chain.name] = rusty_chain
        dungeon_gym.actions[forbidden_locker.name] = forbidden_locker

        # Clock Tower setup
        clock_tower.doors[tower_to_court.name] = tower_to_court
        clock_tower.npcs[tick_tock.name] = tick_tock
        clock_tower.items[clock_gear.name] = clock_gear
        clock_tower.actions[clock_mechanism.name] = clock_mechanism

        # Rooftop setup
        rooftop.doors[roof_to_dorm.name] = roof_to_dorm
        rooftop.items[gargoyle_eye.name] = gargoyle_eye
        rooftop.items[weather_vane.name] = weather_vane
        rooftop.actions[gargoyle_statue.name] = gargoyle_statue

        # Basement setup
        basement.doors[base_to_gym.name] = base_to_gym
        basement.doors[base_to_teachers.name] = base_to_teachers
        basement.npcs[ghost_timmy.name] = ghost_timmy
        basement.items[ritual_candle.name] = ritual_candle
        basement.items[basement_map.name] = basement_map
        basement.actions[ritual_circle.name] = ritual_circle

        # Teachers Lounge setup
        teachers_lounge.doors[teach_to_base.name] = teach_to_base
        teachers_lounge.doors[teach_to_trophy.name] = teach_to_trophy
        teachers_lounge.npcs[ghost_professor.name] = ghost_professor
        teachers_lounge.items[detention_records.name] = detention_records
        teachers_lounge.actions[coffee_machine.name] = coffee_machine

        # Trophy Room setup
        trophy_room.doors[trophy_to_teach.name] = trophy_to_teach
        trophy_room.doors[trophy_to_final.name] = trophy_to_final
        trophy_room.npcs[sir_portrait.name] = sir_portrait
        trophy_room.items[cursed_trophy.name] = cursed_trophy
        trophy_room.actions[suspicious_painting.name] = suspicious_painting

        # Final Confrontation Room
        final_confrontation.doors[final_to_trophy.name] = final_to_trophy
        final_confrontation.npcs[dean_malvora.name] = dean_malvora
        final_confrontation.items[soul_contract.name] = soul_contract

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
