"""Test script to reproduce the monster respawn bug reported by user."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from caislean_gaofar.core.game import Game
from caislean_gaofar.systems.save_game import SaveGame


def print_monsters(game, label):
    """Helper to print current monsters."""
    print(f"\n{label}:")
    print(f"  Map ID: {game.dungeon_manager.current_map_id}")
    print(f"  Monsters count: {len(game.entity_manager.monsters)}")
    for m in game.entity_manager.monsters:
        print(f"    - {m.monster_type} at ({m.grid_x}, {m.grid_y})")
    print(f"  Killed monsters count: {len(game.entity_manager.killed_monsters)}")
    for km in game.entity_manager.killed_monsters:
        print(f"    - {km['type']} at ({km['x']}, {km['y']}) on map {km['map_id']}")


def main():
    print("=== Testing Monster Respawn Bug ===")

    # Create a new game
    print("\n1. Creating new game...")
    game = Game()
    print_monsters(game, "After game creation")

    # Get monsters on world map
    world_monsters = list(game.entity_manager.monsters)
    print(f"\nTotal monsters on world map: {len(world_monsters)}")

    if len(world_monsters) < 2:
        print("ERROR: Not enough monsters to test! Need at least 2.")
        return

    # Kill first two monsters (simulating user killing leprechaun and cat)
    print("\n2. Killing first two monsters...")
    monster1 = world_monsters[0]
    monster2 = world_monsters[1]

    print(
        f"   Killing {monster1.monster_type} at ({monster1.grid_x}, {monster1.grid_y})"
    )
    print(
        f"   Killing {monster2.monster_type} at ({monster2.grid_x}, {monster2.grid_y})"
    )

    monster1.is_alive = False
    monster2.is_alive = False

    # Process deaths
    game.entity_manager.check_monster_deaths(game.dungeon_manager)
    print_monsters(game, "After killing 2 monsters")

    # Enter a dungeon (find a cave entrance)
    print("\n3. Finding and entering a dungeon...")
    dungeon_spawns = game.world_map.get_entity_spawns("dungeons")
    if not dungeon_spawns:
        print("ERROR: No dungeon entrances found!")
        return

    cave_entrance = dungeon_spawns[0]
    dungeon_id = cave_entrance.get("id")
    cave_x = cave_entrance.get("x")
    cave_y = cave_entrance.get("y")

    print(f"   Found dungeon '{dungeon_id}' at ({cave_x}, {cave_y})")

    # Move warrior to cave entrance
    game.warrior.grid_x = cave_x
    game.warrior.grid_y = cave_y

    # Trigger dungeon entry through transition manager
    game.dungeon_transition_manager.check_and_handle_transition(
        game.warrior,
        game.dungeon_manager,
        game.entity_manager,
        lambda w, h: game.camera,  # on_camera_update
        lambda msg: print(f"   Message: {msg}"),  # on_message
    )

    print_monsters(game, "After entering dungeon")

    # Exit dungeon
    print("\n4. Exiting dungeon back to world map...")
    # Find exit tile (typically at 1, 1 in dungeon maps)
    for y in range(game.world_map.height):
        for x in range(game.world_map.width):
            if game.dungeon_manager.check_for_exit(x, y):
                game.warrior.grid_x = x
                game.warrior.grid_y = y
                print(f"   Found exit at ({x}, {y})")
                break
        else:
            continue
        break

    # Trigger dungeon exit
    game.dungeon_transition_manager.check_and_handle_transition(
        game.warrior,
        game.dungeon_manager,
        game.entity_manager,
        lambda w, h: game.camera,
        lambda msg: print(f"   Message: {msg}"),
    )

    print_monsters(game, "After exiting dungeon")

    # Check if killed monsters respawned
    print("\n5. Checking for bug...")
    respawned = False
    for monster in game.entity_manager.monsters:
        if (
            monster.grid_x == world_monsters[0].grid_x
            and monster.grid_y == world_monsters[0].grid_y
        ):
            print(
                f"   BUG FOUND: Monster 1 ({world_monsters[0].monster_type}) respawned!"
            )
            respawned = True
        if (
            monster.grid_x == world_monsters[1].grid_x
            and monster.grid_y == world_monsters[1].grid_y
        ):
            print(
                f"   BUG FOUND: Monster 2 ({world_monsters[1].monster_type}) respawned!"
            )
            respawned = True

    if not respawned:
        print("   ✓ Monsters did NOT respawn after dungeon transition")

    # Test save/load scenario
    print("\n6. Testing save/load scenario...")
    print("   Saving game...")
    SaveGame.save_game(game, "test_respawn")

    print("   Loading save data...")
    save_data = SaveGame.load_game("test_respawn")

    print("   Creating new game instance...")
    game2 = Game()
    print_monsters(game2, "After creating new game instance (before load)")

    print("   Loading game state...")
    game2.load_game_state(save_data)
    print_monsters(game2, "After loading game state")

    # Check if killed monsters respawned in loaded game
    print("\n7. Checking for save/load bug...")
    respawned_after_load = False
    for monster in game2.entity_manager.monsters:
        if (
            monster.grid_x == world_monsters[0].grid_x
            and monster.grid_y == world_monsters[0].grid_y
        ):
            print(
                f"   BUG FOUND: Monster 1 ({world_monsters[0].monster_type}) respawned after load!"
            )
            respawned_after_load = True
        if (
            monster.grid_x == world_monsters[1].grid_x
            and monster.grid_y == world_monsters[1].grid_y
        ):
            print(
                f"   BUG FOUND: Monster 2 ({world_monsters[1].monster_type}) respawned after load!"
            )
            respawned_after_load = True

    if not respawned_after_load:
        print("   ✓ Monsters did NOT respawn after save/load")

    # Cleanup
    SaveGame.delete_save("test_respawn")

    print("\n=== Test Complete ===")
    if not respawned and not respawned_after_load:
        print("✓ NO BUGS FOUND - System working correctly!")
        return 0
    else:
        print("✗ BUGS FOUND - Monsters are respawning incorrectly!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
