from dataclasses import dataclass
from pathlib import Path
from copy import deepcopy
import json
from Settings import JSON_DIR, COURSE_DIR, root_dir
COURSE_JSON_DIR = JSON_DIR / 'courses'


def get_json_location(identifier: str) -> Path:
    return COURSE_JSON_DIR / identifier


def get_course_directory(identifier: str) -> Path:
    return COURSE_DIR / identifier


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
        self.identifier = f'{self.department[:4].upper()}{self.number}{self.institution[0].upper}'
        self.syllabus = Syllabus()

        get_course_directory(self.identifier).mkdir()
        get_json_location(self.identifier).touch()

    def write_json_file(self):
        with open(get_json_location(self.identifier), 'w') as file:
            json_vars = deepcopy(vars(self))
            for k in ('identifier', 'syllabus'):
                json_vars.pop(k, None)
            json.dump(json_vars, file)

    def _ct(self):
        return (self.year, self.identifier)

    def __eq__(self, other):
        return self.ct() == other.ct()

    def __ne__(self, other):
        return self.ct() != other.ct()

    def __lt__(self, other):
        return self.ct() < other.ct()

    def __le__(self, other):
        return self.ct() <= other.ct()

    def __gt__(self, other):
        return self.ct() > other.ct()

    def __ge__(self, other):
        return self.ct() >= other.ct()

    def __cmp__(self, other):
        return self.ct().__cmp__(other.ct())


class Syllabus:
    def __get__(self, owner: CourseInfo, objtype=None):
        return Path(owner.directory / 'syllabus.pdf')


def CourseInfo_from_json(file_path: Path or str):
    file_path = str(file_path)
    with open(file_path, 'r') as f:
        course_vars = json.load(f)

    return CourseInfo(**course_vars)


def CourseInfo_from_identifier(identifier: str) -> CourseInfo:
    file_path = get_json_location(identifier)
    return CourseInfo_from_json(file_path)
