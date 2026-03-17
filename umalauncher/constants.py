SCENARIO_DICT = {
    1: "URA Finals",
    2: "Aoharu Cup",
    3: "Grand Live",
    4: "Make a New Track",
    5: "Grand Masters",
    6: "Project L'Arc",
    7: "U.A.F. Ready GO!",
    8: "Great Food Festival",
    9: "Run! Mecha Umamusume",
    10: "The Twinkle Legends",
    11: "Design Your Island",
    12: "Yukoma Hot Springs",
    13: "Beyond Dreams"
}

MOTIVATION_DICT = {
    5: "Very High",
    4: "High",
    3: "Normal",
    2: "Low",
    1: "Very Low"
}

SUPPORT_CARD_RARITY_DICT = {
    1: "R",
    2: "SR",
    3: "SSR"
}

SUPPORT_CARD_TYPE_DICT = {
    (101, 1): "speed",
    (105, 1): "stamina",
    (102, 1): "power",
    (103, 1): "guts",
    (106, 1): "wiz",
    (0, 2): "friend",
    (0, 3): "group"
}

SUPPORT_CARD_TYPE_DISPLAY_DICT = {
    "speed": "Speed",
    "stamina": "Stamina",
    "power": "Power",
    "guts": "Guts",
    "wiz": "Wisdom",
    "friend": "Friend",
    "group": "Group"
}

SUPPORT_TYPE_TO_COMMAND_IDS = {
    "speed": [101, 601, 901, 1101, 2101, 2201, 2301, 3601],
    "stamina": [105, 602, 905, 1102, 2102, 2202, 2302, 3602],
    "power": [102, 603, 902, 1103, 2103, 2203, 2303, 3603],
    "guts": [103, 604, 903, 1104, 2104, 2204, 2304, 3604],
    "wiz": [106, 605, 906, 1105, 2105, 2205, 2305, 3605],
    "friend": [],
    "group": []
}

COMMAND_ID_TO_KEY = {
    101: "speed",
    105: "stamina",
    102: "power",
    103: "guts",
    106: "wiz",
    601: "speed",
    602: "stamina",
    603: "power",
    604: "guts",
    605: "wiz",
    901: "speed",
    902: "power",
    903: "guts",
    905: "stamina",
    906: "wiz",
    1101: "speed",
    1102: "stamina",
    1103: "power",
    1104: "guts",
    1105: "wiz",
    2101: "speed",
    2102: "stamina",
    2103: "power",
    2104: "guts",
    2105: "wiz",
    2201: "speed",
    2202: "stamina",
    2203: "power",
    2204: "guts",
    2205: "wiz",
    2301: "speed",
    2302: "stamina",
    2303: "power",
    2304: "guts",
    2305: "wiz",
    "ss_match": "ss_match",
    # DYI
    3101: "ticket",
    3601: "speed",
    3602: "stamina",
    3603: "power",
    3604: "guts",
    3605: "wiz",
    # Onsen
    "pr_activities": "pr_activities"
}

TARGET_TYPE_TO_KEY = {
    1: "speed",
    2: "stamina",
    3: "power",
    4: "guts",
    5: "wiz"
}

MONTH_DICT = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

GL_TOKEN_LIST = [
    'dance',
    'passion',
    'vocal',
    'visual',
    'mental'
]

ORIENTATION_DICT = {
    True: 'game_position_portrait',
    False: 'game_position_landscape',
    'game_position_portrait': True,
    'game_position_landscape': False,
}

# Request packets contain keys that should not be kept for privacy reasons.
REQUEST_KEYS_TO_BE_REMOVED = [
    "device",
    "device_id",
    "device_name",
    "graphics_device_name",
    "ip_address",
    "platform_os_version",
    "carrier",
    "keychain",
    "locale",
    "button_info",
    "dmm_viewer_id",
    "dmm_onetime_token",
]

HEROES_SCORE_TO_LEAGUE_DICT = {
    0: "Bronze 1",
    1000: "Bronze 2",
    2000: "Bronze 3",
    3000: "Bronze 4",
    4000: "Silver 1",
    5500: "Silver 2",
    7000: "Silver 3",
    8500: "Silver 4",
    10000: "Gold 1",
    12500: "Gold 2",
    15000: "Gold 3",
    17500: "Gold 4",
    20000: "Platinum 1",
    23000: "Platinum 2",
    26000: "Platinum 3",
    30000: "Platinum 4"
}

SCOUTING_RANK_LIST = [
    "No rank",
    "E",
    "E1",
    "E2",
    "E3",
    "D",
    "D1",
    "D2",
    "D3",
    "C",
    "C1",
    "C2",
    "C3",
    "B",
    "B1",
    "B2",
    "B3",
    "A",
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "S",
    "S1",
    "S2",
    "S3",
    "S4",
    "S5",
    "SS"
]

BOND_COLOR_DICT = {
    0: "#2AC0FF",
    60: "#A2E61E",
    80: "#FFAD1E",
    100: "#FFEB78"
}

UAF_COLOR_DICT = {
    "1": "rgba(0, 0, 255, 0.1)",
    "2": "rgba(255, 0, 0, 0.1)",
    "3": "rgba(255, 255, 0, 0.1)",
}

DEFAULT_TRAINING_SECTIONS = (
    (1, "cyan", "Pre-Debut"),
    (13, "lightgreen", "Junior"),
    (25, "salmon", "Classic"),
    (37, "yellow", "Classic Summer"),
    (41, "salmon", "Classic"),
    (49, "plum", "Senior"),
    (61, "yellow", "Senior Summer"),
    (65, "plum", "Senior"),
    (73, "gold", "URA Finals"),
    (79, "black", "END")
)


DEFAULT_DREAMS_SECTIONS = (
    (1, "cyan", "Pre-Debut"),
    (13, "lightgreen", "Junior"),
    (25, "salmon", "Classic"),
    (37, "yellow", "Classic Summer"),
    (41, "salmon", "Classic"),
    (49, "plum", "Senior"),
    (61, "yellow", "Senior Summer"),
    (65, "plum", "Senior"),
    (69, "black", "END")
)

DEFAULT_ARC_SECTIONS = (
    (1, "cyan", "Pre-Debut"),
    (13, "lightgreen", "Junior"),
    (25, "salmon", "Classic"),
    (37, "yellow", "Overseas Expedition"),
    (44, "salmon", "Classic"),
    (49, "plum", "Senior"),
    (61, "yellow", "Overseas Expedition"),
    (68, "black", "END")
)

GT_LANGUAGE_URL_DICT = {
    "English": "",
    "Japanese": "ja/",
}

GFF_VEG_ID_TO_IMG_ID = {
    100: "00",
    200: "01",
    300: "02",
    400: "03",
    500: "04"
}

RMU_KEY_TO_ORDER = {
    101: 1,
    105: 2,
    102: 3,
    103: 4,
    106: 5,
}

DYI_KEY_TO_ORDER = {
    101: 1,
    105: 2,
    102: 3,
    103: 4,
    106: 5,
}

ONSEN_KEY_TO_ORDER = {
    101: 1,
    105: 2,
    102: 3,
    103: 4,
    106: 5,
}

# Names used in UmaTL
MANT_ITEM_ID_TO_NAME = {
    1001: "Notepad of Speed",
    1002: "Notepad of Stamina",
    1003: "Notepad of Power",
    1004: "Notepad of Guts",
    1005: "Notepad of Wit",
    1101: "Writings of Speed",
    1102: "Writings of Stamina",
    1103: "Writings of Power",
    1104: "Writings of Guts",
    1105: "Writings of Wit",
    1201: "Scroll of Speed",
    1202: "Scroll of Stamina",
    1203: "Scroll of Power",
    1204: "Scroll of Guts",
    1205: "Scroll of Wit",
    2001: "Vital 20",
    2002: "Vital 40",
    2003: "Vital 65",
    2101: "Royal BitterJuice",
    2201: "MAX Energy Drink",
    2202: "MAX Energy Drink Long",
    2301: "Plain Cupcake",
    2302: "Sweet Cupcake",
    3001: "Delicious Catfood",
    3101: "Carrot BBQ Set",
    4001: "Pretty Mirror",
    4002: "Reporter's Binocs (famous item)",
    4003: "Tricks to Efficient Training",
    4004: "Erudite Hat",
    4101: "Peaceful Zzz's Pillow",
    4102: "Pocket Scheduler",
    4103: "Moist Hand Cream",
    4104: "Biometric Scales",
    4105: "Aroma Diffuser",
    4106: "Training Helper DVD",
    4201: "HealALL",
    5001: "Speed Training Petition",
    5002: "Stamina Training Petition",
    5003: "Power Training Petition",
    5004: "Guts Training Petition",
    5005: "Wit Training Petition",
    7001: "Reset Whistle",
    8001: "Cheering Megaphone",
    8002: "Spartan Megaphone",
    8003: "Bootcamp Megaphone",
    9001: "Speed Ankle Weight",
    9002: "Stamina Ankle Weight",
    9003: "Power Ankle Weight",
    9004: "Guts Ankle Weight",
    10001: "Good Health Amulet",
    11001: "Horseshoe Hammer (Fine)",
    11002: "Horseshoe Hammer (Superior)",
    11003: "Three-Color Penlight"
}

# Names used in global
MANT_ITEM_ID_TO_NAME_GLB = {
    1001: "Speed Notepad",
    1002: "Stamina Notepad",
    1003: "Power Notepad",
    1004: "Guts Notepad",
    1005: "Wit Notepad",
    1101: "Speed Manual",
    1102: "Stamina Manual",
    1103: "Power Manual",
    1104: "Guts Manual",
    1105: "Wit Manual",
    1201: "Speed Scroll",
    1202: "Stamina Scroll",
    1203: "Power Scroll",
    1204: "Guts Scroll",
    1205: "Wit Scroll",
    2001: "Vita 20",
    2002: "Vita 40",
    2003: "Vita 65",
    2101: "Royal Kale Juice",
    2201: "Energy Drink MAX",
    2202: "Energy Drink MAX EX",
    2301: "Plain Cupcake",
    2302: "Berry Sweet Cupcake",
    3001: "Yummy Cat Food",
    3101: "Grilled Carrots",
    4001: "Pretty Mirror",
    4002: "Reporter's Binoculars",
    4003: "Master Practice Guide",
    4004: "Scholar's Hat",
    4101: "Fluffy Pillow",
    4102: "Pocket Planner",
    4103: "Rich Hand Cream",
    4104: "Smart Scale",
    4105: "Aroma Diffuser",
    4106: "Practice Drills DVD",
    4201: "Miracle Cure",
    5001: "Speed Training Application",
    5002: "Stamina Training Application",
    5003: "Power Training Application",
    5004: "Guts Training Application",
    5005: "Wit Training Application",
    7001: "Reset Whistle",
    8001: "Coaching Megaphone",
    8002: "Motivating Megaphone",
    8003: "Empowering Megaphone",
    9001: "Speed Ankle Weights",
    9002: "Stamina Ankle Weights",
    9003: "Power Ankle Weights",
    9004: "Guts Ankle Weights",
    10001:"Good-Luck Charm",
    11001:"Artisan Cleat Hammer",
    11002:"Master Cleat Hammer",
    11003:"Glow Sticks"
}


MANT_ITEM_ID_TO_DESCRIPTION = {
    1001: "Increase speed by 3 \n※Only half effect over 1200",
    1002: "Increase stamina by 3 \n※Only half effect over 1200",
    1003: "Increase power by 3 \n※Only half effect over 1200",
    1004: "Increase guts by 3 \n※Only half effect over 1200",
    1005: "Increase wit by 3 \n※Only half effect over 1200",
    1101: "Increase speed by 7 \n※Only half effect over 1200",
    1102: "Increase stamina by 7 \n※Only half effect over 1200",
    1103: "Increase power by 7 \n※Only half effect over 1200",
    1104: "Increase guts by 7 \n※Only half effect over 1200",
    1105: "Increase wit by 7 \n※Only half effect over 1200",
    1201: "Increase stamina by 15 \n※Only half effect over 1200",
    1202: "Increase stamina by 15 \n※Only half effect over 1200",
    1203: "Increase power by 15 \n※Only half effect over 1200",
    1204: "Increase guts by 15 \n※Only half effect over 1200",
    1205: "Increase wit by 15 \n※Only half effect over 1200",
    2001: "Energy +20",
    2002: "Energy +40",
    2003: "Energy +65",
    2101: "Energy +100, Mood -1",
    2201: "Maximum energy +4, Energy +5",
    2202: "Maximum energy +8",
    2301: "Mood +1",
    2302: "Mood +2",
    3001: "Director Akikawa's Friendship Gauge +5",
    3101: "All support card's Friendship Gauge +5",
    4001: "Get \"Charming\" status effect",
    4002: "Get \"Hot Topic\" status effect",
    4003: "Get \"Practice Perfect\" status effect",
    4004: "Get \"Fast Learner\" status effect",
    4101: "Heal Night Owl",
    4102: "Heal Slacker",
    4103: "Heal Dry Skin",
    4104: "Heal Slow Metabolism",
    4105: "Heal Migraine",
    4106: "Heal Practice Poor",
    4201: "Heal all negative status effects",
    5001: "Speed Training Level +1",
    5002: "Stamina Training Level +1",
    5003: "Power Training Level +1",
    5004: "Guts Training Level +1",
    5005: "Wit Training Level +1",
    7001: "Shuffle support cards in training facilities",
    8001: "All stats gained from training +20% for 4 turns (doesn't stack)",
    8002: "All stats gained from training +40% for 3 turns (doesn't stack)",
    8003: "All stats gained from training +60% for 2 turns (doesn't stack)",
    9001: "Speed training: 20% increased energy consumption, but 50% extra stats (doesn't stack)",
    9002: "Stamina training: 20% increased energy consumption, but 50% extra stats (doesn't stack)",
    9003: "Power training: 20% increased energy consumption, but 50% extra stats (doesn't stack)",
    9004: "Guts training: 20% increased energy consumption, but 50% extra stats (doesn't stack)",
    10001: "Training failure rate set to 0% on used turn",
    11001: "20% race bonus on used turn (doesn't stack)",
    11002: "35% race bonus on used turn (doesn't stack)",
    11003: "Race fan gain +50% on used turn (doesn't stack)"
}

MANT_ITEM_ID_TO_MODIFIER = {
    2001: "+20",
    2002: "+40",
    8001: "+20%",
    8002: "+40%",
    8003: "+60%",
    11001: "+20%",
    11002: "+35%",
}