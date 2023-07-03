import click
import pandas as pd
import numpy as np
import urllib
import json
import os
import things

@click.group("import_project")
def import_project():
    pass

@import_project.command('import_asana')
@click.argument('path_to_csv', type=click.Path(exists=True))
@click.option('--name', type=str, default=None)
def import_asana(path_to_csv: str, name: str = None):
    name = name if name is not None else path_to_csv.strip(".csv")

    # check if project exists
    for project in things.projects():
        if project["title"] == name:
            print(f'Project {name} already exists. Delete it first —-- this function will overwrite existing projects.')
            # return

    print(f'Importing project {name} from {path_to_csv}...')
    project = pd.read_csv(path_to_csv)
    project["completion-date"] = pd.to_datetime(project["Completed At"]).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    items = []
    headings = {}
    for i, reminder in project.iterrows():
        attributes = {
            "title": reminder["Name"],
            "completed": not pd.isna(reminder["Completed At"])
        }
        if not pd.isna(reminder["Completed At"]):
            attributes["completion-date"] = reminder["completion-date"]
        if not pd.isna(reminder["Notes"]):
            attributes["notes"] = reminder["Notes"]
        if not pd.isna(reminder["Due Date"]):
            attributes["when"] = reminder["Due Date"]
            attributes["deadline"] = reminder["Due Date"]
        if not (reminder["Section/Column"] == "(no section)" or pd.isna(reminder["Section/Column"])):
            attributes["heading"] = reminder["Section/Column"]
            if reminder["Section/Column"] not in headings.keys():
                headings[reminder["Section/Column"]] = {
                    "type": "heading",
                    "attributes": {
                        "title": reminder["Section/Column"]
                    }
                }
        items.append({
            "type": "to-do",
            "attributes": attributes
        })
    
    print(headings)
    print(items[-1])

    # test post
    post_to_things([
        {
            "type": "project",
            "attributes": {
                "title": name,
                "items": list(headings.values()) + items
            }
        }
    ])


def post_to_things(data):
    url = "things:///json?data="
    token = json.load(open('token.json'))['token']
    print(json.dumps(data))
    uri = url + urllib.parse.quote(json.dumps(data))
    os.system(f"open {uri}")


if __name__ == "__main__":
    import_project()
