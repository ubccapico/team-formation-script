from abc import ABCMeta, abstractmethod, abstractproperty
import math

class BaseTeams:
    __metaclass__ = ABCMeta

    def __init__(self, data, group_all_sections, total_teams=None, team_size=None):
        self.data = data
        self.group_all_sections = group_all_sections
        # by default allow both total_teams and team_size
        # to be None since an algorithm could potentially figure out optimum
        # team sizes though the data somehow
        self.total_teams = total_teams
        self.team_size = team_size

        if total_teams and total_teams <= 0:
            raise Exception('total_teams must be 1 or greater')

        if team_size and team_size <= 0:
            raise Exception('team_size must be 1 or greater')

        self.student_section_buckets = []
        if group_all_sections:
            self.student_section_buckets.append(
                (None, self.data['students_df'])
            )
        else:
            # Note if students are in more than one section for some reason
            # they will be put into a team for only the first section
            students_df = self.data['students_df']
            for index, section in data['sections_df'].iterrows():
                section_student_ids = section['students']['id'].values

                # filter active students by section students
                # section students may contain invited/inactive students
                team_df = students_df[students_df['id'].isin(section_student_ids)]

                # remove students from students_df so they are not added to
                # groups in multiple sections (if they are in multiple sections somehow)
                students_df.drop(team_df.index)
                students_df = students_df.drop(team_df.index)
                self.student_section_buckets.append(
                    (section['name'], team_df)
                )

    # return array of tuples (group_name, student_df)
    def form_teams(self):
        teams = []
        for section_name, students_df in self.student_section_buckets:
            section_teams = self._form_teams(students_df)
            for index, students_df in enumerate(section_teams):
                teams.append(
                    (self._group_name(section_name, index), students_df),
                )
        return teams

    @abstractmethod
    def _form_teams(self, student_bucket):
        pass

    def _get_total_teams(self, number_of_students):
        if self.total_teams:
            return self.total_teams
        elif self.team_size:
            if self.team_size >= number_of_students:
                return 1
            return int(math.ceil(float(number_of_students) / float(self.team_size)))
        else:
            raise Exception('team_size or total_teams required for this algorithm')

    def get_team_sizes(self, number_of_students):
        team_sizes = []

        number_of_teams = self._get_total_teams(number_of_students)

        for i in range(number_of_students):
            if i < number_of_teams:
                team_sizes.append(1)
            else:
                team_sizes[i % number_of_teams] += 1

        return team_sizes

    def _group_name(self, section_name, index):
        if section_name:
            return "{} Group {}".format(section_name, index+1)
        return "Group {}".format(index+1)

