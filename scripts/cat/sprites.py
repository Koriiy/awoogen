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
            'lines',
            'base', 'basetail', 'dark', 'darkears', 'darkfade', 'darkforest', 'darktail',
            'extras', 'eyes', 'fadebg', 'herbs', 'highlights', 
            'highlightsears', 'highlightstail', 'koriacc', 'lines',
	'linetail', 'merle', 'merleears', 'merletail', 'mouth',
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
        self.make_group('lines', (0, 0), 'lines')
        self.make_group('lineears', (0, 0), 'lineears')
        self.make_group('linetail', (0, 0), 'linetail')
        self.make_group('shaders', (0, 0), 'shaders')

        # base pelt - to be expanded with extras later
        self.make_group('base', (0, 0), 'baseSOLID')
        self.make_group('basetail', (0, 0), 'basetailSOLID')
        self.make_group('mouth', (0, 0), 'mouth')

        # dead stuff
        self.make_group('starfog', (0, 0), 'starfog')
        self.make_group('darkforest', (0, 0), 'darkforest')
        self.make_group('fadebg', (0, 0), 'fadebg')

        # Fading Fog
        for i in range(0, 3):
            self.make_group('starfade', (i, 0), f'starfade{i}')
            self.make_group('darkfade', (i, 0), f'darkfade{i}')

        # skin
        for a, i in enumerate([|"SOLID", "BUTTERFLY", "DUDLEY", "SNOWNOSE", "SPECKLED"]):
            self.make_group('skin', (a, 0), f'skin{i}')
        # eyes
        for a, i in enumerate(["SCLERA", "BASE", "HIGHLIGHT"]):
            self.make_group('eyes', (a, 0), f'eye{i}')

        # White Patches
        white_patches = [["BACKLEG", "BEE", "BLAZE", "BLOTCH", "BLUETICK", "DAPPLES", "DIAMOND", "EXTREMEPIEBALD", "FLASH", "HALF"],
            ["HEART", "HEAVYDALMATIAN", "HEELER", "HIGHLIGHT", "HOUND", "IRISH", "JACKAL", "KING", "LIGHTDALMATIAN", "LOCKET"],
            ["MOONRISE", "MUNSTERLANDER", "PIEBALD", "POINTED", "SNOWFLAKE", "SOCKS", "SPECKLES", "SPITZ", "SPLIT", "STAR"],
            ["STRIPE", "SUMMERFOX", "TAIL", "TICKING", "TOES", "TRIM", "URAJIRO", "WOLFTICKING"]]
        for row, patches in enumerate(white_patches):
            for col, patch in enumerate(patches):
                self.make_group('white', (col, row), f'white{patch}')
        for a, i in enumerate(["INNEREARS", "DAPPLES", "EXTREMEPIEBALD", "LIGHTDALMATIAN", "SNOWFLAKE", "SPLIT", "TAIL"]):
            self.make_group('whiteears', (a, 0), f'whiteears{i}')
        white_tails = [["UNDERTAIL", "SOLIDTAIL", "TIPTAIL", "SMALLTAIL", "HALFTAIL", "BEE", "BLUETICK", "DAPPLES"],
            ["DIAMOND", "HEART", "HEAVYDALMATIAN", "HEELER", "KING", "LIGHTDALMATIAN", "MUNSTERLANDER", "SNOWFLAKE"],
            ["SPECKLES", "SPITZ", "SPLIT", "STAR", "TICKING"]]
        for row, tails in enumerate(white_tails):
            for col, tail in enumerate(tails):
                self.make_group('whitetail', (col, row), f'whitetail{tail}')

        # Colorpoints
        for a, i in enumerate(["SEPIA", "MINK", "POINT", "CLEAR", "HIMALAYAN", "BEW"]):
            self.make_group('points', (a, 0), f'points{i}')
        for a, i in enumerate(["SOLID", "HIMALAYAN", "BEW"]):
            self.make_group('pointsears', (a, 0), f'pointsears{i}')
        for a, i in enumerate(["SOLID", "HIMALAYAN", "BEW"]):
            self.make_group('pointstail', (a, 0), f'pointstail{i}')
            
        # Merles
        merle_patches = [["BRIGHTLEAF", "BRINDLECLOUD", "DAPPLECLOUD", "DARKDAPPLE", "DAYSKY", "SEAFUR", "SHADOWSNEAK", "SILVERCLAW"],
                              ["STORMSONG", "WILLOWLEAF"]]
        for row, patches in enumerate(merle_patches):
            for col, patch in enumerate(patches):
                self.make_group('merle', (col, row), f'merle{patch}')
        for a, i in enumerate(["SOLID", "BRIGHTLEAF", "BRINDLECLOUD", "DAPPLECLOUD", "DARKDAPPLE", "DAYSKY", "SEAFUR", "SHADOWSNEAK"]):
            self.make_group('merleears', (a, 0), f'merleears{i}')
        merle_tails = [["BRIGHTLEAF", "BRINDLECLOUD", "DAPPLECLOUD", "DARKDAPPLE", "DAYSKY", "SEAFUR", "SHADOWSNEAK", "SILVERCLAW"],
                              ["STORMSONG", "WILLOWLEAF"]]
        for row, tails in enumerate(merle_tails):
            for col, tail in enumerate(tails):
                self.make_group('merletail', (col, row), f'merletail{tail}')
        
        # Red Highlights
        red_highlights = [["ASPEN", "CALI", "FOXY", "GRAYWOLF", "MEXICAN", "OPHELIA"],
            ["RUNIC", "STORMY", "TIMBER", "VIBRANT"]]
        for row, redhighlight in enumerate(red_highlights):
            for col, rh in enumerate(redhighlight):
                self.make_group('red', (col, row), f'red{rh}')
        for a, i in enumerate(["SOLID", "MOST", "ASPEN", "OPHELIA"]):
            self.make_group('redears', (a, 0), f'redears{i}')
        for a, i in enumerate(["MOST", "ASPEN", "CALI", "FOXY", "GRAYWOLF", "OPHELIA", "RUNIC", "STORMY"]):
            self.make_group('redtail', (a, 0), f'redtail{i}')

        # Highlights
        highlights = [["AGOUTI", "ARCTIC", "ASPEN", "CALI", "FOXY", "GRAYWOLF", "GRIZZLE", "HUSKY"],
            ["MEXICAN", "OPHELIA", "RUNICMID", "RUNIC", "SABLE", "SEMISOLID", "SHEPHERD", "SMOKEY"],
            ["STORMY", "SVALBARD", "TIMBER", "VIBRANT", "WINTER"]]
        for row, highlight in enumerate(highlights):
            for col, hl in enumerate(highlight):
                self.make_group('highlights', (col, row), f'highlight{hl}')
        for a, i in enumerate(["EXTRA", "INNER", "AGOUTI", "CALI", "OPHELIA", "SVALBARD"]):
            self.make_group('highlightsears', (a, 0), f'highlightears{i}')
        highlight_tails = [["AGOUTI", "ARCTIC", "ASPEN", "CALI", "FOXY", "GRIZZLE", "HUSKY", "MEXICAN"],
                              ["SEMISOLID", "SHEPHERD", "SVALBARD"]]
        for row, tails in enumerate(highlight_tails):
            for col, tail in enumerate(tails):
                self.make_group('highlightstail', (col, row), f'highlighttail{tail}')

        # Dark Shading
        dark_shading = [["AGOUTI", "ARCTIC", "ASPEN", "BRINDLE", "CALI", "COLORPOINT", "FOXY", "GRAYWOLF"],
            ["GRIZZLE", "HUSKY", "MEXICAN", "OPHELIA", "POINTS", "RUNIC", "SABLE", "SEMISOLID"],
            ["SHEPHERD", "SMOKEY", "SOLID", "STORMY", "SVALBARD", "TIMBER", "VIBRANT", "WINTER"]]
        for row, darkshading in enumerate(dark_shading):
            for col, ds in enumerate(darkshading):
                self.make_group('dark', (col, row), f'dark{ds}')
        dark_ears = [["MOST", "SHADED", "AGOUTI", "ARCTIC", "BRINDLE", "CALI", "FOXY", "GRAYWOLF"],
                              ["GRIZZLE", "MEXICAN", "RUNIC", "STORMY", "SVALBARD", "TIMBER", "VIBRANT", "WINTER"]]
        for row, ears in enumerate(dark_ears):
            for col, ear in enumerate(ears):
                self.make_group('darkears', (col, row), f'darkears{ear}')
        dark_tail = [["SOLID", "STRIPE", "AGOUTI", "ARCTIC", "ASPEN", "BRINDLE", "CALI", "FOXY"],
            ["GRAYWOLF", "GRIZZLE", "HUSKY", "MEXICAN", "OPHELIA", "RUNIC", "SABLE", "SEMISOLID"],
            ["SMOKEY", "SOLID", "SVALBARD", "TIMBER", "VIBRANT", "WINTER"]]
        for row, tails in enumerate(dark_tail):
            for col, tail in enumerate(tails):
                self.make_group('darktail', (col, row), f'darktail{tail}')

        # Torties
        tortie_patches = [["CAPE", "DIPPED", "HEARTBREAKER", "INKSPILL", "MINIMAL", "PHANTOM", "PUDDLES", "REDTAIL"],
            ["SHADOWSTEP", "SPLIT", "SPLOTCH", "WATERFALL"]]
        for row, tortiepatches in enumerate(tortie_patches):
            for col, tp in enumerate(tortiepatches):
                self.make_group('torties', (col, row), f'tortie{tp}')
        for a, i in enumerate(["SOLID", "HEARTBREAKER", "MINIMAL", "PUDDLES", "REDTAIL", "SHADOWSTEP", "SPLIT"]):
            self.make_group('tortieears', (a, 0), f'tortieears{i}')
        for a, i in enumerate(["SOLID", "HEARTBREAKER", "INKSPILL", "PHANTOM", "SPLIT", "SPLOTCH", "WATERFALL"]):
            self.make_group('tortietail', (a, 0), f'tortietail{i}')

        self.load_scars()
        self.load_symbols()

    def load_scars(self):
        """
        Loads scar sprites and puts them into groups.
        """
        scars_data = [["ONE", "TWO", "THREE", "MANLEG", "BRIGHTHEART", "MANTAIL", "BRIDGE", "RIGHTBLIND", "LEFTBLIND",
             "BOTHBLIND", "BURNPAWS", "BURNTAIL"],
            ["BURNBELLY", "BEAKCHEEK", "BEAKLOWER", "BURNRUMP", "CATBITE", "RATBITE", "FROSTFACE", 
             "FROSTMITT", "FROSTSOCK", "QUILLCHUNK", "QUILLSCRATCH", "FROSTTAIL"],
            ["TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "TOETRAP", "SNAKE", "LEGBITE",
             "NECKBITE", "FACE"],
            ["HINDLEG", "BACK", "QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR"]]
        for row, scars in enumerate(scars_data):
            for col, scar in enumerate(scars):
                self.make_group('scars', (col, row), f'scars{scar}')
                
        for a, i in enumerate(["BURNBELLY", "BURNTAIL", "FROSTFACE", "FROSTTAIL", "HALFTAIL", "LEFTEAR", "MANTAIL", "NOLEFTEAR", "NOPAW", "NORIGHTEAR", "RIGHTEAR", "TAILSCAR"]):
            self.make_group('scarsmissing', (a, 0), f'scarsmissing{i}')

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
        for a, i in enumerate(["BANDANABACK", "BANDANA", "BELL", "BOW", "COLLAR", "HARNESS", "LEATHER", "NYLON", "RADIO"]):
            self.make_group('petacc', (a, 0), f'petlines{i}')
        base_petacc = [["BANDANABACK", "BANDANA", "BOWLIGHT", "BOW", "COLLAR", "HARNESS", "RADIO", "accentHARNESS", "metalLEATHER", "accentNYLON", "highlightBOW", "metalBELL"],
                              ["tagNYLON"]]
        for row, accessories in enumerate(base_petacc):
            for col, accessory in enumerate(accessories):
                self.make_group('petaccbase', (col, row), f'petbase{accessory}')
        for a, i in enumerate(["GENERAL", "BANDANABACK"]):
            self.make_group('petaccmissing', (a, 0), f'petmissing{i}')
        pattern_petacc = [["plaidBANDANABACK", "swirlBANDANABACK"],
                              ["plaidBANDANA", "swirlBANDANA"]]
        for row, accessories in enumerate(base_petacc):
            for col, accessory in enumerate(accessories):
                self.make_group('petaccpatterns', (col, row), f'petpattern{accessory}')
        

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
