import CourseInfo
from pathlib import Path
from Settings import JSON_DIR, COURSE_DIR, root_dir


class Course(object):
    """Stores a Course and its Files"""

    course_info: CourseInfo.CourseInfo

    def __init__(self, course_info: CourseInfo.CourseInfo = None, json_file: Path or str = None):
        """Create a new Course Object

        Parameters
        ----------
        course_info : A ``CourseInfo`` 


        """
        if course_info:
            pass
        elif self.json_file:
            course_info = CourseInfo.CourseInfo_from_json(json_file)
        else:
            raise Exception()
        self.course_info = course_info


class Files:
    """File Descriptor class that retrives files"""

    def __get__(self, owner: Course):
        # directory = owner.directory
        pass
