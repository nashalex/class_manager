from datetime import date
import re
from functools import total_ordering
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from pathlib import Path
import json
import CourseInfo
from Settings import JSON_DIR, COURSE_DIR, root_dir
from datetime import datetime

FILE_JSON_DIR = JSON_DIR / 'files'

header_pattern = re.compile(r'\\(.*?){(\d+)}{(\w{3} \d{2})}(?:{(.*?)})?')


class FileType(Enum):
    """Enum for the different types of supported LaTeX files
    """
    note = 0
    homework = 1
    assignment = 2


def subdir_name(file_type: FileType, title: str = '') -> str:
    """Get the subdirectory name of a specific FileType

    """
    if file_type == FileType.homework:
        return 'hw'
    elif file_type == FileType.assignment and len(title) > 0:
        return title.lower()
    else:
        return file_type.name + "s"


def json_directory(course_identifier: str, file_type: FileType) -> Path:
    """Get the json directory that holds all the files for a course

    Parameters
    ----------
        course_identifier : str
            The identifier of a course.
        file_type: FileType
            The FileType of the file in question
    """
    return FILE_JSON_DIR / course_identifier / subdir_name(file_type)


def get_file_directory(course_identifier: str, file_type: FileType, title: str = ''):
    """Get the directory of all files of a course, of type FileType"""

    course_dir = CourseInfo.get_course_directory(course_identifier)
    return course_dir / subdir_name(file_type, title)


def parse_header(header: str):
    # \[file_type]{number}{date}{title}
    match = header_pattern.match(header)
    file_type = FileType[match[1]]
    number = int(match[2])
    file_date = datetime.strptime(
        match[3], '%b %d').date().replace(year=date.today().year)
    title = match[4] if match[4] else ''
    return {'file_type': file_type, 'number': number, 'file_date': file_date, 'title': title}


def TexFile_from_path(texfile_path):
    course_identifier = texfile_path.parent.parent.name
    with open(texfile_path, 'r') as file:
        header = file.readline().strip()
    header_vars = parse_header(header)
    tf = TexFile(course_identifier=course_identifier, **header_vars)
    return tf


def TexFile_from_json(file_path: Path or str):
    """Create a new TexFile from a JSON file.
    Parameters
    ----------
        file_path: Path or str:
            The path to the JSON file.
    """
    with open(file_path, 'r') as f:
        file_vars = json.load(f)

    return TexFile(**file_vars)


@total_ordering
@dataclass
class TexFile(object):

    """TexFile Superclass"""
    course_identifier: str
    file_type: FileType or str
    number: int
    title: str = ''
    file_date: date or str = date.today()
    active: bool = True

    def __post_init__(self):
        """Create a new TexFile object """
        if self.title == None:
            self.title = ''

        # if loaded from json this will have happened:
        if type(self.file_date) is str:
            self.file_date = date.fromisoformat(self.file_date)

        if type(self.file_type) is str:
            self.file_type = FileType[self.file_type]

        self.location = get_file_directory(
            self.course_identifier, self.file_type, self.title) / f'{self.number:02d}.tex'

        self.json_location = json_directory(
            self.course_identifier, self.file_type) / f'{self.number:02d}.json'

        if not self.json_location.parent.exists():
            self.json_location.parent.mkdir(parents=True)

        if not self.location.parent.exists():
            self.location.parent.mkdir(parents=True)
        self.write_json()
        self.write_file()

    def formatted_date(self):
        return self.file_date.strftime(r'%b %d')

    def get_latex_header(self):
        """Method that returns a string corresponding to this TexFile's latex header"""

        if self.file_type == FileType.homework:
            return f'\\{self.file_type.name}{{{self.number:02d}}}{{{self.formatted_date()}}}'
        else:
            return f'\\{self.file_type.name}{{{self.number:02d}}}{{{self.formatted_date()}}}{{{self.title}}}'

    def write_json(self):
        """Write to the json file associated with this TexFile"""
        with open(self.json_location, 'w') as file:
            json_vars = deepcopy(vars(self))
            for k in ('location', 'json_location'):
                del json_vars[k]  # json_vars.pop(k, None)

            json_vars['file_type'] = self.file_type.name
            json_vars['file_date'] = str(self.file_date)
            json.dump(json_vars, file)

    def write_file(self):
        if self.location.exists():
            return

        with open(self.location, 'w') as f:
            f.write(self.get_latex_header())

    def set_active(self, Bool: bool = True):
        self.active = Bool
        self.write_json()

    def include_str(self):
        return '/'.join(list(self.location.parts)[-2:])

    def type_and_num(self):
        return self.file_type, self.number

    def ct(self):
        # return (self.course_identifier, self.file_type, self.number, self.file_date)
        return (self.file_type, self.number, self.title)

    def __eq__(self, other):
        ct = other.ct() if type(other) is TexFile else other
        return self.ct() == ct

    def __lt__(self, other):
        ct = other.ct() if type(other) is TexFile else other
        return self.ct() < ct

    def __str__(self):
        s = f'{self.course_identifier} {self.file_type.name} {self.number}'
        if len(self.title) > 0:
            s += f': {self.title}'
        if self.active:
            s += '  (active)'
        return s


if __name__ == "__main__":
    t = TexFile("COMP332D", FileType.homework, 1)
    t.write_file()
    print(t)
    loc = t.json_location
    print(loc)
    t2 = TexFile_from_json(loc)
    print(t2)
    loc2 = t.location
    t3 = TexFile_from_path(loc2)
    print("seeing how to generate from a location")
    print(t3)
    # print(get_course_files('COMP332D', FileType.assignment))
