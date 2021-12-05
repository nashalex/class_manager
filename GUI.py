import PySimpleGUI as sg
from Manager import CourseManager as CM
from Course import Course as C
from CourseInfo import CourseInfo as CI
from File import (TexFile as TFile, FileType as FT)
import subprocess


class CourseGUIManager:
    def __init__(self):
        self.year = None
        self.semester = None
        self.institution = None
        self.make_course_window()

    def make_course_window(self):
        institutions = CI.existing_vals('institution')
        years = CI.existing_vals('year', institution=self.institution)
        semesters = CI.existing_vals(
            'semester', year=self.year, institution=self.institution)
        courses = C.get_all_Courses(
            year=self.year, semester=self.semester, institution=self.institution)

        layout = [
            [sg.Text('Institutions: ', key='institutions_label', size=10)] +
            [sg.Button(str(v), key=('institution', i))
             for i, v in enumerate(institutions)],

            [sg.Text('Years: ', key='years_label', size=10)] +
            [sg.Button(str(v), key=('year', i)) for i, v in enumerate(years)],

            [sg.Text('Semesters: ', key='semesters_label', size=10)] +
            [sg.Button(str(v), key=('semester', i))
             for i, v in enumerate(semesters)],

            [sg.Text('Courses: ', key='courses_label', size=10)] +
            [sg.Button(str(v), key=('course', i))
             for i, v in enumerate(courses)],
            [sg.Button('Add course')]
        ]
        e, v = sg.Window('course manager', layout).read(close=True)
        print(e)
        # if e ==
        if e == 'Add course':
            self.add_course()
        elif type(e) is tuple:
            var, index = e
            val = locals()[f'{var}s'][index]
            if var == 'course':
                self.course_manager(courses[index])
            else:
                setattr(self, var, val)

                self.make_course_window()

        return e, v

    def add_course(self):
        ncl = []
        for arg in C.get_CourseInfo_args():
            ncl.append([sg.Text(f'Enter {arg}:')])
            vals = CI.existing_vals(arg)
            print(f'\n\nPRINTING VALS: {vals}')
            default = vals[0] if len(vals) > 0 else ''
            # if len(vals) > 0:
            ncl.append([sg.Combo(values=vals, default_value=default, key=arg)])
        ncl.append([sg.Button('done')])
        w = sg.Window('new course', ncl)

        e, v = w.read(close=True)
        if e == 'done':
            c = CI(**v)
            print(f'made new course: {c}')

        print(v)

    @staticmethod
    def make_file_tab(identifier, file_type: FT):
        ft_files = sorted(TFile.get_course_files(
            identifier, file_type))
        ft_layout = [
            [sg.Listbox(values=[f for f in ft_files],
                        select_mode='extended', key=file_type.name, size=(30, 25))]
        ]
        return sg.Tab(file_type.name, ft_layout)

    def course_manager(self, course):
        # c = C(info)
        identifier = course.info.identifier
        # notes_files = sorted(TFile.get_course_files(identifier, FT.note))
        # notes_layout = [
        # [sg.Listbox(values=[str(f) for f in notes_files],
        # select_mode='extended', key='notes', size=(30, 25))]
        # ]
        # hw_files = sorted(TFile.get_course_files(identifier, FT.homework))
        # hw_layout = [
        # [sg.Listbox(values=[str(f) for f in hw_files],
        # select_mode='extended', key='notes', size=(30, 25))]
        # ]
        # layout = [[sg.TabGroup([[sg.Tab('notes', notes_layout), sg.Tab('hw', hw_layout)]])
        # ]]
        layout = [
            [sg.TabGroup(
                [
                    [CourseGUIManager.make_file_tab(
                        identifier, file_type) for file_type in FT]
                ], key='tab')
             ],
            [sg.Button('open'), sg.Button('new file')]
        ]
        e, v = sg.Window('tabs', layout).read(close=True)
        print(v)
        if v['tab'] is not None:
            file_type = FT[v['tab'][:-1]]
        if e == 'open':
            active_files = v[file_type.name]
            print(file_type)
            subprocess.call(('open', active_files[0].location))
        elif e == 'new file':
            CourseGUIManager.new_tex_file(course, file_type)
            # self.new_tex_file(
            # course.new

    def new_tex_file(course, file_type):
        print(file_type)
        print(course.largest_file_number(file_type))
        layout = [
            [sg.Text('enter a file number: '), sg.InputText(
                default_text=1 + course.largest_file_number(file_type), key='number')],
            [sg.Text('enter a title: '), sg.Combo(
                values=course.get_possible_titles(file_type), key='title', size=(30, 10))],
            [sg.Button('make file'), sg.Button('cancel')]
        ]
        e, v = sg.Window('new file', layout).read(close=True)
        if e == 'cancel':
            return

        title = v['title']
        number = int(v['number'])
        file = course.new_tex_file(file_type, number=number, title=title)
        subprocess.call(('open', file.location))


if __name__ == "__main__":
    gm = CourseGUIManager()
