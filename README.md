# Adventure Game

an attempt to create a point and click adventure game in python  with pygame
You will need the pygame library. Then just run:
	 python3 main.py

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
	- Double-click on Items, NPCs, Actions, or Doors to walk at 2x speed
		- Speed automatically resets when destination is reached
		- Clicking on empty walkable space cancels fast walk and queued interactions
- There is now a small Text Area that displays the objectname of whatever you are pointing at
- The Inventory is now centered
- Cutscenes! There is now the possibility to have Text-based Cutscenes for intros or short explanations of story.
	- They can be triggered via Actionfuncs
- Walkable Areas!
	- You can now create a mask for rooms, so players can only walk on the white Areas of the Mask. Black and Transparent Areas are blocked paths.
	- See [WALKABLE_AREAS_AGENT_GUIDE.md](WALKABLE_AREAS_AGENT_GUIDE.md) for complete documentation
- Asset Generator
	- there is now an Asset Generator in the tools folder. It can be used to generate Assets with [Hugging Face (default, FREE unlimited) or Stability AI!](https://huggingface.co)
	- Check [the docs](tools/README.md)



# Todo List:

## Improve Documentation
- create index
- properly route through documentation

# Sound
- When the Game Menu is entered, the Music and Dialog should be paused
- When Clicking on New Game - any prior sound should be stopped

## Player Character
	- Improve Walking
		- improve player walking animation

## inventory
- slot system size (currently 20) - what if i have more items? scrolling?

## Items
- I would like to implement an "endless" item, from which the player always pick up one
	- there is now a test case but somehow the item is only given once.
- how to manage it when picking up an item should change dialog choices?
		- should Items have actions, that get executed on pickup? could change active_dialogs or locked dialogs?
		--> is implemented, requires testing (no test case implemented, yet)

## Asset Generation
- we want to add a text-to-speech provider, so we can generate the audio files
- we need to revisit the Dual-Item Feature to use an image2image API on huggingface

# Thanks and Grateful links to external helping tools:
Background Music from: [Musicfox](https://www.musicfox.com/info/kostenlose-gemafreie-musik/).  
Sound Effeces from:
freesound.org
	- Brickhario (unlocking doors)

