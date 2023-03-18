import argparse
import json
import os
import subprocess
import winreg


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
            self.project_name = None

    def run(self):
        try:
            self.parse_args()
            self.handle_command()
        except Exception as e:
            print(f'Error: {e}')

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
            self.project_name = self.args.project_name
            print(f'Creating simple JavaFX project {self.project_name}...')
            self.create_directory()
        else:
            raise Exception('Invalid project type')

    def handle_setup_command(self):
        if not os.path.exists(self.args.sdk_path):
            raise Exception('JavaFX SDK not found')
        print('JavaFX SDK found')
        self.set_sdk_path(self.args.sdk_path)

    def handle_doctor_command(self):
        check1 = "Checking if Java is installed: "
        command = "java -version"
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            result1 = "\033[1mJava is installed ✔️\033[0m"
        except subprocess.CalledProcessError:
            result1 = "\033[1mJava is not installed ❌\033[0m"
        print("{}{}".format(check1, result1))

        check2 = "Checking if JavaFX is setup: "
        try:
            with open('bin/constants.json', 'r') as f:
                constants = json.load(f)
            if os.path.exists(constants['javafxPath']):
                result2 = "\033[1mJavaFX is setup ✔️\033[0m"
            else:
                result2 = "\033[1mJavaFX is not setup ❌\033[0m"
        except:
            print('Error checking JavaFX setup')
        
        print("{}{}".format(check2, result2))

    def set_sdk_path(self, sdk_path):
        try:
            with open('bin/constants.json', 'r') as f:
                constants = json.load(f)
            constants['javafxPath'] = sdk_path
            constants['jarPath'] = sdk_path + '/lib'
            with open('bin/constants.json', 'w') as f:
                json.dump(constants, f, indent=4)
        except:
            raise Exception('Error setting JavaFX SDK path')
        
    def create_directory(self):
        try:
            new_folder = os.path.join(self.current_dir, f'{self.project_name}')
            if not os.path.exists(new_folder):
                print(f'Creating directory {self.project_name}')
                os.mkdir(new_folder)
                os.chdir(new_folder)
                subprocess.run(['git', 'init'])
                self.create_gitignore()
                self.create_readme()
            else:
                print('Project already exists')
        except OSError as e:
            print(f"Error creating directory: {e}")
        
    def create_gitignore(self):
        try:
            os.chdir(self.current_dir)
            with open('src/simple/.gitignore', 'r') as f:
                git_ignore = f.read()
            os.chdir(self.project_name)
            print('Creating .gitignore file')
            with open('.gitignore', 'w') as f:
                f.write(git_ignore)
            self.vscode_folder()
        except OSError as e:
            print(f"Error creating .gitignore file: {e}")

    def create_readme(self):
        try:
            os.chdir(self.current_dir)
            print('Creating README.md file')
            with open('src/simple/README.md') as f:
                readme = f.read()
            
            readme = readme.replace('project_name', f"Project Name: {self.project_name}")

            os.chdir(self.project_name)

            with open('README.md', 'w') as f:
                f.write(readme)
        except OSError as e:
            print(f"Error creating README.md file: {e}")

    def vscode_folder(self):
        try:
            # create .vscode folder
            os.chdir(self.current_dir)
            os.chdir(self.project_name)
            os.mkdir('.vscode')
            self.create_launch_json()
            self.create_settings_json()
        except OSError as e:
            print(f"Error creating .vscode folder: {e}")

    def create_launch_json(self):
        try:
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
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error creating launch.json file: {e}")

    def create_settings_json(self):
        try:
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
        except Exception as e:
            print(f'Error creating settings.json file: {e}')

    def create_bin_folder(self):
        try:
            print('Creating bin folder')
            os.mkdir('bin')
        except OSError as e:
            print(f"Error creating bin folder: {e}")

    def create_src_folder(self):
        try:
            print('Creating src folder')
            os.mkdir('src')
            os.chdir('src')
            self.create_src_files()
        except OSError as e:
            print(f"Error creating src folder: {e}")


    def create_src_files(self):
        try:
            print('Creating src files')
            # os.chdir(self.current_dir)
            with open('../../src/simple/src/App.java.txt', 'r') as f:
                app = f.read()

            with open('App.java', 'w') as f:
                f.write(app)
        except OSError as e:
            print(f"Error creating src files: {e}")


if __name__ == '__main__':
    CJX().run()