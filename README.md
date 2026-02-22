# Point&Click Adventure Game Engine

This is an attempt to create a Point&Click Adventure Game Engine in python with [pygame](https://www.pygame.org/)
You will need the python installed with the pygame library. To see the example game, just run:
````
	 python3 main.py
````



## Features Implemented
- creation of items, doors, actions and rooms.
- stashing of items
- items can now be destroyed on usage or not. if not, they go back to the inventory after usage
- Items can now be combined but it only works if done the correct way around..
- switching rooms with doors
- hitting space makes items, doors, NPCs and actions shine
- Actionfuncs are a way to teach an action button tricks. With this theoretically anything can be executed via Actions
- unlocking an action will also execute it's actionfuncs
- Save and Loading the Game is now possible! Press 'S' to Save and 'L' to Load
- Right-Click on NPCs, Doors, Items and Actions gives now a description about them
	- different descriptions based on the lock state possible
- Sounds!
	- Rooms now have background music!
	- NPCs can have voice, when talking!
	- actions can play sounds on Activation (when unlocked)
	- clicking should skip to the next line
- NPCs	
	- can give items, when unlockd
	- can open doors, when unlocked
	- can have a speechcolor
	- There are now different ways to take and give items from NPCs
			- by unlocking them (possible via item, action or dialog)
- Conversations!
	- each line of speech should have a configurable talking time 
	- active dialog (dialog state of NPC) answers could change based on:
			- specific replies chosen (should execute actionfunc)
			- actions executed (actionfunc to change actve dialog of npc)
	- doors are disabled from clicking while conversations are ongoing
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
- Introduced a Player. At the moment it simply spawns and can be send to a destination
	- The Player has now a left and right walking animation
- There is now a small Text Area that displays the objectname of whatever you are pointing at
- The Inventory is now centered
- Cutscenes! There is now the possibility to have Text-based Cutscenes for intros or short explanations of story
		


# Todo List: 
- need to find a clean way to assign and create doors and rooms and assign items (currently in main func)
	- it would be nice to have the "Game Definition" in a yaml file.
		- All Items in a Yaml
		- All Rooms in a Yaml
		- All NPCs in a Yaml
		- all Doors in a Yaml
## Conversations
	- how to manage it when picking up an item should change dialog choices?
		- should Items have actions, that get executed on pickup? could change active_dialogs or locked dialogs?
	- how to have multiple NPCs talk at the same time?
	- i partly implemented multiline text and auto-detection of speech length. Needs further thorough testing and improvement though
## Saving/Loading:
	- how to save and load the game?
		- save to yaml
			- should provide some savename input
			- support multiple savefiles
		- load from yaml
			- select savefile
	- needs further debugging - currently items are not correctly restored
## Player Character
	- doubleclick on actions, doors, items for faster walking speed
	- Improve Walking
		- requires a walkable area as clickable area per room
		- how to define that area?
		- improve player walking animation

## Items
- I would like to implement an "endless" item, from which the player always pick up one
	- there is now a test case but somehow the item is only given once.


# Thanks and Grateful links to external helping tools:
Background Music from: https://www.musicfox.com/info/kostenlose-gemafreie-musik/
Sound Effeces from:
freesound.org
	- Brickhario (unlocking doors)

