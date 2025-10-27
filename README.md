# UPSGC Debate Resolver v1.0.0

This package provides a powerful command-line tool and library for automatically resolving versus (VS) debates between fictional characters. It is based on the **Unified Power-Scaling System for General Use (UPSGC)** framework.

The resolver analyzes characters based on their power tier, physicality, strategic intelligence, and a comprehensive list of special abilities (hax). It then calculates a Final Combat Score to determine the winner and generates a detailed verdict with a visual radar chart.

## Features

-   **Tier-Based Power**: Uses an exponential power scale from Street Level to Transcendent.
-   **Regex-Powered Hax Detection**: Automatically detects abilities like time manipulation, reality-warping, causality manipulation, and more from a text description.
-   **Resistance Counter-Play**: Hax can be negated if a character has explicit resistances.
-   **Quantifiable Physicality**: Considers numerical values for strength (kgf) and speed (m/s).
-   **Visual Analysis**: Generates a Matplotlib radar chart to visually compare the combatants.
-   **Command-Line Interface**: Run a debate directly from your terminal.

## Installation

You can install the resolver via pip:

```bash
pip install upsgc-resolver
```
*(Note: You will need to upload the package to PyPI for this to work. For local installation, navigate to the project root and run `pip install .`)*

## How to Use

### As a Command-Line Tool

After installation, you can run the pre-configured Goku vs. Rimuru debate directly from your terminal:

```bash
upsgc-resolve
```

This will print the detailed verdict to the console and display the matchup chart.

### As a Python Library

You can import the resolver into your own Python projects to analyze any characters you define.

```python
from upsgc_resolver.resolver import Character, resolve_debate, create_debate_chart

# 1. Define your characters
character_A = Character(
    name="Character B",
    tier="Planet",
    strength_kgf=5.972e24, # Earth's mass in kg
    speed_ms=29979245, # 10% the speed of light
    abilities="destroy planets, Shoots energy beams. Flies", # just drop the word, overcomplexity is just unnecessary.
    strategy_score=7
)

character_B = Character(
    name="Character B",
    tier="City Block",
    strength_kgf=100000,
    speed_ms=1700, # Mach 5
    abilities="Soul Manipulation",
    strategy_score=9
)

# 2. Resolve the debate
winner, loser, verdict = resolve_debate(character_A, character_B)

# 3. Print the results and show the chart
print(verdict)
create_debate_chart(character_A, character_B, winner.name)
```

### Licence
MIT Licence

Help us make a database for pre-built characters!