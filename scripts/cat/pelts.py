import random
from random import choice
from re import sub

from scripts.cat.sprites import sprites
from scripts.game_structure.game_essentials import game


class Pelt:
    sprites_names = {
        'Arctic': 'arctic',
        'Colorpoint': 'colorpoint',
        'Graywolf': 'graywolf',
        'Mexican': 'mexican',
        'Ophelia': 'ophelia',
        'Runic': 'runic',
        'Semisolid': 'semisolid',
        'Smokey': 'smokey',
        'Stormy': 'stormy',
        'Timber': 'timber',
        'Vibrant': 'vibrant',
        'Winter': 'winter',
        'Brindle': 'brindle',
        'Husky': 'husky',
        'Points': 'points',
        'Sable': 'sable',
        'Shepherd': 'shepherd',
        'Solid': 'solid',
        'Tortie': None,
        'Calico': None,
    }

    # ATTRIBUTES, including non-pelt related
    pelt_colours = [
        'SPICE', 'GINGER', 'HONEY', 'FLAXEN', 'CREAM', 'PEARL', 'MIST', 'ASH', 'STEEL',
		'BLACK', 'CHOCOLATE', 'BLUE', 'LILAC', 'GOLD', 'COPPER', 'BRASS', 'SILVER',
		'ONYX', 'SUNSTONE', 'MOONSTONE', 'COCOA', 'SPRUCE', 'ISABELLA',
                        'SUNNY', 'LUNA', "SNOWY", "FROST", "GOSLING", "HAZELNUT", "THISTLE",
                        "DAISY", "VOID", "REDWOOD", "PYRITE", "PEACHY"
    ]
    #torties
    tortiepatterns = ['CAPE', 'DIPPED', 'HEARTBREAKER', 'INKSPILL', 'MINIMAL', 'PHANTOM',
		'PUDDLES', 'REDTAIL', 'SHADOWSTEP', 'SPLIT', 'SPLOTCH', 'WATERFALL']
    tortiebases = ["Graywolf", "Ophelia", "Runic", "Timber", "Sable", "Shepherd", 
		"Arctic", "Winter", "Husky", "Mexican", "Stormy", "Vibrant", "Colorpoint", "Smokey", 
		"Points", "Semisolid", "Solid", "Agouti", "Aspen", "Cali", "Grizzle", "Foxy", "Svalbard"]
    # I want to get rid of this eventually
    pelt_length = ["short", "medium", "long"]
    # eyes
    eye_colours = ['DAYLIGHT', 'ICE', 'NAVY', 'RAIN', 'SAPPHIRE', 'SEAFOAM', 'SKY', 'STORM', 'TEAL', 
				'ALMOND', 'BEAR', 'CASHEW', 'HAZEL', 'LATTE', 'SPARROW', 'BLACK', 'GULL', 
				'SILVER', 'SMOKE', 'WHITE', 'EMERALD', 'FERN', 'FOREST', 'LEAF', 'LIME', 
				'MINT', 'HARVEST', 'PEACH', 'PUMPKIN', 'TANGELO', 'TWILIGHT', 'AMETHYST',
                                                'DAWN', 'DUSK', 'LILAC', 'MIDNIGHT', 'VIOLET', 'BUBBLEGUM', 'PINK', 'ROUGE',
                                                'RUBY', 'SCARLET', 'AMBER', 'LEMON', 'PALE', 'SUNBEAM', 'SUNLIGHT', 'WHEAT']
    yellow_eyes = ['AMBER', 'LEMON', 'PALE', 'SUNBEAM', 'SUNLIGHT', 'WHEAT']
    orange_eyes = ['HARVEST', 'PEACH', 'PUMPKIN', 'TANGELO', 'TWILIGHT']
    green_eyes = ['EMERALD', 'FERN', 'FOREST', 'LEAF', 'LIME', 'MINT']
    gray_eyes = ['BLACK', 'GULL', 'SILVER', 'SMOKE', 'WHITE']
    brown_eyes = ['ALMOND', 'BEAR', 'CASHEW', 'HAZEL', 'LATTE', 'SPARROW']
    blue_eyes = ['DAYLIGHT', 'ICE', 'NAVY', 'RAIN', 'SAPPHIRE', 'SEAFOAM', 'SKY', 'STORM', 'TEAL']
    purple_eyes = ['AMETHYST', 'DAWN', 'DUSK', 'LILAC', 'MIDNIGHT', 'VIOLET']
    red_eyes = ['BUBBLEGUM', 'PINK', 'ROUGE', 'RUBY', 'SCARLET']
    # scars1 is scars from other cats, other animals - scars2 is missing parts - scars3 is "special" scars that could only happen in a special event
    # bite scars by @wood pank on discord
    # none of this makes sense just put missing scars in 2 and scars you don't want randomly generating in 3
    scars1 = ["ONE", "TWO", "THREE", "TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY",
            "LEGBITE", "NECKBITE", "FACE", "MANLEG", "BRIGHTHEART", "MANTAIL", "BRIDGE", "RIGHTBLIND", "LEFTBLIND",
            "BOTHBLIND", "BEAKCHEEK", "BEAKLOWER", "CATBITE", "RATBITE", "QUILLCHUNK", "QUILLSCRATCH", "HINDLEG", 
            "BACK", "QUILLSIDE", "SCRATCHSIDE", "BEAKSIDE", "CATBITETWO", "FOUR", "GIN"]
    scars2 = ["BRIGHTHEART", "BURNBELLY", "BURNTAIL", "LEFTEAR", "RIGHTEAR", "NOTAIL", "HALFTAIL", "NOPAW", "NOLEFTEAR", "NORIGHTEAR", "NOEAR"]
    scars3 = ["SNAKE", "TOETRAP", "BURNPAWS", "BURNTAIL", "BURNBELLY", "BURNRUMP", "FROSTFACE", "FROSTTAIL", "FROSTMITT",
            "FROSTSOCK", "TOE", "SNAKETWO", "BLIND"]
    scars4 = []
    # accessories, the bane of my existance
    # make sure to add plural and singular forms of new accs to acc_display.json so that they will display nicely
    plant_accessories = ["MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS",
            "RYE STALK", "CATTAIL", "POPPY", "ORANGE POPPY", "CYAN POPPY",
            "WHITE POPPY", "PINK POPPY", "BLUEBELLS", "LILY OF THE VALLEY",
            "SNAPDRAGON", "HERBS", "PETALS", "NETTLE", "HEATHER", "GORSE", "JUNIPER",
            "RASPBERRY", "LAVENDER", "OAK LEAVES", "CATMINT", "MAPLE SEED", "LAUREL",
            "BULB WHITE", "BULB YELLOW", "BULB ORANGE", "BULB PINK", "BULB BLUE",
            "CLOVER", "DAISY", "DRY HERBS", "DRY CATMINT", "DRY NETTLES", "DRY LAURELS"
            "BLACK EYED SUSANS", "GOLD HERBS", "IVY", "MARIGOLD", "PURPLE PETALS",
            "ROSE", "SAKURA", "SUNFLOWER", "WHITE ROSE"]
    wild_accessories = ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "GULL FEATHERS",
            "SPARROW FEATHERS", "MOTH WINGS", "ROSY MOTH WINGS",
            "MORPHO BUTTERFLY", "MONARCH BUTTERFLY", "CICADA WINGS",
            "BLACK CICADA", "CROW FEATHERS", "DOVE FEATHERS"]
    manmade_accessories = ['TOWEL', 'SILK CLOAK']
    special_accessories = ["HIBISCUS", "RED HIBISCUS", "WHITE HIBISCUS", "BIG LEAVES", "STARFISH", "PINK STARFISH",
                           "PURPLE STARFISH", "PEARLS", "SEASHELLS", "TOWEL", "SILK CLOAK"]
    collars = [
        "CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME", "GREEN", "RAINBOW",
        "BLACK", "SPIKES", "WHITE", "PINK", "PURPLE", "MULTI", "INDIGO", "BELLBLACK", "BELLBLUE", 
		"BELLCRIMSON", "BELLCYAN", "BELLGREEN", "BELLINDIGO", "BELLLIME", "BELLMULTI", "BELLPINK", 
		"BELLPURPLE", "BELLRAINBOW", "BELLRED", "BELLSPIKES", "BELLWHITE", "BELLYELLOW", 
		"BOWBLACK", "BOWBLUE", "BOWCRIMSON", "BOWCYAN", "BOWGREEN", "BOWINDIGO", "BOWLIME", 
		"BOWMULTI", "BOWPINK", "BOWPURPLE", "BOWRAINBOW", "BOWRED", "BOWSPIKES", "BOWWHITE", "BOWYELLOW", 
		"NYLONBLACK", "NYLONBLUE", "NYLONCRIMSON", "NYLONCYAN", "NYLONGREEN", "NYLONINDIGO", "NYLONLIME", 
		"NYLONMULTI", "NYLONPINK", "NYLONPURPLE", "NYLONRAINBOW", "NYLONRED", "NYLONSPIKES", "NYLONWHITE", 
		"NYLONYELLOW",
		"PASTELNYLONBLACK", "PASTELNYLONBLUE", "PASTELNYLONCRIMSON", "PASTELNYLONCYAN", "PASTELNYLONGREEN", 
		"PASTELNYLONINDIGO", "PASTELNYLONLIME", "PASTELNYLONMULTI", "PASTELNYLONPINK", "PASTELNYLONPURPLE", 
		"PASTELNYLONRAINBOW", "PASTELNYLONRED", "PASTELNYLONSPIKES", "PASTELNYLONWHITE", "PASTELNYLONYELLOW"
    ]
    radiocollars = [
		"RADIOBLACK", "RADIOBLUE", "RADIOCRIMSON", "RADIOCYAN", "RADIOGREEN", 
		"RADIOINDIGO", "RADIOLIME", "RADIOMULTI", "RADIOPINK", "RADIOPURPLE", 
		"RADIORAINBOW", "RADIORED", "RADIOSPIKES", "RADIOWHITE", "RADIOYELLOW"
	]
    harnesses = [
		"HARNESSBLACK", "HARNESSBLUE", "HARNESSCRIMSON", "HARNESSCYAN", "HARNESSGREEN", 
		"HARNESSINDIGO", "HARNESSLIME", "HARNESSMULTI", "HARNESSPINK", "HARNESSPURPLE", 
		"HARNESSRAINBOW", "HARNESSRED", "HARNESSSPIKES", "HARNESSWHITE", "HARNESSYELLOW"
	]
    bandanas = [
		"BANDANABLACK", "BANDANABLUE", "BANDANACRIMSON", "BANDANACYAN", "BANDANAGREEN", 
		"BANDANAINDIGO", "BANDANALIME", "BANDANAMULTI", "BANDANAPINK", "BANDANAPURPLE", 
		"BANDANARAINBOW", "BANDANARED", "BANDANASPIKES", "BANDANAWHITE", "BANDANAYELLOW", 
		"PLAIDBANDANABLACK", "PLAIDBANDANABLUE", "PLAIDBANDANACRIMSON", "PLAIDBANDANACYAN", "PLAIDBANDANAGREEN", 
		"PLAIDBANDANAINDIGO", "PLAIDBANDANALIME", "PLAIDBANDANAMULTI", "PLAIDBANDANAPINK", "PLAIDBANDANAPURPLE", 
		"PLAIDBANDANARAINBOW", "PLAIDBANDANARED", "PLAIDBANDANASPIKES", "PLAIDBANDANAWHITE", "PLAIDBANDANAYELLOW"
	]
    every_acc_list = [plant_accessories, wild_accessories, collars, radiocollars, harnesses, bandanas]
    # pelts
    standardpelts = ["Graywolf", "Ophelia", "Runic", "Timber", "Sable", "Shepherd", "Aspen"]
    northpelts = ["Arctic", "Winter", "Husky", "Svalbard"]
    southpelts = ["Mexican", "Stormy", "Vibrant", "Cali", "Foxy"]
    darkpelts = ["Colorpoint", "Smokey", "Points", "Agouti", "Grizzle"]
    specialpelts = ["Semisolid", "Solid", "Brindle"]
    torties = ["Tortie", "Calico"]
    pelt_categories = [standardpelts, northpelts, southpelts, darkpelts, specialpelts, torties]

    # colors and stuff
    yellow_colors = ['HONEY', 'FLAXEN', 'CREAM', 'PEARL', 'GOLD', 'BRASS', 'SUNSTONE', 'SUNNY', "DAISY", "PEACHY"]
    gray_colors = ['MIST', 'ASH', 'STEEL', 'SILVER', 'MOONSTONE', "SNOW", "GOSLING", "PYRITE"]
    black_colors = ['BLACK', 'ONYX', 'LUNA', "THISTLE", "VOID"]
    red_colors = ['SPICE', 'GINGER', 'COPPER', "REDWOOD"]
    dilute_colors = ['CHOCOLATE', 'COCOA', "HAZELNUT", 'BLUE', 'SPRUCE', "FROST", 'LILAC', 'ISABELLA']
    color_categories = [yellow_colors, gray_colors, black_colors, red_colors, dilute_colors]
    # merles
    merles = ['BRIGHTLEAF', 'SILVERCLAW', 'SEAFUR', 'DAPPLEPELT', 'WILLOWLEAF', 'DAYSKY', 'BRINDLECLOUD', 'SHADOWSNEAK', 'DARKDAPPLE', 'STORMSONG']
    red_merle_colors = {
        'HONEY': (181, 133, 77),
        'FLAXEN': (180, 145, 111),
        'CREAM': (211, 186, 143),
        'PEARL': (229, 213, 183), 
        'GOLD': (206, 148, 62),
        'BRASS': (195, 169, 127),
        'SUNSTONE': (216, 186, 155),
        'SUNNY': (242, 229, 191),
        "DAISY": "#FCF7E2",
        "PEACHY": "#F6AF58",
        'MIST': (199, 196, 187),
        'ASH': (114, 112, 106),
        'STEEL': (69, 66, 59),
        'SILVER': (204, 205, 208),
        'MOONSTONE': (217, 222, 220),
        "SNOW": "#F3F3F3",
        "GOSLING": "#746B5C",
        "PYRITE": "#BBB29F",
        'BLACK': None,
        'ONYX': None,
        'LUNA': None,
        "THISTLE": None,
        "VOID": None,
        'SPICE': (69, 38, 26),
        'GINGER': (141, 75, 34),
        'COPPER': (157, 83, 27),
        "REDWOOD": "#442416",
        'CHOCOLATE': (209, 174, 129),
        'COCOA': (100, 62, 43),
        "HAZELNUT": "#B87B3D",
        'BLUE': (196, 179, 166),
        'SPRUCE': (108, 93, 84),
        "FROST": "#D1D2D2",
        'LILAC': (234, 220, 195),
        'ISABELLA': (178, 165, 154)
        }
    # The pair is dark, light. Each is paired together to avoid weird color combos.
    standard_merle_colors = [[(17, 22, 26), (69, 74, 77)], [(64, 62, 65), (131, 130, 136)], [(42, 41, 47), (187, 186, 194)], [(43, 41, 46), (226, 220, 224)]]
    blue_merle_colors = [[(54, 54, 56), (161, 155, 165)], [(81, 85, 93), (207, 212, 221)], [(75, 76, 81), (145, 146, 151)], [(88, 87, 95), (213, 213, 214)]]
    chocolate_merle_colors = [[(104, 63, 57), (186, 172, 167)], [(53, 37, 24), (164, 152, 140)], [(157, 122, 87), (217, 206, 181)], [(101, 78, 64), (207, 180, 153)], [(110, 71, 50), (171, 133, 96)]]
    lilac_merle_colors = [[(127, 123, 128), (198, 188, 178)], [(147, 128, 111), (197, 176, 155)], [(115, 94, 77), (234, 232, 222)], [(171, 152, 146), (215, 209, 213)]]
    # this list is to include the generation of the red merle parts depending on the pelt
    include_red_merle = ["Graywolf", "Ophelia", "Runic", "Timber", "Sable", "Arctic", "Winter", "Husky", "Mexican", "Stormy", "Vibrant", "Colorpoint", "Smokey", "Aspen", "Cali", "Svalbard"]
    # eyeballs
    eye_sprites = ['DAYLIGHT', 'ICE', 'NAVY', 'RAIN', 'SAPPHIRE', 'SEAFOAM', 'SKY', 'STORM', 'TEAL', 
				'ALMOND', 'BEAR', 'CASHEW', 'HAZEL', 'LATTE', 'SPARROW', 'BLACK', 'GULL', 
				'SILVER', 'SMOKE', 'WHITE', 'EMERALD', 'FERN', 'FOREST', 'LEAF', 'LIME', 
				'MINT', 'HARVEST', 'PEACH', 'PUMPKIN', 'TANGELO', 'TWILIGHT', 'AMETHYST',
                                                'DAWN', 'DUSK', 'LILAC', 'MIDNIGHT', 'VIOLET', 'BUBBLEGUM', 'PINK', 'ROUGE',
                                                'RUBY', 'SCARLET', 'AMBER', 'LEMON', 'PALE', 'SUNBEAM', 'SUNLIGHT', 'WHEAT']
    # white patches
    low_white = ['FLASH', 'HIGHLIGHTS', 'JACKAL', 'LOCKET', 'SNOWFLAKE', 'SOCKS', 'SPLIT', 
				'STRIPE', 'TOES', 'TRIM', 'WOLFTICKING', 'BACKLEG', 'BEE',
                                                'DAPPLES', 'POINTED', 'SPECKLES']
    mid_white = ['BLAZE', 'BLOTCH', 'HALF', 'HEART',  'IRISH', 'MOONRISE', 'MUNSTERLANDER', 
				'SPITZ', 'STAR', 'SUMMERFOX', 'TICKING', 'URAJIRO',
                                                 'DIAMOND', 'HOUND', 'KING']
    high_white = ['BLUETICK', 'EXTREMEPIEBALD', 'LIGHTDALMATIAN', 'PIEBALD', 'TAIL', 'WHITE',
                                                  'HEAVYDALMATIAN', 'HEELER']
    white_sprites = [low_white, mid_white, high_white]
    # points
    point_markings = ['SEPIA', 'MINK', 'POINT', 'CLEAR', 'HIMALAYAN', 'BEW', 'ALBINO']
    point_genes = ['C', 'cb', 'cs', 'ch', 'cw', 'c']
    # vitiligo is inactive currently
    vit = ['VITILIGO', 'VITILIGOTWO', 'MOON', 'PHANTOM', 'KARPATI', 'POWDER', 'BLEACHED', 'SMOKEY']
    # skins
    skin_sprites = ['BLACK', 'BLUE', 'BUTTERFLY', 'DUDLEY', 'DUDLEYBLUE', 'DUDLEYLIVER', 'GRAY', 'ISABELLA', 'LIVER', 'MOCHA', 'PINK', 'SNOWNOSE', 'SPECKLED']
    # sillies - you can add anything here!
    fun_scents = ["pine", "lavender", "rosemary", "thyme", "wet dog", "rain", "grass", "roses", "charcoal", "ash", "maple syrup", "dry leaves", "fresh leaves", "lake",
                  "pond", "fish", "wheat", "peach", "apricot", "apples", "blueberry", "raspberry", "strawberry", "blackberry", "frog", "seabreeze", "salt", "moor", "fern",
                  "mint", "marshland", "seagull", "orchid", "pumpkin", "yam", "squash", "cranberry", "peppermint", "chocolate", "daisy", "marigold", "dandelion", "pet food",
                  "eggs", "milk", "olive oil", "sunflower", "honey", "candy", "mud", "jasmine", "lily", "ginger", "takeout", "hyacinth", "banana", "orange", "grapefruit", "lemon",
                  "lime", "pineapple", "papaya", "pomelo", "citrus", "clementine", "jam", "sap", "acorn", "pinecone", "bark", "walnut", "pistachio", "peanut", "licorice", "rice",
                  "catmint", "holly", "juniper", "gardenia", "cat", "moose", "pie", "sakura", "ice cream", "metal", "denim", "peony", "lilac", "phlox", "crabapple", "seafood",
                  "sushi", "oyster", "fox", "lynx", "extra wolfy", "wisteria", "spices", "paprika", "pepper", "basil", "tomato", "fresh dew", "bayberry", "spring", "summer", "autumn",
                  "winter", "turkey", "hemlock", "cilantro", "garlic", "onion", "twoleg", "sage", "tansy", "wormwood", "spruce", "clover", "grasslands", "deep forest", "alpine flowers",
                  "cherry", "kiwi", "fresh bread", "cookies", "peanut butter", "new leaves", "cool air", "warm air", "popcorn", "pizza", "bear", "soap", "beans", "honeydew", "cantalope",
                  "watermelon", "chicken", "rabbit", "granola", "chili", "sulphur", "copper", "acrid", "starch", "brownies", "vanilla", "mango", "tumeric", "smoke", "marshmallow", "sanitizer",
                  "alfredo", "coconut", "gelato", "eggnog", "tangy", "minerals", "sugar", "brown sugar", "gingerbread", "maple"]
    fun_physical = ["tall", "short", "tiny", "large", "huge", "uneven", "thin", "lanky", "burly", "muscular", "slim", "sleek", "softcoat", "plushcoat", "roughcoat", "fox-like",
                    "lynx-like", "cat-like", "dog-like", "dusty", "clean", "oily", "silkycoat", "wirecoat", "curlycoat", "woolycoat", "warm", "cold", "giant", "runt", "flimsy",
                    "strong", "kinked tail", "snaggle tooth", "crooked tooth", "no fangs", "no dewclaws", "many whiskers", "large nose", "short tail", "extra toe",
                    "piercing gaze", "soft gaze", "sharp features", "soft features"]
    fun_random = ["terrified of spiders", "extremely loud", "loves the rain", "loves the snow" , "loves the sun", 
                  "loves the taste of pet food", "loves the taste of berries", "collects seashells", "collects feathers", "collects rocks", "collects gems", "collects flowers",
                  "collects leaves", "has a silly smile", "not scared of bears", "not scared of twolegs", "terrified of mice", "running from the past", "easily amused", 
                  "loves to sleep", "always sleepy", "always anxious", "over confident", "avid jogger", "frequent moonbather", "frequent sunbather", "watches cars", "watches birds",
                  "cloudwatcher", "finds herbs delicious", "collects dog toys", "likes to sing", "howls a lot", "often cries wolf", "loves to swim", "very quiet", "yips a lot", "has raspy barks",
                  "chatterbox", "collects fabric scraps", "takes long walks at night", "often steals", "pot-stirrer", "huge gossip", "very dramatic", "hates authority", "wants to live alone",
                  "takes city walks", "harasses pets", "loves family", "extremely loyal", "takes frequent baths", "seems suspicious", "rolls in leaves", "storm chaser", "storm watcher",
                  "finds beauty in all things", "always watches the sunset", "always watches the sunrise", "slow to wake up", "goes to bed early", "early bird", "night owl", "clumsy",
                  "likes to have many friends", "likes to run", "has a favorite spot", "has a favorite color", "has a favorite snack", "always snacking", "likes to give gifts", "likes to get gifts",
                  "collects shiny metal", "friends with ravens", "friends with crows", "friends with pigeons", "strong moral compass", "morally flexible", "sneezes a lot", "has seasonal allergies",
                  "a little awkward", "very lovable", "likes to decorate", "lost in thought", "asks a lot of questions", "sits on hills", "relaxes on beaches", "howls like birds sing", "likes to make snow dens",
                  "collects snake skins", "has a fast heartbeat", "has a slow heartbeat", "prefers nicknames", "steals twoleg food", "gets up to no good", "always plotting", "wants to overthrow power",
                  "chases petals", "chases leaves", "chases cars", "would live on a boat", "hates summer", "hates winter", "thinks frogs are cool", "watchful eye", "doesn't like working",
                  "loves their job", "likes their reflection", "collects bugs", "stargazer", "often annoying", "predicts the weather", "a bean", "often licks ice", "snow eater", "appreciates art",
                  "often steals honey", "collects pine needles", "very cute", "very pretty", "very charming", "very fast", "loves the moon", "secretly a werewolf", "has cold toes",
                  "often alone", "never alone", "knows tricks", "steals dog treats", "always bored", "speaks slowly", "speaks too quickly", "easily entertained", "loves a good conversation",
                  "has a deep voice", "has a high-pitched voice", "loves to make jokes", "friend to bees", "loves to scent", "tracks the seasons", "makes comfy nests", "believes in luck", 
                  "doesn't understand jokes", "likes to bark", "rips up leaves", "hopeless romantic", "very optimistic", "very pessimistic", "has a lazy eye", "very emotional", "affectionate",
                  "likes having personal space", "likes to wrestle", "jumps off docks", "listens to twoleg music", "supportive friend", "very silly", "very serious", "can't sit still", "energetic",
                  "passionate", "opinionated", "sneezes at the sun", "likes to be alone", "likes large groups", "always comfy", "always a little uncomfortable", "walks silently", "often stomps around",
                  "afraid of the dark", "collects antlers", "often covered in glitter", "map maker", "terrified of geese", "terrified of moose", "hates being bothered", "likes to spend time in silence",
                  "hates silence", "drawn to others", "drawn to flowers", "likes to dig", "excellent nose", "falls a lot", "drawn to fire", "really mean", "really rude", "good vibes", "always positive",
                  "always negative", "a little offputting", "tends to obsess", "hates getting dirty", "hides from rain", "hides from sun", "ignores problems", "thinks out loud", "largely disinterested",
                  "way too invested", "always lucky", "complains a lot", "giver of compliments", "not very empathetic", "bleeding heart", "never angry", "frequently annoyed", "won't swim",
                  "chirps at birds", "has a long tongue", "abrasive", "likes to chew", "collects sticks", "firestarter", "startles easily", "rarely phased", "always in a phase", "tracks the moon"]

    # appearence information
    # when adding to this, make sure it's done twice
    def __init__(self,
                 name:str="Solid",
                 species:str="Wolf",
                 species_mix:list=["W", "W", "C", "C", "D", "D"],
                 length:str="short",
                 colour:str="WHITE",
                 white_patches:str=None,
                 eye_color:str="BLUE",
                 eye_colour2:str=None,
                 tortiebase:str=None,
                 tortiecolour:str=None,
                 pattern:str=None,
                 tortiepattern:str=None,
                 merle:bool=False,
                 harlequin:bool=False,
                 merle_pattern:list=[None, None, None, None],
                 vitiligo:str=None,
                 points:str=None,
                 points_genes:list=["C", "C"],
                 accessory:str=None,
                 paralyzed:bool=False,
                 opacity:int=100,
                 scars:list=None,
                 tint:str="none",
                 skin:str="BLACK",
                 fun_traits:list=["o", "o", "o"],
                 white_patches_tint:str="none",
                 kitten_sprite:int=None,
                 adol_sprite:int=None,
                 adult_sprite:int=None,
                 senior_sprite:int=None,
                 para_adult_sprite:int=None,
                 reverse:bool=False,
                 ) -> None:
        self.name = name
        self.species = species
        self.species_mix = species_mix
        self.colour = colour
        self.white_patches = white_patches
        self.eye_colour = eye_color
        self.eye_colour2 = eye_colour2
        self.tortiebase = tortiebase
        self.pattern = pattern
        self.tortiepattern = tortiepattern
        self.tortiecolour = tortiecolour
        self.merle = merle
        self.harlequin = harlequin
        self.merle_pattern = merle_pattern
        self.vitiligo = vitiligo
        self.length = length
        self.points = points
        self.points_genes = points_genes
        self.accessory = accessory
        self.paralyzed = paralyzed
        self.opacity = opacity
        self.scars = scars if isinstance(scars, list) else []
        self.tint = tint
        self.fun_traits = fun_traits
        self.white_patches_tint = white_patches_tint
        self.cat_sprites = {"kitten": kitten_sprite if kitten_sprite is not None else 0,
                            "adolescent": adol_sprite if adol_sprite is not None else 0,
                            "young adult": adult_sprite if adult_sprite is not None else 0,
                            "adult": adult_sprite if adult_sprite is not None else 0,
                            "senior adult": adult_sprite if adult_sprite is not None else 0,
                            "senior": senior_sprite if senior_sprite is not None else 0,
                            "para_adult": para_adult_sprite if para_adult_sprite is not None else 0,
                            'newborn': 20,
                            'para_young': 17,
                            "sick_adult": 18,
                            "sick_young": 19}

        self.reverse = reverse
        self.skin = skin

    @staticmethod
    def generate_new_pelt(gender: str, parents: tuple = (), age: str = "adult"):
        new_pelt = Pelt()
        pelt_white = new_pelt.init_pattern_color(parents, gender)
        new_pelt.init_white_patches(pelt_white, parents)
        new_pelt.init_sprite()
        new_pelt.init_scars(age)
        new_pelt.init_accessories(age)
        new_pelt.init_eyes(parents)
        new_pelt.init_pattern()
        new_pelt.init_tint()
            
        # setting up some sillies
        new_pelt.fun_traits = ["o", "o", "o"]
        new_pelt.fun_traits[0] = random.choice(Pelt.fun_scents)
        new_pelt.fun_traits[1] = random.choice(Pelt.fun_physical)
        new_pelt.fun_traits[2] = random.choice(Pelt.fun_random)
        
        return new_pelt

    def check_and_convert(self, convert_dict):
        """Checks for old-type properties for the appearance-related properties
        that are stored in Pelt, and converts them. To be run when loading a cat in. """
        
        # I deleted most of these but this section will likely be used for my own purposes later
        # left one thing so it still runs and doesn't get confused
        # please don't add anything here
        
        if self.cat_sprites['senior'] not in [12, 13, 14]:
            if self.cat_sprites['senior'] == 3:
                self.cat_sprites['senior'] = 12
            elif self.cat_sprites['senior'] == 4:
                self.cat_sprites['senior'] = 13
            elif self.cat_sprites['senior'] == 5:
                self.cat_sprites['senior'] = 14
        
    def init_eyes(self, parents):
        eye_groups = [Pelt.yellow_eyes, Pelt.orange_eyes, Pelt.green_eyes, Pelt.gray_eyes, Pelt.brown_eyes, Pelt.blue_eyes, Pelt.purple_eyes, Pelt.red_eyes]
        if self.points == "BEW" or self.points == "ALBINO":
            if self.points == "BEW":
                self.eye_colour = "ICE"
                return
            if self.points == "ALBINO":
                self.eye_colour = random.choice(Pelt.red_eyes)
                return
        if not parents:
            self.eye_colour = random.choice(random.choices(eye_groups, weights=game.config["random_pelt_generation"]["eyes"], k=1)[0])
        else:
            par_eye_colors = []
            color_base_p = ''
            for p in parents:
                par_eye_colors.append(p.pelt.eye_colour)
            if len(par_eye_colors) <= 1:
                if par_eye_colors[0] == None:
                    color_base_p = par_eye_colors[1]
                else:
                    color_base_p = par_eye_colors[0]
            else:
                color_base_p = random.choice(par_eye_colors)
            if color_base_p in Pelt.yellow_eyes:
                self.eye_colour = random.choice(random.choices(eye_groups, weights=game.config["litter_pelt_generation"]["yelloweye_parent"], k=1)[0])
            elif color_base_p in Pelt.orange_eyes:
                self.eye_colour = random.choice(random.choices(eye_groups, weights=game.config["litter_pelt_generation"]["orangeeye_parent"], k=1)[0])
            elif color_base_p in Pelt.green_eyes:
                self.eye_colour = random.choice(random.choices(eye_groups, weights=game.config["litter_pelt_generation"]["greeneye_parent"], k=1)[0])
            elif color_base_p in Pelt.gray_eyes:
                self.eye_colour = random.choice(random.choices(eye_groups, weights=game.config["litter_pelt_generation"]["grayeye_parent"], k=1)[0])
            elif color_base_p in Pelt.brown_eyes:
                self.eye_colour = random.choice(random.choices(eye_groups, weights=game.config["litter_pelt_generation"]["browneye_parent"], k=1)[0])
            elif color_base_p in Pelt.blue_eyes:
                self.eye_colour = random.choice(random.choices(eye_groups, weights=game.config["litter_pelt_generation"]["blueeye_parent"], k=1)[0])
            elif color_base_p in Pelt.purple_eyes:
                self.eye_colour = random.choice(random.choices(eye_groups, weights=game.config["litter_pelt_generation"]["purpleeye_parent"], k=1)[0])
            else:
                #red eyes
                self.eye_colour = random.choice(random.choices(eye_groups, weights=game.config["litter_pelt_generation"]["redeye_parent"], k=1)[0])
            
        
        #White patches must be initalized before eye color. 
        num = game.config["cat_generation"]["base_heterochromia"]
        if self.white_patches in Pelt.high_white:
            num -= 60
        if self.white_patches == 'WHITE':
            num -= 10
        if self.merle:
            num -= 60
        if self.points != None:
            num -= 10
        for p in parents:
            if p.pelt.eye_colour2:
                num -= 10

        if num < 0:
            num = 1

        if not random.randint(0, num):
            if self.eye_colour in Pelt.yellow_eyes:
                eye_choice = choice([Pelt.green_eyes, Pelt.brown_eyes, Pelt.blue_eyes, Pelt.purple_eyes])
                self.eye_colour2 = choice(eye_choice)
            elif self.eye_colour in Pelt.orange_eyes:
                eye_choice = choice([Pelt.green_eyes, Pelt.brown_eyes, Pelt.blue_eyes, Pelt.red_eyes])
                self.eye_colour2 = choice(eye_choice)
            elif self.eye_colour in Pelt.green_eyes:
                eye_choice = choice([Pelt.yellow_eyes, Pelt.orange_eyes, Pelt.gray_eyes, Pelt.brown_eyes, Pelt.blue_eyes, Pelt.purple_eyes])
                self.eye_colour2 = choice(eye_choice)
            elif self.eye_colour in Pelt.gray_eyes:
                eye_choice = choice([Pelt.green_eyes, Pelt.brown_eyes, Pelt.blue_eyes, Pelt.purple_eyes])
                self.eye_colour2 = choice(eye_choice)
            elif self.eye_colour in Pelt.brown_eyes:
                eye_choice = choice([Pelt.yellow_eyes, Pelt.orange_eyes, Pelt.green_eyes, Pelt.gray_eyes, Pelt.blue_eyes, Pelt.purple_eyes, Pelt.red_eyes])
                self.eye_colour2 = choice(eye_choice)
            elif self.eye_colour in Pelt.blue_eyes:
                eye_choice = choice([Pelt.yellow_eyes, Pelt.orange_eyes, Pelt.green_eyes, Pelt.gray_eyes, Pelt.brown_eyes, Pelt.purple_eyes, Pelt.red_eyes])
                self.eye_colour2 = choice(eye_choice)
            elif self.eye_colour in Pelt.purple_eyes:
                eye_choice = choice([Pelt.yellow_eyes, Pelt.orange_eyes, Pelt.green_eyes, Pelt.gray_eyes, Pelt.brown_eyes, Pelt.blue_eyes, Pelt.red_eyes])
                self.eye_colour2 = choice(eye_choice)
            elif self.eye_colour in Pelt.red_eyes:
                eye_choice = choice([Pelt.green_eyes, Pelt.gray_eyes, Pelt.brown_eyes, Pelt.blue_eyes, Pelt.purple_eyes])
                self.eye_colour2 = choice(eye_choice)

    def pattern_color_inheritance(self, parents: tuple = (), gender="female"):
        # setting parent pelt categories
        #We are using a set, since we don't need this to be ordered, and sets deal with removing duplicates.
        colorpoint_genes = Pelt.point_genes # this is here for easy access
        parents_length = set()
        parents_color = set()
        parents_direct_inheritance = []
        parents_pelt = []
        parents_white = []
        parents_species_mix = [[], []]
        parents_merle = []
        parents_harlequin = []
        parents_points_genes = [[], []]
        temp_parent = [["W", "W", "W", "W", "W", "W"], ["C", "C", "C", "C", "C", "C"], ["D", "D", "D", "D", "D", "D"], ["W", "C", "W", "C", "W", "W"], ["W", "W", "W", "W", "W", "W"]]
        x = 0

        if len(parents) == 2:
            x = 0
            for p in parents:
                parents_direct_inheritance.append(p.pelt)
                parents_length.add(p.pelt.length)
                parents_color.add(p.pelt.colour)
                if p.pelt.name == 'Tortie' or p.pelt.name == 'Calico':
                    parents_pelt.append(p.pelt.tortiebase.capitalize())
                else:
                    parents_pelt.append(p.pelt.name)
                parents_white.append(p.pelt.white)
                parents_merle.append(p.pelt.merle)
                parents_harlequin.append(p.pelt.harlequin)
                parents_points_genes[x] = p.pelt.points_genes
                parents_species_mix[x] = p.pelt.species_mix
                x += 1
        else:
            for p in parents:
                parents_direct_inheritance.append(p.pelt)
                parents_length.add(p.pelt.length)
                parents_color.add(p.pelt.colour)
                if p.pelt.name == 'Tortie' or p.pelt.name == 'Calico':
                    parents_pelt.append(p.pelt.tortiebase.capitalize())
                else:
                    parents_pelt.append(p.pelt.name)
                parents_white.append(p.pelt.white)
                parents_merle.append(p.pelt.merle)
                parents_harlequin.append(p.pelt.harlequin)
                parents_points_genes.append(p.pelt.points_genes)
                parents_points_genes[0] = p.pelt.points_genes
                parents_species_mix[0] = p.pelt.species_mix
            if random.randint(0, 100) <= 20:
                parents_merle.append(True)
            else:
                parents_merle.append(False)
            if random.randint(0, 100) <= 8:
                parents_harlequin.append(True)
            else:
                parents_harlequin.append(False)
            parents_points_genes[1] = [None, None]
            parents_points_genes[1][0] = random.choices(colorpoint_genes, weights=[115, 35, 20, 15, 10, 5], k=1)[0]
            parents_points_genes[1][1] = random.choices(colorpoint_genes, weights=[115, 35, 20, 15, 10, 5], k=1)[0]
            parents_species_mix[1] = random.choice(temp_parent)
            parents_points_genes
            
        chosen_species_mix = ["", "", "", "", "", ""]
        chosen_species = "Wolf"
        y = 0
        z = 1
        for i in range(0, 3):
            p1 = [parents_species_mix[0][y], parents_species_mix[0][z]]
            p2 = [parents_species_mix[1][y], parents_species_mix[1][z]]
            chosen_species_mix[y] = random.choice(p1)
            chosen_species_mix[z] = random.choice(p2)
            y += 2
            z += 2
        if "C" not in chosen_species_mix and "D" not in chosen_species_mix:
            chosen_species = "Wolf"
        elif "D" not in chosen_species_mix and "W" not in chosen_species_mix:
            chosen_species = "Coyote"
        else:
            wolf = chosen_species_mix.count("W")
            yote = chosen_species_mix.count("C")
            dog = chosen_species_mix.count("D")
            if wolf == 5 and yote == 1 or wolf == 4 and yote == 2 or wolf == 3 and yote == 3 or yote == 4 and wolf == 2 or yote == 5 and wolf == 1:
                chosen_species = "Coywolf"
            elif wolf == 5 and dog == 1 or wolf == 4 and dog == 2 or wolf == 3 and dog == 3 or dog == 4 and wolf == 2 or dog == 5 and wolf == 1:
                chosen_species = "Wolfdog"
            elif wolf == 5 or wolf == 4 or wolf == 3:
                chosen_species = "Wolf Hybrid"
            elif yote == 5 and dog == 1 or yote == 4 and dog == 2 or yote == 3 and dog == 3 or dog == 4 and wolf == 2 or dog == 5 and wolf == 1:
                chosen_species = "Coydog"
            elif yote == 5 or yote == 4 or yote == 3:
                chosen_species = "Coyote Hybrid"
            else:
                chosen_species = "Hybrid"
        self.species_mix = chosen_species_mix
        self.species = chosen_species

        # There is a 1/10 chance for kits to have the exact same pelt as one of their parents
        if not random.randint(0, game.config["cat_generation"]["direct_inheritance"]):  # 1/10 chance
            selected = choice(parents_direct_inheritance)
            self.name = selected.name
            self.length = selected.length
            self.colour = selected.colour
            self.tortiebase = selected.tortiebase
            self.merle = selected.merle
            self.harlequin = selected.harlequin
            self.points_genes = selected.points_genes
            self.points = selected.points
            self.merle_pattern = selected.merle_pattern
            return selected.white

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT
        # ------------------------------------------------------------------------------------------------------------#

        # Determine pelt.
        weights = [0, 0, 0, 0, 0]  #Weights for each pelt group. It goes:
        #standardpelts, northpelts, southpelts, darkpelts, specialpelts
        for i in parents_pelt:
            if i in Pelt.standardpelts:
                add_weight = game.config["litter_pelt_generation"]["standardpelt_parent"]
            elif i in Pelt.northpelts:
                add_weight = game.config["litter_pelt_generation"]["northpelt_parent"]
            elif i in Pelt.southpelts:
                add_weight = game.config["litter_pelt_generation"]["southpelt_parent"]
            elif i in Pelt.darkpelts:
                add_weight = game.config["litter_pelt_generation"]["darkpelt_parent"]
            elif i in Pelt.specialpelts:
                add_weight = game.config["litter_pelt_generation"]["specialpelt_parent"]
            elif i is None:
                add_weight = game.config["random_pelt_generation"]["pelt_categories"]
                add_weight = add_weight[:-1]
            else:
                add_weight = game.config["random_pelt_generation"]["pelt_categories"]
                add_weight = add_weight[:-1]

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

        # Now, choose the pelt category and pelt. The extra 0 is for the tortie pelts,
        chosen_pelt = ""
        temp_chosen_pelt = random.choices(Pelt.pelt_categories, weights=weights + [0], k = 1)[0]
        if "Graywolf" in temp_chosen_pelt:
            chosen_pelt = random.choices(Pelt.standardpelts, weights=game.config["random_pelt_generation"]["standardpelts"], k = 1)[0]
        elif "Arctic" in temp_chosen_pelt:
            chosen_pelt = random.choices (Pelt.northpelts, weights=game.config["random_pelt_generation"]["northpelts"], k = 1)[0]
        elif "Mexican" in temp_chosen_pelt:
            chosen_pelt = random.choices(Pelt.southpelts, weights=game.config["random_pelt_generation"]["southpelts"], k = 1)[0]
        elif "Colorpoint" in temp_chosen_pelt:
            chosen_pelt = random.choices(Pelt.darkpelts, weights=game.config["random_pelt_generation"]["darkpelts"], k = 1)[0]
        elif "Semisolid" in temp_chosen_pelt:
            chosen_pelt = random.choices(Pelt.specialpelts, weights=game.config["random_pelt_generation"]["specialpelts"], k = 1)[0]
        else:
            print('Hi you borked the inheritance for pelts')

        # Tortie chance
        tortie_chance_f = game.config["cat_generation"]["base_female_tortie"]
        tortie_chance_m = game.config["cat_generation"]["base_male_tortie"]
        if gender == "female":
            torbie = random.getrandbits(tortie_chance_f) == 1
        else:
            torbie = random.getrandbits(tortie_chance_m) == 1

        chosen_tortie_base = None
        if torbie:
            # If it is tortie, the chosen pelt above becomes the base pelt.
            chosen_tortie_base = str(chosen_pelt).lower()
            chosen_pelt = random.choice(Pelt.torties)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT COLOUR
        # ------------------------------------------------------------------------------------------------------------#
        # Weights for each colour group
        # yellow_colors, gray_colors, black_colors, red_colors, dilute_colors
        weights = [0, 0, 0, 0, 0]
        for i in parents_color:
            if i in Pelt.yellow_colors:
                add_weight = game.config["litter_pelt_generation"]["yellowcolor_parent"]
            elif i in Pelt.gray_colors:
                add_weight = game.config["litter_pelt_generation"]["graycolor_parent"]
            elif i in Pelt.black_colors:
                add_weight = game.config["litter_pelt_generation"]["blackcolor_parent"]
            elif i in Pelt.red_colors:
                add_weight = game.config["litter_pelt_generation"]["redcolor_parent"]
            elif i in Pelt.dilute_colors:
                add_weight = game.config["litter_pelt_generation"]["dilutecolor_parent"]
            elif i is None:
                add_weight = game.config["random_pelt_generation"]["color_categories"]
            else:
                add_weight = game.config["random_pelt_generation"]["color_categories"]

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]
        chosen_pelt_color = ""
        color_list = Pelt.color_categories
        temp_chosen_pelt_color = random.choices(color_list, weights=weights, k=1)[0]
        if "HONEY" in temp_chosen_pelt_color:
            chosen_pelt_color = random.choices(color_list[0], weights=game.config["random_pelt_generation"]["yellowcolors"], k=1)[0]
        elif "MIST" in temp_chosen_pelt_color:
            chosen_pelt_color = random.choices(color_list[1], weights=game.config["random_pelt_generation"]["graycolors"], k=1)[0]
        elif "BLACK" in temp_chosen_pelt_color:
            chosen_pelt_color = random.choices(color_list[2], weights=game.config["random_pelt_generation"]["blackcolors"], k=1)[0]
        elif "SPICE" in temp_chosen_pelt_color:
            chosen_pelt_color = random.choices(color_list[3], weights=game.config["random_pelt_generation"]["redcolors"], k=1)[0]
        elif "CHOCOLATE" in temp_chosen_pelt_color:
            chosen_pelt_color = random.choices(color_list[4], weights=game.config["random_pelt_generation"]["dilutecolors"], k=1)[0]
        else:
            print('color inheritance is borked')
        # ------------------------------------------------------------------------------------------------------------#
        #   PELT LENGTH
        # ------------------------------------------------------------------------------------------------------------#

        weights = [0, 0, 0]  # Weights for each length. It goes (short, medium, long)
        for i in parents_length:
            if i == "short":
                add_weight = (50, 10, 2)
            elif i == "medium":
                add_weight = (25, 50, 25)
            elif i == "long":
                add_weight = (2, 10, 50)
            elif i is None:
                add_weight = (10, 10, 10)
            else:
                add_weight = (10, 10, 10)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

        chosen_pelt_length = random.choices(Pelt.pelt_length, weights=weights, k=1)[0]
        
        # ------------------------------------------------------------------------------------------------------------#
        #   MERLE AND HARLEQUIN
        # ------------------------------------------------------------------------------------------------------------#
        merle_bool = False
        harlequin_bool = False
        chosen_merle_pattern = ["", "", "", ""]
        merle_colors = [Pelt.red_merle_colors, Pelt.standard_merle_colors, Pelt.blue_merle_colors,
                        Pelt.chocolate_merle_colors, Pelt.lilac_merle_colors]
                
        #basically if either or both parents are merle the pup will have a 50/50 chance to be that as well
        if parents_merle[0] or parents_merle[1]:
            if random.randint(0, 1) == 0:
                merle_bool = True
            else:
                merle_bool = False
        if parents_harlequin[0] or parents_harlequin[1]:
            if random.randint(0, 1) == 0:
                harlequin_bool = True
            else:
                harlequin_bool = False

        # only calculate merle info if merle
        if merle_bool:
            #decide on a pattern and color combo [0] = pattern, [1] = dark merle patch, [2] = red merle patch,
            #[3] = dilute merle patch
            chosen_merle_pattern[0] = random.choice(Pelt.merles)
            chosen_merle_pattern[2] = merle_colors[0][chosen_pelt_color]

            #change merle outcomes based on dilutes
            if chosen_pelt_color in Pelt.dilute_colors:
                if chosen_pelt_color == "BLUE" or chosen_pelt_color == "SPRUCE":
                    quickchoice = random.choice(merle_colors[2])
                elif chosen_pelt_color == "CHOCOLATE" or chosen_pelt_color == "COCOA":
                    quickchoice = random.choice(merle_colors[3])
                else:
                    quickchoice = random.choice(merle_colors[4])
            else:
                quickchoice = random.choice(merle_colors[1])

            # overwriting to None if the pelt doesn't need a red color. torties are handled in utility.py
            # torties automatically given the value None to help the process later
            if chosen_pelt not in Pelt.include_red_merle:
                chosen_merle_pattern[2] = None

            #set the final merle colors
            chosen_merle_pattern[1] = quickchoice[0]
            chosen_merle_pattern[3] = quickchoice[1]
        
        # ------------------------------------------------------------------------------------------------------------#
        #   COLORPOINT (NEW)
        # ------------------------------------------------------------------------------------------------------------#
        chosen_points_genes = ["", ""]
        points_outcome = ""
        colorpoint_types = Pelt.point_markings
        
        temp_number = random.randint(0, 1)
        chosen_points_genes[0] = parents_points_genes[0][temp_number]
        temp_number = random.randint(0, 1)
        chosen_points_genes[1] = parents_points_genes[1][temp_number]

        if "C" in chosen_points_genes:
            points_outcome = None
        elif "cb" in chosen_points_genes:
            if "cs" in chosen_points_genes or "ch" in chosen_points_genes:
                points_outcome = colorpoint_types[1]
            elif "cw" in chosen_points_genes or "c" in chosen_points_genes:
                points_outcome = colorpoint_types[2]
            else:
                points_outcome = colorpoint_types[0]
        elif "cs" in chosen_points_genes:
            if "ch" in chosen_points_genes:
                points_outcome = colorpoint_types[2]
            elif "cw" in chosen_points_genes or "c" in chosen_points_genes:
                points_outcome = colorpoint_types[3]
            else:
                points_outcome = colorpoint_types[2]
        elif "ch" in chosen_points_genes:
            points_outcome = colorpoint_types[4]
        elif "cw" in chosen_points_genes:
            points_outcome = colorpoint_types[5]
        elif "c" in chosen_points_genes:
            points_outcome = colorpoint_types[6]
        else:
            print('colorpoint messed up')
        
        # ------------------------------------------------------------------------------------------------------------#
        #   PELT WHITE
        # ------------------------------------------------------------------------------------------------------------#
        chance = 0
        if len(parents) == 2:
            for w in parents_white:
                if w:
                    chance += 35
            if "D" in self.species_mix:
                chance += 20
        else:
            for w in parents_white:
                if w:
                    chance += 35
            if "D" in self.species_mix:
                chance += 40

        chosen_white = random.randint(1, 100) <= chance

        # Adjustments to pelt chosen based on if the pelt has white in it or not
        if chosen_pelt == "Calico":
            if not chosen_white:
                chosen_pelt = "Tortie"

        # SET THE PELT
        self.name = chosen_pelt
        self.colour = chosen_pelt_color
        self.length = chosen_pelt_length
        self.tortiebase = chosen_tortie_base   # This will be none if the cat isn't a tortie.
        self.points_genes = chosen_points_genes
        self.points = points_outcome
        self.merle = merle_bool
        self.harlequin = harlequin_bool
        self.merle_pattern = chosen_merle_pattern
        return chosen_white

    def randomize_pattern_color(self, gender):
        # ------------------------------------------------------------------------------------------------------------#
        #   PELT
        # ------------------------------------------------------------------------------------------------------------#

        # Determine pelt.
        chosen_pelt = ""
        temp_chosen_pelt = random.choices(Pelt.pelt_categories, weights=game.config["random_pelt_generation"]["pelt_categories"], k = 1)[0]
        if "Graywolf" in temp_chosen_pelt:
            chosen_pelt = random.choices(Pelt.standardpelts, weights=game.config["random_pelt_generation"]["standardpelts"], k = 1)[0]
        elif "Arctic" in temp_chosen_pelt:
            chosen_pelt = random.choices (Pelt.northpelts, weights=game.config["random_pelt_generation"]["northpelts"], k = 1)[0]
        elif "Mexican" in temp_chosen_pelt:
            chosen_pelt = random.choices(Pelt.southpelts, weights=game.config["random_pelt_generation"]["southpelts"], k = 1)[0]
        elif "Colorpoint" in temp_chosen_pelt:
            chosen_pelt = random.choices(Pelt.darkpelts, weights=game.config["random_pelt_generation"]["darkpelts"], k = 1)[0]
        elif "Semisolid" in temp_chosen_pelt:
            chosen_pelt = random.choices(Pelt.specialpelts, weights=game.config["random_pelt_generation"]["specialpelts"], k = 1)[0]
        else:
            print('Hi you borked the randomized pelts')

        # Tortie chance
        # There is a default chance for female tortie, slightly increased for completely random generation.
        tortie_chance_f = game.config["cat_generation"]["base_female_tortie"]
        tortie_chance_m = game.config["cat_generation"]["base_male_tortie"]
        if gender == "female":
            torbie = random.getrandbits(tortie_chance_f) == 1
        else:
            torbie = random.getrandbits(tortie_chance_m) == 1

        chosen_tortie_base = None
        if torbie:
            # If it is tortie, the chosen pelt above becomes the base pelt.
            chosen_tortie_base = str(chosen_pelt).lower()
            chosen_pelt = random.choice(Pelt.torties)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT COLOUR
        # ------------------------------------------------------------------------------------------------------------#
        chosen_pelt_color = ""
        color_list = Pelt.color_categories
        temp_chosen_pelt_color = random.choices(color_list, weights=game.config["random_pelt_generation"]["color_categories"], k=1)[0]
        if "HONEY" in temp_chosen_pelt_color:
            chosen_pelt_color = random.choices(color_list[0], weights=game.config["random_pelt_generation"]["yellowcolors"], k=1)[0]
        elif "MIST" in temp_chosen_pelt_color:
            chosen_pelt_color = random.choices(color_list[1], weights=game.config["random_pelt_generation"]["graycolors"], k=1)[0]
        elif "BLACK" in temp_chosen_pelt_color:
            chosen_pelt_color = random.choices(color_list[2], weights=game.config["random_pelt_generation"]["blackcolors"], k=1)[0]
        elif "SPICE" in temp_chosen_pelt_color:
            chosen_pelt_color = random.choices(color_list[3], weights=game.config["random_pelt_generation"]["redcolors"], k=1)[0]
        elif "CHOCOLATE" in temp_chosen_pelt_color:
            chosen_pelt_color = random.choices(color_list[4], weights=game.config["random_pelt_generation"]["dilutecolors"], k=1)[0]
        else:
            print('color randomization is borked')

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT LENGTH
        # ------------------------------------------------------------------------------------------------------------#
        chosen_pelt_length = random.choice(Pelt.pelt_length)
        # ------------------------------------------------------------------------------------------------------------#
        #   SPECIES
        # ------------------------------------------------------------------------------------------------------------#
        chosen_species_mix = ["", "", "", "", "", ""]
        chosen_species = ""
        poss_genes = ["W", "C", "D"]
        quick_genes = [["W", "W", "W", "W", "W", "W"], ["C", "C", "C", "C", "C", "C"]]
        x = 0
        species_grabber = random.randint(0, 10)
        if species_grabber <= 2:
            chosen_species_mix = random.choices(quick_genes, weights=(100, 20), k=1)[0]
        else:
            for i in range(0, 6):
                chosen_species_mix[x] = random.choices(poss_genes, weights=(400, 40, 10), k=1)[0]
                x += 1
        if "C" not in chosen_species_mix and "D" not in chosen_species_mix:
            chosen_species = "Wolf"
        elif "D" not in chosen_species_mix and "W" not in chosen_species_mix:
            chosen_species = "Coyote"
        else:
            wolf = chosen_species_mix.count("W")
            yote = chosen_species_mix.count("C")
            dog = chosen_species_mix.count("D")
            if wolf == 5 and yote == 1 or wolf == 4 and yote == 2 or wolf == 3 and yote == 3 or yote == 4 and wolf == 2 or yote == 5 and wolf == 1:
                chosen_species = "Coywolf"
            elif wolf == 5 and dog == 1 or wolf == 4 and dog == 2 or wolf == 3 and dog == 3 or dog == 4 and wolf == 2 or dog == 5 and wolf == 1:
                chosen_species = "Wolfdog"
            elif wolf == 5 or wolf == 4 or wolf == 3:
                chosen_species = "Wolf Hybrid"
            elif yote == 5 and dog == 1 or yote == 4 and dog == 2 or yote == 3 and dog == 3 or dog == 4 and wolf == 2 or dog == 5 and wolf == 1:
                chosen_species = "Coydog"
            elif yote == 5 or yote == 4 or yote == 3:
                chosen_species = "Coyote Hybrid"
            else:
                chosen_species = "Hybrid"
                
        # ------------------------------------------------------------------------------------------------------------#
        #   MERLE AND HARLEQUIN
        # ------------------------------------------------------------------------------------------------------------#
        merle_bool = False
        harlequin_bool = False
        chosen_merle_pattern = ["", "", "", ""]
        merle_colors = [Pelt.red_merle_colors, Pelt.standard_merle_colors, Pelt.blue_merle_colors,
                        Pelt.chocolate_merle_colors, Pelt.lilac_merle_colors]

        #find out if they're merle or harlequin at all
        temp_chance = random.randint(0, 100)
        if temp_chance <= game.config["random_pelt_generation"]["merle"]:
            merle_bool = True
        temp_chance = random.randint(0, 100)
        if temp_chance <= game.config["random_pelt_generation"]["harlequin"]:
            harlequin_bool = True

        # only calculate merle info if merle
        if merle_bool:
            #decide on a pattern and color combo [0] = pattern, [1] = dark merle patch, [2] = red merle patch,
            #[3] = dilute merle patch
            chosen_merle_pattern[0] = random.choice(Pelt.merles)
            chosen_merle_pattern[2] = merle_colors[0][chosen_pelt_color]

            #change merle outcomes based on dilutes
            if chosen_pelt_color in Pelt.dilute_colors:
                if chosen_pelt_color in ["BLUE", "SPRUCE", "FROST"]:
                    quickchoice = random.choice(merle_colors[2])
                elif chosen_pelt_color in ["CHOCOLATE", "COCOA", "HAZELNUT"]:
                    quickchoice = random.choice(merle_colors[3])
                else:
                    quickchoice = random.choice(merle_colors[4])
            else:
                quickchoice = random.choice(merle_colors[1])

            # overwriting to None if the pelt doesn't need a red color. torties are handled in utility.py
            # torties given value of None here
            if chosen_pelt not in Pelt.include_red_merle:
                chosen_merle_pattern[2] = None

            #set the final merle colors
            chosen_merle_pattern[1] = quickchoice[0]
            chosen_merle_pattern[3] = quickchoice[1]

        # ------------------------------------------------------------------------------------------------------------#
        #   COLORPOINT (NEW)
        # ------------------------------------------------------------------------------------------------------------#
        chosen_points_genes = ["C", "C"]
        points_outcome = None
        colorpoint_types = Pelt.point_markings
        colorpoint_genes = Pelt.point_genes

        chosen_points_genes[0] = random.choices(colorpoint_genes, weights=game.config["random_pelt_generation"]["colorpoint_genes"], k=1)[0]
        chosen_points_genes[1] = random.choices(colorpoint_genes, weights=game.config["random_pelt_generation"]["colorpoint_genes"], k=1)[0]

        if "C" in chosen_points_genes:
            points_outcome = None
        elif "cb" in chosen_points_genes:
            if "cs" in chosen_points_genes or "ch" in chosen_points_genes:
                points_outcome = colorpoint_types[1]
            elif "cw" in chosen_points_genes or "c" in chosen_points_genes:
                points_outcome = colorpoint_types[2]
            else:
                points_outcome = colorpoint_types[0]
        elif "cs" in chosen_points_genes:
            if "ch" in chosen_points_genes:
                points_outcome = colorpoint_types[2]
            elif "cw" in chosen_points_genes or "c" in chosen_points_genes:
                points_outcome = colorpoint_types[3]
            else:
                points_outcome = colorpoint_types[2]
        elif "ch" in chosen_points_genes:
            points_outcome = colorpoint_types[4]
        elif "cw" in chosen_points_genes:
            points_outcome = colorpoint_types[5]
        elif "c" in chosen_points_genes:
            points_outcome = colorpoint_types[6]
        else:
            print('colorpoint messed up')

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT WHITE
        # ------------------------------------------------------------------------------------------------------------#

        if "D" in chosen_species_mix:
            chosen_white = random.randint(1, 100) <= 55
        else:
            chosen_white = random.randint(1, 100) <= 35

        # Adjustments to pelt chosen based on if the pelt has white in it or not.
        if chosen_pelt == "Calico":
            if not chosen_white:
                chosen_pelt = "Tortie"

        self.name = chosen_pelt
        self.colour = chosen_pelt_color
        self.length = chosen_pelt_length
        self.tortiebase = chosen_tortie_base   # This will be none if the cat isn't a tortie.
        self.species_mix = chosen_species_mix
        self.species = chosen_species
        self.points_genes = chosen_points_genes
        self.points = points_outcome
        self.merle = merle_bool
        self.harlequin = harlequin_bool
        self.merle_pattern = chosen_merle_pattern
        return chosen_white

    def init_pattern_color(self, parents, gender) -> bool:
        """Inits self.name, self.colour, self.length, 
            self.tortiebase and determines if the cat 
            will have white patche or not. 
            Return TRUE is the cat should have white patches, 
            false is not. """

        if parents:
            chosen_white = self.pattern_color_inheritance(parents, gender)
        else:
            chosen_white = self.randomize_pattern_color(gender)

        return chosen_white

    def init_sprite(self):
        self.cat_sprites = {
            'newborn': 20,
            'kitten': random.randint(0, 2),
            'adolescent': random.randint(3, 5),
            'senior': random.randint(12, 14),
            'sick_young': 19,
            'sick_adult': 18
        }
        self.reverse = choice([True, False])
        self.cat_sprites['adult'] = random.randint(6, 11)
        self.cat_sprites['para_adult'] = 15
        self.cat_sprites['young adult'] = self.cat_sprites['adult']
        self.cat_sprites['senior adult'] = self.cat_sprites['adult']
        # skin chances
        temp_dilute_list = ['CHOCOLATE', 'COCOA', 'BLUE', 'SPRUCE', 'LILAC', 'ISABELLA']
        skin_sprites = Pelt.skin_sprites.copy()
        low_white = Pelt.low_white.copy()
        mid_white = Pelt.mid_white.copy()
        high_white = Pelt.high_white.copy()
        temp_points = ['HIMALAYAN', 'BEW', 'ALBINO']
        if self.white_patches == None and self.colour not in temp_dilute_list and self.tortiepattern == None and self.points not in temp_points and not self.merle:
            skin_list = [skin_sprites[0], skin_sprites[11]]
            self.skin = random.choices(skin_list, weights=(90, 10), k=1)[0]
        elif self.points in temp_points:
            self.skin = skin_sprites[10]
        elif self.colour in temp_dilute_list:
            if self.colour in ["CHOCOLATE", "COCOA", "HAZELNUT"]:
                if self.white_patches == None and self.tortiepattern == None and not self.merle:
                    skin_list = [skin_sprites[8], skin_sprites[9]]
                    self.skin = random.choices(skin_list, weights=(60, 40), k=1)[0]
                else:
                    skin_list = [skin_sprites[8], skin_sprites[9], skin_sprites[5], skin_sprites[10]]
                    self.skin = random.choices(skin_list, weights=(10, 20, 40, 30), k=1)[0]
            elif self.colour in ["BLUE", "SPRUCE", "FROST"]:
                if self.white_patches == None and self.tortiepattern == None and not self.merle:
                    skin_list = [skin_sprites[1], skin_sprites[6]]
                    self.skin = random.choices(skin_list, weights=(60, 40), k=1)[0]
                else:
                    skin_list = [skin_sprites[1], skin_sprites[6], skin_sprites[4], skin_sprites[10]]
                    self.skin = random.choices(skin_list, weights=(30, 20, 40, 10), k=1)[0]
            else:
                if self.white_patches == None and self.tortiepattern == None and not self.merle:
                    skin_list = [skin_sprites[7], skin_sprites[10]]
                    self.skin = random.choices(skin_list, weights=(80, 20), k=1)[0]
                else:
                    self.skin = skin_sprites[10]
        elif self.white_patches != None:
            if self.tortiepattern != None or self.merle:
                if self.white_patches not in high_white:
                    skin_list = [skin_sprites[0], skin_sprites[2], skin_sprites[3], skin_sprites[11], skin_sprites[12]]
                    self.skin = random.choices(skin_list, weights=(10, 30, 15, 15, 30), k=1)[0]
                else:
                    self.skin = skin_sprites[10]
            elif self.white_patches not in low_white:
                skin_list = [skin_sprites[0], skin_sprites[2], skin_sprites[3], skin_sprites[10], skin_sprites[11], skin_sprites[12]]
                self.skin = random.choices(skin_list, weights=(20, 10, 10, 20, 20, 20), k=1)[0]
            else:
                skin_list = [skin_sprites[0], skin_sprites[3], skin_sprites[11]]
                self.skin = random.choices(skin_list, weights=(60, 20, 20), k=1)[0]
        elif self.tortiepattern != None or self.merle:
            skin_list = [skin_sprites[0], skin_sprites[2], skin_sprites[3], skin_sprites[11]]
            self.skin = random.choice(skin_list)
        else:
            self.skin = choice(Pelt.skin_sprites)


    def init_scars(self, age):
        if age == "newborn":
            return

        if age in ['kitten', 'adolescent']:
            scar_choice = random.randint(0, 50)  # 2%
        elif age in ['young adult', 'adult']:
            scar_choice = random.randint(0, 20)  # 5%
        else:
            scar_choice = random.randint(0, 15)  # 6.67%

        if scar_choice == 1:
            self.scars.append(choice([
                choice(Pelt.scars1),
                choice(Pelt.scars3)
            ]))

        if 'NOTAIL' in self.scars and 'HALFTAIL' in self.scars:
            self.scars.remove('HALFTAIL')

    def init_accessories(self, age):
        if age == "newborn":
            self.accessory = None
            return

        acc_display_choice = random.randint(0, 80)
        if age in ['kitten', 'adolescent']:
            acc_display_choice = random.randint(0, 180)
        elif age in ['young adult', 'adult']:
            acc_display_choice = random.randint(0, 100)
        
        if acc_display_choice in range(1, 30):
            self.accessory = choice([
                choice(Pelt.plant_accessories),
                choice(Pelt.wild_accessories)
            ])
        elif acc_display_choice in range(31, 45):
            self.accessory = choice(Pelt.radiocollars)
        elif acc_display_choice in range(46, 62):
            self.accessory = choice([
                 choice(Pelt.collars),
            	 choice(Pelt.bandanas)
            ])
        elif acc_display_choice in range(63, 71):
            self.accessory = choice(Pelt.harnesses)
        else:
            self.accessory = None

    def init_pattern(self):
        if self.name in Pelt.torties:
            if not self.tortiebase:
                self.tortiebase = choice(Pelt.tortiebases)
            if not self.pattern:
                if random.randint(0, 100) < 10:
                    temp_merle_list = Pelt.merles.copy()
                    if self.merle:
                        print(temp_merle_list)
                        temp_merle_list.remove(str(self.merle_pattern[0]))
                    self.pattern = choice(temp_merle_list)
                else:
                    self.pattern = choice(Pelt.tortiepatterns)

            wildcard_chance = game.config["cat_generation"]["wildcard_tortie"]
            if self.colour:
                # The "not wildcard_chance" allows users to set wildcard_tortie to 0
                # and always get wildcard torties.
                if not wildcard_chance or random.getrandbits(wildcard_chance) == 1:
                    # This is the "wildcard" chance, where you can get funky combinations.
                    # people are fans of the print message, so I'm putting it back
                    print("Wildcard tortie!")

                    # Allow any pattern:
                    self.tortiepattern = choice(Pelt.tortiebases)
                    self.tortiepattern = self.tortiepattern.lower()

                    # Allow any colors that aren't the base color.
                    possible_colors = Pelt.pelt_colours.copy()
                    possible_colors.remove(self.colour)
                    self.tortiecolour = choice(possible_colors)

                else:
                    # Normal generation
                    self.tortiepattern = random.choices([self.tortiebase, 'semisolid', 'solid'], weights=[45, 30, 25], k=1)[0]

                    # Picking out tortie colors
                    if (self.colour in Pelt.black_colors):
                        self.tortiecolour = choice((Pelt.yellow_colors * 2) + Pelt.gray_colors + Pelt.red_colors + Pelt.black_colors)
                    elif self.colour in Pelt.yellow_colors:
                        self.tortiecolour = choice(Pelt.red_colors + (Pelt.black_colors * 2) + Pelt.yellow_colors)
                    elif self.colour in Pelt.gray_colors:
                        self.tortiecolour = choice(Pelt.gray_colors + Pelt.dilute_colors + Pelt.black_colors)
                    elif self.colour in Pelt.red_colors:
                        self.tortiecolour = choice(Pelt.yellow_colors + (Pelt.black_colors * 2))
                    elif self.colour in Pelt.dilute_colors:
                        if self.colour in ["CHOCOLATE", "COCOA", "HAZELNUT"]:
                            choc_temp = ["CHOCOLATE", "COCOA", "HAZELNUT"]
                            self.tortiecolour = choice(choc_temp)
                        if self.colour in ["BLUE", "SPRUCE", "FROST"]:
                            blue_temp = ["BLUE", "SPRUCE", "FROST"]
                            self.tortiecolour = choice(blue_temp)
                        if self.colour == "LILAC" or self.colour == "ISABELLA":
                            lilac_temp = ["LILAC", "ISABELLA"]
                            self.tortiecolour = choice(lilac_temp)
                    
                    else:
                        self.tortiecolour = "HONEY"
            else:
                self.tortiecolour = "HONEY"
        else:
            self.tortiebase = None
            self.tortiepattern = None
            self.tortiecolour = None
            self.pattern = None
        # accounting for a weird thing
        if self.tortiepattern == self.tortiebase and self.colour == self.tortiecolour or self.colour == self.tortiecolour and self.tortiepattern in ["Semisolid", "Solid"] and self.tortiebase in ["Semisolid", "Solid"]:
            temp_tortie = self.tortiepattern.capitalize()
            poss_bases = Pelt.tortiebases.copy()
            poss_bases.remove(temp_tortie)
            self.tortiepattern = random.choice(poss_bases).lower()
            
    def white_patches_inheritance(self, parents: tuple):
        parents_white = []
        white_list = [Pelt.low_white, Pelt.mid_white, Pelt.high_white]

        # collecting parent info (or making it up)
        if len(parents) == 2:
            for p in parents:
                if p:
                    if p.pelt.white_patches:
                        parents_white.append(p.pelt.white_patches)
        else:
            for p in parents:
                if p:
                    if p.pelt.white_patches:
                        parents_white.append(p.pelt.white_patches)
                if random.randint(0, 10) <= 4:
                    parents_white.append(random.choice(random.choices(white_list, weights=[65, 30, 5], k=1)[0]))
            # the alternative is no white patches are added to the list

        # direct inheritance
        if len(parents_white) != 0 and not random.randint(0, game.config["cat_generation"]["direct_inheritance"]):
            if self.name == 'Tortie':
                for i in parents_white:
                    if i in white_list[1] or i in white_list[2]:
                        parents_white.remove(i)
                if len(parents_white) != 0:
                    self.white_patches = random.choice(parents_white)
                else:
                    self.white_patches = random.choice(random.choices(white_list, weights=[1, 0, 0], k=1)[0])
            elif self.name == 'Calico':
                for i in parents_white:
                    if i in white_list[0]:
                        parents_white.remove(i)
                if len(parents_white) != 0:
                    self.white_patches = random.choice(parents_white)
                else:
                    self.white_patches = random.choice(random.choices(white_list, weights=[0, 7, 3], k=1)[0])
            else:
                self.white_patches = random.choice(parents_white)
            return

        # setting weights, starting with checking if there are parent white patches. if not, we'll make up some numbers
        weights = [0, 0, 0]
        if len(parents_white) != 0:
            for i in parents_white:
                if i in white_list[0]: # low white
                    weights[0] += 60
                    weights[1] += 30
                    weights[2] += 10
                elif i in white_list[1]: # mid white
                    weights[0] += 40
                    weights[1] += 50
                    weights[2] += 10
                elif i in white_list[2]: # high white
                    weights[0] += 20
                    weights[1] += 50
                    weights[2] += 30
        else: # if neither parent has white, make up some stuff
            weights = [60, 30, 10]

        if self.name == 'Tortie' or self.name == 'Calico': #adjusting for torties
            if self.name == 'Tortie':
                weights[1] == 0
                weights[2] == 0
            else:
                weights[0] == 0

        chosen_white_patches = random.choices(white_list, weights=weights, k=1)[0]
        chosen_white_patches = random.choice(chosen_white_patches)
        self.white_patches = chosen_white_patches

    def randomize_white_patches(self):
        if self.name == "Tortie":
            weights = (1, 0, 0)
        elif self.name == "Calico":
            weights = (0, 50, 20)
        else:
            weights = (55, 35, 10)

        white_list = [Pelt.low_white, Pelt.mid_white, Pelt.high_white]
        chosen_white_patches = choice(random.choices(white_list, weights=weights, k=1)[0])

        self.white_patches = chosen_white_patches

    def init_white_patches(self, pelt_white, parents:tuple):
        # If the cat was rolled previously to have white patches, then determine the patch they will have
        # these functions also handle points. 
        if pelt_white:
            if parents:
                self.white_patches_inheritance(parents)
            else:
                self.randomize_white_patches()
        else:
            self.white_patches = None

    def init_tint(self):
        # edited this to stop the generation of blue/red combos bc they're ugly

        # PELT TINT
        # Basic tints as possible for all colors.
        if random.randint(0, 1) == 0:
            base_tints = sprites.cat_tints["possible_tints"]["basic"]
            if self.colour in sprites.cat_tints["colour_groups"]:
                color_group = sprites.cat_tints["colour_groups"].get(self.colour, "warm")
                color_tints = sprites.cat_tints["possible_tints"][color_group]
            else:
                color_tints = []
        
            if base_tints or color_tints:
                self.tint = choice(base_tints + color_tints)
            else:
                self.tint = "none"
        else:
            self.tint = "none"

        if self.colour in ["BLACK", "ONYX", "LUNA", "THISTLE", "VOID", "STEEL", "SPICE", "REDWOOD"] and random.randint(0, 6) < 5:
            self.tint = "none"

        # WHITE PATCHES TINT
        if self.white_patches or self.points:
            if random.randint(0, 1) == 0:
                base_tints = sprites.white_patches_tints["possible_tints"]["basic"]
                if self.points == 'BEW' or self.points == 'ALBINO':
                    if self.points == 'BEW':
                        self.white_patches_tint == 'yellowwhite'
                    else:
                        self.white_patches_tint == 'none'
                if self.colour in sprites.cat_tints["colour_groups"]:
                    color_group = sprites.white_patches_tints["colour_groups"].get(self.colour, "white")
                    color_tints = sprites.white_patches_tints["possible_tints"][color_group]
                else:
                    color_tints = []
            
                if base_tints or color_tints:
                    self.white_patches_tint = choice(base_tints + color_tints)
                else:
                    self.white_patches_tint = "none"
            else:
                self.white_patches_tint = "none"
        else:
            self.white_patches_tint = "none"

        # fixing
        if self.white_patches_tint == "darkblue" or self.white_patches_tint == "deepblue":
            if self.tint == "red" or self.tint == "orange" or self.tint == "pink":
                self.white_patches_tint = "none"
        elif self.white_patches_tint == "darkred" or self.white_patches_tint == "deepred":
            if self.tint == "blue" or self.tint == "purple" or self.tint == "gray":
                self.white_patches_tint == "none"
            

    @property
    def white(self):
        return self.white_patches
    
    @white.setter
    def white(self, val):
        print("Can't set pelt.white")
        return

    @staticmethod
    def describe_appearance(cat, short=False):
        
        # first we start deciding how things should look when written out. later other pieces of the code
        # will reference these and decide what it's displaying
        if short:
            renamed_colors = {
                "honey": "honey",
                "flaxen": "flaxen",
                "cream": "cream",
                "pearl": "pearl",
                "gold": "golden",
                "brass": "brass",
                "sunstone": "peach",
                "mist": "gray",
                "ash": "gray",
                "steel": "gray",
                "silver": "gray",
                "moonstone": "gray",
                "black": "black",
                "onyx": "black",
                "spice": "red",
                "ginger": "ginger",
                "copper": "copper",
                "chocolate": "chocolate",
                "blue": "blue",
                "lilac": "lilac",
                "cocoa": "cocoa",
                "spruce": "blue",
                "isabella": "isabella",
                "sunny": "gold",
                "luna": "black",
                "snow": "white",
                "frost": "frost",
                "gosling": "gray",
                "hazelnut": "ochre",
                "thistle": "black",
                "daisy": "white",
                "void": "black",
                "redwood": "red",
                "pyrite": "gray",
                "peachy": "peach"
            }
        else:
            renamed_colors = {
                "honey": "honey",
                "flaxen": "flaxen",
                "cream": "cream",
                "pearl": "cream",
                "gold": "golden",
                "brass": "brass",
                "sunstone": "peachy yellow",
                "mist": "misty gray",
                "ash": "ashen gray",
                "steel": "steel gray",
                "silver": "silver gray",
                "moonstone": "blue-gray",
                "black": "black",
                "onyx": "onyx black",
                "spice": "red",
                "ginger": "ginger",
                "copper": "copper",
                "chocolate": "chocolate",
                "blue": "blue",
                "lilac": "lilac",
                "cocoa": "cocoa",
                "spruce": "dark blue",
                "isabella": "isabella",
                "sunny": "bright gold",
                "luna": "silvery black",
                "snow": "snow white",
                "frost": "frosty blue",
                "gosling": "rich gray",
                "hazelnut": "ochre",
                "thistle": "straw black",
                "daisy": "sunlit white",
                "void": "pitch black",
                "redwood": "deep red",
                "pyrite": "firey gray",
                "peachy": "peach"
            }

        pattern_des = {
            "Graywolf": "agouti",
            "Ophelia": "agouti",
            "Runic": "agouti",
            "Timber": "agouti",
            "Sable": "sable",
            "Shepherd": "saddle",
            "Arctic": "arctic agouti",
            "Winter": "winter agouti",
            "Husky": "domino",
            "Mexican": "flashy agouti",
            "Stormy": "dark agouti",
            "Vibrant": "vibrant agouti",
            "Colorpoint": "colorpoint",
            "Smokey": "smokey agouti",
            "Points": "points",
            "Semisolid": "solid",
            "Solid": "solid",
            'Brindle': 'brindle',
            "Agouti": "shaded agouti",
            "Aspen": "agouti",
            "Cali": "peppered agouti",
            "Grizzle": "grizzle",
            "Foxy": "fox",
            "Svalbard": "patchy saddle"
        }
        eye_des = {
            "AMBER": "amber",
            'LEMON' : "yellow",
            'PALE': "pale yellow",
            'SUNBEAM': "yellow",
            'SUNLIGHT': "amber",
            'WHEAT': "faded yellow",
            'HARVEST': "deep orange",
            'PEACH': "peach",
            'PUMPKIN': "orange",
            'TANGELO': "orange",
            'TWILIGHT': "twilight orange",
            'EMERALD': "emerald green",
            'FERN': "fern green",
            'FOREST': "light green",
            'LEAF': "green",
            'LIME': "lime green",
            'MINT': "mint green",
            'BLACK': "black",
            'GULL': "gray",
            'SILVER': "silver",
            'SMOKE': "gray",
            'WHITE': "white",
            'ALMOND': "brown",
            'BEAR': "brown",
            'CASHEW': "pale brown",
            'HAZEL': "hazel",
            'LATTE': "light brown",
            'SPARROW': "dark brown",
            'DAYLIGHT': "daylight blue",
            'ICE': "ice blue",
            'NAVY': "navy blue",
            'RAIN': "blue",
            'SAPPHIRE': "sapphire blue",
            'SEAFOAM': "seafoam",
            'SKY': "bright blue",
            'STORM': "blue-gray",
            'TEAL': "teal",
            'AMETHYST': "amethyst purple",
            'DAWN': "dawn purple",
            'DUSK': "dusk purple",
            'LILAC': "lilac",
            'MIDNIGHT': "midnight purple",
            'VIOLET': "violet",
            'BUBBLEGUM': "pink",
            'PINK': "pink",
            'ROUGE': "pale red",
            'RUBY': "ruby red",
            'SCARLET': "red"
        }

        # none white are markings that would be extremely blended into the natural pelts, to the point where
        # I feel like people don't usually notice their wolf has white. so they're not even described
        white_none = ['HIGHLIGHTS', 'WOLFTICKING']
        white_minimal = ['LOCKET', 'SOCKS', 'TOES', 'TRIM', 'BACKLEG']
        white_blaze = ["FLASH", 'STRIPE', 'SPECKLES', 'BLAZE']
        white_irish = ['IRISH', 'MOONRISE', 'STAR', 'TICKING', 'DIAMOND']
        white_piebald = ['BLOTCH', 'HEART', 'MUNSTERLANDER', 'HOUND', 'KING', 'BLUETICK', 'PIEBALD']
        white_extreme_piebald = ['EXTREMEPIEBALD', 'TAIL', 'HEELER']
        white_ticking = ['SPECKLES', 'MUNSTERLANDER', 'HEART', 'TICKING', 'BLUETICK']
        white_special = {
            "SNOWFLAKE": "snowflake spots",
            'JACKAL': 'ticked white',
            'SPLIT': "split faced white",
            'BEE': "white stripes",
            'DAPPLES': "dappled white",
            'POINTED': "flashy white",
            'HALF': "split face piebald",
            'SPITZ': "spitz white",
            'SUMMERFOX': "flashy white",
            'URAJIRO': "urajiro",
            'LIGHTDALMATIAN': "light dalmatian",
            'HEAVYDALMATIAN': "heavy dalmatian",
            "WHITE": "white"
            }

        # setting up all the descriptors
        # these will be used to construct sentences at the end
        # descriptors given None will be used later as well to skip over them or modify how the sentence
        # is built. For now, all of them get None
        # some will always be given a string of some kind
        # this includes: colorBASE, basePATTERN, speciesTYPE, and colorEYE

        colorBASE = None
        colorTORTIE = None
        tortiePATTERN = None
        caninePOINTS = None
        specialPOINTS = None
        basePATTERN = None
        merlePATTERN = None
        speciesTYPE = None
        whitePATCH = None
        colorEYE = None
        colorEYETWO = None

        # BASE COLOR
        # this is simple - it takes the color name of the pelt and grabs the dictionary key for it above
        colorBASE = renamed_colors[str(cat.pelt.colour).lower()]

        # TORTIES
        # torties are the same, but we check if torties are active or not. if not, it does nothing
        # and we also specify what kind of tortie we have
        # then we set patterns and decide which pattern is most 'interesting' for the description
        if cat.pelt.name == 'Tortie' or cat.pelt.name == 'Calico':
            temp_agoutis = ["Graywolf", "Ophelia", "Runic", "Timber", "Arctic", "Winter", "Mexican", "Stormy", "Vibrant", "Smokey", "Agouti", "Aspen", "Cali"]
            temp_tortie_type = cat.pelt.tortiebase
            basePATTERN = cat.pelt.tortiepattern
            colorTORTIE = renamed_colors[str(cat.pelt.tortiecolour).lower()]
            # the name of the pelt should be either tortie or calico depending on a few other factors
            tortiePATTERN = str(cat.pelt.name).lower()
            # now we're going to break it down into its base parts
            if temp_tortie_type in temp_agoutis:
                temp_tortie_type = "agouti"
            if basePATTERN in temp_agoutis:
                basePATTERN = "agouti"
            # and then pick the most interesting pattern to list on the description
            if basePATTERN == temp_tortie_type:
                basePATTERN = "agouti"
            elif temp_tortie_type == "Points" or basePATTERN == "Points":
                basePATTERN = "points"
            elif temp_tortie_type in temp_agoutis:
                basePATTERN = str(basePATTERN).lower()
            elif basePATTERN in temp_agoutis:
                basePATTERN = str(temp_tortie_type).lower()
            else:
                basePATTERN = str(basePATTERN).lower()
            # and adjusting two possible words to make it better
            if basePATTERN == "husky":
                basePATTERN = "domino"
            if basePATTERN == "semisolid":
                basePATTERN = "solid"
            # and we're done. for sentence building only this will be referenced along with the 2 colors
        # BASE PATTERN (NON TORTIE)
        # this one is easy - grab the dictionary description for the pattern, then we do one fast check for brindle
        # and then do nothing else
        else:
            basePATTERN = str(pattern_des[cat.pelt.name])
            if basePATTERN == 'brindle' and colorBASE == 'black':
                basePATTERN = 'solid'

        # CANINE POINTS
        # now we've got a difficult one - points. this will only run if the basepattern is points, otherwise
        # it is skipped because it's very intensive. it is based off the appearence of the points in game
        # all other color information is discarded at the end if points are present
        temp_color_name = ''
        if basePATTERN == 'points':
            point_name = str(cat.pelt.colour).lower()
            if point_name in ["black", "thistle", "luna", "void"]:
                temp_color_name = "black"
            elif point_name == "spice" or point_name == "ginger" or point_name == "copper" or point_name == "redwood":
                temp_color_name = "black and red"
            elif point_name == "honey" or point_name == "flaxen":
                temp_color_name = "black and fawn"
            elif point_name == "cream" or point_name == "pearl":
                temp_color_name = "black and cream"
            elif point_name == "mist" or point_name == "ash" or point_name == "silver" or point_name == 'moonstone' or point_name == "pyrite":
                temp_color_name = "gray and silver"
            elif point_name == "steel" or point_name == "onyx" or point_name == "gosling":
                temp_color_name = "black and gray"
            elif point_name == "chocolate" or point_name == "blue" or point_name == "lilac":
                temp_color_name = str(renamed_colors[point_name]) + " and cream"
            elif point_name == "cocoa" or point_name == "hazelnut":
                temp_color_name = "chocolate and fawn"
            elif point_name == "frost":
                temp_color_name = "blue and white"
            elif point_name == "spruce":
                temp_color_name = "blue and gray"
            elif point_name == "isabella":
                temp_color_name = "isabella and silver"
            elif point_name == "sunny":
                temp_color_name = "gold and cream"
            elif point_name == "gold":
                temp_color_name = "black and gold"
            elif point_name == "brass":
                temp_color_name = "brown and tan"
            elif point_name == "sunstone":
                temp_color_name = "peach and cream"
            elif point_name == "daisy":
                temp_color_name = "cream and white"
            elif point_name == "peachy":
                temp_color_name = "red and peach"
            elif point_name == "snow":
                temp_color_name = "silver and white"
            # now we wrap up the point stuff
            if colorTORTIE == None:
                # we are going to change solid black points to match for later, to avoid more calculation
                if temp_color_name == "black":
                    basePATTERN = 'solid'
                    colorBASE = 'black'
                    caninePOINTS = None
                # otherwise, just make the point statement the same as we already determined above
                else:
                    caninePOINTS = str(temp_color_name)
            # torties complicate things yet again. we need to string the sentence together with the tortie color
            else:
                # but we need to account for this first
                if temp_color_name == "black":
                    basePATTERN = 'solid'
                    colorBASE = 'black'
                    caninePOINTS = None
                else:
                    caninePOINTS = colorTORTIE + ", " + temp_color_name
                # and now we need to delete awkward wording. ugh torties
                caninePOINTS.replace("black, black", "black").replace("blue, blue", "blue").replace("golden, gold", "gold").replace("gray, gray", "gray")
                # there will likely be more awkward wording because of 'cream' but this is fine for now

        # COLOR ADJUSTMENT (TORTIES)
        if colorTORTIE != None and caninePOINTS == None:
            colorBASE = str(colorBASE + ' and ' + colorTORTIE)
            
        # SPECIAL POINTS
        # now we dive into true colorpoints. first we'll determine if there's any present at all, then get rid of the
        # one that needs no further expansion
        if cat.pelt.points == None:
            specialPOINTS = None
        else:
            if cat.pelt.points == 'ALBINO':
                basePATTERN = 'solid'
                colorBASE = 'white'
            elif cat.pelt.points == 'BEW':
                colorBASE = 'ghost'
            elif cat.pelt.points == "POINT":
                specialPOINTS = 'pointed'
            elif cat.pelt.points == "HIMALAYAN":
                specialPOINTS = 'himalayan'
            # all the points that are simple to describe
            else:
                specialPOINTS = str(cat.pelt.points).lower() + 'point'

        # MERLES AND HARLEQUINS
        # oh boy oh fun
        # remember that harlequin is only active if merle is, so we check for that first
        # merles and harlequins are boolean values as well, so we don't need to add more to our statements
        if cat.pelt.merle:
            if cat.pelt.harlequin:
                merlePATTERN = "harlequin"
            else:
                merlePATTERN = "merle"

        # SPECIES
        # this is required. it's pretty easy as well
        speciesTYPE = str(cat.pelt.species).lower()

        # WHITE PATCHES
        # now we run into some issues here. we've got a few things going on - the extent and pattern of the white
        # as well as if it's ticked or spotted. earlier we defined these. some have special definitions so we'll do those first
        temp_white = cat.pelt.white_patches # this is done so it's not accessed a million times
        if temp_white == None or temp_white in white_none:
            whitePATCH = None
        elif temp_white in white_special:
            whitePATCH = str(white_special[temp_white])
        elif temp_white in white_minimal:
            if temp_white in white_ticking:
                whitePATCH = "ticked minimal white"
            else:
                whitePATCH = "minimal white"
        elif temp_white in white_blaze:
            if temp_white in white_ticking:
                whitePATCH = "ticked blaze"
            else:
                whitePATCH = "blaze"
        elif temp_white in white_irish:
            if temp_white in white_ticking:
                whitePATCH = "ticked irish white"
            else:
                whitePATCH = "irish white"
        elif temp_white in white_piebald:
            if temp_white in white_ticking:
                whitePATCH = "ticked piebald"
            else:
                whitePATCH = "piebald"
        elif temp_white in white_extreme_piebald:
            if temp_white in white_ticking:
                whitePATCH = "ticked extreme piebald"
            else:
                whitePATCH = "extreme piebald"

        # EYE COLORS
        # okay last step before stringing things together is the eyes. we'll go ahead and have the eye colors defined
        # and then we'll string these together (or not if there's only one eye color)
        # we defined the changed eye colors earlier
        # we're also sticking the term 'eyes' on the end to make sentence building faster
        colorEYE = str(eye_des[cat.pelt.eye_colour])
        if cat.pelt.eye_colour2 == None:
            colorEYE = str(colorEYE + ' eyes')
        elif colorBASE == 'ghost':
            colorEYE = str("piercing ice-blue eyes")
        else:
            colorEYETWO = str(eye_des[cat.pelt.eye_colour2])
            colorEYE = str(colorEYE + ' and ' + colorEYETWO + ' eyes')

        # SENTENCE BUILDING
        # we know from before which ones will always be not none, and which ones are variable. so let's build
        # based on that
        temp_sentence = ''

        # first, get these overrides out of the way
        # this will basically change all color and pattern info to white, so we check it first
        if whitePATCH == 'white' or basePATTERN == 'solid' and colorBASE == 'white':
            if cat.pelt.points == 'ALBINO':
                temp_sentence = str("albino " + speciesTYPE)
            elif cat.pelt.points == 'BEW':
                temp_sentence = str("white " + speciesTYPE + " with piercing ice-blue eyes")
            else:
                temp_sentence = str("white " + speciesTYPE + " with " + colorEYE)
        # now solids mean we ignore pattern info, so we'll do these next
        elif basePATTERN == 'solid':
            temp_sentence = str(colorBASE)
            if merlePATTERN != None:
                temp_sentence = str(temp_sentence + ' ' + merlePATTERN)
            if specialPOINTS != None:
                temp_sentence = str(temp_sentence + ' ' + specialPOINTS)
            if tortiePATTERN != None:
                temp_sentence = str(temp_sentence + ' ' + tortiePATTERN)
            temp_sentence = str(temp_sentence + ' ' + speciesTYPE)
            if whitePATCH != None:
                temp_sentence = str(temp_sentence + ' with ' + whitePATCH)
            if colorEYETWO != None:
                if whitePATCH != None:
                    temp_sentence = str(temp_sentence + "; " + colorEYE)
                else:
                    temp_sentence = str(temp_sentence + ' with ' + colorEYE)
            else:
                if whitePATCH == None:
                    temp_sentence = str(temp_sentence + ' with ' + colorEYE)
                else:
                    temp_sentence = str(temp_sentence + ' and ' + colorEYE)
        # then canine points, which change the structure of our sentences a bit
        elif caninePOINTS != None:
            temp_sentence = str(caninePOINTS)
            # if there's special points we want those displayed instead
            if specialPOINTS != None:
                if merlePATTERN != None:
                    temp_sentence = str(temp_sentence + ' ' + merlePATTERN + ' ' + specialPOINTS)
                else:
                    temp_sentence = str(temp_sentence + ' ' + specialPOINTS)
            else:
                if merlePATTERN != None:
                    temp_sentence = str(temp_sentence + ' ' + merlePATTERN + ' point')
                else:
                    temp_sentence = str(temp_sentence + ' point')
            if tortiePATTERN != None:
                temp_sentence = str(temp_sentence + ' ' + tortiePATTERN)
            temp_sentence = str(temp_sentence + ' ' + speciesTYPE)
            if whitePATCH != None:
                temp_sentence = str(temp_sentence + ' with ' + whitePATCH)
            if colorEYETWO != None:
                if whitePATCH != None:
                    temp_sentence = str(temp_sentence + "; " + colorEYE)
                else:
                    temp_sentence = str(temp_sentence + ' with ' + colorEYE)
            else:
                if whitePATCH == None:
                    temp_sentence = str(temp_sentence + ' with ' + colorEYE)
                else:
                    temp_sentence = str(temp_sentence + ' and ' + colorEYE)
        # and finally, the most common stuff ends up here. thankfully we made the checks above fast so this should
        # load relatively quickly
        else:
            temp_sentence = str(colorBASE)
            if merlePATTERN != None:
                temp_sentence = str(temp_sentence + ' ' + merlePATTERN)
            if specialPOINTS != None:
                temp_sentence = str(temp_sentence + ' ' + specialPOINTS)
            else:
                temp_sentence = str(temp_sentence + ' ' + str(basePATTERN))
            if tortiePATTERN != None:
                temp_sentence = str(temp_sentence + ' ' + tortiePATTERN)
            temp_sentence = str(temp_sentence + ' ' + speciesTYPE)
            if whitePATCH != None:
                temp_sentence = str(temp_sentence + ' with ' + whitePATCH)
            if colorEYETWO != None:
                if whitePATCH != None:
                    temp_sentence = str(temp_sentence + "; " + colorEYE)
                else:
                    temp_sentence = str(temp_sentence + ' with ' + colorEYE)
            else:
                if whitePATCH == None:
                    temp_sentence = str(temp_sentence + ' with ' + colorEYE)
                else:
                    temp_sentence = str(temp_sentence + ' and ' + colorEYE)

        # now it's complete, we'll throw it where it needs to be
        color_name = temp_sentence
        return color_name
        
        # some stuff I may add later below. for now it does nothing, since the name is returned above

        # Here is the place where we can add some additional details about the cat, for the full non-short one. 
        # These include notable missing limbs, vitiligo, long-furred-ness, and 3 or more scars. 
        if not short:
            
            scar_details = {
                "NOTAIL": "no tail",
                "HALFTAIL": "half a tail",
                "NOPAW": "three legs",
                "NOLEFTEAR": "a missing ear",
                "NORIGHTEAR": "a missing ear",
                "NOEAR": "no ears"
            }

            additional_details = []
            #if cat.pelt.vitiligo:
            #    additional_details.append("vitiligo")
            for scar in cat.pelt.scars:
                if scar in scar_details and scar_details[scar] not in additional_details:
                    additional_details.append(scar_details[scar])

            if len(additional_details) > 1:
                color_name = f"{color_name} with {', '.join(additional_details[:-1])} and {additional_details[-1]}"
            elif additional_details:
                color_name = f"{color_name} with {additional_details[0]}"

            if len(cat.pelt.scars) >= 3:
                color_name = f"scarred {color_name}"

        return color_name

    def get_sprites_name(self):
        return Pelt.sprites_names[self.name]
