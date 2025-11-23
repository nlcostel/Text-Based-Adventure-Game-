# CostelloTextBasedGame.py
# Author: Coley Costello :)

# Import time

import time

# Color Setup UX
import os
if os.name == "nt":
    os.system("")

GREEN  = "\033[1;32m"       # bright green
RED    = "\033[1;31m"       # bright red
ORANGE = "\033[38;5;208m"   # bright orange
YELLOW = "\033[1;33m"       # bright yellow
BLUE   = "\033[1;34m"       # bright blue
RESET  = "\033[0m"          # reset to default

# Sound Setup UX

from pathlib import Path
import threading

BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
os.chdir(BASE_DIR)

SND_SUCCESS = BASE_DIR / "Sounds" / "success.wav"
SND_COLLECT = BASE_DIR / "Sounds" / "collected item.wav"
SND_VICTORY = BASE_DIR / "Sounds" / "victory.wav"

def play_sound_success():
    try:
        import winsound  # Windows built-in; reliable for WAV
        winsound.PlaySound(str(SND_SUCCESS), winsound.SND_FILENAME | winsound.SND_ASYNC)
        return
    except Exception:
        pass

    try:
        from playsound import playsound
        threading.Thread(target=playsound, args=(str(SND_SUCCESS),), daemon=True).start()
    except Exception as e:
        print(f"(sound disabled: {e})")

def play_sound_collect():
    try:
        import winsound
        winsound.PlaySound(str(SND_COLLECT), winsound.SND_FILENAME | winsound.SND_ASYNC)
        return
    except Exception:
        pass

    try:
        from playsound import playsound
        threading.Thread(target=playsound, args=(str(SND_COLLECT),), daemon=True).start()
    except Exception as e:
        print(f"(sound disabled: {e})")

def play_sound_victory():
    try:
        import winsound
        # stop any previous sound
        winsound.PlaySound(None, winsound.SND_PURGE)

        if not SND_VICTORY.exists():
            print(f"(sound disabled: file not found at {SND_VICTORY})")
            return

        winsound.PlaySound(str(SND_VICTORY), winsound.SND_FILENAME | winsound.SND_ASYNC)
        return
    except Exception as e:
        print(f"(winsound failed: {e})")

    try:
        from playsound import playsound
        threading.Thread(target=playsound, args=(str(SND_VICTORY),), daemon=True).start()
    except Exception as e:
        print(f"(playsound failed: {e})")

# Room map w/ compass directions
ROOMS = {
    'Trailhead': {
        'North': 'Crystal Cavern',
        'South': 'Stone Circle',
        'East':  'Mossy Hollow',
        'West':  'Foggy Bog'
    },

    'Stone Circle': {
        'North': 'Trailhead',
        'West':  'Willow Dock'
    },

    'Willow Dock': {
        'East': 'Stone Circle'
    },

    'Foggy Bog': {
        'West': 'Old Library',
        'East': 'Trailhead'
    },

    'Old Library': {
        'East': 'Foggy Bog'
    },

    'Mossy Hollow': {
        'West': 'Trailhead'
    },

    'Crystal Cavern': {
        'South': 'Trailhead',
        'North': 'Trolls Bridge',
        'West':  'Ruined Watchtower'
    },

    'Ruined Watchtower': {
        'East': 'Crystal Cavern'
    },

    'Trolls Bridge': {
        'South': 'Crystal Cavern'
    }
}

# Room content & riddle answers

ROOM_CONTENT = {
    'Mossy Hollow': {
        'item': 'Moss Crown',
        'riddle': "I'm green and I grow, but I'm not a tree. Keep me wet and I'll blanket stones. What am I?",
        'answer': 'Moss'

    },
    'Stone Circle': {
    'item': 'Sunstone',
    'riddle': "I rise in the day and set at night; hold me and you'll carry light. What am I?",
    'answer': 'Sun'

    },
    'Ruined Watchtower': {
        'item': 'Runed Key',
        'riddle': "In iron doors I twist with ease, one turn from me and locks appease. What am I?",
        'answer': 'Key'

    },
    'Old Library': {
        'item': 'Riddle Scroll',
        'riddle': "I speak without a mouth but I'm heard on paper. What am I?",
        'answer': 'Book'

    },
    'Foggy Bog': {
        'item': 'Reed Flute',
        'riddle': "I'm hollow and small with holes in line, blow through me and you'll hear me whine. What am I?",
        'answer': 'Flute'

    },
    'Crystal Cavern': {
        'item': 'Echo Crystal',
        'riddle': "I speak your words yet have no tongue, I answer after you are done. What am I?",
        'answer': 'Echo'

    },
    'Willow Dock': {
        'item': 'Boat Ticket',
        'riddle':"To ride the boat, you must show me. What am I?",
        'answer': 'Ticket'

    }
}

START_ROOM = 'Trailhead'
VILLAIN_ROOM= "Trolls Bridge"

# Total items to win
ALL_ITEMS = [ROOM_CONTENT[r]['item'] for r in ROOM_CONTENT]
TOTAL_ITEMS_NEEDED= len(ALL_ITEMS)

from typing import List, Set

def show_status(current_room: str, inventory: List[str], solved_riddles: Set[str]) -> None:
    print(f"\nYou are now in: {current_room}")
    print(f"Inventory: {inventory}")

    # If the room has an item & it's not in inventory, show item/riddle
    if current_room in ROOM_CONTENT:
        item = ROOM_CONTENT[current_room]['item']
        if item not in inventory:
            if current_room in solved_riddles:
                # Riddle already solved here; remind them to get item
                print(f"Tip: Use the 'get' command to pick up {item}")
            else:
                # Riddle not solved yet

                print(f"You see a {item}.\n")
                print(f"To collect the {item} you must answer this riddle:")
                print(f"{BLUE}{ROOM_CONTENT[current_room]['riddle']}{RESET}")
                print("Tip: Use the 'answer' command when you're ready.")
                print()

    # Show exits (only the compass directions)
    exits = [d for d in ROOMS[current_room] if d in ('North', 'South', 'East', 'West')]
    if exits:
        print("Exits available: " + ", ".join(exits))
    print("-" * 60)

def uncollected_item_here(current_room: str, inventory: list) -> str | None:
    if current_room in ROOM_CONTENT:
        item = ROOM_CONTENT[current_room]['item']
        if item not in inventory:
            return item
    return None

# Menu instructions
def show_instructions():
    print("Commands: Enter the below commands to navigate the game.")
    print("  answer    - solve the current room’s riddle")
    print("  get       - pick up an item (after solving)")
    print("  move      - travel in a direction")
    print("  inventory - check what you’ve collected")
    print("  help      - see available commands")
    print("  quit      - exit the game")
    print("-" * 60)

# Normalize direction entry
def parse_direction(cmd: str):
    cmd = cmd.strip().lower()
    # allow "go north" or just "north" / "n"
    if cmd.startswith("go "):
        cmd = cmd[3:].strip()

    short = {'n': 'North', 's': 'South', 'e': 'East', 'w': 'West'}
    if cmd in short:
        return short[cmd]
    if cmd in ('north', 'south', 'east', 'west'):
        return cmd.capitalize()
    return None

# MAIN GAME LOOP

def main():
    current_room = START_ROOM
    inventory = []
    solved_riddles = set()
    collected_set = set()
    all_collected_announced = False
    print()

    print(f"{BLUE}Welcome to Riddles at the Troll’s Bridge!{RESET}\n")
    print(f"{BLUE}At each stop along the way, you will be asked to answer a riddle.{RESET}")
    print(f"{BLUE}Answer the riddles correctly to collect all 7 magical artifacts\nBEFORE reaching the Troll's Bridge.{RESET}\n")

    show_instructions()


    while True:
        # Status panel
        show_status(current_room, inventory, solved_riddles)

        if len(inventory) != len(set(inventory)):
            seen = set()
            inventory[:] = [x for x in inventory if not (x in seen or seen.add(x))]

        # Announce once when the player has everything
        if len(inventory) == TOTAL_ITEMS_NEEDED and not all_collected_announced:
            print("You have ALL artifacts! Head to the Troll's Bridge to win.")
            all_collected_announced = True

        # Win/Lose conditions in Villain Room
        if current_room == VILLAIN_ROOM:
            if len(inventory) == TOTAL_ITEMS_NEEDED:
                # Flash green congratulations
                for _ in range(2):
                    print(f"{GREEN}Congratulations! You’ve collected all artifacts and defeated the Troll!{RESET}",
                          end="\r", flush=True)
                    time.sleep(0.5)
                    print(" " * 100, end="\r", flush=True)
                    time.sleep(0.3)

                play_sound_victory()
                print(f"{GREEN}Congratulations! You’ve collected all artifacts and defeated the Troll!{RESET}")
                time.sleep(6.0)
            else:
                # Flash red 'Game Over'
                for _ in range(2):
                    print(f"{RED}The Troll blocks your path! You didn’t collect all the artifacts. Game over.{RESET}",
                          end="\r", flush=True)
                    time.sleep(0.5)
                    print(" " * 100, end="\r", flush=True)
                    time.sleep(0.3)

                print(f"{RED}The Troll blocks your path! You didn’t collect all the artifacts. Game over.{RESET}")
                time.sleep(1.0)

            break

        # Guided command entry
        cmd = input("Enter command [answer/get/move/help/inventory/quit]: ").strip().lower()

        # Quit
        if cmd in ('quit', 'exit'):
            print(f"{GREEN}Thanks for playing! Goodbye.{RESET}")
            break

        # Help
        if cmd in ('help', '?'):
            show_instructions()
            continue

        # Inventory
        if cmd in ('inventory', 'inv'):
            print(f"Inventory: {inventory if inventory else 'Empty'}")
            continue

        # Answer a riddle
        if cmd in ('answer', 'a'):
            if current_room not in ROOM_CONTENT or 'answer' not in ROOM_CONTENT[current_room]:
                print(f"{ORANGE}There’s no riddle to answer here.{RESET}")
                continue

            item_here = ROOM_CONTENT[current_room]['item']
            # Block answering again if solved or item already take
            if current_room in solved_riddles or item_here in inventory:
                print(f"{ORANGE}This riddle has already been solved.{RESET}")
                continue

            guess = input("Your riddle answer (one word): ").strip().lower()
            correct = ROOM_CONTENT[current_room]['answer'].lower()


            if guess == correct:
                solved_riddles.add(current_room)
                print(f"{GREEN}Correct! The room's magic yields its treasure—you may now pick it up.{RESET} ")
                play_sound_success()
            else:
                print(f"{RED}That is not correct. Think it through and try again.{RESET}")
            continue

        # Pick up an item
        if cmd in ('get', 'g'):


            if current_room not in ROOM_CONTENT or 'item' not in ROOM_CONTENT[current_room]:
                print(f"{ORANGE}There’s nothing to pick up here.{RESET}")
                continue

            item = ROOM_CONTENT[current_room]['item']

            # Guard against duplicates using the set
            if item in collected_set:
                print(f"{ORANGE}You already picked that up.{RESET}")
                continue

            if current_room not in solved_riddles:
                print(f"{ORANGE}You must solve the riddle before taking the item.{RESET}")
                continue

            entry = input(f"Item to pick up (tip: {item}): ").strip()
            if entry.lower() != item.lower():
                print(f"To pick up, type exactly: {item}")
                continue

            # Record once in the set + list
            collected_set.add(item)
            if item not in inventory:
                inventory.append(item)

            print(f"{BLUE}You pick up the {item}.{RESET}")
            play_sound_collect()

            # Check victory using the SET, not the list length
            if len(collected_set) == TOTAL_ITEMS_NEEDED and not all_collected_announced:
                # Flash "You now carry ALL artifacts!"
                for _ in range(2):
                    print(f"{YELLOW}You now carry ALL artifacts!{RESET}", end="\r", flush=True)
                    time.sleep(0.5)
                    print(" " * 80, end="\r", flush=True)  # clear the line
                    time.sleep(0.3)

                print(f"{YELLOW}You now carry ALL artifacts!{RESET}")
                time.sleep(1)
                print(f"{YELLOW}Proceed to the Troll's Bridge to present your treasures.{RESET}")
                all_collected_announced = True
            continue

        # Move to a new room
        if cmd in ('move', 'm'):
            # Reminder if leaving a solved room without taking its item
            room_data = ROOM_CONTENT.get(current_room)
            if room_data:
                item_name = room_data['item']

                if (current_room in solved_riddles) and (item_name not in inventory):
                    # Flash the warning
                    for _ in range(2):
                        print(f"{ORANGE}You haven't picked up the {item_name} yet!{RESET}", end="\r", flush=True)
                        time.sleep(0.5)
                        print(" " * 80, end="\r", flush=True)  # clear the line
                        time.sleep(0.3)
                    print(f"{ORANGE}You haven't picked up the {item_name} yet!{RESET}")
                    stay = input("Do you want to stay and pick it up? (y/n): ").strip().lower()
                    if stay in ('y', 'yes'):
                        continue

            # Ask for direction and attempt the move
            dir_text = input("Which direction? (North/South/East/West or n/s/e/w): ").strip()
            direction = parse_direction(dir_text)
            if not direction:

                print(f"{RED}Invalid direction. Try North/South/East/West (or n/s/e/w).{RESET}")
                continue

            if direction in ROOMS[current_room]:
                current_room = ROOMS[current_room][direction]
                print(f"You travel {direction}...")
            else:

                print(f"{RED}You can’t go that way.{RESET}")
            continue

        # Fallback
        print(f"{RED}Invalid command. Try: answer, get, move, help, inventory, or quit.{RESET}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Game interrupted. Thanks for playing!{RESET}")

