import pygame
import random
from constants import *
from item import *
from inventory import *
from room import *
from door import *
from action import *
from actionfuncs import *
from npc import *
from dialogbox import *
from answerbox import *
from save import *
import time
import wave
import contextlib

def main():
    pygame.init()
    pygame.display.set_caption('Adventure')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting Adventure Game!")
    print("Screen width: " + str(SCREEN_WIDTH))
    print("Screen height: " + str(SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    
    items = pygame.sprite.Group()
    clickables = pygame.sprite.Group()   
    Door.containers = (updatable, clickables)
    Item.containers = (updatable, items)
    Action.containers = (updatable, clickables)
    Inventory.containers = (updatable)
    inventory = Inventory()

    Room.containers = (updatable)

    answerbox = AnswerBox()

    # title screen
    title = Room("assets/rooms/TitleScreen.png", "title", "assets/sounds/background/Talkline7.wav")
   

    # room and door and item assignments specifics...
    # rooms require nothing
    room1 = Room("assets/rooms/RektorOffice.png", "room1", "assets/sounds/background/Albatros.wav")
    room2 = Room("assets/rooms/LivingRoom.png", "room2", "assets/sounds/background/PrettyOrgan.wav")
    BeachBar = Room("assets/rooms/BeachBar.png", "BeachBar", "assets/sounds/background/dancing_street.wav")
    
    # items require nothing (should require rooms and self-register?)
    missile = Item(100, 100, 50, 50, "assets/items/missile.png", "missile") # should come back to inventory
    missile2 = Item(200, 200, 50, 50, "assets/items/missile2.png", "missile2", True) # should self destruct
    comb = Item(at_percentage_width(88), at_percentage_height(80), 50, 50, "assets/items/comb.png", "comb", True) # should self destruct
    herb = Item(300, 300, 50, 50, "assets/items/muckmuck_share.png", "herb", True) # should self destruct
    hay = Item(at_percentage_width(88), at_percentage_height(40), 60, 60, "assets/items/hay.png", "hay", True) # should self destruct
    BookofTruth = Item(at_percentage_width(85), at_percentage_height(30), 30, 30, "assets/items/bookoftruth.png", "BookofTruth", True) # should self destruct
    Paper = Item(at_percentage_width(85), at_percentage_height(30), 20, 30, "assets/items/paper.png", "paper", True) # should self destruct

    # adding item descriptions
    missile.add_description("A durable key. I wonder what Door it is for?", "assets/sounds/items/missile_locked.wav")
    missile2.add_description("A Red shiny thing. Is it a Key?", "assets/sounds/items/missile2_locked.wav")
    comb.add_description("A comb... What is this doing here?", "assets/sounds/items/comb_locked.wav")
    herb.add_description("A herb. It smells like Muckmuck", "assets/sounds/items/herb_locked.wav")
    hay.add_description("A haystack. It smells like a farm", "assets/sounds/items/hay_locked.wav")
    BookofTruth.add_description("The Book I found in the Library. It looks like it is important", "assets/sounds/items/bookoftruth_locked.wav")
    Paper.add_description("A piece of paper, torn from the Book of Truth. The page is about a spell of never ending sleep.", "assets/sounds/items/paper_locked.wav")


    # actions might require items
    button1 = Action(800, 100, 50, 50, "assets/actions/button.png", "button1", False, None)
    button2 = Action(400, 100, 50, 50, "assets/actions/button2.png", "button2", True, missile)
    GreenPlant = Action(at_percentage_width(30), at_percentage_height(50), 50, 80, "assets/actions/greenplant.png", "GreenPlant", False, None) 

    # adding action descriptions
    button1.add_description("I think this switch opens the door", "I think this switch opens the door", "assets/sounds/actions/button1_locked.wav", "assets/sounds/actions/button1_locked.wav")
    button2.add_description("A button. I wonder what it does?", "Great, it can turn on and off...", "assets/sounds/actions/button2_locked.wav", "assets/sounds/actions/button2_unlocked.wav")
    GreenPlant.add_description("The green plant, this strange Owl owns. It smells curious." ,"The green plant, this strange Owl owns. It smells curious.", "assets/sounds/items/greenplant_locked.wav" , "assets/sounds/items/greenplant_locked.wav")

    # NPCs might require Items
    wolfboy = NPC(750, 350, 150, 160, "assets/npcs/werewolfboy.png", "wolfboy", True, missile2, YELLOW, "assets/dialogs/wolfboy.yaml")
    wolfboy2 = NPC(350, 350, 150, 160, "assets/npcs/werewolfboy.png", "wolfboy2", True, comb, WHITE, "assets/dialogs/wolfboy2.yaml")
    muckmuck = NPC(SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2-100, 80, 90, "assets/npcs/muckmuck_cool.png", "muckmuck", True, herb, GREEN, "assets/dialogs/muckmuck.yaml")
    
    # NPCs get their description from the dialog yaml file 

    # doors require rooms and might require items
    Room1door1 = Door(80, 300, 100, 200, "assets/doors/door1.png", "Room1Door1", BeachBar, True, missile)
    Room1door2 = Door(880, 300, 100, 200, "assets/doors/door1.png", "Room1Door2",room2, True, button1)
    Room2door2 = Door(480, 300, 100, 200, "assets/doors/door1.png", "Room2Door2",room1, False, None)
    titledoor = Door(300, 300, 100, 200, "assets/doors/door1.png", "Titledoor", room1, False, None)
    BeachBarExit = Door(0, at_percentage_height(80), 100, 200, "assets/doors/door1.png", "BeachBarExit", title, False, None)

    # adding door descriptions
    titledoor.add_description("", "This is where the Adventure begins!", "assets/sounds/doors/titledoor_unlocked.wav", "assets/sounds/doors/titledoor_unlocked.wav")
    Room2door2.add_description("", "This leads back to the Dean's Office", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")
    Room1door1.add_description("I wonder where this Door leads to... it smells amazing in there!", "Finally! The last Door unlocked! What Mysteries might await me?", "assets/sounds/doors/room1door1_locked.wav", "assets/sounds/doors/room1door1_unlocked.wav")
    Room1door2.add_description("This Door does not look inviting at all...", "Do I really want to go in there?", "assets/sounds/doors/room1door2_locked.wav", "assets/sounds/doors/room1door2_unlocked.wav")
    BeachBarExit.add_description("", "This is where the Adventure ends!", "assets/sounds/doors/room2door2_unlocked.wav", "assets/sounds/doors/room2door2_unlocked.wav")

   # action funcs require items, doors, and actions
    button1.add_function(ChangePicture, button1, "assets/actions/button2.png", "assets/actions/button.png", None) 
    button1.add_function(LogText, "Text Logged")
    button1.add_function(UnlockDoor, button1, Room1door2)

    button2.add_function(ChangePicture, button2, "assets/actions/button.png", "assets/actions/button2.png", None)
    button2.add_function(LogText, "Useless Button pressed")
    button2.add_function(PlaySound, "assets/sounds/actions/grunz.wav")

    GreenPlant.add_function(GiveItem, herb, inventory)
    GreenPlant.add_function(LogText, "You took the herb from the plant")

    #NPCs action funcs
    wolfboy.add_function(GiveItem, missile, inventory)
    wolfboy.add_function(AllowDestroy, missile2)
    wolfboy.add_function(DestroyItem, missile2, inventory)
    wolfboy.add_function(ActionChangeDialog, wolfboy, "bye2")
    
    wolfboy2.add_function(ActionChangeDialog, wolfboy2, "bye")
    wolfboy2.add_function(AllowDestroy, comb)
    wolfboy2.add_function(TakeItem, comb, inventory)
    wolfboy2.add_function(UnlockDoor, button1, Room1door2)

    muckmuck.add_function(GiveItem, herb, inventory)
    muckmuck.add_function(LogText, "Muckmuck shared his herb with you")

    # item action funcs (executed when picked up)

    # item action funcs when combining items
    # combinable items 
    hay.add_combination(herb)
    hay.add_combifunction(AllowDestroy, hay)
    hay.add_combifunction(AllowDestroy, herb)
    hay.add_combifunction(DestroyItem, hay, inventory)
    hay.add_combifunction(DestroyItem, herb, inventory)
    hay.add_combifunction(GiveItem, Paper, inventory)
    
  # appendings doors, items and actions to rooms
    title.doors[titledoor.name] = titledoor
    room2.doors[Room2door2.name] = Room2door2
    room1.doors[Room1door1.name] = Room1door1
    room1.doors[Room1door2.name] = Room1door2
    room1.npcs[wolfboy2.name] = wolfboy2
    room1.actions[button1.name] = button1
    room1.items[missile2.name] = missile2
    room1.items[comb.name] = comb
    room1.items[BookofTruth.name] = BookofTruth
    room2.npcs[wolfboy.name] = wolfboy
    room2.actions[button2.name] = button2
    BeachBar.doors[BeachBarExit.name] = BeachBarExit
    BeachBar.npcs[muckmuck.name] = muckmuck
    BeachBar.items[hay.name] = hay
    BeachBar.actions[GreenPlant.name] = GreenPlant


    # initial state
    active_room = title
    pygame.mixer.music.load(active_room.music)
    pygame.mixer.music.set_volume(BACKGROUND_VOLUME)
    pygame.mixer.music.play(-1,0.0)
    active_box = None
    active_click = None
    active_talker = None
    active_timer = 0
    last_active_click = None
    
    
    # game loop start
    run = True
    while run:
      #eval_dialboxes(active_room, active_timer, inventory, answerbox)
      for dialbox in DialogBox.dialogboxes:
            # cleanup unneeded dialogboxes
            if dialbox.room != active_room:
              speaker = dialbox.state
              if speaker is not None:
                speaker.dialogline = 0
              dialbox.state = None
              active_talker = None
              dialbox.kill()
            if time.time() - dialbox.timer > active_timer:
              #print(dialbox.state.name, "Dialogbox timed out")
              
              speaker = dialbox.state
              if isinstance(speaker, NPC):
                line = speaker.dialog[speaker.active_dialog]["line"]
                if isinstance(line, list):
                  speaker.dialogline += 1
                  if speaker.dialogline >= len(line):
                    speaker.dialogline = 0
                  elif speaker.dialogline < len(line):
                    speaker.talk(active_room, inventory, answerbox)
                  
              dialbox.state = None
              active_talker = None
              dialbox.kill()

      for updatable_object in updatable:
        updatable_object.update(dt)

      # draw screen
      active_room.draw(screen, inventory, answerbox)

      # check for key presses
      keys = pygame.key.get_pressed()
      if keys[pygame.K_SPACE]:
            print("Space key pressed")
            for num, item in inventory.items.items():
                print("Item ID: ", item.id, " Item position: ", item.position)
            for drawable_room in Room.rooms.values():
              if drawable_room == active_room:
                drawable_room.shine(screen)
      if keys[pygame.K_s]:
            print("S key pressed")
            SaveState(active_room, inventory, "save.yaml")
      if keys[pygame.K_l]:
            print("L key pressed")
            inventory.items = {}
            (active_room, new_inventory) = LoadState("save.yaml")
            inventory.items = new_inventory.items

    
    # events (mouse actions)
      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1 or 3:
            # dragging items
            for box in list(dict.fromkeys(list(active_room.items.values()) + list(inventory.items.values()))):
              if box.rect.collidepoint(event.pos):
                active_box = box
                active_click = box
                print("Box pressed in position: ", box.position, "event pos: ", event.pos)

            # clicking doors - skip clicking doors, when an answer is outstanding
            if answerbox.state == None:
              for door in active_room.doors.values():
                if door.rect.collidepoint(event.pos):
                  active_click = door
            # clicking actions
            for action in active_room.actions.values():
              if action.rect.collidepoint(event.pos):
                active_click = action
            # clicking NPCs
            for npc in active_room.npcs.values():
              if npc.rect.collidepoint(event.pos):
                active_click = npc
            # clicking answers
            if answerbox.state != None:
              for answer in answerbox.answers.values():
                if answer.rect.collidepoint(event.pos):
                  active_click = answer

        if event.type == pygame.MOUSEBUTTONUP:
          # dropping and clicking on items (left mouse button)
          dragable = list(active_room.items.values()) + list(inventory.items.values())
          if event.button == 1:
            #clickable = list(active_room.actions.values()) + list(active_room.doors.values())
              
            for box in list(dict.fromkeys(dragable)):
              if box.rect.collidepoint(event.pos):
                # process dropping on doors
                for door in active_room.doors.values():
                  if door.collides_with(box):
                    door.unlock(box)
                    box.kill(inventory, Room.rooms)
                    break
                # process dropping on  actions
                for action in active_room.actions.values():
                  if action.collides_with(box):
                    action.unlock(box, inventory)
                    box.kill(inventory, Room.rooms)
                    break
                # process dropping on  NPCs
                for npc in active_room.npcs.values():
                  if npc.collides_with(box):
                    npc.unlock(box, inventory)
                    box.kill(inventory, Room.rooms)
                    break
                # if item is dropped on other item in iventory
                for item in list(inventory.items.values()):
                  if item.collides_with(box):
                    if isinstance(item, Item) and isinstance(box, Item):
                      if box == item:
                        print("Item dropped on itself, ignoring")
                        continue
                    item.stash(inventory, active_room)
                    item.combine(box)
                    box.kill(inventory, Room.rooms)
                    #break
                 # if item is dropped in inventory
                if inventory.collidepoint(event.pos): 
                  box.stash(inventory, active_room)
                  if isinstance(box, Item):
                    box.action()
                  break 
                # if item is dropped in room
                if active_room.collidepoint(event.pos):
                  box.stash(inventory, active_room)
                  if isinstance(box, Item):
                    box.action()
                  break
               
                # if item is dropped outside of room or inventory
                if not active_room.collidepoint(event.pos) and not inventory.collidepoint(event.pos):
                  box.stash(inventory, active_room)
                  if isinstance(box, Item):
                    box.action()
                  break
            active_box = None

            # process clicking on answers
            if answerbox.state != None:
              for answer in answerbox.answers.values():
                if answer.rect.collidepoint(event.pos):
                  print("Answer pressed in position: ", answer.position)
                  print(answer.answer)
                  if isinstance(answer, Answer) and active_click == answer:
                    active_talker = npc
                    answer.action()
                    print("Answer executed in position: ", answer.position)
                    last_active_click = active_click
                    active_click = None
                  else:
                    last_active_click = active_click
                    active_click = None
            # process clicking on doors
            for door in active_room.doors.values():
              if door.rect.collidepoint(event.pos):
                if isinstance(door, Door) and active_click == door:
                  if not door.locked:
                    active_room = door.target_room
                    active_room.play()
                  else:
                    print("Door is locked in position: ", door.position)
                  last_active_click = active_click
                  active_click = None
                  print("Button pressed in position: ", door.position)
                else:
                  last_active_click = active_click
                  active_click = None
            # process clicking on actions
            for action in active_room.actions.values():
              if action.rect.collidepoint(event.pos):
                if isinstance(action, Action) and active_click == action:
                  action.action()
                  print("Button pressed in position: ", action.position)
                  last_active_click = active_click
                  active_click = None
                else:
                  last_active_click = active_click
                  active_click = None

              # process clicking on NPCs
            for npc in active_room.npcs.values():
              if npc.rect.collidepoint(event.pos):
                if isinstance(npc, NPC) and active_click == npc:
                  npc.talk(active_room, inventory, answerbox)
                  # active_timer = npc.dialog[npc.active_dialog]["duration"]

                  sound = npc.dialog[npc.active_dialog]["sound"]
                  if isinstance(sound, list):
                    # if there are multiple sounds, we take the one from dialogline
                    sound = npc.dialog[npc.active_dialog]["sound"][npc.dialogline]
                  else:
                    # otherwise we take the sound as it is
                    sound = npc.dialog[npc.active_dialog]["sound"]

                  duration = get_sound_duration(sound)
                  active_timer = duration

                  print("NPC pressed in position: ", npc.position)
                  last_active_click = active_click
                  active_click = None
                  active_talker = npc
                else:
                  last_active_click = active_click
                  active_click = None



          if event.button == 3:
            # process right-clicking on doors
            for door in active_room.doors.values():
              if door.rect.collidepoint(event.pos):
                if isinstance(door, Door) and active_click == door:            
                  active_talker = door
                  door.describe(active_room)
                  active_timer = 3
                  last_active_click = active_click
                  active_click = None
                  print("Button pressed in position: ", door.position)
                else:
                  last_active_click = active_click
                  active_click = None
            # process right-clicking on actions
            for action in active_room.actions.values():
              if action.rect.collidepoint(event.pos):
                if isinstance(action, Action) and active_click == action:
                  active_talker = action
                  action.describe(active_room)
                  active_timer = 3
                  print("Button pressed in position: ", action.position)
                  last_active_click = active_click
                  active_click = None
                else:
                  last_active_click = active_click
                  active_click = None

              # process clicking on NPCs
            for npc in active_room.npcs.values():
              if npc.rect.collidepoint(event.pos):
                if isinstance(npc, NPC) and active_click == npc:
                  active_talker = npc
                  npc.describe(active_room)
                  if npc.locked:
                    sound = npc.dialog["description"]["locked"]["sound"]
                    active_timer = get_sound_duration(sound)
                  else:
                    #active_timer = npc.dialog["description"]["unlocked"]["duration"]
                    sound = npc.dialog["description"]["unlocked"]["sound"]
                    active_timer = get_sound_duration(sound)
                  print("NPC describe pressed in position: ", npc.position)
                  last_active_click = active_click
                  active_click = None
                else:
                  last_active_click = active_click
                  active_click = None

            # process right-clicking on items
            for box in list(dict.fromkeys(dragable)):
              if box.rect.collidepoint(event.pos):
                if isinstance(box, Item):
                  active_talker = box
                  active_timer = 3
                  box.describe(active_room)
                  print("Item pressed in position: ", box.position)
                  last_active_click = active_click
                  active_click = None
                else:
                  last_active_click = active_click
                  active_click = None

            active_box = None


        if event.type == pygame.MOUSEMOTION:
          if active_box != None:
            active_box.move_ip(event.rel)

        if event.type == pygame.QUIT:
          run = False

      dt = clock.tick(FPS)
      pygame.display.flip()

      

pygame.quit()



if __name__ == "__main__":
    main()

