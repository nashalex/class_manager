from pathlib import Path
import datetime
import json
root_dir = Path.home() / 'class_man'
COURSE_DIR = root_dir / 'Courses'
JSON_DIR = root_dir / 'json'


SETTINGS_LOCATION = root_dir / 'settings.json'


class Settings:
    last_year: str
    last_course_identifier: str
    last_semester: str

    def __init__(self):
        if SETTINGS_LOCATION.exists():
            self.load_json()
        else:
            self.last_year = datetime.date.today().year

    def load_json(self):
        for k, v in json.load(SETTINGS_LOCATION):
            setattr(self, k, v)

    def write_json(self):
        json.dump(vars(self), SETTINGS_LOCATION)
