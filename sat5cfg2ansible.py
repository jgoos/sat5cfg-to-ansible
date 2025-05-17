#!/usr/bin/env python3
import json
import yaml
from jinja2 import Template
import os
import sys
import magic
import csv

if len(sys.argv) < 2:
    print(f"usage: {os.path.basename(sys.argv[0])} <input_dir>")
    sys.exit(1)

VERBOSE = False
INPUT_DIR = sys.argv[1]
OUTPUT_DIR = INPUT_DIR + "/" + "transformed_files"
WORKDIR = OUTPUT_DIR + "/roles"
ROLE_AUTHOR_NAME = "<change me>"

all_files = []
json_files = []

try:
    all_files = os.listdir(INPUT_DIR)
except FileNotFoundError as e:
    print(e)

for file in all_files:
    if os.path.isfile(INPUT_DIR + "/" + file) and file.endswith(".json"):
        json_files.append(file)

if not json_files:
    print("No json files found")

for file in json_files:
    # strip json from filename
    AnsibleRoleName = os.path.splitext(file)[0]
    if VERBOSE:
        print("Creating role: {} with file: {} as input".format(AnsibleRoleName,file))
    RoleDirectory = WORKDIR + '/' + AnsibleRoleName
    PlaybookDirectory = OUTPUT_DIR + '/playbooks'

    for d in RoleDirectory, PlaybookDirectory:
        try:
            if not os.path.exists(d):
                os.makedirs(d)
        except OSError as e:
            print(e)

    # Create ansible directories for role
    DirsToCreate = ["tasks","files","meta"]
    for d in DirsToCreate:
        try:
            to_create = RoleDirectory + '/' + d
            if not os.path.exists(to_create):
                os.makedirs(to_create)
        except OSError as e:
            print(e)

    with open(INPUT_DIR + "/" + file, 'r') as json_file:
        data = json.load(json_file)

        # Create meta.yml
        ROLE_DESCRIPTION = data[0]['description'].replace("\n", " ")

        with open('templates/meta.j2') as f:
            tmpl = Template(f.read())
            meta_tmpl_processed = tmpl.render(role_author_name = ROLE_AUTHOR_NAME, role_description = ROLE_DESCRIPTION)

            AnsibleFileToWrite = RoleDirectory + "/meta/main.yml"
            with open(AnsibleFileToWrite, 'w') as yaml_file:
                yaml_file.write(meta_tmpl_processed)

        # Create playbook
        with open('templates/playbook.j2') as f:
            tmpl = Template(f.read())
            playbook_tmpl_processed = tmpl.render(role_name = AnsibleRoleName, role_description = ROLE_DESCRIPTION)

            AnsibleFileToWrite = PlaybookDirectory + "/" + AnsibleRoleName + ".yml"
            with open(AnsibleFileToWrite, 'w') as yaml_file:
                yaml_file.write(playbook_tmpl_processed)

        # Create README
        with open('templates/README.j2') as f:
            tmpl = Template(f.read())
            readme_tmpl_processed = tmpl.render(role_name = AnsibleRoleName, role_description = ROLE_DESCRIPTION)

            AnsibleFileToWrite = RoleDirectory + "/README.md"
            with open(AnsibleFileToWrite, 'w') as yaml_file:
                yaml_file.write(readme_tmpl_processed)

        for i in data[0]['files']:
            # DIRECTORY ACTIONS
            if i['type'] == 'directory':
                DIRECTORY_DESTINATION = i['path']
                TASK_DESCRIPTION = "Create directory " + DIRECTORY_DESTINATION
                DIRECTORY_MODE = i['permissions']
                DIRECTORY_OWNER = i['owner']
                DIRECTORY_GROUP = i['group']

                create_directory_template = [
                    {
                        "name": TASK_DESCRIPTION,
                        "ansible.builtin.file": {
                            "path": DIRECTORY_DESTINATION,
                            "state": 'directory',
                            "mode": DIRECTORY_MODE,
                            "owner": DIRECTORY_OWNER,
                            "group": DIRECTORY_GROUP,

                        },
                        "tags": [
                            "directories"
                            ]
                    }
                ]
                AnsibleFileToWrite = RoleDirectory + "/tasks/main.yml"
                with open(AnsibleFileToWrite, 'a') as yaml_file:
                    configuration = yaml.dump(create_directory_template, yaml_file, sort_keys=False)

        # CSV file
        CSV_FILE_PATH = RoleDirectory + "/" + AnsibleRoleName + "_checklist.csv"
        csv_file = open(CSV_FILE_PATH, 'w', newline='')
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["Configuration Channel", "File Path", "File Name", "Type", "Status", "Comment", "Duplicate", "Satellite Variable", "Sensitive Data"])

        for i in data[0]['files']:
            # FILE ACTIONS
            if i['type'] == 'file':

                dirname = os.path.dirname(i['path'])
                basename = os.path.basename(i['path'])

                FILE_CONTENT = i['contents'].encode('ascii', 'ignore').decode('ascii')

                FileToWrite = RoleDirectory + "/files/" + basename

                magic_config = magic.Magic(uncompress=False)
                magic_filetype_found = magic_config.from_buffer(FILE_CONTENT)
                magic_filetype_fixed = magic_filetype_found.replace(';', ' |')
                writer.writerow([AnsibleRoleName, dirname, basename, magic_filetype_fixed, "", "", "", "", ""])

                with open(FileToWrite, "w") as f:
                    f.write(FILE_CONTENT)

                FILE_NAME = basename
                TASK_DESCRIPTION = "Copy file " + FILE_NAME
                FILE_DESTINATION = i['path']
                FILE_MODE = i['permissions']
                FILE_OWNER = i['owner']
                FILE_GROUP = i['group']

                copy_file_template = [
                    {
                        "name": TASK_DESCRIPTION,
                        "ansible.builtin.copy": {
                            "src": FILE_NAME,
                            "dest": FILE_DESTINATION,
                            "mode": FILE_MODE,
                            "owner": FILE_OWNER,
                            "group": FILE_GROUP,
                            "backup": True

                        },
                        "tags": [
                            "files"
                            ]
                    }
                ]

                AnsibleFileToWrite = RoleDirectory + "/tasks/main.yml"
                with open(AnsibleFileToWrite, 'a') as yaml_file:
                    configuration = yaml.dump(copy_file_template, yaml_file, sort_keys=False)

        csv_file.close()

        for i in data[0]['files']:
            # SYMLINK ACTIONS
            if i['type'] == 'symlink':
                SYMLINK_SOURCE = i['path']
                SYMLINK_DESTINATION = i['target_path']
                TASK_DESCRIPTION = "Create symlink " + SYMLINK_DESTINATION

                create_symlink_template = [
                    {
                        "name": TASK_DESCRIPTION,
                        "ansible.builtin.file": {
                            "src": SYMLINK_SOURCE,
                            "dest": SYMLINK_DESTINATION,
                            "state": 'link'
                        },
                        "tags": [
                            "symlinks"
                            ]
                    }
                ]
                AnsibleFileToWrite = RoleDirectory + "/tasks/main.yml"
                with open(AnsibleFileToWrite, 'a') as yaml_file:
                    configuration = yaml.dump(create_symlink_template, yaml_file, sort_keys=False)
