# pylint: disable=line-too-long
"""

TODO: Docs


"""  # pylint: enable=line-too-long

import logging
import re
from itertools import combinations
from random import choice, choices, randint, random, sample, randrange
from sys import exit as sys_exit
from typing import List

import pygame
import ujson

logger = logging.getLogger(__name__)
from scripts.game_structure import image_cache
from scripts.cat.history import History
from scripts.cat.names import names
from scripts.cat.pelts import Pelt
from scripts.cat.sprites import sprites
from scripts.game_structure.game_essentials import game, screen_x, screen_y


# ---------------------------------------------------------------------------- #
#                               Getting Cats                                   #
# ---------------------------------------------------------------------------- #


def get_alive_clan_queens(living_cats):
    living_kits = [
        cat
        for cat in living_cats
        if not (cat.dead or cat.outside) and cat.status in ["kitten", "newborn"]
    ]

    queen_dict = {}
    for cat in living_kits.copy():
        parents = cat.get_parents()
        # Fetch parent object, only alive and not outside.
        parents = [
            cat.fetch_cat(i)
            for i in parents
            if cat.fetch_cat(i)
               and not (cat.fetch_cat(i).dead or cat.fetch_cat(i).outside)
        ]
        if not parents:
            continue

        if (
                len(parents) == 1
                or len(parents) > 2
                or all(i.gender == "male" for i in parents)
                or parents[0].gender == "female"
        ):
            if parents[0].ID in queen_dict:
                queen_dict[parents[0].ID].append(cat)
                living_kits.remove(cat)
            else:
                queen_dict[parents[0].ID] = [cat]
                living_kits.remove(cat)
        elif len(parents) == 2:
            if parents[1].ID in queen_dict:
                queen_dict[parents[1].ID].append(cat)
                living_kits.remove(cat)
            else:
                queen_dict[parents[1].ID] = [cat]
                living_kits.remove(cat)
    return queen_dict, living_kits


def get_alive_status_cats(
        Cat, get_status: list, working: bool = False, sort: bool = False
) -> list:
    """
    returns a list of cat objects for all living cats of get_status in Pack
    :param Cat Cat: Cat class
    :param list get_status: list of statuses searching for
    :param bool working: default False, set to True if you would like the list to only include working cats
    :param bool sort: default False, set to True if you would like list sorted by descending moon age
    """

    alive_cats = [
        i
        for i in Cat.all_cats.values()
        if i.status in get_status and not i.dead and not i.outside
    ]

    if working:
        alive_cats = [i for i in alive_cats if not i.not_working()]

    if sort:
        alive_cats = sorted(alive_cats, key=lambda cat: cat.moons, reverse=True)

    return alive_cats


def get_living_cat_count(Cat):
    """
    Returns the int of all living cats, both in and out of the Pack
    :param Cat: Cat class
    """
    count = 0
    for the_cat in Cat.all_cats.values():
        if the_cat.dead:
            continue
        count += 1
    return count


def get_living_clan_cat_count(Cat):
    """
    Returns the int of all living cats within the Pack
    :param Cat: Cat class
    """
    count = 0
    for the_cat in Cat.all_cats.values():
        if the_cat.dead or the_cat.exiled or the_cat.outside:
            continue
        count += 1
    return count


def get_cats_same_age(Cat, cat, age_range=10):
    """
    Look for all cats in the Pack and returns a list of cats which are in the same age range as the given cat.
    :param Cat: Cat class
    :param cat: the given cat
    :param int age_range: The allowed age difference between the two cats, default 10
    """
    cats = []
    for inter_cat in Cat.all_cats.values():
        if inter_cat.dead or inter_cat.outside or inter_cat.exiled:
            continue
        if inter_cat.ID == cat.ID:
            continue

        if inter_cat.ID not in cat.relationships:
            cat.create_one_relationship(inter_cat)
            if cat.ID not in inter_cat.relationships:
                inter_cat.create_one_relationship(cat)
            continue

        if (
                inter_cat.moons <= cat.moons + age_range
                and inter_cat.moons <= cat.moons - age_range
        ):
            cats.append(inter_cat)

    return cats


def get_free_possible_mates(cat):
    """Returns a list of available cats, which are possible mates for the given cat."""
    cats = []
    for inter_cat in cat.all_cats.values():
        if inter_cat.dead or inter_cat.outside or inter_cat.exiled:
            continue
        if inter_cat.ID == cat.ID:
            continue

        if inter_cat.ID not in cat.relationships:
            cat.create_one_relationship(inter_cat)
            if cat.ID not in inter_cat.relationships:
                inter_cat.create_one_relationship(cat)
            continue

        if inter_cat.is_potential_mate(cat, for_love_interest=True):
            cats.append(inter_cat)
    return cats


def get_random_moon_cat(
        Cat, main_cat, parent_child_modifier=True, mentor_app_modifier=True
):
    """
    returns a random cat for use in moon events
    :param Cat: Cat class
    :param main_cat: cat object of main cat in event
    :param parent_child_modifier: increase the chance of the random cat being a
    parent of the main cat. Default True
    :param mentor_app_modifier: increase the chance of the random cat being a mentor or
    app of the main cat. Default True
    """
    random_cat = None

    # grab list of possible random cats
    possible_r_c = list(
        filter(
            lambda c: not c.dead
                      and not c.exiled
                      and not c.outside
                      and (c.ID != main_cat.ID),
            Cat.all_cats.values(),
        )
    )

    if possible_r_c:
        random_cat = choice(possible_r_c)
        if parent_child_modifier and not int(random() * 3):
            possible_parents = []
            if main_cat.parent1:
                if Cat.fetch_cat(main_cat.parent1) in possible_r_c:
                    possible_parents.append(main_cat.parent1)
            if main_cat.parent2:
                if Cat.fetch_cat(main_cat.parent2) in possible_r_c:
                    possible_parents.append(main_cat.parent2)
            if main_cat.adoptive_parents:
                for parent in main_cat.adoptive_parents:
                    if Cat.fetch_cat(parent) in possible_r_c:
                        possible_parents.append(parent)
            if possible_parents:
                random_cat = Cat.fetch_cat(choice(possible_parents))
        if mentor_app_modifier:
            if (
                    main_cat.status
                    in ["apprentice", "mediator apprentice", "medicine cat apprentice"]
                    and main_cat.mentor
                    and not int(random() * 3)
            ):
                random_cat = Cat.fetch_cat(main_cat.mentor)
            elif main_cat.apprentice and not int(random() * 3):
                random_cat = Cat.fetch_cat(choice(main_cat.apprentice))

    if isinstance(random_cat, str):
        print(f"WARNING: random cat was {random_cat} instead of cat object")
        random_cat = Cat.fetch_cat(random_cat)
    return random_cat


def get_warring_clan():
    """
    returns enemy clan if a war is currently ongoing
    """
    enemy_clan = None
    if game.clan.war.get("at_war", False):
        for other_clan in game.clan.all_clans:
            if other_clan.name == game.clan.war["enemy"]:
                enemy_clan = other_clan

    return enemy_clan


# ---------------------------------------------------------------------------- #
#                          Handling Outside Factors                            #
# ---------------------------------------------------------------------------- #


def get_current_season():
    """
    function to handle the math for finding the Pack's current season
    :return: the Pack's current season
    """

    if game.config["lock_season"]:
        game.clan.current_season = game.clan.starting_season
        return game.clan.starting_season

    modifiers = {"Newleaf": 0, "Greenleaf": 3, "Leaf-fall": 6, "Leaf-bare": 9}
    index = game.clan.age % 12 + modifiers[game.clan.starting_season]

    if index > 11:
        index = index - 12

    game.clan.current_season = game.clan.seasons[index]

    return game.clan.current_season


def change_clan_reputation(difference):
    """
    will change the Pack's reputation with outsider cats according to the difference parameter.
    """
    game.clan.reputation += difference


def change_clan_relations(other_clan, difference):
    """
    will change the Pack's relation with other clans according to the difference parameter.
    """
    # grab the clan that has been indicated
    other_clan = other_clan
    # grab the relation value for that clan
    y = game.clan.all_clans.index(other_clan)
    clan_relations = int(game.clan.all_clans[y].relations)
    # change the value
    clan_relations += difference
    # making sure it doesn't exceed the bounds
    if clan_relations > 30:
        clan_relations = 30
    elif clan_relations < 0:
        clan_relations = 0
    # setting it in the Pack save
    game.clan.all_clans[y].relations = clan_relations


def create_new_cat_block(
        Cat, Relationship, event, in_event_cats: dict, i: int, attribute_list: List[str]
) -> list:
    """
    Creates a single new_cat block and then generates and returns the cats within the block
    :param Cat Cat: always pass Cat class
    :param Relationship Relationship: always pass Relationship class
    :param event: always pass the event class
    :param dict in_event_cats: dict containing involved cats' abbreviations as keys and cat objects as values
    :param int i: index of the cat block
    :param list[str] attribute_list: attribute list contained within the block
    """

    thought = "Is looking around the camp with wonder"
    new_cats = None

    # gather bio parents
    parent1 = None
    parent2 = None
    for tag in attribute_list:
        match = re.match(r"parent:([,0-9]+)", tag)
        if not match:
            continue

        parent_indexes = match.group(1).split(",")
        if not parent_indexes:
            continue

        parent_indexes = [int(index) for index in parent_indexes]
        for index in parent_indexes:
            if index >= i:
                continue

            if parent1 is None:
                parent1 = event.new_cats[index][0]
            else:
                parent2 = event.new_cats[index][0]
        break

    # gather mates
    give_mates = []
    for tag in attribute_list:
        match = re.match(r"mate:([_,0-9a-zA-Z]+)", tag)
        if not match:
            continue

        mate_indexes = match.group(1).split(",")

        # TODO: make this less ugly
        for index in mate_indexes:
            if index in in_event_cats:
                if in_event_cats[index] in [
                    "apprentice",
                    "medicine cat apprentice",
                    "mediator apprentice",
                ]:
                    print("Can't give apprentices mates")
                    continue

                give_mates.append(in_event_cats[index])

            try:
                index = int(index)
            except ValueError:
                print(f"mate-index not correct: {index}")
                continue

            if index >= i:
                continue

            give_mates.extend(event.new_cats[index])

    # determine gender
    if "male" in attribute_list:
        gender = "male"
    elif "female" in attribute_list:
        gender = "female"
    elif (
            "can_birth" in attribute_list and not game.clan.clan_settings["same sex birth"]
    ):
        gender = "female"
    else:
        gender = None

    # will the cat get a new name?
    if "new_name" in attribute_list:
        new_name = True
    elif "old_name" in attribute_list:
        new_name = False
    else:
        new_name = choice([True, False])

    # STATUS - must be handled before backstories
    status = None
    for _tag in attribute_list:
        match = re.match(r"status:(.+)", _tag)
        if not match:
            continue

        if match.group(1) in [
            "newborn",
            "kitten",
            "elder",
            "apprentice",
            "warrior",
            "mediator apprentice",
            "mediator",
            "medicine cat apprentice",
            "medicine cat",
        ]:
            status = match.group(1)
            break

    # SET AGE
    age = None
    for _tag in attribute_list:
        match = re.match(r"age:(.+)", _tag)
        if not match:
            continue

        if match.group(1) in Cat.age_moons:
            age = randint(
                Cat.age_moons[match.group(1)][0], Cat.age_moons[match.group(1)][1]
            )
            break

        # Set same as first mate
        if match.group(1) == "mate" and give_mates:
            age = randint(
                Cat.age_moons[give_mates[0].age][0], Cat.age_moons[give_mates[0].age][1]
            )
            break

        if match.group(1) == "has_kits":
            age = randint(19, 120)
            break

    if status and not age:
        if status in ["apprentice", "mediator apprentice", "medicine cat apprentice"]:
            age = randint(
                Cat.age_moons["adolescent"][0], Cat.age_moons["adolescent"][1]
            )
        elif status in ["warrior", "mediator", "medicine cat"]:
            age = randint(
                Cat.age_moons["young adult"][0], Cat.age_moons["senior adult"][1]
            )
        elif status == "elder":
            age = randint(Cat.age_moons["senior"][0], Cat.age_moons["senior"][1])

    if "pet" in attribute_list:
        cat_type = "pet"
    elif "rogue" in attribute_list:
        cat_type = "rogue"
    elif "loner" in attribute_list:
        cat_type = "loner"
    elif "clancat" in attribute_list:
        cat_type = "former Packwolf"
    else:
        cat_type = choice(['pet', 'loner', 'former Packwolf'])

    # LITTER
    litter = False
    if "litter" in attribute_list:
        litter = True
        if status not in ["kitten", "newborn"]:
            status = "kitten"

    # CHOOSE DEFAULT BACKSTORY BASED ON CAT TYPE, STATUS
    if status in ("kitten", "newborn"):
        chosen_backstory = choice(BACKSTORIES["backstory_categories"]["abandoned_backstories"])
    elif status == "medicine cat" and cat_type == "former Packwolf":
        chosen_backstory = choice(["medicine_cat", "disgraced1"])
    elif status == "medicine cat":
        chosen_backstory = choice(["wandering_healer1", "wandering_healer2"])
    else:
        if cat_type == "former Packwolf":
            x = "former_clancat"
        else:
            x = cat_type
        chosen_backstory = choice(
            BACKSTORIES["backstory_categories"].get(f"{x}_backstories", ["outsider1"])
        )

    # OPTION TO OVERRIDE DEFAULT BACKSTORY
    bs_override = False
    stor = []
    for _tag in attribute_list:
        match = re.match(r"backstory:(.+)", _tag)
        if match:
            stor = [
                x for x in match.group(1).split(",") if x in BACKSTORIES["backstories"]
            ]
            if not stor:
                bs_override = True
                continue
            chosen_backstory = choice(stor)
            break

    # KITTEN THOUGHT
    if status in ["kitten", "newborn"]:
        thought = "Is snuggled safe in the nursery"

    # MEETING - DETERMINE IF THIS IS AN OUTSIDE CAT
    outside = False
    if "meeting" in attribute_list:
        outside = True
        status = cat_type
        new_name = False
        thought = "Is wondering about those new wolves"

    # IS THE CAT DEAD?
    alive = True
    if "dead" in attribute_list:
        alive = False
        thought = "Explores a new, starry world"

    # check if we can use an existing cat here
    chosen_cat = None
    if "exists" in attribute_list:
        existing_outsiders = [
            i for i in Cat.all_cats.values() if i.outside and not i.dead
        ]
        possible_outsiders = []
        for cat in existing_outsiders:
            if stor and cat.backstory not in stor:
                continue
            if cat_type != cat.status:
                continue
            if gender and gender != cat.gender:
                continue
            if age and age not in Cat.age_moons[cat.age]:
                continue
            possible_outsiders.append(cat)

        if possible_outsiders:
            chosen_cat = choice(possible_outsiders)
            game.clan.add_to_clan(chosen_cat)
            chosen_cat.status = status
            chosen_cat.outside = outside
            if not alive:
                chosen_cat.die()

            if new_name:
                name = f"{chosen_cat.name.prefix}"
                spaces = name.count(" ")
                if choice([1, 2]) == 1 and spaces > 0:  # adding suffix to OG name
                    # make a list of the words within the name, then add the OG name back in the list
                    words = name.split(" ")
                    words.append(name)
                    new_prefix = choice(words)  # pick new prefix from that list
                    name = new_prefix
                    chosen_cat.name.prefix = name
                    chosen_cat.name.give_suffix(
                        pelt=chosen_cat.pelt,
                        biome=game.clan.biome,
                        tortiepattern=chosen_cat.pelt.tortiepattern,
                    )
                else:  # completely new name
                    chosen_cat.name.give_prefix(
                        eyes=chosen_cat.pelt.eye_colour,
                        colour=chosen_cat.pelt.colour,
                        biome=game.clan.biome,
                    )
                    chosen_cat.name.give_suffix(
                        pelt=chosen_cat.pelt.colour,
                        biome=game.clan.biome,
                        tortiepattern=chosen_cat.pelt.tortiepattern,
                    )

            new_cats = [chosen_cat]

    # Now we generate the new cat
    if not chosen_cat:
        new_cats = create_new_cat(
            Cat,
            new_name=new_name,
            loner=cat_type in ["loner", "rogue"],
            pet=cat_type == "pet",
            other_clan=cat_type == 'former Packwolf',
            kit=False if litter else status in ["kitten", "newborn"],
            # this is for singular kits, litters need this to be false
            litter=litter,
            backstory=chosen_backstory,
            status=status,
            age=age,
            gender=gender,
            thought=thought,
            alive=alive,
            outside=outside,
            parent1=parent1.ID if parent1 else None,
            parent2=parent2.ID if parent2 else None
            )

        # NEXT
        # add relations to bio parents, if needed
        # add relations to cats generated within the same block, as they are littermates
        # add mates
        # THIS DOES NOT ADD RELATIONS TO CATS IN THE EVENT, those are added within the relationships block of the event

        for n_c in new_cats:

            # SET MATES
            for inter_cat in give_mates:
                if n_c == inter_cat or n_c.ID in inter_cat.mate:
                    continue

                # this is some duplicate work, since this triggers inheritance re-calcs
                # TODO: optimize
                n_c.set_mate(inter_cat)

            # LITTERMATES
            for inter_cat in new_cats:
                if n_c == inter_cat:
                    continue

                y = randrange(0, 20)
                start_relation = Relationship(n_c, inter_cat, False, True)
                start_relation.platonic_like += 30 + y
                start_relation.comfortable = 10 + y
                start_relation.admiration = 15 + y
                start_relation.trust = 10 + y
                n_c.relationships[inter_cat.ID] = start_relation

            # BIO PARENTS
            for par in (parent1, parent2):
                if not par:
                    continue

                y = randrange(0, 20)
                start_relation = Relationship(par, n_c, False, True)
                start_relation.platonic_like += 30 + y
                start_relation.comfortable = 10 + y
                start_relation.admiration = 15 + y
                start_relation.trust = 10 + y
                par.relationships[n_c.ID] = start_relation

                y = randrange(0, 20)
                start_relation = Relationship(n_c, par, False, True)
                start_relation.platonic_like += 30 + y
                start_relation.comfortable = 10 + y
                start_relation.admiration = 15 + y
                start_relation.trust = 10 + y
                n_c.relationships[par.ID] = start_relation

            # UPDATE INHERITANCE
            n_c.create_inheritance_new_cat()

    return new_cats


def get_other_clan(clan_name):
    """
    returns the clan object of given clan name
    """
    for clan in game.clan.all_clans:
        if clan.name == clan_name:
            return clan


def create_new_cat(
        Cat,
        new_name: bool = False,
        loner: bool = False,
        pet: bool = False,
        kit: bool = False,
        litter: bool = False,
        other_clan: bool = None,
        backstory: bool = None,
        status: str = None,
        age: int = None,
        gender: str = None,
        thought: str = "Is looking around the camp with wonder",
        alive: bool = True,
        outside: bool = False,
        parent1: str = None,
        parent2: str = None,
) -> list:
    """
    This function creates new cats and then returns a list of those cats
    :param Cat Cat: pass the Cat class
    :params Relationship Relationship: pass the Relationship class
    :param bool new_name: set True if cat(s) is a loner/rogue receiving a new Pack name - default: False
    :param bool loner: set True if cat(s) is a loner or rogue - default: False
    :param bool pet: set True if cat(s) is a pet - default: False
    :param bool kit: set True if the cat is a lone kitten - default: False
    :param bool litter: set True if a litter of kittens needs to be generated - default: False
    :param bool other_clan: if new cat(s) are from a neighboring clan, set true
    :param bool backstory: a list of possible backstories.json for the new cat(s) - default: None
    :param str status: set as the rank you want the new cat to have - default: None (will cause a random status to be picked)
    :param int age: set the age of the new cat(s) - default: None (will be random or if kit/litter is true, will be kitten.
    :param str gender: set the gender (BIRTH SEX) of the cat - default: None (will be random)
    :param str thought: if you need to give a custom "welcome" thought, set it here
    :param bool alive: set this as False to generate the cat as already dead - default: True (alive)
    :param bool outside: set this as True to generate the cat as an outsider instead of as part of the Pack - default: False (Pack cat)
    :param str parent1: Cat ID to set as the biological parent1
    :param str parent2: Cat ID object to set as the biological parert2
    """
    # TODO: it would be nice to rewrite this to be less bool-centric
    accessory = None
    if isinstance(backstory, list):
        backstory = choice(backstory)

    if backstory in (
            BACKSTORIES["backstory_categories"]["former_clancat_backstories"]
            or BACKSTORIES["backstory_categories"]["otherclan_categories"]
    ):
        other_clan = True

    created_cats = []

    if not litter:
        number_of_cats = 1
    else:
        number_of_cats = choices([2, 3, 4, 5], [5, 4, 1, 1], k=1)[0]

    if not isinstance(age, int):
        if status == "newborn":
            age = 0
        elif litter or kit:
            age = randint(1, 5)
        elif status in ("apprentice", "medicine cat apprentice", "mediator apprentice"):
            age = randint(6, 11)
        elif status == "warrior":
            age = randint(23, 120)
        elif status == "medicine cat":
            age = randint(23, 140)
        elif status == "elder":
            age = randint(120, 130)
        else:
            age = randint(6, 120)

    # setting status
    if not status:
        if age == 0:
            status = "newborn"
        elif age < 6:
            status = "kitten"
        elif 6 <= age <= 11:
            status = "apprentice"
        elif age >= 12:
            status = "warrior"
        elif age >= 120:
            status = "elder"

    # cat creation and naming time
    for index in range(number_of_cats):
        # setting gender
        if not gender:
            _gender = choice(["female", "male"])
        else:
            _gender = gender

        # other Pack cats, apps, and kittens (kittens and apps get indoctrinated lmao no old names for them)
        if other_clan or kit or litter or age < 12 and not (loner or pet):
            new_cat = Cat(
                moons=age,
                status=status,
                gender=_gender,
                backstory=backstory,
                parent1=parent1,
                parent2=parent2,
            )
        else:
            # grab starting names and accs for loners/pets
            if pet:
                name = choice(names.names_dict["loner_names"])
                if choice([1, 2]) == 1:
                    accessory = choice(choices(Pelt.every_acc_list, weights=(0, 0, 60, 0, 20, 20), k=1)[0])
            elif (
                    loner and choice([1, 2]) == 1
            ):  # try to give name from full loner name list
                name = choice(names.names_dict["loner_names"])
                if choice([0, 5]) <= 3:
                    accessory = choice(choices(Pelt.every_acc_list, weights=(20, 20, 15, 30, 5, 10), k=1)[0])
            else:
                name = choice(
                    names.names_dict["normal_prefixes"])  # otherwise give name from prefix list (more nature-y names)
                if choice([0, 5]) <= 3:
                    accessory = choice(choices(Pelt.every_acc_list, weights=(20, 20, 15, 30, 5, 10), k=1)[0])

            # now we make the cats
            if new_name:  # these cats get new names
                if choice([1, 2]) == 1:  # adding suffix to OG name
                    spaces = name.count(" ")
                    if spaces > 0:
                        # make a list of the words within the name, then add the OG name back in the list
                        words = name.split(" ")
                        words.append(name)
                        new_prefix = choice(words)  # pick new prefix from that list
                        name = new_prefix
                    new_cat = Cat(
                        moons=age,
                        prefix=name,
                        status=status,
                        gender=_gender,
                        backstory=backstory,
                        parent1=parent1,
                        parent2=parent2,
                    )
                else:  # completely new name
                    new_cat = Cat(
                        moons=age,
                        status=status,
                        gender=_gender,
                        backstory=backstory,
                        parent1=parent1,
                        parent2=parent2,
                    )
            # these cats keep their old names
            else:
                new_cat = Cat(
                    moons=age,
                    prefix=name,
                    suffix="",
                    status=status,
                    gender=_gender,
                    backstory=backstory,
                    parent1=parent1,
                    parent2=parent2,
                )

        # give em a collar if they got one
        if accessory:
            new_cat.pelt.accessory = accessory

        # give apprentice aged cat a mentor
        if new_cat.age == "adolescent":
            new_cat.update_mentor()

        # Remove disabling scars, if they generated.
        not_allowed = ['NOPAW', 'NOTAIL', 'HALFTAIL', 'NOEAR', 'BOTHBLIND', 'RIGHTBLIND', 
                       'LEFTBLIND', 'BRIGHTHEART', 'NOLEFTEAR', 'NORIGHTEAR', 'MANLEG', 'BLIND']
        for scar in new_cat.pelt.scars:
            if scar in not_allowed:
                new_cat.pelt.scars.remove(scar)

        # chance to give the new cat a permanent condition, higher chance for found kits and litters
        if game.clan.game_mode != "classic":
            if kit or litter:
                chance = int(
                    game.config["cat_generation"]["base_permanent_condition"] / 11.25
                )
            else:
                chance = game.config["cat_generation"]["base_permanent_condition"] + 10
            if not int(random() * chance):
                possible_conditions = []
                for condition in PERMANENT:
                    if (kit or litter) and PERMANENT[condition]["congenital"] not in [
                        "always",
                        "sometimes",
                    ]:
                        continue
                    # next part ensures that a kit won't get a condition that takes too long to reveal
                    age = new_cat.moons
                    leeway = 5 - (PERMANENT[condition]["moons_until"] + 1)
                    if age > leeway:
                        continue
                    possible_conditions.append(condition)

                if possible_conditions:
                    chosen_condition = choice(possible_conditions)
                    born_with = False
                    if PERMANENT[chosen_condition]["congenital"] in [
                        "always",
                        "sometimes",
                    ]:
                        born_with = True

                    new_cat.get_permanent_condition(chosen_condition, born_with)
                    if (
                            new_cat.permanent_condition[chosen_condition]["moons_until"]
                            == 0
                    ):
                        new_cat.permanent_condition[chosen_condition][
                            "moons_until"
                        ] = -2

                    # assign scars
                    if chosen_condition in ["lost a leg", "born without a leg"]:
                        new_cat.pelt.scars.append("NOPAW")
                    elif chosen_condition in ["lost their tail", "born without a tail"]:
                        new_cat.pelt.scars.append("NOTAIL")
                    elif chosen_condition in ['blind']:
                        new_cat.pelt.scars.append("BLIND")

        if outside:
            new_cat.outside = True
        if not alive:
            new_cat.die()

        # newbie thought
        new_cat.thought = thought

        # and they exist now
        created_cats.append(new_cat)
        game.clan.add_cat(new_cat)
        history = History()
        history.add_beginning(new_cat)

        # create relationships
        new_cat.create_relationships_new_cat()
        # Note - we always update inheritance after the cats are generated, to
        # allow us to add parents.
        # new_cat.create_inheritance_new_cat()

    return created_cats


# ---------------------------------------------------------------------------- #
#                             Cat Relationships                                #
# ---------------------------------------------------------------------------- #


def get_highest_romantic_relation(
        relationships, exclude_mate=False, potential_mate=False
):
    """Returns the relationship with the highest romantic value."""
    max_love_value = 0
    current_max_relationship = None
    for rel in relationships:
        if rel.romantic_love < 0:
            continue
        if exclude_mate and rel.cat_from.ID in rel.cat_to.mate:
            continue
        if potential_mate and not rel.cat_to.is_potential_mate(
                rel.cat_from, for_love_interest=True
        ):
            continue
        if rel.romantic_love > max_love_value:
            current_max_relationship = rel
            max_love_value = rel.romantic_love

    return current_max_relationship


def check_relationship_value(cat_from, cat_to, rel_value=None):
    """
    returns the value of the rel_value param given
    :param cat_from: the cat who is having the feelings
    :param cat_to: the cat that the feelings are directed towards
    :param rel_value: the relationship value that you're looking for,
    options are: romantic, platonic, dislike, admiration, comfortable, jealousy, trust
    """
    if cat_to.ID in cat_from.relationships:
        relationship = cat_from.relationships[cat_to.ID]
    else:
        relationship = cat_from.create_one_relationship(cat_to)

    if rel_value == "romantic":
        return relationship.romantic_love
    elif rel_value == "platonic":
        return relationship.platonic_like
    elif rel_value == "dislike":
        return relationship.dislike
    elif rel_value == "admiration":
        return relationship.admiration
    elif rel_value == "comfortable":
        return relationship.comfortable
    elif rel_value == "jealousy":
        return relationship.jealousy
    elif rel_value == "trust":
        return relationship.trust


def get_personality_compatibility(cat1, cat2):
    """Returns:
    True - if personalities have a positive compatibility
    False - if personalities have a negative compatibility
    None - if personalities have a neutral compatibility
    """
    personality1 = cat1.personality.trait
    personality2 = cat2.personality.trait

    if personality1 == personality2:
        if personality1 is None:
            return None
        return True

    lawfulness_diff = abs(cat1.personality.lawfulness - cat2.personality.lawfulness)
    sociability_diff = abs(cat1.personality.sociability - cat2.personality.sociability)
    aggression_diff = abs(cat1.personality.aggression - cat2.personality.aggression)
    stability_diff = abs(cat1.personality.stability - cat2.personality.stability)
    list_of_differences = [
        lawfulness_diff,
        sociability_diff,
        aggression_diff,
        stability_diff,
    ]

    running_total = 0
    for x in list_of_differences:
        if x <= 4:
            running_total += 1
        elif x >= 6:
            running_total -= 1

    if running_total >= 2:
        return True
    if running_total <= -2:
        return False

    return None


def get_cats_of_romantic_interest(cat):
    """Returns a list of cats, those cats are love interest of the given cat"""
    cats = []
    for inter_cat in cat.all_cats.values():
        if inter_cat.dead or inter_cat.outside or inter_cat.exiled:
            continue
        if inter_cat.ID == cat.ID:
            continue

        if inter_cat.ID not in cat.relationships:
            cat.create_one_relationship(inter_cat)
            if cat.ID not in inter_cat.relationships:
                inter_cat.create_one_relationship(cat)
            continue

        # Extra check to ensure they are potential mates
        if (
                inter_cat.is_potential_mate(cat, for_love_interest=True)
                and cat.relationships[inter_cat.ID].romantic_love > 0
        ):
            cats.append(inter_cat)
    return cats


def get_amount_of_cats_with_relation_value_towards(cat, value, all_cats):
    """
    Looks how many cats have the certain value
    :param cat: cat in question
    :param value: value which has to be reached
    :param all_cats: list of cats which has to be checked
    """

    # collect all true or false if the value is reached for the cat or not
    # later count or sum can be used to get the amount of cats
    # this will be handled like this, because it is easier / shorter to check
    relation_dict = {
        "romantic_love": [],
        "platonic_like": [],
        "dislike": [],
        "admiration": [],
        "comfortable": [],
        "jealousy": [],
        "trust": [],
    }

    for inter_cat in all_cats:
        if cat.ID in inter_cat.relationships:
            relation = inter_cat.relationships[cat.ID]
        else:
            continue

        relation_dict["romantic_love"].append(relation.romantic_love >= value)
        relation_dict["platonic_like"].append(relation.platonic_like >= value)
        relation_dict["dislike"].append(relation.dislike >= value)
        relation_dict["admiration"].append(relation.admiration >= value)
        relation_dict["comfortable"].append(relation.comfortable >= value)
        relation_dict["jealousy"].append(relation.jealousy >= value)
        relation_dict["trust"].append(relation.trust >= value)

    return_dict = {
        "romantic_love": sum(relation_dict["romantic_love"]),
        "platonic_like": sum(relation_dict["platonic_like"]),
        "dislike": sum(relation_dict["dislike"]),
        "admiration": sum(relation_dict["admiration"]),
        "comfortable": sum(relation_dict["comfortable"]),
        "jealousy": sum(relation_dict["jealousy"]),
        "trust": sum(relation_dict["trust"]),
    }

    return return_dict


def filter_relationship_type(
        group: list, filter_types: List[str], event_id: str = None, patrol_leader=None
):
    """
    filters for specific types of relationships between groups of cat objects, returns bool
    :param list[Cat] group: the group of cats to be tested (make sure they're in the correct order (i.e. if testing for
    parent/child, the cat being tested as parent must be index 0)
    :param list[str] filter_types: the relationship types to check for. possible types: "siblings", "mates",
    "mates_with_pl" (PATROL ONLY), "not_mates", "parent/child", "child/parent", "mentor/app", "app/mentor",
    (following tags check if value is over given int) "romantic_int", "platonic_int", "dislike_int", "comfortable_int",
    "jealousy_int", "trust_int"
    :param str event_id: if the event has an ID, include it here
    :param Cat patrol_leader: if you are testing a patrol, ensure you include the self.patrol_leader here
    """
    # keeping this list here just for quick reference of what tags are handled here
    possible_rel_types = [
        "siblings",
        "mates",
        "mates_with_pl",
        "not_mates",
        "parent/child",
        "child/parent",
        "mentor/app",
        "app/mentor",
    ]

    possible_value_types = [
        "romantic",
        "platonic",
        "dislike",
        "comfortable",
        "jealousy",
        "trust",
        "admiration",
    ]

    if "siblings" in filter_types:
        test_cat = group[0]
        testing_cats = [cat for cat in group if cat.ID != test_cat.ID]

        siblings = [test_cat.is_sibling(inter_cat) for inter_cat in testing_cats]
        if not all(siblings):
            return False

    if "mates" in filter_types:
        # first test if more than one cat
        if len(group) == 1:
            return False

        # then if cats don't have the needed number of mates
        if not all(len(i.mate) >= (len(group) - 1) for i in group):
            return False

        # Now the expensive test.  We have to see if everone is mates with each other
        # Hopefully the cheaper tests mean this is only needed on events with a small number of cats
        for x in combinations(group, 2):
            if x[0].ID not in x[1].mate:
                return False

    # check if all cats are mates with p_l (they do not have to be mates with each other)
    if "mates_with_pl" in filter_types:
        # First test if there is more than one cat
        if len(group) == 1:
            return False

        # Check each cat to see if it is mates with the patrol leader
        for cat in group:
            if cat.ID == patrol_leader.ID:
                continue
            if cat.ID not in patrol_leader.mate:
                return False

    # Check if all cats are not mates
    if "not_mates" in filter_types:
        # opposite of mate check
        for x in combinations(group, 2):
            if x[0].ID in x[1].mate:
                return False

    # Check if the cats are in a parent/child relationship
    if "parent/child" in filter_types:
        if patrol_leader:
            if patrol_leader in group:
                group.remove(patrol_leader)
            group.insert(0, patrol_leader)
        # It should be exactly two cats for a "parent/child" event
        if len(group) != 2:
            return False
        # test for parentage
        if not group[0].is_parent(group[1]):
            return False

    if "child/parent" in filter_types:
        if patrol_leader:
            if patrol_leader in group:
                group.remove(patrol_leader)
            group.insert(0, patrol_leader)
        # It should be exactly two cats for a "parent/child" event
        if len(group) != 2:
            return False
        # test for parentage
        if not group[1].is_parent(group[0]):
            return False

    if "mentor/app" in filter_types:
        if patrol_leader:
            if patrol_leader in group:
                group.remove(patrol_leader)
            group.insert(0, patrol_leader)
        # It should be exactly two cats for a "parent/child" event
        if len(group) != 2:
            return False
        # test for parentage
        if not group[1].ID in group[0].apprentice:
            return False

    if "app/mentor" in filter_types:
        if patrol_leader:
            if patrol_leader in group:
                group.remove(patrol_leader)
            group.insert(0, patrol_leader)
        # It should be exactly two cats for a "parent/child" event
        if len(group) != 2:
            return False
        # test for parentage
        if not group[0].ID in group[1].apprentice:
            return False

    # Filtering relationship values
    break_loop = False
    for v_type in possible_value_types:
        # first get all tags for current value types
        tags = [constraint for constraint in filter_types if v_type in constraint]

        # If there is not a tag for the current value type, check next one
        if len(tags) == 0:
            continue

            # there should be only one value constraint for each value type
        elif len(tags) > 1:
            print(
                f"ERROR: event {event_id} has multiple relationship constraints for the value {v_type}."
            )
            break_loop = True
            break

        # try to extract the value/threshold from the text
        try:
            threshold = int(tags[0].split("_")[1])
        except:
            print(
                f"ERROR: event {event_id} with the relationship constraint for the value does not {v_type} follow the formatting guidelines."
            )
            break_loop = True
            break

        if threshold > 100:
            print(
                f"ERROR: event {event_id} has a relationship constraint for the value {v_type}, which is higher than the max value of a relationship."
            )
            break_loop = True
            break

        if threshold <= 0:
            print(
                f"ERROR: event {event_id} has a relationship constraint for the value {v_type}, which is lower than the min value of a relationship or 0."
            )
            break_loop = True
            break

        # each cat has to have relationships with this relationship value above the threshold
        fulfilled = True
        for inter_cat in group:
            rel_above_threshold = []
            group_ids = [cat.ID for cat in group]
            relevant_relationships = list(
                filter(
                    lambda rel: rel.cat_to.ID in group_ids
                                and rel.cat_to.ID != inter_cat.ID,
                    list(inter_cat.relationships.values()),
                )
            )

            # get the relationships depending on the current value type + threshold
            if v_type == "romantic":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.romantic_love >= threshold
                ]
            elif v_type == "platonic":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.platonic_like >= threshold
                ]
            elif v_type == "dislike":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.dislike >= threshold
                ]
            elif v_type == "comfortable":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.comfortable >= threshold
                ]
            elif v_type == "jealousy":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.jealousy >= threshold
                ]
            elif v_type == "trust":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.trust >= threshold
                ]
            elif v_type == "admiration":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.admiration >= threshold
                ]

            # if the lengths are not equal, one cat has not the relationship value which is needed to another cat of
            # the event
            if len(rel_above_threshold) + 1 != len(group):
                fulfilled = False
                break

        if not fulfilled:
            break_loop = True
            break

    # if break is used in the loop, the condition are not fulfilled
    # and this event should not be added to the filtered list
    if break_loop:
        return False

    return True


def gather_cat_objects(
        Cat, abbr_list: List[str], event, stat_cat=None, extra_cat=None
) -> list:
    """
    gathers cat objects from list of abbreviations used within an event format block
    :param Cat Cat: Cat class
    :param list[str] abbr_list: The list of abbreviations, supports "m_c", "r_c", "p_l", "s_c", "app1", "app2", "clan",
    "some_clan", "patrol", "multi", "n_c{index}"
    :param event: the controlling class of the event (e.g. Patrol, HandleShortEvents), default None
    :param Cat stat_cat: if passing the Patrol class, must include stat_cat separately
    :param Cat extra_cat: if not passing an event class, include the single affected cat object here. If you are not
    passing a full event class, then be aware that you can only include "m_c" as a cat abbreviation in your rel block.
    The other cat abbreviations will not work.
    :return: list of cat objects
    """
    out_set = set()

    for abbr in abbr_list:
        if abbr == "m_c":
            if extra_cat:
                out_set.add(extra_cat)
            else:
                out_set.add(event.main_cat)
        if abbr == "r_c":
            out_set.add(event.random_cat)
        elif abbr == "p_l":
            out_set.add(event.patrol_leader)
        elif abbr == "s_c":
            out_set.add(stat_cat)
        elif abbr == "app1" and len(event.patrol_apprentices) >= 1:
            out_set.add(event.patrol_apprentices[0])
        elif abbr == "app2" and len(event.patrol_apprentices) >= 2:
            out_set.add(event.patrol_apprentices[1])
        elif abbr == "clan":
            out_set.update(
                [x for x in Cat.all_cats_list if not (x.dead or x.outside or x.exiled)]
            )
        elif abbr == "some_clan":  # 1 / 8 of clan cats are affected
            clan_cats = [
                x for x in Cat.all_cats_list if not (x.dead or x.outside or x.exiled)
            ]
            out_set.update(
                sample(clan_cats, randint(1, max(1, round(len(clan_cats) / 8))))
            )
        elif abbr == "patrol":
            out_set.update(event.patrol_cats)
        elif abbr == "multi":
            cat_num = randint(1, max(1, len(event.patrol_cats) - 1))
            out_set.update(sample(event.patrol_cats, cat_num))
        elif re.match(r"n_c:[0-9]+", abbr):
            index = re.match(r"n_c:([0-9]+)", abbr).group(1)
            index = int(index)
            if index < len(event.new_cats):
                out_set.update(event.new_cats[index])

    return list(out_set)


def unpack_rel_block(
        Cat, relationship_effects: List[dict], event=None, stat_cat=None, extra_cat=None
):
    """
    Unpacks the info from the relationship effect block used in patrol and moon events, then adjusts rel values
    accordingly.

    :param Cat Cat: Cat class
    :param list[dict] relationship_effects: the relationship effect block
    :param event: the controlling class of the event (e.g. Patrol, HandleShortEvents), default None
    :param Cat stat_cat: if passing the Patrol class, must include stat_cat separately
    :param Cat extra_cat: if not passing an event class, include the single affected cat object here. If you are not passing a full event class, then be aware that you can only include "m_c" as a cat abbreviation in your rel block.  The other cat abbreviations will not work.
    """
    possible_values = (
        "romantic",
        "platonic",
        "dislike",
        "comfort",
        "jealous",
        "trust",
        "respect",
    )

    for block in relationship_effects:
        cats_from = block.get("cats_from", [])
        cats_to = block.get("cats_to", [])
        amount = block.get("amount")
        values = [x for x in block.get("values", ()) if x in possible_values]

        # Gather actual cat objects:
        cats_from_ob = gather_cat_objects(Cat, cats_from, event, stat_cat, extra_cat)
        cats_to_ob = gather_cat_objects(Cat, cats_to, event, stat_cat, extra_cat)

        # Remove any "None" that might have snuck in
        if None in cats_from_ob:
            cats_from_ob.remove(None)
        if None in cats_to_ob:
            cats_to_ob.remove(None)

        # Check to see if value block
        if not (cats_to_ob and cats_from_ob and values and isinstance(amount, int)):
            print(f"Relationship block incorrectly formatted: {block}")
            continue

        positive = False

        # grabbing values
        romantic_love = 0
        platonic_like = 0
        dislike = 0
        comfortable = 0
        jealousy = 0
        admiration = 0
        trust = 0
        if "romantic" in values:
            romantic_love = amount
            if amount > 0:
                positive = True
        if "platonic" in values:
            platonic_like = amount
            if amount > 0:
                positive = True
        if "dislike" in values:
            dislike = amount
            if amount < 0:
                positive = True
        if "comfort" in values:
            comfortable = amount
            if amount > 0:
                positive = True
        if "jealous" in values:
            jealousy = amount
            if amount < 0:
                positive = True
        if "trust" in values:
            trust = amount
            if amount > 0:
                positive = True
        if "respect" in values:
            admiration = amount
            if amount > 0:
                positive = True

        if positive:
            effect = f" (positive effect)"
        else:
            effect = f" (negative effect)"

        # Get log
        log1 = None
        log2 = None
        if block.get("log"):
            log = block.get("log")
            if isinstance(log, str):
                log1 = log
            elif isinstance(log, list):
                if len(log) >= 2:
                    log1 = log[0]
                    log2 = log[1]
                elif len(log) == 1:
                    log1 = log[0]
            else:
                print(f"something is wrong with relationship log: {log}")

        if not log1:
            if hasattr(event, "text"):
                try:
                    log1 = event.text + effect
                except AttributeError:
                    print(
                        f"WARNING: event changed relationships but did not create a relationship log"
                    )
            else:
                log1 = "These cats recently interacted." + effect
        if not log2:
            if hasattr(event, "text"):
                try:
                    log2 = event.text + effect
                except AttributeError:
                    print(
                        f"WARNING: event changed relationships but did not create a relationship log"
                    )
            else:
                log2 = f"These cats recently interacted." + effect

        change_relationship_values(
            cats_to_ob,
            cats_from_ob,
            romantic_love,
            platonic_like,
            dislike,
            admiration,
            comfortable,
            jealousy,
            trust,
            log=log1,
        )

        if block.get("mutual"):
            change_relationship_values(
                cats_from_ob,
                cats_to_ob,
                romantic_love,
                platonic_like,
                dislike,
                admiration,
                comfortable,
                jealousy,
                trust,
                log=log2,
            )


def change_relationship_values(
        cats_to: list,
        cats_from: list,
        romantic_love: int = 0,
        platonic_like: int = 0,
        dislike: int = 0,
        admiration: int = 0,
        comfortable: int = 0,
        jealousy: int = 0,
        trust: int = 0,
        auto_romance: bool = False,
        log: str = None,
):
    """
    changes relationship values according to the parameters.

    :param list[Cat] cats_from: list of cat objects whose rel values will be affected
    (e.g. cat_from loses trust in cat_to)
    :param list[Cat] cats_to: list of cats objects who are the target of that rel value
    (e.g. cat_from loses trust in cat_to)
    :param int romantic_love: amount to change romantic, default 0
    :param int platonic_like: amount to change platonic, default 0
    :param int dislike: amount to change dislike, default 0
    :param int admiration: amount to change admiration (respect), default 0
    :param int comfortable: amount to change comfort, default 0
    :param int jealousy: amount to change jealousy, default 0
    :param int trust: amount to change trust, default 0
    :param bool auto_romance: if the cat_from already has romantic value with cat_to, then the platonic_like param value
    will also be applied to romantic, default False
    :param str log: the string to append to the relationship log of cats involved
    """

    # This is just for test prints - DON'T DELETE - you can use this to test if relationships are changing
    """changed = False
    if romantic_love == 0 and platonic_like == 0 and dislike == 0 and admiration == 0 and \
            comfortable == 0 and jealousy == 0 and trust == 0:
        changed = False
    else:
        changed = True"""

    # pick out the correct cats
    for single_cat_from in cats_from:
        for single_cat_to in cats_to:

            # make sure we aren't trying to change a cat's relationship with themself
            if single_cat_from == single_cat_to:
                continue

            # if the cats don't know each other, start a new relationship
            if single_cat_to.ID not in single_cat_from.relationships:
                single_cat_from.create_one_relationship(single_cat_to)

            rel = single_cat_from.relationships[single_cat_to.ID]

            # here we just double-check that the cats are allowed to be romantic with each other
            if (
                    single_cat_from.is_potential_mate(single_cat_to, for_love_interest=True)
                    or single_cat_to.ID in single_cat_from.mate
            ):
                # if cat already has romantic feelings then automatically increase romantic feelings
                # when platonic feelings would increase
                if rel.romantic_love > 0 and auto_romance:
                    romantic_love = platonic_like

                # now gain the romance
                rel.romantic_love += romantic_love

            # gain other rel values
            rel.platonic_like += platonic_like
            rel.dislike += dislike
            rel.admiration += admiration
            rel.comfortable += comfortable
            rel.jealousy += jealousy
            rel.trust += trust

            # for testing purposes - DON'T DELETE - you can use this to test if relationships are changing
            """
            print(str(single_cat_from.name) + " gained relationship with " + str(rel.cat_to.name) + ": " +
                  "Romantic: " + str(romantic_love) +
                  " /Platonic: " + str(platonic_like) +
                  " /Dislike: " + str(dislike) +
                  " /Respect: " + str(admiration) +
                  " /Comfort: " + str(comfortable) +
                  " /Jealousy: " + str(jealousy) +
                  " /Trust: " + str(trust)) if changed else print("No relationship change")"""

            if log and isinstance(log, str):
                if single_cat_to.moons <= 1:
                    log_text = (
                            log
                            + f"- {single_cat_to.name} was {single_cat_to.moons} moon old"
                    )
                    if log_text not in rel.log:
                        rel.log.append(log_text)
                else:
                    log_text = (
                            log
                            + f"- {single_cat_to.name} was {single_cat_to.moons} moons old"
                    )
                    if log_text not in rel.log:
                        rel.log.append(log_text)


# ---------------------------------------------------------------------------- #
#                               Text Adjust                                    #
# ---------------------------------------------------------------------------- #


def get_leader_life_notice() -> str:
    """
    Returns a string specifying how many lives the leader has left or notifying of the leader's full death
    """
    text = ""

    lives = game.clan.leader_lives

    if lives > 0:
        text = f"The leader has {int(lives)} lives left."
    elif lives <= 0:
        if game.clan.instructor.df is False:
            text = "The leader has no lives left and has travelled to StarClan."
        else:
            text = "The leader has no lives left and has travelled to the Dark Forest."

    return text


def get_other_clan_relation(relation):
    """
    converts int value into string relation and returns string: "hostile", "neutral", or "ally"
    :param relation: the other_clan.relations value
    """

    if int(relation) >= 17:
        return "ally"
    elif 7 < int(relation) < 17:
        return "neutral"
    elif int(relation) <= 7:
        return "hostile"


def pronoun_repl(m, cat_pronouns_dict, raise_exception=False):
    """Helper function for add_pronouns. If raise_exception is
    False, any error in pronoun formatting will not raise an
    exception, and will use a simple replacement "error" """

    # Add protection about the "insert" sometimes used
    if m.group(0) == "{insert}":
        return m.group(0)

    inner_details = m.group(1).split("/")

    try:
        d = cat_pronouns_dict[inner_details[1]][1]
        if inner_details[0].upper() == "PRONOUN":
            pro = d[inner_details[2]]
            if inner_details[-1] == "CAP":
                pro = pro.capitalize()
            return pro
        elif inner_details[0].upper() == "VERB":
            return inner_details[d["conju"] + 1]

        if raise_exception:
            raise KeyError(
                f"Pronoun tag: {m.group(1)} is not properly"
                "indicated as a PRONOUN or VERB tag."
            )

        print("Failed to find pronoun:", m.group(1))
        return "error1"
    except (KeyError, IndexError) as e:
        if raise_exception:
            raise

        logger.exception("Failed to find pronoun: " + m.group(1))
        print("Failed to find pronoun:", m.group(1))
        return "error2"


def name_repl(m, cat_dict):
    """Name replacement"""
    return cat_dict[m.group(0)][0]


def process_text(text, cat_dict, raise_exception=False):
    """Add the correct name and pronouns into a string."""
    adjust_text = re.sub(
        r"\{(.*?)\}", lambda x: pronoun_repl(x, cat_dict, raise_exception), text
    )

    name_patterns = [r'(?<!\{)' + re.escape(l) + r'(?!\})' for l in cat_dict]

    adjust_text = re.sub("|".join(name_patterns), lambda x: name_repl(x, cat_dict), adjust_text)
    return adjust_text


def adjust_list_text(list_of_items) -> str:
    """
    returns the list in correct grammar format (i.e. item1, item2, item3 and item4)
    this works with any number of items
    :param list_of_items: the list of items you want converted
    :return: the new string
    """
    if len(list_of_items) == 1:
        insert = f"{list_of_items[0]}"
    elif len(list_of_items) == 2:
        insert = f"{list_of_items[0]} and {list_of_items[1]}"
    else:
        item_line = ", ".join(list_of_items[:-1])
        insert = f"{item_line}, and {list_of_items[-1]}"

    return insert


def adjust_prey_abbr(patrol_text):
    """
    checks for prey abbreviations and returns adjusted text
    """
    for abbr in PREY_LISTS["abbreviations"]:
        if abbr in patrol_text:
            chosen_list = PREY_LISTS["abbreviations"].get(abbr)
            chosen_list = PREY_LISTS[chosen_list]
            prey = choice(chosen_list)
            patrol_text = patrol_text.replace(abbr, prey)

    return patrol_text


def get_special_snippet_list(
        chosen_list, amount, sense_groups=None, return_string=True
):
    """
    function to grab items from various lists in snippet_collections.json
    list options are:
    -prophecy_list - sense_groups = sight, sound, smell, emotional, touch
    -omen_list - sense_groups = sight, sound, smell, emotional, touch
    -clair_list  - sense_groups = sound, smell, emotional, touch, taste
    -dream_list (this list doesn't have sense_groups)
    -story_list (this list doesn't have sense_groups)
    :param chosen_list: pick which list you want to grab from
    :param amount: the amount of items you want the returned list to contain
    :param sense_groups: list which senses you want the snippets to correspond with:
     "touch", "sight", "emotional", "sound", "smell" are the options. Default is None, if left as this then all senses
     will be included (if the list doesn't have sense categories, then leave as None)
    :param return_string: if True then the function will format the snippet list with appropriate commas and 'ands'.
    This will work with any number of items. If set to True, then the function will return a string instead of a list.
    (i.e. ["hate", "fear", "dread"] becomes "hate, fear, and dread") - Default is True
    :return: a list of the chosen items from chosen_list or a formatted string if format is True
    """
    biome = game.clan.biome.casefold()

    # these lists don't get sense specific snippets, so is handled first
    if chosen_list in ["dream_list", "story_list"]:

        if (
                chosen_list == "story_list"
        ):  # story list has some biome specific things to collect
            snippets = SNIPPETS[chosen_list]["general"]
            snippets.extend(SNIPPETS[chosen_list][biome])
        elif (
                chosen_list == "clair_list"
        ):  # the clair list also pulls from the dream list
            snippets = SNIPPETS[chosen_list]
            snippets.extend(SNIPPETS["dream_list"])
        else:  # the dream list just gets the one
            snippets = SNIPPETS[chosen_list]

    else:
        # if no sense groups were specified, use all of them
        if not sense_groups:
            if chosen_list == "clair_list":
                sense_groups = ["taste", "sound", "smell", "emotional", "touch"]
            else:
                sense_groups = ["sight", "sound", "smell", "emotional", "touch"]

        # find the correct lists and compile them
        snippets = []
        for sense in sense_groups:
            snippet_group = SNIPPETS[chosen_list][sense]
            snippets.extend(snippet_group["general"])
            snippets.extend(snippet_group[biome])

    # now choose a unique snippet from each snip list
    unique_snippets = []
    for snip_list in snippets:
        unique_snippets.append(choice(snip_list))

    # pick out our final snippets
    final_snippets = sample(unique_snippets, k=amount)

    if return_string:
        text = adjust_list_text(final_snippets)
        return text
    else:
        return final_snippets


def find_special_list_types(text):
    """
    purely to identify which senses are being called for by a snippet abbreviation
    returns adjusted text, sense list, and list type
    """
    senses = []
    if "omen_list" in text:
        list_type = "omen_list"
    elif "prophecy_list" in text:
        list_type = "prophecy_list"
    elif "dream_list" in text:
        list_type = "dream_list"
    elif "clair_list" in text:
        list_type = "clair_list"
    elif "story_list" in text:
        list_type = "story_list"
    else:
        return text, None, None

    if "_sight" in text:
        senses.append("sight")
        text = text.replace("_sight", "")
    if "_sound" in text:
        senses.append("sound")
        text = text.replace("_sight", "")
    if "_smell" in text:
        text = text.replace("_smell", "")
        senses.append("smell")
    if "_emotional" in text:
        text = text.replace("_emotional", "")
        senses.append("emotional")
    if "_touch" in text:
        text = text.replace("_touch", "")
        senses.append("touch")
    if "_taste" in text:
        text = text.replace("_taste", "")
        senses.append("taste")

    return text, senses, list_type


def history_text_adjust(text, other_clan_name, clan, other_cat_rc=None):
    """
    we want to handle history text on its own because it needs to preserve the pronoun tags and cat abbreviations.
    this is so that future pronoun changes or name changes will continue to be reflected in history
    """
    vowels = ["A", "E", "I", "O", "U"]

    if "o_c_n" in text:
        pos = 0
        for x in range(text.count("o_c_n")):
            if "o_c_n" in text:
                for y in vowels:
                    if str(other_clan_name).startswith(y):
                        modify = text.split()
                        if "o_c_n" in modify:
                            pos = modify.index("o_c_n")
                        if "o_c_n's" in modify:
                            pos = modify.index("o_c_n's")
                        if "o_c_n." in modify:
                            pos = modify.index("o_c_n.")
                        if modify[pos - 1] == "a":
                            modify.remove("a")
                            modify.insert(pos - 1, "an")
                        text = " ".join(modify)
                        break

        text = text.replace('o_c_n', str(other_clan_name))

    if "c_n" in text:
        text = text.replace("c_n", clan.name)
    if "r_c" in text and other_cat_rc:
        text = selective_replace(text, "r_c", str(other_cat_rc.name))
    return text


def selective_replace(text, pattern, replacement):
    i = 0
    while i < len(text):
        index = text.find(pattern, i)
        if index == -1:
            break
        start_brace = text.rfind("{", 0, index)
        end_brace = text.find("}", index)
        if start_brace != -1 and end_brace != -1 and start_brace < index < end_brace:
            i = index + len(pattern)
        else:
            text = text[:index] + replacement + text[index + len(pattern):]
            i = index + len(replacement)

    return text


def ongoing_event_text_adjust(Cat, text, clan=None, other_clan_name=None):
    """
    This function is for adjusting the text of ongoing events
    :param Cat: the cat class
    :param text: the text to be adjusted
    :param clan: the name of the clan
    :param other_clan_name: the other Pack's name if another Pack is involved
    """
    cat_dict = {}
    if "lead_name" in text:
        kitty = Cat.fetch_cat(game.clan.leader)
        cat_dict["lead_name"] = (str(kitty.name), choice(kitty.pronouns))
    if "dep_name" in text:
        kitty = Cat.fetch_cat(game.clan.deputy)
        cat_dict["dep_name"] = (str(kitty.name), choice(kitty.pronouns))
    if "med_name" in text:
        kitty = choice(get_alive_status_cats(Cat, ["medicine cat"], working=True))
        cat_dict["med_name"] = (str(kitty.name), choice(kitty.pronouns))

    if cat_dict:
        text = process_text(text, cat_dict)

    if other_clan_name:
        text = text.replace("o_c_n", other_clan_name).replace("Pack", "Pack")
    if clan:
        clan_name = str(clan.name)
    else:
        if game.clan is None:
            clan_name = game.switches["clan_list"][0]
        else:
            clan_name = str(game.clan.name)

    text = text.replace("c_n", clan_name + "Pack")

    return text


def event_text_adjust(
        Cat,
        text,
        patrol_leader=None,
        main_cat=None,
        random_cat=None,
        stat_cat=None,
        victim_cat=None,
        patrol_cats: list = None,
        patrol_apprentices: list = None,
        new_cats: list = None,
        multi_cats: list = None,
        clan=None,
        other_clan=None,
        chosen_herb: str = None,
):
    """
    handles finding abbreviations in the text and replacing them appropriately, returns the adjusted text
    :param Cat Cat: always pass the Cat class
    :param str text: the text being adjusted
    :param Cat patrol_leader: Cat object for patrol_leader (p_l), if present
    :param Cat main_cat: Cat object for main_cat (m_c), if present
    :param Cat random_cat: Cat object for random_cat (r_c), if present
    :param Cat stat_cat: Cat object for stat_cat (s_c), if present
    :param Cat victim_cat: Cat object for victim_cat (mur_c), if present
    :param list[Cat] patrol_cats: List of Cat objects for cats in patrol, if present
    :param list[Cat] patrol_apprentices: List of Cat objects for patrol_apprentices (app#), if present
    :param list[Cat] new_cats: List of Cat objects for new_cats (n_c:index), if present
    :param list[Cat] multi_cats: List of Cat objects for multi_cat (multi_cat), if present
    :param Pack clan: pass game.clan
    :param OtherClan other_clan: OtherClan object for other_clan (o_c_n), if present
    :param str chosen_herb: string of chosen_herb (chosen_herb), if present
    """
    vowels = ["A", "E", "I", "O", "U"]

    if not text:
        text = "This should not appear, report as a bug please! Tried to adjust the text, but no text was provided."
        print("WARNING: Tried to adjust text, but no text was provided.")

    replace_dict = {}

    # main_cat
    if "m_c" in text:
        replace_dict["m_c"] = (str(main_cat.name), choice(main_cat.pronouns))

    # patrol_lead
    if "p_l" in text:
        replace_dict["p_l"] = (str(patrol_leader.name), choice(patrol_leader.pronouns))

    # random_cat
    if "r_c" in text:
        if random_cat:
            replace_dict["r_c"] = (str(random_cat.name), get_pronouns(random_cat))

    # stat cat
    if "s_c" in text:
        if stat_cat:
            replace_dict["s_c"] = (str(stat_cat.name), get_pronouns(stat_cat))

    # other_cats
    if patrol_cats:
        other_cats = [
            i
            for i in patrol_cats
            if i not in [patrol_leader, random_cat, patrol_apprentices]
        ]
        other_cat_abbr = ["o_c1", "o_c2", "o_c3", "o_c4"]
        for i, abbr in enumerate(other_cat_abbr):
            if abbr not in text:
                continue
            if len(other_cats) > i:
                replace_dict[abbr] = (
                    str(other_cats[i].name),
                    choice(other_cats[i].pronouns),
                )

    # patrol_apprentices
    app_abbr = ["app1", "app2", "app3", "app4", "app5", "app6"]
    for i, abbr in enumerate(app_abbr):
        if abbr not in text:
            continue
        if len(patrol_apprentices) > i:
            replace_dict[abbr] = (
                str(patrol_apprentices[i].name),
                choice(patrol_apprentices[i].pronouns),
            )

    # new_cats (include pre version)
    if "n_c" in text:
        for i, cat_list in enumerate(new_cats):
            if len(new_cats) > 1:
                pronoun = Cat.default_pronouns[0]  # They/them for multiple cats
            else:
                pronoun = choice(cat_list[0].pronouns)

            replace_dict[f"n_c:{i}"] = (str(cat_list[0].name), pronoun)
            replace_dict[f"n_c_pre:{i}"] = (str(cat_list[0].name.prefix), pronoun)

    # mur_c (murdered cat for reveals)
    if "mur_c" in text:
        replace_dict["mur_c"] = (str(victim_cat.name), get_pronouns(victim_cat))

    # lead_name
    if "lead_name" in text:
        leader = Cat.fetch_cat(game.clan.leader)
        replace_dict["lead_name"] = (str(leader.name), choice(leader.pronouns))

    # dep_name
    if "dep_name" in text:
        deputy = Cat.fetch_cat(game.clan.deputy)
        replace_dict["dep_name"] = (str(deputy.name), choice(deputy.pronouns))

    # med_name
    if "med_name" in text:
        med = choice(get_alive_status_cats(Cat, ["medicine cat"], working=True))
        replace_dict["med_name"] = (str(med.name), choice(med.pronouns))

    # assign all names and pronouns
    if replace_dict:
        text = process_text(text, replace_dict)

    # multi_cat
    if "multi_cat" in text:
        name_list = []
        for _cat in multi_cats:
            name_list.append(str(_cat.name))
        list_text = adjust_list_text(name_list)
        text = text.replace("multi_cat", list_text)

    # other_clan_name
    if "o_c_n" in text:
        other_clan_name = other_clan.name
        pos = 0
        for x in range(text.count("o_c_n")):
            if "o_c_n" in text:
                for y in vowels:
                    if str(other_clan_name).startswith(y):
                        modify = text.split()
                        if "o_c_n" in modify:
                            pos = modify.index("o_c_n")
                        if "o_c_n's" in modify:
                            pos = modify.index("o_c_n's")
                        if "o_c_n." in modify:
                            pos = modify.index("o_c_n.")
                        if modify[pos - 1] == "a":
                            modify.remove("a")
                            modify.insert(pos - 1, "an")
                        text = " ".join(modify)
                        break

        text = text.replace('o_c_n', str(other_clan_name) + 'Pack')

    # clan_name
    if "c_n" in text:
        try:
            clan_name = clan.name
        except AttributeError:
            clan_name = game.switches["clan_list"][0]

        pos = 0
        for x in range(text.count("c_n")):
            if "c_n" in text:
                for y in vowels:
                    if str(clan_name).startswith(y):
                        modify = text.split()
                        if "c_n" in modify:
                            pos = modify.index("c_n")
                        if "c_n's" in modify:
                            pos = modify.index("c_n's")
                        if "c_n." in modify:
                            pos = modify.index("c_n.")
                        if modify[pos - 1] == "a":
                            modify.remove("a")
                            modify.insert(pos - 1, "an")
                        text = " ".join(modify)
                        break

        text = text.replace('c_n', str(clan_name) + 'Pack')

    # prey lists
    text = adjust_prey_abbr(text)

    # special lists
    text, senses, list_type = find_special_list_types(text)
    if list_type:
        sign_list = get_special_snippet_list(
            list_type, amount=randint(1, 3), sense_groups=senses
        )
        text = text.replace(list_type, str(sign_list))

    # acc_plural (only works for main_cat's acc)
    if "acc_plural" in text:
        text = text.replace(
            "acc_plural", str(ACC_DISPLAY[main_cat.pelt.accessory]["plural"])
        )

    # acc_singular (only works for main_cat's acc)
    if "acc_singular" in text:
        text = text.replace(
            "acc_singular", str(ACC_DISPLAY[main_cat.pelt.accessory]["singular"])
        )

    if "given_herb" in text:
        if "_" in chosen_herb:
            chosen_herb = chosen_herb.replace("_", " ")
        text = text.replace("given_herb", str(chosen_herb))

    return text


def leader_ceremony_text_adjust(
        Cat,
        text,
        leader,
        life_giver=None,
        virtue=None,
        extra_lives=None,
):
    """
    used to adjust the text for leader ceremonies
    """
    replace_dict = {
        "m_c_star": (str(leader.name.prefix + "star"), choice(leader.pronouns)),
        "m_c": (str(leader.name.prefix + leader.name.suffix), choice(leader.pronouns)),
    }

    if life_giver:
        replace_dict["r_c"] = (
            str(Cat.fetch_cat(life_giver).name),
            choice(Cat.fetch_cat(life_giver).pronouns),
        )

    text = process_text(text, replace_dict)

    if virtue:
        virtue = process_text(virtue, replace_dict)
        text = text.replace("[virtue]", virtue)

    if extra_lives:
        text = text.replace("[life_num]", str(extra_lives))

    text = text.replace("c_n", str(game.clan.name) + "Pack")

    return text


def ceremony_text_adjust(
        Cat,
        text,
        cat,
        old_name=None,
        dead_mentor=None,
        mentor=None,
        previous_alive_mentor=None,
        random_honor=None,
        living_parents=(),
        dead_parents=(),
):
    clanname = str(game.clan.name + "Pack")

    random_honor = random_honor
    random_living_parent = None
    random_dead_parent = None

    adjust_text = text

    cat_dict = {
        "m_c": (
            (str(cat.name), choice(cat.pronouns)) if cat else ("cat_placeholder", None)
        ),
        "(mentor)": (
            (str(mentor.name), choice(mentor.pronouns))
            if mentor
            else ("mentor_placeholder", None)
        ),
        "(deadmentor)": (
            (str(dead_mentor.name), get_pronouns(dead_mentor))
            if dead_mentor
            else ("dead_mentor_name", None)
        ),
        "(previous_mentor)": (
            (str(previous_alive_mentor.name), choice(previous_alive_mentor.pronouns))
            if previous_alive_mentor
            else ("previous_mentor_name", None)
        ),
        "l_n": (
            (str(game.clan.leader.name), choice(game.clan.leader.pronouns))
            if game.clan.leader
            else ("leader_name", None)
        ),
        "c_n": (clanname, None),
    }

    if old_name:
        cat_dict["(old_name)"] = (old_name, None)

    if random_honor:
        cat_dict["r_h"] = (random_honor, None)

    if "p1" in adjust_text and "p2" in adjust_text and len(living_parents) >= 2:
        cat_dict["p1"] = (
            str(living_parents[0].name),
            choice(living_parents[0].pronouns),
        )
        cat_dict["p2"] = (
            str(living_parents[1].name),
            choice(living_parents[1].pronouns),
        )
    elif living_parents:
        random_living_parent = choice(living_parents)
        cat_dict["p1"] = (
            str(random_living_parent.name),
            choice(random_living_parent.pronouns),
        )
        cat_dict["p2"] = (
            str(random_living_parent.name),
            choice(random_living_parent.pronouns),
        )

    if (
            "dead_par1" in adjust_text
            and "dead_par2" in adjust_text
            and len(dead_parents) >= 2
    ):
        cat_dict["dead_par1"] = (
            str(dead_parents[0].name),
            get_pronouns(dead_parents[0]),
        )
        cat_dict["dead_par2"] = (
            str(dead_parents[1].name),
            get_pronouns(dead_parents[1]),
        )
    elif dead_parents:
        random_dead_parent = choice(dead_parents)
        cat_dict["dead_par1"] = (
            str(random_dead_parent.name),
            get_pronouns(random_dead_parent),
        )
        cat_dict["dead_par2"] = (
            str(random_dead_parent.name),
            get_pronouns(random_dead_parent),
        )

    adjust_text = process_text(adjust_text, cat_dict)

    return adjust_text, random_living_parent, random_dead_parent

def get_pronouns(Cat):
    """ Get a cat's pronoun even if the cat has faded to prevent crashes (use gender-neutral pronouns when the cat has faded) """
    if Cat.pronouns == []:
        return{
            "subject": "they",
            "object": "them",
            "poss": "their",
            "inposs": "theirs",
            "self": "themself",
            "conju": 1,
        }
    else:
        return choice(Cat.pronouns)


def shorten_text_to_fit(
        name, length_limit, font_size=None, font_type="resources/fonts/NotoSans-Medium.ttf"
):
    length_limit = (
        length_limit // 2 if not game.settings["fullscreen"] else length_limit
    )
    # Set the font size based on fullscreen settings if not provided
    # Text box objects are named by their fullscreen text size so it's easier to do it this way
    if font_size is None:
        font_size = 30
    font_size = font_size // 2 if not game.settings["fullscreen"] else font_size
    # Create the font object
    font = pygame.font.Font(font_type, font_size)

    # Add dynamic name lengths by checking the actual width of the text
    total_width = 0
    short_name = ""
    for index, character in enumerate(name):
        char_width = font.size(character)[0]
        ellipsis_width = font.size("...")[0]

        # Check if the current character is the last one and its width is less than or equal to ellipsis_width
        if index == len(name) - 1 and char_width <= ellipsis_width:
            short_name += character
        else:
            total_width += char_width
            if total_width + ellipsis_width > length_limit:
                break
            short_name += character

    # If the name was truncated, add '...'
    if len(short_name) < len(name):
        short_name += "..."

    return short_name


# ---------------------------------------------------------------------------- #
#                                    Sprites                                   #
# ---------------------------------------------------------------------------- #


def scale(rect):
    rect[0] = round(rect[0] / 1600 * screen_x) if rect[0] > 0 else rect[0]
    rect[1] = round(rect[1] / 1400 * screen_y) if rect[1] > 0 else rect[1]
    rect[2] = round(rect[2] / 1600 * screen_x) if rect[2] > 0 else rect[2]
    rect[3] = round(rect[3] / 1400 * screen_y) if rect[3] > 0 else rect[3]

    return rect


def scale_dimentions(dim):
    dim = list(dim)
    dim[0] = round(dim[0] / 1600 * screen_x) if dim[0] > 0 else dim[0]
    dim[1] = round(dim[1] / 1400 * screen_y) if dim[1] > 0 else dim[1]
    dim = tuple(dim)

    return dim


def update_sprite(cat):
    # First, check if the cat is faded.
    if cat.faded:
        # Don't update the sprite if the cat is faded.
        return

    # apply
    cat.sprite = generate_sprite(cat)
    # update class dictionary
    cat.all_cats[cat.ID] = cat


def clan_symbol_sprite(clan, return_string=False, force_light=False):
    """
    returns the clan symbol for the given clan_name, if no symbol exists then random symbol is chosen
    :param clan: the clan object
    :param return_string: default False, set True if the sprite name string is required rather than the sprite image
    :param force_light: Set true if you want this sprite to override the dark/light mode changes with the light sprite
    """
    clan_name = clan.name
    clan_color = (255, 255, 255)
    if game.settings["Moonlight"]:
        clan_color = (79, 70, 100)
        if game.settings["dark mode"]:
            clan_color = (232, 223, 253)
    elif game.settings["Seaside"]:
        clan_color = (4, 110, 101)
        if game.settings["dark mode"]:
            clan_color = (78, 185, 178)
    elif game.settings["ClassicClangen"]:
        clan_color = (101, 89, 52)
        if game.settings["dark mode"]:
            clan_color = (239, 229, 206)
            
    if clan.chosen_symbol:
        if return_string:
            return clan.chosen_symbol
        else:
            return sprites.dark_mode_symbol(sprites.sprites[f"{clan.chosen_symbol}"], clan_color)
    else:
        possible_sprites = []
        for sprite in sprites.clan_symbols:
            name = sprite.strip("1234567890")
            if f"symbol{clan_name.upper()}" == name:
                possible_sprites.append(sprite)
        if return_string:  # returns the str of the symbol
            if possible_sprites:
                return choice(possible_sprites)
            else:
                # give random symbol if no matching symbol exists
                print(
                    f"WARNING: attempted to return symbol string, but there's no clan symbol for {clan_name.upper()}.  Random symbol string returned."
                )
                return f"{choice(sprites.clan_symbols)}"

        # returns the actual sprite of the symbol
        if possible_sprites:
            return sprites.dark_mode_symbol(sprites.sprites[choice(possible_sprites)], clan_color)
        else:
            # give random symbol if no matching symbol exists
            print(
                f"WARNING: attempted to return symbol sprite, but there's no clan symbol for {clan_name.upper()}.  Random symbol sprite returned."
            )
            return sprites.dark_mode_symbol(sprites.sprites[f"{choice(sprites.clan_symbols)}"], clan_color)


def generate_sprite(
        cat,
        life_state=None,
        scars_hidden=False,
        acc_hidden=False,
        always_living=False,
        no_not_working=False,
) -> pygame.Surface:
    """
    Generates the sprite for a cat, with optional arguments that will override certain things.

    :param life_state: sets the age life_stage of the cat, overriding the one set by its age. Set to string.
    :param scars_hidden: If True, doesn't display the cat's scars. If False, display cat scars.
    :param acc_hidden: If True, hide the accessory. If false, show the accessory.
    :param always_living: If True, always show the cat with living lineart
    :param no_not_working: If true, never use the not_working lineart.
                    If false, use the cat.not_working() to determine the no_working art.
    """

    if life_state is not None:
        age = life_state
    else:
        age = cat.age

    if always_living:
        dead = False
    else:
        dead = cat.dead

    # setting the cat_sprite (bc this makes things much easier)
    if (
            not no_not_working
            and cat.not_working()
            and age != "newborn"
            and game.config["cat_sprites"]["sick_sprites"]
    ):
        if age in ["kitten", "adolescent"]:
            cat_sprite = str(19)
        else:
            cat_sprite = str(18)
    elif cat.pelt.paralyzed and age != 'newborn':
        if age in ['kitten']:
            cat_sprite = str(17)
        elif age in ['adolescent']:
            cat_sprite = str(16)
        else:
            cat_sprite = str(15)
    else:
        if age == "elder" and not game.config["fun"]["all_cats_are_newborn"]:
            age = "senior"

        if game.config["fun"]["all_cats_are_newborn"]:
            cat_sprite = str(cat.pelt.cat_sprites["newborn"])
        else:
            cat_sprite = str(cat.pelt.cat_sprites[age])

    # Fixing poses for scars. skips ahead if there aren't any scars, the wrong scars, or is baby
    # don't look too closely at this i did it while half asleep ty
    scarchange = []
    posescars = ['BURNTAIL', 'FROSTTAIL', 'HALFTAIL', 'LEFTEAR', 'NOEAR', 'NOLEFTEAR', 'NORIGHTEAR', 'NOTAIL', 'RIGHTEAR']
    if len(cat.pelt.scars) != 0 and age != 'newborn' and not cat.pelt.paralyzed and not cat.not_working():
        for scar in cat.pelt.scars:
            if scar in posescars:
                scarchange.append(scar)
        if len(scarchange) != 0 and age != 'newborn' and not cat.pelt.paralyzed:
            changetail = False
            changenoear = False
            changeleft = False
            changeright = False
            if 'BURNTAIL' in scarchange or 'FROSTTAIL' in scarchange or 'HALFTAIL' in scarchange or 'NOTAIL' in scarchange:
                changetail = True
            if 'NOEAR' in scarchange:
                changenoear = True
            if 'NORIGHTEAR' in scarchange or 'RIGHTEAR' in scarchange:
                changeright = True
            if 'NOLEFTEAR' in scarchange or 'LEFTEAR' in scarchange:
                changeleft = True
            if changetail:
                if changenoear or changeright or changeleft:
                    if age in ['kitten']:
                        cat_sprite = str(2)
                    elif age in ['adolescent']:
                        cat_sprite = str(5)
                    elif age in ['senior']:
                        cat_sprite = str(14)
                    else:
                        cat_sprite = str(8)
                else:
                    if age in ['kitten']:
                        pass
                    elif age in ['adolescent']:
                        cat_sprite = str(5)
                    elif age in ['senior']:
                        if cat_sprite == 13:
                            cat_sprite = str(12)
                    else:
                        if cat_sprite == 8 or cat_sprite == 9 or cat_sprite == 10:
                            pass
                        else:
                            cat_sprite = str(9)
            elif changenoear:
                if age in ['kitten']:
                    if cat_sprite == 0:
                        cat_sprite = str(2)
                elif age in ['adolescent']:
                    if cat_sprite == 3:
                        cat_sprite = str(5)
                elif age in ['senior']:
                    cat_sprite = str(14)
                else:
                    if cat_sprite == 6 or cat_sprite == 8 or cat_sprite == 9 or cat_sprite == 10:
                        pass
                    else:
                        cat_sprite = str(8)
            elif changeright:
                if age in ['kitten']:
                    if cat_sprite == 0:
                        cat_sprite = str(2)
                elif age in ['adolescent']:
                    if cat_sprite == 3:
                        cat_sprite = str(5)
                elif age in ['senior']:
                    if cat_sprite == 13:
                        cat_sprite = str(14)
                else:
                    if cat_sprite == 6 or cat_sprite == 8 or cat_sprite == 9 or cat_sprite == 11:
                        pass
                    else:
                        cat_sprite = str(8)
            elif changeleft:
                if age in ['kitten']:
                    pass
                elif age in ['adolescent']:
                    pass
                elif age in ['senior']:
                    if cat_sprite == 12:
                        cat_sprite = str(14)
                else:
                    if cat_sprite == 6 or cat_sprite == 7 or cat_sprite == 9 or cat_sprite == 10:
                        pass
                    else:
                        cat_sprite = str(10)
            else:
                print('scar changer got confused')

    new_sprite = pygame.Surface((sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA)

    # generating the sprite
    try:
        #base, red, highlight, dark - runic mid, solids base, solids dark, solids light
        color_dict = {
            "HONEY": ["#c09460", "#a05f36", "#f2e9d8", "#1e1c1a", "#d8c093", "#c09460", "#aa774c", "#ceb282"],
            "FLAXEN": ["#cfae8d", "#ad753e", "#f5f3ed", "#1f1c1a", "#e8d9c1", "#cfae8d", "#bd9975", "#e3cdae"],
            "CREAM": ["#e5d1af", "#d09a5b", "#faf6e9", "#1e1c1a", "#f1ebda", "#e5d1af", "#dabc97", "#f6eace"],
            "PEARL": ["#f2e9d8", "#dab487", "#fffcf3", "#1f1d1a", "#fcf4e6", "#f2e9d8", "#d4c5a9", "#fffcf3"],
            "GOLD": ["#e0bc66", "#b96d13", "#fff7e5", "#211f1c", "#f9edda", "#e0bc66", "#c89236", "#f3da9e"],
            "BRASS": ["#d3be9b", "#e6d5cb", "#f7ecdf", "#a07c4e", "#ead5bd", "#d3be9b", "#bea57b", "#e4d6bf"],
            "SUNSTONE": ["#f2dcc6", "#b07748", "#fffaef", "#dcae79", "#f9edda", "#f2dcc6", "#ddb17d", "#fffaef"],
            "SUNNY": ["#f7eed4", "#f1ddab", "#faf4e5", "#d3ab6d", "#faf4e5", "#f7eed3", "#f0e5c2", "#faf4e5"],
            "DAISY": ["#fffcef", "#fff9dc", "#fffef8", "#fff9dc", "#FFFDF4", "#FFFCEF", "#FFFBE6", "#fffef8"],
            "PEACHY": ["#ffc571", "#e89f4c", "#fffcf3", "#c67c3f", "#FFEFD6", "#FFCE85", "#FFBB5C", "#FFEED0"],
            "MIST": ["#d7d4cb", "#daccb7", "#f7f5ed", "#a19e96", "#e9e6dd", "#d7d4cb", "#bfbdb5", "#edeae1"],
            "ASH": ["#87847d", "#afa294", "#f7f5ed", "#62605a", "#ceccc2", "#87847d", "#716e68", "#9a9791"],
            "STEEL": ["#4d4b45", "#877663", "#bdb8aa", "#1b1a18", "#7a776f", "#4d4b45", "#3e3c37", "#6f6c65"],
            "SILVER": ["#e3e4e6", "#bbbcbe", "#f7f8fa", "#797a7c", "#f1f1f2", "#e3e4e6", "#c0c1c5", "#f7f8fa"],
            "MOONSTONE": ["#e9eeec", "#bfc5ce", "#f6f6f6", "#b7bcb9", "#f6f6f6", "#e9eeec", "#d5dad8", "#f6f6f6"],
            "SNOW": ["#fafafa", "#fafafa", "#fafafa", "#efefef", "#fafafa", "#fafafa", "#fafafa", "#fafafa"],
            "GOSLING": ["#8b8171", "#b8ab96", "#a89b87", "#2b2a29", "#9A8E7C", "#8B8171", "#7D7364", "#b8ab96"],
            "PYRITE": ["#e0d7c6", "#dc9b57", "#fffaf6", "#655f55", "#F0E9DE", "#E0D7C6", "#BCAE98", "#F8F2EA"],
            "BLACK": ["#161310", "#76593c", "#161310", "#161310", "#76593c", "#161310", "#161310", "#76593c"],
            "ONYX": ["#3f4144", "#181a1d", "#56595d", "#181a1d", "#4e5154", "#2d2f31", "#2d2f31", "#3f4144"],
            "LUNA": ["#151419", "#a8aaae", "#151419", "#151419", "#a8aaae", "#151419", "#151419", "#d5d8dc"],
            "THISTLE": ["#13110f", "#b89c6c", "#b89c6c", "#13110f", "#13110f", "#13110f", "#13110f", "#b89c6c"],
            "VOID": ["#0f1011", "#0f1011", "#0f1011", "#0f1011", "#0f1011", "#0f1011", "#0f1011", "#0f1011"],
            "SPICE": ["#5e3728", "#2a140c", "#cda781", "#1e1c1a", "#a7794d", "#5e3728", "#512f22", "#825d43"],
            "GINGER": ["#a05f36", "#854219", "#eed9b8", "#1e1c1a", "#caa37a", "#a05f36", "#8e522d", "#bc8c5c"],
            "COPPER": ["#b7702f", "#742a0a", "#f8dfb6", "#080301", "#deba7e", "#b7702f", "#8a501c", "#cda158"],
            "REDWOOD": ["#572f1d", "#422011", "#5e3c26", "#171412", "#5B3622", "#572F1D", "#452A1E", "#5e3c26"],
            "CHOCOLATE": ["#e7caa4", "#a36c48", "#f8ecd6", "#6a4c39", "#f3e3c5", "#6f482f", "#6f482f", "#82583e"],
            "COCOA": ["#6a422e", "#5b3320", "#7d5741", "#512e20", "#7d5741", "#522e20", "#522e20", "#5b3526"],
            "HAZELNUT": ["#cb8d4c", "#a0672e", "#dcaf78", "#4c3826", "#D49E62", "#4C3826", "#4C3826", "#6C4E30"],
            "BLUE": ["#e9d2b4", "#d6ae80", "#f8f3ea", "#897e76", "#f6eddc", "#887e76", "#887e76", "#aba097"],
            "SPRUCE": ["#7d6d63", "#5a514f", "#bcb3ad", "#4c4347", "#bcb3ad", "#564e52", "#564e52", "#665d61"],
            "FROST": ["#efefeb", "#70777c", "#f6f6f0", "#70777c", "#F3F3EE", "#70777c", "#70777c", "#8B9092"],
            "LILAC": ["#f2e9d8", "#ebd2aa", "#fffbf4", "#c4aeae", "#fcf7ec", "#c4aeae", "#c4aeae", "#d4c2c2"],
            "ISABELLA": ["#bbada2", "#d6c3aa", "#ded3c6", "#a99689", "#ded3c6", "#aa988b", "#aa988b", "#bbada2"]
            }
        # set up expectations for markings
        all_markings = ["OPHELIA", "MEXICAN", "GRAYWOLF", "TIMBER", "VIBRANT", "STORMY", "ASPEN", "CALI", "FOXY"] # red, dark + highlights
        both_markings = ["ARCTIC", "SMOKEY", "WINTER", "SHEPHERD", "SABLE", "AGOUTI", "GRIZZLE", "SVALBARD"] # dark + highlights
        dark_markings = ["COLORPOINT", "BRINDLE", "POINTS"] # only dark
        special_markings = ["RUNIC", "SEMISOLID", "SOLID", "HUSKY"] # special kinds of markings
        # SPRITE GENERATION
        # this is gross and don't look at it
        base_name = None
        base_color = None
        tortie_base = None
        tortie_color = None
        if cat.pelt.name not in ['Tortie', 'Calico']:
            base_name = str(cat.pelt.name).upper()
            base_color = str(cat.pelt.colour).upper()
        else:
            base_name = str(cat.pelt.tortiebase).upper()
            base_color = str(cat.pelt.colour).upper()
            tortie_base = str(cat.pelt.tortiepattern).upper()
            tortie_color = str(cat.pelt.tortiecolour).upper()
        black_colors = Pelt.black_colors.copy()
        base_tint = None
        if cat.pelt.points != "ALBINO": # avoid all this shit if it's not needed
            pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
            if cat.pelt.tint != "none":
                base_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                if cat.pelt.tint in sprites.cat_tints["tint_colours"]:
                    base_tint.fill(tuple(sprites.cat_tints["tint_colours"][cat.pelt.tint]))
                elif cat.pelt.tint in sprites.cat_tints["dilute_tint_colours"]:
                    base_tint.fill(tuple(sprites.cat_tints["dilute_tint_colours"][cat.pelt.tint]))
            solid_merle = False
            if cat.pelt.merle:
                # merle pieces for later
                merle_list = cat.pelt.merle_pattern.copy()
                merle_dilute_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                merle_dilute_tint.fill(merle_list[3])
                merle_dark_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                merle_dark_tint.fill(merle_list[1])
                merle_red_tint = None
                if merle_list[2] is not None and base_name != "POINTS":
                    merle_red_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    merle_red_tint.fill(merle_list[2])
                # solid merles are handled differently, so check now
                if base_name == 'solid' or base_name == 'semisolid' or base_color in black_colors:
                    solid_merle = True

            # SETTING UP EACH PIECE
            base_pelt = None
            red_pelt = None
            highlight_pelt = None
            dark_pelt = None

            # pelt marking collection, shortcut for solid merles
            if solid_merle:
                dilute_patch = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                dilute_patch.blit(merle_dilute_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                dark_patch = sprites.sprites["patch" + merle_list[0] + cat_sprite].copy().convert_alpha()
                dark_patch.blit(merle_dark_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                
            elif base_name in special_markings:
                # special markings that require special consideration
                if base_name in ["SEMISOLID", "SOLID"]:
                    base_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    base_tint.fill(color_dict[base_color][5])
                    base_pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                    base_pelt.blit(base_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    dark_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    dark_tint.fill(color_dict[base_color][6])
                    dark_pelt = sprites.sprites['dark' + base_name + cat_sprite].copy().convert_alpha()
                    dark_pelt.blit(dark_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    if base_name == "SEMISOLID":
                        highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        highlight_tint.fill(color_dict[base_color][7])
                        highlight_pelt = sprites.sprites['highlight' + base_name + cat_sprite].copy().convert_alpha()
                        highlight_pelt.blit(highlight_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                else:
                    dark_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    dark_tint.fill(color_dict[base_color][3])
                    dark_pelt = sprites.sprites['dark' + base_name + cat_sprite].copy().convert_alpha()
                    dark_pelt.blit(dark_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    if base_name == "RUNIC":
                        base_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        base_tint.fill(color_dict[base_color][0])
                        base_pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                        base_pelt.blit(base_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        highlight_tint.fill(color_dict[base_color][4])
                        highlight_pelt = sprites.sprites['highlightRUNIC' + cat_sprite].copy().convert_alpha()
                        bright_highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        bright_highlight_tint.fill(color_dict[base_color][2])
                        bright_highlight_pelt = sprites.sprites['highlightRUNICBRIGHT' + cat_sprite].copy().convert_alpha()
                        highlight_pelt.blit(highlight_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        highlight_pelt.blit(bright_highlight_pelt, (0, 0))
                        red_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        red_tint.fill(color_dict[base_color][1])
                        red_pelt = sprites.sprites['redRUNIC' + cat_sprite].copy().convert_alpha()
                        red_pelt.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    elif base_name == "HUSKY":
                        if base_color in ["BLACK", "ONYX"]:
                            base_pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                            base_pelt.blit(dark_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        else:
                            base_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                            base_tint.fill(color_dict[base_color][0])
                            base_pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                            base_pelt.blit(base_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        if base_color in ["REDWOOD", "STEEL", "GOSLING", "BLACK", "ONYX", "LUNA", "VOID", "COCOA", "HAZELNUT", "SPRUCE"]:
                            highlight_pelt = sprites.sprites["highlight" + base_name + cat_sprite].copy().convert_alpha()
                            if cat.pelt.white_patches_tint != "none":
                                highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                                highlight_tint.fill(tuple(sprites.white_patches_tints["tint_colours"][cat.pelt.white_patches_tint]))
                                highlight_pelt.blit(highlight_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        else:
                            highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                            highlight_tint.fill(color_dict[base_color][2])
                            highlight_pelt = sprites.sprites['highlight' + base_name + cat_sprite].copy().convert_alpha()
                            highlight_pelt.blit(highlight_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)        
            else:
                base_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                if base_color in ["BLACK", "LUNA"]:
                    base_tint.fill(color_dict[base_color][1])
                else:
                    base_tint.fill(color_dict[base_color][0])
                base_pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                base_pelt.blit(base_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                if not cat.pelt.merle:
                    dark_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    dark_tint.fill(color_dict[base_color][3])
                    dark_pelt = sprites.sprites['dark' + base_name + cat_sprite].copy().convert_alpha()
                    dark_pelt.blit(dark_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                if base_name not in dark_markings:
                    highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    highlight_tint.fill(color_dict[base_color][2])
                    highlight_pelt = sprites.sprites['highlight' + base_name + cat_sprite].copy().convert_alpha()
                    highlight_pelt.blit(highlight_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    if base_name not in both_markings:
                        red_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        red_tint.fill(color_dict[base_color][1])
                        red_pelt = sprites.sprites['red' + base_name + cat_sprite].copy().convert_alpha()
                        red_pelt.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        
            # tortie pieces
            if tortie_base:
                if tortie_base in special_markings:
                    # special markings that require special consideration
                    if tortie_base in ["SEMISOLID", "SOLID"]:
                        tortie_base_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        tortie_base_tint.fill(color_dict[tortie_color][5])
                        tortie_base_pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                        tortie_base_pelt.blit(tortie_base_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        tortie_dark_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        tortie_dark_tint.fill(color_dict[tortie_color][6])
                        tortie_dark_pelt = sprites.sprites['dark' + tortie_base + cat_sprite].copy().convert_alpha()
                        tortie_dark_pelt.blit(tortie_dark_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        if tortie_base == "SEMISOLID":
                            tortie_highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                            tortie_highlight_tint.fill(color_dict[tortie_color][7])
                            tortie_highlight_pelt = sprites.sprites['highlight' + tortie_base + cat_sprite].copy().convert_alpha()
                            tortie_highlight_pelt.blit(tortie_highlight_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    else:
                        tortie_dark_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        tortie_dark_tint.fill(color_dict[tortie_color][3])
                        tortie_dark_pelt = sprites.sprites['dark' + tortie_base + cat_sprite].copy().convert_alpha()
                        tortie_dark_pelt.blit(tortie_dark_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        if tortie_base == "RUNIC":
                            tortie_base_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                            tortie_base_tint.fill(color_dict[tortie_color][0])
                            tortie_base_pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                            tortie_base_pelt.blit(tortie_base_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                            tortie_highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                            tortie_highlight_tint.fill(color_dict[tortie_color][4])
                            tortie_highlight_pelt = sprites.sprites['highlightRUNIC' + cat_sprite].copy().convert_alpha()
                            tortie_bright_highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                            tortie_bright_highlight_tint.fill(color_dict[tortie_color][2])
                            tortie_bright_highlight_pelt = sprites.sprites['highlightRUNICBRIGHT' + cat_sprite].copy().convert_alpha()
                            tortie_highlight_pelt.blit(tortie_highlight_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                            tortie_highlight_pelt.blit(tortie_bright_highlight_pelt, (0, 0))
                            tortie_red_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                            tortie_red_tint.fill(color_dict[tortie_color][1])
                            tortie_red_pelt = sprites.sprites['redRUNIC' + cat_sprite].copy().convert_alpha()
                            tortie_red_pelt.blit(tortie_red_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        elif tortie_base == "HUSKY":
                            if tortie_color in ["BLACK", "ONYX"]:
                                tortie_base_pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                                tortie_base_pelt.blit(tortie_dark_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                            else:
                                tortie_base_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                                tortie_base_tint.fill(color_dict[tortie_color][0])
                                tortie_base_pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                                tortie_base_pelt.blit(tortie_base_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                            if base_color in ["REDWOOD", "STEEL", "GOSLING", "BLACK", "ONYX", "LUNA", "VOID", "COCOA", "HAZELNUT", "SPRUCE"]:
                                tortie_highlight_pelt = sprites.sprites["highlight" + base_name + cat_sprite].copy().convert_alpha()
                                if cat.pelt.white_patches_tint != "none":
                                    tortie_highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                                    tortie_highlight_tint.fill(tuple(sprites.white_patches_tints["tint_colours"][cat.pelt.white_patches_tint]))
                                    tortie_highlight_pelt.blit(tortie_highlight_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                            else:
                                tortie_highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                                tortie_highlight_tint.fill(color_dict[tortie_color][2])
                                tortie_highlight_pelt = sprites.sprites['highlight' + tortie_base + cat_sprite].copy().convert_alpha()
                                tortie_highlight_pelt.blit(tortie_highlight_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)           
                else:
                    tortie_base_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    if base_color in ["BLACK", "LUNA"]:
                        tortie_base_tint.fill(color_dict[tortie_color][1])
                    else:
                        tortie_base_tint.fill(color_dict[tortie_color][0])
                    tortie_base_pelt = sprites.sprites['baseSOLID' + cat_sprite].copy().convert_alpha()
                    tortie_base_pelt.blit(tortie_base_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    tortie_dark_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    tortie_dark_tint.fill(color_dict[tortie_color][3])
                    tortie_dark_pelt = sprites.sprites['dark' + tortie_base + cat_sprite].copy().convert_alpha()
                    tortie_dark_pelt.blit(tortie_dark_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    if tortie_base not in dark_markings:
                        tortie_highlight_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        tortie_highlight_tint.fill(color_dict[tortie_color][2])
                        tortie_highlight_pelt = sprites.sprites['highlight' + tortie_base + cat_sprite].copy().convert_alpha()
                        tortie_highlight_pelt.blit(tortie_highlight_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        if tortie_base not in both_markings:
                            tortie_red_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                            tortie_red_tint.fill(color_dict[tortie_color][1])
                            tortie_red_pelt = sprites.sprites['red' + tortie_base + cat_sprite].copy().convert_alpha()
                            tortie_red_pelt.blit(tortie_red_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

            # merles that aren't solids
            if not solid_merle and cat.pelt.merle:
                # now all the merling to complete
                dark_pelt = sprites.sprites['dark' + base_name + cat_sprite].copy().convert_alpha()
                dark_pelt.blit(merle_dilute_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                dark_patch = sprites.sprites['dark' + base_name + cat_sprite].copy().convert_alpha()
                dark_patch.blit(merle_dark_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                dark_patch.blit(sprites.sprites["patch" + merle_list[0] + cat_sprite], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                dark_pelt.blit(dark_patch, (0, 0))
                if merle_red_tint != None:
                    red_patch = sprites.sprites["baseSOLID" + cat_sprite].copy().convert_alpha()
                    red_patch.blit(merle_red_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    red_patch.blit(sprites.sprites["patch" + merle_list[0] + cat_sprite], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    base_pelt.blit(red_patch, (0, 0))

            #BUILDING THE PELT FROM PIECES
            if solid_merle:
                pelt.blit(dilute_patch, (0, 0))
                pelt.blit(dark_patch, (0, 0))  
            else:
                pelt.blit(base_pelt, (0, 0))
                if base_name in ["ARCTIC", "GRIZZLE", "SVALBARD"]:
                    pelt.blit(highlight_pelt, (0, 0))
                    pelt.blit(dark_pelt, (0, 0))
                elif base_name in ["OPHELIA", "MEXICAN", "RUNIC", "ASPEN", "CALI", "FOXY"]:
                    pelt.blit(red_pelt, (0, 0))
                    pelt.blit(highlight_pelt, (0, 0))
                    pelt.blit(dark_pelt, (0, 0))
                elif base_name in ["SEMISOLID", "SOLID"]:
                    pelt.blit(dark_pelt, (0, 0))
                    if base_name == "SEMISOLID":
                        pelt.blit(highlight_pelt, (0, 0))
                elif base_name in ["GRAYWOLF", "TIMBER", "VIBRANT", "STORMY"]:
                    pelt.blit(red_pelt, (0, 0))
                    pelt.blit(dark_pelt, (0, 0))
                    pelt.blit(highlight_pelt, (0, 0))
                else:
                    pelt.blit(dark_pelt, (0, 0))
                    if base_name in ["SMOKEY", "WINTER", "HUSKY", "SHEPHERD", "SABLE", "AGOUTI"]:
                        pelt.blit(highlight_pelt, (0, 0))
        
            if tortie_base:
                tortie_pelt = sprites.sprites["baseSOLID" + cat_sprite].copy().convert_alpha()
                tortie_pelt.blit(tortie_base_pelt, (0, 0))
                if tortie_base in ["ARCTIC", "GRIZZLE", "SVALBARD"]:
                    tortie_pelt.blit(tortie_highlight_pelt, (0, 0))
                    tortie_pelt.blit(tortie_dark_pelt, (0, 0))
                elif tortie_base in ["OPHELIA", "MEXICAN", "RUNIC", "ASPEN", "CALI", "FOXY"]:
                    tortie_pelt.blit(tortie_red_pelt, (0, 0))
                    tortie_pelt.blit(tortie_highlight_pelt, (0, 0))
                    tortie_pelt.blit(tortie_dark_pelt, (0, 0))
                elif tortie_base in ["SEMISOLID", "SOLID"]:
                    tortie_pelt.blit(tortie_dark_pelt, (0, 0))
                    if tortie_base == "SEMISOLID":
                        tortie_pelt.blit(tortie_highlight_pelt, (0, 0))
                elif tortie_base in ["GRAYWOLF", "TIMBER", "VIBRANT", "STORMY"]:
                    tortie_pelt.blit(tortie_red_pelt, (0, 0))
                    tortie_pelt.blit(tortie_dark_pelt, (0, 0))
                    tortie_pelt.blit(tortie_highlight_pelt, (0, 0))
                else:
                    tortie_pelt.blit(tortie_dark_pelt, (0, 0))
                    if tortie_base in ["SMOKEY", "WINTER", "HUSKY", "SHEPHERD", "SABLE", "AGOUTI"]:
                        tortie_pelt.blit(tortie_highlight_pelt, (0, 0))
                tortie_pelt.blit(sprites.sprites["patch" + cat.pelt.pattern + cat_sprite], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                pelt.blit(tortie_pelt, (0, 0))

            # apply tints now
            if base_tint != None:
                if cat.pelt.tint in sprites.cat_tints["tint_colours"]:
                    pelt.blit(base_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                elif cat.pelt.tint in sprites.cat_tints["dilute_tint_colours"]:
                    pelt.blit(base_tint, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
                
            if cat.pelt.merle and cat.pelt.harlequin:
                harlequin_base = sprites.sprites["baseSOLID" + cat_sprite].copy().convert_alpha()
                if cat.pelt.white_patches_tint != 'none':
                    tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    tint.fill(tuple(sprites.white_patches_tints["tint_colours"][cat.pelt.white_patches_tint]))
                    harlequin_base.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                pelt.blit(sprites.sprites["patch" + merle_list[0] + cat_sprite], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                new_sprite.blit(harlequin_base, (0, 0))
                new_sprite.blit(pelt, (0, 0))
            else:
                # all normal gen
                new_sprite.blit(pelt, (0, 0))

        # points
        if cat.pelt.points is not None:
            points = sprites.sprites['specialpoint' + cat.pelt.points + cat_sprite].copy()
            if cat.pelt.white_patches_tint != "none":
                tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                tint.fill(
                    tuple(
                        sprites.white_patches_tints["tint_colours"][
                            cat.pelt.white_patches_tint
                        ]
                    )
                )
                points.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            new_sprite.blit(points, (0, 0))

        # draw white patches
        if cat.pelt.white_patches is not None:
            white_patches = sprites.sprites['white' + cat.pelt.white_patches + cat_sprite].copy()
            # Apply tint to white patches.
            if cat.pelt.white_patches_tint != "none":
                tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                tint.fill(tuple(sprites.white_patches_tints["tint_colours"][cat.pelt.white_patches_tint]))
                white_patches.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            new_sprite.blit(white_patches, (0, 0))

        #if cat.pelt.vitiligo:
            #new_sprite.blit(sprites.sprites['white' + cat.pelt.vitiligo + cat_sprite], (0, 0))

        # draw eyes & scars1
        eyes = sprites.sprites["eyes" + cat.pelt.eye_colour + cat_sprite].copy()
        if cat.pelt.eye_colour2 != None:
            eyes.blit(
                sprites.sprites["eyes2" + cat.pelt.eye_colour2 + cat_sprite], (0, 0)
            )
        new_sprite.blit(eyes, (0, 0))

        blendmode = pygame.BLEND_RGBA_MIN
        new_sprite.blit(sprites.sprites['skin' + cat.pelt.skin + cat_sprite], (0, 0))
        # draw line art
        if game.settings["shaders"] and not dead:
            new_sprite.blit(
                sprites.sprites["shaders" + cat_sprite],
                (0, 0),
                special_flags=pygame.BLEND_RGB_MULT,
            )
            new_sprite.blit(sprites.sprites["lighting" + cat_sprite], (0, 0))

        if not dead:
            new_sprite.blit(sprites.sprites["lines" + cat_sprite], (0, 0))
        elif cat.df:
            new_sprite.blit(sprites.sprites['lineartdf' + cat_sprite], (0, 0))
            
        # draw skin and scars2
        if not scars_hidden:
            for scar in cat.pelt.scars:
                if scar in cat.pelt.scars1:
                    new_sprite.blit(sprites.sprites['scars' + scar + cat_sprite], (0, 0))
                if scar in cat.pelt.scars3:
                    new_sprite.blit(sprites.sprites['scars' + scar + cat_sprite], (0, 0))
        
        if not scars_hidden and not dead or cat.df and not scars_hidden:
            for scar in cat.pelt.scars:
                if scar in cat.pelt.scars2:
                    new_sprite.blit(sprites.sprites['scarsmissing' + scar + cat_sprite], (0, 0), special_flags=blendmode)
                    new_sprite.blit(sprites.sprites['scars' + scar + cat_sprite], (0, 0))

        # kori's fun glitter friends
        glitter = {
            'DAYLIGHT': (120, 215, 216),
            'ICE': (233, 255, 255),
            'NAVY': (47, 63, 114),
            'RAIN': (87, 145, 178),
            'SAPPHIRE': (15, 21, 114),
            'SEAFOAM': (179, 239, 220),
            'SKY': (124, 216, 217),
            'STORM': (142, 168, 199),
            'TEAL': (88, 186, 185), 
	'ALMOND': (163, 95, 29),
            'BEAR': (111, 68, 43),
            'CASHEW': (237, 189, 151),
            'HAZEL': (160, 183, 98),
            'LATTE': (185, 134, 85),
            'SPARROW': (110, 78, 62),
            'BLACK': (30, 33, 35),
            'GULL': (164, 180, 183), 
	'SILVER': (232, 240, 241),
            'SMOKE': (214, 224, 226),
            'WHITE': (255, 255, 255),
            'EMERALD': (81, 150, 48),
            'FERN': (189, 212, 148),
            'FOREST': (154, 184, 102),
            'LEAF': (113, 168, 86),
            'LIME': (203, 232, 103), 
            'MINT': (229, 250, 196),
            'HARVEST': (255, 157, 20),
            'PEACH': (237, 184, 137),
            'PUMPKIN': (239, 137, 27),
            'TANGELO': (206, 103, 17),
            'TWILIGHT': (222, 122, 10),
            'AMETHYST': (170, 114, 199),
            'DAWN': (255, 251, 205),
            'DUSK': (168, 79, 94),
            'LILAC': (218, 199, 228),
            'MIDNIGHT': (90, 60, 99),
            'VIOLET': (141, 77, 157),
            'BUBBLEGUM': (255, 210, 210), 
	'PINK': (235, 183, 189),
            'ROUGE': (245, 133, 94),
            'RUBY': (174, 0, 0),
            'SCARLET': (225, 77, 73),
            'AMBER': (244, 220, 55),
            'LEMON': (247, 240, 127),
            'PALE': (255, 251, 205),
            'SUNBEAM': (249, 236, 162),
            'SUNLIGHT': (239, 232, 121), 
	'WHEAT': (223, 225, 159)
            }
        
        # draw accessories
        if not acc_hidden and not dead or cat.df and not scars_hidden:        
            if cat.pelt.accessory in cat.pelt.plant_accessories:
                new_sprite.blit(sprites.sprites['natural' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.wild_accessories:
                new_sprite.blit(sprites.sprites['natural' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.collars:
                new_sprite.blit(sprites.sprites['collars' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.radiocollars:
                new_sprite.blit(sprites.sprites['collars' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.harnesses:
                new_sprite.blit(sprites.sprites['collars' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.bandanas:
                new_sprite.blit(sprites.sprites['collars' + cat.pelt.accessory + cat_sprite], (0, 0))
            elif cat.pelt.accessory in cat.pelt.special_accessories:
                if cat.pelt.accessory in ["HIBISCUS", "RED HIBISCUS", "WHITE HIBISCUS", "BIG LEAVES", "STARFISH", "PINK STARFISH", "PURPLE STARFISH", "PEARLS", "SEASHELLS"]:
                    new_sprite.blit(sprites.sprites['natural' + cat.pelt.accessory + cat_sprite], (0, 0))
                elif cat.pelt.accessory == "TOWEL":
                    new_sprite.blit(sprites.sprites['junk' + cat.pelt.accessory + cat_sprite], (0, 0))
                elif cat.pelt.accessory == "SILK CLOAK":
                    cloak = sprites.sprites["cloakSILK CLOAK" + cat_sprite].copy()
                    cloak_color = glitter[str(cat.pelt.eye_colour)]
                    cloak_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    cloak_tint.fill(cloak_color)
                    cloak.blit(cloak_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    new_sprite.blit(cloak, (0, 0))

        
        if dead and not cat.df:
            new_sprite.blit(sprites.sprites['lines' + cat_sprite], (0, 0))
            if not scars_hidden:
                for scar in cat.pelt.scars:
                    if scar in cat.pelt.scars2:
                        new_sprite.blit(sprites.sprites['scarsmissing' + scar + cat_sprite], (0, 0), special_flags=blendmode)
                        new_sprite.blit(sprites.sprites['scars' + scar + cat_sprite], (0, 0))
            if not acc_hidden:        
                if cat.pelt.accessory in cat.pelt.plant_accessories:
                    new_sprite.blit(sprites.sprites['natural' + cat.pelt.accessory + cat_sprite], (0, 0))
                elif cat.pelt.accessory in cat.pelt.wild_accessories:
                    new_sprite.blit(sprites.sprites['natural' + cat.pelt.accessory + cat_sprite], (0, 0))
                elif cat.pelt.accessory in cat.pelt.collars:
                    new_sprite.blit(sprites.sprites['collars' + cat.pelt.accessory + cat_sprite], (0, 0))
                elif cat.pelt.accessory in cat.pelt.radiocollars:
                    new_sprite.blit(sprites.sprites['collars' + cat.pelt.accessory + cat_sprite], (0, 0))
                elif cat.pelt.accessory in cat.pelt.harnesses:
                    new_sprite.blit(sprites.sprites['collars' + cat.pelt.accessory + cat_sprite], (0, 0))
                elif cat.pelt.accessory in cat.pelt.bandanas:
                    new_sprite.blit(sprites.sprites['collars' + cat.pelt.accessory + cat_sprite], (0, 0))
                elif cat.pelt.accessory in cat.pelt.special_accessories:
                    if cat.pelt.accessory in ["HIBISCUS", "RED HIBISCUS", "WHITE HIBISCUS", "BIG LEAVES", "STARFISH", "PINK STARFISH", "PURPLE STARFISH", "PEARLS", "SEASHELLS"]:
                        new_sprite.blit(sprites.sprites['natural' + cat.pelt.accessory + cat_sprite], (0, 0))
                    elif cat.pelt.accessory == "TOWEL":
                        new_sprite.blit(sprites.sprites['junk' + cat.pelt.accessory + cat_sprite], (0, 0))
                    elif cat.pelt.accessory == "SILK CLOAK":
                        cloak = sprites.sprites["cloakSILK CLOAK" + cat_sprite].copy()
                        cloak_color = glitter[str(cat.pelt.eye_colour)]
                        cloak_tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                        cloak_tint.fill(cloak_color)
                        cloak.blit(cloak_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                        new_sprite.blit(cloak, (0, 0))
            deadglitter = sprites.sprites['lineartdead' + cat_sprite].copy()
            deadcolor = glitter[str(cat.pelt.eye_colour)]
            deadtint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
            deadtint.fill(deadcolor)
            deadglitter.blit(deadtint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            new_sprite.blit(deadglitter, (0, 0))

        # Apply fading fog
        if (
                cat.pelt.opacity <= 97
                and not cat.prevent_fading
                and game.clan.clan_settings["fading"]
                and dead
        ):

            stage = "0"
            if 80 >= cat.pelt.opacity > 45:
                # Stage 1
                stage = "1"
            elif cat.pelt.opacity <= 45:
                # Stage 2
                stage = "2"

            new_sprite.blit(
                sprites.sprites["fademask" + stage + cat_sprite],
                (0, 0),
                special_flags=pygame.BLEND_RGBA_MULT,
            )

            if cat.df:
                temp = sprites.sprites["fadedf" + stage + cat_sprite].copy()
                temp.blit(new_sprite, (0, 0))
                new_sprite = temp
            else:
                temp = sprites.sprites['fadestarclan' + stage + cat_sprite].copy()
                #temp.blit(new_sprite, (0, 0))
                #new_sprite = temp
                deadtint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                deadtint.fill(deadcolor)
                temp.blit(deadtint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                new_sprite.blit(temp, (0, 0))

        # reverse, if assigned so
        if cat.pelt.reverse:
            new_sprite = pygame.transform.flip(new_sprite, True, False)

    except (TypeError, KeyError):
        logger.exception("Failed to load sprite")

        # Placeholder image
        new_sprite = image_cache.load_image(
            f"sprites/error_placeholder.png"
        ).convert_alpha()

    return new_sprite


def apply_opacity(surface, opacity):
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            pixel = list(surface.get_at((x, y)))
            pixel[3] = int(pixel[3] * opacity / 100)
            surface.set_at((x, y), tuple(pixel))
    return surface


# ---------------------------------------------------------------------------- #
#                                     OTHER                                    #
# ---------------------------------------------------------------------------- #


def chunks(L, n):
    return [L[x: x + n] for x in range(0, len(L), n)]


def is_iterable(y):
    try:
        0 in y
    except TypeError:
        return False


def get_text_box_theme(theme_name=""):
    """Updates the name of the theme based on dark or light mode"""
    if game.settings["dark mode"]:
        if theme_name == "":
            return "#default_dark"
        else:
            return theme_name + "_dark"
    else:
        if theme_name == "":
            return "#text_box"
        else:
            return theme_name


def quit(savesettings=False, clearevents=False):
    """
    Quits the game, avoids a bunch of repeated lines
    """
    if savesettings:
        game.save_settings()
    if clearevents:
        game.cur_events_list.clear()
    game.rpc.close_rpc.set()
    game.rpc.update_rpc.set()
    pygame.display.quit()
    pygame.quit()
    if game.rpc.is_alive():
        game.rpc.join(1)
    sys_exit()


with open(f"resources/dicts/conditions/permanent_conditions.json", "r") as read_file:
    PERMANENT = ujson.loads(read_file.read())

with open(f"resources/dicts/acc_display.json", "r") as read_file:
    ACC_DISPLAY = ujson.loads(read_file.read())

with open(f"resources/dicts/snippet_collections.json", "r") as read_file:
    SNIPPETS = ujson.loads(read_file.read())

with open(f"resources/dicts/prey_text_replacements.json", "r") as read_file:
    PREY_LISTS = ujson.loads(read_file.read())

with open(f"resources/dicts/backstories.json", "r") as read_file:
    BACKSTORIES = ujson.loads(read_file.read())
