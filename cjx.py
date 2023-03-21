import argparse
import json
import os
import subprocess
from simple import Simple

class CJX:    
    def __init__(self):
            self.parser = argparse.ArgumentParser(prog='cjx', description='CJX CLI', usage='%(prog)s [command] [options]')
            self.subparsers = self.parser.add_subparsers(dest='command')
            self.doctor_parser = self.subparsers.add_parser('doctor', help='checks if the necessary pre-requisites are installed')
            self.init_parser = self.subparsers.add_parser('init', help='initializes the CJX CLI')
            self.path_parser = self.subparsers.add_parser('set-path', help='sets the path of the CJX CLI')
            self.setup_parser = self.subparsers.add_parser('setup', help='Setting up environment for JavaFX development')
            self.setup_parser.add_argument('sdk_path', help='Path of the JavaFX SDK')
            self.create_parser = self.subparsers.add_parser('create', help='Create a new JavaFX project')
            self.create_subparsers = self.create_parser.add_subparsers(dest='project_type')
            self.simple_parser = self.create_subparsers.add_parser('simple', help='Create a simple JavaFX project')
            self.simple_parser.add_argument('project_name', help='Name of the JavaFX project')
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

    def cjx_logo(self):
        print('''
         ___    _____  _    _     ___    _      _ 
        (  _ \ (___  )( )  ( )   (  _ \ ( )    (_)
        | ( (_)    | | \ \/ /    | ( (_)| |    | |
        | |  _  _  | |  )  (     | |  _ | |  _ | |
        | (_( )( )_| | / /\ \    | (_( )| |_( )| |
        (____/  \___/ ( )  (_)   (____/ ((___/ (_)
                      /(                (_)       
                     (__)                         
        ''')
        
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
                    self.set_cjx_path()
            else:
                print("Error: CJX CLI not initialized")
        elif command is None:
            self.cjx_logo()
            self.parser.print_help()
        else:
            print(f'Error: Invalid command: {command}')  

    def handle_create_command(self):
        if self.args.project_type == 'simple':
            self.project_name = self.args.project_name
            print(f'\n\tCreating simple JavaFX project {self.project_name}\n')
            Simple.handle_simple(self)
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

        check4 = "Checking if Visual Studio Code is installed: "
        result4 = ""
        command = "code -v"
        try:
            subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
            result4 = "\033[1mVisual Studio Code is installed ✔️\033[0m"
        except subprocess.CalledProcessError:
            result4 = "\033[1mVisual Studio Code is not installed ❌\033[0m"
        print("{}{}".format(check4, result4))

        check2 = "Checking if CJX CLI path is set: "
        result2 = ""
        
        with open(self.cjx_path, 'r') as f:
            path = json.load(f)

        if path['cjxPath'] != "":
            result2 = "\033[1mCJX CLI path is set ✔️\033[0m"
        else:
            result2 = "\033[1mCJX CLI path is not set ❌\033[0m"

        print("{}{}".format(check2, result2))

        check3 = "Checking if JavaFX is setup: "
        result3 = ""
        try:

            with open(self.cjx_path, 'r') as f:
                path = json.load(f)

            utils_path_json = f"{path['cjxPath']}/utils/utils_path.json"

            try:
                with open(utils_path_json, 'r') as f:
                    utils_path = json.load(f)
                if os.path.exists(utils_path['javafxPath']):
                    result3 = "\033[1mJavaFX is setup ✔️\033[0m"
                else:
                    result3 = "\033[1mJavaFX is not setup ❌\033[0m"
            except:
                result3 = "\033[1mJavaFX is not setup, because CJX CLI path is not set ❌\033[0m"

        except:
            result3 = "\033[1mError checking JavaFX Setup\033[0m"
        
        print("{}{}".format(check3, result3))

    def set_cjx_path(self):
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

if __name__ == '__main__':
    CJX().run()