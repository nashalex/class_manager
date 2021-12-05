from Course import Course as C


class CoursesDescriptor(object):

    """Descriptor that manages the classes attribute of Manager"""

    def __get__(self, instance, owner):
        # print(f'calling with vars: {vars(instance)}')
        return C.get_all_Courses(year=instance.year, semester=instance.semester, institution=instance.institution)


class CourseManager(object):

    """Manages all Courses"""
    year: int
    semester: str
    courses = CoursesDescriptor()

    def __init__(self, year: str = None, semester: str = None, institution: str = None):
        """Create a Mananger """
        self.year = year
        self.semester = semester
        self.institution = institution
        # if None in (year, semester, institution):
        # c = self.courses[0]
        # if not year:
        # self.year = c.info.year
        # if not semester:
        # self.semester = c.info.semester
        # if not institution:
        # self.institution = c.info.institution

    def get_possible_vals(self, key):
        # return [v for k,v in
        # return [v for k, v in d.items() for d in self]
        # vals = []
        # for course in self:
        # vals.append(course[key])
        if key not in self[0]:
            raise Exception(f'{key} is not a valid course attribute!')

        return list({c[key] for c in self})
        # return [v for d in self for k, v in d.items() if k == key]

    def get_possible_args(self):
        possible_args = {}
        for arg in C.get_CourseInfo_args():
            possible_args[arg] = self.get_possible_vals(arg)
        return possible_args

    # def new_course(self, department):
        # """Make a new Course using current information"""

        # year: int
        # semester: str
        # department: str
        # number: int
        # title: str
        # institution: str
        # professor: str
        # website: str

    def __getitem__(self, item):
        return self.courses[item]

    def __iter__(self):
        return iter(self.courses)

    def __contains__(self, identifier):
        ids = [c['identifier'] for c in self]
        return identifier in ids

    def change_year(self, year):
        self.year = year

    def change_semester(self, semester):
        self.semester = semester

    def get_courses(self):
        return C.get_all_Courses(year=self.year, semester=self.semester, institution=self.institution)


if __name__ == "__main__":
    m = CourseManager(2021)
    # for c in m:
    # print(c)
    # print(m.get_possible_vals(key='year'))
    # print(f'{"COMP332D" in m = }')
    print(vars(m))
    print(f'{len(m.courses) = }')
    # m.semester = "Spring"
    m.change_semester('Spring')
    print(vars(m))
    print(f'{len(m.courses) = }')
    # print(m.get_possible_args())
