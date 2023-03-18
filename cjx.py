import argparse
import json
import os
import subprocess


class CJX:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.parser = argparse.ArgumentParser(prog='cjx')
        self.subparsers = self.parser.add_subparsers(dest='command')
        self.create_parser = self.subparsers.add_parser('create', help='Create a new JavaFX project')
        self.create_subparsers = self.create_parser.add_subparsers(dest='project_type')
        self.simple_parser = self.create_subparsers.add_parser('simple', help='Create a simple JavaFX project')
        self.simple_parser.add_argument('project_name', help='Name of the JavaFX project')
        self.setup_parser = self.subparsers.add_parser('setup', help='Setting up environment for JavaFX development')
        self.setup_parser.add_argument('sdk_path', help='Path of the JavaFX SDK')
        self.doctor_parser = self.subparsers.add_parser('doctor', help='checks if the necessary pre-requisites are installed')
        self.args = None

    def run(self):
        self.parse_args()
        self.handle_command()

    def parse_args(self):
        self.args = self.parser.parse_args()

    def handle_command(self):
        command = self.args.command
        if command == 'create':
            self.handle_create_command()
        elif command == 'setup':
            self.handle_setup_command()
        elif command == 'doctor':
            self.handle_doctor_command()
        else:
            raise Exception(f'Invalid command: {command}')

    def handle_create_command(self):
        if self.args.project_type == 'simple':
            print(f'Creating simple JavaFX project {self.args.project_name}...')
            self.create_directory(self.args.project_name)
        else:
            raise Exception('Invalid project type')

    def handle_setup_command(self):
        if os.path.exists(self.args.sdk_path):
            print('JavaFX SDK found')
            self.set_sdk_path(self.args.sdk_path)
        else:
            print('JavaFX SDK not found')

    def handle_doctor_command(self):
        print('I am the doctor')
        print('Checking if Java is installed')
        if os.system('java -version') == 0:
            print('Java is installed ✔️')
        else:
            print('Java is not installed ❌')
        print('Checking if JavaFX is setup')
        with open('bin/constants.json', 'r') as f:
            constants = json.load(f)
        if os.path.exists(constants['javafxPath']):
            print('JavaFX is setup ✔️')
        else:
            print('JavaFX is not setup ❌')

    def set_sdk_path(self, sdk_path):
        with open('bin/constants.json', 'r') as f:
            constants = json.load(f)
        constants['javafxPath'] = sdk_path
        constants['jarPath'] = sdk_path + '/lib'
        with open('bin/constants.json', 'w') as f:
            json.dump(constants, f, indent=4)

    def create_directory(self, project_name):
        new_folder = os.path.join(self.current_dir, f'{project_name}')
        if not os.path.exists(new_folder):
            print(f'Creating directory {project_name}')
            os.mkdir(new_folder)
            os.chdir(new_folder)
            subprocess.run(['git', 'init'])
            self.create_gitignore(project_name)
            self.create_readme(project_name)
        else:
            print('Project already exists')

    def create_gitignore(self, project_name):
        os.chdir(self.current_dir)
        with open('src/simple/.gitignore', 'r') as f:
            git_ignore = f.read()
        os.chdir(project_name)
        print('Creating .gitignore file')
        with open('.gitignore', 'w') as f:
            f.write(git_ignore)
        self.vscode_folder(project_name)

    def create_readme(self, project_name):
        os.chdir(self.current_dir)
        print('Creating README.md file')
        with open('src/simple/README.md') as f:
            readme = f.read()
        
        readme = readme.replace('project_name', project_name)

        os.chdir(project_name)

        with open('README.md', 'w') as f:
            f.write(readme)

    def vscode_folder(self,project_name):
        # create .vscode folder
        os.chdir(self.current_dir)
        os.chdir(project_name)
        os.mkdir('.vscode')
        self.create_launch_json()
        self.create_settings_json()


    def create_launch_json(self):
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


    def create_settings_json(self):
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

        self.create_bin_folder()
        self.create_src_folder()

    def create_bin_folder(self):
        print('Creating bin folder')
        os.mkdir('bin')

    def create_src_folder(self):
        print('Creating src folder')
        os.mkdir('src')
        os.chdir('src')

        self.create_src_files()

    def create_src_files(self):
        print('Creating src files')
        with open('../../src/simple/src/App.java', 'r') as f:
            app = f.read()

        with open('App.java', 'w') as f:
            f.write(app)

if __name__ == '__main__':
    CJX().run()
