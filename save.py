from action import *
from door import *
from item import *
from rectshape import *
from room import *
from inventory import *
from npc import *

def SaveState(active_room, rooms, inventory,  filename):
    savedata = {}
    
    for room in rooms.values():
        savedata[room.name] = {}
        savedata[room.name]['doors'] = {}
        savedata[room.name]['actions'] = {}
        savedata[room.name]['items'] = {}
        savedata[room.name]['npcs'] = {}
        for door in room.doors.values():
            savedata[room.name]['doors'][door.name] = {"locked": door.locked}
        for item in room.items.values():
            savedata[room.name]['items'][item.name] = {"stashed": item.stashed, "allow_destroy": item.allow_destroy}
        for action in room.actions.values():
            savedata[room.name]['actions'][action.id] = {"locked": action.locked}
        for npc in room.npcs.values():
            savedata[room.name]['npcs'][npc.name] = {"active_dialog": npc.active_dialog, "locked": npc.locked}
        savedata['inventory'] = {}
        for item in inventory.items.values():
            savedata['inventory'][item.name] = {"stashed": item.stashed, "allow_destroy": item.allow_destroy}
        
        savedata['active_room'] = active_room.name

    yaml_output = yaml.dump_all(savedata, sort_keys=False)

    with open(filename, 'w') as f:
        f.write(yaml_output)
    print('Written to file successfully')


def LoadState(filename):
    with open(filename, 'r') as f:
        data = yaml.safe_load

        #return active_room, rooms, inventory
    

# collect the gamestate from
# - main
#     - active_room
# - inventory
# - every door
#    
# - every npc (excluding npc.dialog if possible)
#     - self.active_dialog
# - every action
#     - action.locked
# - every room
#     room.doors = {}
#        - door.locked
#     room.items = {}
#       - item.stashed
#       - item.stashed
#       - item.allow_destroy
#     room.actions = {}
#     room.npcs = {}
# - answerbox.state
# - dialogbox.state
    


