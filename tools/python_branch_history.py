import base64
import time
import os
import gitlab

def main():
    # token authentication from config file
    gl = gitlab.Gitlab.from_config(config_files=['/Users/victorzhang/.python-gitlab.cfg'])

    # projects 
    # Note: difference among gl.projects.list() / gl.projects.list(all=True) / gl.projects.owned() 
    projects = gl.projects.list(all=True)

    project_release_branches = []

    for project in projects:
        # use try/except to avoid script exit from exception when there's no 'release' branch
        try:
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
    with open(abs_file_path, mode="w") as out_file:
        out_file.write("|Project name|release branch latest modified time|\n")
        out_file.write("|---|---|\n")
        for branch in branches:
            project_name = branch['name']
            latest_modified = branch['latest_modified']

            print(' project name:  ' + project_name + ' | ' + 'release branch latest modified time: ' + latest_modified)

            out_file.write("|")
            out_file.write(project_name)
            out_file.write("|")
            out_file.write(latest_modified)
            out_file.write("|")
            out_file.write("|\n")

if __name__ == "__main__":
    main()