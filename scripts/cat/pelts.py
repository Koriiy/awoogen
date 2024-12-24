import random
from random import choice
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
        if self.points == "BEW" or self.points == "ALBINO":
            if self.points == "BEW":
                self.eye_color = random.choice(sprites.pelt_generation["points_eyes"]["BEW"])
                return
            if self.points == "ALBINO":
                self.eye_color = random.choice(sprites.pelt_generation["points_eyes"]["ALBINO"])
                return
        if not parents:
            temp_eye_category = random.choices(Pelt.eye_categories, weights=sprites.pelt_generation["random_eye_colors"]["categories"], k=1)[0]
            self.eye_color = random.choice(sprites.pelt_generation["eye_colors"][temp_eye_category])
        else:
            par_eye_colors = []
            color_base_p = ""
            for p in parents:
                par_eye_colors.append(p.pelt.eye_color)
            if len(par_eye_colors) <= 1:
                if par_eye_colors[0] == None:
                    color_base_p = par_eye_colors[1]
                else:
                    color_base_p = par_eye_colors[0]
            else:
                color_base_p = random.choice(par_eye_colors)

            for color in Pelt.eye_categories:
                if color_base_p in Pelt.eye_colors[color]:
                    temp_weights = sprites.pelt_generation["parent_eye_colors"][color_base_p]
                    temp_eye_category = random.choices(Pelt.eye_categories, weights=temp_weights, k=1)[0]
                    self.eye_color = random.choice(sprites.pelt_generation["eye_colors"][temp_eye_category])
                    break
                  
        #heterochromia stuff
        het_chance = sprites.pelt_generation["heterochromia_chance"]
        num = het_chance["base"]
        if self.white_patches in Pelt.high_white:
            num -= het_chance["high_white"]
        if self.white_patches in Pelt.mid_white:
            num -= het_chance["mid_white"]
        if self.white_patches == 'WHITE':
            num -= 10
        if self.merle:
            num -= het_chance["merle"]
        if self.points != None:
            num -= het_chance["points"]
        for p in parents:
            if p.pelt.eye_color2:
                num -= het_chance["parent"]

        if num < 0:
            num = 1

        if not random.randint(0, num):
            for color in Pelt.eye_categories:
                if self.eye_color in Pelt.eye_colors[color]:
                    self.eye_color2 = random.choice(Pelt.eye_colors[random.choice(sprites.pelt_generation["heterochromia_pairing"][color])])
                    break

    def pattern_color_inheritance(self, parents: tuple = (), gender="female"):
        # setting parent pelt categories
        #We are using a set, since we don't need this to be ordered, and sets deal with removing duplicates.
        colorpoint_genes = Pelt.point_genes # this is here for easy access
        parents_length = set()
        parents_color = set()
        parents_direct_inheritance = []
        parents_pelt = []
        parents_white = []
        parents_species_mix = []
        parents_merle = []
        parents_harlequin = []
        parents_points_genes = []
        temp_parent = [["W", "W", "W", "W", "W", "W"], ["C", "C", "C", "C", "C", "C"], ["D", "D", "D", "D", "D", "D"], ["W", "C", "W", "C", "W", "W"], ["W", "W", "W", "W", "W", "W"]]

        if len(parents) == 2:
            for p in parents:
                parents_direct_inheritance.append(p.pelt)
                parents_length.add(p.pelt.length)
                parents_color.add(p.pelt.color)
                if p.pelt.name == 'Tortie' or p.pelt.name == 'Calico':
                    parents_pelt.append(p.pelt.tortiebase.capitalize())
                else:
                    parents_pelt.append(p.pelt.name)
                parents_white.append(p.pelt.white)
                parents_merle.append(p.pelt.merle)
                parents_harlequin.append(p.pelt.harlequin)
                parents_points_genes.append(p.pelt.points_genes)
                parents_species_mix.append(p.pelt.species_mix)
        else:
            for p in parents:
                parents_direct_inheritance.append(p.pelt)
                parents_length.add(p.pelt.length)
                parents_color.add(p.pelt.color)
                if p.pelt.name == 'Tortie' or p.pelt.name == 'Calico':
                    parents_pelt.append(p.pelt.tortiebase.capitalize())
                else:
                    parents_pelt.append(p.pelt.name)
                parents_white.append(p.pelt.white)
                parents_merle.append(p.pelt.merle)
                parents_harlequin.append(p.pelt.harlequin)
                parents_points_genes.append(p.pelt.points_genes)
                parents_species_mix.append(p.pelt.species_mix)
            if random.randint(0, 100) <= 20:
                parents_merle.append(True)
            else:
                parents_merle.append(False)
            if random.randint(0, 100) <= 8:
                parents_harlequin.append(True)
            else:
                parents_harlequin.append(False)
            parents_points_genes.append(random.choices(colorpoint_genes, weights=[115, 35, 20, 15, 10, 5], k=1)[0])
            parents_species_mix.append(random.choice(temp_parent))
            
        chosen_species_mix = []
        chosen_species = "Wolf"
        
        for g in range(0, 6):
            gene_choice = []
            for p in parents_species_mix:
                gene_choice.append(p[g])
            chosen_species_mix.append(random.choice(gene_choice))
            
        if "C" not in chosen_species_mix and "D" not in chosen_species_mix:
            chosen_species = "Wolf"
        elif "D" not in chosen_species_mix and "W" not in chosen_species_mix:
            chosen_species = "Coyote"
        else:
            wolf = chosen_species_mix.count("W")
            yote = chosen_species_mix.count("C")
            dog = chosen_species_mix.count("D")
            if dog == 0:
                chosen_species = "Coywolf"
            elif yote == 0:
                chosen_species = "Wolfdog"
            elif wolf == 0:
                chosen_species = "Coydog"
            elif wolf >= 3:
                chosen_species = "Wolf Hybrid"
            elif yote >= 3:
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
            self.color = selected.color
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
                add_weight = sprites.pelt_generation["parent_pelt_patterns"]["standardpelts"]
            elif i in Pelt.northpelts:
                add_weight = sprites.pelt_generation["parent_pelt_patterns"]["northpelts"]
            elif i in Pelt.southpelts:
                add_weight = sprites.pelt_generation["parent_pelt_patterns"]["southpelts"]
            elif i in Pelt.darkpelts:
                add_weight = sprites.pelt_generation["parent_pelt_patterns"]["darkpelts"]
            elif i in Pelt.specialpelts:
                add_weight = sprites.pelt_generation["parent_pelt_patterns"]["specialpelts"]
            elif i is None:
                add_weight = sprites.pelt_generation["random_pelt_patterns"]["pelt_categories"]
                add_weight = add_weight[:-1]
            else:
                add_weight = sprites.pelt_generation["random_pelt_patterns"]["pelt_categories"]
                add_weight = add_weight[:-1]

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

        chosen_pelt = ""
        temp_chosen_pelt = random.choices(Pelt.pelt_categories, weights=weights + [0], k = 1)
        if temp_chosen_pelt == "standardpelts":
            chosen_pelt = random.choices(Pelt.standardpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["standardpelts"], k = 1)[0]
        elif temp_chosen_pelt == "northpelts":
            chosen_pelt = random.choices (Pelt.northpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["northpelts"], k = 1)[0]
        elif temp_chosen_pelt == "southpelts":
            chosen_pelt = random.choices(Pelt.southpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["southpelts"], k = 1)[0]
        elif temp_chosen_pelt == "darkpelts":
            chosen_pelt = random.choices(Pelt.darkpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["darkpelts"], k = 1)[0]
        elif temp_chosen_pelt == "specialpelts":
            chosen_pelt = random.choices(Pelt.specialpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["specialpelts"], k = 1)[0]

        # Tortie chance
        tortie_chance_f = game.config["cat_generation"]["base_female_tortie"]
        tortie_chance_m = game.config["cat_generation"]["base_male_tortie"]
        if gender == "female":
            torbie = random.getrandbits(tortie_chance_f) == 1
        else:
            torbie = random.getrandbits(tortie_chance_m) == 1

        chosen_tortie_pattern = None
        if torbie:
            chosen_tortie_pattern = random.choice(Pelt.tortiepatterns)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT color
        # ------------------------------------------------------------------------------------------------------------#
        # Weights for each color group
        # yellow_colors, gray_colors, black_colors, red_colors, dilute_colors
        # unless you heathens changed it. then you're on your own
        weights = []
        for n in Pelt.pelt_color_categories:
            weights.append(0)
            
        for i in parents_color:
            if i is None:
                add_weight = sprites.pelt_generation["random_pelt_colors"]["color_categories"]
            else:
                for x in pelt_colors:
                    if i in pelt_colors[x]:
                        add_weight = sprites.pelt_generation["parent_pelt_colors"][x]
                        break
            for x in range(0, len(weights)):
                weights[x] += add_weight[x]
                
        chosen_pelt_color = ""
        temp_chosen_pelt_color = random.choices(Pelt.pelt_color_categories, weights=weights, k=1)[0]
        chosen_pelt_color = random.choices(pelt_colors[temp_chosen_pelt_color], weights=sprites.pelt_generation["random_pelt_colors"][temp_chosen_pelt_color], k=1)[0]
        
        # ------------------------------------------------------------------------------------------------------------#
        #   PELT LENGTH
        # ------------------------------------------------------------------------------------------------------------#

        weights = [0, 0, 0]  # Weights for each length. It goes (short, medium, long)
        for i in parents_length:
            if i == "short":
                add_weight = (50, 30, 20)
            elif i == "medium":
                add_weight = (20, 60, 20)
            elif i == "long":
                add_weight = (10, 30, 60)
            elif i is None:
                add_weight = (10, 50, 10)
            else:
                add_weight = (10, 50, 10)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

        chosen_pelt_length = random.choices(Pelt.pelt_length, weights=weights, k=1)[0]
        
        # ------------------------------------------------------------------------------------------------------------#
        #   MERLE AND HARLEQUIN
        # ------------------------------------------------------------------------------------------------------------#
        merle_bool = False
        harlequin_bool = None
        chosen_merle_pattern = None
        merle_colors = sprites.pelt_colors["merles"]
                
        #basically if either or both parents are merle the pup will have a 50/50 chance to be that as well
        for m in parents_merle:
            if m:
                if random.randint(0, 1) == 0:
                    merle_bool = True
                else:
                    merle_bool = False
                break
        for h in parents_harlequin:
            if h:
                if random.randint(0, 1) == 0:
                    harlequin_bool = True
                else:
                    harlequin_bool = False
                break

        # only calculate merle info if merle
        if merle_bool:
            chosen_merle_pattern = []
            merle_category = sprites.pelt_colors["colors"][chosen_pelt_color]["merle"]
            chosen_merle_pattern.append(random.choice(Pelt.merles))
            chosen_merle_pattern.append(merle_category)
            random_merle_color = []
            for m in merle_colors[merle_category]:
                random_merle_color.append(m)
            chosen_merle_pattern.append(random.choice(random_merle_color[1:]))
        
        # ------------------------------------------------------------------------------------------------------------#
        #   COLORPOINT (NEW)
        # ------------------------------------------------------------------------------------------------------------#
        chosen_points_genes = ["", ""]
        points_outcome = ""
        colorpoint_types = Pelt.point_markings
        possible_colorpoint = [[], []]

        for c in parents_point_genes:
            possible_colorpoint[0].append(c[0])
            possible_colorpoint[1].append(c[1])
        chosen_points_genes[0] = random.choice(possible_colorpoint[0])
        chosen_points_genes[1] = random.choice(possible_colorpoint[1])

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

        # SET THE PELT
        self.pattern = chosen_pelt
        self.color = chosen_pelt_color
        self.length = chosen_pelt_length
        self.tortie = chosen_tortie_pattern   # This will be none if the cat isn't a tortie.
        self.points_genes = chosen_points_genes
        self.points = points_outcome
        self.merle = chosen_merle_pattern
        self.harlequin = harlequin_possibility
        return chosen_white

    def randomize_pattern_color(self, gender):
        # ------------------------------------------------------------------------------------------------------------#
        #   PELT
        # ------------------------------------------------------------------------------------------------------------#

        # Determine pelt.
        chosen_pelt = ""
        temp_chosen_pelt = random.choices(Pelt.pelt_categories, weights=sprites.pelt_generation["random_pelt_patterns"]["pelt_categories"], k = 1)[0]
        if temp_chosen_pelt == "standardpelts":
            chosen_pelt = random.choices(Pelt.standardpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["standardpelts"], k = 1)[0]
        elif temp_chosen_pelt == "northpelts":
            chosen_pelt = random.choices (Pelt.northpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["northpelts"], k = 1)[0]
        elif temp_chosen_pelt == "southpelts":
            chosen_pelt = random.choices(Pelt.southpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["southpelts"], k = 1)[0]
        elif temp_chosen_pelt == "darkpelts":
            chosen_pelt = random.choices(Pelt.darkpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["darkpelts"], k = 1)[0]
        elif temp_chosen_pelt == "specialpelts":
            chosen_pelt = random.choices(Pelt.specialpelts, weights=sprites.pelt_generation["random_pelt_patterns"]["specialpelts"], k = 1)[0]
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
            chosen_tortie_pattern = random.choice(Pelt.tortiepatterns)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT color
        # ------------------------------------------------------------------------------------------------------------#
        weights = []
        for n in Pelt.pelt_color_categories:
            weights.append(0)
        for i, w in enumerate(sprites.pelt_generation["random_pelt_colors"]["color_categories"]):
            weights[i] += w
            
        chosen_pelt_color = ""
        temp_chosen_pelt_color = random.choices(Pelt.pelt_color_categories, weights=weights, k=1)[0]
        chosen_pelt_color = random.choices(Pelt.pelt_colors[temp_chosen_pelt_color], weights=sprites.pelt_generation["random_pelt_colors"][temp_chosen_pelt_color], k=1)[0]

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
        species_grabber = random.randint(0, 10)
        if species_grabber <= 3:
            chosen_species_mix = random.choices(quick_genes, weights=(100, 20), k=1)[0]
        else:
            for i in range(0, 6):
                chosen_species_mix[i] = random.choices(poss_genes, weights=(400, 40, 10), k=1)[0]
        if "C" not in chosen_species_mix and "D" not in chosen_species_mix:
            chosen_species = "Wolf"
        elif "D" not in chosen_species_mix and "W" not in chosen_species_mix:
            chosen_species = "Coyote"
        else:
            wolf = chosen_species_mix.count("W")
            yote = chosen_species_mix.count("C")
            dog = chosen_species_mix.count("D")
            if dog == 0:
                chosen_species = "Coywolf"
            elif yote == 0:
                chosen_species = "Wolfdog"
            elif wolf == 0:
                chosen_species = "Coydog"
            elif wolf >= 3:
                chosen_species = "Wolf Hybrid"
            elif yote >= 3:
                chosen_species = "Coyote Hybrid"
            else:
                chosen_species = "Hybrid"
                
        # ------------------------------------------------------------------------------------------------------------#
        #   MERLE AND HARLEQUIN
        # ------------------------------------------------------------------------------------------------------------#
        merle_bool = False
        harlequin_possibility = None
        chosen_merle_pattern = None

        #find out if they're merle or harlequin at all
        temp_chance = random.randint(0, 100)
        if temp_chance <= sprites.pelt_generation["pelt_misc"]["merle"]:
            merle_bool = True
        temp_chance = random.randint(0, 100)
        if temp_chance <= sprites.pelt_generation["pelt_misc"]["harlequin"]:
            harlequin_possibility = True

        # only calculate merle info if merle
        if merle_bool:
            chosen_merle_pattern = []
            merle_category = sprites.pelt_colors["colors"][chosen_pelt_color]["merle"]
            chosen_merle_pattern.append(random.choice(Pelt.merles))
            chosen_merle_pattern.append(merle_category)
            random_merle_color = []
            for m in sprites.pelt_colors["merles"][merle_category]:
                random_merle_color.append(m)
            chosen_merle_pattern.append(random.choice(random_merle_color[1:]))

        # ------------------------------------------------------------------------------------------------------------#
        #   COLORPOINT (NEW)
        # ------------------------------------------------------------------------------------------------------------#
        chosen_points_genes = ["C", "C"]
        points_outcome = None
        colorpoint_types = Pelt.point_markings
        possible_colorpoint = [[], []]

        chosen_points_genes[0] = random.choices(Pelt.point_genes, weights=sprites.pelt_generation["pelt_misc"]["colorpoint_genes"], k=1)[0]
        chosen_points_genes[1] = random.choices(Pelt.point_genes, weights=sprites.pelt_generation["pelt_misc"]["colorpoint_genes"], k=1)[0]

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

        self.pattern = chosen_pelt
        self.color = chosen_pelt_color
        self.length = chosen_pelt_length
        self.tortie = chosen_tortie_base   # This will be none if the cat isn't a tortie.
        self.species_mix = chosen_species_mix
        self.species = chosen_species
        self.points_genes = chosen_points_genes
        self.points = points_outcome
        self.merle = chosen_merle_pattern
        self.harlequin = harlequin_possibility
        return chosen_white

    def init_pattern_color(self, parents, gender) -> bool:
        """Inits self.name, self.color, self.length, 
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
        skin_sprites = Pelt.skin_sprites.copy()
        low_white = Pelt.low_white.copy()
        mid_white = Pelt.mid_white.copy()
        high_white = Pelt.high_white.copy()
        temp_points = ['HIMALAYAN', 'BEW', 'ALBINO']
        possible_skins = [0, 0, 0, 0, 0]
        pink_solid = False
        merle_weights = [0, 0, 0, 0, 0]
        tortie_weights = [0, 0, 0, 0, 0]

        if self.points in temp_points:
            possible_skins = [100, 0, 0, 0, 0]
            pink_solid = True
        elif self.white_patches == None:
            if self.merle:
                possible_skins = [60, 20, 0, 0, 20]
            else:
                possible_skins = [90, 0, 0, 10, 0]
        else:
            if self.white_patches in high_white:
                possible_skins = [80, 10, 0, 0, 10]
                pink_solid = True
            elif self.white_patches in mid_white:
                possible_skins = [60, 10, 10, 10, 10]
            else:
                possible_skins = [80, 5, 10, 10, 5]   
            if self.merle:
                merle_weights = [0, 30, 0, 10, 20]
            if self.tortie:
                tortie_weights = [0, 10, 20, 20, 10]
        for i, x in enumerate(possible_skins):
            x += merle_weights[i]
            x += tortie_weights[i]
        skin_choice = random.choices(skin_sprites, weights=possible_skins, k=1)[0]
        self.skin = []
        self.skin.append(skin_choice)
        base_skin = sprites.pelt_colors["colors"][self.color]["skin"]
        base_skin_list = []
        for x in sprites.misc_colors["skins"][base_skin]:
            base_skin_list.append(x)
        pink_color = sprites.pelt_generation["pelt_misc"]["white_skin_category"]
        pink_color_list = []
        for x in sprites.misc_colors["skins"][pink_color]:
            pink_color_list.append(x)
        if skin_choice == "SOLID" and pink_solid:
            self.skin.append(pink_color)
            self.skin.append(random.choice(pink_color_list))
        else:
            if skin_choice == "SOLID":
                self.skin.append(base_skin)
                self.skin.append(random.choice(base_skin_list))
            else:
                self.skin.append(base_skin)
                self.skin.append(random.choice(base_skin_list))
                self.skin.append(pink_color)
                self.skin.append(random.choice(pink_color_list))

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
            self.accessory = ["", None, None]
            self.accessory[0] = choice([
                choice(Pelt.plant_accessories),
                choice(Pelt.wild_accessories)
            ])
        elif acc_display_choice in range(31, 45):
            self.accessory = ["RADIO", "SOLID", ""]
            self.accessory[2] = choice(Pelt.acc_potential_colors[random.choices(Pelt.pet_accessories_color_categories, weights=Pelt.acc_category_weights, k=1)[0]])
        elif acc_display_choice in range(46, 62):
            #collars
            self.accessory = ["", "SOLID", ""]
            possible_collars = ["BANDANA", "BANDANABACK", "BELL", "BOW", "COLLAR", "LEATHER", "NYLON"]
            collar_weights = [10, 5, 5, 5, 20, 20, 10]
            self.accessory[0] = random.choices(possible_collars, weights=collar_weights, k=1)[0]
            if self.accessory[0] in ["BANDANA", "BANDANABACK"] and random.randint(1, 3) == 3:
                self.accessory[1] = choice(Pelt.bandana_patterns)
            self.accessory[2] = choice(Pelt.acc_potential_colors[random.choices(Pelt.pet_accessories_color_categories, weights=Pelt.acc_category_weights, k=1)[0]])
        elif acc_display_choice in range(63, 71):
            self.accessory = ["HARNESS", "SOLID", ""]
            self.accessory[2] = choice(Pelt.acc_potential_colors[random.choices(Pelt.pet_accessories_color_categories, weights=Pelt.acc_category_weights, k=1)[0]])
        else:
            self.accessory = None

    def init_pattern(self):
        if self.tortie:
            possible_pelt_patterns = Pelt.tortiebases.copy()
            possible_pelt_colors = sprites.pelt_generation["tortie_combos"][self.color].copy()
            wildcard_chance = game.config["cat_generation"]["wildcard_tortie"]
            if not wildcard_chance or random.getrandbits(wildcard_chance) == 1:
                print("Wildcard tortie!")
                self.tortiepattern = random.choice(possible_pelt_patterns)
                possible_pelt_colors.remove(self.color)
                self.tortiecolor = random.choice(possible_pelt_colors)
            else:
                if rand.int(0, 10) <= 2:
                    self.tortiepattern = self.pattern.copy()
                else:
                    if rand.int(0, 2) == 1:
                        solid_pelts = ["SOLID", "SEMISOLID"]
                        self.tortiepattern = random.choice(solid_pelts)
                    else:
                        possible_pelt_patterns.remove(self.pattern)
                        self.tortiepattern = random.choice(possible_pelt_patterns)
                if rand.int(0, 10) == 10 and self.tortiepattern != self.pattern:
                    self.tortiecolor = self.color.copy()
                else:
                    self.tortiecolor = random.choice(possible_pelt_colors)
        else:
            self.tortiepattern = None
            self.tortiecolor = None
            
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
        if len(parents_white) != 0 and not random.randint(0, sprites.pelt_generation["pelt_misc"]["direct_inheritance"]):
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

        chosen_white_patches = random.choices(white_list, weights=weights, k=1)[0]
        chosen_white_patches = random.choice(chosen_white_patches)
        self.white_patches = chosen_white_patches

    def randomize_white_patches(self):
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
            if self.color in sprites.cat_tints["color_groups"]:
                color_group = sprites.cat_tints["color_groups"].get(self.color, "warm")
                color_tints = sprites.cat_tints["possible_tints"][color_group]
            else:
                color_tints = []
        
            if base_tints or color_tints:
                self.tint = choice(base_tints + color_tints)
            else:
                self.tint = None
        else:
            self.tint = None

        # WHITE PATCHES TINT
        if self.white_patches or self.points:
            if random.randint(0, 1) == 0:
                base_tints = sprites.white_patches_tints["possible_tints"]["basic"]
                if self.points == 'BEW' or self.points == 'ALBINO':
                    if self.points == 'BEW':
                        self.white_patches_tint == 'yellowwhite'
                    else:
                        self.white_patches_tint == None
                if self.color in sprites.cat_tints["color_groups"]:
                    color_group = sprites.white_patches_tints["color_groups"].get(self.color, "white")
                    color_tints = sprites.white_patches_tints["possible_tints"][color_group]
                else:
                    color_tints = []
            
                if base_tints or color_tints:
                    self.white_patches_tint = choice(base_tints + color_tints)
                else:
                    self.white_patches_tint = None
            else:
                self.white_patches_tint = None
        else:
            self.white_patches_tint = None

        # fixing
        if self.white_patches_tint == "darkblue" or self.white_patches_tint == "deepblue":
            if self.tint == "red" or self.tint == "orange" or self.tint == "pink":
                self.white_patches_tint = None
        elif self.white_patches_tint == "darkred" or self.white_patches_tint == "deepred":
            if self.tint == "blue" or self.tint == "purple" or self.tint == "gray":
                self.white_patches_tint == None

        if self.tint == "none":
            self.tint = None
        if self.white_patches_tint == "none":
            self.white_patches_tint = None
            

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
