import pygame
import random
from constants import *
from item import *
from inventory import *
from room import *
from door import *
from action import *
from actionfuncs import *

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

    # title screen
    title = Room("assets/rooms/TitleScreen.png")
   

    # room and door and item assignments specifics...
    # rooms require nothing
    room1 = Room("assets/rooms/RektorOffice.png")
    room2 = Room("assets/rooms/LivingRoom.png")
    # items require nothing
    missile = Item(100, 100, 50, 50, "assets/items/missile.png") # should come back to inventory
    missile2 = Item(200, 200, 50, 50, "assets/items/missile2.png", True) # should self destruct
    # actions might require items
    button1 = Action(800, 100, 50, 50, "assets/actions/button.png", False, None)
    button2 = Action(400, 100, 50, 50, "assets/actions/button2.png", True, missile)
   # doors require rooms and might require items
    Room1door1 = Door(80, 300, 100, 200, "assets/doors/door1.png", room2, True, missile2)
    Room1door2 = Door(880, 300, 100, 200, "assets/doors/door1.png", room2, True, button1)
    Room2door2 = Door(480, 300, 100, 200, "assets/doors/door1.png", room1, False, None)
    titledoor = Door(300, 300, 100, 200, "assets/doors/door1.png", room1, False, None)

   # action funcs require items, doors, and actions
    button1.add_function(ChangePicture, button1, "assets/actions/button2.png", "assets/actions/button.png", None) 
    button1.add_function(LogText, "Text Logged")
    button1.add_function(UnlockDoor, button1, Room1door2)

    button2.add_function(ChangePicture, button2, "assets/actions/button.png", "assets/actions/button2.png", None)
    button2.add_function(LogText, "Button 2 Text Logged")
    button2.add_function(AllowDestroy, missile2)


  # appendings doors, items and actions to rooms
    title.doors[titledoor.id] = titledoor
    room2.doors[Room2door2.id] = Room2door2
    room1.doors[Room1door1.id] = Room1door1
    room1.doors[Room1door2.id] = Room1door2
    room1.items[missile.id] = missile
    room1.actions[button1.id] = button1
    room2.items[missile2.id] = missile2
    room2.actions[button2.id] = button2


    
    for i in range(5):
      x = random.randint(50, 700)
      y = random.randint(50, 350)
      w = random.randint(35, 65)
      h = random.randint(35, 65)
      image = 'assets/items/missile.png'
      item = Item(x, y, w, h, image)
      room2.items[item.id] = item


    # initial state
    active_room = title
    active_box = None
    active_click = None
    last_active_click = None
    
    # game loop
    run = True
    while run:


      for updatable_object in updatable:
        updatable_object.update(dt)
      
      # draw screen
      #for drawable_room in rooms:
      #  if drawable_room == active_room:
      #    drawable_room.draw(screen, inventory)
      active_room.draw(screen, inventory)
  
      keys = pygame.key.get_pressed()
      if keys[pygame.K_SPACE]:
            print("Space key pressed")
            for num, item in inventory.items.items():
                print("Item ID: ", item.id, " Item position: ", item.position)
            for drawable_room in Room.rooms.values():
              if drawable_room == active_room:
                drawable_room.shine(screen)

    
    # events
      FPS = 60
      dt = clock.tick(FPS)

      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
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

        if event.type == pygame.MOUSEBUTTONUP:
          # dropping items
          if event.button == 1:
            clickable = list(active_room.actions.values()) + list(active_room.doors.values())
            dragable = list(active_room.items.values()) + list(inventory.items.values())
            
            for box in list(dict.fromkeys(dragable)):
              if box.rect.collidepoint(event.pos):
                # process doors
                for door in active_room.doors.values():
                  if door.collides_with(box):
                    door.unlock(box, inventory)
                    box.kill(inventory, Room.rooms)
                    break
                # process actions
                for action in active_room.actions.values():
                  if action.collides_with(box):
                    action.unlock(box, inventory)
                    box.kill(inventory, Room.rooms)
                    break
                # process room
                if active_room.collidepoint(event.pos):
                  box.stash(inventory)
                  break
                if inventory.collidepoint(event.pos):
                  box.stash(inventory)
                  break
            active_box = None
            
            for door in active_room.doors.values():
              if door.rect.collidepoint(event.pos):
                if isinstance(door, Door) and active_click == door:
                  if not door.locked:
                    active_room = door.target_room
                  else:
                    print("Door is locked in position: ", door.position)
                  last_active_click = active_click
                  active_click = None
                  print("Button pressed in position: ", door.position)
                else:
                  last_active_click = active_click
                  active_click = None

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

        if event.type == pygame.MOUSEMOTION:
          if active_box != None:
            active_box.move_ip(event.rel)

        if event.type == pygame.QUIT:
          run = False

      pygame.display.flip()
      pygame.display.update()
      

pygame.quit()



if __name__ == "__main__":
    main()

