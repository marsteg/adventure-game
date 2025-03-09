import pygame
import random
from constants import *
from item import *
from inventory import *

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
    items = pygame.sprite.Group()
    Item.containers = (updatable, drawable, items, dragable)
    Inventory.containers = (updatable, drawable)
    inventory = Inventory()


    active_box = None

    # room specifics...
    items = []
    for i in range(5):
      x = random.randint(50, 700)
      y = random.randint(50, 350)
      w = random.randint(35, 65)
      h = random.randint(35, 65)
      image = 'assets/items/missile.png'
      item = Item(x, y, w, h, image)
      items.append(item)
    
    # game loop
    run = True
    while run:

      screen.fill("turquoise1")


      for updatable_object in updatable:
        updatable_object.update(dt)

      for drawable_object in drawable:
        drawable_object.draw(screen)    
    
    
    # events
      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            for num, box in enumerate(dragable):
              if box.rect.collidepoint(event.pos):
                active_box = num

        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            for num, box in enumerate(dragable):
              if box.rect.collidepoint(event.pos):
                if box.collides_with(inventory):
                  box.stash()      
            active_box = None

        if event.type == pygame.MOUSEMOTION:
          if active_box != None:
            items[active_box].move_ip(event.rel)

        if event.type == pygame.QUIT:
          run = False

      pygame.display.flip()

pygame.quit()



if __name__ == "__main__":
    main()

