import random
from pathlib import Path

from PIL import Image, ImageDraw

# Define floor properties
tile_width = 64  # Width of a single rhombus
tile_height = 64  # Height of a single rhombus


people_sprites = Image.open(Path(__file__).parent / "day_06_people.png")
thing_sprites = Image.open(Path(__file__).parent / "day_06_things.png")

sprite_width = 32
sprite_height = 45

thing_dimension = 64


def get_people_sprite(direction=(0, -1), step=0):
    step_offset = step * sprite_width
    if direction == (0, -1):
        step_offset += 640
    elif direction == (1, 0):
        step_offset += 960
    elif direction == (0, 1):
        step_offset += 320
    elif direction == (-1, 0):
        step_offset += 0

    return people_sprites.crop(
        (step_offset, 0, step_offset + sprite_width, sprite_height)
    )


def get_thing_sprite(num=None):
    if num is None:
        num = random.randrange(0, 43)

    x = num % 14 * thing_dimension
    y = num // 14 * thing_dimension

    return thing_sprites.crop((x, y, x + thing_dimension, y + thing_dimension))


class GridImage:
    def __init__(self, grid):
        self.grid = grid

        # Image size
        self.img_width = grid.width * tile_width
        self.img_height = grid.height * tile_height // 2 + grid.height * tile_height

        self.img = Image.new("RGB", (self.img_width, self.img_height), "white")
        self.draw = ImageDraw.Draw(self.img)

    def get_rhombus_coordinates(self, row, col):
        """Calculate the coordinates for a rhombus at the given grid position.
        (0,0) is at the top middle of the grid.
        x increases downward and right
        y increases downward and left"""

        # Calculate center offset to place (0,0) at top middle
        center_offset = 0
        vertical_offset = self.img_height // 2

        # Calculate base position with y-axis compression (0.577 ≈ 1/√3)
        x = (row + col) * tile_width // 2  # Move right as both x,y increase
        y = (row - col) * tile_height // 2 * 0.577  # Compress y-axis for isometric look

        # Apply offsets
        x = center_offset + x
        y = vertical_offset + y

        # Return all corner coordinates with compressed height
        return {
            "top": (x + tile_width // 2, y),
            "left": (x, y + tile_height // 2 * 0.577),
            "right": (x + tile_width, y + tile_height // 2 * 0.577),
            "bottom": (x + tile_width // 2, y + tile_height * 0.577),
            "center": (x + tile_width // 2, y + tile_height // 2 * 0.577),
        }

    def draw_floor(self):
        # Define colors
        light_gray = (200, 200, 200)
        dark_gray = (100, 100, 100)

        # Draw the isometric tiles
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                coords = self.get_rhombus_coordinates(row, col)

                # Choose color based on the checkerboard pattern
                color = light_gray if (row + col) % 2 == 0 else dark_gray

                # Draw the rhombus
                self.draw.polygon(
                    [coords["top"], coords["right"], coords["bottom"], coords["left"]],
                    fill=color,
                )

    def get_obstacle_sprite(self, pos):
        coords = self.get_rhombus_coordinates(pos[1], pos[0])
        cx, cy = coords["center"]
        cx -= 28
        cy -= 44
        sprite = get_thing_sprite()
        return sprite, (int(cx), int(cy))

    def get_guard_sprite(self, pos, direction=(0, -1), step=0):
        coords = self.get_rhombus_coordinates(pos[1], pos[0])
        cx, cy = coords["center"]
        cx -= sprite_width // 2
        cy -= sprite_height
        sprite = get_people_sprite(direction, step)
        return sprite, (int(cx), int(cy))

    def draw_objects(self, guard_pos, heading=(0, -1), step=0, steps=None):
        if steps is not None:
            steps.append(self.get_rhombus_coordinates(guard_pos[1], guard_pos[0]))
            for s in steps:
                sx, sy = s["center"]
                self.draw.ellipse((sx - 1, sy - 1, sx + 1, sy + 1), fill="grey")
                sx += 2 * heading[0]
                sy += 2 * heading[1]
                self.draw.ellipse((sx - 1, sy - 1, sx + 1, sy + 1), fill="grey")

        sprites = {}
        guard_sprite, sprite_pos = self.get_guard_sprite(guard_pos, heading, step)
        sprites[sprite_pos] = guard_sprite

        random.seed(0)
        for item in self.grid.grid.values():
            sprite, sprite_pos = self.get_obstacle_sprite(item.position)
            sprites[sprite_pos] = sprite

        sprite_positions = list(sprites.keys())
        sprite_positions.sort(key=lambda x: x[1])
        for sprite_pos in sprite_positions:
            self.img.paste(sprites[sprite_pos], sprite_pos, sprites[sprite_pos])

    def crop(self, crop, guard_pos):
        cx, cy = crop
        gx, gy = guard_pos
        coords = self.get_rhombus_coordinates(gy, gx)
        gx, gy = coords["center"]
        self.img = self.img.crop((gx - cx, gy - cy, gx + cx, gy + cy))


class Animator:
    def __init__(self, grid):
        self.grid = grid
        self.images = []
        self.last_pos = None
        self.steps = []

    def draw_position(self, position, heading, crop=None, step=0):
        img = GridImage(self.grid)
        img.draw_floor()
        img.draw_objects(position, heading, step=step, steps=self.steps)
        if crop:
            img.crop(crop, position)
        self.images.append(img.img)

    def draw(self, guard, crop=None, steps=4):
        if self.last_pos:
            lx, ly = self.last_pos
            dx, dy = guard.x - lx, guard.y - ly
            # We create three interim animations to make a smoother animation
            for i in range(steps):
                position = (lx + dx * i / steps, ly + dy * i / steps)
                self.draw_position(position, guard.heading, crop=crop, step=i)
        else:
            self.draw_position(guard.position, guard.heading, crop=crop)
        self.last_pos = guard.position

    def save_animation(self, filename):
        self.images[0].save(
            filename, save_all=True, append_images=self.images[1:], duration=10, loop=0
        )
