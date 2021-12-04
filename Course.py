import CourseInfo
from pathlib import Path
from Settings import JSON_DIR, COURSE_DIR, root_dir
import File


class TexFilesDescriptor:
    """File Descriptor class that retrives files"""

    def __get__(self, owner, objtype=None):
        return File.get_course_files(owner.course_info.identifier)


class Course(object):
    """Stores a Course and its Files"""

    course_info: CourseInfo.CourseInfo
    files = TexFilesDescriptor()

    def __init__(self, course_info: CourseInfo.CourseInfo or Path or str):
        """Create a new Course Object

        Parameters
        ----------
        course_info : A CourseInfo.CourseInfo or Path or str
            A ``CourseInfo`` object, or the identifier of one, or the path to the JSON file of one.
        """

        if type(course_info) is CourseInfo.CourseInfo:
            self.course_info = course_info
        elif Path(course_info).exists():
            self.course_info = CourseInfo.CourseInfo_from_json(course_info)
        else:
            self.course_info = CourseInfo.CourseInfo_from_identifier(
                course_info)
        self.master_file_location = self.course_info.directory / 'master.tex'

    def __str__(self):
        return str(self.course_info)

    def largest_file_number(self, file_type: File.FileType):
        return max(f.number for f in self.files if f.file_type == file_type)
        # filtered = filter(lambda f: f.file_type == file_type, self.files)
        # return max(filtered, key=lambda f: f.number).number

    def new_tex_file(self, file_type: File.FileType):
        File.TexFile(course_identifier=self.course_info.identifier,
                     file_type=file_type, number=1 + self.largest_file_number(file_type))


if __name__ == "__main__":
    c = Course('COMP332D')
    print(c)
    print(c.files)
    print('\n'.join(str(f) for f in c.files))
    print(c.largest_file_number(File.FileType.homework))
    c.new_tex_file(File.FileType.homework)
    print('\n'.join(str(f) for f in c.files))
