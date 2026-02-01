import pygame
import yaml
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class TextCutscene:
    """Displays a story text with typewriter effect for intros or cutscenes."""

    def __init__(self, yaml_path=None):
        if yaml_path:
            self.load_from_yaml(yaml_path)
        else:
            self._setup_default_intro()


        self.slides = [
            {
                "title": "Grimwood Academy",
                "text": [
                    "Welcome to Grimwood Academy for the Magically Gifted...",
                    "...and their emotionally unavailable parents.",
                    "Where werewolf kids learn next to zombie toddlers. Health & Safety gave up years ago."
                ]
            },
            {
                "title": "You Are Morticia",
                "text": [
                    "You are Morticia - yes, THAT Morticia. Daughter of Death himself.",
                    "Dad wanted you to follow the family business. You wanted a gap year.",
                    "Compromise: Magic school. At least the cafeteria serves souls on Tuesdays."
                ]
            },
            {
                "title": "Something Is Wrong",
                "text": [
                    "But something dark lurks beneath the school's cheerful facade...",
                    "(Besides the literal dungeon. That's just the gym.)",
                    "Students whisper about the Order of the Crimson Moon. Teachers change the subject.",
                    "The Dean smiles too much. Nobody smiles that much without hiding something."
                ]
            },
            {
                "title": "Your Mission",
                "text": [
                    "Uncover the school's dark secret before it's too late.",
                    "Make friends. Make enemies. Make questionable life choices.",
                    "And maybe, just maybe, earn the right to leave this place...",
                    "",
                    "...for a trip to Wonderland. (Dad owes you big time.)"
                ]
            }
        ]
        self.current_slide = 0
        self.char_index = 0
        self.line_index = 0
        self.timer = 0
        self.char_delay = 35  # ms between characters
        self.line_delay = 800  # ms between lines
        self.waiting_for_line = False
        self.done = False
        self.font_title = pygame.font.Font(None, 52)
        self.font_text = pygame.font.Font(None, 32)
        self.skip_requested = False


    def _setup_default_intro(self):
        """Sets up a default intro sequence if no YAML is provided."""
        self.slides = [
            {
                "title": "Welcome to the Adventure",
                "text": [
                    "In a world full of mysteries and magic...",
                    "You are about to embark on an unforgettable journey.",
                    "Prepare yourself for challenges, friendships, and discoveries."
                ]
            },
            {
                "title": "Your Story Begins",
                "text": [
                    "You find yourself in a quaint village, surrounded by curious townsfolk.",
                    "Strange happenings have been reported lately.",
                    "It's up to you to uncover the truth and restore peace."
                ]
            }
        ]


    def update(self, dt):
        if self.done:
            return

        self.timer += dt

        if self.waiting_for_line:
            if self.timer >= self.line_delay:
                self.timer = 0
                self.waiting_for_line = False
                self.line_index += 1
                self.char_index = 0

                slide = self.slides[self.current_slide]
                if self.line_index >= len(slide["text"]):
                    # Slide complete, wait for click
                    pass
        else:
            if self.timer >= self.char_delay:
                self.timer = 0
                slide = self.slides[self.current_slide]
                if self.line_index < len(slide["text"]):
                    current_line = slide["text"][self.line_index]
                    if self.char_index < len(current_line):
                        self.char_index += 1
                    else:
                        self.waiting_for_line = True

    def next_slide(self):
        """Move to next slide or mark as done."""
        self.current_slide += 1
        self.line_index = 0
        self.char_index = 0
        self.timer = 0
        self.waiting_for_line = False

        if self.current_slide >= len(self.slides):
            self.done = True

    def skip_to_end(self):
        """Skip current slide's text animation."""
        slide = self.slides[self.current_slide]
        self.line_index = len(slide["text"]) - 1
        self.char_index = len(slide["text"][self.line_index])

    def draw(self, surface):

        # Dark background
        surface.fill((8, 8, 12))

        if self.current_slide >= len(self.slides):
            return

        slide = self.slides[self.current_slide]

        # Title with accent color
        title_surf = self.font_title.render(slide["title"], True, (210, 175, 110))
        title_x = (SCREEN_WIDTH - title_surf.get_width()) // 2
        surface.blit(title_surf, (title_x, 120))

        # Decorative line under title
        line_width = min(title_surf.get_width() + 100, SCREEN_WIDTH - 200)
        pygame.draw.line(surface, (60, 55, 50), (SCREEN_WIDTH // 2 - line_width // 2, 180),
                         (SCREEN_WIDTH // 2 + line_width // 2, 180), 1)

        # Text lines
        y = 240
        for i, line in enumerate(slide["text"]):
            if i < self.line_index:
                # Fully displayed line
                text_surf = self.font_text.render(line, True, (200, 195, 190))
            elif i == self.line_index:
                # Currently typing line
                displayed = line[:self.char_index]
                text_surf = self.font_text.render(displayed, True, (235, 230, 225))
            else:
                # Not yet displayed
                continue

            text_x = (SCREEN_WIDTH - text_surf.get_width()) // 2
            surface.blit(text_surf, (text_x, y))
            y += 45

        # "Click to continue" prompt (only when slide text is complete)
        if self.line_index >= len(slide["text"]) - 1 and self.char_index >= len(slide["text"][-1]):
            prompt = "Click to continue..." if self.current_slide < len(self.slides) - 1 else "Click to begin your adventure..."
            prompt_surf = self.font_text.render(prompt, True, (120, 115, 110))
            prompt_x = (SCREEN_WIDTH - prompt_surf.get_width()) // 2
            surface.blit(prompt_surf, (prompt_x, SCREEN_HEIGHT - 100))

        # Skip hint
        skip_surf = pygame.font.Font(None, 22).render("Press SPACE to skip", True, (80, 75, 70))
        surface.blit(skip_surf, (SCREEN_WIDTH - skip_surf.get_width() - 20, SCREEN_HEIGHT - 30))

    def load_from_yaml(self, yaml_path):
        """Load cutscene slides from a YAML file."""
        try:
            with open(yaml_path, 'r') as file:
                dialog = yaml.safe_load(file)
                print("Dialog loaded: ", dialog)
                return dialog
        except FileNotFoundError:
            print(f"Dialog file not found: {yaml_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing dialog file {yaml_path}: {e}")
            return {}
 


        
