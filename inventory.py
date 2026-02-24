import pygame
import os

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT, at_percentage_width


class Inventory(pygame.sprite.Sprite):
    containers = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - INVENTORY_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT)
        self.items = {}  # Instance variable, not class variable
        self.slots = {}  # Instance variable, not class variable
        self._init_slots()

    def _init_slots(self):
        """Initialize inventory slots."""
        for i in range(20):
            self.slots[i] = {
                "pos": (at_percentage_width(i * 5) + 5, SCREEN_HEIGHT - INVENTORY_HEIGHT + 5),
                "item": None
            }

    def draw(self, screen):
        inv = pygame.draw.rect(screen, "brown", self.rect)
        screen.fill("brown", inv)
        for item in self.items.values():
            item.draw(screen)

    def update(self, dt):
        pass

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def get_available_slots(self, item):
        """Find and assign an available slot for an item."""
        for slot in self.slots.values():
            if slot["item"] is None:
                slot["item"] = item
                return slot["pos"]
        return None

    def release_slots(self, item):
        """Release the slot occupied by an item."""
        for slot in self.slots.values():
            if slot["item"] == item:
                slot["item"] = None
                return

    def clear_all_slots(self):
        """Clear all inventory slots - used during save restoration"""
        for slot in self.slots.values():
            slot["item"] = None
        print("All inventory slots cleared")

    def get_slot_data_for_save(self):
        """Get inventory data in slot-based format for saving"""
        slot_data = {}
        slot_index = 0

        for item_name, item in self.items.items():
            # Find which slot this item occupies
            for slot_id, slot in self.slots.items():
                if slot["item"] == item:
                    slot_data[str(slot_id)] = {
                        "item_name": item_name,
                        "allow_destroy": getattr(item, 'allow_destroy', False),
                        "self_destruct": getattr(item, 'self_destruct', False),
                        "imagepath": getattr(item, 'imagepath', ''),
                        "width": item.rect.width,
                        "height": item.rect.height
                    }
                    break

        return {"slots": slot_data}

    def restore_inventory_from_slots(self, slot_data, debug=False, skip_items=None):
        """Restore inventory from slot-based save data"""
        if debug:
            print("=== Restoring Inventory from Slot Data ===")

        # Items to skip (e.g., items restored to rooms)
        skip_items = skip_items or set()
        if skip_items and debug:
            print(f"Skipping items restored to rooms: {skip_items}")

        # Clear current state
        self.clear_all_slots()
        self.items.clear()

        errors = []
        restored_count = 0

        for slot_id_str, item_info in slot_data.get("slots", {}).items():
            try:
                slot_id = int(slot_id_str)
                if slot_id >= len(self.slots):
                    errors.append(f"Invalid slot ID: {slot_id}")
                    continue

                item_name = item_info["item_name"]

                # Skip items that were restored to rooms
                if item_name in skip_items:
                    if debug:
                        print(f"  Skipping '{item_name}' - restored to room")
                    continue

                # Create item for this slot
                from item import Item

                # Handle missing image paths gracefully
                imagepath = item_info.get("imagepath", "")
                if not imagepath or not os.path.exists(imagepath):
                    # Skip items with missing images during restoration
                    if debug:
                        print(f"  Skipping '{item_name}': missing image '{imagepath}'")
                    continue

                item = Item(
                    0, 0,  # Position will be set by slot
                    item_info.get("width", 50),
                    item_info.get("height", 50),
                    imagepath,
                    item_name,
                    item_info.get("self_destruct", False)
                )

                # Set item properties
                item.allow_destroy = item_info.get("allow_destroy", False)
                item.stashed = True

                # Place in specific slot
                slot = self.slots[slot_id]
                slot["item"] = item
                item.rect.topleft = slot["pos"]
                item.position = pygame.Vector2(slot["pos"])

                # Add to items dictionary
                self.items[item_name] = item

                restored_count += 1
                if debug:
                    print(f"  Restored '{item_name}' to slot {slot_id}")

            except (ValueError, KeyError) as e:
                errors.append(f"Error restoring slot {slot_id_str}: {e}")

        if debug:
            print(f"Restored {restored_count} items with {len(errors)} errors")
            if errors:
                for error in errors:
                    print(f"  Error: {error}")

        return errors
