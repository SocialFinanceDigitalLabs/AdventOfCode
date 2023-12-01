from pathlib import Path

import usersettings

settings = usersettings.Settings("kws.aoc23")
settings.add_setting("username", str)
settings.load_settings()


class Config:
    INPUTS_DIR = Path(__file__).parent.parent / "inputs"
    SAMPLE_DIR = INPUTS_DIR / "samples"

    @property
    def USER_DIR(self):
        return self.INPUTS_DIR / settings.username


config = Config()
