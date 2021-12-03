import CourseInfo
from Settings import JSON_DIR, COURSE_DIR, root_dir
FILE_JSON_DIR = JSON_DIR / 'files'


class File(object):

    """File Superclass"""
    file_type: str
    number: int
    course_identifier: str

    def __init__(self, file_type, number, course_identifier):
        """TODO: to be defined. """
        self.file_type = file_type
        self.number = number
        self.course_identifier
        self.course_info = InfoDescriptor()

        course_dir = CourseInfo.get_course_directory(self.course_identifier)
        self.location = course_dir / str(self.file_type) / f'{self.number}.tex'

    def json_location(self):
        return FILE_JSON_DIR / self.course_identifier / str(self.file_type) / f'{self.number}.json'


class InfoDescriptor:
    def __get__(self, owner: File):
        return CourseInfo.CourseInfo_from_identifier(owner.course_identifier)
