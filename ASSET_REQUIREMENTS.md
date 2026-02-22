# Lucky Luke's Olympic Blunders - Asset Requirements

## Visual Style: Comic Book Style
- **Bright, vibrant colors**
- **Bold black outlines on all characters and objects**
- **Cartoon-like character proportions**
- **Exaggerated expressions and poses**
- **Clear, readable visual hierarchy**

## Required Assets

### BACKGROUNDS (assets/rooms/)
1. **tourist_shop.png** (1024x768)
   - Greek souvenir shop interior
   - Shelves with trinkets, postcards, fake artifacts
   - Counter with cash register
   - Mediterranean color palette (blues, whites, earth tones)
   - Comic book style with bold outlines

2. **ancient_temple.png** (1024x768)
   - Classical Greek temple interior
   - Marble columns, ancient architecture
   - Mystical atmosphere with soft glowing light
   - Oracle seating area, altar space
   - Mix of authentic ancient and tourist-friendly elements

3. **underworld_entrance.png** (1024x768)
   - Dark, mysterious cave entrance
   - River Styx with dock area
   - Atmospheric shadows and mist
   - Ancient stone architecture
   - Ominous but not too scary (keep it comedic)

4. **mount_olympus.png** (1024x768)
   - Divine throne room of the gods
   - Golden architectural elements
   - Clouds and heavenly lighting
   - Majestic but approachable atmosphere
   - Zeus's throne prominently featured

### CHARACTER SPRITES (assets/npcs/)
All characters should have comic book style with bold outlines and expressive features.

1. **shopkeeper.png** (80x120 pixels)
   - Dimitri: Middle-aged Greek man
   - Tourist shop apron or casual Mediterranean clothing
   - Friendly but slightly money-focused expression
   - Maybe holding calculator or clipboard

2. **oracle.png** (100x140 pixels)
   - Oracle of Delphi: Mystical elderly woman
   - Flowing robes, headpiece or veil
   - Wise but slightly absent-minded expression
   - Perhaps holding crystals or scrolls

3. **hermes.png** (90x130 pixels)
   - Hermes: Young, athletic messenger god
   - Winged sandals and helmet
   - Modern business-casual mixed with classical elements
   - Confident, fast-talking salesperson vibe

4. **zeus.png** (120x180 pixels)
   - Zeus: Powerful but approachable king of gods
   - Flowing beard, crown or headpiece
   - Royal robes with lightning motifs
   - Commanding presence but kind expression

### ITEMS (assets/items/)
1. **brochure.png** (40x30) - Colorful tourist brochure
2. **golden_olive.png** (50x60) - Glowing golden olive branch
3. **silver_coin.png** (30x30) - Ancient Greek drachma coin
4. **pomegranate.png** (45x55) - Magical glowing pomegranate
5. **ambrosia.png** (50x40) - Divine food with sparkly effects

### INTERACTIVE OBJECTS (assets/actions/)
1. **vase.png** (60x80) - Beautiful ancient Greek vase
2. **vase_broken.png** (60x80) - Same vase, shattered
3. **puzzle_box.png** (70x70) - Ancient puzzle box with Greek symbols
4. **charons_boat.png** (120x80) - Small boat at dock
5. **golden_throne.png** (100x120) - Zeus's magnificent throne

### DOORS (assets/doors/)
1. **temple_entrance.png** (100x150) - Stone archway entrance
2. **temple_exit.png** (80x120) - Temple exit door
3. **temple_return.png** (80x120) - Return passage to temple
4. Note: Several doors are invisible (empty filename) for mystical passages

### PLAYER CHARACTER (assets/player/)
Comic book style character representing Lucky Luke:
1. **daisy_waiting.png** - Idle pose (standing still)
2. **daisy_walking.png** - Basic walking sprite
3. **walking/left0.png** through **walking/left5.png** - 6 frames of left-walking animation
4. **walking/right0.png** through **walking/right5.png** - 6 frames of right-walking animation

### SOUND EFFECTS (assets/sounds/)

#### Background Music (assets/sounds/background/)
1. **mediterranean_breeze.wav** - Light, tourist-friendly music for shop
2. **mystical_temple.wav** - Mysterious but not scary temple ambience
3. **underworld_ambience.wav** - Dark but not terrifying underworld sounds
4. **divine_throne_room.wav** - Majestic, heavenly orchestral music

#### Voice Acting (assets/sounds/dialogs/)
**Dimitri (Shopkeeper)** - Greek accent, enthusiastic salesperson:
- dimitri_welcome.wav, dimitri_vase.wav, dimitri_insurance.wav
- dimitri_price.wav, dimitri_ancient.wav, dimitri_cosmic.wav
- dimitri_temple.wav, dimitri_broken_vase.wav, dimitri_payment.wav, dimitri_zeus.wav

**Oracle** - Mystical, wise but slightly scattered:
- oracle_vision.wav, oracle_three_gifts.wav, oracle_experience.wav
- oracle_locations.wav, oracle_luck.wav, oracle_insurance.wav
- oracle_favor.wav, oracle_hermes_hint.wav, oracle_coin_hint.wav, oracle_tourist_wisdom.wav

**Hermes** - Fast-talking, modern business style:
- hermes_intro.wav, hermes_transport.wav, hermes_payment_methods.wav
- hermes_proof.wav, hermes_premium.wav, hermes_skeptical.wav
- hermes_historical_value.wav, hermes_coin_approved.wav, hermes_boat_ready.wav
- hermes_divine_knowledge.wav, hermes_gossip.wav, hermes_throne_warning.wav
- hermes_puzzle_hint.wav, hermes_bureaucracy.wav

**Zeus** - Powerful but warm, divine authority with humor:
- zeus_amused_intro.wav, zeus_entertainment.wav, zeus_reality_tv.wav
- zeus_items_approved.wav, zeus_curse_reveal.wav, zeus_magnificent_luck.wav
- zeus_fortuna.wav, zeus_official_laugh.wav, zeus_favor_explanation.wav
- zeus_pure_heart.wav, zeus_boring_curse.wav, zeus_poetic.wav
- zeus_blessing.wav, zeus_farewell.wav, zeus_charmed_life.wav
- zeus_throne_friend.wav, zeus_benefits.wav

#### Item Descriptions (assets/sounds/items/)
- brochure_description.wav, olive_description.wav, coin_description.wav
- pomegranate_description.wav, ambrosia_description.wav

#### Action Sounds (assets/sounds/actions/)
- vase_break.wav, box_open.wav, boat_ride.wav
- thunder_laugh.wav (Zeus's amused thunder)

#### Door Sounds (assets/sounds/doors/)
- temple_door.wav, mystical_portal.wav, divine_ascension.wav

## Asset Creation Guidelines

### Visual Consistency:
- **Bold black outlines** on all interactive elements
- **Bright, saturated colors** appropriate for comic book style
- **Clear silhouettes** for easy recognition
- **Consistent lighting** across all room backgrounds
- **Readable text** in any UI elements

### Character Design:
- **Exaggerated facial expressions** for emotional clarity
- **Cultural authenticity** mixed with comedic interpretation
- **Clear visual hierarchy** (Zeus biggest, mortals smaller)
- **Distinctive color schemes** for each character

### Technical Requirements:
- **PNG format with transparency** for sprites
- **1024x768 resolution** for room backgrounds
- **Consistent pixel density** across similar object types
- **Optimized file sizes** for smooth gameplay

### Audio Guidelines:
- **WAV format** for all audio files
- **Consistent volume levels** across all voice acting
- **Clear dialogue recording** with appropriate accents
- **Atmospheric but not overwhelming** background music
- **Comedic timing** in voice delivery to match dialog text

## Comedy Elements to Emphasize in Assets:
- **Anachronistic details** (modern elements in ancient settings)
- **Exaggerated reactions** in character sprites
- **Visual gags** in background details
- **Contrast between ordinary and mythical** elements
- **Luke's consistently surprised expressions** in player sprites

This asset list provides everything needed to create the complete "Lucky Luke's Olympic Blunders" adventure game using the engine framework.