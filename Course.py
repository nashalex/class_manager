import CourseInfo
from pathlib import Path
from Settings import JSON_DIR, COURSE_DIR, root_dir
import File
from File import FileType as FT
from File import TexFile as TFile


class TexFilesDescriptor:
    """File Descriptor class that retrives files"""

    def __get__(self, owner, objtype=None):
        return sorted(File.get_course_files(owner.course_info.identifier))


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
        self.active_files_file = self.course_info.directory / 'active_files.tex'

    def __str__(self):
        return str(self.course_info)

    def largest_file_number(self, file_type: FT):
        return max(f.number for f in self.files if f.file_type == file_type)
        # filtered = filter(lambda f: f.file_type == file_type, self.files)
        # return max(filtered, key=lambda f: f.number).number

    def new_tex_file(self, file_type: FT):
        TFile(course_identifier=self.course_info.identifier,
              file_type=file_type, number=1 + self.largest_file_number(file_type))
        # self.update_master(
        self.update_active_files()

    # def update_master(self, files: list[TFile] or TFile):
        # if type(files) is TFile:
        # files = [files]

    def get_file(self, ft: FT, number: int):
        """get a file from its file_type and number"""
        return next(f for f in self.files if f.type_and_num() == (ft, number))

    def set_active_files(self, to_activate=TFile or list[TFile]
                         or (FT, int), update=True):
        """Set which files are active

        Parameters
        ----------
            to_activate: list of TexFile's or a TexFile
                A list of files to set as active. All TexFiles not in this list will be set as inactive.
            update: bool
                If ``True``, Update ``active_file.tex`` after setting the active files.
    """
        if type(to_activate) is not list:
            to_activate = list[to_activate]
        if type(to_activate[0]) is TFile:
            a_tuples = [a.type_and_num() for a in to_activate]
        else:
            a_tuples = to_activate

        for f in self.files:
            # deactivate it if f is not in active
            f.set_active(f.type_and_num() in a_tuples)
        if update:
            self.update_active_files()

    def update_active_files(self):
        active_files = (f for f in self.files if f.active)
        with open(self.active_files_file, 'w') as f:
            for active_file in active_files:
                f.write(f'\\include{{{active_file.include_str()}}}\n')


if __name__ == "__main__":
    c = Course('COMP332D')
    print(c)
    print(c.files)
    print('\n'.join(str(f) for f in c.files))
    print(c.largest_file_number(FT.homework))
    c.new_tex_file(FT.homework)
    print('\n'.join(str(f) for f in c.files))
    print(c.get_file(FT.homework, 15))

    c.set_active_files([(FT.homework, 14),
                       (FT.homework, 15)])
