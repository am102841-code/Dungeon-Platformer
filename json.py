import json

# Example player data
player_data = {
    "name": "Knight",
    "level": 3,
    "health": 10,
    "coins": 5
}

# --- Save data to a file ---
with open("savegame.json", "w") as f:
    json.dump(player_data, f)

print("Game saved!")

# --- Load data from a file ---
with open("savegame.json", "r") as f:
    loaded_data = json.load(f)

print("Loaded data:", loaded_data)
