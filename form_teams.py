# -*- coding: utf-8 -*-
import requests
import canvasapi
import click

from team_formation.prompts import group_name_prompt
from fetch_data import _fetch_data
from team_formation import config
from team_formation.algorithms.random_teams import RandomTeams
from team_formation.data_helpers import store_teams_generated

@click.command()
@click.option('--test_run',
    help='If flag is present, teams will not be pushed back to Canvas',
    is_flag=True,
    envvar='CANVAS_TEST_RUN')
@click.option('--store_data',
    default=False,
    is_flag=True,
    help='Store data fetched into `.csv` files. [default: False]',
    envvar='CANVAS_STORE_DATA_LOCALLY')
@click.option('--team_size',
    help='Total number of students per team desired.',
    type=int,
    envvar='CANVAS_TEAM_SIZE')
@click.option('--total_teams',
    help='Total number of teams desired. Each course section will have this many teams unless `group_all_sections` is enabled',
    type=int,
    envvar='CANVAS_TOTAL_TEAMS')
@click.option('--strategy',
    help='Select a team formation strategy.',
    type=click.Choice(config.STRATEGIES),
    default='random',
    envvar='CANVAS_GROUP_STRATEGY')
@click.option('--group_category_name',
    help='Name for new Canvas Group Category.',
    type=str,
    envvar='CANVAS_GROUP_CATEGORY_NAME')
@click.option('--group_all_sections',
    help='Group students across different course sections (default False).',
    is_flag=True,
    envvar='CANVAS_GROUP_ALL_SECTIONS')
@click.option('--course_id',
    help='Canvas Course ID.',
    type=int,
    envvar='CANVAS_COURSE_ID')
@click.option('--token',
    prompt=True,
    hide_input=True,
    help='Canvas API token.',
    required=True,
    envvar='CANVAS_API_TOKEN')
@click.option('--url',
    default='https://canvas.ubc.ca',
    help='Canvas Url. [default: https://canvas.ubc.ca]',
    required=True,
    envvar='CANVAS_BASE_URL')
def form_teams(url, token, course_id, group_all_sections, group_category_name,
               strategy, total_teams, team_size, store_data, test_run):
    config.STORE_DATA_LOCALLY = store_data

    canvas = canvasapi.Canvas(url, token)

    (course, data) = _fetch_data(url, token, course_id)

    (group_category_name, group_category) = group_name_prompt(course, group_category_name)

    teams = None
    if strategy.lower() == 'random':
        random_teams = RandomTeams(
            data,
            group_all_sections=group_all_sections,
            total_teams=total_teams,
            team_size=team_size
        )
        teams = random_teams.form_teams()
    else:
        click.echo('Invalid strategy')
        import sys
        sys.exit()

    if len(teams) == 0:
        click.echo('No Teams could be generated')
        import sys
        sys.exit()

    store_teams_generated(teams)

    # only push new group category and teams to canvas if a real run
    if not test_run:
        if not group_category:
            # create new group category
            group_category = course.create_group_category(
                group_category_name
            )
        else:
            # remove existing groups
            groups = group_category.get_groups()
            for group in groups:
                group.delete()

        # push teams to canvas
        for (group_name, students_df) in teams:
            # create group
            group = group_category.create_group(
                name=group_name,
                join_level='invitation_only'
            )

            # add members to group
            group.edit(members=students_df['id'].values)


if __name__ == '__main__':
    form_teams()