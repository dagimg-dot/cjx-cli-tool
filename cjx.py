import argparse
import json
import os
import subprocess


class CJX:    
    def __init__(self):
            self.parser = argparse.ArgumentParser(prog='cjx')
            self.subparsers = self.parser.add_subparsers(dest='command')
            self.create_parser = self.subparsers.add_parser('create', help='Create a new JavaFX project')
            self.create_subparsers = self.create_parser.add_subparsers(dest='project_type')
            self.simple_parser = self.create_subparsers.add_parser('simple', help='Create a simple JavaFX project')
            self.simple_parser.add_argument('project_name', help='Name of the JavaFX project')
            self.setup_parser = self.subparsers.add_parser('setup', help='Setting up environment for JavaFX development')
            self.setup_parser.add_argument('sdk_path', help='Path of the JavaFX SDK')
            self.doctor_parser = self.subparsers.add_parser('doctor', help='checks if the necessary pre-requisites are installed')
            self.path_parser = self.subparsers.add_parser('set-path', help='sets the path of the CJX CLI')
            self.init_parser = self.subparsers.add_parser('init', help='initializes the CJX CLI')
            self.args = None
            self.project_name = None
            self.cjx_path = None


    def run(self):
        try:
            self.parse_args()
            self.handle_command()
        except Exception as e:
            print(f'Error: {e}')

    def parse_args(self):
        self.args = self.parser.parse_args()

    def init(self):
        try:
            if not os.path.exists('c:/.cjx'):
                os.chdir('c:/')
                os.mkdir('.cjx')
                os.chdir('.cjx')
                with open('utils_cjx.json', 'w') as f:
                    json.dump({}, f, indent=4)

                with open('utils_cjx.json', 'r') as f :
                    utils_cjx = json.load(f)

                utils_cjx["cjxPath"] = ""

                with open('utils_cjx.json', 'w') as f:
                    json.dump(utils_cjx, f, indent=4)

                print("CJX CLI initialized successfully 🎉")                
            else:
                print("Error: CJX CLI already initialized")
        except Exception as e:
            print(f'Error: {e}')
        

    def handle_command(self):
        command = self.args.command
        if command == 'init':
            self.init()
        elif command in ['create', 'setup', 'doctor', 'set-path']:
            if os.path.exists('c:/.cjx'):
                self.cjx_path = 'c:/.cjx/utils_cjx.json'
                if command == 'create':
                    self.handle_create_command()
                elif command == 'setup':
                    self.handle_setup_command()
                elif command == 'doctor':
                    self.handle_doctor_command()
                elif command == 'set-path':
                    self.set_path()
            else:
                print("Error: CJX CLI not initialized")
        else:
            print(f'Error: Invalid command: {command}')

    def handle_create_command(self):
        if self.args.project_type == 'simple':
            self.project_name = self.args.project_name
            print(f'\n\tCreating simple JavaFX project {self.project_name}...')
            self.create_directory()
        else:
            print('Error: Invalid project type')

    def handle_setup_command(self):
        if not os.path.exists(self.args.sdk_path):
            print('Error: JavaFX SDK not found')
        else:
            print('JavaFX SDK found')
            self.set_sdk_path(self.args.sdk_path)

    def handle_doctor_command(self):
        check1 = "Checking if Java is installed: "
        result1 = ""
        command = "java -version"
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            result1 = "\033[1mJava is installed ✔️\033[0m"
        except subprocess.CalledProcessError:
            result1 = "\033[1mJava is not installed ❌\033[0m"
        print("{}{}".format(check1, result1))

        check3 = "Checking if CJX CLI path is set: "
        result3 = ""
        
        with open(self.cjx_path, 'r') as f:
            path = json.load(f)

        if path['cjxPath'] != "":
            result3 = "\033[1mCJX CLI path is set ✔️\033[0m"
        else:
            result3 = "\033[1mCJX CLI path is not set ❌\033[0m"


        print("{}{}".format(check3, result3))

        check2 = "Checking if JavaFX is setup: "
        result2 = ""
        try:

            with open(self.cjx_path, 'r') as f:
                path = json.load(f)

            utils_path_json = f"{path['cjxPath']}/utils/utils_path.json"

            try:
                with open(utils_path_json, 'r') as f:
                    utils_path = json.load(f)
                if os.path.exists(utils_path['javafxPath']):
                    result2 = "\033[1mJavaFX is setup ✔️\033[0m"
                else:
                    result2 = "\033[1mJavaFX is not setup ❌\033[0m"
            except:
                result2 = "\033[1mJavaFX is not setup, because CJX CLI path is not set ❌\033[0m"

        except:
            result2 = "\033[1mError checking JavaFX Setup\033[0m"
        
        print("{}{}".format(check2, result2))


    def set_path(self):
        if os.path.exists('cjx.exe') or os.path.exists('cjx.py'):
            current_dir = os.getcwd()   
            try:
                with open('c:/.cjx/utils_cjx.json', 'r') as f:
                    path = json.load(f)

                current_dir = current_dir.replace('\\', '/')
                path['cjxPath'] = current_dir

                with open('c:/.cjx/utils_cjx.json', 'w') as f:
                    json.dump(path, f, indent=4)

                print('CJX CLI path set successfully to', current_dir)
            except:
                print('Error setting CJX path, check your current path. It has to be in the same directory as the dependencies folder.')
        else:
            print('Error: CJX executable not found, check your current path. It has to be in the same directory as the cjx executable.')

    def set_sdk_path(self, sdk_path):
        try:
            with open(self.cjx_path, 'r') as f:
                path = json.load(f)

            if path['cjxPath'] == "":
                print('Error: CJX CLI path not set')
            else:
                utils_path_json = f"{path['cjxPath']}/utils/utils_path.json"

                with open(utils_path_json, 'r') as f:
                    utils_path = json.load(f)
                utils_path['javafxPath'] = sdk_path
                utils_path['jarPath'] = sdk_path + '/lib'
                with open(utils_path_json, 'w') as f:
                    json.dump(utils_path, f, indent=4)

                print('JavaFX SDK path set successfully to', sdk_path)
        except:
            print('Error setting JavaFX SDK path')

    def get_cjx_path(self):
        with open(self.cjx_path, 'r') as f:
            path = json.load(f)
        return path['cjxPath']  
        
    def create_directory(self):
        try:
            new_folder = self.project_name
            if not os.path.exists(new_folder):
                print(f'\tCreating directory {self.project_name}\n')
                os.mkdir(new_folder)
                os.chdir(new_folder)
                subprocess.run(['git', 'init'])
                self.create_gitignore()
                self.create_readme()

                print(f'\n\t\033[1mProject {self.project_name} created successfully 🎇\033[0m\n')
                print(f"To open the project in VS Code, type '\033[1mcd {self.project_name}\033[0m', then type '\033[1mcode .\033[0m'\n")
            else:
                print('Project already exists')
        except OSError as e:
            print(f"Error creating directory: {e}")
        
    def create_gitignore(self):
        try:
            print('Creating .gitignore file')
            git_ignore = '''            
# Ignore Visual Studio Code directory
.vscode/

# Ignore compiled binary files
bin/
            '''

            with open('.gitignore', 'w') as f:
                f.write(git_ignore)
            self.vscode_folder()
        except OSError as e:
            print(f"Error creating .gitignore file: {e}")

    def create_readme(self):
        os.chdir('..')
        try:
            print('Creating README.md file')
            with open(f'{self.get_cjx_path()}/src/simple/README.md') as f:
                readme = f.read()
            
            readme = readme.replace('project_name', f"Project Name: {self.project_name}")

            with open('README.md', 'w') as f:
                f.write(readme)
        except OSError as e:
            print(f"Error creating README.md file: {e}")

    def vscode_folder(self):
        try:
            os.mkdir('.vscode')
            self.create_launch_json()
            self.create_settings_json()
        except OSError as e:
            print(f"Error creating .vscode folder: {e}")

    def create_launch_json(self):
        try:
            print('Creating launch.json file')
            with open(f'{self.get_cjx_path()}/src/simple/.vscode/launch.json', 'r') as f:
                launch = json.load(f)

            with open(f'{self.get_cjx_path()}/utils/utils_path.json', 'r') as f:
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
            with open(f'{self.get_cjx_path()}/src/simple/.vscode/settings.json', 'r') as f:
                settings = json.load(f)

            with open(f'{self.get_cjx_path()}/utils/utils_path.json', 'r') as f:
                constants = json.load(f)

            jar_path = constants['jarPath']


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
            with open(f'{self.get_cjx_path()}/src/simple/src/App.java.txt', 'r') as f:
                app = f.read()

            with open('App.java', 'w') as f:
                f.write(app)
        except OSError as e:
            print(f"Error creating src files: {e}")


if __name__ == '__main__':
    CJX().run()