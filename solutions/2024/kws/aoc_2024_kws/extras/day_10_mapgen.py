from pathlib import Path

import amulet
import click
from amulet.api.block import Block
from amulet.api.level import BaseLevel
from amulet_nbt import IntTag


def load_map(map_path):
    map_data = Path(map_path).read_text()
    # Initialize empty grids for height and type
    height_grid = []
    type_grid = []

    # Process each line of the map
    for line in map_data.splitlines():
        # Split line into pairs of characters and process
        height_row = []
        type_row = []

        # Skip empty lines
        if not line.strip():
            continue

        # Process pairs of characters
        chars = line.split()
        for cell in chars:
            # First character is height (0-9)
            height = int(cell[0])
            # Second character is type flag (e.g. '*' or ' ')
            type_flag = cell[1] if len(cell) > 1 else " "

            height_row.append(height)
            type_row.append(type_flag)

        height_grid.append(height_row)
        type_grid.append(type_row)

    return height_grid, type_grid


def translate_to_world_coordinates(
    local_x, local_y, local_z, start_x, start_y, start_z
):
    world_x = start_x + local_x
    world_y = start_y + local_y
    world_z = start_z + local_z
    return world_x, world_y, world_z


@click.command()
@click.argument("world_path")
def generate_mountain(world_path):
    map_path = Path(__file__).parent / "day_10.map"

    height_grid, type_grid = load_map(map_path)

    # Starting coordinates for the grid in the Minecraft world
    start_x, start_z = 0, 0
    base_y = 80  # Base Y coordinate (ground level)

    # Block types for the mountain
    stone_block = Block("minecraft", "obsidian")
    carpet_block = Block("minecraft", "white_carpet")
    fire_block = Block("minecraft", "fire", {"age": IntTag(0)})

    # Coordinates for the spawn position
    spawn_x, spawn_y, spawn_z = start_x - 10, base_y, start_z - 10

    # Game mode (0 = Survival, 1 = Creative, 2 = Adventure, 3 = Spectator)
    game_mode = 1

    # Open the world
    print("Opening the world...")
    level = amulet.load_level(world_path)

    # Assuming 'dimension' and 'version' are known or can be determined
    dimension = "minecraft:overworld"  # Updated dimension to a string
    version = ("bedrock", (1, 16, 20))  # the version that we want the block data in.

    try:
        # print("Clearing the area...")
        # # Clear all blocks in the grid area
        # for x in range(-1,len(height_grid[0]) + 1):
        #     for z in range(-1,len(height_grid) + 1):
        #         for y in range(10):
        #             world_x, world_y, world_z = translate_to_world_coordinates(x, y, z, start_x, base_y, start_z)
        #             level.set_version_block(
        #                 world_x,
        #                 world_y,
        #                 world_z,
        #                 dimension,
        #                 version,
        #                 Block("minecraft", "air")
        #             )

        # Build the mountain
        print("Building the mountain...")
        for z, height_row in enumerate(height_grid):
            for x, height in enumerate(height_row):
                type_flag = type_grid[z][x]
                for y in range(-1, height):
                    world_x, world_y, world_z = translate_to_world_coordinates(
                        x, y, z, start_x, base_y, start_z
                    )
                    level.set_version_block(
                        world_x, world_y, world_z, dimension, version, stone_block
                    )
                    if y == height - 1:
                        block_type = carpet_block if type_flag == "*" else fire_block
                        level.set_version_block(
                            world_x,
                            world_y + 1,
                            world_z,
                            dimension,
                            version,
                            block_type,
                        )

        # Access the root tag of level.dat
        root_tag = level.level_wrapper.root_tag

        # Set the spawn position
        print(f"Setting spawn position to ({spawn_x}, {spawn_y}, {spawn_z})...")
        root_tag["Data"]["SpawnX"] = IntTag(spawn_x)
        root_tag["Data"]["SpawnY"] = IntTag(spawn_y)
        root_tag["Data"]["SpawnZ"] = IntTag(spawn_z)

        # Enable commands by setting allowCommands to 1
        root_tag["Data"]["allowCommands"] = IntTag(1)

        # Change the game mode
        print(f"Changing game mode to {game_mode}...")
        root_tag["Data"]["GameType"] = IntTag(game_mode)

        print("Enabling cheats...")
        root_tag["Data"]["allowCommands"] = IntTag(1)

        # Save changes
        print("Saving the world...")
        level.save()

        print("All tasks completed successfully!")

    finally:
        # Close the world
        level.close()
        print("World closed.")


if __name__ == "__main__":
    generate_mountain()
