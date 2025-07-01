import random
from re import sub

from scripts.cat.sprites import sprites
from scripts.game_structure.game_essentials import game


class Pelt:

    #torties
    tortiepatterns = ['CAPE', 'DIPPED', 'HEARTBREAKER', 'INKSPILL', 'MINIMAL', 'PHANTOM',
		'PUDDLES', 'REDTAIL', 'SHADOWSTEP', 'SPLIT', 'SPLOTCH', 'WATERFALL']
    tortiebases = ["GRAYWOLF", "OPHELIA", "RUNIC", "TIMBER", "SABLE", "SHEPHERD", 
		"ARCTIC", "WINTER", "HUSKY", "MEXICAN", "STORMY", "VIBRANT", "COLORPOINT", "SMOKEY", 
		"POINTS", "SEMISOLID", "SOLID", "AGOUTI", "ASPEN", "CALI", "GRIZZLE", "FOXY", "SVALBARD"]
    # I want to get rid of this eventually
    pelt_length = ["short", "medium", "long"]
    # eyes
    eye_categories = sprites.pelt_generation["eye_color_categories"]
    eye_colors = sprites.pelt_generation["eye_colors"]
    eye_info = sprites.misc_colors["eyes"]
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
            "CLOVER", "DAISY", "DRY HERBS", "DRY CATMINT", "DRY NETTLES", "DRY LAURELS",
            "BLACK EYED SUSANS", "GOLD HERBS", "IVY", "MARIGOLD", "PURPLE PETALS",
            "ROSE", "SAKURA", "SUNFLOWER", "WHITE ROSE"]
    wild_accessories = ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "GULL FEATHERS",
            "SPARROW FEATHERS", "MOTH WINGS", "ROSY MOTH WINGS",
            "MORPHO BUTTERFLY", "MONARCH BUTTERFLY", "CICADA WINGS",
            "BLACK CICADA", "CROW FEATHERS", "DOVE FEATHERS"]
    manmade_accessories = ['TOWEL', 'SILK CLOAK']
    special_accessories = ["HIBISCUS", "RED HIBISCUS", "WHITE HIBISCUS", "BIG LEAVES", "STARFISH", "PINK STARFISH",
                           "PURPLE STARFISH", "PEARLS", "SEASHELLS", "TOWEL", "SILK CLOAK"]
    pet_accessories = ["BANDANABACK", "BANDANA", "BELL", "BOW", "COLLAR", "HARNESS", "LEATHER", "NYLON", "RADIO"]
    pet_accessories_color_categories = sprites.pet_accessory_colors["color_categories"]["CATEGORIES"]
    bandana_patterns = ["PLAID", "SWIRL"]
    every_acc_list = [plant_accessories, wild_accessories, pet_accessories]
    acc_category_weights = sprites.pet_accessory_colors["color_categories"]["WEIGHTS"]
    acc_potential_colors = sprites.pet_accessory_colors["color_categories"]
    pet_accessory_info = sprites.pet_accessory_colors["colors"]
    # pelts
    standardpelts = ["GRAYWOLF", "OPHELIA", "RUNIC", "TIMBER", "SABLE", "SHEPHERD", "ASPEN"]
    northpelts = ["ARCTIC", "WINTER", "HUSKY", "SVALBARD"]
    southpelts = ["MEXICAN", "STORMY", "VIBRANT", "CALI", "FOXY"]
    darkpelts = ["COLORPOINT", "SMOKEY", "POINTS", "AGOUTI", "GRIZZLE"]
    specialpelts = ["SEMISOLID", "SOLID", "BRINDLE"]
    pelt_categories = ["standardpelts", "northpelts", "southpelts", "darkpelts", "specialpelts"]

    # colors and stuff
    pelt_color_categories = sprites.pelt_generation["pelt_color_categories"]
    pelt_colors = sprites.pelt_generation["pelt_colors"]
    
    # merles
    merles = ['BRIGHTLEAF', 'SILVERCLAW', 'SEAFUR', 'DAPPLEPELT', 'WILLOWLEAF', 'DAYSKY', 'BRINDLECLOUD', 'SHADOWSNEAK', 'DARKDAPPLE', 'STORMSONG']
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
    skin_sprites = ["SOLID", "BUTTERFLY", "DUDLEY", "SNOWNOSE", "SPECKLED"]
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
                 species:str="Wolf",
                 species_mix:list=["W", "W", "C", "C", "D", "D"],
                 eye_color:str="BLUE",
                 eye_color2:str=None,
                 skin:list=None,
                 pattern:str="SOLID",
                 color:str="WHITE",
                 tortie:str=None,
                 tortiepattern:str=None,
                 tortiecolor:str=None,
                 merle:list=False,
                 harlequin:bool=False,
                 white_patches:str=None,
                 points:str=None,
                 points_genes:list=["C", "C"],
                 vitiligo:str=None,
                 tint:str=None,
                 white_patches_tint:str=None,
                 length:str="short",
                 accessory:str=None,
                 scars:list=None,
                 opacity:int=100,
                 fun_traits:list=["o", "o", "o"],
                 paralyzed:bool=False,
                 kitten_sprite:int=None,
                 adol_sprite:int=None,
                 adult_sprite:int=None,
                 senior_sprite:int=None,
                 para_adult_sprite:int=None,
                 reverse:bool=False,
                 ) -> None:
        self.species = species
        self.species_mix = species_mix
        self.eye_color = eye_color
        self.eye_color2 = eye_color2
        self.skin = skin
        self.pattern = pattern
        self.color = color
        self.tortie = tortie
        self.tortiepattern = tortiepattern
        self.tortiecolor = tortiecolor
        self.merle = merle
        self.harlequin = harlequin
        self.white_patches = white_patches
        self.points = points
        self.points_genes = points_genes
        self.vitiligo = vitiligo
        self.tint = tint
        self.white_patches_tint = white_patches_tint
        self.length = length
        self.accessory = accessory
        self.scars = scars if isinstance(scars, list) else []
        self.opacity = opacity
        self.fun_traits = fun_traits
        self.paralyzed = paralyzed
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
        

    @staticmethod
    def generate_new_pelt(gender: str, parents: tuple = (), age: str = "adult"):
        new_pelt = Pelt()

        parents_species = []
        parents_length = []
        parents_pattern = []
        parents_color = []
        parents_merle = []
        parents_harlequin = []
        parents_white_patches = []
        parents_points_genes = []
        parents_eyecolor = []
        parents_eyecolor2 = []
        
        if parents:
            for parent in parents:
                if parent:
                    pelt = parent.pelt
                    parents_species.append(pelt.species_mix)
                    parents_length.append(pelt.length)
                    parents_pattern.append(pelt.pattern)
                    parents_color.append(pelt.color)
                    parents_merle.append(pelt.merle)
                    parents_harlequin.append(pelt.harlequin)
                    parents_white_patches.append(pelt.white_patches)
                    parents_points_genes.append(pelt.points_genes)
                    parents_eyecolor.append(pelt.eye_color)
                    parents_eyecolor2.append(pelt.eye_color2)

        new_pelt.init_species(parents_species)
        new_pelt.init_length()
        new_pelt.init_pattern(parents_pattern, parents_color)
        new_pelt.init_tortie(gender)
        new_pelt.init_merle(parents_merle, parents_harlequin)
        new_pelt.init_white(parents_white_patches)
        new_pelt.init_points(parents_points_genes)
        new_pelt.init_tint()
        new_pelt.init_skin()
        new_pelt.init_eyes(parents_eyecolor, parents_eyecolor2)
        new_pelt.init_accessory(age)
        new_pelt.init_scars(age)
        new_pelt.init_fun_traits()
        new_pelt.init_sprite()

        print(new_pelt.species)
        print(new_pelt.species_mix)
        print(new_pelt.pattern)
        print(new_pelt.color)
        print(new_pelt.tortie)
        print(new_pelt.tortiepattern)
        print(new_pelt.tortiecolor)
        print(new_pelt.skin)
        print(new_pelt.eye_color)
        print(new_pelt.eye_color2)
        print(new_pelt.merle)
        print(new_pelt.harlequin)
        print(new_pelt.points)
        print(new_pelt.points_genes)
        print(new_pelt.white_patches)
        
        return new_pelt

    def init_species(self, parents_species):
        # sets species and species_mix
        #### --- genes --- ####
        genes = ["", "", "", "", "", ""]
        poss_genes = ["W", "C", "D"]
        quick_genes = [["W", "W", "W", "W", "W", "W"], ["C", "C", "C", "C", "C", "C"]]
        if parents_species:
            # choose something with the parents species
            parent_number = len(parents_species)
            # add a 'parent' if there's only one
            if parent_number < 2:
                parent_number = 2
                parents_species.append(random.choices(quick_genes, weights = [100, 20], k=1)[0])
            index = random.randint(0, parent_number - 1)
            parent_gene_1 = parents_species[index]
            parents_species.pop(index)
            parent_number -= 1
            index = random.randint(0, parent_number - 1)
            parent_gene_2 = parents_species[index]

            for index, gene in enumerate(genes):
                if random.getrandbits(1):
                    genes[index] = parent_gene_1[index]
                else:
                    genes[index] = parent_gene_2[index]
        else:
            # randomize
            if random.randint(0, 10) > 3:
                genes = random.choices(quick_genes, weights = [100, 20], k=1)[0]
            else:
                for index, gene in enumerate(genes):
                    genes[index] = random.choices(poss_genes, weights=(400, 40, 10), k=1)[0]

        #### --- species --- ####
        species = ""
        if "C" not in genes and "D" not in genes:
            species = "Wolf"
        elif "D" not in genes and "W" not in genes:
            species = "Coyote"
        else:
            wolf = genes.count("W")
            yote = genes.count("C")
            dog = genes.count("D")
            if dog == 0:
                species = "Coywolf"
            elif yote == 0:
                species = "Wolfdog"
            elif wolf == 0:
                species = "Coydog"
            elif wolf >=3:
                species = "Wolf Hybrid"
            elif yote >=3:
                species = "Coyote Hybrid"
            else:
                species = "Hybrid"

        self.species_mix = genes
        self.species = species

    def init_length(self):
        # sets pelt length
        # later will be reused to set pelt features in general
        self.length = random.choice(Pelt.pelt_length)

    def init_pattern(self, parents_pattern, parents_color):
        # sets pattern and color
        #### --- pelt pattern --- ####
        weights = [0, 0, 0, 0, 0] #standard, north, south, dark, special
        # sets weights for random pelt pattern choices
        if parents_pattern:
            if len(parents_pattern) < 2:
                # add some randomization to not copy the parent if there's only 1
                parents_pattern.append(None)
            for parent in parents_pattern:
                if parent:
                    if parent in Pelt.standardpelts:
                        add_weight = sprites.pelt_generation["parent_pelt_patterns"]["standardpelts"]
                    elif parent in Pelt.northpelts:
                        add_weight = sprites.pelt_generation["parent_pelt_patterns"]["northpelts"]
                    elif parent in Pelt.southpelts:
                        add_weight = sprites.pelt_generation["parent_pelt_patterns"]["southpelts"]
                    elif parent in Pelt.darkpelts:
                        add_weight = sprites.pelt_generation["parent_pelt_patterns"]["darkpelts"]
                    elif parent in Pelt.specialpelts:
                        add_weight = sprites.pelt_generation["parent_pelt_patterns"]["specialpelts"]
                else:
                    add_weight = sprites.pelt_generation["random_pelt_patterns"]["pelt_categories"]
                for index, weight in enumerate(weights):
                    weights[index] += add_weight[index]
        else:
            # randomly choose
            weights = sprites.pelt_generation["random_pelt_patterns"]["pelt_categories"]

        # set the pelt pattern
        pelt_pattern = ""
        temp_pattern = random.choices(Pelt.pelt_categories, weights=weights, k=1)[0]
        if temp_pattern == "standardpelts":
            pelt_pattern = random.choices(Pelt.standardpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["standardpelts"], k = 1)[0]
        elif temp_pattern == "northpelts":
            pelt_pattern = random.choices (Pelt.northpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["northpelts"], k = 1)[0]
        elif temp_pattern == "southpelts":
            pelt_pattern = random.choices(Pelt.southpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["southpelts"], k = 1)[0]
        elif temp_pattern == "darkpelts":
            pelt_pattern = random.choices(Pelt.darkpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["darkpelts"], k = 1)[0]
        elif temp_pattern == "specialpelts":
            pelt_pattern = random.choices(Pelt.specialpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["specialpelts"], k = 1)[0]

        #### --- pelt color --- ####
        weights = []
        for n in Pelt.pelt_color_categories:
            weights.append(0)

        if parents_color:
            if len(parents_color) < 2:
                parents_color.append(None)
            for color in parents_color:
                if parent:
                    for x in Pelt.pelt_colors:
                        if parent in Pelt.pelt_colors[x]:
                            add_weight = sprites.pelt_generation["parent_pelt_colors"][x]
                            break
                else:
                    add_weight = sprites.pelt_generation["random_pelt_colors"]["color_categories"]
                for index, weight in enumerate(weights):
                    weights[index] += add_weight[index]
        else:
            weights = sprites.pelt_generation["random_pelt_colors"]["color_categories"]

        temp_pelt_color = random.choices(Pelt.pelt_color_categories, weights=weights, k=1)[0]
        pelt_color = random.choices(Pelt.pelt_colors[temp_pelt_color], weights=sprites.pelt_generation["random_pelt_colors"][temp_pelt_color], k=1)[0]

        self.pattern = pelt_pattern
        self.color = pelt_color

    def init_tortie(self, gender):
        # sets tortie, tortiepattern, and tortiecolor, if the tortie is generated
        f_chance = game.config["cat_generation"]["base_female_tortie"]
        m_chance = game.config["cat_generation"]["base_male_tortie"]
        tortie = False
        if gender == "female":
            tortie = random.getrandbits(f_chance) == 1
        else:
            tortie = random.getrandbits(m_chance) == 1

        if tortie:
            # tortie was generated
            possible_pelt = Pelt.tortiebases.copy()
            possible_colors = sprites.pelt_generation["tortie_combos"][self.color].copy()
            wildcard_chance = game.config["cat_generation"]["wildcard_tortie"]

            #### --- tortie --- ####
            self.tortie = random.choice(Pelt.tortiepatterns)
            if not wildcard_chance or random.getrandbits(wildcard_chance) == 1:
                print("Wildcard tortie!")
                self.tortiepattern = random.choice(possible_pelt)
                possible_pelt_colors.remove(self.color)
                # KORI - check for bugs
                possible_colors = []
                for pelt in sprites.pelt_generation["pelt_colors"]:
                    for color in sprites.pelt_generation["pelt_colors"][pelt]:
                        possible_colors.append(color)
                self.tortiecolor = random.choice(possible_colors)
            else:
                if random.randint(0, 10) <= 2:
                    self.tortiepattern = self.pattern
                else:
                    if random.randint(0, 2) == 1:
                        solid_pelts = ["SOLID", "SEMISOLID"]
                        self.tortiepattern = random.choice(solid_pelts)
                    else:
                        possible_pelt.remove(self.pattern)
                        self.tortiepattern = random.choice(possible_pelt)
                if random.randint(0, 10) == 10 and self.tortiepattern != self.pattern:
                    self.tortiecolor = self.color
                else:
                    self.tortiecolor = random.choice(possible_colors)
        
    def init_merle(self, parents_merle, parents_harlequin):
        # sets merle and harlequin
        merle_bool = False
        harlequin_bool = False
        if parents_merle:
            if len(parents_merle) < 2:
                parents_merle.append(None)
                parents_harlequin.append(None)
            if random.choice(parents_merle):
                merle_bool = True
            if random.choice(parents_harlequin):
                harlequin_bool = True
        else:
            if random.randint(0, 100) <= sprites.pelt_generation["pelt_misc"]["merle"]:
                merle_bool = True
            if random.randint(0, 100) <= sprites.pelt_generation["pelt_misc"]["harlequin"]:
                harlequin_bool = True
        if merle_bool:
            merle_pattern = []
            merle_category = sprites.pelt_colors["colors"][self.color]["merle"]
            merle_pattern.append(random.choice(Pelt.merles)) # the merle mask
            merle_pattern.append(merle_category) # the merle color category
            possible_color = []
            for m in sprites.pelt_colors["merles"][merle_category]:
                possible_color.append(m)
            merle_pattern.append(random.choice(possible_color[1:])) # the merle color
            self.merle = merle_pattern
        self.harlequin = harlequin_bool
            
    def init_white(self, parents_white):
        # sets white_patches
        white_bool = False
        white_chance = 0
        dog_influence = self.species_mix.count("D")
        white_list = [Pelt.low_white, Pelt.mid_white, Pelt.high_white]
        if parents_white:
            for white in parents_white:
                if white:
                    white_chance += 35
        white_chance += dog_influence * 5
        if random.randint(0, 10) > 8:
            white_chance += 10
        if white_chance > 100:
            white_bool = True
        elif random.randint(0, 100) < white_chance:
            white_bool = True
        if white_bool:
            weights = [0, 0, 0]
            weights = [55, 35, 10]
            for w in parents_white:
                if w:
                    if w in white_list[0]: # low white
                        weights[0] += 60
                        weights[1] += 30
                        weights[2] += 10
                    elif w in white_list[1]: # mid white
                        weights[0] += 40
                        weights[1] += 50
                        weights[2] += 10
                    elif w in white_list[2]: # high white
                        weights[0] += 20
                        weights[1] += 50
                        weights[2] += 30
                else:
                    weights[0] += 55
                    weights[1] += 35
                    weights[2] += 10
            white_category = random.choices(white_list, weights=weights, k=1)[0]        
            self.white_patches = random.choice(white_category)

    def init_points(self, parents_points):
        # sets points and point_genes
        #### --- point genes --- #####
        points_genes = ["C", "C"]
        if parents_points:
            if len(parents_points) < 2:
                points_genes[0] = random.choice(parents_points[0])
                points_genes[1] = random.choices(Pelt.point_genes, weights=sprites.pelt_generation["pelt_misc"]["colorpoint_genes"], k=1)[0]
            else:
                temp_genes = random.randint(0, len(parents_points))
                points_genes[0] = random.choice(parents_points[temp_genes])
                parents_points.pop(temp_genes)
                if len(parents_points) < 2:
                    temp_genes = 0
                else:
                    temp_genes = random.randint(0, len(parents_points))
                points_genes[1] = random.choice(parents_points[temp_genes])
        else:
            points_genes[0] = random.choices(Pelt.point_genes, weights=sprites.pelt_generation["pelt_misc"]["colorpoint_genes"], k=1)[0]
            points_genes[1] = random.choices(Pelt.point_genes, weights=sprites.pelt_generation["pelt_misc"]["colorpoint_genes"], k=1)[0]

        #### --- points --- ####
        outcome = None
        if "C" in points_genes:
            outcome = None
        elif "cb" in points_genes:
            if "cs" in points_genes or "ch" in points_genes:
                outcome = "MINK"
            elif "cw" in points_genes or "c" in points_genes:
                outcome = "POINT"
            else:
                outcome = "SEPIA"
        elif "cs" in points_genes:
            if "ch" in points_genes:
                outcome = "POINT"
            elif "cw" in points_genes or "c" in points_genes:
                outcome = "CLEAR"
            else:
                outcome = "POINT"
        elif "ch" in points_genes:
            outcome: "HIMALAYAN"
        elif "cw" in points_genes:
            outcome: "BEW"
        else:
            outcome: "ALBINO"

        self.points_genes = points_genes
        self.points = outcome
            
    def init_tint(self):
        # sets tint and white_patch_tint

        #### --- pelt tint --- ####
        if random.getrandbits(1):
            base_tints = sprites.cat_tints["possible_tints"]["basic"]
            color_tints = []
            tint = ""
            if self.color in sprites.cat_tints["color_groups"]:
                color_group = sprites.cat_tints["color_groups"].get(self.color, "warm")
                color_tints = sprites.cat_tints["possible_tints"][color_group]
            tint = random.choice(base_tints + color_tints)
            if tint == "none":
                self.tint = None
            else:
                self.tint = tint

        #### --- white tint --- ####
        if self.white_patches or self.points:
            # apply a tint
            white_tint = ""
            color_tints = []
            if random.getrandbits(1):
                base_tints = sprites.white_patches_tints["possible_tints"]["basic"]
                # bypass tint selection to avoid weird combos if mostly white
                if self.points == "BEW":
                    white_tint = "yellowwhite"
                elif self.points == "ALBINO" or self.white_patches == "WHITE":
                    white_tint = "none"
                # do regular tint selection otherwise
                elif self.color in sprites.cat_tints["color_groups"]:
                    color_group = sprites.white_patches_tints["color_groups"].get(self.color, "white")
                    color_tints = sprites.white_patches_tints["possible_tints"][color_group]
                    white_tint = random.choice(base_tints + color_tints)
                else:
                    white_tint = random.choice(base_tints)
                if white_tint == "none":
                    self.white_patches_tint = None
                else:
                    self.white_patches_tint = white_tint

        #### --- ugly combo fix --- #####
        if self.white_patches_tint:
            if self.white_patches_tint in ["darkblue", "deepblue"]:
                if self.tint in ["red", "orange", "pink"]:
                    self.white_patches_tint = None
            elif self.white_patches_tint in ["darkred", "deepred"]:
                if self.tint in ["blue", "purple", "gray"]:
                    self.white_patches_tint == None
        
    def init_skin(self):
        # sets skin
        # relies on a few other factors
        # complex because it has to be

        skin_sprites = Pelt.skin_sprites.copy()
        low_white = Pelt.low_white.copy()
        mid_white = Pelt.mid_white.copy()
        high_white = Pelt.high_white.copy()
        possible_skins = [0, 0, 0, 0, 0]
        pink_solid = False
        merle_weights = [0, 0, 0, 0, 0]
        tortie_weights = [0, 0, 0, 0, 0]
        
        if self.points == "ALBINO" or self.points == "BEW":
            possible_skins = [100, 0, 0, 0, 0]
            pink_solid = True
        elif self.points == "HIMALAYAN" and random.getrandbits(1):
            possible_skins = [100, 0, 0, 0, 0]
            pink_solid = True
        elif self.white_patches:
            if self.white_patches in high_white:
                possible_skins = [80, 10, 0, 0, 10]
                if random.getrandbits(1):
                    pink_solid = True
            elif self.white_patches in mid_white:
                possible_skins = [60, 10, 10, 10, 10]
            else:
                possible_skins = [80, 5, 10, 10, 5]
            if self.merle:
                merle_weights = [0, 30, 0, 10, 20]
            if self.tortie:
                tortie_weights = [0, 10, 20, 20, 10]
        else:
            if self.merle:
                merle_weights = [60, 20, 0, 0, 20]
            else:
                possible_skins = [90, 0, 5, 5, 0]
            if self.tortie:
                tortie_weights = [0, 10, 20, 20, 10]
        if self.merle or self.tortie:
            for index, weight in enumerate(possible_skins):
                possible_skins[index] += merle_weights[index]
                possible_skins[index] += tortie_weights[index]

        # setting up the skin sprites
        # skin pattern, skin color category, skin color
        self.skin = []
        self.skin.append(random.choices(skin_sprites, weights=possible_skins, k=1)[0])

        base_skin = sprites.pelt_colors["colors"][self.color]["skin"]
        base_skin_list = []
        for x in sprites.misc_colors["skins"][base_skin]:
            base_skin_list.append(x)
        pink_color = sprites.pelt_generation["pelt_misc"]["white_skin_category"]
        pink_color_list = []
        for x in sprites.misc_colors["skins"][pink_color]:
            pink_color_list.append(x)

        # assigns colors
        if self.skin[0] == "SOLID" and pink_solid:
            self.skin.append(pink_color)
            self.skin.append(random.choice(pink_color_list))
        else:
            if self.skin[0] == "SOLID":
                self.skin.append(base_skin)
                self.skin.append(random.choice(base_skin_list))
            else:
                self.skin.append(base_skin)
                self.skin.append(random.choice(base_skin_list))
                self.skin.append(pink_color)
                self.skin.append(random.choice(pink_color_list))
        
    def init_eyes(self, parents_eyes, parents_eyes2):
        # sets eye_color and eye_color2
        # relies on a few other factors
        # KORI - modify the config to handle setting different weights for merles, white patches, and stuff

        # shortcut, points do weird things
        if self.points == "ALBINO":
            self.eye_color = random.choice(sprites.pelt_generation["points_eyes"]["ALBINO"])
            return
        elif self.points == "BEW":
            self.eye_color = random.choice(sprites.pelt_generation["points_eyes"]["BEW"])
            return

        # set up which base to draw the weights from
        if not parents_eyes:
            # set the eye color if there's no parents
            temp_eye_category = random.choices(Pelt.eye_categories, weights=sprites.pelt_generation["random_eye_colors"]["categories"], k=1)[0]
            self.eye_color = random.choice(sprites.pelt_generation["eye_colors"][temp_eye_category])
        else:
            parent_color_base = ""
            if len(parents_eyes) < 2:
                temp_eye_category = random.choices(Pelt.eye_categories, weights=sprites.pelt_generation["random_eye_colors"]["categories"], k=1)[0]
                parents_eyes.append(random.choice(sprites.pelt_generation["eye_colors"][temp_eye_category]))
            parent_color_base = random.choice(parents_eyes)

            # set the eye color if there's parents
            for color in Pelt.eye_categories:
                if parent_color_base in Pelt.eye_colors[color]:
                    weights = sprites.pelt_generation["parent_eye_colors"][color]
                    eye_category = random.choices(Pelt.eye_categories, weights=weights, k=1)[0]
                    self.eye_color = random.choice(sprites.pelt_generation["eye_colors"][eye_category])
                    break

        #### --- heterochromia --- ####
        het_chance = sprites.pelt_generation["heterochromia_chance"]
        chance = het_chance["base"]
        if self.white_patches in Pelt.high_white:
            chance -= het_chance["high_white"]
        elif self.white_patches in Pelt.mid_white:
            chance -= het_chance["mid_white"]
        if self.white_patches == "WHITE":
            chance -= 10
        if self.merle:
            chance -= het_chance["merle"]
        if self.points:
            chance -= het_chance["points"]
        for eye in parents_eyes2:
            if eye:
                chance -= het_chance["parent"]

        if chance < 0:
            chance = 1

        # find an appropriate het pairing
        if not random.randint(0, chance):
            for color in Pelt.eye_categories:
                if self.eye_color in Pelt.eye_colors[color]:
                    self.eye_color2 = random.choice(Pelt.eye_colors[random.choice(sprites.pelt_generation["heterochromia_pairing"][color])])
                    break
                
    def init_accessory(self, age):
        # gives them an accessory if they generate with one
        if age == "newborn":
            self.accessory = None
            return
        acc_display_choice = random.randint(0, 80)
        if age in ["kitten", "adolescent"]:
            acc_display_choice = random.randint(0, 180)
        elif age in ["adult", "young adult"]:
            acc_display_choice = random.randint(0, 100)

        if acc_display_choice in range(1, 30):
            self.accessory = ["", None, None]
            self.accessory[0] = random.choice([
                random.choice(Pelt.plant_accessories),
                random.choice(Pelt.wild_accessories)])
        elif acc_display_choice in range(31, 45):
            self.accessory = ["RADIO", "SOLID", ""]
            self.accessory[2] = random.choice(Pelt.acc_potential_colors[random.choices(Pelt.pet_accessories_color_categories, weights=Pelt.acc_category_weights, k=1)[0]])
        elif acc_display_choice in range(46, 62):
            # collars
            self.accessory = ["", "SOLID", ""]
            possible_collars = ["BANDANA", "BANDANABACK", "BELL", "BOW", "COLLAR", "LEATHER", "NYLON"]
            collar_weights = [10, 5, 5, 5, 20, 20, 10]
            self.accessory[0] = random.choices(possible_collars, weights=collar_weights, k=1)[0]
            if self.accessory[0] in ["BANDANA", "BANDANABACK"] and random.randint(1, 3) == 3:
                self.accessory[1] = random.choice(Pelt.bandana_patterns)
            self.accessory[2] = random.choice(Pelt.acc_potential_colors[random.choices(Pelt.pet_accessories_color_categories, weights=Pelt.acc_category_weights, k=1)[0]])
        elif acc_display_choice in range(63, 71):
            self.accessory = ["HARNESS", "SOLID", ""]
            self.accessory[2] = random.choice(Pelt.acc_potential_colors[random.choices(Pelt.pet_accessories_color_categories, weights=Pelt.acc_category_weights, k=1)[0]])
        else:
            self.accessory = None
        
    def init_scars(self, age):
        # gives them scars if they generate with them
        if age == "newborn":
            return
        if age in ['kitten', 'adolescent']:
            scar_choice = random.randint(0, 50)  # 2%
        elif age in ['young adult', 'adult']:
            scar_choice = random.randint(0, 20)  # 5%
        else:
            scar_choice = random.randint(0, 15)  # 6.67%

        if scar_choice == 1:
            self.scars.append(random.choice([
                random.choice(Pelt.scars1),
                random.choice(Pelt.scars3)
            ]))

        if 'NOTAIL' in self.scars and 'HALFTAIL' in self.scars:
            self.scars.remove('HALFTAIL')
        
    def init_fun_traits(self):
        # some silly stuff
        self.fun_traits[0] = random.choice(Pelt.fun_scents)
        self.fun_traits[1] = random.choice(Pelt.fun_physical)
        self.fun_traits[2] = random.choice(Pelt.fun_random)

    def init_sprite(self):
        # gives poses
        self.cat_sprites = {
            'newborn': 20,
            'kitten': random.randint(0, 2),
            'adolescent': random.randint(3, 5),
            'senior': random.randint(12, 14),
            'sick_young': 19,
            'sick_adult': 18
        }
        self.reverse = random.choice([True, False])
        self.cat_sprites['adult'] = random.randint(6, 11)
        self.cat_sprites['para_adult'] = 15
        self.cat_sprites['young adult'] = self.cat_sprites['adult']
        self.cat_sprites['senior adult'] = self.cat_sprites['adult']
        
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
        colorBASE = renamed_colors[str(cat.pelt.color).lower()]

        # TORTIES
        # torties are the same, but we check if torties are active or not. if not, it does nothing
        # and we also specify what kind of tortie we have
        # then we set patterns and decide which pattern is most 'interesting' for the description
        if cat.pelt.name == 'Tortie' or cat.pelt.name == 'Calico':
            temp_agoutis = ["Graywolf", "Ophelia", "Runic", "Timber", "Arctic", "Winter", "Mexican", "Stormy", "Vibrant", "Smokey", "Agouti", "Aspen", "Cali"]
            temp_tortie_type = cat.pelt.tortiebase
            basePATTERN = cat.pelt.tortiepattern
            colorTORTIE = renamed_colors[str(cat.pelt.tortiecolor).lower()]
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
            point_name = str(cat.pelt.color).lower()
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
        colorEYE = str(eye_des[cat.pelt.eye_color])
        if cat.pelt.eye_color2 == None:
            colorEYE = str(colorEYE + ' eyes')
        elif colorBASE == 'ghost':
            colorEYE = str("piercing ice-blue eyes")
        else:
            colorEYETWO = str(eye_des[cat.pelt.eye_color2])
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
