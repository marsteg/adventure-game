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
- Save and Loading the Game is now possible! Press 'S' to Save and 'L' to Load
- Sounds!
	- Rooms now have background music!
	- NPCs can have voice, when talking!
- NPCs	
	- can give items, when unlockd
	- can open doors, when unlocked
	- can have a speechcolor
	- There are now different ways to take and give items from NPCs
			- by unlocking them (possible via item, action or dialog)
	Conversations!
	- each line of speech should have a configurable talking time 
		- active dialog (dialog state of NPC) answers could change based on:
			- specific replies chosen (should execute actionfunc)
			- actions executed (actionfunc to change actve dialog of npc)
		- NPCs can give the player Items right after successfully giving an Item to them. 
		- Speech Lines are objects defined in yaml
				- Speech Lines have:
					- text
					- duration
					- speaker (NPC or player) (requires matching names in NPC creation and yaml dialog)
					- Have Answer Objects
						- Answers can have X actionfuncs (most common: change active dialog)
						- Answer Lines have:
							- text
							- actionfuncs
							- trigger next speech line or exit dialog
		


# todo: 
- need to find a clean way to assign and create doors and rooms and assign items (currently in main func)
- if actions, doors cannot be executed (are locked), there should be some "negative" feedback, like a comment by the player or narrator
- Conversations
	- text currently stays X seconds - clicking should skip to the next line
	- how to manage it when picking up an item should change dialog choices?
		- should Items have actions, that get executed on pickup? could change active_dialogs or locked dialogs?
	- how to have multiple NPC talk at the same time?
	- position
		- text should be positioned relative to the character speaking
	- active answer window should make the rest of the screen unclickable (?)
- Saving/Loading:
	- how to save and load the game?
		- save to yaml
			- should provide some savename input
			- support multiple savefiles
		- load from yaml
			- select savefile
- Player Character?
	- doubleclick on items for fast collecting

## inventory
- items should get ordered / aligned in the inventory
	- slot system size (currently 20) - what if i have more items? scrolling?


## Sound
- actions should play sounds on Unlock

## actions
- actions work now, but i need more functions
	- play a sound


Music files from: https://www.musicfox.com/info/kostenlose-gemafreie-musik/


