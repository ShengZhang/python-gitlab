#!/usr/bin/python
# usage example: python python_branch_history.py "2017 3 22 23 40"
#
import base64
import datetime
import os
import gitlab
import sys

def main():
    # token authentication from config file
    gl = gitlab.Gitlab.from_config(config_files=['/Users/victorzhang/.python-gitlab.cfg'])

    # projects 
    # Note: difference among gl.projects.list() / gl.projects.list(all=True) / gl.projects.owned() 
    projects = gl.projects.list(all=True)
    print('all projects count: ' + str(len(projects)))
    print('all projects name - ')
    project_release_branches = []

    for project in projects:
        # use try/except to avoid script exit from exception when there's no 'release' branch
        try:
            print('  '+ project.name)
            project_release_branch = project.branches.get('release')
        except Exception:
            project_release_branch = None

        if project_release_branch is not None : 
            latest_comitted_date = project_release_branch.commit['committed_date']
            project_release_branches.append({'name':project.name, 'latest_modified':latest_comitted_date})


    # Sort branches by modified time 
    project_release_branches.sort(key=lambda r: r['latest_modified'], reverse=True)

    # print result
    export(project_release_branches)

def export(branches):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "release_branches.md"
    abs_file_path = os.path.join(script_dir, rel_path)
    temp_argv_list = sys.argv[1].split()
    year   = int(temp_argv_list[0])
    month  = int(temp_argv_list[1])
    day    = int(temp_argv_list[2])
    hour   = int(temp_argv_list[3])
    minute = int(temp_argv_list[4])
    valid_date = unicode(datetime.datetime(year,month,day,hour,minute))

    print('\n')
    print('projects (have release branch) - ')

    with open(abs_file_path, mode="w") as out_file:
        out_file.write("|Project name|release branch latest modified time|Release or not(Yes/No)|\n")
        out_file.write("|---|---|---|\n")
        for branch in branches:
            project_name = branch['name']
            latest_modified = branch['latest_modified']
            release_or_not = 'Yes'

            if latest_modified < valid_date:
                release_or_not = 'No'

            print('  project name:  ' + project_name + ' | ' + 'release branch latest modified time: ' + latest_modified + ' | ' + 'Release or not(Yes/No) : ' + release_or_not )

            out_file.write("|")
            out_file.write(project_name)
            out_file.write("|")
            out_file.write(latest_modified)
            out_file.write("|")
            out_file.write(release_or_not)
            out_file.write("|")
            out_file.write("|\n")

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        main()
    else:
        print('wrong arguments number(2 arguments)!')
    
    