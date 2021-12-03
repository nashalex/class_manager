from Enum import Enum
import CourseInfo
from Settings import JSON_DIR, COURSE_DIR, root_dir
FILE_JSON_DIR = JSON_DIR / 'files'


class FILE_TYPE(Enum):
    HW = 0
    ASSIGNMENT = 1
    NOTES = 2


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
        return FILE_JSON_DIR / self.course_identifier / str(self.file_type) / f'{self.number}.json'


class InfoDescriptor:
    """Descriptor that returns course information when necessary"""

    def __get__(self, owner: File):
        return CourseInfo.CourseInfo_from_identifier(owner.course_identifier)


class HWFile(File):

    """A file that stores homework files"""

    def __init__(self, number, course_identifier):
        """Make a new HWFile """
        File.__init__(self)
