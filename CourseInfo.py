from dataclasses import dataclass
from functools import total_ordering
from pathlib import Path
from copy import deepcopy
import json
from Settings import JSON_DIR, COURSE_DIR, root_dir
COURSE_JSON_DIR = JSON_DIR / 'courses'


def get_json_location(identifier: str) -> Path:
    return COURSE_JSON_DIR / identifier


def get_course_directory(identifier: str) -> Path:
    return COURSE_DIR / identifier


@total_ordering
@dataclass()
class CourseInfo:
    year: int
    semester: str
    department: str
    number: int
    title: str
    institution: str
    professor: str
    website: str

    def __post_init__(self):
        self.identifier = f'{self.department[:4].upper()}{self.number}{self.institution[0].upper()}'

        self.directory = get_course_directory(self.identifier)
        self.json_location = get_json_location(self.identifier)
        self.write_json()

    def get_syllabus(self):
        return self.directory / 'syllabus.pdf'

    def write_json(self):
        if self.json_location.exists():
            return

        if not self.json_location.parent.exists():
            self.json_location.parent.mkdir(parents=True)

        with open(get_json_location(self.identifier), 'w') as file:
            json_vars = deepcopy(vars(self))
            for k in ('identifier', 'directory', 'json_location'):
                json_vars.pop(k, None)
            json.dump(json_vars, file)

    def _ct(self):
        return (self.year, self.identifier)

    def __eq__(self, other):
        return self.ct() == other.ct()

    def __lt__(self, other):
        return self.ct() < other.ct()

    def __str__(self):
        return f'{self.identifier[:-1]}: {self.title}'


def CourseInfo_from_json(file_path: Path or str):
    file_path = str(file_path)
    with open(file_path, 'r') as f:
        course_vars = json.load(f)

    return CourseInfo(**course_vars)


def CourseInfo_from_identifier(identifier: str) -> CourseInfo:
    file_path = get_json_location(identifier)
    return CourseInfo_from_json(file_path)


if __name__ == "__main__":
    ci = CourseInfo(year=2021, semester='Fall', department='COMP', number=332,
                    title='Analysis of Algorithms', institution='Dickinson', professor='Richard Forrester', website='')
    print(ci)
    ci2 = CourseInfo_from_json(ci.json_location)
    print(ci2)
