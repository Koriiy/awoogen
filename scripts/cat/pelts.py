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
                temp_genes = random.randint(0, len(parents_points) - 1)
                points_genes[0] = random.choice(parents_points[temp_genes])
                parents_points.pop(temp_genes)
                if len(parents_points) < 2:
                    temp_genes = 0
                else:
                    temp_genes = random.randint(0, len(parents_points) - 1)
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
        # dear god i hate this
        pattern_des = {
            "graywolf": "agouti",
            "ophelia": "agouti",
            "runic": "agouti",
            "timber": "agouti",
            "sable": "sable",
            "shepherd": "saddle",
            "arctic": "arctic",
            "winter": "winter",
            "husky": "domino",
            "mexican": "lustrous",
            "stormy": "umbrous",
            "vibrant": "vibrant",
            "colorpoint": "colorpoint",
            "smokey": "smokey",
            "points": "points",
            "semisolid": "solid",
            "solid": "solid",
            'brindle': 'brindle',
            "agouti": "shaded",
            "aspen": "agouti",
            "cali": "peppered",
            "grizzle": "grizzle",
            "foxy": "fox-like",
            "svalbard": "patchy saddle"
        }

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
            'HEAVYDALMATIAN': "heavy dalmatian"
            }

        # contains pelt pattern and color information
        # eyes, species, and special features come later
        pelt_description = ""
        final_description = ""
        color = sprites.pelt_colors["colors"][cat.pelt.color]["allegiances"]
        pattern = pattern_des[cat.pelt.pattern.lower()]
        tortie_color = ""
        tortie_pattern = ""
        tortie_type = ""
        colorpoint = ""
        merle = ""
        white_patch = ""

        species = cat.pelt.species.lower()
        eyes = ""

        if cat.pelt.eye_color2:
            temp_eye = Pelt.eye_info[cat.pelt.eye_color2]["allegiances"]
            eyes = Pelt.eye_info[cat.pelt.eye_color]["allegiances"] + " and " + temp_eye + " eyes"
        else:
            eyes = Pelt.eye_info[cat.pelt.eye_color]["allegiances"] + " eyes"

        if cat.pelt.white_patches:
            if cat.pelt.white_patches in white_ticking:
                white_patch += "ticked "
            if cat.pelt.white_patches in white_special:
                white_patch += white_special[cat.pelt.white_patches]
            elif cat.pelt.white_patches in white_minimal:
                white_patch += "minimal white"
            elif cat.pelt.white_patches in white_blaze:
                white_patch += "white blaze"
            elif cat.pelt.white_patches in white_irish:
                white_patch += "irish white"
            elif cat.pelt.white_patches in white_piebald:
                white_patch += "piebald"
            elif cat.pelt.white_patches in white_extreme_piebald:
                white_patch += "extreme piebald"

        if cat.pelt.tortie:
            tortie_color = sprites.pelt_colors["colors"][cat.pelt.tortiecolor]["allegiances"]
            tortie_pattern = pattern_des[cat.pelt.tortiepattern.lower()]
            if cat.pelt.white_patches:
                if cat.pelt.white_patches in Pelt.low_white:
                    tortie_type = "tortie"
                else:
                    tortie_type = "calico"
            else:
                tortie_type = "tortie"
        if cat.pelt.points:
            if cat.pelt.points == "SEPIA":
                colorpoint = "sepiapoint"
            elif cat.pelt.points == "MINK":
                colorpoint = "minkpoint"
            elif cat.pelt.points == "POINT":
                colorpoint = "graypoint"
            elif cat.pelt.points == "CLEAR":
                colorpoint = "clearpoint"
            elif cat.pelt.points == "HIMALAYAN":
                colorpoint = "himalayan"
        if cat.pelt.merle:
            merle_color = sprites.pelt_colors["merles"][cat.pelt.merle[1]]["display"]
            if cat.pelt.harlequin:
                merle = merle_color + " harlequin"
            else:
                merle = merle_color + " merle"
            if sprites.pelt_colors["colors"][cat.pelt.color]["blackpelt"]:
                color = ""
                pattern = ""
            if cat.pelt.tortie and sprites.pelt_colors["colors"][cat.pelt.tortiecolor]["blackpelt"]:
                tortie_color = ""
                tortie_pattern = ""
        if cat.pelt.pattern == "Points":
            color = sprites.pelt_colors["colors"][cat.pelt.color]["pointsdisplay"]
            if tortie and tortie_pattern == "Points":
                tortie_color = sprites.pelt_colors["colors"][cat.pelt.tortiecolor]["pointsdisplay"]
        if cat.pelt.points == "BEW":
            # should only be patterns and white patches. colors are obscured
            color = "ghost"
            if tortie_color:
                tortie_color = "ghost"
            if merle:
                if cat.pelt.harlequin:
                    merle = "harlequin"
                else:
                    merle = "merle" 

        with_used = False # this dictates if the next added word is 'and'
        if cat.pelt.points == "ALBINO":
            pelt_description = "albino"
        elif cat.pelt.white_patches == "WHITE":
            pelt_description = "solid white"
        else:
            if cat.pelt.tortie:
                if tortie_color == color:
                    tortie_color = ""
                if tortie_pattern == pattern:
                    tortie_pattern = ""
                elif "agouti" in tortie_pattern and "agouti" in pattern:
                    tortie_pattern.replace("agouti", "").replace(" ", "")
                    if tortie_pattern:
                        pattern = tortie_pattern + ", " + pattern
            if merle:
                pelt_description += merle + " "
            print(pelt_description)
            if cat.pelt.tortie:
                if tortie_color and not tortie_pattern:
                    pelt_description += color + " and " + tortie_color + " " + pattern + " " + tortie_type
                elif tortie_color:
                    pelt_description += color + ", " + tortie_color + " " + pattern + " and " + tortie_pattern + " " + tortie_type
                elif not tortie_color and not tortie_pattern:
                    pelt_description += color + " " + pattern + " " + tortie_type
                print(pelt_description)
            else:
                pelt_description += color + " " + pattern
            if colorpoint:
                pelt_description += " " + colorpoint
            if white_patch:
                pelt_description += " with " + white_patch
                with_used = True
            pelt_description.replace("  ", " ").replace("   ", " ")
            print(pelt_description)

        final_description = pelt_description + " " + cat.pelt.species.lower()
        
        if with_used:
            if cat.pelt.eye_color2:
                eyes.replace(" and ", ", ")
            final_description += " and " + eyes
        else:
            final_description += " with " + eyes
        print(pelt_description)

        final_description.replace("  ", " ").replace("   ", " ")    
        color_name = final_description

        return color_name

    def get_sprites_name(self):
        return Pelt.sprites_names[self.name]
