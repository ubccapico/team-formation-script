# -*- coding: utf-8 -*-
import sys
import click

from team_formation import config
from team_formation.data_helpers import process_canvas_courses, \
    process_canvas_group_categories

def course_prompt(canvas):
    courses = canvas.get_courses(
        enrollment_type='teacher',
        enrollment_state='active',
        per_page=config.PER_PAGE,
        include=['sections', 'total_students']
    )

    #fetch all courses (unwrap PaginatedList)
    courses = [course for course in courses]
    course_ids = [course.id for course in courses]

    # save courses data
    process_canvas_courses(courses)

    if len(courses) == 0:
        click.echo('No active courses found for token...')
        sys.exit()

    format_width = len(str(max(course_ids)))

    click.echo("Select one of the following courses:")
    for course in courses:
        click.echo("[{:{width}}]: {} (sections: {}, students: {})".format(
            course.id,
            course.name,
            len(course.sections),
            course.total_students,
            width=format_width
        ))

    while True:
        result = click.prompt("Enter the course id", type=int)
        if result in course_ids:
            return result
        else:
            click.echo("Invalid course id")

def group_name_prompt(course, group_category_name):
    # prompt for group category if needed
    if not group_category_name or not group_category_name.strip():
        while True:
            result = click.prompt("Enter a new group category name", type=str)
            result = result.strip()
            if result:
                group_category_name = result
                break
            else:
                click.echo("Invalid group name")

    # check if group category already exists
    group_categories = course.get_group_categories()
    process_canvas_group_categories(group_categories)

    for group_category in group_categories:
        if group_category_name == group_category.name:
            if click.confirm("Group category name already in use. Would you like to overwrite it?"):
                return (group_category_name, group_category)
            else:
                click.echo('Try again with a different group category name')
                sys.exit()

    return (group_category_name, None)