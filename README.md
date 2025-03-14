# Adventure Game

an attempt to create a point and click adventure game in python  with pygame
You will need the pygame library. Then just run:
	 python3 main.py

## Features Implemented
- creation of items, doors, actions and rooms.
- stashing of items
- items can now be destroyed on usage or not. if not, they go back to the inventory after usage
- switching rooms with doors
- hitting space makes items, doors and actions shine
- Actionfuncs are a way to teach an action button tricks. With this theoretically anything can be executed via Actions

# Design Questions:
- how can items interact with Actions?
	- validate unlocking of Actions
	- should unlock of an action also execute it's actionfuncs?

# todo: 
- doubleclick on items for fast collecting
- items should not be movable off the screen
- need to find a clean way to assign and create doors and rooms and assign items (currently in main func)
- NPCs
	- single line talking
	- conversations
- Gamestate:
	- how to save and load the game?
- Player Character?
- Sound

## inventory
- items should get ordered / aligned in the inventory
	- the inventory will need slots 

## Sound
- Rooms should provide background music

## actions
- actions work now, but i need more functions
	- play a sound

	


