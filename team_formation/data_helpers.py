# -*- coding: utf-8 -*-
import pandas
import os

from team_formation import config
from team_formation.io import get_root_folder, format_filename, get_output_folder

def process_canvas_course(course):
    course_df = pandas.DataFrame([course.attributes])

    if config.STORE_DATA_LOCALLY:
        file_path = "{}/course.csv".format(get_root_folder())
        course_df.to_csv(file_path, index=False)

    return course_df

def process_canvas_courses(courses):
    courses_df = pandas.DataFrame([course.attributes for course in courses])

    if config.STORE_DATA_LOCALLY:
        file_path = "{}/courses.csv".format(get_root_folder())
        courses_df.to_csv(file_path, index=False)

    return courses_df

def process_canvas_sections(sections):
    section_data = []
    for section in sections:
        data = section.attributes
        data['students'] = pandas.DataFrame(data['students'])
        section_data.append(data)

    sections_df = pandas.DataFrame(section_data)

    if config.STORE_DATA_LOCALLY:
        file_path = "{}/sections.csv".format(get_root_folder())
        sections_without_students_df = sections_df.drop(columns=['students'])
        sections_without_students_df.to_csv(file_path, index=False)

        for index, section in sections_df.iterrows():
            file_path = "{}/section_{}_students.csv".format(get_root_folder(), section['id'])
            section['students'].to_csv(file_path, index=False)

    return sections_df

def process_canvas_students(students):
    students_df = pandas.DataFrame([student.attributes for student in students])

    if config.STORE_DATA_LOCALLY:
        file_path = "{}/students.csv".format(get_root_folder())
        students_df.to_csv(file_path, index=False)

    return students_df

def process_canvas_group_categories(group_categories):
    group_categories_df = pandas.DataFrame([group_category.attributes for group_category in group_categories])

    if config.STORE_DATA_LOCALLY:
        file_path = "{}/group_categories.csv".format(get_root_folder())
        group_categories_df.to_csv(file_path, index=False)

    return group_categories_df


def store_teams_generated(teams):
    if config.STORE_DATA_LOCALLY:
        folder_path = get_output_folder()

        for (group_name, students_df) in teams:
            file_path = "{}/{}.csv".format(folder_path, format_filename(group_name))
            students_df.to_csv(file_path, index=False)
