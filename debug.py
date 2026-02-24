"""
Debug utilities for the save/load system

Provides comprehensive logging and state tracking for troubleshooting
inventory restoration and save system issues.
"""

import pygame
from datetime import datetime


class SaveDebugger:
    """Centralized debug logging for save/load operations"""

    def __init__(self, enabled=True):
        self.enabled = enabled
        self.log_entries = []

    def log(self, message, level="INFO"):
        """Add a debug log entry"""
        if not self.enabled:
            return

        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = f"[{timestamp}] {level}: {message}"
        self.log_entries.append(entry)
        print(entry)

    def debug_inventory_state(self, inventory, context=""):
        """Debug helper to track inventory state comprehensively"""
        if not self.enabled:
            return

        self.log(f"=== Inventory Debug: {context} ===", "DEBUG")

        # Basic counts
        items_count = len(inventory.items) if hasattr(inventory, 'items') else 0
        self.log(f"Items in inventory.items: {items_count}")

        if hasattr(inventory, 'slots'):
            occupied_slots = sum(1 for slot in inventory.slots.values() if slot.get("item") is not None)
            self.log(f"Occupied slots: {occupied_slots}/{len(inventory.slots)}")
        else:
            self.log("No slot system detected")

        # Detailed item information
        if hasattr(inventory, 'items') and inventory.items:
            self.log("Item details:")
            for item_name, item in inventory.items.items():
                pos = (item.rect.left, item.rect.top) if hasattr(item, 'rect') else (0, 0)
                stashed = getattr(item, 'stashed', 'unknown')
                self.log(f"  {item_name}: pos={pos}, stashed={stashed}")

            # Check for slot consistency
            if hasattr(inventory, 'slots'):
                self.log("Slot consistency check:")
                for slot_id, slot in inventory.slots.items():
                    if slot["item"] is not None:
                        item_name = slot["item"].name if hasattr(slot["item"], 'name') else 'unnamed'
                        self.log(f"  Slot {slot_id}: {item_name}")

        self.log("=" * (len(context) + 24))

    def debug_save_data(self, save_data, context=""):
        """Debug save data structure"""
        if not self.enabled:
            return

        self.log(f"=== Save Data Debug: {context} ===", "DEBUG")

        # Basic structure
        version = save_data.get("save_version", "unknown")
        active_room = save_data.get("active_room", "unknown")
        self.log(f"Save version: {version}")
        self.log(f"Active room: {active_room}")

        # Inventory structure
        inventory_data = save_data.get("inventory", {})
        if "slots" in inventory_data:
            slots = inventory_data["slots"]
            self.log(f"Slot-based inventory with {len(slots)} slots")
            for slot_id, item_info in slots.items():
                item_name = item_info.get("item_name", "unknown")
                self.log(f"  Slot {slot_id}: {item_name}")
        else:
            self.log(f"Legacy inventory with {len(inventory_data)} items")
            for item_name in inventory_data.keys():
                self.log(f"  Item: {item_name}")

        # Room states
        rooms = save_data.get("rooms", {})
        self.log(f"Rooms in save: {len(rooms)}")
        for room_name in rooms.keys():
            self.log(f"  Room: {room_name}")

        self.log("=" * (len(context) + 22))

    def debug_load_process(self, filename, loaded_room, inventory, player_pos):
        """Debug the complete load process"""
        if not self.enabled:
            return

        self.log(f"=== Load Process Debug: {filename} ===", "DEBUG")

        # Load results
        self.log(f"Loaded room: {loaded_room.name if loaded_room else 'None'}")
        self.log(f"Loaded inventory: {'Success' if inventory else 'Failed'}")
        self.log(f"Player position: {player_pos}")

        if inventory:
            self.debug_inventory_state(inventory, "After Load")

        self.log("=" * (len(filename) + 26))

    def debug_room_items(self, rooms, context=""):
        """Debug items in all rooms"""
        if not self.enabled:
            return

        self.log(f"=== Room Items Debug: {context} ===", "DEBUG")

        for room_name, room in rooms.items():
            if hasattr(room, 'items') and room.items:
                self.log(f"Room '{room_name}':")
                for item_name, item in room.items.items():
                    stashed = getattr(item, 'stashed', 'unknown')
                    self.log(f"  {item_name}: stashed={stashed}")
            else:
                self.log(f"Room '{room_name}': no items")

        self.log("=" * (len(context) + 25))

    def get_log_summary(self):
        """Get a summary of recent log entries"""
        if not self.log_entries:
            return "No debug logs recorded"

        recent_logs = self.log_entries[-20:]  # Last 20 entries
        return "\n".join(recent_logs)

    def clear_logs(self):
        """Clear all log entries"""
        self.log_entries.clear()
        self.log("Debug logs cleared")


# Global debug instance
debug = SaveDebugger(enabled=True)


def debug_inventory_state(inventory, context=""):
    """Convenience function for inventory debugging"""
    debug.debug_inventory_state(inventory, context)


def debug_save_data(save_data, context=""):
    """Convenience function for save data debugging"""
    debug.debug_save_data(save_data, context)


def debug_load_process(filename, loaded_room, inventory, player_pos):
    """Convenience function for load process debugging"""
    debug.debug_load_process(filename, loaded_room, inventory, player_pos)


def debug_room_items(rooms, context=""):
    """Convenience function for room items debugging"""
    debug.debug_room_items(rooms, context)


def toggle_debug(enabled=None):
    """Toggle or set debug logging state"""
    if enabled is None:
        debug.enabled = not debug.enabled
    else:
        debug.enabled = enabled

    debug.log(f"Debug logging {'enabled' if debug.enabled else 'disabled'}")
    return debug.enabled