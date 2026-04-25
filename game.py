#!/usr/bin/env python3
"""
Satanic Pimp: Underworld Chronicles
A text-based MMORPG set in the infernal underworld.
Play as a rising Pimp Devil, building your empire from the streets of Hell.
"""

import random
import time
import json
import os
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

__author__ = "doughboyP"
__version__ = "1.0.0"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SAVE_FILE = "savegame.json"

TITLE_ART = r"""
  ____        _              _        ____  _
 / ___|  __ _| |_ __ _ _ __ (_) ___  |  _ \(_)_ __ ___  _ __
 \___ \ / _` | __/ _` | '_ \| |/ __| | |_) | | '_ ` _ \| '_ \
  ___) | (_| | || (_| | | | | | (__  |  __/| | | | | | | |_) |
 |____/ \__,_|\__\__,_|_| |_|_|\___| |_|   |_|_| |_| |_| .__/
                                                          |_|
          U N D E R W O R L D   C H R O N I C L E S
"""

# ---------------------------------------------------------------------------
# Data definitions — items, enemies, quests, locations
# ---------------------------------------------------------------------------

ITEM_CATALOG = {
    "rusty_pitchfork": {
        "name": "Rusty Pitchfork",
        "type": "weapon",
        "atk_bonus": 5,
        "value": 30,
        "description": "A well-worn pitchfork, favored by low-ranking imps.",
    },
    "hellfire_cane": {
        "name": "Hellfire Cane",
        "type": "weapon",
        "atk_bonus": 14,
        "value": 120,
        "description": "A stylish obsidian cane that crackles with hellfire.",
    },
    "soul_blade": {
        "name": "Soul Blade",
        "type": "weapon",
        "atk_bonus": 25,
        "value": 350,
        "description": "Forged from the crystallised screams of a thousand souls.",
    },
    "demon_king_sceptre": {
        "name": "Demon King Sceptre",
        "type": "weapon",
        "atk_bonus": 45,
        "value": 1000,
        "description": "The ultimate symbol of infernal authority.",
    },
    "sinners_rags": {
        "name": "Sinner's Rags",
        "type": "armor",
        "def_bonus": 3,
        "value": 20,
        "description": "Tattered robes stripped from a freshly arrived sinner.",
    },
    "brimstone_suit": {
        "name": "Brimstone Suit",
        "type": "armor",
        "def_bonus": 12,
        "value": 150,
        "description": "A sharp three-piece suit woven from compressed brimstone.",
    },
    "shadow_cloak": {
        "name": "Shadow Cloak",
        "type": "armor",
        "def_bonus": 22,
        "value": 400,
        "description": "A flowing cloak made from solidified shadows of the abyss.",
    },
    "infernal_plate": {
        "name": "Infernal Plate",
        "type": "armor",
        "def_bonus": 38,
        "value": 900,
        "description": "Heavy obsidian armor, nearly impervious to mortal weapons.",
    },
    "health_potion": {
        "name": "Health Potion",
        "type": "consumable",
        "heal": 40,
        "value": 25,
        "description": "A vial of glowing red liquid that restores vitality.",
    },
    "greater_health_potion": {
        "name": "Greater Health Potion",
        "type": "consumable",
        "heal": 100,
        "value": 75,
        "description": "A potent brew that restores a large amount of health.",
    },
    "soul_essence": {
        "name": "Soul Essence",
        "type": "quest_item",
        "value": 50,
        "description": "The distilled essence of a captured soul.",
    },
    "demon_horn": {
        "name": "Demon Horn",
        "type": "quest_item",
        "value": 80,
        "description": "A jagged horn from a slain demon, useful for dark rituals.",
    },
    "gold_coin_pouch": {
        "name": "Gold Coin Pouch",
        "type": "misc",
        "value": 100,
        "description": "A leather pouch heavy with infernal gold coins.",
    },
    "street_rep_badge": {
        "name": "Street Rep Badge",
        "type": "misc",
        "value": 200,
        "description": "A badge that marks you as a major player in the underworld.",
    },
}

ENEMY_CATALOG = {
    "imp": {
        "name": "Imp",
        "hp": 30,
        "atk": 6,
        "defense": 2,
        "xp": 20,
        "gold": (5, 15),
        "loot": [("health_potion", 0.25)],
        "description": "A small, cackling imp looking for trouble.",
    },
    "lost_soul": {
        "name": "Lost Soul",
        "hp": 45,
        "atk": 10,
        "defense": 4,
        "xp": 35,
        "gold": (8, 20),
        "loot": [("soul_essence", 0.40)],
        "description": "A tormented soul wandering the infernal wastes.",
    },
    "hellhound": {
        "name": "Hellhound",
        "hp": 70,
        "atk": 16,
        "defense": 6,
        "xp": 60,
        "gold": (15, 35),
        "loot": [("health_potion", 0.30), ("demon_horn", 0.20)],
        "description": "A massive hound wreathed in dark flames.",
    },
    "succubus": {
        "name": "Succubus",
        "hp": 90,
        "atk": 22,
        "defense": 10,
        "xp": 100,
        "gold": (25, 60),
        "loot": [("greater_health_potion", 0.25), ("soul_essence", 0.35)],
        "description": "A cunning and dangerous seductress of the underworld.",
    },
    "rival_pimp": {
        "name": "Rival Pimp",
        "hp": 120,
        "atk": 28,
        "defense": 14,
        "xp": 150,
        "gold": (50, 100),
        "loot": [
            ("brimstone_suit", 0.15),
            ("greater_health_potion", 0.40),
            ("street_rep_badge", 0.10),
        ],
        "description": "A ruthless competitor trying to muscle in on your turf.",
    },
    "demon_lord": {
        "name": "Demon Lord",
        "hp": 250,
        "atk": 40,
        "defense": 22,
        "xp": 400,
        "gold": (100, 200),
        "loot": [
            ("soul_blade", 0.20),
            ("shadow_cloak", 0.20),
            ("greater_health_potion", 0.60),
        ],
        "description": "A towering Demon Lord who commands legions of the damned.",
    },
    "arch_devil": {
        "name": "Arch Devil",
        "hp": 500,
        "atk": 60,
        "defense": 35,
        "xp": 1000,
        "gold": (200, 400),
        "loot": [
            ("demon_king_sceptre", 0.30),
            ("infernal_plate", 0.30),
            ("greater_health_potion", 1.00),
        ],
        "description": "The most feared being in all of Hell — an Arch Devil in full fury.",
    },
}

LOCATION_DATA = {
    "sinners_alley": {
        "name": "Sinner's Alley",
        "description": (
            "A grimy back-street of the underworld, crawling with fresh sinners "
            "and petty imps. The air reeks of sulfur and cheap brimstone whiskey."
        ),
        "enemies": ["imp", "lost_soul"],
        "min_level": 1,
        "shop": True,
        "shop_items": [
            "rusty_pitchfork",
            "sinners_rags",
            "health_potion",
        ],
    },
    "infernal_bazaar": {
        "name": "Infernal Bazaar",
        "description": (
            "A sprawling market where demons hawk stolen goods and soul contracts. "
            "The neon hellfire signs flicker over endless stalls."
        ),
        "enemies": ["lost_soul", "hellhound"],
        "min_level": 3,
        "shop": True,
        "shop_items": [
            "hellfire_cane",
            "brimstone_suit",
            "health_potion",
            "greater_health_potion",
        ],
    },
    "pit_of_despair": {
        "name": "Pit of Despair",
        "description": (
            "A vast crater where condemned souls are put to work for eternity. "
            "Powerful creatures lurk at the edges, hunting the weak."
        ),
        "enemies": ["hellhound", "succubus"],
        "min_level": 6,
        "shop": False,
        "shop_items": [],
    },
    "devils_boulevard": {
        "name": "Devil's Boulevard",
        "description": (
            "The main drag of Hell City — flashy, dangerous, and profitable. "
            "Rival pimps and demons compete viciously for control."
        ),
        "enemies": ["succubus", "rival_pimp"],
        "min_level": 10,
        "shop": True,
        "shop_items": [
            "soul_blade",
            "shadow_cloak",
            "greater_health_potion",
        ],
    },
    "infernal_palace": {
        "name": "Infernal Palace",
        "description": (
            "The seat of power in the underworld — gleaming obsidian towers "
            "and rivers of lava surround this fortress of pure evil."
        ),
        "enemies": ["rival_pimp", "demon_lord"],
        "min_level": 15,
        "shop": True,
        "shop_items": [
            "demon_king_sceptre",
            "infernal_plate",
            "greater_health_potion",
        ],
    },
    "abyss_throne": {
        "name": "The Abyss Throne",
        "description": (
            "The deepest, most terrifying realm of Hell. Only the mightiest dare "
            "set foot here. The Arch Devil sits upon a throne of crushed bones."
        ),
        "enemies": ["demon_lord", "arch_devil"],
        "min_level": 20,
        "shop": False,
        "shop_items": [],
    },
}

QUEST_DATA = {
    "q01_street_cred": {
        "id": "q01_street_cred",
        "name": "Street Credibility",
        "giver": "Mammon the Broker",
        "description": (
            "Mammon needs someone to rough up some imps that are squatting on prime "
            "corner space. Defeat 5 Imps in Sinner's Alley."
        ),
        "objectives": [{"type": "kill", "enemy": "imp", "count": 5, "current": 0}],
        "reward_xp": 80,
        "reward_gold": 60,
        "reward_item": "hellfire_cane",
        "location": "sinners_alley",
        "min_level": 1,
        "completed": False,
        "active": False,
    },
    "q02_soul_collection": {
        "id": "q02_soul_collection",
        "name": "Soul Collection",
        "giver": "Lady Lilith",
        "description": (
            "Lady Lilith requires 4 Soul Essences for a ritual. Collect them from "
            "Lost Souls haunting the Infernal Bazaar."
        ),
        "objectives": [
            {"type": "collect", "item": "soul_essence", "count": 4, "current": 0}
        ],
        "reward_xp": 150,
        "reward_gold": 120,
        "reward_item": "brimstone_suit",
        "location": "infernal_bazaar",
        "min_level": 3,
        "completed": False,
        "active": False,
    },
    "q03_hound_hunt": {
        "id": "q03_hound_hunt",
        "name": "Hellhound Patrol",
        "giver": "Sergeant Bael",
        "description": (
            "A pack of rogue hellhounds has broken loose in the Pit of Despair. "
            "Put down 3 of them before they cause more chaos."
        ),
        "objectives": [
            {"type": "kill", "enemy": "hellhound", "count": 3, "current": 0}
        ],
        "reward_xp": 250,
        "reward_gold": 200,
        "reward_item": "shadow_cloak",
        "location": "pit_of_despair",
        "min_level": 6,
        "completed": False,
        "active": False,
    },
    "q04_turf_war": {
        "id": "q04_turf_war",
        "name": "Turf War",
        "giver": "The Don of Hell",
        "description": (
            "Rival Pimps are encroaching on your territory on Devil's Boulevard. "
            "Take down 4 Rival Pimps to assert dominance."
        ),
        "objectives": [
            {"type": "kill", "enemy": "rival_pimp", "count": 4, "current": 0}
        ],
        "reward_xp": 500,
        "reward_gold": 400,
        "reward_item": "soul_blade",
        "location": "devils_boulevard",
        "min_level": 10,
        "completed": False,
        "active": False,
    },
    "q05_final_ascension": {
        "id": "q05_final_ascension",
        "name": "Final Ascension",
        "giver": "Ancient Prophecy",
        "description": (
            "An ancient prophecy foretells that one Pimp Devil will overthrow the "
            "Arch Devil and claim the Abyss Throne. Defeat the Arch Devil to "
            "complete your destiny and rule all of Hell."
        ),
        "objectives": [
            {"type": "kill", "enemy": "arch_devil", "count": 1, "current": 0}
        ],
        "reward_xp": 5000,
        "reward_gold": 2000,
        "reward_item": "demon_king_sceptre",
        "location": "abyss_throne",
        "min_level": 20,
        "completed": False,
        "active": False,
    },
}

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def slow_print(text: str, delay: float = 0.03) -> None:
    """Print text character-by-character for dramatic effect."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def divider(char: str = "─", width: int = 60) -> None:
    print(char * width)


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def prompt_choice(options: list, prompt: str = "Choose: ") -> int:
    """Display numbered options and return the 0-based index of the choice."""
    for idx, option in enumerate(options, 1):
        print(f"  [{idx}] {option}")
    while True:
        try:
            raw = input(prompt).strip()
            choice = int(raw)
            if 1 <= choice <= len(options):
                return choice - 1
        except (ValueError, EOFError):
            pass
        print(f"  Please enter a number between 1 and {len(options)}.")


def get_yes_no(prompt: str) -> bool:
    """Prompt the user for a yes/no answer."""
    while True:
        raw = input(prompt + " [y/n]: ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False


# ---------------------------------------------------------------------------
# XP / Level table
# ---------------------------------------------------------------------------

XP_TABLE = [0, 100, 250, 450, 700, 1000, 1400, 1900, 2500, 3200, 4000,
            5000, 6200, 7600, 9200, 11000, 13000, 15500, 18500, 22000, 26000]

MAX_LEVEL = len(XP_TABLE) - 1


def xp_for_level(level: int) -> int:
    if level >= MAX_LEVEL:
        return XP_TABLE[MAX_LEVEL]
    return XP_TABLE[level]


# ---------------------------------------------------------------------------
# Character classes
# ---------------------------------------------------------------------------

CLASS_DATA = {
    "Pimp Devil": {
        "description": "Charismatic and cunning. High starting gold, balanced stats.",
        "base_hp": 120,
        "base_atk": 15,
        "base_def": 10,
        "gold_bonus": 50,
        "skill": "Silver Tongue",
        "skill_desc": "Charm an enemy, reducing their attack by 30% for 3 rounds.",
    },
    "Hellfire Mage": {
        "description": "Master of infernal magic. High attack, low defense.",
        "base_hp": 90,
        "base_atk": 22,
        "base_def": 6,
        "gold_bonus": 20,
        "skill": "Hellfire Blast",
        "skill_desc": "Unleash a torrent of hellfire dealing 2x normal damage.",
    },
    "Bone Crusher": {
        "description": "Brute-force warrior. Very high HP and defense, low attack.",
        "base_hp": 160,
        "base_atk": 12,
        "base_def": 18,
        "gold_bonus": 20,
        "skill": "Infernal Rage",
        "skill_desc": "Enter a rage state, doubling your attack for 2 rounds.",
    },
    "Shadow Rogue": {
        "description": "Stealthy and lethal. High crit chance, low HP.",
        "base_hp": 100,
        "base_atk": 18,
        "base_def": 8,
        "gold_bonus": 30,
        "skill": "Shadow Strike",
        "skill_desc": "A guaranteed critical hit dealing 2.5x damage.",
    },
}


# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------


@dataclass
class Player:
    name: str
    char_class: str
    level: int = 1
    xp: int = 0
    gold: int = 0
    max_hp: int = 100
    current_hp: int = 100
    base_atk: int = 10
    base_def: int = 5
    weapon: Optional[str] = None
    armor: Optional[str] = None
    inventory: dict = field(default_factory=dict)
    quests: dict = field(default_factory=dict)
    current_location: str = "sinners_alley"
    skill_cooldown: int = 0
    kills: dict = field(default_factory=dict)
    collected_items: dict = field(default_factory=dict)
    game_won: bool = False

    # --- derived stats ---

    @property
    def attack(self) -> int:
        bonus = 0
        if self.weapon and self.weapon in ITEM_CATALOG:
            bonus = ITEM_CATALOG[self.weapon].get("atk_bonus", 0)
        return self.base_atk + bonus

    @property
    def defense(self) -> int:
        bonus = 0
        if self.armor and self.armor in ITEM_CATALOG:
            bonus = ITEM_CATALOG[self.armor].get("def_bonus", 0)
        return self.base_def + bonus

    # --- inventory helpers ---

    def add_item(self, item_key: str, qty: int = 1) -> None:
        self.inventory[item_key] = self.inventory.get(item_key, 0) + qty

    def remove_item(self, item_key: str, qty: int = 1) -> bool:
        if self.inventory.get(item_key, 0) >= qty:
            self.inventory[item_key] -= qty
            if self.inventory[item_key] == 0:
                del self.inventory[item_key]
            return True
        return False

    def has_item(self, item_key: str, qty: int = 1) -> bool:
        return self.inventory.get(item_key, 0) >= qty

    # --- HP helpers ---

    def heal(self, amount: int) -> int:
        before = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - before

    def take_damage(self, amount: int) -> int:
        mitigated = max(1, amount - self.defense)
        self.current_hp = max(0, self.current_hp - mitigated)
        return mitigated

    def is_alive(self) -> bool:
        return self.current_hp > 0

    # --- levelling ---

    def grant_xp(self, amount: int) -> list:
        """Grant XP and return a list of level-up messages."""
        messages = []
        self.xp += amount
        while self.level < MAX_LEVEL and self.xp >= xp_for_level(self.level + 1):
            self.level_up()
            messages.append(
                f"🎉  LEVEL UP! You are now level {self.level}!"
            )
        return messages

    def level_up(self) -> None:
        self.level += 1
        hp_gain = random.randint(8, 15)
        atk_gain = random.randint(1, 3)
        def_gain = random.randint(1, 2)
        self.max_hp += hp_gain
        self.base_atk += atk_gain
        self.base_def += def_gain
        self.current_hp = self.max_hp  # full heal on level up

    def xp_to_next(self) -> int:
        if self.level >= MAX_LEVEL:
            return 0
        return xp_for_level(self.level + 1) - self.xp

    # --- status display ---

    def status_bar(self) -> str:
        hp_pct = self.current_hp / self.max_hp
        filled = int(hp_pct * 20)
        bar = "█" * filled + "░" * (20 - filled)
        return (
            f"HP [{bar}] {self.current_hp}/{self.max_hp}  "
            f"ATK:{self.attack}  DEF:{self.defense}  "
            f"LV:{self.level}  XP:{self.xp}/{xp_for_level(min(self.level+1, MAX_LEVEL))}"
        )

    # --- serialisation ---

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        return cls(**data)


# ---------------------------------------------------------------------------
# Combat engine
# ---------------------------------------------------------------------------


class CombatResult:
    WIN = "win"
    LOSE = "lose"
    FLEE = "flee"


def run_combat(player: Player, enemy_key: str) -> str:
    """Run a full combat encounter and return a CombatResult."""
    template = ENEMY_CATALOG[enemy_key]
    enemy_hp = template["hp"]
    enemy_max_hp = template["hp"]
    enemy_name = template["name"]
    enemy_atk = template["atk"]
    enemy_def = template["defense"]
    round_num = 0
    skill_active = False
    skill_rounds_left = 0
    rage_active = False
    rage_rounds_left = 0

    divider()
    slow_print(f"⚔  A {enemy_name} appears!  {template['description']}")
    divider()

    while True:
        round_num += 1
        print(f"\n--- Round {round_num} ---")
        print(f"  {player.name}: {player.current_hp}/{player.max_hp} HP")
        hp_pct = enemy_hp / enemy_max_hp
        bar_filled = int(hp_pct * 20)
        enemy_bar = "█" * bar_filled + "░" * (20 - bar_filled)
        print(f"  {enemy_name}: [{enemy_bar}] {enemy_hp}/{enemy_max_hp} HP")

        # Skill cooldown tick
        if player.skill_cooldown > 0:
            player.skill_cooldown -= 1

        # Build action menu
        actions = ["Attack", "Use Item"]
        skill_name = CLASS_DATA[player.char_class]["skill"]
        if player.skill_cooldown == 0:
            actions.append(f"Use Skill: {skill_name}")
        actions.append("Flee")

        print()
        choice_idx = prompt_choice(actions, "Your action: ")
        chosen = actions[choice_idx]

        # --- ATTACK ---
        if chosen == "Attack":
            dmg = max(1, player.attack - enemy_def + random.randint(-3, 5))
            crit = random.random() < 0.10
            if crit:
                dmg = int(dmg * 1.5)
                print(f"  💥 Critical hit! You strike {enemy_name} for {dmg} damage!")
            else:
                print(f"  ⚔  You strike {enemy_name} for {dmg} damage.")
            enemy_hp -= dmg

        # --- USE ITEM ---
        elif chosen == "Use Item":
            consumables = {
                k: v
                for k, v in player.inventory.items()
                if ITEM_CATALOG.get(k, {}).get("type") == "consumable"
            }
            if not consumables:
                print("  You have no consumable items!")
            else:
                item_keys = list(consumables.keys())
                item_labels = [
                    f"{ITEM_CATALOG[k]['name']} x{v}  — {ITEM_CATALOG[k]['description']}"
                    for k, v in consumables.items()
                ]
                item_labels.append("Cancel")
                item_keys.append(None)
                pick = prompt_choice(item_labels, "Use which item? ")
                item_key = item_keys[pick]
                if item_key:
                    heal_amount = ITEM_CATALOG[item_key]["heal"]
                    healed = player.heal(heal_amount)
                    player.remove_item(item_key)
                    print(f"  💊 You use {ITEM_CATALOG[item_key]['name']} and restore {healed} HP.")
                else:
                    print("  Cancelled.")

        # --- USE SKILL ---
        elif chosen.startswith("Use Skill"):
            player.skill_cooldown = 5

            if player.char_class == "Pimp Devil":
                # Silver Tongue: reduce enemy atk
                skill_active = True
                skill_rounds_left = 3
                print(
                    f"  🎩  You flash your most dazzling smile. {enemy_name} is charmed! "
                    f"Their attack is reduced for {skill_rounds_left} rounds."
                )
            elif player.char_class == "Hellfire Mage":
                # Hellfire Blast: 2x damage
                dmg = max(1, player.attack * 2 - enemy_def + random.randint(0, 8))
                enemy_hp -= dmg
                print(
                    f"  🔥 Hellfire Blast! You engulf {enemy_name} in infernal fire "
                    f"dealing {dmg} damage!"
                )
            elif player.char_class == "Bone Crusher":
                # Infernal Rage: double atk for 2 rounds
                rage_active = True
                rage_rounds_left = 2
                print(
                    f"  💢 Infernal Rage! Your eyes glow red. Attack doubled for "
                    f"{rage_rounds_left} rounds!"
                )
            elif player.char_class == "Shadow Rogue":
                # Shadow Strike: 2.5x guaranteed crit
                dmg = int(max(1, player.attack - enemy_def + random.randint(0, 6)) * 2.5)
                enemy_hp -= dmg
                print(
                    f"  🗡  Shadow Strike! You emerge from the darkness and deal "
                    f"{dmg} devastating damage to {enemy_name}!"
                )

        # --- FLEE ---
        elif chosen == "Flee":
            flee_chance = 0.45
            if random.random() < flee_chance:
                slow_print(f"  🏃  You manage to escape from {enemy_name}!")
                return CombatResult.FLEE
            else:
                slow_print(f"  {enemy_name} cuts off your escape! You cannot flee!")

        # Apply rage bonus attack if active
        if rage_active and chosen == "Attack":
            bonus_dmg = max(1, player.attack - enemy_def + random.randint(0, 4))
            enemy_hp -= bonus_dmg
            print(f"  💢 Rage bonus strikes {enemy_name} for an additional {bonus_dmg} damage!")
            rage_rounds_left -= 1
            if rage_rounds_left <= 0:
                rage_active = False
                print("  Your rage subsides.")

        # Check enemy death
        if enemy_hp <= 0:
            slow_print(f"\n  ☠  {enemy_name} has been defeated!")
            _handle_combat_rewards(player, enemy_key, template)
            return CombatResult.WIN

        # --- ENEMY TURN ---
        effective_atk = enemy_atk
        if skill_active:
            effective_atk = int(enemy_atk * 0.70)
            skill_rounds_left -= 1
            if skill_rounds_left <= 0:
                skill_active = False
                print(f"  {enemy_name}'s attack recovers to normal.")

        raw_dmg = effective_atk + random.randint(-3, 5)
        damage_taken = player.take_damage(raw_dmg)
        print(f"\n  {enemy_name} attacks you for {damage_taken} damage.")

        if not player.is_alive():
            slow_print(f"\n  💀 You have been slain by {enemy_name}!")
            return CombatResult.LOSE

    return CombatResult.LOSE  # unreachable, satisfies type checkers


def _handle_combat_rewards(player: Player, enemy_key: str, template: dict) -> None:
    """Distribute XP, gold, and loot after a combat win."""
    gold_earned = random.randint(*template["gold"])
    player.gold += gold_earned

    xp_msgs = player.grant_xp(template["xp"])
    print(f"\n  💰 You earned {gold_earned} gold and {template['xp']} XP.")
    for msg in xp_msgs:
        slow_print(f"  {msg}")

    # Loot drops
    for item_key, drop_chance in template.get("loot", []):
        if random.random() < drop_chance:
            player.add_item(item_key)
            item_name = ITEM_CATALOG[item_key]["name"]
            print(f"  📦 {enemy_name_from_key(enemy_key)} dropped: {item_name}")

    # Track kills for quest objectives
    player.kills[enemy_key] = player.kills.get(enemy_key, 0) + 1

    # Update active kill quests
    for qid, quest in player.quests.items():
        if quest["active"] and not quest["completed"]:
            for obj in quest["objectives"]:
                if obj["type"] == "kill" and obj["enemy"] == enemy_key:
                    if obj["current"] < obj["count"]:
                        obj["current"] += 1
                        print(
                            f"  📜 Quest '{quest['name']}': {obj['current']}/{obj['count']} "
                            f"{ENEMY_CATALOG[enemy_key]['name']}s defeated."
                        )


def enemy_name_from_key(key: str) -> str:
    return ENEMY_CATALOG.get(key, {}).get("name", key)


# ---------------------------------------------------------------------------
# Quest system
# ---------------------------------------------------------------------------


def check_quest_completion(player: Player) -> None:
    """Check if any active quests are now complete and mark them."""
    for qid, quest in player.quests.items():
        if not quest["active"] or quest["completed"]:
            continue
        all_done = all(obj["current"] >= obj["count"] for obj in quest["objectives"])
        if all_done:
            quest["completed"] = True
            slow_print(f"\n  ✅  Quest COMPLETE: '{quest['name']}'!")
            player.gold += quest["reward_gold"]
            msgs = player.grant_xp(quest["reward_xp"])
            print(
                f"  🏆 Rewards: {quest['reward_xp']} XP, {quest['reward_gold']} gold."
            )
            for msg in msgs:
                slow_print(f"  {msg}")
            reward_item = quest.get("reward_item")
            if reward_item and reward_item in ITEM_CATALOG:
                player.add_item(reward_item)
                print(f"  📦 Item reward: {ITEM_CATALOG[reward_item]['name']}")

            if qid == "q05_final_ascension":
                player.game_won = True


def show_quest_log(player: Player) -> None:
    divider()
    print("  📜  QUEST LOG")
    divider()
    if not player.quests:
        print("  You have no active quests. Speak with NPCs to find work.")
        return
    for qid, quest in player.quests.items():
        status = "✅ COMPLETE" if quest["completed"] else ("🔴 ACTIVE" if quest["active"] else "📌 ACCEPTED")
        print(f"\n  [{status}] {quest['name']}")
        print(f"    {quest['description']}")
        for obj in quest["objectives"]:
            if obj["type"] == "kill":
                ename = ENEMY_CATALOG.get(obj["enemy"], {}).get("name", obj["enemy"])
                print(f"    • Defeat {ename}: {obj['current']}/{obj['count']}")
            elif obj["type"] == "collect":
                iname = ITEM_CATALOG.get(obj["item"], {}).get("name", obj["item"])
                print(f"    • Collect {iname}: {obj['current']}/{obj['count']}")


# ---------------------------------------------------------------------------
# Item collection quest tracking
# ---------------------------------------------------------------------------


def update_collection_quests(player: Player, item_key: str) -> None:
    """Called when a collection-type quest item is picked up."""
    for qid, quest in player.quests.items():
        if not quest["active"] or quest["completed"]:
            continue
        for obj in quest["objectives"]:
            if obj["type"] == "collect" and obj["item"] == item_key:
                # Count how many are in inventory
                in_inv = player.inventory.get(item_key, 0)
                obj["current"] = min(obj["count"], in_inv)


# ---------------------------------------------------------------------------
# Shop
# ---------------------------------------------------------------------------


def visit_shop(player: Player, location_key: str) -> None:
    loc = LOCATION_DATA[location_key]
    if not loc["shop"]:
        print("  There is no shop here.")
        return

    while True:
        divider()
        print(f"  🛒  {loc['name']} SHOP   (Your gold: {player.gold})")
        divider()
        shop_items = loc["shop_items"]
        labels = []
        for item_key in shop_items:
            item = ITEM_CATALOG[item_key]
            labels.append(f"{item['name']}  — {item['value']}g  |  {item['description']}")
        labels.append("Leave shop")

        choice = prompt_choice(labels, "Buy: ")

        if choice == len(shop_items):
            break

        item_key = shop_items[choice]
        item = ITEM_CATALOG[item_key]
        cost = item["value"]

        if player.gold < cost:
            print(f"  ❌ Not enough gold. (Need {cost}g, have {player.gold}g)")
            continue

        player.gold -= cost
        player.add_item(item_key)
        print(f"  ✅ Purchased {item['name']} for {cost}g. (Remaining: {player.gold}g)")

        # Auto-equip if better
        if item["type"] == "weapon":
            current_atk = ITEM_CATALOG[player.weapon].get("atk_bonus", 0) if player.weapon else 0
            if item.get("atk_bonus", 0) > current_atk:
                if get_yes_no(f"  Equip {item['name']} as your weapon?"):
                    player.weapon = item_key
                    print(f"  🗡  Equipped {item['name']}.")
        elif item["type"] == "armor":
            current_def = ITEM_CATALOG[player.armor].get("def_bonus", 0) if player.armor else 0
            if item.get("def_bonus", 0) > current_def:
                if get_yes_no(f"  Equip {item['name']} as your armor?"):
                    player.armor = item_key
                    print(f"  🛡  Equipped {item['name']}.")


# ---------------------------------------------------------------------------
# Inventory management screen
# ---------------------------------------------------------------------------


def manage_inventory(player: Player) -> None:
    while True:
        divider()
        print("  🎒  INVENTORY")
        divider()
        print(f"  Gold: {player.gold}g")
        weapon_name = ITEM_CATALOG[player.weapon]["name"] if player.weapon else "None"
        armor_name = ITEM_CATALOG[player.armor]["name"] if player.armor else "None"
        print(f"  Weapon: {weapon_name}  |  Armor: {armor_name}")
        divider()

        if not player.inventory:
            print("  Your inventory is empty.")
            input("  [Press Enter to go back]")
            return

        item_keys = list(player.inventory.keys())
        labels = []
        for k in item_keys:
            item = ITEM_CATALOG.get(k, {})
            qty = player.inventory[k]
            labels.append(f"{item.get('name', k)} x{qty}  — {item.get('description', '')}")
        labels.append("Back")

        choice = prompt_choice(labels, "Select item: ")

        if choice == len(item_keys):
            return

        selected_key = item_keys[choice]
        selected = ITEM_CATALOG.get(selected_key, {})
        item_type = selected.get("type", "misc")

        print(f"\n  {selected.get('name', selected_key)}")
        print(f"  {selected.get('description', '')}")
        print(f"  Value: {selected.get('value', 0)}g  |  Type: {item_type}")

        actions = []
        if item_type == "weapon":
            actions.append("Equip")
        elif item_type == "armor":
            actions.append("Equip")
        elif item_type == "consumable":
            actions.append("Use")
        actions.append("Discard")
        actions.append("Cancel")

        act_choice = prompt_choice(actions, "Action: ")
        action = actions[act_choice]

        if action == "Equip":
            if item_type == "weapon":
                player.weapon = selected_key
                print(f"  🗡  Equipped {selected.get('name')}.")
            else:
                player.armor = selected_key
                print(f"  🛡  Equipped {selected.get('name')}.")
        elif action == "Use":
            heal_amount = selected.get("heal", 0)
            healed = player.heal(heal_amount)
            player.remove_item(selected_key)
            print(f"  💊 Used {selected.get('name')}. Restored {healed} HP.")
        elif action == "Discard":
            if get_yes_no(f"  Discard {selected.get('name')}?"):
                player.remove_item(selected_key)
                print("  Item discarded.")


# ---------------------------------------------------------------------------
# NPC interaction (quest givers)
# ---------------------------------------------------------------------------


def talk_to_npc(player: Player, location_key: str) -> None:
    """Find and interact with quest givers at the current location."""
    available = [
        qdata
        for qid, qdata in QUEST_DATA.items()
        if qdata["location"] == location_key
        and qid not in player.quests
        and player.level >= qdata["min_level"]
    ]

    if not available:
        print("  There is nobody here with work for you right now.")
        return

    for quest_template in available:
        divider()
        print(f"  💬  {quest_template['giver']} approaches you:")
        slow_print(f'  "{quest_template["description"]}"')
        print(
            f"\n  Reward: {quest_template['reward_xp']} XP, {quest_template['reward_gold']}g, "
            f"{ITEM_CATALOG.get(quest_template['reward_item'], {}).get('name', 'Unknown')}"
        )
        if get_yes_no("  Accept this quest?"):
            quest_copy = {
                "id": quest_template["id"],
                "name": quest_template["name"],
                "description": quest_template["description"],
                "objectives": [dict(o) for o in quest_template["objectives"]],
                "reward_xp": quest_template["reward_xp"],
                "reward_gold": quest_template["reward_gold"],
                "reward_item": quest_template["reward_item"],
                "active": True,
                "completed": False,
            }
            player.quests[quest_template["id"]] = quest_copy
            print(f"  📜 Quest accepted: '{quest_template['name']}'")


# ---------------------------------------------------------------------------
# Save / Load
# ---------------------------------------------------------------------------


def save_game(player: Player) -> None:
    try:
        data = player.to_dict()
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  💾  Game saved to {SAVE_FILE}.")
    except OSError as e:
        print(f"  ⚠  Save failed: {e}")


def load_game() -> Optional[Player]:
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        player = Player.from_dict(data)
        print(f"  💾  Game loaded for {player.name}.")
        return player
    except (OSError, json.JSONDecodeError, TypeError) as e:
        print(f"  ⚠  Could not load save: {e}")
        return None


# ---------------------------------------------------------------------------
# Character creation
# ---------------------------------------------------------------------------


def create_character() -> Player:
    divider("═")
    print("  CREATE YOUR CHARACTER")
    divider("═")

    while True:
        name = input("  Enter your name: ").strip()
        if name:
            break
        print("  Name cannot be empty.")

    print("\n  Choose your class:")
    divider()
    class_names = list(CLASS_DATA.keys())
    for i, cname in enumerate(class_names, 1):
        cdata = CLASS_DATA[cname]
        skill = cdata["skill"]
        print(f"  [{i}] {cname}")
        print(f"      {cdata['description']}")
        print(f"      Skill: {skill} — {cdata['skill_desc']}")
        print()

    choice = prompt_choice([c for c in class_names], "Your class: ")
    char_class = class_names[choice]
    cdata = CLASS_DATA[char_class]

    player = Player(
        name=name,
        char_class=char_class,
        max_hp=cdata["base_hp"],
        current_hp=cdata["base_hp"],
        base_atk=cdata["base_atk"],
        base_def=cdata["base_def"],
        gold=cdata["gold_bonus"] + 50,
    )
    # Starting gear
    player.weapon = "rusty_pitchfork"
    player.armor = "sinners_rags"
    player.add_item("health_potion", 3)

    divider()
    slow_print(
        f"\n  Welcome to Hell, {player.name} the {char_class}!\n"
        "  You've just arrived in the underworld with nothing but your wits,\n"
        "  a rusty pitchfork, and a burning ambition to become the greatest\n"
        "  Pimp Devil the underworld has ever seen.\n"
    )
    return player


# ---------------------------------------------------------------------------
# Location / exploration screen
# ---------------------------------------------------------------------------


def show_location(player: Player) -> None:
    loc = LOCATION_DATA[player.current_location]
    divider("═")
    print(f"  📍  {loc['name']}")
    divider("═")
    print(f"  {loc['description']}")
    print(f"\n  {player.status_bar()}")


def travel_menu(player: Player) -> None:
    """Let the player travel to a different location."""
    reachable = [
        (key, data)
        for key, data in LOCATION_DATA.items()
        if key != player.current_location and player.level >= data["min_level"]
    ]
    locked = [
        (key, data)
        for key, data in LOCATION_DATA.items()
        if key != player.current_location and player.level < data["min_level"]
    ]

    divider()
    print("  🗺   TRAVEL — Available Locations")
    divider()

    if not reachable:
        print("  No other locations available yet. Gain more levels!")
        return

    labels = [f"{data['name']}  (Min LV {data['min_level']})" for _, data in reachable]
    labels.append("Stay here")
    if locked:
        print("  🔒 Locked locations:")
        for key, data in locked:
            print(f"    • {data['name']}  (Requires LV {data['min_level']})")
        print()

    choice = prompt_choice(labels, "Travel to: ")
    if choice < len(reachable):
        dest_key, dest_data = reachable[choice]
        player.current_location = dest_key
        slow_print(f"\n  ✈  You travel to {dest_data['name']}...")
        time.sleep(0.5)


# ---------------------------------------------------------------------------
# Main exploration loop
# ---------------------------------------------------------------------------


def exploration_loop(player: Player) -> None:
    while True:
        if player.game_won:
            _show_victory_screen(player)
            return

        show_location(player)
        loc = LOCATION_DATA[player.current_location]
        check_quest_completion(player)

        # Update collection quests based on current inventory
        for item_key in list(player.inventory.keys()):
            update_collection_quests(player, item_key)

        options = ["Explore (fight enemies)", "Quest Log", "Inventory"]
        if loc["shop"]:
            options.append("Visit Shop")
        options.append("Talk to NPC")
        options.append("Travel")
        options.append("Save Game")
        options.append("Quit to Main Menu")

        print()
        choice_idx = prompt_choice(options, "What do you do? ")
        chosen = options[choice_idx]

        if chosen == "Explore (fight enemies)":
            _do_explore(player, loc)
        elif chosen == "Quest Log":
            show_quest_log(player)
            input("\n  [Press Enter to continue]")
        elif chosen == "Inventory":
            manage_inventory(player)
        elif chosen == "Visit Shop":
            visit_shop(player, player.current_location)
        elif chosen == "Talk to NPC":
            talk_to_npc(player, player.current_location)
        elif chosen == "Travel":
            travel_menu(player)
        elif chosen == "Save Game":
            save_game(player)
        elif chosen == "Quit to Main Menu":
            save_game(player)
            return


def _do_explore(player: Player, loc: dict) -> None:
    """Pick a random enemy for the current location and start combat."""
    enemy_key = random.choice(loc["enemies"])
    result = run_combat(player, enemy_key)

    if result == CombatResult.LOSE:
        slow_print("\n  ☠  You have fallen in the underworld...")
        slow_print("  The imps drag your battered body to a resurrection shrine.")
        player.current_hp = player.max_hp // 2
        gold_lost = player.gold // 4
        player.gold -= gold_lost
        print(f"  💸 You lose {gold_lost} gold on resurrection. Remaining: {player.gold}g")

    input("\n  [Press Enter to continue]")


def _show_victory_screen(player: Player) -> None:
    clear_screen()
    divider("★")
    slow_print(TITLE_ART, delay=0.005)
    divider("★")
    slow_print(
        f"\n  CONGRATULATIONS, {player.name}!\n\n"
        "  You have defeated the Arch Devil and claimed the Abyss Throne!\n"
        "  The entire underworld bows before you. Your legend will echo\n"
        "  through Hell for all eternity.\n\n"
        f"  Final Level: {player.level}\n"
        f"  Total Gold Accumulated: {player.gold}g\n"
        f"  Total XP Earned: {player.xp}\n"
    )
    divider("★")
    input("  [Press Enter to return to the main menu]")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------


def main_menu() -> None:
    while True:
        clear_screen()
        print(TITLE_ART)
        divider("═")
        options = ["New Game", "Load Game", "About", "Quit"]
        choice_idx = prompt_choice(options, "Select: ")
        chosen = options[choice_idx]

        if chosen == "New Game":
            player = create_character()
            exploration_loop(player)
        elif chosen == "Load Game":
            player = load_game()
            if player:
                exploration_loop(player)
            else:
                print("  No save file found.")
                input("  [Press Enter to continue]")
        elif chosen == "About":
            divider()
            print("  Satanic Pimp: Underworld Chronicles")
            print("  Version:", __version__)
            print("  Author:", __author__)
            print()
            print("  A text-based MMORPG where you rise from a lowly imp-botherer")
            print("  to the supreme Pimp Devil ruling all of Hell.")
            print()
            print("  Features:")
            print("    • 4 playable character classes, each with a unique skill")
            print("    • 6 explorable locations, unlocked by level")
            print("    • 7 enemy types including an Arch Devil boss")
            print("    • 5 hand-crafted quests with item rewards")
            print("    • Full inventory, equipment, and shop system")
            print("    • Persistent save/load system")
            divider()
            input("  [Press Enter to go back]")
        elif chosen == "Quit":
            slow_print("  May your soul burn brightly in the eternal flame. Goodbye.")
            sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    main_menu()
