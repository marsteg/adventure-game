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
- unlocking an action will also execute it's actionfuncs
- NPCs	
	- can give items, when unlockd
	- can open doors, when unlocked
	- can have a speechcolor


# todo: 
- need to find a clean way to assign and create doors and rooms and assign items (currently in main func)
- NPCs
	- actual conversations
		- text currently stays 3 seconds - clicking should skip to the next line
        - text should be positioned relative to the character speaking
		- each line of speech should have a configurable talking time (and a default value)
		- active dialog (dialog state of NPC) answers could change based on:
			- specific replies chosen (should execute actionfunc)
			- actions executed (actionfunc to change actve dialog of npc)
        - Speech Lines are objects themselves
            - Speech Lines have:
                - text
                - duration
                - speaker (NPC or player)
                - color
                - position
                - trigger next answer lines
            - Answer Lines are objects themselves
                - Answer Lines have:
                    - text
                    - actionfuncs
                    - trigger next speech line or exit dialog
		- dialogs should be objects themselves
			- dialogs have:
                - a "state" of the current dialog
				- can change the state of the current "dialog" of an NPC (trigger change to next one (via actionfunc?))
				- Answer Lines:
                    - List of answers which need to trigger speech lines and actions if desired
				- should make the rest of the screen unclickable"
			- NPC needs a state of the current active dialog
- Gamestate:
	- how to save and load the game?
- Player Character?
	- doubleclick on items for fast collecting
- Sound

## inventory
- items should get ordered / aligned in the inventory
	- the inventory will need slots 

## Sound
- Rooms should provide background music

## actions
- actions work now, but i need more functions
	- play a sound

	


