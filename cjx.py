import argparse
import json
import os
import subprocess


current_dir = os.getcwd()


def main():
    parser = argparse.ArgumentParser(prog='cjx')
    subparsers = parser.add_subparsers(dest='command')

    create_parser = subparsers.add_parser(
        'create', help='Create a new JavaFX project')
    create_subparsers = create_parser.add_subparsers(dest='project_type')

    simple_parser = create_subparsers.add_parser(
        'simple', help='Create a simple JavaFX project')
    simple_parser.add_argument(
        'project_name', help='Name of the JavaFX project')

    setup_parser = subparsers.add_parser(
        'setup', help='Setting up environment for JavaFX development')
    setup_parser.add_argument('sdk_path', help='Path of the JavaFX SDK')

    args = parser.parse_args()
    create_javafx_app(args)


def create_javafx_app(args):
    if args.command == 'create':
        if args.project_type == 'simple':
            print(f'Creating simple JavaFX project {args.project_name}...')
            create_directory(args.project_name)
        else:
            raise Exception('Invalid project type')
    elif args.command == 'setup':
        if os.path.exists(args.sdk_path):
            print('JavaFX SDK found')
            set_sdk_path(args.sdk_path)
        else:
            print('JavaFX SDK not found')


def create_directory(project_name):
    # Get current working directory
    current_dir = os.getcwd()

    # Create new folder in current directory if it doesn't exist
    new_folder = os.path.join(current_dir, f'{project_name}')
    if not os.path.exists(new_folder):
        print(f'Creating directory {project_name}')
        os.mkdir(new_folder)
        os.chdir(new_folder)
        subprocess.run(['git', 'init'])
        create_gitignore(project_name)
        create_readme(project_name)
    else:
        print('Project already exists')


def create_gitignore(project_name):

    os.chdir(current_dir)

    with open('src/simple/.gitignore', 'r') as f:
        git_ignore = f.read()

    os.chdir(project_name)

    print('Creating .gitignore file')

    with open('.gitignore', 'w') as f:
        f.write(git_ignore)

    vscode_folder(project_name)


def create_readme(project_name):

    os.chdir(current_dir)

    print('Creating README.md file')
    with open('src/simple/README.md', 'r') as f:
        readme = f.read()

    readme = readme.replace('project_name', project_name)

    os.chdir(project_name)

    with open('README.md', 'w') as f:
        f.write(readme)

    print('Done!')



def vscode_folder(project_name):
    # create .vscode folder
    os.chdir(current_dir)
    os.chdir(project_name)
    os.mkdir('.vscode')
    create_launch_json()
    create_settings_json()


def create_launch_json():
    print('Creating launch.json file')
    with open('../src/simple/.vscode/launch.json', 'r') as f:
        launch = json.load(f)

    with open('../bin/constants.json', 'r') as f:
        constants = json.load(f)

    module_path = constants['javafxPath'] + '/lib'

    for config in launch['configurations']:
        config['vmArgs'] = f"--module-path \"{module_path}\" --add-modules javafx.controls,javafx.fxml"

    with open('.vscode/launch.json', 'w') as f:
        json.dump(launch, f, indent=4)


def create_settings_json():
    print('Creating settings.json file')
    with open('../src/simple/.vscode/settings.json', 'r') as f:
        settings = json.load(f)

    with open('../bin/constants.json', 'r') as f:
        constants = json.load(f)

    jar_path = constants['jarPath']

    # files = os.listdir(jar_path)

    settings_filled = settings["java.project.referencedLibraries"] = []
    settings_filled.append("lib/**/*.jar")
  
    for jarfiles in constants['jarFiles']:
        if not jarfiles.endswith('.jar'):
            continue
        settings_filled.append(f"{jar_path}/{jarfiles}")



    with open('.vscode/settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

    create_bin_folder()
    create_src_folder()

def create_bin_folder():
    print('Creating bin folder')
    os.mkdir('bin')

def create_src_folder():
    print('Creating src folder')
    os.mkdir('src')
    os.chdir('src')

    create_src_files()

def create_src_files():
    print('Creating src files')
    with open('../../src/simple/src/App.java', 'r') as f:
        app = f.read()

    with open('App.java', 'w') as f:
        f.write(app)


def set_sdk_path(sdk_path):
    with open('bin/constants.json', 'r') as f:
        constants = json.load(f)

    constants['javafxPath'] = sdk_path
    constants['jarPath'] = sdk_path + '/lib'

    with open('bin/constants.json', 'w') as f:
        json.dump(constants, f, indent=4)


if __name__ == '__main__':
    main()
