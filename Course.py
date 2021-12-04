import CourseInfo
from pathlib import Path
from Settings import JSON_DIR, COURSE_DIR, root_dir
import File
from File import FileType as FT
from File import TexFile as TFile


def get_course_files(course_identifier: str,
                     file_types: FT or list[FT] = FT) -> list[Path]:
    """Returns a list all TexFiles of a specified course

    Parameters
    ----------
        course_identifier: str
            The course to get files from.
        file_types: FileType or list[FileType]
            Limit search to only the files of type FileType.
            Default: all file types.
    """

    if type(file_types) is FT:
        file_types = [file_types]
    files = []
    for ft in file_types:
        directory = File.json_directory(course_identifier, ft)
        json_paths = list(directory.glob('*'))
        files.extend([File.TexFile_from_json(jp) for jp in json_paths])
    return files


class TexFilesDescriptor:
    """File Descriptor class that retrives files"""

    def __get__(self, owner, objtype=None):
        return sorted(get_course_files(owner.course_info.identifier))


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
        self.make_master()

    def __str__(self):
        return str(self.course_info)

    def largest_file_number(self, file_type: FT):
        return max((f.number for f in self.files if f.file_type == file_type or 0), default=0)
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

    def get_file(self, ft: FT, number: int, title: str = ''):
        """get a file from its file_type and number"""
        return next((f for f in self.files if f == (ft, number, title)), None)

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

        for i, a in enumerate(to_activate):
            if type(a) is not TFile:
                to_activate[i] = self.get_file(*a)

        for f in self.files:
            # deactivate it if f is not in active
            f.set_active(f in to_activate)
        if update:
            self.update_active_files()

    def update_active_files(self):
        active_files = (f for f in self.files if f.active)
        with open(self.active_files_file, 'w') as f:
            for active_file in active_files:
                f.write(f'\\include{{{active_file.include_str()}}}\n')

    def make_master(self):
        if self.master_file_location.exists():
            return
        with open(self.master_file_location, 'w') as file:
            file.write(r'''\documentclass[a4paper]{article}
\input{../preamble.tex}
''' f'\\title{{{self.course_info.title}}}' r'''
\PassOptionsToPackage{hidelinks}{hyperref}
\author{Alex Nash}
\date{\vspace{-3ex}}
\begin{document}
    \maketitle
    \input{active_files.tex}
\end{document} ''')


if __name__ == "__main__":
    c = Course('COMP332D')
    print(c)
    # print(c.files)
    print('\n'.join(str(f) for f in c.files))
    # print(c.largest_file_number(FT.homework))
    c.new_tex_file(FT.homework)
    print('\n'.join(str(f) for f in c.files))
    print(c.get_file(FT.homework, 15))

    c.set_active_files([(FT.homework, 14),
                       (FT.homework, 15)])
