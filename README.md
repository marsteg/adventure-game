# Adventure Game

an attempt to create a point and click adventure game in python  with pygame
You will need the pygame library. Then just run:
	 python3 main.py

## Features Implemented
- creation of items, doors, actions and rooms.
- stashing of items
- switching rooms with doors
- hitting space makes items, doors and actions shine


# todo: 
- item management: what should happen to items, that are unstashed? currently, they go back to their rooms, to the position they were dropped on. Should they:
	- move to the room and position, they were dropped?
	- go back to the inventory? (do not unstash...)
	- go back to their room to make them "re-findable?"
- how can items interact with Actions?
	- validate unlocking of Actions
	- should unlock of an action also execute it's actionfuncs?
- doubleclick on items for fast collecting
- items should not be movable off the screen
- need to find a clean way to assign and create doors and rooms and assign items (currently in main func)
- NPCs
	- single line talking
	- conversations
- Sound
- Gamestate:
	- how to save and load the game?
- Player Character?

## inventory
- items should get ordered / aligned in the inventory
	- the inventory will need slots 


## actions
- actions work now, but i need more functions
	


