import argparse
import json
import os
import subprocess
from app.simple import Simple
from app.jfxml import JFXML


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
            self.jfxml_parser = self.create_subparsers.add_parser('jfxml', help='Create a JavaFX project with FXML')
            self.jfxml_parser.add_argument('project_name', help='Name of the JavaFX project')
            self.args = None
            self.project_name = None
            self.cjx_path = None
            self.package_name = None

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
                print(self.cjx_logo('welcome'))
                print("\t\033[CJX CLI initialized successully 🎉\033[0m") 
                               
            else:
                print("Error: CJX CLI already initialized")
        except Exception as e:
            print(f'Error: {e}')

    def cjx_logo(self,type='main'):
        main = '''
         ___    _____  _    _     ___    _      _ 
        (  _ \ (___  )( )  ( )   (  _ \ ( )    (_)
        | ( (_)    | | \ \/ /    | ( (_)| |    | |
        | |  _  _  | |  )  (     | |  _ | |  _ | |
        | (_( )( )_| | / /\ \    | (_( )| |_( )| |
        (____/  \___/ ( )  (_)   (____/ ((___/ (_)
                      /(                (_)       
                     (__)                         
        '''
        welcome = '''
                        __                                     __          
        __  _  __ ____ |  |   ____   ____   _____   ____     _/  |_  ____  
        \ \/ \/ // __ \|  | _/ ___\ / __ \ /     \_/ __ \    \   __\/ __ \ 
        \     /\  ___/_  |__  \___(  \_\ )  | |  \  ___/_    |  | (  \_\ )
        \/\_/  \___  /____/\___  /\____/|__|_|  /\___  /    |__|  \____/ 
                    \/          \/             \/     \/                  
  
                                ┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃
                                ┃┃┃┃┃┃┃┏┓┃┃┃┃┃┃
                                ┏━━┓┃┃┃┗┛┃┃┃┓┏┓
                                ┃┏━┛┃┃┃┏┓┃┃┃╋╋┛
                                ┃┗━┓┃┃┃┃┃┃┃┃╋╋┓
                                ┗━━┛┃┃┃┃┃┃┃┃┛┗┛
                                ┃┃┃┃┃┃┃┛┃┃┃┃┃┃┃
                                ┃┃┃┃┃┃┃━┛┃┃┃┃┃┃
        '''
        if type == 'welcome':
            return welcome
        
        return main
        
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
        elif self.args.project_type == 'jfxml':
            self.project_name = self.args.project_name
            pak_name = input(f'Enter package name for project {self.project_name} (default: cjx): ')
            self.validity_checker(pak_name)
            print(f'\n\tCreating JavaFX project {self.project_name} with FXML support\n')
            JFXML.handle_jfxml(self)
        else:
            print('Error: Invalid project type')     

    def validity_checker(self,pak_name):
        validinput = False
        while not validinput:
            if pak_name == '':
                self.package_name = 'cjx'
                validinput = True
            else:
                try:
                    self.package_name = pak_name
                    validinput = True
                except ValueError:
                    print('Error: Invalid package name')
                    pak_name = input(f'Enter package name for project {self.project_name} (default: cjx): ')

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

        check4 = "Checking if VS Code is installed: "
        result4 = ""
        command = "code -v"
        try:
            subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
            result4 = "\033[1mVisual Studio Code is installed ✔️\033[0m"
        except subprocess.CalledProcessError:
            result4 = "\033[1mVisual Studio Code is not installed ❌\033[0m"
        print("{}{}".format(check4, result4))

        check5 = "Checking if Git is installed: "
        result5 = ""
        command = "git --version"
        try:
            subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
            result5 = "\033[1mGit is installed ✔️\033[0m"
        except subprocess.CalledProcessError:
            result5 = "\033[1mGit is not installed ❌\033[0m"
        print("{}{}".format(check5, result5))

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
    
    def error_handling(self):
        print("Possible reasons:")
        print("\t1. Project already exists")
        print("\t2. You don't have permission to create a project in this directory")
        print("\t3. You don't have git installed")

if __name__ == '__main__':
    CJX().run()