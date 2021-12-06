import inspect
from dataclasses import dataclass
from functools import total_ordering
from pathlib import Path
from copy import deepcopy
import json
from Settings import JSON_DIR, COURSE_DIR

COURSE_JSON_DIR = JSON_DIR / 'courses'


@total_ordering
@dataclass()
class CourseInfo:
    year: int
    semester: str
    institution: str
    department: str
    number: int
    title: str
    professor: str
    website: str

    @staticmethod
    def get_json_location(identifier: str) -> Path:
        return COURSE_JSON_DIR / f'{identifier}.json'

    @staticmethod
    def get_args():
        """Get all the parameters needed for the CourseInfo constructor
        Returns
        -------
        TODO

        """
        # first one is going to be 'self', which causes problems
        return [p.name for p in inspect.signature(CourseInfo.__init__).parameters.values()][1:]

    @staticmethod
    def from_json(file_path: Path or str):
        """Create a new CourseInfo from a JSON Path.

        Parameters
        ----------
        file_path : Path | str
            Path of a CourseInfo JSON file.

        Returns
        -------
        A ``CourseInfo`` object.

        """
        with open(file_path, 'r') as f:
            course_vars = json.load(f)

        return CourseInfo(**course_vars)

    @staticmethod
    def from_identifier(identifier: str):
        """Create a new ``CourseInfo`` from a course identifier

        Parameters
        ----------
        identifier : str
            The identifier of a ``CourseInfo``.

        Returns
        -------
        TODO

        """
        file_path = CourseInfo.get_json_location(identifier)
        return CourseInfo.from_json(file_path)

    @staticmethod
    def get_all_CourseInfos(year: int = None, semester: str = None, institution: str = None):
        """Get all the existing CourseInfos
        Returns
        -------
        All the existing CourseInfos

        """
        # print({k: v for k, v in locals().items() if v})
        filters = {(k, v) for k, v in locals().items() if v}
        # print(filters)
        paths = COURSE_JSON_DIR.glob('*.json')
        infos = []

        if len(filters) == 0:
            for p in paths:
                # fj = CourseInfo.from_json(p)
                # print(fj)
                infos.append(CourseInfo.from_json(p))
        else:
            for p in paths:
                ci = CourseInfo.from_json(p)
                if filters <= set(vars(ci).items()):
                    infos.append(ci)
        return infos

    @staticmethod
    def get_course_directory(identifier: str, semester: str = None, year: int = None) -> Path:
        if (semester, year) == (None, None):
            info = CourseInfo.from_identifier(identifier)
            semester, year = info.semester, info.year

        return COURSE_DIR / f'{semester}{year}' / identifier

    def __post_init__(self):
        self.identifier = f'{self.department[:4].upper()}{self.number}{self.institution[0].upper()}'
        self.write_json()

    def write_json(self):
        json_location = CourseInfo.get_json_location(self.identifier)
        if not json_location.parent.exists():
            json_location.parent.mkdir(parents=True)

        with open(json_location, 'w') as file:
            json_vars = deepcopy(vars(self))
            for k in ('identifier',):
                json_vars.pop(k, None)
            for k, v in json_vars.items():
                if type(v) is str:
                    if v.isnumeric():
                        json_vars[k] = int(v)
                    else:
                        json_vars[k] = v.strip()
            json.dump(json_vars, file)

    def _ct(self):
        return (self.year, self.identifier)

    def __eq__(self, other):
        return self._ct() == other._ct()

    def __lt__(self, other):
        return self._ct() < other._ct()

    def __str__(self):
        return f'{self.identifier[:-1]}: {self.title}'

    def __getitem__(self, item):
        return vars(self)[item]

    def __contains__(self, key):
        return key in vars(self)


if __name__ == "__main__":
    ci = CourseInfo(year=2021, semester='Fall', department='COMP', number=332,
                    title='Analysis of Algorithms', institution='Dickinson', professor='Richard Forrester', website='')
    print(ci)
    ci2 = CourseInfo.from_json(ci.json_location)
    print(ci2)
    print(CourseInfo.get_all_CourseInfos())
