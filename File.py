from datetime import date
from functools import total_ordering
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from pathlib import Path
import json
import CourseInfo
from Settings import JSON_DIR, COURSE_DIR, root_dir

FILE_JSON_DIR = JSON_DIR / 'files'


class FileType(Enum):
    """Enum for the different types of supported LaTeX files
    """
    note = 0
    homework = 1
    assignment = 2


def subdir_name(file_type: FileType, title: str = None) -> str:
    """Get the subdirectory name of a specific FileType

    """
    if file_type == FileType.homework:
        return 'hw'
    elif file_type == FileType.assignment and title:
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


def get_file_directory(course_identifier: str, file_type: FileType, title: str = None):
    """Get the directory of all files of a course, of type FileType"""

    course_dir = CourseInfo.get_course_directory(course_identifier)
    return course_dir / subdir_name(file_type)


def get_course_files(course_identifier: str,
                     file_types: FileType or list[FileType] = FileType) -> list[Path]:
    """Returns a list all TexFiles of a specified course

    Parameters
    ----------
        course_identifier: str
            The course to get files from.
        file_types: FileType or list[FileType]
            Limit search to only the files of type FileType.
            Default: all file types.
    """

    if type(file_types) is FileType:
        file_types = [file_types]
    files = []
    for ft in file_types:
        directory = json_directory(course_identifier, ft)
        json_paths = list(directory.glob('*'))
        files.extend([TexFile_from_json(jp) for jp in json_paths])
    return files


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
    title: str = None
    file_date: date or str = date.today()
    active: bool = True

    def __post_init__(self):
        """Create a new TexFile object """

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
        return (self.course_identifier, self.file_type, self.number, self.file_date)

    def __eq__(self, other):
        return self.ct() == other.ct()

    def __lt__(self, other):
        return self.ct() < other.ct()

    def __str__(self):
        s = f'{self.course_identifier} {self.file_type.name} {self.number}'
        if self.title:
            s += f': {self.title}'
        return s


if __name__ == "__main__":
    t = TexFile("COMP332D", FileType.homework, 1)
    t.write_file()
    print(t)
    loc = t.json_location
    print(loc)
    t2 = TexFile_from_json(loc)
    print(t2)
    print(get_course_files('COMP332D', FileType.assignment))
