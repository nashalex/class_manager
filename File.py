from Enum import Enum
from copy import deepcopy
import json
import CourseInfo
from Settings import JSON_DIR, COURSE_DIR, root_dir
FILE_JSON_DIR = JSON_DIR / 'files'


class FILE_TYPE(Enum):
    note = 0
    hw = 1
    assignment = 2


class File(object):

    """File Superclass"""
    file_type: str
    number: int
    course_identifier: str

    def __init__(self, file_type, number, course_identifier):
        """Create a new File object """
        self.file_type = file_type
        self.number = number
        self.course_identifier
        self.course_info = InfoDescriptor()

        course_dir = CourseInfo.get_course_directory(self.course_identifier)
        self.location = course_dir / str(self.file_type) / f'{self.number}.tex'

    def json_location(self):
        """Return the location of this File's associated json file"""
        return FILE_JSON_DIR / self.course_identifier / str(self.file_type) / f'{self.number}.json'

    def get_latex_header(self):
        """Method that returns a string corresponding to this File's latex header"""

    def write_json_file(self):
        """Write to the json file associated with this File"""
        with open(self.json_location(), 'w') as file:
            json_vars = deepcopy(vars(self))
            for k in ('course_info', 'location'):
                del json_vars[k]  # json_vars.pop(k, None)
            json.dump(json_vars, file)


class InfoDescriptor:
    """Descriptor that returns course information when necessary"""

    def __get__(self, owner: File):
        return CourseInfo.CourseInfo_from_identifier(owner.course_identifier)


class HWFile(File):

    """A file that stores homework files"""

    def __init__(self, number, course_identifier):
        """Make a new HWFile """
        File.__init__(self)
