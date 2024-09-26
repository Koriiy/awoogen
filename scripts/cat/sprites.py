import os
from copy import copy

import pygame
import ujson

from scripts.game_structure.game_essentials import game


class Sprites:
    cat_tints = {}
    white_patches_tints = {}
    clan_symbols = []

    def __init__(self):
        """Class that handles and hold all spritesheets. 
        Size is normally automatically determined by the size
        of the lineart. If a size is passed, it will override 
        this value. """
        self.symbol_dict = None
        self.size = None
        self.spritesheets = {}
        self.images = {}
        self.sprites = {}

        # Shared empty sprite for placeholders
        self.blank_sprite = None

        self.load_tints()

    def load_tints(self):
        try:
            with open("sprites/dicts/tint.json", 'r') as read_file:
                self.cat_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading Tints")

        try:
            with open("sprites/dicts/white_patches_tint.json", 'r') as read_file:
                self.white_patches_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading White Patches Tints")

    def spritesheet(self, a_file, name):
        """
        Add spritesheet called name from a_file.

        Parameters:
        a_file -- Path to the file to create a spritesheet from.
        name -- Name to call the new spritesheet.
        """
        self.spritesheets[name] = pygame.image.load(a_file).convert_alpha()

    def make_group(self,
                   spritesheet,
                   pos,
                   name,
                   sprites_x=3,
                   sprites_y=7,
                   no_index=False):  # pos = ex. (2, 3), no single pixels

        """
        Divide sprites on a spritesheet into groups of sprites that are easily accessible
        :param spritesheet: Name of spritesheet file
        :param pos: (x,y) tuple of offsets. NOT pixel offset, but offset of other sprites
        :param name: Name of group being made
        :param sprites_x: default 3, number of sprites horizontally
        :param sprites_y: default 3, number of sprites vertically
        :param no_index: default False, set True if sprite name does not require cat pose index
        """

        # KORI - replace spritesheet checks once this bug is fixed
        if spritesheet == 'symbols':
            group_x_ofs = pos[0] * sprites_x * 50
            group_y_ofs = pos[1] * sprites_y * 50
        else:
            group_x_ofs = pos[0] * sprites_x * self.size
            group_y_ofs = pos[1] * sprites_y * self.size
        i = 0

        # splitting group into singular sprites and storing into self.sprites section
        for y in range(sprites_y):
            for x in range(sprites_x):
                if no_index:
                    full_name = f"{name}"
                else:
                    full_name = f"{name}{i}"

                try:
                    if spritesheet == 'symbols':
                        new_sprite = pygame.Surface.subsurface(
                            self.spritesheets[spritesheet],
                            group_x_ofs + x * 50,
                            group_y_ofs + y * 50,
                            50, 50
                        )
                    else:   
                        new_sprite = pygame.Surface.subsurface(
                            self.spritesheets[spritesheet],
                            group_x_ofs + x * self.size,
                            group_y_ofs + y * self.size,
                            self.size, self.size
                        )

                except ValueError:
                    # Fallback for non-existent sprites
                    print(f"WARNING: nonexistent sprite - {full_name}")
                    if not self.blank_sprite:
                        self.blank_sprite = pygame.Surface(
                            (self.size, self.size),
                            pygame.HWSURFACE | pygame.SRCALPHA
                        )
                    new_sprite = self.blank_sprite

                self.sprites[full_name] = new_sprite
                i += 1

    def load_all(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load('sprites/lineart.png')
        width, height = lineart.get_size()
        del lineart  # unneeded

        # if anyone changes lineart for whatever reason update this
        if isinstance(self.size, int):
            pass
        elif width / 3 == height / 7:
            self.size = width / 3
        else:
            self.size = 50 # default, what base clangen uses
            print(f"lineart.png is not 3x7, falling back to {self.size}")
            print(f"if you are a modder, please update scripts/cat/sprites.py and "
                  f"do a search for 'if width / 3 == height / 7:'")

        del width, height  # unneeded

        for x in [
            'lineart',
            'base', 'basetail', 'dark', 'darkears', 'darkfade', 'darkforest', 'darktail',
            'extras', 'eyes', 'fadebg', 'herbs', 'highlights', 
            'highlightsears', 'highlightstail', 'koriacc', 'lines',
	'lineears', 'linetail', 'merle', 'merleears', 'merletail', 'mouth',
            'petacc', 'petaccbase', 'petaccmissing', 
            'petaccpatterns', 'points', 'pointsears', 'pointstail', 'red', 'redears', 'redtail',
            'scars', 'scarsmissing', 'shading', 'skin', 'starfade', 'starfog', 'tortieears',
            'torties', 'tortietail', 'white', 'whiteears', 'whitetail', 'wild',
            'symbols'

        ]:
            if 'lineart' in x and game.config['fun']['april_fools']:
                self.spritesheet(f"sprites/aprilfools{x}.png", x)
            else:
                self.spritesheet(f"sprites/{x}.png", x)

        # Line art
        self.make_group('lineart', (0, 0), 'lines')
        self.make_group('shadersnewwhite', (0, 0), 'shaders')
        self.make_group('lightingnew', (0, 0), 'lighting')

        self.make_group('lineartdead', (0, 0), 'lineartdead')
        self.make_group('lineartdf', (0, 0), 'lineartdf')

        # Fading Fog
        for i in range(0, 3):
            self.make_group('fademask', (i, 0), f'fademask{i}')
            self.make_group('fadestarclan', (i, 0), f'fadestarclan{i}')
            self.make_group('fadedarkforest', (i, 0), f'fadedf{i}')

        # Eyes
        eye_colors = [['ICE', 'NAVY', 'RAIN', 'SAPPHIRE', 'SEAFOAM', 'SKY', 'STORM', 'TEAL'],
            ['ALMOND', 'BEAR', 'CASHEW', 'HAZEL', 'LATTE', 'SPARROW', 'BLACK', 'GULL'],
            ['SILVER', 'SMOKE', 'WHITE', 'EMERALD', 'FERN', 'FOREST', 'LEAF', 'LIME'],
            ['MINT', 'PEACH', 'PUMPKIN', 'TANGELO', 'AMETHYST', 'LILAC', 'BUBBLEGUM', 'PINK'],
            ['ROUGE', 'SCARLET', 'AMBER', 'LEMON', 'PALE', 'SUNBEAM', 'SUNLIGHT', 'WHEAT'],
            ['HARVEST', 'VIOLET', 'RUBY', 'DAWN', 'DAYLIGHT', 'TWILIGHT', 'DUSK', 'MIDNIGHT']]
        for row, colors in enumerate(eye_colors):
            for col, color in enumerate(colors):
                self.make_group('eyes', (col, row), f'eyes{color}')
                self.make_group('eyes2', (col, row), f'eyes2{color}')

        # White Patches
        white_patches = [['FLASH', 'HIGHLIGHTS', 'JACKAL', 'LOCKET', 'SNOWFLAKE', 'SOCKS', 'SPLIT', 'STRIPE', 'TOES', 'TRIM'],
            ['WOLFTICKING', 'BLAZE', 'BLOTCH', 'HALF', 'HEART', 'IRISH', 'MOONRISE', 'MUNSTERLANDER', 'SPITZ', 'STAR'],
            ['SUMMERFOX', 'TICKING', 'URAJIRO', 'BLUETICK', 'EXTREMEPIEBALD', 'LIGHTDALMATIAN', 'PIEBALD', 'TAIL', 'WHITE', 'HEAVYDALMATIAN'],
            ['BACKLEG', 'BEE', 'DAPPLES', 'POINTED', 'SPECKLES', 'DIAMOND', 'HOUND', 'KING', 'HEELER']]
        for row, patches in enumerate(white_patches):
            for col, patch in enumerate(patches):
                self.make_group('whitepatches', (col, row), f'white{patch}')

        # Colorpoints
        special_points = [['SEPIA', 'MINK', 'POINT', 'CLEAR'],
            ['HIMALAYAN', 'BEW', 'ALBINO']]
        for row, specialpoints in enumerate(special_points):
            for col, point in enumerate(specialpoints):
                self.make_group('specialpoints', (col, row), f'specialpoint{point}')

        # Merles
        for a, i in enumerate(['DARKDAPPLE', 'SHADOWSNEAK', 'STORMSONG', 'BRINDLECLOUD', 'DAPPLEPELT', 'DAYSKY', 'WILLOWLEAF', 'BRIGHTLEAF', 'SEAFUR', 'SILVERCLAW']):
            self.make_group('merle', (a, 0), f'patch{i}')
        
        # base pelt - to be expanded with extras later
        self.make_group('base', (0, 0), 'baseSOLID')

        # Red Highlights
        red_highlights = [['RUNIC', 'OPHELIA', 'MEXICAN', 'GRAYWOLF', 'TIMBER', 'VIBRANT', 'STORMY'],
            ['ASPEN', 'CALI', 'FOXY']]
        for row, redhighlight in enumerate(red_highlights):
            for col, rh in enumerate(redhighlight):
                self.make_group('red', (col, row), f'red{rh}')

        # Highlights
        highlights = [['RUNIC', 'RUNICBRIGHT', 'OPHELIA', 'MEXICAN', 'GRAYWOLF', 'TIMBER', 'VIBRANT'],
            ['STORMY', 'SMOKEY', 'WINTER', 'HUSKY', 'SHEPHERD', 'SABLE', 'ARCTIC'],
            ['SEMISOLID', 'AGOUTI', 'ASPEN', 'CALI', 'FOXY', 'GRIZZLE', 'SVALBARD']]
        for row, highlight in enumerate(highlights):
            for col, hl in enumerate(highlight):
                self.make_group('highlights', (col, row), f'highlight{hl}')

        # Dark Shading
        dark_shading = [['BLACK', 'RUNIC', 'OPHELIA', 'MEXICAN', 'GRAYWOLF', 'TIMBER', 'VIBRANT'],
            ['STORMY', 'SMOKEY', 'WINTER', 'HUSKY', 'SHEPHERD', 'SABLE', 'ARCTIC'],
            ['COLORPOINT', 'BRINDLE', 'POINTS', 'SEMISOLID', 'SOLID', 'AGOUTI', 'ASPEN'],
            ['CALI', 'FOXY', 'GRIZZLE', 'SVALBARD']]
        for row, darkshading in enumerate(dark_shading):
            for col, ds in enumerate(darkshading):
                self.make_group('dark', (col, row), f'dark{ds}')

        # Torties
        tortie_patches = [['CAPE', 'DIPPED', 'HEARTBREAKER', 'INKSPILL', 'MINIMAL', 'PHANTOM'],
            ['PUDDLES', 'REDTAIL', 'SHADOWSTEP', 'SPLIT', 'SPLOTCH', 'WATERFALL']]
        for row, tortiepatches in enumerate(tortie_patches):
            for col, tp in enumerate(tortiepatches):
                self.make_group('tortiepatchesmasks', (col, row), f'patch{tp}')

        # Skins
        skin_colors = [['BLACK', 'BLUE', 'BUTTERFLY', 'DUDLEY', 'DUDLEYBLUE', 'DUDLEYLIVER'],
            ['GRAY', 'ISABELLA', 'LIVER', 'MOCHA', 'PINK', 'SNOWNOSE'],
            ['SPECKLED']]
        for row, colors in enumerate(skin_colors):
            for col, color in enumerate(colors):
                self.make_group('skin', (col, row), f"skin{color}")

        self.load_scars()
        self.load_symbols()

    def load_scars(self):
        """
        Loads scar sprites and puts them into groups.
        """
        scars_data = [["BEAKLOWER", "BEAKCHEEK", "BELLY", "BLIND", "BOTHBLIND", "BRIDGE", 
            "BRIGHTHEART", "BURNPAWS", "BURNRUMP", "BURNBELLY", "BURNTAIL", "CATBITE"],
            ["CHEEK", "FACE", "FROSTFACE", "FROSTMITT", "FROSTSOCK", "FROSTTAIL",
            "HALFTAIL", "LEFTBLIND", "LEFTEAR", "LEGBITE", "MANTAIL", "MANLEG"],
            ["NECKBITE", "NOEAR", "NOLEFTEAR", "NOPAW", "NORIGHTEAR", "NOTAIL", "ONE",
            "QUILLCHUNK", "QUILLSCRATCH", "RATBITE", "RIGHTBLIND", "RIGHTEAR"],
            ["SIDE", "SNAKE", "SNOUT", "TAILBASE", "TAILSCAR", "THREE", "THROAT", "TOETRAP",
            "TWO", "GIN", "HINDLEG", "BACK"],
            ["QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR"]]
        missing_parts_data = [["BRIGHTHEART", "BURNBELLY", "BURNTAIL", "FROSTTAIL", "HALFTAIL", "LEFTEAR"],
                              ["NOEAR", "NOLEFTEAR", "NOPAW", "NORIGHTEAR", "NOTAIL", "RIGHTEAR"]]
        for row, scars in enumerate(scars_data):
            for col, scar in enumerate(scars):
                self.make_group('scars', (col, row), f'scars{scar}')
        for row, missing_parts in enumerate(missing_parts_data):
            for col, missing_part in enumerate(missing_parts):
                self.make_group('missingscars', (col, row), f'scarsmissing{missing_part}')

        # Accessories
        # Natural stuff
        herb_data = [["MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS",
            "RYE STALK", "CATTAIL", "POPPY", "ORANGE POPPY", "CYAN POPPY",
            "WHITE POPPY", "PINK POPPY"],
            ["BLUEBELLS", "LILY OF THE VALLEY", "SNAPDRAGON", "HERBS", "PETALS",
            "NETTLE", "HEATHER", "GORSE", "JUNIPER", "RASPBERRY", "LAVENDER"],
            ["OAK LEAVES", "CATMINT", "MAPLE SEED", "LAUREL", "BULB WHITE",
            "BULB YELLOW", "BULB ORANGE", "BULB PINK", "BULB BLUE", "CLOVER", "DAISY"],
            ["DRY HERBS", "DRY CATMINT", "DRY NETTLES", "DRY LAURELS"]]
        wild_data = [["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "GULL FEATHERS",
            "SPARROW FEATHERS", "MOTH WINGS", "ROSY MOTH WINGS",
            "MORPHO BUTTERFLY", "MONARCH BUTTERFLY", "CICADA WINGS",
            "BLACK CICADA"]]
        kori_data = [["BLACK EYED SUSANS", "CROW FEATHERS", "DOVE FEATHERS",
            "GOLD HERBS", "IVY", "MARIGOLD", "PURPLE PETALS", "ROSE", "SAKURA",
            "SUNFLOWER"],
            ["WHITE ROSE", "HIBISCUS", "RED HIBISCUS", "WHITE HIBISCUS", "STARFISH",
             "PINK STARFISH", "PURPLE STARFISH", "PEARLS", "SEASHELLS", "BIG LEAVES"]]

        for row, herbs in enumerate(herb_data):
            for col, herb in enumerate(herbs):
                self.make_group('herbs', (col, row), f'natural{herb}')
        for row, wilds in enumerate(wild_data):
            for col, wild in enumerate(wilds):
                self.make_group('wild', (col, 0), f'natural{wild}')
        for row, moreaccs in enumerate(kori_data):
            for col, moreacc in enumerate(moreaccs):
                self.make_group('koriacc', (col, 0), f'natural{moreacc}')
                
        self.make_group('extras', (0, 0), f'junkTOWEL')
        self.make_group('extras', (1, 0), f'cloakSILK CLOAK')

        # Collars, Harnesses, Bandanas
        collar_color_data = [["BLACK", "BLUE", "CRIMSON", "CYAN", "GREEN"],
            ["INDIGO", "LIME", "MULTI", "PINK", "PURPLE"],
            ["RAINBOW", "RED", "SPIKES", "WHITE", "YELLOW"]]
        for row, collars in enumerate(collar_color_data):
            for col, color in enumerate(collars):
                self.make_group('collars', (col, row), f'collars{color}')
                self.make_group('bellcollars', (col, row), f'collarsBELL{color}')
                self.make_group('bowcollars', (col, row), f'collarsBOW{color}')
                self.make_group('nyloncollars', (col, row), f'collarsNYLON{color}')
                self.make_group('nylonpastelcollars', (col, row), f'collarsPASTELNYLON{color}')
                self.make_group('radio', (col, row), f'collarsRADIO{color}')
                self.make_group('harness', (col, row), f'collarsHARNESS{color}')
                self.make_group('bandana', (col, row), f'collarsBANDANA{color}')
                self.make_group('bandanaplaid', (col, row), f'collarsPLAIDBANDANA{color}')

    def load_symbols(self):
        """
        loads clan symbols
        """

        if os.path.exists('resources/dicts/clan_symbols.json'):
            with open('resources/dicts/clan_symbols.json') as read_file:
                self.symbol_dict = ujson.loads(read_file.read())

        # U and X omitted from letter list due to having no prefixes
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "V", "W", "Y", "Z"]

        # sprite names will format as "symbol{PREFIX}{INDEX}", ex. "symbolSPRING0"
        y_pos = 1
        for letter in letters:
            for i, symbol in enumerate([symbol for symbol in self.symbol_dict if
                                        letter in symbol and self.symbol_dict[symbol]["variants"]]):
                x_mod = 0
                for variant_index in range(self.symbol_dict[symbol]["variants"]):
                    x_mod += variant_index
                    self.clan_symbols.append(f"symbol{symbol.upper()}{variant_index}")
                    self.make_group('symbols',
                                    (i + x_mod, y_pos),
                                    f"symbol{symbol.upper()}{variant_index}",
                                    sprites_x=1, sprites_y=1, no_index=True)

            y_pos += 1

    def dark_mode_symbol(self, symbol, color):
        """Change the color of the symbol to dark mode, then return it
        :param Surface symbol: The clan symbol to convert"""
        dark_mode_symbol = copy(symbol)
        var = pygame.PixelArray(dark_mode_symbol)
        var.replace((255, 255, 255), color)
        del var
        # dark mode color (239, 229, 206)
        # debug hot pink (255, 105, 180)

        return dark_mode_symbol

# CREATE INSTANCE
sprites = Sprites()
