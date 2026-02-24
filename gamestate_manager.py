"""Game State Manager for Adventure Game Engine

This module provides a singleton GameStateManager class that enables safe
state transitions and cutscene management from within action functions.
It serves as a bridge between ActionFuncs and the main game loop.
"""

import os
from collections import deque
from textcutscene import TextCutscene


class GameStateManager:
    """
    Singleton class for managing game state transitions and cutscene queueing.

    This class provides a safe way for ActionFuncs to request cutscenes without
    directly manipulating global game state variables. It maintains a queue of
    pending cutscenes and a stack of previous states for proper transition handling.
    """

    _instance = None

    def __init__(self):
        """Initialize the GameStateManager with empty queue and state stack."""
        if GameStateManager._instance is not None:
            raise Exception("GameStateManager is a singleton. Use get_instance() instead.")

        self.cutscene_queue = deque()  # Queue of pending cutscene file paths
        self.state_stack = []          # Stack of previous game states
        self.current_cutscene = None   # Currently loaded cutscene object

        GameStateManager._instance = self

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of GameStateManager.

        Returns:
            GameStateManager: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def enqueue_cutscene(self, yaml_path):
        """
        Safely enqueue a cutscene for playback.

        This method validates the file exists and adds it to the queue.
        Called by ActionFuncs to request cutscene playback.

        Args:
            yaml_path (str): Path to the YAML cutscene file

        Returns:
            bool: True if cutscene was enqueued successfully, False otherwise
        """
        try:
            # Validate file exists
            if not os.path.exists(yaml_path):
                print(f"GameStateManager: Cutscene file not found: {yaml_path}")
                return False

            # Validate file extension
            if not yaml_path.lower().endswith(('.yaml', '.yml')):
                print(f"GameStateManager: Invalid cutscene file format: {yaml_path}")
                return False

            # Add to queue
            self.cutscene_queue.append(yaml_path)
            print(f"GameStateManager: Cutscene queued successfully: {yaml_path}")
            return True

        except Exception as e:
            print(f"GameStateManager: Error queueing cutscene {yaml_path}: {e}")
            return False

    def get_pending_cutscene(self):
        """
        Get the next pending cutscene from the queue.

        This method is called by the main game loop to check for pending cutscenes.
        It creates and returns a TextCutscene object if one is queued.

        Returns:
            TextCutscene or None: The next cutscene to play, or None if queue is empty
        """
        if not self.cutscene_queue:
            return None

        try:
            yaml_path = self.cutscene_queue.popleft()
            cutscene = TextCutscene(yaml_path)
            self.current_cutscene = cutscene
            print(f"GameStateManager: Loading cutscene: {yaml_path}")
            return cutscene

        except Exception as e:
            print(f"GameStateManager: Error loading cutscene: {e}")
            return None

    def push_state(self, current_state):
        """
        Save the current game state before transitioning to cutscene.

        This enables the system to return to the exact previous state
        after the cutscene completes.

        Args:
            current_state (str): The current game state to save
        """
        self.state_stack.append(current_state)
        print(f"GameStateManager: State saved: {current_state}")

    def pop_state(self):
        """
        Return to the previous game state after cutscene completion.

        Returns:
            str or None: The previous state to return to, or None if stack is empty
        """
        if not self.state_stack:
            print("GameStateManager: Warning - No previous state to return to")
            return None

        previous_state = self.state_stack.pop()
        print(f"GameStateManager: Returning to state: {previous_state}")
        return previous_state

    def has_pending_cutscenes(self):
        """
        Check if there are any pending cutscenes in the queue.

        Returns:
            bool: True if cutscenes are queued, False otherwise
        """
        return len(self.cutscene_queue) > 0

    def clear_queue(self):
        """
        Clear all pending cutscenes from the queue.

        This method can be used for cleanup or emergency reset.
        """
        self.cutscene_queue.clear()
        print("GameStateManager: Cutscene queue cleared")

    def get_queue_size(self):
        """
        Get the number of pending cutscenes in the queue.

        Returns:
            int: Number of cutscenes waiting to be played
        """
        return len(self.cutscene_queue)

    def reset(self):
        """
        Reset the GameStateManager to initial state.

        Clears the cutscene queue and state stack. Used for cleanup
        when returning to menu or starting a new game.
        """
        self.cutscene_queue.clear()
        self.state_stack.clear()
        self.current_cutscene = None
        print("GameStateManager: Reset complete")


# Convenience function for ActionFuncs to access the manager easily
def get_game_state_manager():
    """
    Convenience function to get the GameStateManager instance.

    Returns:
        GameStateManager: The singleton instance
    """
    return GameStateManager.get_instance()