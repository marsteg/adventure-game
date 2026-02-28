# Point&Click Adventure Game Engine

This is an attempt to create a Point&Click Adventure Game Engine in python with [pygame](https://www.pygame.org/)
You will need the python installed with the pygame library. To see the example game, just run:
````
	 python3 main.py
````

To create your own game, create update game.py with your game specifications.

The Project is also prepared to work with AI Agents. Try letting your AI Agent generate a Game for you ;)


## Features Implemented
- the game itself gets completely assempled in game.py. Here you define all your Rooms, NPCs, Items, Actions and their Actionfuncs.
- creation of items, doors, actions and rooms.
- stashing of items
- items can now be destroyed on usage or not. if not, they go back to the inventory after usage
- Items can now be combined but it only works if done the correct way around..
- switching rooms with doors
- hitting space makes items, doors, NPCs and actions shine
- Actionfuncs are a way to teach an action button tricks. With this theoretically anything can be executed via Actions
- unlocking an action will also execute it's actionfuncs
- Save and Loading the Game is now possible! Press 'S' to Save and 'L' to Load
	- now with menu and support for multiple savefiles
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
	- each block of speech has a configurable talking time 
	- speech can be a single line or an array of lines
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
- Cutscenes! There is now the possibility to have Text-based Cutscenes for intros or short explanations of story.
	- They can be triggered via Actionfuncs
- Walkable Areas!
	- You can now create a mask for rooms, so players can only walk on the white Areas of the Mask. Black and Transparent Areas are blocked paths.
- Asset Generator
	- there is now an Asset Generator in the tools folder. It can be used to generate Assets with [Stability AI or huggingface (default)!](https://platform.stability.ai/)
	- Check [the docs](tools/README.md)
		

## Improve Documentation
- create index
- properly route through documentation

## Player Character
	- doubleclick on actions, doors, items for faster walking speed
	- Improve Walking
		- requires a walkable area as clickable area per room
		- how to define that area?
		- improve player walking animation

## Items
- I would like to implement an "endless" item, from which the player always pick up one


# Thanks and Grateful links to external helping tools:
Background Music from: [Musicfox](https://www.musicfox.com/info/kostenlose-gemafreie-musik/).  
Sound Effeces from:
freesound.org
	- Brickhario (unlocking doors)

