import player
import pygame
import yaml
import os
from datetime import datetime
import base64

from room import Room
from inventory import Inventory
from item import Item
from player import Player
from debug import debug_inventory_state, debug_save_data, debug_load_process, debug_room_items, debug


def SaveState(active_room, inventory, player, filename):
    """Save the current game state to a YAML file with improved format."""
    debug.log(f"Starting save operation to {filename}")
    debug_inventory_state(inventory, "Before Save")

    # Create save data with versioning and metadata
    savedata = {
        "save_version": "2.0",
        "game_content_hash": "lucky_luke_olympic_blunders",
        "rooms": {},
        "inventory": {},
        "active_room": active_room.name
    }

    debug.log(f"Active room for save: {active_room.name}")

    # Save room states
    for room in Room.rooms.values():
        room_data = {
            "doors": {},
            "actions": {},
            "items": {},
            "npcs": {}
        }

        for door in room.doors.values():
            room_data["doors"][door.name] = {"locked": door.locked}

        for item in room.items.values():
            room_data["items"][item.name] = {
                "stashed": item.stashed,
                "allow_destroy": item.allow_destroy
            }

        for action in room.actions.values():
            room_data["actions"][action.name] = {
                "locked": action.locked,
                "state": action.state,
                "imagepath": action.imagepath
            }

        for npc in room.npcs.values():
            room_data["npcs"][npc.name] = {
                "active_dialog": npc.active_dialog,
                "locked": npc.locked
            }

        savedata["rooms"][room.name] = room_data

    # Save inventory using slot-based format (IMPROVED)
    if hasattr(inventory, 'get_slot_data_for_save'):
        # Use new slot-based format
        savedata["inventory"] = inventory.get_slot_data_for_save()
        print(f"Saved inventory with slot-based format: {len(inventory.items)} items")
    else:
        # Fallback to old format for compatibility
        savedata["inventory"] = {}
        for item in inventory.items.values():
            savedata["inventory"][item.name] = {
                "stashed": item.stashed,
                "allow_destroy": item.allow_destroy,
                "self_destruct": item.self_destruct,
                "left": item.rect.left,
                "top": item.rect.top,
                "width": item.rect.width,
                "height": item.rect.height,
                "imagepath": item.imagepath
            }
        print(f"Saved inventory with legacy format: {len(inventory.items)} items")
    
    # Save player location
    savedata["player"] = {
        "left": player.sprites()[0].rect.left,
        "top": player.sprites()[0].rect.top
    }

    try:
        # Debug the save data before writing
        debug_save_data(savedata, "Before Write")

        yaml_output = yaml.dump(savedata, sort_keys=False)
        with open(filename, 'w') as f:
            f.write(yaml_output)

        debug.log(f"Save completed successfully: {len(yaml_output)} bytes written")
        print(f"Game saved to {filename} successfully")

    except IOError as e:
        debug.log(f"IO Error during save: {e}", "ERROR")
        print(f"Error saving game: {e}")
    except yaml.YAMLError as e:
        debug.log(f"YAML Error during save: {e}", "ERROR")
        print(f"Error serializing game state: {e}")


def validate_save_compatibility(data):
    """Validate save file compatibility with current game"""
    # Check save version
    save_version = data.get("save_version", "1.0")
    print(f"Save file version: {save_version}")

    # Check active room exists in current game
    active_room_name = data.get("active_room")
    if not active_room_name:
        return False, "No active room specified in save file"

    if active_room_name not in Room.rooms:
        return False, f"Room '{active_room_name}' not found in current game"

    # Check game content compatibility
    game_hash = data.get("game_content_hash", "unknown")
    current_hash = "lucky_luke_olympic_blunders"

    if save_version == "2.0" and game_hash != current_hash:
        print(f"Warning: Save content hash '{game_hash}' differs from current '{current_hash}'")

    return True, "Compatible"


def LoadState(filename):
    """Load a game state from a YAML file with validation."""
    debug.log(f"Starting load operation from {filename}")

    try:
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        debug.log(f"Successfully parsed YAML data: {len(str(data))} characters")
    except FileNotFoundError:
        debug.log(f"Save file not found: {filename}", "ERROR")
        print(f"Save file not found: {filename}")
        return None, None, None
    except yaml.YAMLError as e:
        debug.log(f"YAML parsing error: {e}", "ERROR")
        print(f"Error parsing save file: {e}")
        return None, None, None
    except IOError as e:
        debug.log(f"File reading error: {e}", "ERROR")
        print(f"Error reading save file: {e}")
        return None, None, None

    if not data:
        debug.log("Save file contains no data", "ERROR")
        print("Save file is empty or invalid")
        return None, None, None

    # Debug the loaded data
    debug_save_data(data, "Loaded from File")

    # Validate compatibility
    is_compatible, message = validate_save_compatibility(data)
    if not is_compatible:
        debug.log(f"Compatibility validation failed: {message}", "ERROR")
        print(f"Save file incompatible: {message}")
        return None, None, None

    debug.log(f"Save validation: {message}")
    print(f"Save validation: {message}")

    # Restore room states
    for room_name, room_data in data.get("rooms", {}).items():
        if room_name not in Room.rooms:
            continue

        room = Room.rooms[room_name]

        # Restore door states
        for door_name, door_data in room_data.get("doors", {}).items():
            if door_name in room.doors:
                room.doors[door_name].locked = door_data["locked"]

        # FIXED: Properly restore room items to saved state
        saved_items = room_data.get("items", {})

        # Remove items that weren't in the room when saved
        items_to_delete = [
            item_name for item_name in room.items
            if item_name not in saved_items
        ]
        for item_name in items_to_delete:
            debug.log(f"Removing '{item_name}' from room '{room_name}' (not in save)")
            del room.items[item_name]

        # Add back items that should be in the room but aren't currently there
        for item_name, item_data in saved_items.items():
            if item_name not in room.items:
                # Item needs to be restored to this room
                # Check if it exists in Item.items (global registry)
                if item_name in Item.items:
                    item = Item.items[item_name]
                    # Remove from any current room or inventory
                    for other_room in Room.rooms.values():
                        if item_name in other_room.items and other_room != room:
                            del other_room.items[item_name]

                    # Restore item properties from save
                    item.allow_destroy = item_data.get("allow_destroy", False)
                    item.stashed = False  # Item is back in room, not stashed

                    # Add to room
                    room.items[item_name] = item
                    debug.log(f"Restored '{item_name}' to room '{room_name}'")
                else:
                    debug.log(f"Warning: Item '{item_name}' not found in global registry", "WARNING")

        # Restore action states
        for action_name, action_data in room_data.get("actions", {}).items():
            if action_name in room.actions:
                action = room.actions[action_name]
                action.locked = action_data["locked"]
                action.state = action_data["state"]
                action.imagepath = action_data["imagepath"]

        # Restore NPC states
        for npc_name, npc_data in room_data.get("npcs", {}).items():
            if npc_name in room.npcs:
                npc = room.npcs[npc_name]
                npc.active_dialog = npc_data["active_dialog"]
                npc.locked = npc_data["locked"]

    # Before restoring inventory, collect items that were restored to rooms
    items_in_rooms = set()
    for room_name, room_data in data.get("rooms", {}).items():
        for item_name in room_data.get("items", {}):
            items_in_rooms.add(item_name)

    debug.log(f"Items restored to rooms: {items_in_rooms}")

    # Restore inventory with support for both old and new formats
    inventory = Inventory()
    inventory_data = data.get("inventory", {})

    # Detect save format
    if "slots" in inventory_data:
        # New slot-based format (v2.0+)
        print("Loading inventory using new slot-based format")
        errors = inventory.restore_inventory_from_slots(inventory_data, debug=True, skip_items=items_in_rooms)
        if errors:
            print("Inventory restoration warnings:")
            for error in errors:
                print(f"  - {error}")
    else:
        # Legacy format (v1.0) - convert to slot-based
        print("Loading inventory using legacy format")
        inventory.items = {}

        for item_name, item_data in inventory_data.items():
            # FIXED: Skip items that were restored to rooms
            if item_name in items_in_rooms:
                debug.log(f"Skipping '{item_name}' in inventory - restored to room")
                continue

            # Support both old 'selfdestruct' and new 'self_destruct' keys
            self_destruct = item_data.get("self_destruct", item_data.get("selfdestruct", False))

            # Create item at (0,0) to avoid position conflicts
            item = Item(
                0, 0,  # Position will be set by inventory system
                item_data["width"],
                item_data["height"],
                item_data["imagepath"],
                item_name,
                self_destruct
            )

            # Set properties BEFORE positioning
            item.allow_destroy = item_data["allow_destroy"]
            item.stashed = True

            # Remove from any rooms first
            for room in Room.rooms.values():
                if item_name in room.items:
                    del room.items[item_name]

            # Add to inventory and assign slot position
            inventory.items[item_name] = item
            pos = inventory.get_available_slots(item)
            if pos:
                item.rect.topleft = pos
                item.position = pygame.Vector2(pos)
                print(f"Restored item '{item_name}' to inventory slot at {pos}")
            else:
                print(f"Warning: No slot available for item '{item_name}'")

    # Restore active room
    active_room_name = data.get("active_room")
    active_room = Room.rooms.get(active_room_name)

    if active_room:
        print(f"Loaded from {filename} successfully")
        print(f"Active room: {active_room.name}")
        print(f"Inventory: {list(inventory.items.keys())}")
    else:
        print(f"Warning: Active room '{active_room_name}' not found")

    # Restore player position
    player_data = data.get("player", {})

    # Final debugging
    debug_inventory_state(inventory, "Final Load Result")
    debug_room_items(Room.rooms, "After Room Restoration")
    debug_load_process(filename, active_room, inventory, player_data)

    debug.log("Load operation completed successfully")
    return active_room, inventory, player_data


# ===== NEW SLOT-BASED SAVE SYSTEM =====

def get_slot_filename(slot_number):
    """Get the filename for a given slot number (0-9)."""
    return f"saves/save_slot_{slot_number}.yaml"


def get_slot_thumbnail_filename(slot_number):
    """Get the thumbnail filename for a given slot number."""
    return f"saves/save_slot_{slot_number}.png"


def SaveStateToSlot(active_room, inventory, player, slot_number, playtime_seconds=0, thumbnail_surface=None):
    """Save the current game state to a specific slot with metadata and thumbnail.

    Args:
        active_room: Current active room
        inventory: Current inventory state
        player: Player sprite group
        slot_number: Slot number (0-9, where 0 is auto-save)
        playtime_seconds: Total playtime in seconds
        thumbnail_surface: Pygame surface to save as thumbnail (optional)
    """
    filename = get_slot_filename(slot_number)
    debug.log(f"Starting save operation to slot {slot_number}: {filename}")
    debug_inventory_state(inventory, "Before Save")

    # Ensure saves directory exists
    os.makedirs("saves", exist_ok=True)

    # Create metadata
    metadata = {
        "slot_number": slot_number,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "room_name": active_room.name,
        "playtime_seconds": playtime_seconds,
        "has_thumbnail": thumbnail_surface is not None
    }

    # Create save data with versioning and metadata
    savedata = {
        "save_version": "2.1",  # Updated version for slot system
        "game_content_hash": "lucky_luke_olympic_blunders",
        "metadata": metadata,
        "rooms": {},
        "inventory": {},
        "active_room": active_room.name
    }

    debug.log(f"Active room for save: {active_room.name}")
    debug.log(f"Playtime: {playtime_seconds} seconds")

    # Save room states
    for room in Room.rooms.values():
        room_data = {
            "doors": {},
            "actions": {},
            "items": {},
            "npcs": {}
        }

        for door in room.doors.values():
            room_data["doors"][door.name] = {"locked": door.locked}

        for item in room.items.values():
            room_data["items"][item.name] = {
                "stashed": item.stashed,
                "allow_destroy": item.allow_destroy
            }

        for action in room.actions.values():
            room_data["actions"][action.name] = {
                "locked": action.locked,
                "state": action.state,
                "imagepath": action.imagepath
            }

        for npc in room.npcs.values():
            room_data["npcs"][npc.name] = {
                "active_dialog": npc.active_dialog,
                "locked": npc.locked
            }

        savedata["rooms"][room.name] = room_data

    # Save inventory using slot-based format
    if hasattr(inventory, 'get_slot_data_for_save'):
        savedata["inventory"] = inventory.get_slot_data_for_save()
        print(f"Saved inventory with slot-based format: {len(inventory.items)} items")
    else:
        savedata["inventory"] = {}
        for item in inventory.items.values():
            savedata["inventory"][item.name] = {
                "stashed": item.stashed,
                "allow_destroy": item.allow_destroy,
                "self_destruct": item.self_destruct,
                "left": item.rect.left,
                "top": item.rect.top,
                "width": item.rect.width,
                "height": item.rect.height,
                "imagepath": item.imagepath
            }
        print(f"Saved inventory with legacy format: {len(inventory.items)} items")

    # Save player location
    savedata["player"] = {
        "left": player.sprites()[0].rect.left,
        "top": player.sprites()[0].rect.top
    }

    # Save playtime
    savedata["playtime_seconds"] = playtime_seconds

    try:
        # Debug the save data before writing
        debug_save_data(savedata, "Before Write")

        yaml_output = yaml.dump(savedata, sort_keys=False)
        with open(filename, 'w') as f:
            f.write(yaml_output)

        debug.log(f"Save completed successfully: {len(yaml_output)} bytes written")
        print(f"Game saved to slot {slot_number} successfully")

        # Save thumbnail if provided
        if thumbnail_surface:
            thumbnail_filename = get_slot_thumbnail_filename(slot_number)
            pygame.image.save(thumbnail_surface, thumbnail_filename)
            debug.log(f"Thumbnail saved: {thumbnail_filename}")
            print(f"Thumbnail saved for slot {slot_number}")

        return True

    except IOError as e:
        debug.log(f"IO Error during save: {e}", "ERROR")
        print(f"Error saving game: {e}")
        return False
    except yaml.YAMLError as e:
        debug.log(f"YAML Error during save: {e}", "ERROR")
        print(f"Error serializing game state: {e}")
        return False


def LoadStateFromSlot(slot_number):
    """Load a game state from a specific slot.

    Returns:
        tuple: (active_room, inventory, player_data, playtime_seconds) or (None, None, None, 0) if failed
    """
    filename = get_slot_filename(slot_number)
    debug.log(f"Starting load operation from slot {slot_number}: {filename}")

    try:
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        debug.log(f"Successfully parsed YAML data: {len(str(data))} characters")
    except FileNotFoundError:
        debug.log(f"Save file not found: {filename}", "ERROR")
        print(f"Save slot {slot_number} is empty")
        return None, None, None, 0
    except yaml.YAMLError as e:
        debug.log(f"YAML parsing error: {e}", "ERROR")
        print(f"Error parsing save file: {e}")
        return None, None, None, 0
    except IOError as e:
        debug.log(f"File reading error: {e}", "ERROR")
        print(f"Error reading save file: {e}")
        return None, None, None, 0

    if not data:
        debug.log("Save file contains no data", "ERROR")
        print("Save file is empty or invalid")
        return None, None, None, 0

    # Debug the loaded data
    debug_save_data(data, "Loaded from File")

    # Validate compatibility
    is_compatible, message = validate_save_compatibility(data)
    if not is_compatible:
        debug.log(f"Compatibility validation failed: {message}", "ERROR")
        print(f"Save file incompatible: {message}")
        return None, None, None, 0

    debug.log(f"Save validation: {message}")
    print(f"Save validation: {message}")

    # Restore room states
    for room_name, room_data in data.get("rooms", {}).items():
        if room_name not in Room.rooms:
            continue

        room = Room.rooms[room_name]

        # Restore door states
        for door_name, door_data in room_data.get("doors", {}).items():
            if door_name in room.doors:
                room.doors[door_name].locked = door_data["locked"]

        # Properly restore room items to saved state
        saved_items = room_data.get("items", {})

        # Remove items that weren't in the room when saved
        items_to_delete = [
            item_name for item_name in room.items
            if item_name not in saved_items
        ]
        for item_name in items_to_delete:
            debug.log(f"Removing '{item_name}' from room '{room_name}' (not in save)")
            del room.items[item_name]

        # Add back items that should be in the room but aren't currently there
        for item_name, item_data in saved_items.items():
            if item_name not in room.items:
                if item_name in Item.items:
                    item = Item.items[item_name]
                    # Remove from any current room or inventory
                    for other_room in Room.rooms.values():
                        if item_name in other_room.items and other_room != room:
                            del other_room.items[item_name]

                    # Restore item properties from save
                    item.allow_destroy = item_data.get("allow_destroy", False)
                    item.stashed = False

                    # Add to room
                    room.items[item_name] = item
                    debug.log(f"Restored '{item_name}' to room '{room_name}'")
                else:
                    debug.log(f"Warning: Item '{item_name}' not found in global registry", "WARNING")

        # Restore action states
        for action_name, action_data in room_data.get("actions", {}).items():
            if action_name in room.actions:
                action = room.actions[action_name]
                action.locked = action_data["locked"]
                action.state = action_data["state"]
                action.imagepath = action_data["imagepath"]

        # Restore NPC states
        for npc_name, npc_data in room_data.get("npcs", {}).items():
            if npc_name in room.npcs:
                npc = room.npcs[npc_name]
                npc.active_dialog = npc_data["active_dialog"]
                npc.locked = npc_data["locked"]

    # Before restoring inventory, collect items that were restored to rooms
    items_in_rooms = set()
    for room_name, room_data in data.get("rooms", {}).items():
        for item_name in room_data.get("items", {}):
            items_in_rooms.add(item_name)

    debug.log(f"Items restored to rooms: {items_in_rooms}")

    # Restore inventory with support for both old and new formats
    inventory = Inventory()
    inventory_data = data.get("inventory", {})

    # Detect save format
    if "slots" in inventory_data:
        print("Loading inventory using new slot-based format")
        errors = inventory.restore_inventory_from_slots(inventory_data, debug=True, skip_items=items_in_rooms)
        if errors:
            print("Inventory restoration warnings:")
            for error in errors:
                print(f"  - {error}")
    else:
        print("Loading inventory using legacy format")
        inventory.items = {}

        for item_name, item_data in inventory_data.items():
            if item_name in items_in_rooms:
                debug.log(f"Skipping '{item_name}' in inventory - restored to room")
                continue

            self_destruct = item_data.get("self_destruct", item_data.get("selfdestruct", False))

            item = Item(
                0, 0,
                item_data["width"],
                item_data["height"],
                item_data["imagepath"],
                item_name,
                self_destruct
            )

            item.allow_destroy = item_data["allow_destroy"]
            item.stashed = True

            for room in Room.rooms.values():
                if item_name in room.items:
                    del room.items[item_name]

            inventory.items[item_name] = item
            pos = inventory.get_available_slots(item)
            if pos:
                item.rect.topleft = pos
                item.position = pygame.Vector2(pos)
                print(f"Restored item '{item_name}' to inventory slot at {pos}")
            else:
                print(f"Warning: No slot available for item '{item_name}'")

    # Restore active room
    active_room_name = data.get("active_room")
    active_room = Room.rooms.get(active_room_name)

    # Restore player position
    player_data = data.get("player", {})

    # Restore playtime
    playtime_seconds = data.get("playtime_seconds", 0)

    if active_room:
        print(f"Loaded from slot {slot_number} successfully")
        print(f"Active room: {active_room.name}")
        print(f"Inventory: {list(inventory.items.keys())}")
        print(f"Playtime: {playtime_seconds} seconds")
    else:
        print(f"Warning: Active room '{active_room_name}' not found")

    # Final debugging
    debug_inventory_state(inventory, "Final Load Result")
    debug_room_items(Room.rooms, "After Room Restoration")
    debug_load_process(filename, active_room, inventory, player_data)

    debug.log("Load operation completed successfully")
    return active_room, inventory, player_data, playtime_seconds


def GetSlotMetadata(slot_number):
    """Get metadata for a specific save slot without loading the full save.

    Returns:
        dict or None: Metadata dictionary or None if slot is empty/invalid
        {
            "slot_number": int,
            "timestamp": str,
            "room_name": str,
            "playtime_seconds": int,
            "has_thumbnail": bool
        }
    """
    filename = get_slot_filename(slot_number)

    if not os.path.exists(filename):
        return None

    try:
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)

        if not data:
            return None

        # For v2.1+ saves with metadata section
        if "metadata" in data:
            return data["metadata"]

        # For older saves, construct basic metadata
        return {
            "slot_number": slot_number,
            "timestamp": "Unknown",
            "room_name": data.get("active_room", "Unknown"),
            "playtime_seconds": data.get("playtime_seconds", 0),
            "has_thumbnail": False
        }

    except Exception as e:
        debug.log(f"Error reading slot {slot_number} metadata: {e}", "ERROR")
        return None


def GetAllSlotMetadata():
    """Get metadata for all 10 save slots (0-9).

    Returns:
        dict: Dictionary mapping slot number to metadata (or None if empty)
    """
    metadata = {}
    for slot_num in range(10):  # 0-9 slots
        metadata[slot_num] = GetSlotMetadata(slot_num)
    return metadata


def DeleteSlot(slot_number):
    """Delete a save slot and its thumbnail.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        filename = get_slot_filename(slot_number)
        thumbnail_filename = get_slot_thumbnail_filename(slot_number)

        # Delete save file
        if os.path.exists(filename):
            os.remove(filename)
            debug.log(f"Deleted save slot {slot_number}: {filename}")

        # Delete thumbnail
        if os.path.exists(thumbnail_filename):
            os.remove(thumbnail_filename)
            debug.log(f"Deleted thumbnail for slot {slot_number}")

        print(f"Save slot {slot_number} deleted successfully")
        return True

    except Exception as e:
        debug.log(f"Error deleting slot {slot_number}: {e}", "ERROR")
        print(f"Error deleting save slot {slot_number}: {e}")
        return False


def GetMostRecentSlot():
    """Find the most recently saved slot (excluding auto-save slot 0).

    Returns:
        int or None: Slot number of most recent save, or None if no saves exist
    """
    most_recent_slot = None
    most_recent_time = None

    for slot_num in range(1, 10):  # Skip slot 0 (auto-save)
        metadata = GetSlotMetadata(slot_num)
        if metadata and metadata.get("timestamp"):
            try:
                timestamp_str = metadata["timestamp"]
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

                if most_recent_time is None or timestamp > most_recent_time:
                    most_recent_time = timestamp
                    most_recent_slot = slot_num
            except Exception:
                continue

    return most_recent_slot


def MigrateOldSave():
    """Migrate old save.yaml to new slot-based system (slot 1).

    Returns:
        bool: True if migration occurred, False if no old save found
    """
    old_save_path = "save.yaml"

    if not os.path.exists(old_save_path):
        return False

    try:
        # Read old save
        with open(old_save_path, 'r') as f:
            old_data = yaml.safe_load(f)

        if not old_data:
            return False

        # Add metadata for slot 1
        if "metadata" not in old_data:
            old_data["metadata"] = {
                "slot_number": 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "room_name": old_data.get("active_room", "Unknown"),
                "playtime_seconds": 0,
                "has_thumbnail": False
            }

        # Update version
        old_data["save_version"] = "2.1"

        # Ensure saves directory exists
        os.makedirs("saves", exist_ok=True)

        # Write to new slot
        new_save_path = get_slot_filename(1)
        with open(new_save_path, 'w') as f:
            yaml.dump(old_data, f, sort_keys=False)

        print("=" * 60)
        print("SAVE FILE MIGRATED")
        print("=" * 60)
        print(f"Your old save file has been migrated to Slot 1")
        print(f"The new save system supports 9 save slots!")
        print("=" * 60)

        # Optionally delete old save (or rename it)
        os.rename(old_save_path, "save.yaml.backup")
        print(f"Old save backed up as: save.yaml.backup")

        return True

    except Exception as e:
        debug.log(f"Error migrating old save: {e}", "ERROR")
        print(f"Error migrating old save file: {e}")
        return False
