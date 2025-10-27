# upsgc_resolver.py

import re
import matplotlib.pyplot as plt
import numpy as np
import math

# --- CORE DATA AND DEFINITIONS ---

TIER_VALUES = {
    # TIER: Base Power Value (PV)
    "Street": 10,
    "Building": 100,
    "City Block": 1_000,
    "Small City": 10_000,
    "Large City": 50_000,
    "Mountain": 100_000,
    "Country": 1_000_000,
    "Continental": 10_000_000,
    "Planet": 100_000_000,
    "Stellar": 10**12,
    "Galactic": 10**18,
    "Universal": 10**30,
    "Low Multiversal": 10**40,
    "High Multiversal": 10**50,
    "Complex Multiversal": 10**70,
    "Omniversal": float('inf'),
    "Transcendent": float('inf'),
}

HAX_DICTIONARY = {
    # HAX_NAME: {multiplier, regex_keywords}
    "Conceptual Manipulation": {"multiplier": 6.0, "keywords": r"conceptual|platonic|erase concept|concept manipulation"},
    "Causality Manipulation": {"multiplier": 5.0, "keywords": r"causality|fate|probability|predestination|cause and effect"},
    "Reality Warping": {"multiplier": 4.5, "keywords": r"reality warp|alter reality|reality manipulation"},
    "Time Manipulation": {"multiplier": 4.0, "keywords": r"time stop|time travel|temporal|chronokinesis"},
    "Information Manipulation": {"multiplier": 3.5, "keywords": r"information manipulation|data manipulation|akashic records"},
    "Soul Manipulation": {"multiplier": 3.0, "keywords": r"soul crush|soul steal|astral form"},
    "Durability Negation": {"multiplier": 3.0, "keywords": r"ignore durability|internal attack|spatial slice|atomic destruction"},
    "Regeneration": {"multiplier": 2.0, "keywords": r"regeneration|healing factor"},
    "Teleportation": {"multiplier": 1.5, "keywords": r"teleport|instant transmission|spatial movement"},
}

RESISTANCE_KEYWORDS = {
    "Conceptual": HAX_DICTIONARY["Conceptual Manipulation"]["keywords"],
    "Causality": HAX_DICTIONARY["Causality Manipulation"]["keywords"],
    "Reality": HAX_DICTIONARY["Reality Warping"]["keywords"],
    "Time": HAX_DICTIONARY["Time Manipulation"]["keywords"],
    "Information": HAX_DICTIONARY["Information Manipulation"]["keywords"],
    "Soul": HAX_DICTIONARY["Soul Manipulation"]["keywords"],
}

class Character:
    """Stores all data and calculated scores for a single character."""
    def __init__(self, name, tier, strength_kgf, speed_ms, abilities, strategy_score):
        self.name = name
        self.tier_str = tier
        self.strength = strength_kgf
        self.speed = speed_ms
        self.abilities = abilities
        self.strategy = strategy_score # A score from 1 to 10

        # Calculated values
        self.base_pv = self._parse_tier()
        self.hax_score = self._calculate_hax_score()
        self.resistance_score = self._calculate_resistance_score()
        self.final_combat_score = 0
        self.verdict_notes = []

    def _parse_tier(self):
        """Finds the closest matching tier and returns its PV."""
        for key, value in TIER_VALUES.items():
            if re.search(key, self.tier_str, re.IGNORECASE):
                return value
        return 1 # Default to lowest if no match

    def _calculate_hax_score(self):
        """Calculates total hax score based on abilities."""
        score = 0
        for hax, data in HAX_DICTIONARY.items():
            if re.search(data["keywords"], self.abilities, re.IGNORECASE):
                score += data["multiplier"]
        return score

    def _calculate_resistance_score(self):
        """Calculates resistance score for specific hax categories."""
        resistances = {}
        for res_name, keywords in RESISTANCE_KEYWORDS.items():
            if re.search(r"(resist|immune|negate).*" + keywords, self.abilities, re.IGNORECASE):
                resistances[res_name] = True
        return resistances


def resolve_debate(char1, char2):
    """
    Analyzes two characters and determines the winner.
    Returns the winner, loser, and a detailed verdict.
    """
    # --- HAX ADVANTAGE CALCULATION ---
    char1_hax_advantage = 1.0
    char2_hax_advantage = 1.0

    # Compare char1's hax to char2's resistances
    for hax, data in HAX_DICTIONARY.items():
        if re.search(data["keywords"], char1.abilities, re.IGNORECASE):
            resistance_key = next((key for key in RESISTANCE_KEYWORDS if key in hax), None)
            if not char2.resistance_score.get(resistance_key):
                char1_hax_advantage += data["multiplier"]
                char1.verdict_notes.append(f"Utilized '{hax}' which {char2.name} could not resist.")

    # Compare char2's hax to char1's resistances
    for hax, data in HAX_DICTIONARY.items():
        if re.search(data["keywords"], char2.abilities, re.IGNORECASE):
            resistance_key = next((key for key in RESISTANCE_KEYWORDS if key in hax), None)
            if not char1.resistance_score.get(resistance_key):
                char2_hax_advantage += data["multiplier"]
                char2.verdict_notes.append(f"Utilized '{hax}' which {char1.name} could not resist.")
    
    # --- PHYSICALITY & STRATEGY MULTIPLIER ---
    phys_strat_multiplier1 = 1.0
    phys_strat_multiplier2 = 1.0

    if char1.speed > char2.speed * 2:
        phys_strat_multiplier1 += 0.2
        char1.verdict_notes.append(f"Holds a significant speed advantage ({char1.speed:,} m/s vs {char2.speed:,} m/s).")
    if char2.speed > char1.speed * 2:
        phys_strat_multiplier2 += 0.2
        char2.verdict_notes.append(f"Holds a significant speed advantage ({char2.speed:,} m/s vs {char1.speed:,} m/s).")

    if char1.strength > char2.strength * 2:
        phys_strat_multiplier1 += 0.1
    if char2.strength > char1.strength * 2:
        phys_strat_multiplier2 += 0.1

    phys_strat_multiplier1 += (char1.strategy - 5) / 10 # Strategy bonus/penalty from -0.4 to +0.5
    phys_strat_multiplier2 += (char2.strategy - 5) / 10


    # --- FINAL SCORE CALCULATION ---
    char1.final_combat_score = (char1.base_pv * phys_strat_multiplier1) * char1_hax_advantage
    char2.final_combat_score = (char2.base_pv * phys_strat_multiplier2) * char2_hax_advantage

    # --- DETERMINE WINNER ---
    if char1.final_combat_score > char2.final_combat_score:
        winner, loser = char1, char2
    else:
        winner, loser = char2, char1

    # --- GENERATE VERDICT ---
    tier_diff = winner.base_pv / loser.base_pv if loser.base_pv > 0 else float('inf')
    
    verdict = f"--- DEBATE VERDICT: {winner.name} vs. {loser.name} ---\n\n"
    verdict += f"**WINNER: {winner.name}**\n\n"
    verdict += f"**Final Combat Scores:**\n"
    verdict += f"  - {winner.name}: {winner.final_combat_score:,.2e}\n"
    verdict += f"  - {loser.name}: {loser.final_combat_score:,.2e}\n\n"
    verdict += "**Key Factors in Victory:**\n"

    if tier_diff > 100_000_000:
        verdict += f"- **Overwhelming Power Difference**: {winner.name}'s Tier ({winner.tier_str}) is fundamentally superior, representing a power gap of over {tier_diff:,.0f} times.\n"
    
    if winner.verdict_notes:
        for note in winner.verdict_notes:
            verdict += f"- {note}\n"
    else:
        verdict += "- The victory was primarily decided by a higher base power level and overall stats.\n"

    return winner, loser, verdict

def create_debate_chart(char1, char2, winner_name):
    """Generates and displays a radar chart of the matchup."""
    labels = ['Tier', 'Strength', 'Speed', 'Hax Score', 'Strategy']
    
    # Normalize stats for visualization
    def normalize_stats(char):
        tier_stat = math.log10(char.base_pv if char.base_pv > 0 else 1)
        strength_stat = math.log10(char.strength if char.strength > 0 else 1)
        speed_stat = math.log10(char.speed if char.speed > 0 else 1)
        hax_stat = char.hax_score
        strategy_stat = char.strategy
        return [tier_stat, strength_stat, speed_stat, hax_stat, strategy_stat]

    stats1 = normalize_stats(char1)
    stats2 = normalize_stats(char2)

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    stats1 = np.concatenate((stats1, [stats1[0]]))
    stats2 = np.concatenate((stats2, [stats2[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.fill(angles, stats1, color='red', alpha=0.25)
    ax.plot(angles, stats1, color='red', linewidth=2, label=char1.name)
    ax.fill(angles, stats2, color='blue', alpha=0.25)
    ax.plot(angles, stats2, color='blue', linewidth=2, label=char2.name)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    plt.title(f"Matchup Analysis: {char1.name} vs. {char2.name}\nWinner: {winner_name}", size=15)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.show()

def main():
    """Example usage of the debate resolver."""
    # --- Character Definitions ---
    goku = Character(
        name="Goku (DBS)",
        tier="Universal",
        strength_kgf=1e30, # Incalculable, placeholder value
        speed_ms=3e8 * 1_000_000, # Massively FTL+
        abilities="Superhuman strength and speed, energy projection (Kamehameha), flight, instant transmission (teleport), can adapt in combat. Lacks exotic hax.",
        strategy_score=8
    )

    rimuru = Character(
        name="Rimuru (WN)",
        tier="Complex Multiversal",
        strength_kgf=1e30, # Incalculable, placeholder value
        speed_ms=float('inf'), # Immeasurable speed
        abilities="""Controls Turn Null energy to create/destroy universes. Can stop time (Time Manipulation), alter cause and effect (Causality Manipulation),
        and erase beings from existence conceptually (Conceptual Manipulation). Possesses absolute regeneration and near-omniscience.
        Immune to time manipulation and conceptual attacks.""",
        strategy_score=10
    )

    # --- Resolve and Print ---
    winner, loser, verdict = resolve_debate(goku, rimuru)
    print(verdict)

    # --- Visualize ---
    create_debate_chart(goku, rimuru, winner.name)

if __name__ == '__main__':
    main()