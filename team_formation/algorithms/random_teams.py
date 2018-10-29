from team_formation.algorithms.base import BaseTeams
import math
import random

class RandomTeams(BaseTeams):
    def __init__(self, data, group_all_sections, total_teams=None, team_size=None):
        BaseTeams.__init__(self, data, group_all_sections, total_teams, team_size)

        if not self.total_teams and not self.team_size:
            raise Exception('Random team algorithm requires number of teams or students in a team')

    def _form_teams(self, students_df):
        number_of_students = len(students_df.index)
        team_sizes = self.get_team_sizes(number_of_students)

        teams = []
        for team_size in team_sizes:
            # get team members though pandas sample
            team = students_df.sample(n=team_size)
            students_df = students_df.drop(team.index)

            teams.append(team)

        # randomize team order
        random.shuffle(teams)

        return teams