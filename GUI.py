import PySimpleGUI as sg
from Manager import CourseManager as CM
from Course import Course as C
from CourseInfo import CourseInfo as CI


class CourseGUIManager:
    def __init__(self):
        self.vals = {}
        # self.dm = CM()  # used for listing all possible values
        self.am = CM()  # active course manager
        self.layout, self.window = None, None
        self.make_window()
        # self.add_course()
        self.main_loop()

    def make_window(self):
        self.refresh_vals()
        self.layout = [
            [sg.Text('Years: ', key='years_label', size=10)],
            [sg.Text('Institutions: ', key='institutions_label', size=10)],
            [sg.Text('Semesters: ', key='semesters_label', size=10)],
            [sg.Text('Courses: ', key='courses_label', size=10)],
            [sg.Button('Add course')]
        ]
        self.create_buttons()
        self.window = sg.Window('course manager', self.layout)

    def refresh_vals(self):
        self.vals = {k: self.am.get_possible_vals(
            key=k) for k in ('year', 'institution', 'semester')}
        # self.vals['courses'] = self.am.courses

    def create_buttons(self):
        for row, (k, possible_vals) in enumerate(self.vals.items()):
            buttons = []
            for i, v in enumerate(possible_vals):
                buttons.append(sg.Button(str(v), key=f'{k}_{i}'))
                print(f'{row,k,v=}')

            # year buttons
            self.layout[row][1:] = buttons
        buttons = []
        for i, c in enumerate(self.am.courses):
            buttons.append(sg.Button(str(c), key=f'courses_{i}'))
        self.layout[3][1:] = buttons

    def update_course_buttons(self):
        # for row, (k, possible_vals) in enumerate(self.vals.items()):
        # for i, v in enumerate(possible_vals):
        # self.window[f'{k}_{i}'].update(text=str(v))
        # for i, _ in enumerate(self.layout[row][len(possible_vals):]):
        # self.window[f'{k}_{i}'].update(visible=False)
        print('updating buttons')
        print(vars(self.am))
        print(self.am.get_courses())
        for i, c in enumerate(self.am.get_courses()):
            self.window[f'courses_{i}'].update(visible=True, text=str(c))
        for i, _ in enumerate(self.layout[3][len(self.am.get_courses()) + 1:]):
            self.window[f'courses_{i}'].update(visible=False)
        # possible_courses = self.am.get

    # def possible_vals(self, key):
        # if key == 'year':
        # return

    def add_course(self):
        ncl = []
        for arg in C.get_CourseInfo_args():
            ncl.append([sg.Text(f'Enter {arg}:')])
            vals = self.am.get_possible_vals(arg)
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

    def main_loop(self):
        while True:
            event, values = self.window.read()
            self.update_course_buttons()
            if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
                self.window.close()
                break
            if event == 'Add course':
                self.window.close()
                self.add_course()
                self.make_window()
            arg, i = event.split('_')
            i = int(i)
            button_val = self.vals.get(arg)[i]
            print(f'\n\nBUTTON CLICKED: {arg = }\n\t{button_val = }\n\n')
            # if type(button_val) is str and button_val.isnumeric():
            # button_val = int(button_val)
            if arg != 'courses':
                setattr(self.am, arg, button_val)
                print(vars(self.am).get(arg))
                print(len(self.am.courses))
            if arg == 'semester':
                self.am.change_semester(button_val)

            # print('You entered ', values[0])


if __name__ == "__main__":
    gm = CourseGUIManager()
