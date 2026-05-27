import sys, os
sys.path = [p for p in sys.path if not p.endswith(os.sep + "source") and p != "source"]

import numpy as np

PLAYERS = ["Player 1", "Player 2", "Player 3", "Player 4"]
NUM_ROUNDS = 20

rng = np.random.default_rng(seed=42)
rolls = rng.integers(1, 7, size=(len(PLAYERS), NUM_ROUNDS))

# --- Console summary ---
print("\n=== Dice Simulator Results ===\n")
print("Random figures (numpy array):")
print(rolls)
print()
header = f"{'Round':<8}" + "".join(f"{p:<12}" for p in PLAYERS)
print(header)
print("-" * len(header))

for r in range(NUM_ROUNDS):
    row = f"{'Round ' + str(r + 1):<12}" + "".join(f"{rolls[i][r]:<12}" for i in range(len(PLAYERS)))
    print(row)


winner = PLAYERS[np.argmax([rolls[i].sum() for i in range(len(PLAYERS))])]
print(f"\nWinner: {winner}!")
