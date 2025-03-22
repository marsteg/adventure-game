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

    dialogbox = DialogBox()
    answerbox = AnswerBox()

    # title screen
    title = Room("assets/rooms/TitleScreen.png", "title", "assets/sounds/background/Talkline7.wav")
   

    # room and door and item assignments specifics...
    # rooms require nothing
    room1 = Room("assets/rooms/RektorOffice.png", "room1", "assets/sounds/background/Albatros.wav")
    room2 = Room("assets/rooms/LivingRoom.png", "room2", "assets/sounds/background/PrettyOrgan.wav")
    
    # items require nothing (should require rooms and self-register?)
    missile = Item(100, 100, 50, 50, "assets/items/missile.png", "missile") # should come back to inventory
    missile2 = Item(200, 200, 50, 50, "assets/items/missile2.png", "missile2", True) # should self destruct
    comb = Item(at_percentage_width(88), at_percentage_height(80), 50, 50, "assets/items/comb.png", "comb", True) # should self destruct

    # actions might require items
    button1 = Action(800, 100, 50, 50, "assets/actions/button.png", "button1", False, None)
    button2 = Action(400, 100, 50, 50, "assets/actions/button2.png", "button2", True, missile)

    # NPCs might require Items
    wolfboy = NPC(750, 350, 150, 160, "assets/npcs/werewolfboy.png", "wolfboy", True, missile2, GREEN, "assets/dialogs/wolfboy.yaml")
    wolfboy2 = NPC(350, 350, 150, 160, "assets/npcs/werewolfboy.png", "wolfboy2", True, comb, WHITE, "assets/dialogs/wolfboy2.yaml")
    
   # doors require rooms and might require items
    Room1door1 = Door(80, 300, 100, 200, "assets/doors/door1.png", "Room1Door1", title, True, missile)
    Room1door2 = Door(880, 300, 100, 200, "assets/doors/door1.png", "Room1Door2",room2, True, button1)
    Room2door2 = Door(480, 300, 100, 200, "assets/doors/door1.png", "Room2Door2",room1, False, None)
    titledoor = Door(300, 300, 100, 200, "assets/doors/door1.png", "Titledoor", room1, False, None)

    
   # action funcs require items, doors, and actions
    button1.add_function(ChangePicture, button1, "assets/actions/button2.png", "assets/actions/button.png", None) 
    button1.add_function(LogText, "Text Logged")
    button1.add_function(UnlockDoor, button1, Room1door2)

    button2.add_function(ChangePicture, button2, "assets/actions/button.png", "assets/actions/button2.png", None)
    button2.add_function(LogText, "Button 2 Text Logged")
    button2.add_function(AllowDestroy, missile2)

    #NPCs action funcs
    wolfboy.add_function(GiveItem, missile, inventory)
    wolfboy.add_function(AllowDestroy, missile2)
    wolfboy.add_function(ActionChangeDialog, wolfboy, "bye2")
    wolfboy.add_function(DestroyItem, missile2, inventory)
    
    wolfboy2.add_function(ActionChangeDialog, wolfboy2, "bye")
    wolfboy2.add_function(AllowDestroy, comb)
    wolfboy2.add_function(TakeItem, comb, inventory)
    wolfboy2.add_function(UnlockDoor, button1, Room1door2)

    
    #wolfboy.add_function(UnlockDoor, wolfboy, Room1door1)
  # appendings doors, items and actions to rooms
    title.doors[titledoor.name] = titledoor
    room2.doors[Room2door2.name] = Room2door2
    room1.doors[Room1door1.name] = Room1door1
    room1.doors[Room1door2.name] = Room1door2
    room1.npcs[wolfboy2.name] = wolfboy2
    room1.actions[button1.name] = button1
    room1.items[missile2.name] = missile2
    room1.items[comb.name] = comb
    room2.npcs[wolfboy.name] = wolfboy
    room2.actions[button2.name] = button2

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

      for npc in active_room.npcs.values():
        #if dialogbox.state != None and npc.active_dialog != None and active_talker != None:
        if npc.active_dialog != None and active_talker != None:
          if dialogbox.room != active_room:
            dialogbox.state = None
            active_talker = None
            continue      
          #if time.time() - dialogbox.timer > active_talker.dialog[active_talker.active_dialog]["duration"]:
          if time.time() - dialogbox.timer > active_timer:
            active_talker = None
            dialogbox.state = None



      for updatable_object in updatable:
        updatable_object.update(dt)

      # draw screen
      active_room.draw(screen, inventory, dialogbox, answerbox)

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
                print("Box pressed in position: ", box.position, "event pos: ", event.pos)

            # clicking doors
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
          # dropping items (left mouse button)
          dragable = list(active_room.items.values()) + list(inventory.items.values())
          if event.button == 1:
            #clickable = list(active_room.actions.values()) + list(active_room.doors.values())
              
            for box in list(dict.fromkeys(dragable)):
              if box.rect.collidepoint(event.pos):
                # process dropping on doors
                for door in active_room.doors.values():
                  if door.collides_with(box):
                    door.unlock(box, inventory)
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
                # if item is dropped in room
                if active_room.collidepoint(event.pos):
                  box.stash(inventory, active_room)
                  break
                # if item is dropped in inventory
                if inventory.collidepoint(event.pos): 
                  box.stash(inventory, active_room)
                  break
                # if item is dropped outside of room or inventory
                if not active_room.collidepoint(event.pos) and not inventory.collidepoint(event.pos):
                  box.stash(inventory, active_room)
                  break
            active_box = None
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
                  #dialogbox.timer = time.time()
                  npc.talk(active_room, inventory, dialogbox, answerbox)
                  active_timer = npc.dialog[npc.active_dialog]["duration"]
                  dialogbox.timer = time.time()
                  print("NPC pressed in position: ", npc.position)
                  last_active_click = active_click
                  active_click = None
                  active_talker = npc
                else:
                  last_active_click = active_click
                  active_click = None

              # process clicking on answers
            if answerbox.state != None:
              for answer in answerbox.answers.values():
                if answer.rect.collidepoint(event.pos):
                  print("Answer pressed in position: ", answer.position)
                  print(answer.answer)
                  if isinstance(answer, Answer) and active_click == answer:
                    #dialogbox.timer = time.time()
                    active_talker = npc
                    answer.action()
                    dialogbox.timer = time.time()
                    print("Answer executed in position: ", answer.position)
                    last_active_click = active_click
                    active_click = None
                  else:
                    last_active_click = active_click
                    active_click = None

          if event.button == 3:
            # process right-clicking on doors
            for door in active_room.doors.values():
              if door.rect.collidepoint(event.pos):
                if isinstance(door, Door) and active_click == door:
                  if not door.locked:
                    # play and display an "unlocked" description
                    pass
                  else:
                    print("Door is locked in position: ", door.position)
                  last_active_click = active_click
                  active_click = None
                  # play and display a "locked" description
                  print("Button pressed in position: ", door.position)
                else:
                  last_active_click = active_click
                  active_click = None
            # process right-clicking on actions
            for action in active_room.actions.values():
              if action.rect.collidepoint(event.pos):
                if isinstance(action, Action) and active_click == action:
                  if not action.locked:
                    # play and display an "unlocked" description
                    pass
                  else:
                    print("Action is locked in position: ", action.position)
                    # play and display a "locked" description
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
                  npc.describe(dialogbox, active_room)
                  if npc.locked:
                    active_timer = npc.dialog["description"]["locked"]["duration"]
                  else:
                    active_timer = npc.dialog["description"]["unlocked"]["duration"]
                  dialogbox.timer = time.time()
                  print("NPC describe pressed in position: ", npc.position)
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

