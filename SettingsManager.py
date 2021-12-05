from Settings import SETTINGS_LOCATION
import json


def get_settings():
    return Settings()


def set_settings(last_year=None, last_course_identifier=None, last_semester=None):
    s = Settings()
    for k, v in locals():
        if v:
            setattr(s, k, v)
    s.write_json()


class Settings:
    import Course
    last_year: str
    last_course_identifier: str
    last_semester: str

    def __init__(self):
        if SETTINGS_LOCATION.exists():
            self.load_json()
        else:
            from CourseInfo import CourseInfo as CI
            infos = CI.get_all_CourseInfos()
            if len(infos) > 0:
                i = infos[0]
                self.last_year = i.year
                self.last_course_identifier = i.identifier
                self.last_semester = i.semester
            else:
                self.last_year = datetime.date.today().year

            self.write_json()

    def load_json(self):
        for k, v in json.load(SETTINGS_LOCATION):
            setattr(self, k, v)

    def write_json(self):
        json.dump(vars(self), SETTINGS_LOCATION)
