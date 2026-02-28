# Lucky Luke's Olympic Blunders - Game Content
# Compatible with the existing main.py structure

from constants import WHITE, YELLOW, PURPLE
import actionfuncs
from room import Room
from npc import NPC
from item import Item
from action import Action
from door import Door
from textcutscene import TextCutscene

def get_metadata():
    title = "Lucky Luke's Olympic Blunders"
    player_start_position_percent = (23, 77)  # x and y starting position of player in percentage of screen width/height (0.3 means 30% across the screen)
    return title, player_start_position_percent


def create_game_content(player, inventory):
    """
    Creates Lucky Luke game content using existing engine patterns
    Returns: (rooms_dict, starting_room, intro)
    """

    intro = TextCutscene("assets/textcutscenes/intro.yaml")

    # Clear existing content
    Room.rooms = {}

    # =============================================================================
    # ROOM 1: GREEK TOURIST SHOP
    # =============================================================================
    tourist_shop = Room(player, "assets/rooms/TitleScreen.png", "Tourist Shop", "assets/sounds/background/Talkline7.wav", walkable_mask="assets/rooms/TitleScreen_mask.png")

    # =============================================================================
    # ROOM 2: ANCIENT TEMPLE
    # =============================================================================
    ancient_temple = Room(player, "assets/rooms/RektorOffice.png", "Ancient Temple", "assets/sounds/background/Albatros.wav")

    # =============================================================================
    # ROOM 3: UNDERWORLD ENTRANCE
    # =============================================================================
    underworld_entrance = Room(player, "assets/rooms/SecretChamber.png", "Underworld Entrance", "assets/sounds/background/PrettyOrgan.wav")

    # =============================================================================
    # ROOM 4: MOUNT OLYMPUS
    # =============================================================================
    mount_olympus = Room(player, "assets/rooms/MainHall.png", "Mount Olympus", "assets/sounds/background/dancing_street.wav")

    # =============================================================================
    # ITEMS
    # =============================================================================

    # Tourist Brochure - Gives hint about temple
    brochure = Item(115, 585, 40, 30, "assets/items/paper.png", "Tourist Brochure", True)
    brochure.add_description("A colorful brochure about ancient Greek sites", "assets/sounds/items/herb_locked.wav")

    # Golden Olive Branch - First mythical item needed
    olive_branch = Item(300, 250, 50, 60, "assets/items/ancient_scroll.png", "Golden Olive Branch", True)
    olive_branch.add_description("A shimmering branch from Athena's sacred tree", "assets/sounds/items/missile_locked.wav")

    # Silver Coin - Given by puzzle box, needed for Hermes
    silver_coin = Item(0, 0, 30, 30, "assets/items/crystal_key.png", "Silver Coin", True)
    silver_coin.add_description("An ancient drachma, still gleaming", "assets/sounds/items/missile2_locked.wav")

    # Pomegranate of Persephone - Second mythical item
    pomegranate = Item(150, 350, 45, 55, "assets/items/muckmuck_share.png", "Pomegranate of Persephone", True)
    pomegranate.add_description("A magical fruit that glows with underworld power", "assets/sounds/items/herb_locked.wav")

    # Ambrosia - Final reward item
    ambrosia = Item(300, 250, 50, 40, "assets/items/hay.png", "Divine Ambrosia", True)
    ambrosia.add_description("Food of the gods - Luke's reward for his 'heroic' journey", "assets/sounds/items/hay_locked.wav")

    # =============================================================================
    # NPCs (Define before Actions so they can be used as keys)
    # =============================================================================

    # Shopkeeper NPC - Starting character who gives quest
    shopkeeper = NPC(463, 396, 80, 120, "assets/npcs/janitor.png", "Dimitri", False, None, WHITE, "assets/dialogs/shopkeeper.yaml")

    # Oracle NPC - Gives cryptic but helpful advice
    oracle = NPC(500, 180, 100, 140, "assets/npcs/librarian.png", "Oracle of Delphi", False, None, PURPLE, "assets/dialogs/oracle.yaml")

    # Hermes NPC - Messenger god who helps for a price
    hermes = NPC(400, 200, 90, 130, "assets/npcs/lupin.png", "Hermes", True, silver_coin, YELLOW, "assets/dialogs/hermes.yaml")

    # Zeus NPC - Final boss/character who resolves the story
    zeus = NPC(500, 150, 120, 180, "assets/npcs/muckmuck_cool.png", "Zeus", False, None, YELLOW, "assets/dialogs/zeus.yaml")

    # =============================================================================
    # ACTIONS (NPCs defined above can now be used as keys)
    # =============================================================================

    # Ancient Vase - The item Luke will accidentally break
    ancient_vase = Action(406, 601, 20, 70, "assets/actions/button.png", "Ancient Vase", False, None)
    ancient_vase.add_description("A priceless ancient Greek vase", "Oh no! You broke it!", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button2_unlocked.wav")

    # Ancient Puzzle Box - Requires brochure to solve
    puzzle_box = Action(700, 300, 70, 70, "assets/actions/button2.png", "Ancient Puzzle Box", True, brochure)
    puzzle_box.add_description("A mysterious box with Greek symbols. You need instructions.", "Following the brochure, you solve the puzzle!", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button2_unlocked.wav")

    # Charon's Boat - Action to get to Olympus (unlocked by Hermes)
    boat = Action(600, 350, 120, 80, "assets/actions/greenplant.png", "Charon's Boat", True, hermes)
    boat.add_description("Charon won't let you aboard without proper payment", "All aboard for Mount Olympus!", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button2_unlocked.wav")

    # Golden Throne - Easter egg action
    throne = Action(450, 250, 100, 120, "assets/actions/button.png", "Zeus's Throne", False, None)
    throne.add_description("You probably shouldn't sit on Zeus's throne...", "Luke accidentally sits down - lightning flashes but nothing bad happens!", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button2_unlocked.wav")


    # =============================================================================
    # DOORS
    # =============================================================================

    # Door to Temple (initially locked until vase is broken)
    temple_door = Door(520, 405, 100, 150, None, "Temple Entrance", ancient_temple, (100, 400), True, ancient_vase)
    temple_door.add_description("A passage to the ancient temple. Locked until something dramatic happens.", "To the Ancient Temple!", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")

    # Door to Underworld (unlocked by puzzle box)
    underworld_door = Door(650, 400, 80, 100, "assets/doors/door1.png", "Underworld Passage", underworld_entrance, (200, 300), True, puzzle_box)
    underworld_door.add_description("A mystical passage opened by solving the puzzle", "Into the Underworld!", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")

    # Door to Olympus (unlocked by boat action)
    olympus_door = Door(700, 300, 80, 100, "assets/doors/door1.png", "Olympus Gateway", mount_olympus, (300, 400), True, boat)
    olympus_door.add_description("The gateway to Mount Olympus", "To the realm of the gods!", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")

    # Return doors
    shop_return = Door(50, 350, 80, 120, "assets/doors/door1.png", "Shop Return", tourist_shop, (504, 490), False, None)
    shop_return.add_description("", "Back to the tourist shop", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

    temple_return = Door(50, 300, 80, 120, "assets/doors/door1.png", "Temple Return", ancient_temple, (650, 400), False, None)
    temple_return.add_description("", "Back to the temple", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

    # =============================================================================
    # ACTION FUNCTIONS
    # =============================================================================

    # Ancient Vase functions
    ancient_vase.add_function(actionfuncs.LogText, "Luke accidentally bumps the vase!")
    ancient_vase.add_function(actionfuncs.PlaySound, "assets/sounds/actions/grunz.wav")
    ancient_vase.add_function(actionfuncs.ChangePicture, ancient_vase, "assets/actions/button2.png", "assets/actions/button.png", None)
    ancient_vase.add_function(actionfuncs.UnlockDoor, ancient_vase, temple_door)


    # Puzzle Box functions
    puzzle_box.add_function(actionfuncs.LogText, "The box opens, revealing a secret passage!")
    puzzle_box.add_function(actionfuncs.PlaySound, "assets/sounds/actions/grunz.wav")
    puzzle_box.add_function(actionfuncs.UnlockDoor, puzzle_box, underworld_door)
    puzzle_box.add_function(actionfuncs.GiveItem, silver_coin, inventory)
    puzzle_box.add_function(actionfuncs.PlayTextCutScene, "assets/textcutscenes/puzzle_solved.yaml")

    # Boat functions
    boat.add_function(actionfuncs.LogText, "Luke trips getting in but somehow lands perfectly!")
    boat.add_function(actionfuncs.PlaySound, "assets/sounds/actions/grunz.wav")
    boat.add_function(actionfuncs.UnlockDoor, boat, olympus_door)

    # Throne functions
    throne.add_function(actionfuncs.LogText, "Zeus laughs: 'You have courage, mortal!'")
    throne.add_function(actionfuncs.PlaySound, "assets/sounds/actions/grunz.wav")

    # Hermes functions - unlock boat when given silver coin
    hermes.add_function(actionfuncs.UnlockAction, hermes, boat)
    hermes.add_function(actionfuncs.LogText, "Hermes: 'The boat is ready for your divine journey!'")

    # =============================================================================
    # ASSIGN OBJECTS TO ROOMS (using existing syntax)
    # =============================================================================

    # Tourist Shop
    tourist_shop.npcs[shopkeeper.name] = shopkeeper
    tourist_shop.items[brochure.name] = brochure
    tourist_shop.actions[ancient_vase.name] = ancient_vase
    tourist_shop.doors[temple_door.name] = temple_door

    # Ancient Temple
    ancient_temple.npcs[oracle.name] = oracle
    ancient_temple.items[olive_branch.name] = olive_branch
    ancient_temple.actions[puzzle_box.name] = puzzle_box
    ancient_temple.doors[shop_return.name] = shop_return
    ancient_temple.doors[underworld_door.name] = underworld_door

    # Underworld Entrance
    underworld_entrance.npcs[hermes.name] = hermes
    underworld_entrance.items[pomegranate.name] = pomegranate
    underworld_entrance.actions[boat.name] = boat
    underworld_entrance.doors[temple_return.name] = temple_return
    underworld_entrance.doors[olympus_door.name] = olympus_door

    # Mount Olympus
    mount_olympus.npcs[zeus.name] = zeus
    mount_olympus.items[ambrosia.name] = ambrosia
    mount_olympus.actions[throne.name] = throne

    print(intro.slides)

    return Room.rooms, tourist_shop, intro