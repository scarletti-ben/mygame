
parent = "G:/new"
assets = parent + "/assets"

defaults = {
    'background': 'slay_clean.png',
    'scroll': "scroll.png",
    'button': "three_stage_button-48x16.png",
    'font': "monogram.ttf",
    'trait': "trait_crossbow.png",
    'entity': "wizard_default.png",
    'player': "wizard_default.png",
    'enemy': "wizard_evil.png",
    'sorcerer': "wizard_evil_200x300.png",
    'worm': "worm_cropped.png",
    'card': "card_cropped.png",
    'cursor': 'cursor.png',
    'traits': "tilesheet_traits_shadowed_edited.png",
    'ninja': "ninja_default.png",

}

intents = {
    'attack1': "attack1.png",
    'attack2': "attack2.png",
    'attack3': "attack3.png",
    'attack4': "attack4.png",
    'attack5': "attack5.png",
    'attack6': "attack6.png",
    'attack7': "attack7.png",
    'defend': "defend.png",
    'defend_buff': "defend_buff.png",

}

defaults = {key: assets + '/defaults/' + value for key, value in defaults.items()}
intents = {key: assets + '/defaults/intents/' + value for key, value in intents.items()}