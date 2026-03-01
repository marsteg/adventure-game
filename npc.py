import pygame
import yaml
import time

from rectshape import RectShape
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    at_percentage_width, at_percentage_height
)
from dialogbox import DialogBox, VoiceManager
from answer import Answer
from dialogfuncs import ChangeDialog, ExitDialog, TakeItemString, UnlockNPC


# Registry for dialog functions - safer than using globals()
DIALOG_FUNCTIONS = {
    'ChangeDialog': ChangeDialog,
    'ExitDialog': ExitDialog,
    'TakeItemString': TakeItemString,
    'UnlockNPC': UnlockNPC,
}


class NPC(RectShape):
    _id_counter = 1
    containers = []
    NPCs = {}

    def __init__(self, left, top, width, height, image, name, locked, key, speechcolor, dialogfile):
        super().__init__(left, top, width, height, image)
        self.rotation = 0
        self.id = NPC._id_counter
        NPC._id_counter += 1
        self.position = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.name = name
        self.functions = []
        self.locked = locked
        self.key = key
        self.active_dialog = "start"
        self.dialogfile = dialogfile
        self.dialog = self._load_dialog()
        self.speechcolor = speechcolor
        self.dialogline = 0
        NPC.NPCs[self.id] = self

    def add_function(self, func, *args, **kwargs):
        self.functions.append((func, args, kwargs))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        pass

    def action(self):
        if self.locked:
            print("NPC is locked")
            return
        for func, args, kwargs in self.functions:
            func(*args, **kwargs)
            print("Action Function triggered in position: ", self.position)

    def unlock(self, key, inventory):
        if self.key is None:
            print("No key required")
            return
        if key.name != self.key.name:
            print("Wrong key")
            return
        print("NPC unlocked: ", self.locked)
        self.locked = False
        key.allow_destroy = True
        self.action()

    def _load_dialog(self):
        """Load dialog from YAML file with error handling."""
        try:
            with open(self.dialogfile, 'r') as file:
                dialog = yaml.safe_load(file)
                print("Dialog loaded: ", dialog)

                # Validate that description exists, if not create a default
                if "description" not in dialog:
                    print(f"Warning: No 'description' section in {self.dialogfile} for NPC {self.name}")
                    print(f"Creating default description...")
                    # Create a default description
                    dialog["description"] = {
                        "locked": {
                            "line": f"{self.name} doesn't want to talk right now.",
                            "sound": "assets/sounds/dialogs/default_locked.wav"
                        },
                        "unlocked": {
                            "line": f"{self.name} looks friendly.",
                            "sound": "assets/sounds/dialogs/default_unlocked.wav"
                        }
                    }

                return dialog
        except FileNotFoundError:
            print(f"Dialog file not found: {self.dialogfile}")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing dialog file {self.dialogfile}: {e}")
            return {}

    def shutup(self):
        self.active_dialog = "bye"

    def speak(self):
        sound = self.dialog[self.active_dialog]["sound"]
        if isinstance(sound, list):
            sound = sound[self.dialogline]
        print("Speaking: ", self.name, "dialog:", sound)
        VoiceManager.play_voice(sound)

    def speak_description(self):
        if self.locked:
            line = self.dialog["description"]["locked"]["sound"]
        else:
            line = self.dialog["description"]["unlocked"]["sound"]
        print(line)
        VoiceManager.play_voice(line)

    def talk_description(self, room):
        # Clean up any existing dialog boxes for this NPC to prevent accumulation
        for existing_dialog in DialogBox.dialogboxes[:]:  # Use slice to avoid modification during iteration
            existing_speaker = getattr(existing_dialog, 'speaking_npc', None)
            if existing_speaker == self:
                existing_dialog.kill()

        dialbox = DialogBox(room, time.time())
        dialbox.state = "describe"
        dialbox.room = room

        if self.locked:
            line = self.dialog["description"]["locked"]["line"]
            sound_file = self.dialog["description"]["locked"]["sound"]
        else:
            line = self.dialog["description"]["unlocked"]["line"]
            sound_file = self.dialog["description"]["unlocked"]["sound"]

        print("Describe Talking: ", self.name, "dialog:", line)

        # Calculate duration from sound file
        from dialogbox import get_sound_duration
        dialbox.dialog_duration = get_sound_duration(sound_file)

        # Store text for new renderer
        dialbox.dialog_text = line
        dialbox.speaker_name = ""
        dialbox.speaking_npc = self  # Add NPC reference for positioning

    def describe(self, room):
        print("NPC right-clicked: ", self.name)
        self.speak_description()
        self.talk_description(room)

    def talk(self, room, inventory, answerbox):
        """Main dialog interaction method."""
        self.timer = time.time()
        print("NPC Talking: ", self.name)

        # Clean up any existing dialog boxes for this NPC to prevent accumulation
        speaker = self._find_speaker(room)
        for existing_dialog in DialogBox.dialogboxes[:]:  # Use slice to avoid modification during iteration
            existing_speaker = getattr(existing_dialog, 'speaking_npc', None)
            if existing_speaker == speaker:
                existing_dialog.kill()

        dialbox = DialogBox(room, time.time())
        dialbox.state = self
        dialbox.room = room
        self.speak()

        # Find the speaker (might be a different NPC)
        speaker = self._find_speaker(room)

        line = speaker.dialog[self.active_dialog]["line"]
        if isinstance(line, list):
            # Setup for array of lines
            dialbox.total_lines = len(line)
            dialbox.total_duration = speaker.dialog[self.active_dialog].get("duration", 3)
            dialbox.line_duration = dialbox.total_duration / dialbox.total_lines
            dialbox.current_line_index = self.dialogline
            dialbox.auto_advance = True
            dialbox.dialog_duration = dialbox.line_duration  # Use per-line duration
            line = line[self.dialogline]
        else:
            # Single line - use existing behavior
            dialbox.auto_advance = False
            dialbox.line_duration = speaker.dialog[self.active_dialog].get("duration", 3)
            dialbox.dialog_duration = dialbox.line_duration  # Use full duration

        print("NPC Talking: ", speaker.name, "dialog:", line)

        # Store text and speaker info for new renderer
        dialbox.dialog_text = line
        dialbox.speaker_name = speaker.name
        dialbox.speaker_color = speaker.speechcolor
        dialbox.speaking_npc = speaker  # Add NPC reference for positioning

        # Check if the dialog unlocks something
        if self.dialog[self.active_dialog].get("unlock") is True:
            print("Calling unlock function")
            self.unlock(self.key, inventory)

        # Check if dialog has an exit
        exit_data = self.dialog[self.active_dialog].get("exit", {})
        if "ExitDialog" in exit_data:
            answerbox.answers = {}
            answerbox.state = None
            answerbox.room = None
            self.active_dialog = exit_data["ExitDialog"]
            return

        # Build answers only if this is not an incomplete array dialog
        line = speaker.dialog[self.active_dialog]["line"]
        if isinstance(line, list):
            # For array dialogs, only show answers after the last line
            if self.dialogline >= len(line) - 1:
                self._build_answers(room, inventory, answerbox)
            else:
                # Clear any existing answers - don't show until array is complete
                answerbox.answers = {}
                answerbox.state = None
        else:
            # Single line dialog - show answers immediately
            self._build_answers(room, inventory, answerbox)

    def _find_speaker(self, room):
        """Find the NPC who should speak (might be different from self)."""
        speaker_name = self.dialog[self.active_dialog]["speaker"]
        for npc in room.npcs.values():
            if npc.name == speaker_name:
                return npc
        return self

    def _build_answers(self, room, inventory, answerbox):
        """Build answer options from dialog data."""
        answers_data = self.dialog[self.active_dialog].get("answers")
        if not answers_data:
            return

        answerbox.answers = {}
        answerbox.state = answers_data
        answerbox.room = room

        for i, answer_data in enumerate(answers_data):
            answer = Answer(answer_data["line"], i)
            answerbox.add_answer(answer)

            for action in answer_data.get("actionfuncs", []):
                for func_name, args in action.items():
                    func = DIALOG_FUNCTIONS.get(func_name)
                    if func:
                        if isinstance(args, list):
                            func_args = (*args, room, self, inventory, answerbox)
                        else:
                            func_args = (args, room, self, inventory, answerbox)
                        answer.add_dialogfunction(func, *func_args)
                        print(f"Function added: {func_name} with args: {args}")
                    else:
                        print(f"Function {func_name} not found in DIALOG_FUNCTIONS.")

            answer.npc = self
