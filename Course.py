import CourseInfo
from CourseInfo import CourseInfo as CI
from pathlib import Path
from Settings import JSON_DIR, COURSE_DIR, root_dir
import File
from File import FileType as FT
from File import TexFile as TFile
import inspect


class TexFilesDescriptor:
    """File Descriptor class that retrives files"""

    def __get__(self, owner, objtype=None):
        return sorted(TFile.get_course_files(owner.info.identifier))


class Course:
    """Stores a Course and its Files"""

    info: CourseInfo.CourseInfo
    files = TexFilesDescriptor()

    @staticmethod
    def get_CourseInfo_args():
        """Get all the parameters needed for the CourseInfo constructor
        Returns
        -------
        TODO

        """
        # first one is going to be 'self', which causes problems
        return [p.name for p in inspect.signature(CI.__init__).parameters.values()][1:]

    @ staticmethod
    def get_all_Courses(year: int = None, semester: str = None, institution: str = None):
        """Get all the existing Courses
        Returns
        -------
        All the existing CourseInfos

        """
        return [Course(ci) for ci in CI.get_all_CourseInfos(**locals())]

    def __init__(self, info: CourseInfo.CourseInfo or Path or str):
        """Create a new Course Object

        Parameters
        ----------
        info : A CourseInfo.CourseInfo or Path or str
            A ``CourseInfo`` object, or the identifier of one, or the path to the JSON file of one.
        """

        if type(info) is CI:
            self.info = info
        elif Path(info).exists():
            self.info = CI.from_json(info)
        else:
            self.info = CI.from_identifier(
                info)
        self.master_file_location = self.info.directory / 'master.tex'
        self.active_files_file = self.info.directory / 'active_files.tex'
        self.make_master()
        self.update_active_files()

    def __str__(self):
        return str(self.info)

    def largest_file_number(self, file_type: FT):
        return max((f.number for f in self.files if f.file_type == file_type or 0), default=0)
        # filtered = filter(lambda f: f.file_type == file_type, self.files)
        # return max(filtered, key=lambda f: f.number).number

    def new_tex_file(self, file_type: FT, number: int = None, title: str = None):
        if number is None:
            number = 1 + self.largest_file_number(file_type)
        f = TFile(course_identifier=self.info.identifier,
                  file_type=file_type, number=number, title=title)
        # self.update_master(
        self.update_active_files()
        return f

    def get_possible_titles(self, file_type: FT):
        return list({f.title for f in self.files if f.file_type == file_type})

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
''' f'\\title{{{self.info.title}}}' r'''
\PassOptionsToPackage{hidelinks}{hyperref}
\author{Alex Nash}
\date{\vspace{-3ex}}
\begin{document}
    \maketitle
    \input{active_files.tex}
\end{document} ''')

    def __getitem__(self, item):
        return vars(self.info)[item]

    def __contains__(self, item):
        return item in vars(self.info)


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

    print(Course.get_CourseInfo_args())
