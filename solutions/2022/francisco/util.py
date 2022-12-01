import os



class FileParser:

    def __init__(self, dir_path: str, file_name: str) -> None:
        self.dir_path = dir_path
        self.file_name = file_name
    
    def load(self) -> list:
        with open(self.file_path) as f:
            data = [d.strip("\n") for d in f.readlines()]
        return data

    def read(self) -> list[str]:
        self.file_path = os.path.join(self.dir_path, self.file_name)
        return self.load()

