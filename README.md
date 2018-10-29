Team Formation
==========

Introduction
------------
Script for forming team in Canvas. The two scripts provided, `fetch_data.py` and `form_teams.py`, are used to aid in the creation of Canvas groups based on a set of criteria. Currently only random group assignment is available.

### Prerequisites

* [Python 2.7 or 3.4+](https://www.python.org/downloads/)

Install pip libraries
----------

    pip install -r requirements.txt

Fetch Data Script
----------

The fetch data script (`fetch_data.py`) is useful for test fetching information from Canvas/other sources and viewing the collected data (used by the Form Teams Script). It was developed as a separate script to provide an opportunity to evaluate the data available independently of group formation and be easily expanded upon in the future (easier to testing fetch data from different sources, etc).

### Basic usage

    python fetch_data.py

### Options

`--url`: set the base url of the Canvas installation (default: `https://canvas.ubc.ca`)

`--token`: set the Canvas api token. Exact permissions required for the user/token to be determined

`--course_id`: set the Canvas course id to fetch the data for (Optional). If not specified, will be prompted to select from a list all courses the user token has access to.

`--store_data`: set if data fetched should be stored locally (default: False). Useful for exploring available data for developing a group formation strategies but should not be used for general use (since it can store sensitive information).

Form Teams Script
----------

The form team script (`form_teams.py`) will use the fetch data script to collect data from Canvas/other sources and then form teams based on input such as: team formation strategy, desired team size, and desired number of teams. Use the `--test_run` flag to test the team formation script without pushing teams back to Canvas. Currently one of `--team_size` or `--total_teams` must be provided to scope the desired number of groups or size of groups.

### Basic usage

    python form_teams.py --team_size=NUMBER_OF_STUDENTS_PER_TEAM

or

    python form_teams.py --total_teams=TOTAL_NUMBER_OF_TEAMS

### Options

`--url`: set the base url of the Canvas installation (default: `https://canvas.ubc.ca`)

`--token`: set the Canvas api token. Exact permissions required for the user/token to be determined

`--course_id`: set the Canvas course id to fetch the data for (Optional). If not specified, will be prompted to select from a list all courses the user token has access to.

`--group_category_name`: Set the Canvas Group Category name (Optional). If not specified, will be prompted to enter one. If Canvas Group Category name already in use, will be prompted to overwrite the current groups (all old groups will be erased from Group Category).

`--strategy`: set the team formation grouping strategy (default: `random`). Currently only random is supported.

`--group_all_sections`: Will group students together across all sections that the token has access to within the course if present. When present, all students in the course will be grouped together to meet the `team_size` and `total_teams` requirements. When not present, students of each section will be grouped together to meet the `team_size` and `total_teams` requirements independently.

`--total_teams=###`: Total number of teams that will be generated.

`--team_size=###`: Total number of students to assign to each team.

`--store_data`: set if data fetched and teams produce should be stored locally (default: False). Useful for exploring available data and the resulting teams for developing a group formation strategies but should not be used for general use (since it can store sensitive information).

`--test_run`: Will not push Canvas Group Category or groupings back to canvas when flag is present. Useful for testing the group formation script out without

Viewing Data Stored
----------

Each run of either `fetch_data.py` or `form_teams.py` with the `--store_data` flag will create `csv` files of for all data pulled from canvas in the `.data/dump/%Y-%m-%d %H:%M:%S` folder (ex: `.data/dump/2018-02-27 14:15:29`.

The `form_teams.py` script will additionally add an `.data/dump/%Y-%m-%d %H:%M:%S/output` folder containing files for each group's students generated.