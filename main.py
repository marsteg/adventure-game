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
    
    drawable = pygame.sprite.Group()
    dragable = pygame.sprite.Group()
    clickable = pygame.sprite.Group()
    items = pygame.sprite.Group()   
    Door.containers = (updatable, clickable)
    Item.containers = (updatable, dragable)
    Action.containers = (updatable, clickable)
    Inventory.containers = (updatable, drawable)
    inventory = Inventory()

    rooms = pygame.sprite.Group()
    Room.containers = (updatable, rooms)

    # title screen
    title = Room("assets/rooms/TitleScreen.png")
   

    # room and door and item assignments specifics...
    room1 = Room("assets/rooms/RektorOffice.png")
    room2 = Room("assets/rooms/LivingRoom.png")
    missile = Item(100, 100, 50, 50, "assets/items/missile.png")
    missile2 = Item(200, 200, 50, 50, "assets/items/missile2.png")
    door1 = Door(80, 300, 100, 200, "assets/doors/door1.png", room2, True, missile)
    door2 = Door(480, 300, 100, 200, "assets/doors/door1.png", room1, False, None)
    titledoor = Door(300, 300, 100, 200, "assets/doors/door1.png", room1, False, None)
    title.doors.append(titledoor)
   
    room2.doors.append(door2)

    button1 = Action(800, 100, 50, 50, "assets/actions/button.png", False, None)
    button1.add_function(ChangePicture, button1, "assets/actions/button2.png", "assets/actions/button.png", None) 
    button1.add_function(LogText, "Text Logged")
    button1.add_function(UnlockDoor, missile, door1)
    room1.doors.append(door1)
    room1.items.append(missile)
    room1.actions.append(button1)
    room2.items.append(missile2)

    
    

    
    for i in range(5):
      x = random.randint(50, 700)
      y = random.randint(50, 350)
      w = random.randint(35, 65)
      h = random.randint(35, 65)
      image = 'assets/items/missile.png'
      item = Item(x, y, w, h, image)
      room2.items.append(item)


    # initial state
    active_room = title
    active_box = None
    active_click = None
    
    # game loop
    run = True
    while run:


      for updatable_object in updatable:
        updatable_object.update(dt)
    
      inventory.draw(screen, inventory)

      for drawable_room in rooms:
        if drawable_room == active_room:
          drawable_room.draw(screen)

  
      keys = pygame.key.get_pressed()
      if keys[pygame.K_SPACE]:
            print("Space key pressed")
            for num, item in inventory.items.items():
                print("Item ID: ", item.id, " Item position: ", item.position)
            for drawable_room in rooms:
              if drawable_room == active_room:
                drawable_room.shine(screen)

    
    # events
      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            for num, box in enumerate(dragable):
              if box.rect.collidepoint(event.pos):
                active_box = box

            for num, door in enumerate(clickable):
              if door.rect.collidepoint(event.pos):
                active_click = door

        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            for num, box in enumerate(dragable):
              if box.rect.collidepoint(event.pos):
                
                for num, clickable_item in enumerate(clickable):
                  if clickable_item.collides_with(box):
                    clickable_item.unlock(box)
                if box.collides_with(inventory):
                  box.stash(inventory)   
                elif box.stashed:
                    box.unstash(inventory, event.pos) 
            active_box = None
            
            for num, door in enumerate(clickable):
              if door.rect.collidepoint(event.pos):
                if isinstance(door, Door) and active_click == door:
                  if not door.locked:
                    active_room = door.target_room
                  active_click = None
                  print("Button pressed in position: ", door.position)
                elif isinstance(door, Action) and active_click == door:
                    door.action()
                    print("Button pressed in position: ", door.position)
                    active_click = None
                else:
                  active_click = None

        if event.type == pygame.MOUSEMOTION:
          if active_box != None:
            active_box.move_ip(event.rel)

        if event.type == pygame.QUIT:
          run = False

      pygame.display.flip()

pygame.quit()



if __name__ == "__main__":
    main()

