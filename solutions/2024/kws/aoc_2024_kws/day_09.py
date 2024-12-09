import math
from typing import Generator
import click
from aocd import submit

from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config

from rich.progress import track


def part_1(input_data, sample):
    disk_image = []
    file_id = 0
    while input_data:
        data_length = int(input_data[0])
        if len(input_data) > 1:
            free_space_after = int(input_data[1])
        else:
            free_space_after = 0
        print(data_length, free_space_after)

        for _ in range(data_length):
            disk_image.append(file_id)

        for _ in range(free_space_after):
            disk_image.append(".")

        input_data = input_data[2:]
        file_id += 1

    while "." in disk_image:
        first_dot = disk_image.index(".")
        last_file = disk_image.pop(-1)
        if last_file == ".":
            continue
        disk_image[first_dot] = last_file


    check_sum = 0
    for ix, x in enumerate(disk_image):
        check_sum += ix * x

    print(check_sum)

    if not sample:
        submit(check_sum, part="a", day=9, year=2024)


class FileData:
    def __init__(self, id: int, length: int):
        self.id = id
        self.length = length

    def __repr__(self):
        return f"File {self.id} from {self.start} to {self.start + self.length - 1}"

class FileRecord:
    def __init__(self, start_pos: int, file: FileData):
        self.start_pos = self.original_start_pos = start_pos
        self.file = file
        self.checked = False

    @property
    def end_pos(self):
        return self.start_pos + self.file.length - 1

    def __repr__(self):
        return f"FileRecord {self.file.id} from {self.start_pos} to {self.start_pos + self.file.length - 1}"
    
    def __hash__(self):
        return hash(self.file.id)
    
    def __eq__(self, other):
        return self.file.id == other.file.id

class DiskMap:
    def __init__(self, ):
        self.files = {}

    def add_file(self, start_pos: int, file: FileData):
        self.files[file.id] = FileRecord(start_pos, file)

    def get_file_by_id(self, id: int):
        for file in self.files:
            if file.file.id == id:
                return file
        return None
    
    def get_max_file_id(self):
        return max([file.file.id for file in self.files])
    
    def order_by_start_pos(self, reverse=False):
        return sorted(self.files.values(), key=lambda x: x.start_pos, reverse=reverse)
    
    def order_by_id(self, reverse=False):
        return sorted(self.files.values(), key=lambda x: x.file.id, reverse=reverse)
    
    def get_free_space(self) -> Generator[int, None, None]:
        ordered_files = self.order_by_start_pos()
        
        for i in range(len(ordered_files) - 1):
            current_file = ordered_files[i]
            next_file = ordered_files[i + 1]
            free_space = next_file.start_pos - (current_file.start_pos + current_file.file.length)
            if free_space > 0:
                yield current_file.start_pos + current_file.file.length, free_space

    def find_free_space(self, size: int):
        for free_space_start, free_space_length in self.get_free_space():
            if free_space_length >= size:
                return free_space_start, free_space_length
        return None

    def __len__(self):
        return len(self.files)

    def __repr__(self):
        return f"DiskMap {self.files}"
    
class ImageGenerator:
    def __init__(self, disk_length: int, output_dir: str):
        self.disk_length = disk_length
        self.output_dir = output_dir
        self.dimensions = math.ceil(math.sqrt(disk_length))
        self.step = 0

    def generate_image(self, files: DiskMap, current_block: FileRecord):
        from PIL import Image, ImageDraw
        import os

        # Create a new image with white background
        img = Image.new('RGB', (self.dimensions, self.dimensions), 'white')
        draw = ImageDraw.Draw(img)

        sorted_records = files.order_by_start_pos()
        for record in sorted_records:
            if record is current_block and record.start_pos == record.original_start_pos:
                color = 'red'
            elif record is current_block:
                color = 'purple'
            elif record.start_pos != record.original_start_pos:
                color = 'darkgreen'
            elif record.checked:
                color = 'green'
            else:
                color = 'blue'
            
            
            # Color each pixel in the file's range
            for pos in range(record.start_pos, record.end_pos + 1):
                y = pos // self.dimensions
                x = pos % self.dimensions
                draw.point((x, y), fill=color)

            if record is current_block:
                for pos in range(record.original_start_pos, record.original_start_pos + record.file.length):
                    y = pos // self.dimensions
                    x = pos % self.dimensions
                    draw.point((x, y), fill=color)

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Save the image
        img.save(f"{self.output_dir}/step_{self.step}.png")
        self.step += 1

def part_2(input_data, sample):
    files = DiskMap()
    start_pos = 0
    while input_data:
        data_length = int(input_data[0])
        if len(input_data) > 1:
            free_space_after = int(input_data[1])
        else:
            free_space_after = 0

        files.add_file(start_pos, FileData(len(files), data_length))
        start_pos += data_length + free_space_after
        input_data = input_data[2:]

    disk_length = files.order_by_start_pos()[-1].end_pos

    image_generator = ImageGenerator(disk_length, "day09/images")
    for block in track(files.order_by_id(reverse=True), description="Checking files"):
        block.checked = True
        size = block.file.length

        free_space = files.find_free_space(size)
        if free_space and free_space[0] < block.start_pos:
            block.start_pos = free_space[0]
        image_generator.generate_image(files, block)
    image_generator.generate_image(files, None)
        


    print("\nFile layout is now\n")
    check_sum = 0
    for block in files.order_by_start_pos():
        print(block)
        for i in range(block.start_pos, block.end_pos+1):
            check_sum += i * block.file.id

    print(check_sum)
    if not sample:
        submit(check_sum, part="b", day=9, year=2024)


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day09(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day09.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day09.txt").read_text()
        
    # part_1(str(input_data), sample)

    part_2(str(input_data), sample)